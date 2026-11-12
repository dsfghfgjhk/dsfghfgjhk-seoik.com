import fitz,pathlib,re,json
import argparse
p=argparse.ArgumentParser();p.add_argument('pdf_directory',type=pathlib.Path);p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[1]/'math');args=p.parse_args()
root=args.output;src=args.pdf_directory;(root/'assets').mkdir(parents=True,exist_ok=True)
def sections(path,solution,stem):
 d=fitz.open(path);marks=[]
 for pi,p in enumerate(d):
  for b in p.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    t=''.join(s['text'] for s in l['spans']);m=re.match(r'^(\d+)\.\s*'+(r'\[출제의도\]' if solution else ''),t)
    if m and 1<=int(m[1])<=30:marks.append(dict(n=int(m[1]),p=pi,x=l['bbox'][0],y=l['bbox'][1],title=t))
 xs=[]
 for m in sorted(marks,key=lambda a:a['x']):
  if not xs or abs(m['x']-xs[-1])>25:xs.append(m['x'])
 assert len({m['n'] for m in marks})==30,(path,len(marks))
 for m in marks:m['c']=min(range(len(xs)),key=lambda c:abs(xs[c]-m['x']))
 marks.sort(key=lambda a:(a['p'],a['c'],a['y']));out={}
 for i,m in enumerate(marks):
  end=marks[i+1] if i+1<len(marks) else dict(p=len(d)-1,c=len(xs)-1,y=d[-1].rect.height-45)
  imgs=[]
  for pi in range(m['p'],end['p']+1):
   for c,x in enumerate(xs):
    if (pi,c)<(m['p'],m['c']) or (pi,c)>(end['p'],end['c']):continue
    y0=m['y']-3 if (pi,c)==(m['p'],m['c']) else 60
    y1=end['y']-5 if (pi,c)==(end['p'],end['c']) else d[pi].rect.height-45
    if y1<=y0:continue
    x1=xs[c+1]-8 if c+1<len(xs) else d[pi].rect.width-(45 if solution else 70)
    rect=fitz.Rect(x-4,y0,x1,y1)&d[pi].rect
    filename=f'{stem}-{m["n"]}-{len(imgs)}.png';d[pi].get_pixmap(matrix=fitz.Matrix(2,2),clip=rect,alpha=False).save(root/'assets'/filename);imgs.append('assets/'+filename)
  out[m['n']]=dict(images=imgs,title=re.sub(r'^\d+\.\s*\[출제의도\]\s*','',m['title']))
 return out
units=[('도형의 방정식',r'거리|직선의 평행|위치 관계|내분|대칭이동|평행이동|원의 방정식|원과 직선'),('행렬',r'행렬'),('경우의 수',r'순열|조합|합의 법칙|곱의 법칙'),('다항식',r'다항식|항등식|나머지|인수|곱셈\s*공식')]
hints={'도형의 방정식':'좌표와 조건을 먼저 정리하세요. 거리·기울기·내분점 공식을 적용하고, 원과 직선의 위치 관계는 중심에서 직선까지의 거리와 반지름을 비교하세요.','행렬':'행과 열의 위치를 확인하세요. 같은 행렬은 대응하는 성분이 같고, 곱셈은 앞 행렬의 행과 뒤 행렬의 열을 차례로 곱해 더합니다.','경우의 수':'순서를 구별하는지 먼저 판단하세요. 겹치지 않는 경우는 더하고, 연속 선택은 곱합니다. 중복과 빠진 경우가 없는지 확인하세요.','다항식':'동류항을 정리하고 조건을 식으로 바꾸세요. 나머지정리는 나누는 식의 근을 대입하고, 항등식은 계수를 비교하거나 알맞은 값을 대입합니다.','방정식과 부등식':'식을 정리한 뒤 근·판별식·그래프 중 적절한 도구를 선택하세요. 부등식은 경계값의 포함 여부를, 최대·최소는 정의역과 꼭짓점 위치를 확인하세요.'}
records=[]
for year in [25,26]:
 for month in [6,9,10]:
  stem=f'{year}-{month}';q=sections(next(src.rglob(f'{year}년 고1 {month}모 수학.pdf')),False,stem+'q');a=sections(next(src.rglob(f'{year}년 고1 {month}모 수학 해설.pdf')),True,stem+'a')
  for n in range(1,31):
   title=a[n]['title'];unit=next((u for u,rx in units if re.search(rx,title)),'방정식과 부등식')
   # A line's position relative to a quadratic graph belongs to Common Math 1.
   if '이차' in title:unit='방정식과 부등식'
   course=2 if unit=='도형의 방정식' else 1
   records.append(dict(id=f'{stem}-{n}',year=2000+year,month=month,number=n,course=course,unit=unit,title=title,question=q[n]['images'],solution=a[n]['images'],hint=hints[unit]))
(root/'questions.json').write_text(json.dumps(records,ensure_ascii=False))
print('questions',len(records),'courses',{i:sum(r['course']==i for r in records) for i in [1,2]})
