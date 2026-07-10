---
name: add-job-portal
description: Codex workflow for creating a new job-portal search skill under .agents/skills. Use for adding a local market job board, investigating public search/detail access, checking robots and terms, scaffolding a Bun TypeScript CLI that follows the portal-skill contract, live-testing search/detail commands, and registering the portal for job search.
---

# Add Job Portal

Create a new portal search skill for a public job board. Do not generate a portal
that requires login or violates clear access restrictions.

## Workflow

1. Collect portal URL, skill name, market/language, and a realistic test query.
2. Ensure the skill name is kebab-case, ends in `-search`, and does not collide
   with an existing `.agents/skills/<name>/` folder.
3. Investigate before writing code:
   - Search URL pattern.
   - Query, location, recency, and pagination parameters.
   - JSON API if present; otherwise parseable HTML structure.
   - Detail page URL pattern.
   - Fields available: id, title, company, location, posting date, URL,
     description, deadline, employment type, apply link.
   - `robots.txt` and access/terms constraints.
4. If listings require authentication, stop and explain that this project only
   supports public listings unless the user later adds an official API flow.
5. If access is legally or ethically constrained, explain the issue and require
   explicit user choice before proceeding. Add a personal-use-only warning to the
   generated skill when appropriate.
6. Scaffold `.agents/skills/<name>/` with:

```text
SKILL.md
url-reference.md
cli/package.json
cli/tsconfig.json
cli/README.md
cli/src/cli.ts
cli/src/helpers.ts
cli/src/commands/search.ts
cli/src/commands/detail.ts
cli/tests/helpers.ts
```

7. Follow the portal-skill contract:
   - Commands: `search` and `detail <id|url>`.
   - Search flags: query, recency when supported, page, limit, JSON/table/plain.
   - Include location flag only if the portal supports it directly.
   - JSON output: `meta` and `results`; each result includes `id`, `title`,
     `company`, `location`, `date`, and `url`.
   - Errors go to stderr as JSON and exit with code 1.
   - Fetch with browser user-agent and backoff for 429/5xx.
8. Test:
   - `bun install`
   - `bun run typecheck`
   - `bun test --timeout 30000`
   - Live `search` with the test query.
   - Live `detail` for one result.
9. If Bun is unavailable locally, report the environment block and leave clear
   commands for the user or CI to run.
10. Register by ensuring `$job-search` can discover the new skill through its
    `SKILL.md`; do not hard-code the portal in `$job-search`.

## Rules

- Prefer structured APIs over fragile HTML parsing when available.
- Do not scrape authenticated content.
- Keep generated portal skills market-specific and locally owned.
- Preserve existing portal skill behavior.
