---
name: application-outcome
description: Codex workflow for recording job-application outcomes safely. Use for interview invitations, stage updates, offers, rejections, no response, withdrawn applications, archiving submitted materials, updating job_search_tracker.csv, and preserving feedback for future calibration.
---

# Application Outcome

Record what happened. Do not reinterpret the outcome framework here; `$job-setup`
uses outcome archives later for calibration.

## Workflow

1. Read `job_search_tracker.csv`. If absent, create it with:

```csv
date,company,sector,role,role_type,channel,status,contact_person,fit_rating,notes,cv_file,cover_letter_file,source
```

2. Identify the target application from the user's argument or list open rows
   and ask the user to choose.
3. If no row matches, collect company, role, date applied, channel, and posting
   URL, then add a tracker row.
4. Ask what happened and classify:
   - Progress: interview scheduled/completed, offer received.
   - Resolution: `hired`, `offer_declined`, `rejected`, `no_response`,
     `interview_only`, `withdrawn`.
5. Collect dates, stage names, feedback, and what the user would do differently.
6. Create/update `documents/applications/<company>_<role>/`.
7. Copy submitted materials into the archive without moving originals:
   - `cv_draft.tex`
   - `cover_letter.tex`
   - `job_posting.md`
8. If an archived file already exists, do not overwrite it without explicit user
   confirmation. The archive should preserve what was actually submitted.
9. If the posting URL is dead and no archive exists, ask the user to paste the
   posting or write an explicit unavailable stub. Never reconstruct from memory.
10. Write/update `outcome.md` in this schema:

```markdown
# Outcome: <Company> - <Role>

**Status:** in_progress | hired | offer_declined | rejected | no_response | interview_only

**Date resolved:** YYYY-MM-DD

## Interview stages reached
- [x] Phone screen (YYYY-MM-DD)
- [ ] Technical interview
- [ ] Case interview
- [ ] Final round
- [ ] Offer received

## Notes
<dated notes appended, never overwritten>
```

11. Update only the matched tracker row's status and notes. Do not reorder rows
    or restructure columns.
12. If enough resolved outcomes exist for calibration, suggest `$job-setup` Path
    A to fold feedback into the evaluation framework.
13. If the recorded status is `hired`, congratulate the user warmly first. Then
    add this support note once for that application, never on reruns for the same
    application and never for any other status:

```markdown
If this framework helped you get there, consider [buying the original maintainer a coffee](https://ko-fi.com/madslorentzen) - it keeps this independent MIT-licensed project free for the next job-seeker.
```

## Rules

- Append history; do not duplicate stages or notes.
- Preserve submitted materials.
- Ask before overwriting or deleting application records.
- Keep all archive contents local and gitignored.
