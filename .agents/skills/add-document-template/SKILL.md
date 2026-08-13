---
name: add-document-template
description: Codex workflow for registering custom CV or cover-letter templates that compile to PDF. Use to list, activate, or deactivate templates; inspect LaTeX, Typst, or another command-line source bundle; create manifests; run mandatory test compiles; and wire templates into application generation.
---

# Add Document Template

Register custom PDF-producing templates without weakening compile, layout, privacy, or
ATS requirements.

## Arguments

- `--list` lists registered templates.
- `--use <name>` runs Switch Mode, resolves a registered template's metadata,
  then activates it without re-running registration steps.
- `--use default` deactivates a custom template.
- A file or directory path starts registration.

## Listing and Switch Mode

For `--list`, read `templates/**/TEMPLATE.md` and show name, type, source
extension, compile command/toolchain, fonts, page limit, and active status. A template is active when the matching
job-application-core template reference contains an `ACTIVE-TEMPLATE` managed
block naming it. If no custom templates exist, say so and explain that
`$add-document-template` registers one.

For `--use <name>`:

1. If `<name>` is `default`, skip template resolution and continue to activation
   with `default` as the target.
2. Find `templates/**/TEMPLATE.md` manifests whose parent folder name exactly
   matches `<name>`.
3. If none match, stop and say the template is not registered. Suggest
   `$add-document-template --list`.
4. If more than one manifest matches, stop, list the matching manifest paths,
   and ask the user to rename one template. Activation must be unambiguous.
5. Read the matching `TEMPLATE.md` and extract type, source extension, full
   compile command, engine/toolchain label, page limit, and font summary.
6. Verify `template<source-extension>` exists beside the manifest. If it is missing, stop
   because registration is incomplete.
7. Derive the template kind from the manifest path:
   `templates/cv/<name>/TEMPLATE.md` means CV, and
   `templates/cover_letters/<name>/TEMPLATE.md` means cover letter.
8. Continue to activation using the resolved metadata, template skeleton path,
   and manifest path. Do not re-run registration, storage, or compile-test
   steps when switching an already-registered template.

## Registration Workflow

1. Determine template type: CV or cover letter.
2. Read the provided source and referenced classes, packages, fonts, or assets.
   Ask for any required missing local dependency.
3. Infer and confirm:
   - Template name, kebab-case.
   - Source extension such as `.tex` or `.typ`.
   - Full compile command using `<file>` as the basename placeholder, plus an
     engine/toolchain display label. Infer LaTeX or Typst commands; ask for other
     toolchains.
   - Fonts and whether they are bundled, system, or TeX-distribution fonts.
   - Page limit, default two pages for CV and one page for cover letter.
   - Style rules, section order, spacing, colors, date format, and pitfalls.
4. Create:
   - `templates/cv/<name>/` for CVs, or
   - `templates/cover_letters/<name>/` for cover letters.
5. Store:
   - `template<source-extension>` with personal data replaced by placeholders.
   - Any needed `.cls` or `.sty`.
   - Bundled fonts under a relative `fonts/` path.
   - `TEMPLATE.md` manifest with name, type, source extension, full compile
     command, toolchain, fonts, page limit, style rules, known pitfalls, and
     validation command.
6. Run a mandatory compile test using fictional data and the declared command.
   If the toolchain is unavailable, report the environment block and do not mark
   the template fully verified.
7. Delete every test-compilation scratch file and output after the compile
   attempt: `_compile_test.tex`, `_compile_test.pdf`, `_compile_test.aux`,
   `_compile_test.log`, `_compile_test.out`, `_compile_test.fls`,
   `_compile_test.fdb_latexmk`, `_compile_test.synctex.gz`, and any other
   `_compile_test.*` byproduct.
8. Activate by adding or replacing a managed active-template block in:
   - `../job-application-core/references/05-cv-templates.md`, or
   - `../job-application-core/references/06-cover-letter-templates.md`.
9. Confirm the active template and the compile status.

## Activation

Activation wires the template into `$job-apply` by adding a managed
`ACTIVE-TEMPLATE` block near the top of the relevant shared reference:

- `../job-application-core/references/05-cv-templates.md` for CVs.
- `../job-application-core/references/06-cover-letter-templates.md` for cover
  letters.

If activation was reached from Switch Mode, use the metadata resolved from
`TEMPLATE.md`. If activation was reached after registering a new template, use
the metadata collected and verified during registration.

Activation rules:

- Exactly one managed block per reference file.
- Replace the complete block between `BEGIN ACTIVE-TEMPLATE` and
  `END ACTIVE-TEMPLATE`; never stack blocks.
- `--use default` removes the managed block entirely and restores stock
  guidance.
- Do not modify text outside the managed markers.
- Include the skeleton path, manifest path, compile engine, font summary, page
  limit, source extension, full compile command, and role-bearing output-file
  convention in the block.

## Rules

- Never store real personal data in reusable templates.
- Preserve exact page-limit and ATS expectations.
- Do not activate a template that cannot compile unless the user accepts the
  blocked local verification status explicitly.
- Do not leave `_compile_test.*` files in the repository or template folder.
