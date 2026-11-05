import json,csv,datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.table import Table,TableStyleInfo
from openpyxl.formatting.rule import CellIsRule,DataBarRule
R=json.load(open('models.json'))
ORDER=sorted({r['dev'] for r in R},key=str.lower)
R.sort(key=lambda r:(r['dev'].lower(),r.get('cd') or r.get('ci') or '9',r['name']))
D=lambda s:dt.datetime.strptime(s,'%Y-%m-%d').date() if s else None
STG={'ga':'General availability','open_weights_release':'Open weights','preview':'Preview','beta':'Beta','experimental':'Experimental','gated':'Gated / limited access'}
ARC={'moe':'Mixture of experts','dense':'Dense'};MM={'t':'text','i':'image','a':'audio','v':'video','pdf':'PDF'}
cols=[('Developer','dev',16,'t'),('Model','name',34,'t'),('Stage at launch','st',20,'s'),
('Counted (strict rule)','counted',11,'y'),('Count date','cd',13,'d'),('Count basis','cb',26,'t'),('Reason not counted','why',34,'t'),('Date if any stage counted','ci',13,'d'),
('Announced','an',13,'d'),('First available','fa',13,'d'),('General availability','ga',13,'d'),('API available','api',13,'d'),('Open weights','wt',13,'d'),
('Status','stat',12,'t'),('Retired on','ret',13,'d'),('Replaced by','rep',22,'t'),
('Context window (tokens)','ctx',14,'n'),('Max output (tokens)','mx',13,'n'),('Knowledge cutoff','ck',12,'t'),
('Input $ / 1M tokens','pi',11,'p'),('Cached input $ / 1M','pc',11,'p'),('Output $ / 1M tokens','po',11,'p'),
('Licence','lic',22,'t'),('Params total (B)','pt',10,'g'),('Params active (B)','pa',10,'g'),('Architecture','ar',18,'a'),('Input modalities','mi',16,'m'),('Reasoning','rm',11,'t'),
('Available on','plat',28,'t'),('API model ID','apiid',26,'t'),('Variant of','snap',26,'t'),('Vendor page','src',40,'l'),('Model card','card',40,'l'),('Confidence','conf',11,'t'),('Verified','unv',11,'v'),('Notes','note',60,'t'),('Model key','id',34,'t')]
F='Arial';hf=Font(name=F,bold=True,color='FFFFFF',size=10);hfill=PatternFill('solid',fgColor='2A3F5F');body=Font(name=F,size=10)
wb=Workbook();ws=wb.active;ws.title='Models';ws.append([c[0] for c in cols])
for r in R:
    row=[]
    for h,k,w,t in cols:
        v=r.get(k)
        if v in (None,''):row.append(None);continue
        if t=='d':v=D(v)
        elif t=='s':v=STG.get(v,v)
        elif t=='a':v=ARC.get(v,v)
        elif t=='y':v='Yes' if v else 'No'
        elif t=='v':v='Unverified' if v else None
        elif t=='m':v=', '.join(MM.get(x,x) for x in v.split(','))
        elif k=='plat':v=v.replace(',',', ')
        row.append(v)
    ws.append(row)
n=len(R)+1;ix={c[1]:i+1 for i,c in enumerate(cols)}
for i,(h,k,w,t) in enumerate(cols,1):
    c=ws.cell(1,i);c.font=hf;c.fill=hfill;c.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center');ws.column_dimensions[L(i)].width=w
    for rr in range(2,n+1):
        c=ws.cell(rr,i);c.font=body;c.alignment=Alignment(vertical='top',wrap_text=(k=='note'),horizontal='right' if t in 'npg' else ('center' if t in 'dy' else 'left'))
        if t=='d':c.number_format='dd mmm yyyy'
        elif t=='n':c.number_format='#,##0'
        elif t=='p':c.number_format='$#,##0.00#'
        elif t=='g':c.number_format='#,##0.0'
        elif t=='l' and c.value:c.hyperlink=c.value;c.font=Font(name=F,size=10,color='0563C1',underline='single')
ws.row_dimensions[1].height=44;ws.freeze_panes='C2'
t=Table(displayName='Models',ref=f'A1:{L(len(cols))}{n}');t.tableStyleInfo=TableStyleInfo(name='TableStyleLight1',showRowStripes=True);ws.add_table(t)
for txt,col in [('active','D9EAD3'),('legacy','FFF2CC'),('deprecated','FCE5CD'),('retired','EDEDED')]:
    c=L(ix['stat']);ws.conditional_formatting.add(f'{c}2:{c}{n}',CellIsRule(operator='equal',formula=[f'"{txt}"'],fill=PatternFill('solid',bgColor=col)))
c=L(ix['counted']);ws.conditional_formatting.add(f'{c}2:{c}{n}',CellIsRule(operator='equal',formula=['"No"'],fill=PatternFill('solid',bgColor='F4CCCC')))
col=lambda k:f"Models!${L(ix[k])}$2:${L(ix[k])}${n}"
# README
rd=wb.create_sheet('Read me',0)
txt=[('AI model releases, 14 March 2023 to 7 October 2026',1),('224 general-purpose models from eight developers, listed alphabetically by developer and then by date. One row per model. Retrieved 5 November 2026.',0),('',0),
('Sheets',1),('Models: the data. Filter with the header arrows; the first two columns stay frozen.',0),('Counts: models per developer and year, computed live from Models under the strict rule, plus the last-12-months comparison.',0),('Compare versions: first-public dates in versions v1, v2, v3 and v4 side by side; the spread and a change flag are formulas.',0),('Not counted: models in the list but outside the strict count, with the reason.',0),('Coverage: how complete each field is. Fields / Sources: dictionary and every URL used.',0),('',0),
('Rules',1),('First available: first date the public could use the model, from the vendor\'s own page, changelog or release notes. Third-party trackers were used only to settle conflicts between vendor pages.',0),
('Strict count rule: a model counts once, at its first date of general availability. General-availability launches count at first availability; open-weights releases at the weights date; preview, beta, experimental and gated launches count at their verified GA date, or are not counted if none is verified.',0),
('Inclusive count: every model counted at its first date whatever its stage ("Date if any stage counted"). Both are given because the choice changes the totals; the choice is the author\'s.',0),
('Where two vendor pages disagree, the Notes column gives both dates and the one kept. Prices are USD per million tokens. Blank means not verified, never zero.',0),
('Rows marked Unverified, or Confidence low, were not confirmed against a vendor page and should not be cited without checking. Specialised lines (code, maths, speech, image, OCR) and restricted releases are out of scope.',0)]
for i,(s,b) in enumerate(txt,1):
    c=rd.cell(i,1,s);c.font=Font(name=F,size=14 if i==1 else 11,bold=bool(b));c.alignment=Alignment(wrap_text=True,vertical='top')
rd.column_dimensions['A'].width=125;rd.sheet_view.showGridLines=False
# Counts
ct=wb.create_sheet('Counts');years=[2023,2024,2025,2026]
ct.append(['Developer']+[str(y) for y in years]+['Total'])
for j,d in enumerate(ORDER,2):
    ct.cell(j,1,d)
    for k,y in enumerate(years,2):
        ct.cell(j,k,f'=COUNTIFS({col("dev")},$A{j},{col("counted")},"Yes",{col("cd")},">="&DATE({y},1,1),{col("cd")},"<="&DATE({y},12,31))')
    ct.cell(j,6,f'=SUM(B{j}:E{j})')
tr=len(ORDER)+2;ct.cell(tr,1,'Total')
for k in range(2,7):ct.cell(tr,k,f'=SUM({L(k)}2:{L(k)}{tr-1})')
ct.cell(tr+1,1,'Inclusive (any stage)')
for k,y in enumerate(years,2):ct.cell(tr+1,k,f'=COUNTIFS({col("ci")},">="&DATE({y},1,1),{col("ci")},"<="&DATE({y},12,31))')
ct.cell(tr+1,6,f'=SUM(B{tr+1}:E{tr+1})')
b=tr+4
ct.cell(b,1,'Last 12 months vs previous 12 months (strict)').font=Font(name=F,bold=True)
ct.cell(b+1,1,'8 Oct 2025 to 7 Oct 2026');ct.cell(b+1,2,f'=COUNTIFS({col("counted")},"Yes",{col("cd")},">="&DATE(2025,10,8),{col("cd")},"<="&DATE(2026,10,7))')
ct.cell(b+2,1,'8 Oct 2024 to 7 Oct 2025');ct.cell(b+2,2,f'=COUNTIFS({col("counted")},"Yes",{col("cd")},">="&DATE(2024,10,8),{col("cd")},"<="&DATE(2025,10,7))')
ct.cell(b+3,1,'Change');ct.cell(b+3,2,f'=B{b+1}/B{b+2}-1');ct.cell(b+3,2).number_format='0%'
ct.cell(b+4,1,'Two-sided exact binomial p (H0: equal)');ct.cell(b+4,2,f'=MIN(1,2*MIN(_xlfn.BINOM.DIST(B{b+1},B{b+1}+B{b+2},0.5,TRUE),1-_xlfn.BINOM.DIST(B{b+1}-1,B{b+1}+B{b+2},0.5,TRUE)))');ct.cell(b+4,2).number_format='0.00'
ct.cell(b+6,1,'Models in the list but not counted (strict)');ct.cell(b+6,2,f'=COUNTIF({col("counted")},"No")')
for row in ct.iter_rows():
    for c in row:
        if c.value is not None and not c.font.bold:c.font=body
for k in range(1,7):
    ct.cell(1,k).font=hf;ct.cell(1,k).fill=hfill
for x in (tr,tr+1):ct.cell(x,1).font=Font(name=F,bold=True,size=10)
ct.column_dimensions['A'].width=44
for x in 'BCDEF':ct.column_dimensions[x].width=12
# Compare versions
cmp=wb.create_sheet('Compare versions')
cmp.append(['Developer','Model','v1','v2','v3 (consensus)','v4 first available','v4 count date','Spread v1-v4 (days)','Changed since v1?','Model key'])
vers={}
for r in csv.DictReader(open('../out/AI_model_releases_long_v1_v2.csv',encoding='utf-8-sig')):vers.setdefault(r['model_id'],{})[r['version']]=r['first_public_date']
for r in R:
    v=vers.get(r['id'],{});cmp.append([r['dev'],r['name'],D(v.get('v1')),D(v.get('v2')),D(v.get('v3_proposed')),D(r.get('fa')),D(r.get('cd')),None,None,r['id']])
m=len(R)+1
for rr in range(2,m+1):
    cmp.cell(rr,8,f'=IF(COUNT(C{rr}:F{rr})<2,"",MAX(C{rr}:F{rr})-MIN(C{rr}:F{rr}))');cmp.cell(rr,9,f'=IF(H{rr}="","",IF(H{rr}=0,"No","Yes"))')
    for k in range(1,11):
        c=cmp.cell(rr,k);c.font=body
        if 3<=k<=7:c.number_format='dd mmm yyyy';c.alignment=Alignment(horizontal='center')
for k in range(1,11):c=cmp.cell(1,k);c.font=hf;c.fill=hfill;c.alignment=Alignment(wrap_text=True,horizontal='center',vertical='center')
for x,w in zip('ABCDEFGHIJ',(16,34,13,13,14,14,14,13,12,34)):cmp.column_dimensions[x].width=w
cmp.freeze_panes='C2';cmp.auto_filter.ref=f'A1:J{m}';cmp.row_dimensions[1].height=32
cmp.conditional_formatting.add(f'I2:I{m}',CellIsRule(operator='equal',formula=['"Yes"'],fill=PatternFill('solid',bgColor='FFF2CC')))
# Not counted (static list, with reasons)
nc=wb.create_sheet('Not counted');nc.append(['Developer','Model','Stage at launch','First available','Reason'])
for r in R:
    if not r['counted']:nc.append([r['dev'],r['name'],STG.get(r['st'],r['st']),D(r.get('fa') or r.get('an')),r['why']])
for row in nc.iter_rows(min_row=2):
    for c in row:c.font=body
    row[3].number_format='dd mmm yyyy'
for k in range(1,6):c=nc.cell(1,k);c.font=hf;c.fill=hfill
for x,w in zip('ABCDE',(16,40,24,14,50)):nc.column_dimensions[x].width=w
nc.freeze_panes='A2'
# Coverage
cv=wb.create_sheet('Coverage');cv.append(['Field','Filled','Total models','Fill rate'])
for c in cv[1]:c.font=hf;c.fill=hfill
for i,(h,k,w,t) in enumerate(cols,1):
    if h in('Developer','Model','Model key'):continue
    r=cv.max_row+1;cv.cell(r,1,h);cv.cell(r,2,f'=COUNTA(Models!{L(i)}2:{L(i)}{n})');cv.cell(r,3,f'=COUNTA(Models!$B$2:$B${n})');cv.cell(r,4,f'=B{r}/C{r}');cv.cell(r,4).number_format='0%'
for row in cv.iter_rows(min_row=2):
    for c in row:c.font=body
cv.column_dimensions['A'].width=30
for x in 'BCD':cv.column_dimensions[x].width=14
cv.conditional_formatting.add(f'D2:D{cv.max_row}',DataBarRule(start_type='num',start_value=0,end_type='num',end_value=1,color='5B8DEF'))
cv.freeze_panes='A2';cv.cell(cv.max_row+2,1,'A low rate is a gap at the vendor source or not yet verified, not a zero.').font=Font(name=F,italic=True,size=10)
# Fields
desc={'Counted (strict rule)':'Yes if the model counts under the strict rule (see Read me).','Count date':'Date at which a counted model is counted.','Count basis':'Which date was used: first available, open-weights release or general availability.','Reason not counted':'Why a strict count excludes the model.','Date if any stage counted':'First available (or weights) date used for the inclusive count.','Stage at launch':'Release stage when first public, as the vendor labels it.','Announced':'Vendor announcement date.','First available':'First date the public could use the model, from the vendor page.','General availability':'Date of full GA. Equals first available where the model launched as GA.','API available':'First date available through the vendor API.','Open weights':'Date weights were published.','Status':'active, legacy, deprecated or retired per vendor.','Retired on':'Vendor retirement date (scheduled where the note says so).','Replaced by':'Vendor-named successor.','Context window (tokens)':'Maximum input context.','Max output (tokens)':'Maximum generated tokens.','Knowledge cutoff':'Training data cutoff, YYYY-MM.','Input $ / 1M tokens':'USD per million input tokens.','Cached input $ / 1M':'USD per million cached input tokens.','Output $ / 1M tokens':'USD per million output tokens.','Licence':'Weights licence or proprietary.','Params total (B)':'Total parameters, billions.','Params active (B)':'Active parameters per token, billions.','Architecture':'Dense or mixture of experts.','Input modalities':'text, image, audio, video, PDF.','Reasoning':'Reasoning mode if the vendor states one.','Available on':'Platforms.','API model ID':'String used in API calls.','Variant of':'Parent model if a size variant or snapshot.','Vendor page':'Primary vendor source.','Model card':'Model or system card.','Confidence':'high, medium or low, from how directly vendor sources state the facts.','Verified':'Unverified where not confirmed against a vendor page.','Notes':'Conflicts, caveats, alternative dates.','Model key':'Stable identifier developer__model-slug; joins versions.'}
fl=wb.create_sheet('Fields');fl.append(['Column','Meaning'])
for c in fl[1]:c.font=hf;c.fill=hfill
for h,*_ in cols:
    if h in desc:fl.append([h,desc[h]])
for row in fl.iter_rows(min_row=2):
    for c in row:c.font=body;c.alignment=Alignment(wrap_text=True,vertical='top')
fl.column_dimensions['A'].width=28;fl.column_dimensions['B'].width=100
# Sources
so=wb.create_sheet('Sources');so.append(['Developer','Model','URL','Retrieved'])
for c in so[1]:c.font=hf;c.fill=hfill
for r in R:
    for u in r.get('allsrc',[]):
        so.append([r['dev'],r['name'],u,dt.date(2026,11,5)]);c=so.cell(so.max_row,3);c.hyperlink=u;c.font=Font(name=F,size=10,color='0563C1',underline='single');so.cell(so.max_row,4).number_format='dd mmm yyyy'
        for k in (1,2):so.cell(so.max_row,k).font=body
for x,w in zip('ABCD',(16,34,90,13)):so.column_dimensions[x].width=w
so.freeze_panes='A2';so.auto_filter.ref=f'A1:D{so.max_row}'
wb.save('AI_model_releases_v4.xlsx')
# CSV master (machine)
keys=[c[1] for c in cols]
with open('AI_model_releases_v4.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(keys)
    for r in R:w.writerow([('' if r.get(k) is None else r.get(k)) for k in keys])
print(n-1,'rows',sum(len(r.get('allsrc',[])) for r in R),'source urls')
