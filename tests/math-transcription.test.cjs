const assert = require('node:assert/strict');
const test = require('node:test');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const root = path.join(__dirname, '..');
const original = JSON.parse(readFileSync(path.join(root, 'math/transcriptions/2026-06-text.json'), 'utf8'));
const context = {window:{}};
vm.runInNewContext(readFileSync(path.join(root, 'math/transcribed-2026-06.js'), 'utf8'), context);

test('2026 June exam has 21 original answers and points from the supplied answer key', () => {
  const answers = [5,1,4,3,4,2,3,2,3,1,1,3,4,4,5,5,4,2,1,2,1];
  assert.equal(original.length, 25);
  assert.deepEqual(original.slice(0,21).map(q => q.correct + 1), answers);
  assert.deepEqual(original.slice(0,21).map(q => q.points), [...Array(3).fill(2),...Array(10).fill(3),...Array(8).fill(4)]);
  assert(original.slice(0,21).every((q,i) => q.source === `2026년 6월 고1 ${i+1}번` && q.fixed));
  assert(original.slice(21).every(q => q.source === '기출 유형 변형'));
});

test('screen data matches transcription, with text and redrawn figures rather than captures', () => {
  assert.deepEqual(JSON.parse(JSON.stringify(context.window.SEOIK_2026_06_TEXT)), original);
  for (const q of original) {
    assert.equal(q.choices.length, 5);
    assert.equal(new Set(q.choices).size, 5);
    assert(q.q && q.explain);
    assert(!/<img\b/i.test(q.q));
  }
  assert.match(original[11].q, /<svg\b/);
  assert.match(original[17].q, /<svg\b/);
});

test('2025 June exam uses official answer order and text-based figures', () => {
  const items = JSON.parse(readFileSync(path.join(root, 'math/transcriptions/2025-06-text.json'), 'utf8'));
  const ctx = {window:{}};
  vm.runInNewContext(readFileSync(path.join(root, 'math/transcribed-2025-06.js'), 'utf8'), ctx);
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.window.SEOIK_2025_06_TEXT)), items);
  assert.equal(items.length,25);
  assert.deepEqual(items.slice(0,21).map(q=>q.correct+1),[3,5,1,3,3,5,4,3,2,4,2,1,2,5,2,3,1,2,4,2,1]);
  assert.deepEqual(items.slice(0,21).map(q=>q.points),[...Array(3).fill(2),...Array(10).fill(3),...Array(8).fill(4)]);
  assert(items.slice(0,21).every((q,i)=>q.source === `2025년 6월 고1 ${i+1}번` && q.fixed && !/<img\b/i.test(q.q)));
  assert.match(items[13].q,/<svg\b/);assert.match(items[15].q,/<svg\b/);
});

test('2025 September exam matches the official answer key and contains no page captures', () => {
  const items = JSON.parse(readFileSync(path.join(root, 'math/transcriptions/2025-09-text.json'), 'utf8'));
  const ctx={window:{}};
  vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2025-09.js'),'utf8'),ctx);
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.window.SEOIK_2025_09_TEXT)),items);
  assert.equal(items.length,25);
  assert.deepEqual(items.slice(0,21).map(q=>q.correct+1),[3,5,2,1,5,3,4,4,2,2,1,3,1,3,4,2,5,4,1,3,5]);
  assert.deepEqual(items.slice(0,21).map(q=>q.points),[...Array(3).fill(2),...Array(10).fill(3),...Array(8).fill(4)]);
  assert(items.slice(0,21).every((q,i)=>q.source===`2025년 9월 고1 ${i+1}번` && q.fixed && !/<img\b/i.test(q.q) && new Set(q.choices).size===5));
});

test('2026 September paper matches the official answers, points and redrawn diagrams', () => {
  const items=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2026-09-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2026-09.js'),'utf8'),ctx);
  assert.deepEqual(JSON.parse(JSON.stringify(ctx.window.SEOIK_2026_09_TEXT)),items);
  assert.equal(items.length,25);
  assert.deepEqual(items.slice(0,21).map(q=>q.correct+1),[3,5,1,3,1,4,5,5,4,2,1,4,2,3,3,2,4,2,1,3,5]);
  assert.deepEqual(items.slice(0,21).map(q=>q.points),[...Array(3).fill(2),...Array(10).fill(3),...Array(8).fill(4)]);
  assert(items.slice(0,21).every((q,i)=>q.source===`2026년 9월 고1 ${i+1}번` && q.fixed && !/<img\b/i.test(q.q) && new Set(q.choices).size===5));
  assert.match(items[17].q,/<svg\b/);assert.match(items[18].q,/<svg\b/);
});

test('2026 June short answers match the supplied answer key and are included in the mixed paper', () => {
  const shorts=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2026-06-short-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2026-06-mixed.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2026_06_MIXED));
  assert.equal(shorts.length,9);assert.equal(mixed.length,25);
  assert.deepEqual(shorts.map(q=>q.answer),[15,7,6,18,11,82,143,84,23]);
  assert.deepEqual(shorts.map(q=>q.points),[3,3,3,3,4,4,4,4,4]);
  assert(shorts.every((q,i)=>q.type==='short'&&q.source===`2026년 6월 고1 ${i+22}번`&&q.choices.length===0&&!/<img\b/i.test(q.q)));
  assert.deepEqual(mixed.slice(16),shorts);assert.match(shorts[5].q,/<svg\b/);
});

test('2025 June short answers match the supplied answer key and mixed paper', () => {
  const shorts=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2025-06-short-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2025-06-mixed.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2025_06_MIXED));
  assert.equal(mixed.length,25);
  assert.deepEqual(shorts.map(q=>q.answer),[17,3,270,7,21,23,8,65,114]);
  assert.deepEqual(shorts.map(q=>q.points),[3,3,3,3,4,4,4,4,4]);
  assert(shorts.every((q,i)=>q.type==='short'&&q.source===`2025년 6월 고1 ${i+22}번`&&!/<img\b/i.test(q.q)));
  assert.deepEqual(mixed.slice(16),shorts);
});

test('2025 September short answers match the supplied key and mixed paper', () => {
  const shorts=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2025-09-short-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2025-09-mixed.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2025_09_MIXED));
  assert.equal(mixed.length,25);
  assert.deepEqual(shorts.map(q=>q.answer),[28,21,3,6,88,16,12,720,163]);
  assert.deepEqual(shorts.map(q=>q.points),[3,3,3,3,4,4,4,4,4]);
  assert(shorts.every((q,i)=>q.type==='short'&&q.source===`2025년 9월 고1 ${i+22}번`&&!/<img\b/i.test(q.q)));
  assert.deepEqual(mixed.slice(16),shorts);assert.match(shorts[6].q,/<svg\b/);
});

test('2026 September short answers match the supplied key and mixed paper', () => {
  const shorts=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2026-09-short-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2026-09-mixed.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2026_09_MIXED));
  assert.equal(mixed.length,25);
  assert.deepEqual(shorts.map(q=>q.answer),[23,7,5,12,6,77,167,66,24]);
  assert.deepEqual(shorts.map(q=>q.points),[3,3,3,3,4,4,4,4,4]);
  assert(shorts.every((q,i)=>q.type==='short'&&q.source===`2026년 9월 고1 ${i+22}번`&&!/<img\b/i.test(q.q)));
  assert.deepEqual(mixed.slice(16),shorts);
});

test('October geometry paper has the official answers and text questions with variations', () => {
  const items=JSON.parse(readFileSync(path.join(root,'math/transcriptions/october-geometry-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-oct-geometry.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_OCT_GEOMETRY));
  assert.equal(items.length,15);assert.equal(mixed.length,25);
  assert.deepEqual(items.slice(0,11).map(q=>q.correct+1),[2,4,1,4,1,1,5,4,4,3,1]);
  assert.deepEqual(items.slice(11).map(q=>q.answer),[2,40,17,103]);
  assert.deepEqual(mixed.slice(0,11),items.slice(0,11));assert.deepEqual(mixed.slice(21),items.slice(11));
  assert(mixed.every(q=>!/<img\b/i.test(q.q)));assert.match(items[10].q,/<svg\b/);
});

test('2025 October algebra matches the official answers and mixed paper', () => {
  const items=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2025-10-algebra-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2025-10-algebra.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2025_10_ALGEBRA));
  assert.equal(items.length,22);assert.equal(mixed.length,25);
  assert.deepEqual(items.slice(0,15).map(q=>q.correct+1),[4,3,1,2,5,3,5,4,4,3,2,5,4,2,5]);
  assert.deepEqual(items.slice(15).map(q=>q.answer),[13,6,144,18,20,133,16]);
  assert.deepEqual(mixed.slice(0,15),items.slice(0,15));assert.deepEqual(mixed.slice(18),items.slice(15));
  assert(mixed.every(q=>!/<img\b/i.test(q.q)));assert.match(items[20].q,/<svg\b/);
});

test('2026 October algebra matches the official answers and mixed paper', () => {
  const items=JSON.parse(readFileSync(path.join(root,'math/transcriptions/2026-10-algebra-text.json'),'utf8'));
  const ctx={window:{}};vm.runInNewContext(readFileSync(path.join(root,'math/transcribed-2026-10-algebra.js'),'utf8'),ctx);
  const mixed=JSON.parse(JSON.stringify(ctx.window.SEOIK_2026_10_ALGEBRA));
  assert.equal(items.length,23);assert.equal(mixed.length,25);
  assert.deepEqual(items.slice(0,16).map(q=>q.correct+1),[3,2,2,2,3,5,4,5,5,3,3,2,1,4,5,2]);
  assert.deepEqual(items.slice(16).map(q=>q.answer),[8,4,48,630,39,32,72]);
  assert.deepEqual(mixed.slice(0,16),items.slice(0,16));assert.deepEqual(mixed.slice(18),items.slice(16));
  assert(mixed.every(q=>!/<img\b/i.test(q.q)));assert.match(items[13].q,/<svg\b/);
});

test('all six uploaded exams have every original problem transcribed as text', () => {
  const files=['2025-06-text','2025-06-short-text','2025-09-text','2025-09-short-text','2026-06-text','2026-06-short-text','2026-09-text','2026-09-short-text','october-geometry-text','2025-10-algebra-text','2026-10-algebra-text'];
  const originals=files.flatMap(name=>JSON.parse(readFileSync(path.join(root,`math/transcriptions/${name}.json`),'utf8'))).filter(q=>/^20\d\d년 (6|9|10)월 고1 \d+번$/.test(q.source||''));
  const sources=new Set(originals.map(q=>q.source));
  assert.equal(sources.size,180);
  for(const year of [2025,2026]) for(const month of [6,9,10]) for(let n=1;n<=30;n++) assert(sources.has(`${year}년 ${month}월 고1 ${n}번`),`${year}-${month} #${n}`);
  assert(originals.every(q=>!/<img\b/i.test(q.q)));
});

test('practice pools preserve all original questions and extra variants are unique', () => {
  const ctx={window:{}};
  for(const f of ['practice-pools.js','practice-extra.js']) vm.runInNewContext(readFileSync(path.join(root,'math',f),'utf8'),ctx);
  for(const [course,count] of [['1',165],['2',15]]) {
    const pool=ctx.window.SEOIK_PRACTICE_POOLS[course], sets=ctx.window.SEOIK_PRACTICE_EXTRA[course];
    assert.equal(pool.length,count);assert.equal(new Set(pool.map(q=>q.source)).size,count);
    assert(pool.every(q=>[2,3,4].includes(q.points)));
    assert.equal(sets.length,2);assert(sets.every(s=>s.length===25));
    const variants=sets.flat();assert.equal(new Set(variants.map(q=>q.q)).size,50);
    assert(variants.every(q=>q.choices.length===5&&new Set(q.choices).size===5&&q.explain&&q.source.startsWith('변형')));
  }
});
