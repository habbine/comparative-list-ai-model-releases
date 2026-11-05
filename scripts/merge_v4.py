import json,glob,re,datetime as dt
dev={'anthropic':'Anthropic','openai':'OpenAI','google':'Google','meta':'Meta','xai':'xAI','mistral':'Mistral','deepseek':'DeepSeek','qwen':'Qwen (Alibaba)'}
names={}
for f in glob.glob('../xl/in_*.json'):
    try:
        for r in json.load(open(f)): names.setdefault(r['model_id'],r['model'])
    except Exception: pass
R={}
for f in sorted(glob.glob('[a-z]*.jsonl')):
    for l in open(f):
        d=json.loads(l);R[d['id']]=d
iso=lambda s:bool(s and re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(s)))
def norm_stage(s):
    s=(s or '').lower()
    for k in ('open_weights','preview','beta','experimental','gated'):
        if s.startswith(k): return 'open_weights_release' if k=='open_weights' else k
    return 'ga'
def norm_status(s):
    s=(s or '').lower()
    for k in ('active','legacy','deprecated','retired'):
        if s.startswith(k): return k
def norm_mi(s):
    if not s: return None
    if isinstance(s,list): s=','.join(map(str,s))
    m={'text':'t','image':'i','audio':'a','video':'v','pdf':'pdf'}
    return ','.join(m[x.strip().lower()] for x in re.split(r'[,/+ ]+',s) if x.strip().lower() in m) or None
srcs={}
# Qwen merge
ARB={ # arbitration of vendor conflicts: id -> (fa, note)
'qwen__qwen3-7-flash':('2026-07-21','Model Studio 21 Jul; QwenCloud changelog 25 Jul; unresolved, earlier vendor date kept'),
'qwen__qwen3-8-omni-flash':('2026-09-18','QwenCloud changelog and Model Studio card 18 Sep; Alibaba Cloud product news 17 Sep (time-zone offset likely)'),
'qwen__qwen3-8-27b':('2026-08-14','HF upload 13 Aug; repository release record 14 Aug; later date kept (public release)'),
'qwen__qwen3-0-6b-32b-dense-30b-a3b-235b-a22b':('2025-04-29','blog header and repository record 29 Apr; HF metadata 28 Apr'),
'qwen__qwen3-5-plus':('2026-02-16','Model Studio lists 15 Feb; release record 16 Feb'),
'qwen__qwen-vl-max':('2024-01-18','GitHub news 18 Jan; blog 25 Jan; earliest vendor date kept'),
'qwen__qwen2-vl':('2024-08-29','page header 29 Aug; metadata 28 Aug'),
}
for f in ('qwen_result_a.json','qwen_result_b.json'):
    for a in json.load(open(f)):
        d=R[a['id']];fa=a.get('first_available')
        if not a.get('verified'): d['unv']=1;d['conf']='low';continue
        d.pop('unv',None)
        if iso(fa): d['fa']=fa
        d['st']=norm_stage(a.get('stage'))
        if iso(a.get('ga_date')): d['ga']=a['ga_date']
        wd=a.get('weights_date')
        if iso(wd): d['wt']=wd
        elif wd and re.match(r'\d{4}-\d{2}-\d{2}',wd): d['wt']=wd[:10]
        for k,ak in (('ctx','ctx'),('mx','max_out'),('ck','cutoff'),('pt','params_total_b'),('pa','params_active_b'),('ar','arch'),('lic','licence'),('pi','price_in'),('po','price_out'),('apiid','api_id')):
            v=a.get(ak)
            if v not in (None,'','not stated'): d[k]=v
        mi=norm_mi(a.get('modalities'))
        if mi:d['mi']=mi
        s=norm_status(a.get('status'))
        if s:d['stat']=s
        if iso(a.get('retired_on')): d['ret']=a['retired_on']; d['note']=(d.get('note','')+'; retirement scheduled per vendor banner, shutdown not confirmed').lstrip('; ')
        d['conf']=a.get('confidence') or 'medium'
        srcs[a['id']]=a.get('source_urls') or []
        if srcs[a['id']]: d['src']=srcs[a['id']][0]
        d['note']=(a.get('date_note') or '')[:400]+(('; '+d['note']) if d.get('note') and 'retirement' in d['note'] else '')
        if a['id'] in ARB: d['fa']=ARB[a['id']][0]; d['note']=ARB[a['id']][1]
# special qwen
q=R['qwen__tongyi-qianwen-proprietary-chat-service-api-public-opening'];q.update(st='beta',an='2023-04-11',fa='2023-04-11',ga='2023-09-13',note='enterprise beta 11 Apr 2023; public opening 13 Sep 2023 not confirmed to the day on a vendor page (Alibaba Cloud repost 18 Sep says opened)',conf='medium')
q=R['qwen__qwen3-max-instruct'];q.update(ga='2025-09-24',note='qwen3-max-preview first listed 5 Sep 2025; general release 23 Sep (Model Studio) / 24 Sep (blog); 24 Sep kept')
q=R['qwen__qwen3-8-max'];q['wt']='2026-08-12'
for k in ('qwen__qwen-plus','qwen__qwen-turbo'): R[k].update(unv=1,conf='low',note='launch date not stated on the Qwen2.5 blog (19 Sep 2024); date is the blog date')
# others
oth={o['item']:o for o in json.load(open('other_result.json'))}
def S(i,k):
    o=oth[k];R[i].setdefault('src',(o.get('source_urls') or [None])[0]);srcs[i]=o.get('source_urls') or []
for i,k,ret in [('anthropic__claude-1','Claude 1 (claude-1)','2024-11-06'),('anthropic__claude-instant-1','Claude Instant 1 (claude-instant-1)','2024-11-06'),('anthropic__claude-instant-1-2','Claude Instant 1.2','2024-11-06'),('anthropic__claude-2','Claude 2 (claude-2.0)','2025-07-21'),('anthropic__claude-2-1','Claude 2.1','2025-07-21'),('anthropic__claude-3-sonnet','Claude 3 Sonnet (claude-3-sonnet-20240229)','2025-07-21')]:
    R[i]['ret']=ret
    srcs.setdefault(i,[]).extend([u for u in (next(o for o in json.load(open('other_result.json')) if o['item']==k and o['task']=='A').get('source_urls') or [])])
R['anthropic__claude-1']['note']='alias claude-1 not on the deprecations page; mapped to claude-1.x retirement'
R['anthropic__claude-instant-1']['note']='alias not listed; mapped to claude-instant-1.0/1.1 retirement'
R['anthropic__claude-instant-1-2'].update(conf='high');R['anthropic__claude-instant-1-2'].pop('unv',None)
bl=[o for o in json.load(open('other_result.json'))]
def get(item,t):return next(o for o in bl if o['item']==item and o['task']==t)
def urls(i,item,t):
    u=get(item,t).get('source_urls') or [];srcs.setdefault(i,[]).extend(u)
    if u and not R[i].get('src'):R[i]['src']=u[0]
urls('anthropic__claude-instant-1-2','Claude Instant 1.2','B')
g=R['google__palm-2'];g.update(st='preview',fa='2023-05-10',ga='2023-06-07',ret='2025-04-21',conf='medium',note='preview 10 May 2023; GA 7 Jun from Vertex model card (medium-low); Gemini API PaLM decommissioned 15 Aug 2024, Vertex retired 21 Apr 2025');g.pop('unv',None);urls('google__palm-2','Google PaLM 2','B');urls('google__palm-2','Google PaLM 2 (PaLM API / text-bison etc.)','A') if any(o['item'].startswith('Google PaLM 2 (')for o in bl) else None
g=R['google__gemini-1-0-nano'];g.update(conf='high',note='Pixel 8 Pro 6 Dec 2023; Smart Reply developer preview; AICore early preview');g.pop('unv',None);urls('google__gemini-1-0-nano','Gemini 1.0 Nano','B')
g=R['google__gemini-1-0-pro'];g.update(st='preview',fa='2023-12-06',ga='2024-02-15',api='2023-12-13',ret='2025-04-21',conf='high',note='Bard 6 Dec 2023; developer access 13 Dec (Vertex Preview); Vertex GA 15 Feb 2024; Gemini API dropped 18 Feb 2025, Vertex retired 21 Apr 2025');g.pop('unv',None);urls('google__gemini-1-0-pro','Gemini 1.0 Pro','B')
g=R['google__gemini-1-0-ultra'];g.update(st='gated',fa='2024-02-08',ga='2024-02-15',ret='2025-04-09',conf='medium',note='Gemini Advanced 8 Feb 2024; Vertex GA via allowlist 15 Feb; retirement 9 Apr 2025 from a forum post quoting the Vertex notice (low), may be 21 Apr');urls('google__gemini-1-0-ultra','Gemini 1.0 Ultra','B')
g=R['deepseek__deepseekmoe-16b'];g.update(fa='2024-01-11',wt='2024-01-11',conf='medium',note='paper date 11 Jan 2024; HF updated 12 Jan; repo created 2 Jan; no dated vendor release statement');g.pop('unv',None);urls('deepseek__deepseekmoe-16b','DeepSeekMoE 16B','B')
R['deepseek__deepseek-r1-lite-preview']['note']='retirement date not stated by DeepSeek; api-docs dates release 20 Nov 2024, deepseek.com news header 19 Nov';
g=R['xai__grok-1-5'];g['basis']='announcement';g['note']='first availability not on a vendor page (x.ai says "in the coming days"); 28 Mar 2024 is the announcement'
g=R['xai__grok-4-20-multi-agent'];g.update(conf='medium',note='docs.x.ai release notes 10 Mar 2026; model page titled Beta; no GA stated');urls('xai__grok-4-20-multi-agent','xAI Grok 4.20 multi-agent','B')
g=R['openai__gpt-6-astra-pro'];g.update(note='no separate start date or API ID on a vendor page; likely a higher-compute mode of Astra; openai.com metadata 8 Aug vs help centre 3 Sep');
R['openai__gpt-6-astra']['note']=(R['openai__gpt-6-astra'].get('note','')+'; openai.com page metadata shows 8 Aug 2026, help centre 3 Sep').lstrip('; ')
# derived ga
for d in R.values():
    d['dev']=dev[d['id'].split('__')[0]];d['name']=d.get('vn') or names.get(d['id']) or d['id'].split('__')[1]
    if d['st']=='ga' and not d.get('ga') and d.get('fa'): d['ga']=d['fa']
    if d['st']=='open_weights_release' and not d.get('wt') and d.get('fa'): d['wt']=d['fa']
    # counting rule
    s=d['st'];reason=None
    if s=='ga': cd,b=d.get('fa'),'first available'
    elif s=='open_weights_release': cd,b=d.get('wt') or d.get('fa'),'open-weights release'
    else:
        cd,b=d.get('ga'),'general availability'
        if not cd and d.get('wt'): cd,b=d['wt'],'open-weights release (weights are public)'
        if not cd: reason=f'{s} at launch and no GA date verified'
    if d.get('basis')=='announcement': cd,b=d['an'],'announcement (first availability not stated)'
    if not cd and not reason: reason='no verified date'
    if cd and not ('2023-03-14'<=cd<='2026-10-07'): reason=f'outside window ({cd})'
    d['ci']=d.get('wt') if (d['st']=='open_weights_release' and d.get('wt')) else (d.get('fa') or d.get('an'))
    d['cd']=cd;d['cb']=b;d['counted']=0 if reason else 1;d['why']=reason
    d['allsrc']=sorted(set([u for u in ([d.get('src'),d.get('card')]+srcs.get(d['id'],[])) if u]))
rows=sorted(R.values(),key=lambda r:(r['dev'].lower(),r.get('cd') or r.get('fa') or r.get('an') or '9'))
json.dump(rows,open('../v4out/models.json','w'),separators=(',',':'))
import collections
print('inclusive',sum(1 for r in rows if r.get('ci') and '2023-03-14'<=r['ci']<='2026-10-07'))
print(len(rows),sum(r['counted'] for r in rows))
print(collections.Counter(r['dev'] for r in rows if r['counted']))
for r in rows:
    if not r['counted']:print(' EXCL',r['id'],'|',r['why'])
