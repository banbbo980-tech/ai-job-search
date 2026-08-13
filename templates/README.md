# Custom Templates

This folder holds user-registered templates (LaTeX, Typst, or another
command-line toolchain that compiles to PDF), managed by the
`$add-document-template` skill. The framework works out of the box with its
stock templates (moderncv for CVs and `cover.cls` for cover letters); this
folder only gains content when you register your own.

## Layout

```
templates/
├── cv/
│   └── <template-name>/
│       ├── template.<ext>  # Profile-agnostic skeleton ([PLACEHOLDER] tokens), e.g. template.tex or template.typ
│       ├── TEMPLATE.md      # Manifest: source extension, compile command, fonts, page limit, style rules, pitfalls
│       ├── *.cls / *.sty    # Custom class/style files, or Typst packages (if the template needs them)
│       └── fonts/           # Bundled font files (if not using system fonts)
└── cover_letters/
    └── <template-name>/
        └── (same layout)
```

## How it works

- `$add-document-template` captures the source extension, compile command,
  fonts, style rules, and page limit, stores the files here, and requires a
  successful test compile before registration.
- Activation adds a managed block to `05-cv-templates.md` or
  `06-cover-letter-templates.md`; `$job-apply` reads it for both drafting and
  compilation.
- `$add-document-template --list` shows registered templates;
  `$add-document-template --use <name>` switches templates; and
  `$add-document-template --use default` restores the stock templates.

Templates are stored with `[PLACEHOLDER]` tokens instead of personal data, so they are safe to commit and share.
