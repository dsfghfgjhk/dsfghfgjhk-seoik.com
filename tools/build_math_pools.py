import json,re
from math_diagrams import with_figure
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'math'
files=['2025-06-text','2025-06-short-text','2025-09-text','2025-09-short-text','2026-06-text','2026-06-short-text','2026-09-text','2026-09-short-text','october-geometry-text','2025-10-algebra-text','2026-10-algebra-text']
pools={'1':{},'2':{}}
for name in files:
 for q in json.loads((r/'transcriptions'/f'{name}.json').read_text()):
  src=q.get('source','')
  if not re.fullmatch(r'20\d\d년 (6|9|10)월 고1 \d+번',src): continue
  course='2' if name=='october-geometry-text' else '1'
  pools[course][src]=with_figure(q)
assert len(pools['1'])==165 and len(pools['2'])==15
(r/'practice-pools.js').write_text('window.SEOIK_PRACTICE_POOLS = '+json.dumps({k:list(v.values()) for k,v in pools.items()},ensure_ascii=False,separators=(',',':'))+';\n')
