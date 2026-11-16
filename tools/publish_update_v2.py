#!/usr/bin/env python3
"""Validate an owner-approved public GARD v2 JSON, preserve public history, update Netlify site.
Use on an offline local repository copy; GitHub deployment must be committed separately.
"""
import argparse,datetime,hashlib,json,pathlib,re,shutil,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SITE=ROOT/'site'/'data'

def validate(doc):
    if not isinstance(doc,dict) or set(doc)!={'schema','release','meetings','entries','statements','integrity'}:raise ValueError('루트 공개 JSON 필드가 잘못되었습니다.')
    if doc['schema']!='gard-ledger-disclosure/v2':raise ValueError('GARD v2 JSON이 아닙니다.')
    release=doc['release'];ri=doc['integrity']
    if not isinstance(release,dict) or release.get('audience')!='public':raise ValueError('공개 대상 public만 GitHub에 게시할 수 있습니다.')
    if not isinstance(release.get('id'),str) or not re.fullmatch(r'[A-Za-z0-9_-]{3,80}',release['id']):raise ValueError('공개버전 ID를 확인하세요.')
    if not isinstance(release.get('years'),list) or not release['years'] or not all(isinstance(y,str) and re.fullmatch(r'20\d\d',y) for y in release['years']):raise ValueError('공개 연도 오류')
    if not isinstance(doc['meetings'],list) or not isinstance(doc['entries'],list) or not isinstance(doc['statements'],list):raise ValueError('배열 형식 오류')
    if len(doc['entries'])>3000 or len(doc['meetings'])>3000:raise ValueError('항목 제한 초과')
    for entry in doc['entries']:
        if not isinstance(entry,dict) or set(entry)!={'id','date','meetingId','description','debit','credit','amount','entity','status'}:raise ValueError('분개 공개범위 불일치')
        if not isinstance(entry['amount'],int) or isinstance(entry['amount'],bool) or entry['amount']<=0:raise ValueError('잘못된 분개 금액')
        if entry['entity']!=release.get('entity'):raise ValueError('보고 주체가 일치하지 않습니다.')
    for mtg in doc['meetings']:
        if not isinstance(mtg,dict) or set(mtg)!={'id','date','title','type','status','summary','nextAction'}:raise ValueError('미팅 공개범위 불일치')
    if not isinstance(ri,dict) or ri.get('algorithm')!='SHA-256':raise ValueError('해시 형식 오류')
    raw={k:v for k,v in doc.items() if k!='integrity'}
    actual=hashlib.sha256(json.dumps(raw,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
    if actual!=ri.get('sha256'):raise ValueError('SHA-256 불일치. 승인 JSON을 수정한 경우 오너 앱에서 다시 내보내세요.')
    return release['id']

def main():
    p=argparse.ArgumentParser(description='GARD OWNER 공개 승인본 v2 점검 및 GitHub 업로드 폴더 반영')
    p.add_argument('approved_json');p.add_argument('--approve',action='store_true',help='사람이 공개 내용 직접 확인한 후 반영')
    args=p.parse_args();src=pathlib.Path(args.approved_json)
    if not src.is_file() or src.stat().st_size>2_000_000:p.error('2MB 이하 JSON만 선택하세요.')
    try:doc=json.loads(src.read_text(encoding='utf-8'));rid=validate(doc)
    except (ValueError,TypeError,json.JSONDecodeError) as e:p.error(str(e))
    print('공개버전:',rid,'연도:',doc['release']['years'],'회의:',len(doc['meetings']),'분개:',len(doc['entries']))
    print('수익·부채 등 선택 공개 수치는 원본 전체 회계를 대표하지 않습니다.')
    if not args.approve:return 0
    history_path=SITE/'history.json';public_path=SITE/'public.json';history=json.loads(history_path.read_text(encoding='utf-8'))
    if any(e['id']==rid for e in history.get('releases',[])):p.error('중복 버전 ID입니다. 새 버전 ID로 다시 승인하세요.')
    old=json.loads(public_path.read_text(encoding='utf-8'));validate(old)
    folder=SITE/'versions';folder.mkdir(exist_ok=True)
    old_id=old['release']['id']
    if not (folder/(old_id+'.json')).exists():shutil.copy2(public_path,folder/(old_id+'.json'))
    (folder/(rid+'.json')).write_text(src.read_text(encoding='utf-8'),encoding='utf-8')
    public_path.write_text(src.read_text(encoding='utf-8'),encoding='utf-8')
    history['releases'].append({'id':rid,'date':doc['release']['generatedAt'],'hash':doc['integrity']['sha256'],'meetings':len(doc['meetings']),'entries':len(doc['entries'])})
    history_path.write_text(json.dumps(history,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('반영 완료: site/data/public.json, history.json, versions/'+rid+'.json')
    print('GitHub 커밋 및 Netlify 공개는 별도 작업입니다.')
    return 0
if __name__=='__main__':sys.exit(main())
