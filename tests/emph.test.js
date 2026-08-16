/* Unit tests for the inline-emphasis renderer in assets/app.js.
   Run: node tests/emph.test.js  (exit 0 = pass)

   The notes in `data/` are written in Markdown and were rendered with `esc`
   alone, so 46 strings across the dataset printed their own asterisks. The
   emphasis is load-bearing in those notes — it marks the sentence the author
   wants read first — so `emph` introduces the tags.

   Anything that turns escaped text back into markup earns a test. The order
   matters: `emph` must escape FIRST and only then add tags, or a note becomes
   an injection point. The dataset is public and its notes quote source prose,
   so that is not a theoretical concern. */

const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, '..', 'assets', 'app.js'), 'utf8');
const grab = name => {
  const m = src.match(new RegExp(`^function ${name}\\(s\\) \\{[\\s\\S]*?^\\}`, 'm'));
  if (!m) throw new Error(`could not find function ${name} in app.js`);
  return m[0];
};
eval(grab('esc'));
eval(grab('emph'));

let failures = 0;
const check = (label, got, want) => {
  const ok = got === want;
  console.log(`  ${ok ? 'ok   ' : 'FAIL '} ${label}`);
  if (!ok) { console.log(`        want ${JSON.stringify(want)}`);
             console.log(`        got  ${JSON.stringify(got)}`); failures++; }
};

console.log('Inline emphasis');

check('bold becomes strong',
  emph('**Contested.** Three sources disagree'),
  '<strong>Contested.</strong> Three sources disagree');

check('italic becomes em',
  emph('Formerly *Kassina maculata*.'),
  'Formerly <em>Kassina maculata</em>.');

check('backticks become code',
  emph('the `partOf` hierarchy'),
  'the <code>partOf</code> hierarchy');

/* The reason escaping has to come first. If `emph` added tags before escaping,
   or escaped the result of its own substitutions, this note would execute. */
check('markup in a note is inert',
  emph('<script>alert(1)</script> **x**'),
  '&lt;script&gt;alert(1)&lt;/script&gt; <strong>x</strong>');

check('ampersands and quotes still escape',
  emph(`Meers & Romer's "acromion"`),
  'Meers &amp; Romer&#39;s &quot;acromion&quot;');

/* A lone asterisk between digits is multiplication, not emphasis. Muscle notes
   carry ratios and counts, and turning `2*4` into an <em> would eat the text
   between two unrelated numbers anywhere in the paragraph. */
check('arithmetic is left alone',
  emph('5*3 and 2*4'),
  '5*3 and 2*4');

check('an unclosed asterisk is left alone',
  emph('digit 1 is gone *and'),
  'digit 1 is gone *and');

check('bold inside a sentence',
  emph('Retained in monotremes, and **it is not a vestige**: five muscles.'),
  'Retained in monotremes, and <strong>it is not a vestige</strong>: five muscles.');

/* Bold is matched before italic, so a bold run must not be read as two italics
   with an empty middle. */
check('bold is not two italics',
  emph('**a** and **b**'),
  '<strong>a</strong> and <strong>b</strong>');

check('empty and null are safe',
  emph(null) + emph('') + emph(undefined), '');

console.log(failures ? `\n${failures} failing` : '\nall passing');
process.exit(failures ? 1 : 0);
