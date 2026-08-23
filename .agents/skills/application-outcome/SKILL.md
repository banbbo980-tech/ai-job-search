---
name: application-outcome
description: Codex workflow for recording job-application outcomes safely. Use for interview invitations, stage updates, offers, rejections, no response, withdrawn applications, archiving submitted materials, updating job_search_tracker.csv, and preserving feedback for future calibration.
---

# Application Outcome

Record what happened. Do not reinterpret the outcome framework here; `$job-setup`
uses outcome archives later for calibration.

## Tracker Status Vocabulary

Write only these canonical underscore values:

`drafted` | `applied` | `interview` | `offer` | `hired` | `rejected` |
`no_response` | `offer_declined` | `withdrawn`

Final statuses are `hired`, `rejected`, `no_response`, `offer_declined`, and
`withdrawn`; everything else is open. `drafted` is open but means nothing was
sent, so no follow-up is due. On read, accept legacy `no response` and
`offer declined` as equivalent final values, but never write space spellings.
The archive-only `interview_only` value is not a tracker status.

## Workflow

1. Read `job_search_tracker.csv`. If absent, create it with:

```csv
date,company,sector,role,role_type,channel,status,contact_person,fit_rating,notes,cv_file,cover_letter_file,source,deadline
```

If an existing header does not end in `,deadline`, append `,deadline` to the
header line only. Legacy rows then have an empty deadline; do not rewrite them.

2. Identify the target application from the user's argument or list open rows
   with company, role, applied date, status, deadline, days quiet, and follow-up
   count, then ask the user to choose. Keep drafted rows in a separate
   "Drafted, not yet submitted" group: they are never quiet, but a deadline
   within seven days is urgent and a passed deadline is called out explicitly.
3. If no row matches, collect company, role, date applied, channel, and posting
   URL, then add a tracker row.
4. Ask what happened and classify:
   - Progress: `applied`, `interview`, or `offer`.
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

11. Update only the matched tracker row's status and notes, plus the application
    date when moving a `drafted` row to a submitted status. Preserve every other
    parsed or future field, including `deadline`. Do not reorder rows or
    restructure columns. Never reopen a final row or move a row backward without
    explicit correction from the user.
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

## Follow-Up Branch

When the user asks for `followup`, list open applications that are neither final
nor `drafted`, have been quiet for at least 10 days since application or the last
`followed up YYYY-MM-DD` marker, and have fewer than two logged follow-ups. Skip
unparseable dates rather than guessing.

For each selected row, draft a 60-120 word note using only claims in that
application's archived posting, CV, and cover letter. Match its language and
channel, address the known contact or team, restate role-specific interest, give
one verified value reminder, and ask politely about timing. No new claims.

Only after the user confirms they will send or have sent it, append
`followed up YYYY-MM-DD` to tracker notes and save
`followup_YYYY-MM-DD.md` in the ignored archive. Never send the message. After
two follow-ups, do not propose a third; ask whether the user wants to record
`no_response`. This 10-day action threshold is distinct from `$gmail-sync`'s
30-day read-only staleness alert.
