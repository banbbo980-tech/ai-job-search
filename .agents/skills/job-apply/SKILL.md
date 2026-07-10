---
name: job-apply
description: Complete Codex job-application workflow for a URL or pasted posting. Use to evaluate fit, request proceed confirmation, draft a tailored LaTeX CV and cover letter, run an independent Codex reviewer or fallback review, revise, compile PDFs, inspect layout, verify ATS extraction, and present final files without inventing candidate facts.
---

# Job Apply

Codex is the drafter. Preserve the full application pipeline and never add
unsupported skills or achievements.

## Inputs

- A job posting URL, or
- The complete pasted job description.

## Workflow

### 1. Parse the Posting

Fetch the URL with available browsing/web capabilities, or use pasted text
directly. Extract company, role, department, location, language, deadline,
requirements, preferred skills, responsibilities, and application contact.

If the URL cannot be fetched, ask the user to paste the posting. Do not infer a
posting from search snippets.

### 2. Evaluate Fit Before Drafting

Read:

- `../job-application-core/references/01-candidate-profile.md`
- `../job-application-core/references/02-behavioral-profile.md`
- `../job-application-core/references/04-job-evaluation.md`

Evaluate skills, experience, behavioral/culture fit, logistics, career
alignment, salary benchmark if configured, deal-breakers, urgency, and gaps.

Run optional salary lookup only if useful:

```bash
python salary_lookup.py "<Company Name>" --json
```

Add `--city "<City>"` when the posting city is known. If `salary_data.json` is
missing or the tool fails, skip salary lookup and report the graceful skip.

Present the fit evaluation and ask:

`Should I proceed with drafting the CV and cover letter for this role?`

Stop if the user does not clearly approve.

### 3. Draft CV and Cover Letter

Read:

- `../job-application-core/references/03-writing-style.md`
- `../job-application-core/references/05-cv-templates.md`
- `../job-application-core/references/06-cover-letter-templates.md`
- The most relevant existing `cv/main_*.tex` or `cv/main_example.tex`
- The most relevant existing `cover_letters/cover_*.tex` or
  `cover_letters/cover_example.tex`

Create:

- `cv/main_<company>.tex`
- `cover_letters/cover_<company>_<role>.tex`

CV rules:

- Always write the CV in English unless the user explicitly chooses otherwise.
- Preserve the moderncv/banking structure or active custom template.
- Tailor profile statement, skills, and evidence-backed bullets.
- Keep to the required page limit.

Cover-letter rules:

- Match the posting language when the existing workflow requires it.
- Use `cover.cls` or the active custom cover-letter template.
- Address a named person when supported by the posting; otherwise use the
  appropriate hiring-manager greeting.
- Keep to the required page limit.

AI-tooling wording must be truthful. Do not say the candidate used a tool unless
the profile supports it. For future-facing tool references in this migrated
project, prefer neutral wording such as "agentic coding tools" or "Codex/ChatGPT
Work" only when supported by the candidate's real experience.

### 4. Independent Reviewer

When Codex subagents are available, delegate a fresh reviewer. Provide:

- Exact posting text.
- Candidate evidence from the relevant profile references.
- Exact CV draft text or path.
- Exact cover-letter draft text or path.
- Review criteria below.

Reviewer criteria:

- Research the company only when allowed and necessary.
- Identify weak framing, missed supported keywords, generic language, unsupported
  claims, role mismatch, company mismatch, tone mismatch, and evidence gaps.
- Return structured edits when possible with file, old text, new text, and reason.
- Return narrative recommendations for non-mechanical issues.
- Never invent experience.

If subagents are unavailable, perform a second-pass reviewer fallback:

1. Pause drafting mentally and reload the exact posting and evidence.
2. Review the drafts against the same criteria.
3. Record findings under "Reviewer fallback findings".
4. Apply only valid, evidence-backed improvements.

The drafter must verify all reviewer/company claims before incorporating them.

### 5. Revise

Apply structured reviewer edits only when the old text matches and the new text
is factual. For narrative suggestions, revise with judgment. Supported keywords
belong in concrete evidence bullets where possible. Genuine gaps remain visible.

### 6. Compile and Inspect PDFs

Compile:

```bash
cd cv && lualatex -interaction=nonstopmode main_<company>.tex
cd ../cover_letters && xelatex -interaction=nonstopmode cover_<company>_<role>.tex
```

If local LaTeX is unavailable, report the environment block and do not claim PDF
verification passed.

Inspect rendered PDFs with available PDF/rendering capabilities. Verify:

- CV exactly two pages when required.
- No orphaned entry titles or isolated headings.
- No clipped text or awkward whitespace.
- Cover letter exactly one page when required.
- Signature visible.
- Bullet fonts match the body rules.

Iterate on LaTeX until clean when the toolchain is available.

### 7. ATS Verification

Check `pdftotext -v`. If available:

```bash
cd cv && pdftotext -layout main_<company>.pdf main_<company>.txt
```

Inspect extracted text for:

- No `(cid:*)` markers or replacement characters.
- Literal email and phone.
- Reading order matching visual order.
- Recognizable dates.
- Supported keyword coverage without stuffing.
- Keyword status categories should preserve the original distinction: covered,
  synonym-only, missing but genuinely supported by the profile, and missing (gap)
  where the candidate does not have the requirement.

Delete the extracted `.txt` after the final check. If `pdftotext` is missing,
report reduced ATS verification and perform a visual keyword review only.

### 8. Final Output

Report:

- Fit verdict and proceed confirmation status.
- Key tailoring decisions.
- Reviewer method used: subagent or fallback.
- Files created.
- Compile/layout/ATS checklist with pass, fail, or environment-blocked status.
- Gaps that remain honest.
- Suggested next skill: `$application-outcome` after submission, or
  `$interview-prep` when an interview is scheduled.
