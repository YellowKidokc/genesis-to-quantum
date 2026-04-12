---
name: stt-artifact-scanner
description: >
  Scans Theophysics articles for speech-to-text artifacts before any other review
  step. David works via voice-to-text and dictation artifacts regularly leak into
  drafts — stray phrases, phone conversations, meta-commentary, typos from dictation
  errors. Use this skill FIRST whenever reviewing, editing, or preparing any article
  David has written. Also triggers on "clean up," "check for artifacts," "speech to
  text," "dictation," "voice to text," "there's junk in this," or any review task
  on David's writing. Run this BEFORE voice checks, scaffolding, or publication
  review. A single artifact in a published article destroys reader trust instantly.
---

# Speech-to-Text Artifact Scanner

## Why This Exists

David Lowe works primarily via voice-to-text dictation. This means his drafts
regularly contain artifacts that are invisible to him (he's heard them as speech,
not read them as text) but immediately visible — and credibility-destroying — to
a reader. During the Convergence Series review (March 30, 2026), we found five
artifacts in Article 1 and one in Article 2 that would have been published if not
caught.

**This scan runs FIRST. Before voice review. Before scaffolding. Before anything.**
A perfectly scaffolded article with "OK bye aunt" in the middle is worse than an
unscaffolded article without it.

## What To Scan For

### Category 1: Phone/Conversation Bleed-Through

David sometimes takes calls or talks to people while dictating. Fragments of those
conversations leak into the text.

**Pattern:** Abrupt change in topic, casual speech fragments that don't connect to
surrounding content, greetings/goodbyes that aren't part of the article.

**Examples found in the wild:**
- "OK bye aunt" (appended to a section heading)
- "Two muscles I gotta hang up No this is the wrong one It's the wrong one on a second you"
- "Bye bye" (inserted mid-sentence)

**Detection approach:** Look for:
- Greeting/farewell words appearing mid-text: "bye", "hello", "hey", "hang on",
  "one second", "gotta go", "hold on"
- Sentence fragments that break the surrounding flow completely
- Multiple unrelated clauses jammed together without punctuation

### Category 2: Meta-Commentary

David sometimes talks about the article structure or process while dictating. These
are instructions to himself or to an AI, not article content.

**Pattern:** Sentences about what the article should do rather than doing it. References
to "the picture," "the key findings," "start off with," "we can," planning language.

**Examples found in the wild:**
- "And then you kind of have the key findings and critical standpoint so we can start
  off with the picture and then say um"
- "you know" (standalone, end of section)

**Detection approach:** Look for:
- Planning/meta language: "we should," "start with," "kind of have," "and then say"
- Filler words on their own lines: "you know," "um," "like," "so yeah"
- Sentences that reference the article as an object ("this section should...")
  when the surrounding text is first-person narrative

### Category 3: Dictation Typos

Voice-to-text engines mishear words, split words, or insert wrong words.

**Pattern:** Words that are phonetically close to the intended word but wrong, or
words split by spaces that shouldn't be.

**Examples found in the wild:**
- "info I rmation" (should be "information")
- "fYounger" (should be "Younger" — capitalization artifact)
- "Everyone fYounger" (garbled heading)

**Detection approach:** Look for:
- Single letters standing alone between words (especially "I" used as a space)
- Unusual capitalization mid-word
- Words that are almost-but-not-quite right ("their" for "there" is normal typo,
  but "thermodynamicks" is dictation)

### Category 4: Command Bleed

Voice commands intended for the dictation software that got transcribed as text.

**Pattern:** OS or app commands appearing as text.

**Examples to watch for:**
- "period" "comma" "new line" "new paragraph" (transcribed literally)
- "delete that" "go back" "undo"
- "stop listening" "hey siri" "ok google"

## How To Report

For each artifact found, report:

```
ARTIFACT FOUND:
  Location: [Article name], Line [N]
  Text: "[exact artifact text]"
  Category: [1-4]
  Context: "[surrounding sentence so David can find it]"
  Suggested fix: [what the text probably should say, or "DELETE"]
```

## Severity

**Every artifact is CRITICAL.** There is no "low priority" artifact. A single
"OK bye aunt" in a published Substack article about physics and theology will:
1. Make the reader question whether the author proofread at all
2. Undermine the credibility of the technical claims
3. Become the thing people screenshot and share

Clean all artifacts before any other review step proceeds.

## Integration With Other Skills

Run this skill BEFORE:
- `publish-review` (publication gate check)
- `article-scaffolder` (structural scaffolding)
- `theophysics-voice` (voice review)
- `cross-domain-strengthener` (claim strengthening)

The scanning order is: **artifacts → voice → scaffolding → content → publication.**

---

*Skill created: March 30, 2026*
*Source: Convergence Series review — 6 artifacts found across 2 articles*
*David handles the actual fixes (surgical find-and-replace). This skill finds them.*
