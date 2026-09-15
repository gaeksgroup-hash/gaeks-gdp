<?php
declare(strict_types=1);
require_once __DIR__ . '/bootstrap.php';

$pdo=gaeks_db();$user=gaeks_current_user();$uid=(string)$user['id'];$input=$_SERVER['REQUEST_METHOD']==='POST'?gaeks_input(4194304):[];$action=(string)($_GET['action']??$input['action']??'list');
if($_SERVER['REQUEST_METHOD']==='POST')gaeks_require_csrf($user);

function cv_id(string $id): string { if(!preg_match('/^[A-Za-z0-9_-]{1,36}$/',$id))gaeks_error('invalid_id','ID resume tidak valid.',422);return $id; }
function cv_ms(?string $value): ?int { return $value?strtotime($value)*1000:null; }
function cv_result(array $r,bool $withData=true): array { $out=['id'=>$r['id'],'title'=>$r['title'],'isDraft'=>(bool)$r['is_draft'],'completeness'=>(int)$r['completeness'],'version'=>(int)$r['version'],'updatedAt'=>cv_ms($r['updated_at']),'deletedAt'=>cv_ms($r['deleted_at'])];if($withData)$out['data']=json_decode((string)$r['data_json'],true)?:[];return $out; }

if($action==='list'){$trash=($_GET['tab']??'active')==='trash';$s=$pdo->prepare('SELECT * FROM cvs WHERE user_id=:uid AND deleted_at '.($trash?'IS NOT NULL':'IS NULL').' ORDER BY updated_at DESC');$s->execute([':uid'=>$uid]);gaeks_ok(array_map(static fn($r)=>cv_result($r,true),$s->fetchAll()));}

if($action==='get'){$id=cv_id((string)($_GET['id']??$input['id']??''));$s=$pdo->prepare('SELECT * FROM cvs WHERE id=:id AND user_id=:uid LIMIT 1');$s->execute([':id'=>$id,':uid'=>$uid]);$row=$s->fetch();if(!$row)gaeks_error('not_found','Resume tidak ditemukan.',404);gaeks_ok(cv_result($row,true));}

if($action==='save'){
    $cv=$input['cv']??$input;$id=!empty($cv['id'])?cv_id((string)$cv['id']):gaeks_uuid();$title=trim((string)($cv['title']??'CV Tanpa Judul'));if($title==='')$title='CV Tanpa Judul';$title=substr($title,0,255);$data=$cv['data']??[];if(!is_array($data))gaeks_error('invalid_data','Data resume tidak valid.',422);$json=json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_INVALID_UTF8_SUBSTITUTE);$comp=max(0,min(100,(int)($cv['completeness']??0)));$draft=!empty($cv['isDraft'])?1:0;
    $pdo->beginTransaction();try{$s=$pdo->prepare('SELECT * FROM cvs WHERE id=:id'.(gaeks_is_sqlite($pdo)?'':' FOR UPDATE'));$s->execute([':id'=>$id]);$old=$s->fetch();if($old&&$old['user_id']!==$uid){$pdo->rollBack();gaeks_error('not_found','Resume tidak ditemukan.',404);}if($old){$expected=isset($cv['version'])?(int)$cv['version']:null;if($expected!==null&&$expected!==(int)$old['version']){$pdo->rollBack();gaeks_error('version_conflict','Resume telah berubah di perangkat lain. Muat ulang sebelum menyimpan.',409);}$revisionSql=(gaeks_is_sqlite($pdo)?'INSERT OR IGNORE':'INSERT IGNORE')." INTO document_revisions (id,document_type,document_id,user_id,version,data_json) VALUES (:rid,'cv',:doc,:uid,:version,:data)";$pdo->prepare($revisionSql)->execute([':rid'=>gaeks_uuid(),':doc'=>$id,':uid'=>$uid,':version'=>$old['version'],':data'=>$old['data_json']]);$pdo->prepare('UPDATE cvs SET title=:title,data_json=:data,is_draft=:draft,completeness=:comp,version=version+1,deleted_at=NULL WHERE id=:id AND user_id=:uid')->execute([':title'=>$title,':data'=>$json,':draft'=>$draft,':comp'=>$comp,':id'=>$id,':uid'=>$uid]);}else{$pdo->prepare('INSERT INTO cvs (id,user_id,title,data_json,is_draft,completeness) VALUES (:id,:uid,:title,:data,:draft,:comp)')->execute([':id'=>$id,':uid'=>$uid,':title'=>$title,':data'=>$json,':draft'=>$draft,':comp'=>$comp]);}$pdo->commit();}catch(Throwable $e){if($pdo->inTransaction())$pdo->rollBack();throw $e;}
    $s=$pdo->prepare('SELECT * FROM cvs WHERE id=:id AND user_id=:uid');$s->execute([':id'=>$id,':uid'=>$uid]);gaeks_audit($pdo,$uid,'cv.saved','cv',$id);gaeks_ok(cv_result($s->fetch(),true),$old?200:201,'Resume tersimpan di server.');
}

if(in_array($action,['delete','restore','delete_permanent'],true)){
    $id=cv_id((string)($input['id']??$_GET['id']??''));$s=$pdo->prepare('SELECT id FROM cvs WHERE id=:id AND user_id=:uid');$s->execute([':id'=>$id,':uid'=>$uid]);if(!$s->fetch())gaeks_error('not_found','Resume tidak ditemukan.',404);
    if($action==='delete_permanent'){$pdo->beginTransaction();try{$pdo->prepare("DELETE FROM document_revisions WHERE document_type='cv' AND document_id=:id AND user_id=:uid")->execute([':id'=>$id,':uid'=>$uid]);$pdo->prepare('DELETE FROM cvs WHERE id=:id AND user_id=:uid')->execute([':id'=>$id,':uid'=>$uid]);$pdo->commit();}catch(Throwable $e){if($pdo->inTransaction())$pdo->rollBack();throw $e;}}
    elseif($action==='delete')$pdo->prepare('UPDATE cvs SET deleted_at=UTC_TIMESTAMP(),updated_at=UTC_TIMESTAMP() WHERE id=:id AND user_id=:uid')->execute([':id'=>$id,':uid'=>$uid]);
    else $pdo->prepare('UPDATE cvs SET deleted_at=NULL,updated_at=UTC_TIMESTAMP() WHERE id=:id AND user_id=:uid')->execute([':id'=>$id,':uid'=>$uid]);
    gaeks_audit($pdo,$uid,'cv.'.$action,'cv',$id);gaeks_ok(null,200,$action==='restore'?'Resume dipulihkan.':($action==='delete'?'Resume dipindahkan ke sampah.':'Resume dihapus permanen.'));
}

gaeks_error('unknown_action','Aksi resume tidak dikenal.',404);
