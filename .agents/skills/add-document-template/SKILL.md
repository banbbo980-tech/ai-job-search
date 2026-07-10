---
name: add-document-template
description: Codex workflow for registering custom LaTeX CV or cover-letter templates. Use to list templates, activate a template, deactivate custom templates, inspect a user-provided .tex/.cls/.sty/font bundle, create TEMPLATE.md manifests, run mandatory test compiles, and wire templates into application generation.
---

# Add Document Template

Register custom LaTeX templates without weakening compile, layout, privacy, or
ATS requirements.

## Arguments

- `--list` lists registered templates.
- `--use <name>` activates a registered template.
- `--use default` deactivates a custom template.
- A file or directory path starts registration.

## Registration Workflow

1. Determine template type: CV or cover letter.
2. Read the provided `.tex` file and any referenced `.cls`, `.sty`, fonts, or
   assets. If a required local class/style file is missing, ask for it.
3. Infer and confirm:
   - Template name, kebab-case.
   - Compile engine: `lualatex`, `xelatex`, or `pdflatex`.
   - Fonts and whether they are bundled, system, or TeX-distribution fonts.
   - Page limit, default two pages for CV and one page for cover letter.
   - Style rules, section order, spacing, colors, date format, and pitfalls.
4. Create:
   - `templates/cv/<name>/` for CVs, or
   - `templates/cover_letters/<name>/` for cover letters.
5. Store:
   - `template.tex` with personal data replaced by placeholders.
   - Any needed `.cls` or `.sty`.
   - Bundled fonts under a relative `fonts/` path.
   - `TEMPLATE.md` manifest with name, type, engine, fonts, page limit, style
     rules, known pitfalls, and validation command.
6. Run a mandatory compile test. If LaTeX is unavailable locally, report the
   environment block and do not mark the template fully verified.
7. Activate by adding or replacing a managed active-template block in:
   - `../job-application-core/references/05-cv-templates.md`, or
   - `../job-application-core/references/06-cover-letter-templates.md`.
8. Confirm the active template and the compile status.

## Listing and Activation

For `--list`, read `templates/**/TEMPLATE.md` and show name, type, engine, fonts,
page limit, and active status.

For `--use`, verify the manifest exists before changing active-template blocks.

## Rules

- Never store real personal data in reusable templates.
- Preserve exact page-limit and ATS expectations.
- Do not activate a template that cannot compile unless the user accepts the
  blocked local verification status explicitly.
