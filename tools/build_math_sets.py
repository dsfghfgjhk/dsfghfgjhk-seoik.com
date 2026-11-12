import json,math
from pathlib import Path
root = Path(__file__).resolve().parents[1]
v=json.loads((root/'math/variants.json').read_text())
def item(text,answer,explain,points,source=None):
 answer=int(answer); opts=[str(answer-2),str(answer-1),str(answer),str(answer+1),str(answer+2)]
 return dict(q=text,choices=opts,correct=2,explain=explain,points=points,source=source)
def fromvar(x,points):return item(x['problem'],x['answer'],x['explanation'],points,x['source'])
c1=[fromvar(x,2 if i<5 else 3) for i,x in enumerate([x for x in v if x['course']==1])]
for a,b in [(2,4),(3,5),(4,6)]:
 c1.append(item(f'다항식 P(x) = x² + {a}x + {b}를 x − 2로 나눈 나머지는?',4+2*a+b,f'나머지정리에 따라 P(2) = 2² + {a}×2 + {b} = {4+2*a+b}이다.',3))
for a,b in [(2,3),(3,4),(4,5)]:
 c1.append(item(f'방정식 x² − {a+b}x + {a*b} = 0의 두 근의 제곱의 합은?',a*a+b*b,f'좌변은 (x − {a})(x − {b})로 인수분해된다. 두 근은 {a}, {b}이고 제곱의 합은 {a*a+b*b}이다.',3))
for a,b in [(1,2),(1,3),(2,3),(2,4),(3,4)]:
 ans=a**4+b**4
 c1.append(item(f'이차방정식 x² − {a+b}x + {a*b} = 0의 두 근을 α, β라 할 때 α⁴ + β⁴의 값은?',ans,f'근과 계수의 관계로 α + β = {a+b}, αβ = {a*b}이다. α² + β² = ({a+b})² − 2×{a*b} = {a*a+b*b}이고, α⁴ + β⁴ = ({a*a+b*b})² − 2×({a*b})² = {ans}이다.',4))
c2=[fromvar(x,2 if i<5 else 3) for i,x in enumerate([x for x in v if x['course']==2])]
for a,b in [(2,3),(3,4)]:c2.append(item(f'점 ({a}, {b})를 원점에 대하여 대칭이동한 점의 두 좌표의 합은?',-a-b,f'원점 대칭은 두 좌표의 부호를 모두 바꾼다. 대칭점은 (−{a}, −{b})이므로 합은 {-(a+b)}이다.',3))
for a,b in [(2,3),(3,5)]:c2.append(item(f'집합 A = {{{a}, {b}}}, B = {{{b}, {b+1}}}에 대하여 A ∪ B의 원소의 개수는?',3,f'합집합은 중복을 한 번만 세므로 {{{a}, {b}, {b+1}}}이고 원소는 3개이다.',3))
for a,b in [(2,3),(3,2)]:c2.append(item(f'함수 f(x) = {a}x + {b}에 대하여 f(2)의 값은?',2*a+b,f'x = 2를 대입하면 f(2) = {a}×2 + {b} = {2*a+b}이다.',3))
for a,b in [(1,4),(2,5)]:c2.append(item(f'원의 방정식 (x − {a})² + (y − {b})² = 16에서 중심의 두 좌표의 합은?',a+b,f'원의 중심은 ({a}, {b})이므로 두 좌표의 합은 {a+b}이다.',3))
for a,b in [(2,1),(3,2)]:c2.append(item(f'직선 y = {a}x + {b} 위에서 x = 2일 때 y의 값은?',2*a+b,f'x = 2를 대입하면 y = {a}×2 + {b} = {2*a+b}이다.',3))
for a,b in [(2,3),(3,4)]:c2.append(item(f'집합 A = {{1, 2, 3, 4, 5}}의 부분집합 중 원소의 개수가 {a}인 부분집합의 개수는?',math.comb(5,a),f'순서를 구별하지 않고 5개 중 {a}개를 선택하므로 ₅C{a} = {math.comb(5,a)}이다.',3))
for a,b in [(2,1),(3,2)]:c2.append(item(f'함수 f(x) = {a}x + {b}의 역함수 f⁻¹(x)에 대하여 f⁻¹({2*a+b})의 값은?',2,f'f(2) = {a}×2 + {b} = {2*a+b}이므로 역함수의 정의에 의해 f⁻¹({2*a+b}) = 2이다.',3))
for a,b in [(1,2),(2,3),(3,1),(1,4),(4,2)]:
 ans=(a+3)**2+(b+4)**2
 c2.append(item(f'점 P({a}, {b})를 x축 방향으로 3, y축 방향으로 4만큼 평행이동한 점을 Q라 할 때 원점을 중심으로 하고 Q를 지나는 원의 반지름의 제곱은?',ans,f'Q = ({a}+3, {b}+4) = ({a+3}, {b+4})이다. 원점과 Q 사이 거리의 제곱이 반지름의 제곱이므로 ({a+3})² + ({b+4})² = {ans}이다.',4))
assert len(c1)==len(c2)==25
for c in (c1,c2):assert [sum(x['points']==p for x in c) for p in (2,3,4)]==[5,15,5]
(root/'math/exam-sets.js').write_text('window.SEOIK_MATH_EXAMS = '+json.dumps({'1':c1,'2':c2},ensure_ascii=False,separators=(',',':'))+';\n')
print('created two 25-question sets, 75 points each')
