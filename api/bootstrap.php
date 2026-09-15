<?php
declare(strict_types=1);

require_once __DIR__ . '/config.php';
ini_set('display_errors', APP_ENV === 'production' ? '0' : '1');
ini_set('log_errors', '1');
date_default_timezone_set('UTC');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header('Cache-Control: no-store');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { header('Allow: GET, POST, OPTIONS'); http_response_code(204); exit; }

function gaeks_uuid(): string { $b=random_bytes(16); $b[6]=chr((ord($b[6])&15)|64); $b[8]=chr((ord($b[8])&63)|128); $h=bin2hex($b); return substr($h,0,8).'-'.substr($h,8,4).'-'.substr($h,12,4).'-'.substr($h,16,4).'-'.substr($h,20); }
function gaeks_request_id(): string { static $id; return $id ??= gaeks_uuid(); }
function gaeks_json(array $payload, int $status=200): never { http_response_code($status); $payload['request_id'] ??= gaeks_request_id(); echo json_encode($payload, JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_INVALID_UTF8_SUBSTITUTE); exit; }
function gaeks_ok(mixed $data=null, int $status=200, ?string $message=null): never { $p=['ok'=>true,'status'=>'success','data'=>$data]; if($message!==null)$p['message']=$message; gaeks_json($p,$status); }
function gaeks_error(string $code,string $message,int $status=400,array $fields=[]): never { $p=['ok'=>false,'status'=>'error','error'=>['code'=>$code,'message'=>$message],'message'=>$message]; if($fields!==[])$p['error']['fields']=$fields; gaeks_json($p,$status); }

function gaeks_input(int $maxBytes=2097152): array {
    if((int)($_SERVER['CONTENT_LENGTH']??0)>$maxBytes)gaeks_error('payload_too_large','Ukuran data melebihi batas yang diizinkan.',413);
    $raw=file_get_contents('php://input'); if($raw===false||$raw==='')return []; if(strlen($raw)>$maxBytes)gaeks_error('payload_too_large','Ukuran data melebihi batas yang diizinkan.',413);
    try{$decoded=json_decode($raw,true,512,JSON_THROW_ON_ERROR);}catch(JsonException){gaeks_error('invalid_json','Payload JSON tidak valid.',400);} return is_array($decoded)?$decoded:[];
}

function gaeks_db(): PDO {
    static $pdo; if($pdo instanceof PDO)return $pdo;
    if(SESSION_SECRET===''||strlen(SESSION_SECRET)<32)throw new RuntimeException('SESSION_SECRET belum dikonfigurasi dengan aman.');
    $dsn=DB_DSN!==''?DB_DSN:sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',DB_HOST,DB_PORT,DB_NAME);
    if(DB_DSN===''&&(DB_NAME===''||DB_USER===''))throw new RuntimeException('Konfigurasi database belum lengkap.');
    $pdo=new PDO($dsn,DB_USER,DB_PASSWORD,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC,PDO::ATTR_EMULATE_PREPARES=>false]);
    if($pdo->getAttribute(PDO::ATTR_DRIVER_NAME)==='sqlite'){$pdo->exec('PRAGMA foreign_keys=ON');$pdo->sqliteCreateFunction('UTC_TIMESTAMP',static fn()=>gmdate('Y-m-d H:i:s'));}
    return $pdo;
}
function gaeks_is_sqlite(PDO $pdo): bool { return $pdo->getAttribute(PDO::ATTR_DRIVER_NAME)==='sqlite'; }

function gaeks_client_ip(): string { return (string)($_SERVER['REMOTE_ADDR']??'0.0.0.0'); }
function gaeks_hash(string $v): string { return hash_hmac('sha256',$v,SESSION_SECRET); }
function gaeks_email(string $email): ?string { $email=strtolower(trim($email)); return filter_var($email,FILTER_VALIDATE_EMAIL)?$email:null; }
function gaeks_is_https(): bool { return APP_ENV==='production'||(!empty($_SERVER['HTTPS'])&&$_SERVER['HTTPS']!=='off')||($_SERVER['HTTP_X_FORWARDED_PROTO']??'')==='https'; }
function gaeks_set_cookie(string $name,string $value,int $expires,bool $httpOnly): void { setcookie($name,$value,['expires'=>$expires,'path'=>'/','secure'=>gaeks_is_https(),'httponly'=>$httpOnly,'samesite'=>'Lax']); }

function gaeks_user_payload(array $row): array {
    $isPro=($row['role']??'user')==='admin';
    return ['id'=>$row['id'],'email'=>$row['email'],'name'=>$row['name'],'avatar'=>$row['avatar_url']??null,'provider'=>$row['provider']??'email_otp','isAdmin'=>($row['role']??'user')==='admin','isPro'=>$isPro,'plan'=>$isPro?'PRO_VIP':'FREE','planLabel'=>$isPro?'SUPER ADMIN':'Free Tier'];
}

function gaeks_create_session(PDO $pdo,string $userId): array {
    $token=bin2hex(random_bytes(32)); $csrf=bin2hex(random_bytes(24)); $expires=time()+APP_SESSION_TTL_SECONDS;
    $stmt=$pdo->prepare('INSERT INTO sessions (id,user_id,token_hash,csrf_secret_hash,ip_hash,user_agent_hash,expires_at) VALUES (:id,:uid,:token,:csrf,:ip,:ua,:expires)');
    $stmt->execute([':id'=>gaeks_uuid(),':uid'=>$userId,':token'=>gaeks_hash($token),':csrf'=>gaeks_hash($csrf),':ip'=>gaeks_hash(gaeks_client_ip()),':ua'=>gaeks_hash(substr((string)($_SERVER['HTTP_USER_AGENT']??''),0,500)),':expires'=>gmdate('Y-m-d H:i:s',$expires)]);
    gaeks_set_cookie(APP_SESSION_COOKIE,$token,$expires,true); gaeks_set_cookie('gaeks_csrf',$csrf,$expires,false); return ['csrfToken'=>$csrf,'expiresAt'=>$expires*1000];
}

function gaeks_current_user(bool $required=true): ?array {
    $token=(string)($_COOKIE[APP_SESSION_COOKIE]??''); if($token===''){if($required)gaeks_error('unauthenticated','Silakan masuk untuk melanjutkan.',401);return null;}
    $pdo=gaeks_db(); $stmt=$pdo->prepare("SELECT u.*,COALESCE(ai.provider,'email_otp') provider,s.id session_id,s.csrf_secret_hash FROM sessions s JOIN users u ON u.id=s.user_id LEFT JOIN auth_identities ai ON ai.user_id=u.id WHERE s.token_hash=:token AND s.revoked_at IS NULL AND s.expires_at>UTC_TIMESTAMP() AND u.status='active' ORDER BY ai.last_used_at DESC LIMIT 1");
    $stmt->execute([':token'=>gaeks_hash($token)]); $row=$stmt->fetch(); if(!$row){gaeks_set_cookie(APP_SESSION_COOKIE,'',time()-3600,true);gaeks_set_cookie('gaeks_csrf','',time()-3600,false);if($required)gaeks_error('session_expired','Sesi berakhir. Silakan masuk kembali.',401);return null;}
    $pdo->prepare('UPDATE sessions SET last_seen_at=UTC_TIMESTAMP() WHERE id=:id')->execute([':id'=>$row['session_id']]); return $row;
}

function gaeks_require_csrf(array $user): void { $h=trim((string)($_SERVER['HTTP_X_CSRF_TOKEN']??'')); if($h===''||!hash_equals((string)$user['csrf_secret_hash'],gaeks_hash($h)))gaeks_error('csrf_failed','Permintaan keamanan tidak valid. Muat ulang halaman lalu coba lagi.',403); }
function gaeks_revoke_session(PDO $pdo,array $user): void { $pdo->prepare('UPDATE sessions SET revoked_at=UTC_TIMESTAMP() WHERE id=:id')->execute([':id'=>$user['session_id']]);gaeks_set_cookie(APP_SESSION_COOKIE,'',time()-3600,true);gaeks_set_cookie('gaeks_csrf','',time()-3600,false); }

function gaeks_rate_limit(PDO $pdo,string $action,int $max,int $windowSeconds): void {
    $scope=gaeks_hash($action.'|'.gaeks_client_ip());$window=intdiv(time(),$windowSeconds)*$windowSeconds;$start=gmdate('Y-m-d H:i:s',$window);
    $sql=gaeks_is_sqlite($pdo)?'INSERT INTO rate_limit_buckets (scope_hash,action_key,window_start,request_count) VALUES (:scope,:action,:window,1) ON CONFLICT(scope_hash,action_key,window_start) DO UPDATE SET request_count=request_count+1':'INSERT INTO rate_limit_buckets (scope_hash,action_key,window_start,request_count) VALUES (:scope,:action,:window,1) ON DUPLICATE KEY UPDATE request_count=request_count+1';
    $pdo->prepare($sql)->execute([':scope'=>$scope,':action'=>$action,':window'=>$start]);
    $s=$pdo->prepare('SELECT request_count FROM rate_limit_buckets WHERE scope_hash=:scope AND action_key=:action AND window_start=:window');$s->execute([':scope'=>$scope,':action'=>$action,':window'=>$start]);if((int)$s->fetchColumn()>$max){header('Retry-After: '.max(1,($window+$windowSeconds)-time()));gaeks_error('rate_limited','Terlalu banyak percobaan. Silakan tunggu sebentar.',429);}
}

function gaeks_http_json(string $url,string $method='GET',array $fields=[]): ?array {
    if(function_exists('curl_init')){
        $ch=curl_init($url);$options=[CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>10,CURLOPT_CONNECTTIMEOUT=>5,CURLOPT_FOLLOWLOCATION=>false,CURLOPT_HTTPHEADER=>['Accept: application/json','User-Agent: GAEKS-GDP/1.0']];
        if($method==='POST'){$options[CURLOPT_POST]=true;$options[CURLOPT_POSTFIELDS]=http_build_query($fields);$options[CURLOPT_HTTPHEADER][]='Content-Type: application/x-www-form-urlencoded';}
        curl_setopt_array($ch,$options);$raw=curl_exec($ch);$status=(int)curl_getinfo($ch,CURLINFO_RESPONSE_CODE);curl_close($ch);if(!is_string($raw)||$status<200||$status>=300)return null;$decoded=json_decode($raw,true);return is_array($decoded)?$decoded:null;
    }
    $options=['http'=>['method'=>$method,'header'=>"Accept: application/json\r\nUser-Agent: GAEKS-GDP/1.0\r\n",'timeout'=>10,'ignore_errors'=>true]];
    if($method==='POST'){$options['http']['header'].="Content-Type: application/x-www-form-urlencoded\r\n";$options['http']['content']=http_build_query($fields);}
    $raw=@file_get_contents($url,false,stream_context_create($options));$decoded=$raw?json_decode($raw,true):null;return is_array($decoded)?$decoded:null;
}

function gaeks_verify_turnstile(string $token): void {
    if(APP_ENV!=='production'&&$token==='test-bypass')return; if($token===''||TURNSTILE_SECRET_KEY==='')gaeks_error('captcha_required','Verifikasi keamanan belum lengkap.',422);
    $r=gaeks_http_json('https://challenges.cloudflare.com/turnstile/v0/siteverify','POST',['secret'=>TURNSTILE_SECRET_KEY,'response'=>$token,'remoteip'=>gaeks_client_ip()]);if(!is_array($r)||empty($r['success']))gaeks_error('captcha_failed','Verifikasi keamanan gagal. Silakan ulangi CAPTCHA.',422);
}

function gaeks_audit(PDO $pdo,?string $actor,string $action,?string $type=null,?string $target=null,array $meta=[]): void {
    try{$s=$pdo->prepare('INSERT INTO audit_events (actor_user_id,action_key,target_type,target_id,request_id,metadata_json) VALUES (:actor,:action,:type,:target,:request,:meta)');$s->execute([':actor'=>$actor,':action'=>$action,':type'=>$type,':target'=>$target,':request'=>gaeks_request_id(),':meta'=>$meta===[]?null:json_encode($meta,JSON_UNESCAPED_SLASHES)]);}catch(Throwable $e){error_log('Audit write failed: '.$e->getMessage());}
}

set_exception_handler(static function(Throwable $e): void { error_log(sprintf('[%s] %s in %s:%d',gaeks_request_id(),$e->getMessage(),$e->getFile(),$e->getLine()));gaeks_error('server_error',APP_ENV==='production'?'Layanan sedang mengalami kendala.':$e->getMessage(),500); });
