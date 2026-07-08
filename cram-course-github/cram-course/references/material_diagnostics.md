# Material Diagnostics

Use this before generating the final cram package. The goal is to avoid confident-looking output from weak inputs.

## Diagnostic Table

| Material condition | Signals | Action |
|---|---|---|
| usable slides/notes | headings plus explanatory bullets, formulas, examples, tables | proceed with normal workflow |
| thin slides | many pages have only titles or slogans | ask for textbook pages, class notes, exam scope, or recorded lecture notes |
| scanned PDF/images | extracted text is empty or garbled | ask user to OCR first; do not invent missing content |
| question-bank-only | mostly exercises with little theory | reverse-map questions to knowledge points, then generate notes from confirmed patterns |
| fragmented materials | overlapping files, inconsistent chapter order | create a source map first and ask about official exam scope if unclear |
| calculation-heavy but formula-poor | formulas appear without definitions or examples | request formula sheet or solved examples |
| essay-heavy but outline-poor | broad topic names without argument structure | ask for teacher emphasis, rubric, or past paper |

## Output Behavior

If material quality is weak, state the limitation inside `01_学习计划.md` and `02_覆盖矩阵.md`.

Do not hide gaps. Mark unresolved units as:

```text
status: needs source
reason: slide has title only / scanned text unavailable / formula lacks context
next action: ask user for ...
```

## Minimum Viable Source

Proceed without asking only when each major chapter has at least one of:

- explanatory bullet points,
- definitions,
- formulas with surrounding text,
- examples or case descriptions,
- past-paper questions tied to that topic.

If none are present, switch to a source-request response before generating detailed notes.
