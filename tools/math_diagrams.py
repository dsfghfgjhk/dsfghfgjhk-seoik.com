"""Text-based, redrawn figures for uploaded mathematics papers."""
import math

def svg(body,label,w=260,h=200):
 return f'<div class="math-diagram"><svg xmlns="http://www.w3.org/2000/svg" style="display:block;width:min(100%,{w}px);height:auto;margin:10px auto" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{body}</svg></div>'
def cards(labels):
 width=len(labels)*32+10
 return svg('<g fill="white" stroke="currentColor">'+''.join(f'<rect x="{5+i*32}" y="8" width="27" height="38" rx="2"/>' for i in range(len(labels)))+'</g><g fill="currentColor" font-size="17">'+''.join(f'<text x="{18.5+i*32}" y="34" text-anchor="middle">{v}</text>' for i,v in enumerate(labels))+'</g>','숫자와 문자가 적힌 카드 '+', '.join(map(str,labels)),width,55)
def line(fn,x0,x1,step=.05,ox=30,oy=180,scale=40):
 xs=[x0+(x1-x0)*i/round((x1-x0)/step) for i in range(round((x1-x0)/step)+1)]
 return ' '.join(('M' if i==0 else 'L')+f'{ox+scale*x:.1f},{oy-scale*fn(x):.1f}' for i,x in enumerate(xs))

def grade2_4():
 labels='<g fill="currentColor" font-size="13"><text x="40" y="15">X</text><text x="210" y="15">X</text><text x="120" y="15">f</text>'+''.join(f'<text x="55" y="{36+28*i}">{i+1}</text><text x="196" y="{36+28*i}">{i+1}</text>' for i in range(5))+'</g>'
 arrows=''.join(f'<path d="M69 {32+28*i} L187 {32+28*(j-1)}" marker-end="url(#arrow-g2-4)"/>' for i,j in enumerate([3,1,5,2,4]))
 return svg('<defs><marker id="arrow-g2-4" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="currentColor"/></marker></defs><g fill="none" stroke="currentColor"><ellipse cx="59" cy="87" rx="26" ry="76"/><ellipse cx="202" cy="87" rx="26" ry="76"/>'+arrows+'</g>'+labels,'함수 대응도: 1은 3, 2는 1, 3은 5, 4는 2, 5는 4에 대응',260,175)
def grade2_12():
 f=line(lambda x:2*math.sqrt(x),0,4.4);g=line(lambda x:x*x/4,0,4.3)
 return svg(f'<g fill="none" stroke="currentColor" stroke-width="1.1"><path d="M10 180 H235 M30 192 V8 {f} {g} M30 180 L190 20 M40 140 L110 140 M40 140 L190 20 L110 140 M10 140 H230"/></g><g font-size="12" fill="currentColor"><text x="19" y="195">O</text><text x="195" y="12">A</text><text x="34" y="155">B</text><text x="67" y="155">P</text><text x="108" y="155">C</text><text x="210" y="184">x</text><text x="18" y="13">y</text><text x="151" y="53">f</text><text x="190" y="54">g</text></g>','곡선 f와 g, 교점 O와 A, 수평선 위의 B P C',245,205)
def grade2_14():
 return svg('<g fill="none" stroke="currentColor" stroke-width="1.2"><path d="M12 170 H240 M30 187 V8 M30 170 L188 12 M70 170 L76.7 123.3 L142 114"/><circle cx="170" cy="110" r="28.3"/></g><g fill="currentColor" font-size="12"><text x="19" y="185">O</text><text x="67" y="185">A</text><text x="67" y="120">Q</text><text x="137" y="108">P</text><text x="201" y="108">C</text><text x="178" y="28">y=x</text><text x="230" y="183">x</text><text x="20" y="14">y</text></g>','원 C와 직선 y=x, 점 A Q P',245,200)
def grade2_17():
 m=2-math.sqrt(3); hx=3*(1+m)/(1+m*m);hy=m*hx; bx=hx-math.sqrt(4.5)/math.sqrt(1+m*m);by=m*bx
 x=lambda v:30+26*v;y=lambda v:200-26*v
 return svg(f'<g fill="none" stroke="currentColor" stroke-width="1.1"><path d="M12 200 H240 M30 215 V5 M30 200 L230 {y(m*(200/26)):.2f} M{x(3):.2f} {y(3):.2f} L{x(hx):.2f} {y(hy):.2f}"/><circle cx="108" cy="122" r="78"/></g><g fill="currentColor" font-size="12"><text x="18" y="214">O</text><text x="102" y="117">A</text><text x="{x(bx)-8:.1f}" y="{y(by)-6:.1f}">B</text><text x="{x(hx):.1f}" y="{y(hy)+15:.1f}">H</text><text x="180" y="52">C</text><text x="190" y="{y(m*(160/26))-8:.1f}">y=mx</text><text x="232" y="214">x</text><text x="18" y="12">y</text></g>','원 C와 직선 y=mx의 교점 B, 중심 A, 수선의 발 H',250,225)
def chairs():
 parts=[]
 for row in range(4):
  for col in range(2):
   x=48+col*65;y=8+(3-row)*40;num=(row+1)*10+col+1
   parts.append(f'<rect x="{x}" y="{y}" width="42" height="30" rx="5"/><text x="{x+21}" y="{y+21}" text-anchor="middle" fill="currentColor" stroke="none">{num}</text>')
 return svg('<g fill="none" stroke="currentColor">'+''.join(parts)+'</g>','좌석 배치: 앞에서부터 11 12, 21 22, 31 32, 41 42',200,175)
def activity_table():
 labels=['종목','월','화','수','목','금'];cells=''
 for r in range(5):
  for c in range(6):
   x=8+c*36;y=30+r*24;v=labels[c] if r==0 else ('ABCD'[r-1] if c==0 else '')
   cells+=f'<rect x="{x}" y="{y}" width="36" height="24"/><text x="{x+18}" y="{y+16}" text-anchor="middle" stroke="none" fill="currentColor">{v}</text>'
 return svg('<text x="116" y="20" text-anchor="middle" fill="currentColor" font-size="13">스포츠 활동 신청서</text><g stroke="currentColor" fill="none" font-size="11">'+cells+'</g>','스포츠 활동 신청서: 월요일부터 금요일까지 종목 A B C D',232,158)
def boxes_balls():
 boxes=''.join(f'<rect x="{8+i*32}" y="20" width="32" height="39"/><text x="{24+i*32}" y="45" text-anchor="middle" fill="currentColor" stroke="none">{i+1}</text>' for i in range(7))
 balls=''.join(f'<circle cx="{38+i*39}" cy="85" r="13"/><text x="{38+i*39}" y="90" text-anchor="middle" fill="currentColor" stroke="none">{chr(65+i)}</text>' for i in range(5))
 return svg('<g fill="none" stroke="currentColor" font-size="13">'+boxes+balls+'</g>','1부터 7까지 적힌 빈 상자와 A B C D E 공',240,108)
FIGURES={
 '2026년 3월 고2 4번':grade2_4,
 '2026년 3월 고2 12번':grade2_12,
 '2026년 3월 고2 14번':grade2_14,
 '2026년 3월 고2 17번':grade2_17,
 '2026년 3월 고2 27번':chairs,
 '2025년 9월 고1 21번':activity_table,
 '2026년 9월 고1 20번':boxes_balls,
 '2025년 9월 고1 29번':lambda:cards(list(range(1,9))),
 '2025년 10월 고1 25번':lambda:cards(list(range(1,7))),
 '2026년 10월 고1 21번':lambda:cards([1,2,3,4,'A','B','C']),
 '2026년 9월 고1 17번':lambda:cards(list(range(1,8))),
}
def with_figure(q):
 q=dict(q)
 fig=FIGURES.get(q.get('source'))
 if fig and '<svg' not in q.get('q',''):q['q']+=fig()
 return q
