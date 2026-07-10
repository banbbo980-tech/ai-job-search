---
name: job-search
description: Codex job-search workflow for finding new postings via installed portal skills, normalizing results, deduplicating against seen jobs and the tracker, handling inaccessible portals honestly, and presenting matches for ranking or application.
---

# Job Search

Search job portals using the installed portal CLI skills under `.agents/skills/`,
then deduplicate and store results in `job_scraper/seen_jobs.json`.

## Inputs

- Optional focus text, e.g. `data science`.
- Optional `broad` mode to run all configured query categories.
- Search configuration in `../job-application-core/references/search-queries.md`.

## Workflow

1. Load or create `job_scraper/seen_jobs.json` with `{"seen": {}}`.
2. Load `job_search_tracker.csv` if present. Build an exclusion set from
   company+role pairs already applied to or intentionally tracked.
3. Read `../job-application-core/references/search-queries.md`.
4. Discover portal skills by reading every `.agents/skills/*/SKILL.md` that
   documents a job portal CLI. Do not guess flags; use each portal skill's own
   command examples and supported options.
5. Check whether Bun is available with `bun --version`.
6. If Bun is available, run portal CLI searches with each skill's documented
   `search` command, recency filter, limit, and JSON format. Run independent
   portal calls in parallel where the environment supports it.
7. If Bun is unavailable or a portal command fails, use available web search or
   browsing capabilities as a fallback and report the degraded path.
8. For promising CLI results, call the portal skill's documented `detail`
   command to fetch full description, deadline, employment type, and apply link.
9. For web fallback results, fetch the posting page when accessible. If a portal
   blocks automated access, report that honestly and allow the user to paste the
   full job description later.
10. Normalize every result to include at least title, company, location, date,
    URL, source portal, deadline when known, and description snippet.
11. Deduplicate by URL and company+title. Skip entries already present in
    `seen_jobs.json` or `job_search_tracker.csv`.
12. Add all fetched jobs to `seen_jobs.json` without dropping existing fields.
    Use this shape:

```json
{
  "seen": {
    "<url_or_company_title_key>": {
      "title": "...",
      "company": "...",
      "url": "...",
      "first_seen": "YYYY-MM-DD",
      "fit": "high|medium|low",
      "status": "new|skipped|evaluated|ranked|expired"
    }
  }
}
```

13. Preserve any fields added by `$job-rank`, including `rank_score`,
    `rank_verdict`, and `rank_date`.
14. Present only new jobs in a table sorted high, medium, low fit. Include
    deadline, location, URL, and one-line red flags.
15. Ask whether the user wants a detailed evaluation for any result. For long
    result lists, suggest `$job-rank`.

## Quick Fit

Quick fit is a triage signal only:

- High: role directly uses core skills or target domain.
- Medium: adjacent role with clear transferable evidence.
- Low: substantial unsupported requirements or obvious preference mismatch.

Do not make every job look good. Gaps and deal-breakers must remain visible.

## Safety and Access

- Respect portal access warnings documented in each portal skill.
- LinkedIn and similarly restricted sources are personal-use-only. Keep volume
  low and do not automate bulk collection.
- Do not fabricate postings from titles or snippets. If a posting cannot be
  fetched, mark it unavailable or ask the user to paste it.
