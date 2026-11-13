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
