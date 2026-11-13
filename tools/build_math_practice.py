import json, random
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def item(q,answer,explain,points,source):
    opts=[answer-2,answer-1,answer,answer+1,answer+2]
    random.Random(q).shuffle(opts)
    return {'q':q,'choices':list(map(str,opts)),'correct':opts.index(answer),'points':points,'explain':explain,'source':'변형 · '+source,'fixed':True}
def make(course,n):
    a=n+2;b=n+3
    if course==1:
        return [
          item(f'P(x) = x² + {a}x + {b}를 x − 2로 나눈 나머지는?',4+2*a+b,f'나머지정리로 P(2) = 4 + 2×{a} + {b} = {4+2*a+b}이다.',2,'2025년 10월 고1 9번'),
          item(f'이차방정식 x² − {a+b}x + {a*b} = 0의 두 근의 제곱의 합은?',a*a+b*b,f'두 근은 {a}, {b}이므로 제곱의 합은 {a*a+b*b}이다.',3,'이차방정식 근과 계수'),
          item(f'항등식 x² + kx + {a*b} = (x + {a})(x + {b})일 때, k의 값은?',a+b,f'우변을 전개하면 x의 계수는 {a} + {b} = {a+b}이다.',2,'2025년 10월 고1 4번'),
          item(f'두 행렬 A = [[{a}, 1], [0, {b}]], B = [[1, 2], [3, 0]]에 대하여 A + 2B의 모든 성분의 합은?',a+b+13,f'A + 2B = [[{a+2}, 5], [6, {b}]]이므로 합은 {a+b+13}이다.',3,'2025년 10월 고1 3번'),
          item(f'이차방정식 x² − {a+b}x + {a*b} = 0의 두 근을 α, β라 할 때 α⁴ + β⁴의 값은?',a**4+b**4,f'두 근은 {a}, {b}이므로 α⁴ + β⁴ = {a}⁴ + {b}⁴ = {a**4+b**4}이다.',4,'근과 계수를 활용한 변형')]
    return [
      item(f'좌표평면 위의 두 점 (0, 0), ({a}, {b}) 사이의 거리의 제곱은?',a*a+b*b,f'거리의 제곱은 {a}² + {b}² = {a*a+b*b}이다.',2,'2025년 10월 고1 2번'),
      item(f'점 ({a}, {b})를 x축 방향으로 3, y축 방향으로 −2만큼 평행이동한 점의 두 좌표의 합은?',a+b+1,f'이동한 점은 ({a+3}, {b-2})이므로 합은 {a+b+1}이다.',3,'2025년 10월 고1 5번'),
      item(f'직선 y = ({a} − k)x + 1이 직선 y = −2x + 3과 평행할 때 k의 값은?',a+2,f'평행한 두 직선의 기울기가 같으므로 {a} − k = −2, k = {a+2}이다.',2,'2025년 10월 고1 22번'),
      item(f'두 점 A(0, 0), B({3*a}, {3*b})를 1 : 2로 내분하는 점의 두 좌표의 합은?',a+b,f'내분점은 ({a}, {b})이므로 합은 {a+b}이다.',3,'2026년 10월 고1 8번'),
      item(f'원 (x − {a})² + (y − {b})² = 25의 중심을 점 P라 할 때, 점 P를 원점에 대하여 대칭이동한 점과 ({a}, {b}) 사이의 거리의 제곱은?',4*(a*a+b*b),f'중심 P = ({a}, {b}), 대칭점은 (−{a}, −{b})이다. 거리의 제곱은 (2×{a})² + (2×{b})² = {4*(a*a+b*b)}이다.',4,'2025년 10월 고1 21번')]
sets={str(c):[[] for _ in range(2)] for c in (1,2)}
for c in (1,2):
 for n in range(10): sets[str(c)][n//5].extend(make(c,n))
for blocks in sets.values():
 for block in blocks:
  random.Random(20261113+len(block)+sum(q['correct'] for q in block)).shuffle(block)
  assert len(block)==25 and all(len(set(q['choices']))==5 for q in block)
(root/'math/practice-extra.js').write_text('window.SEOIK_PRACTICE_EXTRA = '+json.dumps(sets,ensure_ascii=False,separators=(',',':'))+';\n')
