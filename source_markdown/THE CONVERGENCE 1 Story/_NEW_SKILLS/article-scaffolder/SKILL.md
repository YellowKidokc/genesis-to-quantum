---
name: article-scaffolder
description: >
  Builds the complete structural scaffolding for a Theophysics article in the
  correct element order. Use whenever David says "scaffold," "add the structure,"
  "build out the article," "add FACTS card," "add rigor card," "add the scaffolding,"
  "format this for publication," or any variation of adding publication-ready
  structure to a draft article. Also triggers when creating a new article from
  scratch, when an article is missing structural elements, or when David says
  "make this look like the others." This skill governs ELEMENT ORDER and FORMAT —
  not content or voice. Load theophysics-voice for voice, load this for structure.
---

# Article Scaffolder — Build Order for Theophysics Articles

## Why This Exists

During the Convergence Series scaffolding (March 30, 2026), we learned that element
order matters. David's preference — confirmed through correction — is that the rigor
card (non-collapsible 7Q FACTS) goes BEFORE the media callout, not after. The full
build order was established through trial and error across four articles and is
captured here so no future session has to rediscover it.

## The Build Order

Every Theophysics article follows this exact sequence, top to bottom. Missing elements
should be added in this order. Do not rearrange.

```
1.  YAML Frontmatter
2.  Rigor Card (non-collapsible [!7q-infobox] FACTS)
3.  Media Callout ([!info]- Listen, Watch and Download)
4.  Canonical Navigation ([!abstract]- Canonical Navigation)
5.  Article Title (# heading)
6.  Substack tagline
7.  --- (horizontal rule)
8.  MAIN CONTENT
9.  --- (horizontal rule)
10. Cross-References ([!note]- Cross-References) — minimum 2 exits
11. Cross-Domain Bridges ([!abstract] Cross-Domain Bridges)
12. Disclaimer ([!warning]- Disclaimer)
13. Formal Foundations ([!info]- Formal Foundations)
14. The Audit (## The Audit — three tiers)
15. Series Navigation ([!abstract]- Series Navigation)
```

## Element Templates

### 1. YAML Frontmatter

```yaml
---
schema_version: "theophysics-master-v1.0"
title: "Article Title"
series: series-name
series_position: N
article_type: narrative | technical-narrative | capstone | proof
author: "David Lowe"
date_created: YYYY-MM-DD
lenses: [intro, researcher, proof, synthesis]
laws: [1, 5, 8]              # L01-L10 numbers
variables: [S, G, C]          # Master Equation variables used
pillar: entropy-as-adversary   # or observer-posture, convergence, etc.
domains: [physics, theology, information-theory]
narrative_layers: [anchor, principle, insight, bomb, falsification]
tags:
  - series-tag
  - topic-tags
confidence: developing | high | verified
status: draft-complete | review | publication-ready
next_article: "Next Title" | null
prev_article: "Prev Title" | null
---
```

### 2. Rigor Card — THE CRITICAL ONE

This is **non-collapsible** (no dash after the callout type). It is always visible.
It goes BEFORE the media callout. This was the correction that created this skill.

```markdown
> [!7q-infobox] FACTS
>
> ## Article Title
>
> **Confidence Level** | T = **X.XX**
>
> ### Core Claim
>
> One sentence. No hedging. What the article asserts.
>
> ### Theory Resonance
>
> | . | . |
> |---|---|
> | Theory/Law Name | **STRUCTURAL** or ANALOGICAL |
> | Another Theory  | **STRUCTURAL** or ANALOGICAL |
>
> N structural mappings carry real predictive weight. M analogical mappings suggest pattern.
>
> ### Strongest
>
> **QN Label** (score) — Why this is the strongest element.
>
> ### Weakest
>
> **QN Label** (score) — Why this is the weakest element and what would break it.
>
> ### Kill Threat
>
> N kill conditions | **Most dangerous:**
> State the single most dangerous falsification condition.
> *Status: NOT MET / MET / NOT TESTED*
>
> ### ISO Status
>
> **ISO-DEMONSTRATED** or **ISO-PARALLEL** — Brief explanation of mapping status.
>
> ### At A Glance
>
> | . | . |
> |---|---|
> | Type | Narrative / Technical-Narrative / Capstone |
> | Domains | N (list) |
> | Key metric | What was tested |
> | Decisive test | What would prove or kill this |
> | Performed? | **Yes / No / Deferred** |
```

**Key distinction:** `[!7q-infobox] FACTS` (no dash) = always visible rigor card.
`[!7q-infobox]- FACTS` (with dash) = collapsible. David wants the rigor card
ALWAYS VISIBLE. Do not make it collapsible.

### 3. Media Callout

```markdown
> [!info]- Listen, Watch and Download
> [Audio Version (Google Drive)](URL)
> [Supplemental Audio (Google Drive)](URL)
```

If no media links exist yet, use: `> *Audio and media versions coming soon.*`

Google Drive links go in proper callout format — never bare URLs at the top of the article.

### 4-15. Remaining Elements

See the publish-review skill for templates of the remaining elements (Canonical
Navigation, Disclaimer, Formal Foundations, Series Navigation). The Audit section
template:

```markdown
## The Audit

**Load-bearing (these hold under scrutiny):**
- Claim 1 — why it holds
- Claim 2 — why it holds

**Suggestive (structural parallels that need more formal work):**
- Claim 3 — what's strong, what needs formalization

**Overreached:**
- Either specific overreach items, or: "I looked for overreach in this article.
  [Explanation of what was checked and why it passed.]"
```

The Audit is the scientific honesty move. It's what separates this from apologetics.
Every article needs one. Articles making large claims (capstone pieces, proof articles)
need it most.

## Cross-Reference Rules

- Minimum 2 wikilinked exits per article (3+ preferred)
- Format: `[[filename|Display Text]]`
- Each exit should include a one-line description of what the linked article contains
- Cross-references go in a `[!note]- Cross-References` callout after the main content

## Lessons Learned (Why This Skill Exists)

1. **Rigor card placement:** In the first scaffolding pass, the FACTS card was made
   collapsible and placed without the full 7Q scoring format. David corrected this —
   the rigor card is non-collapsible, scored, and goes before everything except YAML.

2. **Google Drive links:** Were initially left as bare URLs at the top of Article 1.
   These must be inside a proper `[!info]` media callout.

3. **Element order matters:** The sequence above isn't arbitrary. The rigor card
   establishes credibility. The media callout gives access options. The canonical
   nav orients. Then the article. Then the structural apparatus at the bottom
   (cross-refs, bridges, disclaimer, audit, nav) in order of decreasing reader
   engagement — the most engaged readers make it to the Audit.

---

*Skill created: March 30, 2026*
*Source: Convergence Series scaffolding session — corrections applied from David Lowe*
*Complements: publish-review (reviews existing scaffolding), theophysics-voice (content voice)*
