<?php
declare(strict_types=1);

require_once __DIR__ . '/bootstrap.php';
require_once __DIR__ . '/mailer.php';

$pdo = gaeks_db();
$input = $_SERVER['REQUEST_METHOD'] === 'POST' ? gaeks_input(131072) : [];
$action = (string) ($_GET['action'] ?? $input['action'] ?? 'me');

function auth_name(string $name): string
{
    $name = trim(preg_replace('/\s+/u', ' ', $name) ?? '');
    if ($name === '' || strlen($name) < 2 || strlen($name) > 160) gaeks_error('invalid_name', 'Nama harus berisi 2–160 karakter.', 422, ['name'=>'invalid']);
    return $name;
}

function auth_password(string $password): string
{
    if (strlen($password) < 8 || strlen($password) > 128) gaeks_error('invalid_password', 'Kata sandi harus berisi 8–128 karakter.', 422, ['password'=>'invalid']);
    return $password;
}

function auth_find_user(PDO $pdo, string $email): ?array
{
    $s=$pdo->prepare('SELECT * FROM users WHERE email_normalized=:email LIMIT 1');$s->execute([':email'=>$email]);$row=$s->fetch();return $row?:null;
}

function auth_login_response(PDO $pdo, array $user, string $provider, bool $created=false): never
{
    $session=gaeks_create_session($pdo,(string)$user['id']);$user['provider']=$provider;
    gaeks_audit($pdo,(string)$user['id'],$created?'auth.registered':'auth.login','user',(string)$user['id'],['provider'=>$provider]);
    gaeks_ok(['user'=>gaeks_user_payload($user),'csrfToken'=>$session['csrfToken'],'expiresAt'=>$session['expiresAt'],'created'=>$created],$created?201:200,$created?'Akun berhasil dibuat.':'Berhasil masuk.');
}

if ($action === 'public_config') {
    gaeks_ok(['googleClientId'=>GOOGLE_CLIENT_ID,'turnstileSiteKey'=>TURNSTILE_SITE_KEY,'billingEnabled'=>BILLING_ENABLED]);
}

if ($action === 'me') {
    $user=gaeks_current_user(false); if(!$user)gaeks_error('unauthenticated','Belum masuk.',401); gaeks_ok(['user'=>gaeks_user_payload($user)]);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') gaeks_error('method_not_allowed','Gunakan metode POST.',405);

if ($action === 'register_request' || $action === 'send_otp') {
    gaeks_rate_limit($pdo,'register_request',5,900);
    gaeks_verify_turnstile((string)($input['captchaToken']??$input['captcha_token']??''));
    $email=gaeks_email((string)($input['email']??''));if(!$email)gaeks_error('invalid_email','Alamat email tidak valid.',422,['email'=>'invalid']);
    $name=auth_name((string)($input['name']??''));
    if(auth_find_user($pdo,$email))gaeks_error('already_registered','Email sudah terdaftar. Silakan masuk.',409);
    $otp=(APP_ENV==='test' && preg_match('/^\d{6}$/',TEST_OTP_CODE))?TEST_OTP_CODE:(string)random_int(100000,999999);$id=gaeks_uuid();$expires=gmdate('Y-m-d H:i:s',time()+OTP_TTL_SECONDS);
    $pdo->prepare("UPDATE otp_challenges SET consumed_at=UTC_TIMESTAMP() WHERE email_normalized=:email AND purpose='register' AND consumed_at IS NULL")->execute([':email'=>$email]);
    $pdo->prepare("INSERT INTO otp_challenges (id,email_normalized,purpose,code_hmac,expires_at,request_ip_hash) VALUES (:id,:email,'register',:code,:expires,:ip)")->execute([':id'=>$id,':email'=>$email,':code'=>gaeks_hash($id.'|'.$email.'|'.$otp),':expires'=>$expires,':ip'=>gaeks_hash(gaeks_client_ip())]);
    $mail=gaeks_send_otp_email($email,$name,$otp); if(empty($mail['ok'])){error_log('OTP mail failed for '.$email);gaeks_error('email_delivery_failed','Kode tidak dapat dikirim. Silakan coba kembali.',503);}
    gaeks_ok(['expiresIn'=>OTP_TTL_SECONDS],200,'Kode verifikasi telah dikirim.');
}

if ($action === 'register_verify' || $action === 'verify_otp') {
    gaeks_rate_limit($pdo,'register_verify',10,900);
    $email=gaeks_email((string)($input['email']??''));if(!$email)gaeks_error('invalid_email','Alamat email tidak valid.',422);
    $name=auth_name((string)($input['name']??''));$password=auth_password((string)($input['password']??''));$code=trim((string)($input['code']??''));
    if(!preg_match('/^\d{6}$/',$code))gaeks_error('invalid_otp','Kode harus terdiri dari 6 angka.',422);
    $pdo->beginTransaction();
    try {
        $lock=gaeks_is_sqlite($pdo)?'': ' FOR UPDATE';$s=$pdo->prepare("SELECT * FROM otp_challenges WHERE email_normalized=:email AND purpose='register' AND consumed_at IS NULL ORDER BY sent_at DESC LIMIT 1".$lock);$s->execute([':email'=>$email]);$challenge=$s->fetch();
        if(!$challenge||strtotime((string)$challenge['expires_at'])<time()){ $pdo->rollBack();gaeks_error('otp_expired','Kode verifikasi tidak ditemukan atau telah kedaluwarsa.',422); }
        if((int)$challenge['attempts']>=OTP_MAX_ATTEMPTS){$pdo->rollBack();gaeks_error('otp_locked','Terlalu banyak kode yang salah. Minta kode baru.',429);}
        $valid=hash_equals((string)$challenge['code_hmac'],gaeks_hash($challenge['id'].'|'.$email.'|'.$code));
        if(!$valid){$pdo->prepare('UPDATE otp_challenges SET attempts=attempts+1 WHERE id=:id')->execute([':id'=>$challenge['id']]);$pdo->commit();gaeks_error('otp_invalid','Kode verifikasi tidak cocok.',422);}
        if(auth_find_user($pdo,$email)){ $pdo->rollBack();gaeks_error('already_registered','Email sudah terdaftar. Silakan masuk.',409); }
        $userId=gaeks_uuid();$role=$email==='gaeks.group@gmail.com'?'admin':'user';
        $pdo->prepare('INSERT INTO users (id,email,email_normalized,name,email_verified_at,password_hash,role) VALUES (:id,:email,:normalized,:name,UTC_TIMESTAMP(),:password,:role)')->execute([':id'=>$userId,':email'=>$email,':normalized'=>$email,':name'=>$name,':password'=>password_hash($password,PASSWORD_DEFAULT),':role'=>$role]);
        $pdo->prepare("INSERT INTO auth_identities (id,user_id,provider,provider_subject,last_used_at) VALUES (:id,:uid,'email_otp',:subject,UTC_TIMESTAMP())")->execute([':id'=>gaeks_uuid(),':uid'=>$userId,':subject'=>$email]);
        $pdo->prepare('UPDATE otp_challenges SET consumed_at=UTC_TIMESTAMP() WHERE id=:id')->execute([':id'=>$challenge['id']]);$pdo->commit();
        $user=auth_find_user($pdo,$email);$notifications=gaeks_send_new_user_notifications($user,'email_otp');if(empty($notifications['admin']['ok']))error_log('Admin new-user notification failed for '.$email);auth_login_response($pdo,$user,'email_otp',true);
    } catch(Throwable $e){if($pdo->inTransaction())$pdo->rollBack();throw $e;}
}

if ($action === 'login') {
    gaeks_rate_limit($pdo,'login',10,900);gaeks_verify_turnstile((string)($input['captchaToken']??''));
    $email=gaeks_email((string)($input['email']??''));$password=(string)($input['password']??'');
    $user=$email?auth_find_user($pdo,$email):null;
    if(!$user||empty($user['password_hash'])||!password_verify($password,(string)$user['password_hash'])){usleep(250000);gaeks_error('invalid_credentials','Email atau kata sandi salah.',401);}
    if(($user['status']??'active')!=='active')gaeks_error('account_unavailable','Akun tidak dapat digunakan.',403);
    auth_login_response($pdo,$user,'email_otp');
}

if ($action === 'google') {
    gaeks_rate_limit($pdo,'google_login',10,900);gaeks_verify_turnstile((string)($input['captchaToken']??''));$credential=(string)($input['credential']??'');
    if($credential==='')gaeks_error('missing_google_credential','Credential Google tidak ditemukan.',422);
    $claims=gaeks_http_json('https://oauth2.googleapis.com/tokeninfo?id_token='.rawurlencode($credential));
    if(!is_array($claims)||($claims['aud']??'')!==GOOGLE_CLIENT_ID||!in_array(($claims['iss']??''),['accounts.google.com','https://accounts.google.com'],true)||(int)($claims['exp']??0)<time()||!in_array($claims['email_verified']??false,[true,'true','1'],true))gaeks_error('google_verification_failed','Akun Google tidak dapat diverifikasi.',401);
    $email=gaeks_email((string)($claims['email']??''));$subject=(string)($claims['sub']??'');if(!$email||$subject==='')gaeks_error('google_profile_invalid','Profil Google tidak lengkap.',422);
    $user=auth_find_user($pdo,$email);$created=false;
    $pdo->beginTransaction();
    try {
        if(!$user){$created=true;$uid=gaeks_uuid();$name=auth_name((string)($claims['name']??explode('@',$email)[0]));$role=$email==='gaeks.group@gmail.com'?'admin':'user';$pdo->prepare('INSERT INTO users (id,email,email_normalized,name,avatar_url,email_verified_at,role) VALUES (:id,:email,:normalized,:name,:avatar,UTC_TIMESTAMP(),:role)')->execute([':id'=>$uid,':email'=>$email,':normalized'=>$email,':name'=>$name,':avatar'=>substr((string)($claims['picture']??''),0,2048)?:null,':role'=>$role]);$user=auth_find_user($pdo,$email);}
        $check=$pdo->prepare("SELECT user_id FROM auth_identities WHERE provider='google' AND provider_subject=:subject LIMIT 1");$check->execute([':subject'=>$subject]);$owner=$check->fetchColumn();if($owner&&$owner!==$user['id']){$pdo->rollBack();gaeks_error('google_identity_conflict','Identitas Google sudah terhubung dengan akun lain.',409);}
        if(!$owner)$pdo->prepare("INSERT INTO auth_identities (id,user_id,provider,provider_subject,last_used_at) VALUES (:id,:uid,'google',:subject,UTC_TIMESTAMP())")->execute([':id'=>gaeks_uuid(),':uid'=>$user['id'],':subject'=>$subject]);else $pdo->prepare("UPDATE auth_identities SET last_used_at=UTC_TIMESTAMP() WHERE provider='google' AND provider_subject=:subject")->execute([':subject'=>$subject]);$pdo->commit();
        if($created){$notifications=gaeks_send_new_user_notifications($user,'google');if(empty($notifications['admin']['ok']))error_log('Admin new-user notification failed for '.$email);}auth_login_response($pdo,$user,'google',$created);
    }catch(Throwable $e){if($pdo->inTransaction())$pdo->rollBack();throw $e;}
}

if ($action === 'logout') {$user=gaeks_current_user();gaeks_require_csrf($user);gaeks_audit($pdo,$user['id'],'auth.logout','user',$user['id']);gaeks_revoke_session($pdo,$user);gaeks_ok(null,200,'Berhasil keluar.');}

gaeks_error('unknown_action','Aksi authentication tidak dikenal.',404);
