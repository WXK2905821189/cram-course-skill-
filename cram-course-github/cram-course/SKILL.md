---
name: cram-course
description: Use when the user needs to cram for a university or college exam from PPTX, PDF, DOCX, slides, lecture notes, textbooks, or question banks; wants a study plan, chapter notes, practice questions, spaced repetition, active recall drills, error tracking, or a mock exam generated from course materials.
---

# Cram Course

## Purpose

Turn electronic course materials into an exam-cram package students can actually use:

1. diagnose blind spots,
2. extract course structure,
3. plan the remaining days,
4. generate chapter notes and chapter quizzes,
5. verify slide/page coverage,
6. build cross-chapter drills,
7. schedule spaced repetition,
8. produce a mock exam and final 24-hour checklist.

Prioritize exam usefulness over beautiful summaries. The output should help the student recall, explain, compare, calculate, and answer under time pressure.

## Intake

Ask only for missing information that changes the plan:

- course name and exam date,
- daily available study time,
- known exam scope or teacher emphasis,
- provided material paths,
- whether the exam is closed-book, open-book, oral, written, calculation-heavy, or essay-heavy.

If exam date or daily time is missing, continue with reasonable assumptions and mark them clearly in `01_学习计划.md`.

## Mode Selection

Choose the workflow by time remaining:

| Time left | Mode | Output emphasis |
|---|---|---|
| `< 2 days` | Emergency | core notes, high-frequency questions, answer templates, mock exam, final checklist |
| `2-5 days` | Sprint | chapter notes, chapter quizzes, coverage matrix, high-yield drills, error log |
| `6+ days` | Full | complete workflow, spaced repetition, all drills, mock exam, final review |

If materials are thin, scanned, or mostly images, pause after extraction and ask for textbook pages, class notes, exam scope, or OCR output.

Before generating final study files, run a quick material diagnosis and adapt the question mix to the subject. Use `references/material_diagnostics.md` for input quality decisions and `references/subject_modes.md` for discipline-specific exam patterns.

## Workflow

1. **Extract**: Run `scripts/extract_content.py` for PPTX/PDF/DOCX materials and save `study_materials.json`.
2. **Diagnose Materials**: Check whether the extracted material is usable, thin, scanned, fragmented, or question-bank-only.
3. **Orientation**: Generate `00_课程导学.md` with a course map, familiarity markers, and guiding questions. Do not require zero-basis students to answer exam-like pretest questions.
4. **Plan**: Generate `01_学习计划.md` using remaining days, daily hours, predicted difficulty, and unfamiliar high-yield areas.
5. **Chapter Notes**: Generate one `10_第01章_<章节名>_01学习笔记.md` style note per chapter or major section. Increment the leading prefix by chapter: `10`, `11`, `12`, ...
6. **Chapter Quiz**: Generate one `10_第01章_<章节名>_02章节题库.md` style quiz per chapter or major section, adapted to the subject mode.
7. **Coverage Matrix**: Generate `02_覆盖矩阵.md` mapping each slide/page/section to notes and quiz items.
8. **Cross-Chapter Drills**: Generate drills by question type, not by chapter.
9. **Review System**: Generate `40_间隔复习计划.md` with `scripts/spaced_repetition.py` and `41_错题本.md` from the template.
10. **Mock Exam**: Generate `50_模拟考试.md` with timing, scoring points, answers, and a final 24-hour checklist.

## File Naming

Use Chinese, Obsidian-friendly Markdown filenames by default. Keep technical intermediate files such as `study_materials.json` in English unless the user asks otherwise.

| Prefix | File |
|---|---|
| `00` | `00_课程导学.md` |
| `01` | `01_学习计划.md` |
| `02` | `02_覆盖矩阵.md` |
| `10+` | `10_第01章_<章节名>_01学习笔记.md`, `10_第01章_<章节名>_02章节题库.md` |
| `30-34` | `30_名词解释专项.md`, `31_公式计算专项.md`, `32_对比辨析专项.md`, `33_简答论述专项.md`, `34_综合应用专项.md` |
| `40-41` | `40_间隔复习计划.md`, `41_错题本.md` |
| `50` | `50_模拟考试.md` |

## Required Outputs

Every normal run must produce:

```text
00_课程导学.md
01_学习计划.md
02_覆盖矩阵.md
10_第01章_<章节名>_01学习笔记.md
10_第01章_<章节名>_02章节题库.md
30_名词解释专项.md
31_公式计算专项.md
32_对比辨析专项.md
33_简答论述专项.md
34_综合应用专项.md
40_间隔复习计划.md
41_错题本.md
50_模拟考试.md
```

Emergency mode may reduce depth, but must still produce `02_覆盖矩阵.md`, `50_模拟考试.md`, and a final checklist so omissions are visible.

## Coverage Rules

PPTX slides and PDF pages are coverage units. DOCX heading sections are coverage units.

For every unit, ensure at least one of the following:

- a note section explains it,
- a quiz item tests it,
- a drill item includes it,
- or `02_覆盖矩阵.md` explicitly marks it as low-value/skipped with a reason.

Use `assets/coverage_matrix_template.md`. If any coverage unit has no note, no quiz, and no skip reason, the package is incomplete.

## Chapter Notes

Use `assets/note_template.md`.

Each note file should include:

- core definitions in plain language,
- at least two concrete examples for abstract concepts when possible,
- formulas with symbols, conditions, and common traps,
- comparison tables for confusable concepts,
- `> [!important]` blocks for high-yield memorization,
- at least one self-explanation prompt per section,
- five one-line exam points at the end.

Keep notes concise enough to review under time pressure. Do not turn slides into long textbook prose.

## Chapter Quizzes

Use `references/question_templates.md`.

Each quiz file should include a balanced mix:

- multiple-choice questions for recognition,
- true/false questions for boundaries and traps,
- fill-in-the-blank questions for key terms and formulas,
- short-answer questions for explanation,
- free-recall prompts for structure,
- variant questions for transfer,
- confidence rating after each item.

Add a compact "背题速过 / quick cram" section at the end with question-answer keywords only.

## Cross-Chapter Drills

After chapter outputs, reorganize the entire course by exam task:

| File | Purpose |
|---|---|
| `30_名词解释专项.md` | all important definitions as term-explanation practice |
| `31_公式计算专项.md` | formulas, calculations, unit traps, formula transformations |
| `32_对比辨析专项.md` | confusable concepts, comparison tables, judgment questions |
| `33_简答论述专项.md` | short-answer and essay frameworks by predicted frequency |
| `34_综合应用专项.md` | cross-chapter application and mock big questions |

Use `assets/topic_drill_template.md`.

## Review And Errors

Use `scripts/spaced_repetition.py`:

```bash
python scripts/spaced_repetition.py --topics study_materials.json --exam-date "2026-06-28" --output "40_间隔复习计划.md"
```

Default review intervals: 1, 3, 7, 14 days, plus final review.

Use `assets/error_log_template.md` and classify mistakes as:

| Type | Meaning | Next action |
|---|---|---|
| concept unclear | misunderstood or mixed up concepts | return to notes and self-explain |
| memory lapse | learned but cannot recall | add to spaced repetition |
| careless error | read wrong, unit mistake, calculation slip | record trap and prevention rule |
| application difficulty | knows concept but cannot solve | do variants and explain solution path |

## Quality Gates

Before final response, check:

- all required files exist for the selected mode,
- `02_覆盖矩阵.md` has no uncovered required unit,
- every chapter has both notes and a quiz,
- quizzes include answers and explanations,
- high-confidence wrong answers are highlighted in `41_错题本.md` if user answers are available,
- mock exam matches the likely exam style,
- output warns that AI-generated exam predictions require human review.

## Resource Routing

Load only what is needed:

| Need | Read |
|---|---|
| input quality and missing material decisions | `references/material_diagnostics.md` |
| subject-specific exam patterns | `references/subject_modes.md` |
| learning-science rationale | `references/learning_theory.md` |
| question formats and scoring | `references/question_templates.md` |
| daily schedule and energy planning | `references/time_management.md` |
| study plan format | `assets/study_plan_template.md` |
| notes format | `assets/note_template.md` |
| coverage verification | `assets/coverage_matrix_template.md` |
| cross-chapter drills | `assets/topic_drill_template.md` |
| error tracking | `assets/error_log_template.md` |

## Scripts

- `scripts/extract_content.py`: extracts PPTX/PDF/DOCX text into `study_materials.json`.
- `scripts/spaced_repetition.py`: generates a Markdown review schedule from extracted topics.

Prefer PPTX/DOCX or text-layer PDFs. Old `.ppt` files should be converted to `.pptx`; scanned PDFs need OCR first.
