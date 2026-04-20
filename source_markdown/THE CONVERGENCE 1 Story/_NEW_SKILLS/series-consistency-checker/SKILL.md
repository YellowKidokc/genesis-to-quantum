---
name: series-consistency-checker
description: >
  Validates cross-references, article ordering, and continuity across a multi-article
  Theophysics series. Use whenever reviewing a series of connected articles (Convergence,
  Genesis to Quantum, or any multi-part sequence). Catches ordering conflicts, broken
  thread pickups, swapped references, repeated introductions, and arc integrity problems.
  Triggers on "check the series," "do these connect," "series review," "continuity check,"
  "cross-reference check," "do the articles link up," or any task involving multiple
  connected articles. Also triggers automatically as part of publish-review when reviewing
  a series folder. This skill catches the kind of bug that's invisible when reading one
  article but obvious when reading all of them in order.
---

# Series Consistency Checker

## Why This Exists

During the Convergence Series review (March 30, 2026), we found a critical ordering
conflict: Article 2 claimed to be "the first piece in the Convergence series," and
Article 3's closing summary referenced Articles 1 and 2 in the wrong order. Neither
error was visible when reading any single article. Both became obvious only when
reading the series sequentially. This skill ensures that every cross-reference,
thread pickup, and arc claim is verified against the actual article contents.

## The Five Checks

### Check 1: Article Order Verification

**What to check:** Every article that references its position in the series
("this is the first piece," "in the last article," "the second piece showed...").

**How:**
1. Read all articles and note every self-referencing position claim
2. Compare against: (a) file numbering, (b) YAML series_position, (c) YAML
   prev_article/next_article
3. Flag ANY contradiction between text claims and metadata

**The error we caught:** Article 2's closing said "This is the first piece" when
it was actually the second. This happened because the articles were drafted in a
different order than the final publication sequence.

**Output format:**
```
ORDER CHECK:
  Article 1: "What Separates Us"
    - YAML position: 1 ✓
    - Text claims: none (doesn't self-reference position) ✓
    - prev/next: null / "The Photographer..." ✓

  Article 2: "The Photographer..."
    - YAML position: 2 ✓
    - Text claims: "This is the first piece" ✗ CONFLICT — says first, is second
    - prev/next: "What Separates Us" / "The Same Equation" ✓

  CONFLICTS FOUND: 1
```

### Check 2: Cross-Reference Accuracy

**What to check:** Every time an article references what a previous article
"showed," "proved," or "established."

**How:**
1. Collect every backward reference ("In the last piece I showed you...",
   "The first article established...", "As we saw in...")
2. Go to the referenced article and verify the claim is actually there
3. Flag references to content that doesn't exist or exists in a different article

**The error we caught:** Article 3's closing said "In the first piece, I showed
you that every judgment argument runs the same code" — but judgment arguments were
in Article 2, not Article 1. The articles were referenced in swapped order.

**Output format:**
```
CROSS-REF CHECK:
  Article 3 references Article 1: "showed you that every judgment argument
  runs the same code"
    → Article 1 actual content: Six divides, fragmentation, good vs evil
    → Judgment arguments are in Article 2
    → ✗ MISMATCH — reference points to wrong article
```

### Check 3: Thread Continuity

**What to check:** Each article should pick up a thread from the previous one.
The closing of Article N should set up a question or promise. The opening of
Article N+1 should address it.

**How:**
1. Read the closing 2-3 paragraphs of each article (except the last)
2. Read the opening 2-3 paragraphs of the next article
3. Verify the thread connects — the promise made is the promise picked up
4. Flag any article that opens without connecting to the previous

**What good looks like:**
- Article 1 closes: "The next piece goes into why entropy maps exactly onto evil."
- Article 3 opens: "In the last piece I made a claim I didn't prove."
  → Thread connects. Promise made, promise acknowledged.

**What bad looks like:**
- Article N closes: "Next we'll explore the quantum implications."
- Article N+1 opens: "Let me tell you about my childhood."
  → No thread pickup. Reader feels lost.

### Check 4: No Repeated Introductions

**What to check:** Each article should assume the reader read the previous ones.
Terms defined in Article 1 should not be re-defined in Article 2 unless explicitly
flagged as a recap.

**How:**
1. Track every term/concept defined in each article
2. Check if any subsequent article re-defines the same term without flagging it
3. Exception: capstone articles may deliberately compress previous content
   ("let me compress it to one paragraph"). This is fine IF flagged.

**Output:** List of repeated definitions with recommendation (cut / flag as recap).

### Check 5: Arc Integrity

**What to check:** The series should build. Each article should escalate in
precision, scope, or stakes. The arc should be identifiable in one sentence.

**How:**
1. Summarize each article's role in one sentence
2. Verify escalation: does each article go deeper/further than the last?
3. Check: is Jesus load-bearing in the theological articles, or decorative?
   (Can Christ be removed without the argument collapsing? If yes, red flag.)
4. Check: does the series voice stay consistent? If one article sounds more
   academic than the others, flag it.

**Arc format:**
```
ARC CHECK:
  Article 1: [role] — sets up [what]
  Article 2: [role] — deepens [what]
  Article 3: [role] — proves [what]
  Article 4: [role] — converges on [what]

  Escalation: ✓ INTACT / ✗ BROKEN at Article N
  Jesus load-bearing: ✓ in Articles [list] / ✗ decorative in Articles [list]
  Voice consistency: ✓ CONSISTENT / ✗ Article N sounds [different how]
```

## When To Run This

- **Always** as part of a series-level publish-review
- **Always** when article order changes (renumbering, resequencing, new article added)
- **Always** when an article's closing or opening paragraphs are edited
- **After** the stt-artifact-scanner (artifacts first, then consistency)
- **Before** final publication approval

## Output Format

```
# SERIES CONSISTENCY REPORT
## Series: [Name]
## Date: [Date]
## Articles reviewed: [N]

### Order Verification: PASS / FAIL
[details]

### Cross-Reference Accuracy: PASS / FAIL
[details per reference]

### Thread Continuity: PASS / FAIL
[details per transition]

### Repeated Introductions: PASS / WARN
[details if any]

### Arc Integrity: PASS / FAIL
[arc summary + escalation check]

### VERDICT: CONSISTENT / CONFLICTS FOUND (N)
[list of all conflicts with recommended fixes]
```

---

*Skill created: March 30, 2026*
*Source: Convergence Series review — article order conflict caught between Articles 2 and 3*
*Complements: publish-review (single-article checks), stt-artifact-scanner (pre-review cleanup)*
