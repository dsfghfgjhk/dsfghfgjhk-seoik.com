import json,os,math
from pathlib import Path
os.chdir(Path(__file__).resolve().parents[1])
def line(fn,xs):return ' '.join(('M' if i==0 else 'L')+f'{62+25*x:.2f},{183-13*fn(x):.2f}' for i,x in enumerate(xs))
xs=[-2+i*.08 for i in range(106)]
f=line(lambda x:x*x-2*x+2,xs);g=line(lambda x:-x*x+8*x-6,xs)
fig=f'''<div class="math-diagram"><svg style="display:block;width:min(100%,240px);height:auto;margin:10px auto" viewBox="0 0 240 210" role="img" aria-label="두 이차함수 f와 g가 수평선 y=k와 각각 A B, C D에서 만나는 그래프"><defs><clipPath id="graph27"><rect x="0" y="0" width="240" height="210"/></clipPath></defs><g stroke="currentColor" fill="none" stroke-width="1.2" clip-path="url(#graph27)"><path d="{f} M0 76.4 H235 M10 183 H235 M62 205 V5 {g}"/></g><g fill="currentColor" font-size="12"><text x="16" y="90">A</text><text x="126" y="90">C</text><text x="151" y="90">B</text><text x="196" y="90">D</text><text x="50" y="197">O</text><text x="207" y="71">y=k</text><text x="226" y="196">x</text><text x="48" y="14">y</text></g></svg></div>'''
rows=[
('모든 실수 x에 대하여 (x + a)(x + 2) = x² + bx + 6이 성립할 때, a × b의 값을 구하시오. (단, a, b는 상수이다.)',15,3,'상수항에서 2a = 6이므로 a = 3이다. x의 계수는 b = a + 2 = 5이므로 ab = 15이다.'),
('x에 대한 부등식 |x − a| < 5의 해가 −4 < x < b일 때, a + b의 값을 구하시오. (단, a, b는 상수이다.)',7,3,'|x − a| < 5의 해는 a − 5 < x < a + 5이다. a − 5 = −4에서 a = 1이고 b = 6이므로 합은 7이다.'),
('이차함수 y = x² + ax + 5의 그래프가 x축과 만나는 서로 다른 두 점의 x좌표를 각각 α, β라 하자. (α − 1)(β − 1) = 12일 때, 상수 a의 값을 구하시오.',6,3,'근과 계수의 관계로 α + β = −a, αβ = 5이다. (α − 1)(β − 1) = αβ − (α + β) + 1 = 6 + a = 12이므로 a = 6이다.'),
('복소수 z = 1 − i에 대하여 (z̄/z)²ⁿ + (z/√2)²ⁿ = 0을 만족시키는 10 이하의 모든 자연수 n의 값의 합을 구하시오. (단, i = √−1이고, z̄는 z의 켤레복소수이다.)',18,3,'(z̄/z)² = −1, (z/√2)² = −i이다. 따라서 (−1)ⁿ + (−i)ⁿ = 0이다. 네 개씩 반복하는 값을 비교하면 n ≡ 2 (mod 4)이고, 10 이하에서는 2, 6, 10이므로 합은 18이다.'),
('다항식 x³ + (a + 2)x² + (a² − 3a + 2)x + b는 (x + 1){x² + (a + 1)x + b}로 인수분해되고, 이차방정식 x² + (a + 1)x + b = 0의 두 근을 α, β라 하자. α² + β² = 24일 때, a + b의 값을 구하시오. (단, a, b는 상수이다.)',11,4,'계수 비교로 b = a² − 4a + 1이다. 근과 계수의 관계를 쓰면 α² + β² = (a + 1)² − 2b = −a² + 10a − 1 = 24이다. 따라서 (a − 5)² = 0, a = 5, b = 6이므로 합은 11이다.'),
('직선 y = k가 이차함수 f(x) = x² − 2x + 2의 그래프와 서로 다른 두 점 A, B에서 만나고, 직선 y = k가 이차함수 g(x) = −x² + 8x − 6의 그래프와 서로 다른 두 점 C, D에서 만난다. AB = 2CD를 만족시키는 실수 k에 대하여 10k의 값을 구하시오. (단, 1 < k < 10)'+fig,82,4,'f(x) = k의 두 근의 합은 2, 곱은 2 − k이므로 AB² = 2² − 4(2 − k) = 4k − 4이다. g(x) = k의 두 근의 합은 8, 곱은 k + 6이므로 CD² = 8² − 4(k + 6) = 40 − 4k이다. AB² = 4CD²를 풀면 k = 41/5이고 10k = 82이다.'),
('다항식 A(x)와 최고차항의 계수가 1인 일차다항식 B(x)가 다음 조건을 만족시킨다.<div class="mat-box">(가) A(x) = {B(x)}⁴ − 2{B(x)}³ − {B(x)}² + 2B(x)<br>(나) A(1) = 24, A(2) = 0</div>A(x)를 x² − 7x − 1로 나눈 나머지를 구하시오.',143,4,'T⁴ − 2T³ − T² + 2T = T(T − 1)(T − 2)(T + 1)이다. 조건과 B(x)의 최고차항 계수를 이용하면 B(x) = x − 3이고 A(x) = (x − 2)(x − 3)(x − 4)(x − 5)이다. x² − 7x − 1을 Y로 두면 A(x) = (Y + 11)(Y + 13)이므로 나머지는 143이다.'),
('최고차항의 계수가 1인 두 다항식 A(x), B(x)가 다음 조건을 만족시킨다.<div class="mat-box">(가) A(x)를 B(x)로 나눈 몫은 B(x) + x이고 나머지는 B(x) − x²이다.<br>(나) A(x)는 B(x) − x로 나누어떨어진다.</div>A(2)의 값을 구하시오.',84,4,'(가)에서 A = B(B + x) + B − x²이다. B − x²의 차수가 B보다 작으므로 B는 최고차항의 계수가 1인 이차식이다. B − x로 나눈 나머지를 생각해 B ≡ x를 대입하면 A ≡ x(x + 1)이다. (나)에 의해 이차식 B − x는 x(x + 1)과 같으므로 B = x² + 2x이다. B(2) = 8이므로 A(2) = 8(8 + 2) + 8 − 4 = 84이다.'),
('두 함수 f(x) = x² − 5x, g(x) = −(1/2)x + 5/2가 있다. 실수 a에 대하여 직선 y = x + k가 x < a에서 y = f(x)의 그래프와 만나는 서로 다른 점의 개수를 m, x ≥ a에서 y = g(x)의 그래프와 만나는 서로 다른 점의 개수를 n이라 하자. m + n = 3인 실수 k가 존재하도록 하는 모든 a의 값의 범위는 p < a < q이다. p × q의 값을 구하시오. (단, p, q는 상수이다.)',23,4,'직선과 g의 교점은 항상 하나이므로 m + n = 3이려면 포물선과의 서로 다른 교점 두 개가 모두 x < a에 있고, g와의 교점은 x ≥ a에 있어야 한다. 포물선과의 교점은 x = 3 ± t (t = √(9 + k) > 0)이고, g와의 교점은 x = (23 − 2t²)/3이다. 따라서 3 + t < a ≤ (23 − 2t²)/3을 만족하는 t > 0이 존재해야 하므로 3 < a < 23/3이다. 이 구간의 a에 대해서는 충분히 작은 양수 t를 택할 수 있다. 따라서 pq = 23이다.')]
assert len(rows)==9
shorts=[dict(q=q,type='short',choices=[],answer=answer,points=points,explain=explain,source=f'2026년 6월 고1 {i}번') for i,(q,answer,points,explain) in enumerate(rows,22)]
original=json.loads(Path('math/transcriptions/2026-06-text.json').read_text())[:16]
items=original+shorts
Path('math/transcriptions/2026-06-short-text.json').write_text(json.dumps(shorts,ensure_ascii=False,indent=2)+'\n')
Path('math/transcribed-2026-06-mixed.js').write_text('window.SEOIK_2026_06_MIXED = '+json.dumps(items,ensure_ascii=False,separators=(',',':'))+';\n')
