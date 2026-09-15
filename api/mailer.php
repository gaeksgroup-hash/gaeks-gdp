<?php
declare(strict_types=1);

require_once __DIR__ . '/config.php';

function gaeks_mail_header(string $value): string
{
    return str_replace(["\r", "\n"], '', $value);
}

function gaeks_send_mail(string $toEmail, string $toName, string $subject, string $html): array
{
    if (!filter_var($toEmail, FILTER_VALIDATE_EMAIL)) return ['ok' => false, 'error' => 'invalid_recipient'];
    if (APP_ENV === 'test' && MAIL_TRANSPORT === 'test') return ['ok' => true, 'transport' => 'test'];
    $toName = gaeks_mail_header($toName);
    $subject = gaeks_mail_header($subject);
    $from = SMTP_USER !== '' ? SMTP_USER : 'no-reply@gaeks.com';

    if (SMTP_USER !== '' && SMTP_PASSWORD !== '') {
        $socket = @fsockopen('ssl://' . SMTP_HOST, SMTP_PORT, $errno, $errstr, 15);
        if ($socket) {
            $read = static function ($stream): string { $out=''; while(($line=fgets($stream,515))!==false){$out.=$line;if(strlen($line)>3&&$line[3]===' ')break;} return $out; };
            $command = static function ($stream, callable $read, string $value, array $expected): string { fwrite($stream,$value."\r\n");$result=$read($stream);if(!in_array(substr($result,0,3),$expected,true))throw new RuntimeException('smtp_rejected_'.substr($result,0,3));return $result; };
            try {
                $read($socket);
                $command($socket,$read,'EHLO '.($_SERVER['SERVER_NAME']??'gdp.gaeks.com'),['250']);
                $command($socket,$read,'AUTH LOGIN',['334']);
                $command($socket,$read,base64_encode(SMTP_USER),['334']);
                $command($socket,$read,base64_encode(SMTP_PASSWORD),['235']);
                $command($socket,$read,'MAIL FROM:<'.$from.'>',['250']);
                $command($socket,$read,'RCPT TO:<'.$toEmail.'>',['250','251']);
                $command($socket,$read,'DATA',['354']);
                $headers = [
                    'MIME-Version: 1.0',
                    'Content-Type: text/html; charset=UTF-8',
                    'From: =?UTF-8?B?'.base64_encode(SMTP_FROM_NAME).'?= <'.$from.'>',
                    'To: =?UTF-8?B?'.base64_encode($toName).'?= <'.$toEmail.'>',
                    'Reply-To: <'.REPLY_TO_EMAIL.'>',
                    'Subject: =?UTF-8?B?'.base64_encode($subject).'?=',
                    'Message-ID: <'.bin2hex(random_bytes(12)).'@gaeks.com>',
                    'Date: '.date(DATE_RFC2822),
                ];
                $safeBody = preg_replace('/(?m)^\./', '..', implode("\r\n",$headers)."\r\n\r\n".$html);
                fwrite($socket,$safeBody."\r\n.\r\n");
                $result=$read($socket);
                fwrite($socket,"QUIT\r\n");
                fclose($socket);
                if(substr($result,0,3)==='250')return ['ok'=>true,'transport'=>'smtp'];
            } catch (Throwable $e) {
                fclose($socket);
                error_log('SMTP delivery failed: '.$e->getMessage());
            }
        }
    }

    $headers = implode("\r\n",[
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset=UTF-8',
        'From: '.gaeks_mail_header(SMTP_FROM_NAME).' <'.$from.'>',
        'Reply-To: '.REPLY_TO_EMAIL,
    ]);
    $ok = @mail($toEmail, $subject, $html, $headers);
    return ['ok'=>$ok,'transport'=>'php_mail','error'=>$ok?null:'delivery_failed'];
}

function gaeks_email_shell(string $title, string $body): string
{
    return '<!doctype html><html><body style="margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#14213d"><div style="max-width:600px;margin:32px auto;background:#fff;border:1px solid #dfe7f3;border-radius:18px;overflow:hidden"><div style="padding:24px 28px;background:#112047;color:#fff"><strong style="font-size:20px">GAEKS Digital Products</strong></div><div style="padding:30px 28px"><h1 style="font-size:22px;margin:0 0 16px">'.$title.'</h1>'.$body.'</div><div style="padding:16px 28px;background:#f7f9fc;color:#6b7890;font-size:12px">Email otomatis dari sistem GAEKS Digital Products.</div></div></body></html>';
}

function gaeks_send_otp_email(string $email, string $name, string $otp): array
{
    $safeName=htmlspecialchars($name,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');$safeOtp=htmlspecialchars($otp,ENT_QUOTES,'UTF-8');
    $body='<p>Halo <strong>'.$safeName.'</strong>,</p><p>Gunakan kode berikut untuk menyelesaikan pendaftaran:</p><div style="font-size:32px;font-weight:800;letter-spacing:8px;text-align:center;padding:18px;background:#eef4ff;border-radius:12px">'.$safeOtp.'</div><p style="color:#6b7890">Kode berlaku 10 menit. Jangan berikan kode ini kepada siapa pun.</p>';
    return gaeks_send_mail($email,$name,'Kode verifikasi GAEKS Digital: '.$otp,gaeks_email_shell('Verifikasi email Anda',$body));
}

function gaeks_send_new_user_notifications(array $user, string $provider): array
{
    $name=(string)$user['name'];$email=(string)$user['email'];$safeName=htmlspecialchars($name,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');$safeEmail=htmlspecialchars($email,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');
    $welcome=gaeks_email_shell('Selamat datang, '.$safeName.'!','<p>Akun Anda telah aktif dan siap digunakan untuk membuat CV serta presentasi.</p><p><a href="'.APP_URL.'/index.html" style="display:inline-block;padding:12px 20px;border-radius:10px;background:#2463eb;color:#fff;text-decoration:none;font-weight:700">Buka workspace GAEKS</a></p>');
    $admin=gaeks_email_shell('Pengguna baru terdaftar','<p><strong>Nama:</strong> '.$safeName.'</p><p><strong>Email:</strong> '.$safeEmail.'</p><p><strong>Provider:</strong> '.htmlspecialchars($provider,ENT_QUOTES,'UTF-8').'</p><p><strong>Waktu UTC:</strong> '.gmdate('Y-m-d H:i:s').'</p>');
    return ['welcome'=>gaeks_send_mail($email,$name,'Selamat datang di GAEKS Digital Products',$welcome),'admin'=>gaeks_send_mail(ADMIN_NOTIFICATION_EMAIL,'GDP Admin','Pengguna baru GDP: '.$email,$admin)];
}

if (realpath(__FILE__) === realpath($_SERVER['SCRIPT_FILENAME'] ?? '')) {
    http_response_code(404);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok'=>false,'message'=>'Not found']);
}
