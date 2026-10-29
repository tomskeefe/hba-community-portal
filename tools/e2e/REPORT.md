# End-to-end walkthrough report

Generated 2026-10-29 10:10 by `python tools/e2e/run.py` against a local Supabase (http://127.0.0.1:3013). Run time 30 min.

## Bugs found by the walkthrough (October 2026)

### Fixed, each in its own commit with a regression check

| # | What a reader saw | Cause | Fix | Regression check |
|---|---|---|---|---|
| 1 | Editing an issue, meeting, agenda item, minutes, officeholder or register entry; approving minutes; attaching a minutes PDF; replying to a governor message; meeting Zoom settings: all failed with a server error | The backend split left `uid()`, `datetime` and `timezone` un-imported in `governance.py` and `finance.py` (18 routes) | Imports restored | `tools/tests/test_backend_names.py` runs pyflakes over `server/` (CI installs pyflakes) |
| 2 | On a project built from `schema.sql` (the new free hosting), even the administrator got "This account does not have permission for that action" when attaching a newsletter or minutes PDF, approving minutes, publishing a newsletter or volunteer task, changing volunteer e-mail preferences, editing a register entry or category budget, or editing an SMS draft | `schema.sql` kept table grants but dropped all column-level `grant update(…)` lines from the migration history | Grants added to `schema.sql`; `supabase/migrations/002_column_update_grants.sql` for a project already created | `tools/tests/test_schema_grants.py` compares every column grant in the history with `schema.sql`; walkthrough seeds a minutes PDF, newsletter PDF and published volunteer task |
| 3 | The dashboard's Weather now, Next tide and NWS alerts tiles did nothing | They run tool id `bulletin`, which is not in the tool list (same gap as Open calendar) | `run('bulletin')` opens the bulletin section | Walkthrough opens `bulletin` for every role |
| 4 | Submitting a nomination always failed with a permission error, for every role | The form offered fixed years 2027/2029/2031; the database accepts nominations only for an election the board has opened | Form lists only open election years (a note replaces the button when none); the API explains | `test_nomination_needs_an_open_election` |
| 5 | Every board visit logged a failed request, and the Detailed capital model said "Private cleaning allowance was not loaded" | `/api/cleaning-plan` answered 404 when no plan row exists, which is always true on a new project (no screen adds one) | Answers `{"recorded": false}`; the model keeps its estimate | `test_cleaning_plan_missing_is_not_an_error` |
| 6 | A rain date on or before the event date showed raw database text ("violates check constraint rain_date_requires_later_date") | No API check | "The rain date must be after the event date." | `test_rain_date_before_event_is_explained` |
| 7 | Linking an account to a property it already has showed "duplicate key value violates unique constraint" | No API check | "That property is already linked to this account." | `test_linking_a_property_twice_is_explained` |
| 8 | Script error "Cannot set properties of null (setting 'onclick')" in Road ownership research / property reports | A deed image that failed after the reader turned the page looked up its retry button in a detached stage | Only the image still on screen reacts | Walkthrough clicks through `roads` and `reports` |
| 9 | On a slow connection a board member (or resident) could land on the signed-out dashboard layout, a "Sign in" tile and no board tools, until reloading | community.js announced the account as soon as the session answered, sometimes before the dashboard script had loaded and started listening | The first announcement waits for the page to finish parsing | Walkthrough "slow connection" flow serves capabilities.js 2.5 s late (failed 3/3 before, passes after) |

### Not fixed: listed for a decision

- **Four wareham.gov links returned 404** (town site reorganised): fixed by pointing them at Internet Archive
  copies of the same documents, labelled "archived copy": Street Listing PDF (Oct 2025), Town Accepted Streets PDF
  (Nov 2025) and the town's 2026 horseshoe-crab notice (May 2026). The notice is seasonal; link next year's in
  `private-app/bulletin.js` when the town posts it.
- **Workstation paths in data files**: fixed. 976 research image paths (about 4,800 occurrences) pointed at the
  researcher's computer (`/home/user/workspace/…`) in `audit.json`, `property-history.json` (the downloadable evidence
  ledger), `road-wording.*` and `title-trace.*`. 765 now name the app's own copy of the same scan (record-scans
  package); 210 with no copy anywhere became registry citations ("Plymouth County Registry of Deeds, Book 27263,
  Page 1, image 1 (research working copy, not included)"); one working notes file is named as not included.
- **Horseshoe-crab notice**: now edited by the administrator in the bulletin (Edit conservation notice: wording, link,
  dates covered and the conservation-hold months), saved as `public_conservation_notice`.
- **Errors from the database reached readers as raw text** in other places too. Fixed afterwards in dbaa4ba: `hba/supabase.py` now turns constraint violations into plain-language messages.
- `board@hba.test` and `pending@hba.test` did not exist in the local Supabase although `test-accounts.txt` listed them;
  the seed step now creates them through the app's own sign-up and approval.

### By design (reported as warnings, not failures)

Advisories need an official mass.gov or wareham.ma.us link; minutes cannot be dated in the future; a household already
marked paid outside the receipt ledger cannot get a second credit; only the administrator may change a scheduling
office linked to an account; resident-made issues, draft bids and draft volunteer tasks are not shown to other
residents.

## Summary by role

| Role | pass | fail | warn | skip | info |
|---|---|---|---|---|---|
| admin | 105 | 0 | 6 | 1 | 72 |
| board | 95 | 0 | 6 | 1 | 71 |
| resident | 67 | 0 | 2 | 1 | 79 |
| board-as-resident | 42 | 0 | 0 | 0 | 0 |
| pending | 3 | 0 | 0 | 0 | 0 |
| resident @375px | 11 | 0 | 2 | 1 | 8 |
| admin @375px | 48 | 0 | 0 | 0 | 0 |

## Tools opened, per role

Each cell: did the tool open without script errors or unexpected failed requests.

| Tool | admin | board | resident | board-as-resident | pending | resident @375px | admin @375px |
|---|---|---|---|---|---|---|---|
| bulletin | pass | pass | pass | pass | – | – | pass |
| team | pass | pass | pass | pass | – | – | pass |
| payments | pass | pass | pass | pass | – | pass | pass |
| summer | pass | pass | pass | pass | – | pass | pass |
| issues | pass | pass | pass | pass | – | pass | pass |
| planner | pass | pass | pass | pass | – | – | pass |
| duesbuy | pass | pass | pass | pass | – | – | pass |
| newsletter | pass | pass | pass | pass | – | – | pass |
| poll | pass | pass | pass | pass | – | – | pass |
| hosting | pass | pass | pass | pass | – | – | pass |
| volunteers | pass | pass | pass | pass | – | pass | pass |
| events | pass | pass | pass | pass | – | – | pass |
| message | pass | pass | pass | pass | – | pass | pass |
| votes | pass | pass | pass | pass | – | pass | pass |
| elections | pass | pass | pass | pass | – | – | pass |
| meetings | pass | pass | pass | pass | – | – | pass |
| governance | pass | pass | pass | pass | – | – | pass |
| documents | pass | pass | pass | pass | – | – | pass |
| research | pass | pass | pass | pass | – | – | pass |
| trash | pass | pass | pass | pass | – | – | pass |
| townrules | pass | pass | pass | pass | – | – | pass |
| town | pass | pass | pass | pass | – | – | pass |
| bids | pass | pass | pass | pass | – | – | pass |
| island-timeline | pass | pass | pass | pass | – | – | pass |
| storms | pass | pass | pass | pass | – | – | pass |
| postcards | pass | pass | pass | pass | – | – | pass |
| permits | pass | pass | pass | pass | – | – | pass |
| jetties | pass | pass | pass | pass | – | – | pass |
| guide | pass | pass | pass | pass | – | – | pass |
| properties | pass | pass | pass | pass | – | – | pass |
| households | pass | pass | pass | pass | – | – | pass |
| roads | pass | pass | pass | pass | – | – | pass |
| gaps | pass | pass | pass | pass | – | – | pass |
| sand | pass | pass | pass | pass | – | – | pass |
| practice | pass | pass | pass | pass | – | – | pass |
| account | pass | pass | pass | pass | – | – | pass |
| sms | pass | pass | pass | pass | – | – | pass |
| password | pass | pass | pass | pass | – | – | pass |
| calendar | pass | pass | pass | pass | – | pass | pass |
| members | pass | pass | – | – | – | – | pass |
| dues | pass | pass | – | – | – | – | pass |
| finance | pass | pass | – | – | – | – | pass |
| bank | pass | pass | – | – | – | – | pass |
| work | pass | pass | – | – | – | – | pass |
| budget | pass | pass | – | – | – | – | pass |
| reports | pass | – | – | – | – | – | pass |
| appmap | pass | pass | – | – | – | – | pass |
| archive:overview | pass | pass | pass | – | – | – | – |
| archive:newsletter | pass | pass | pass | – | – | – | – |
| archive:sms | pass | pass | pass | – | – | – | – |
| archive:volunteers | pass | pass | pass | – | – | – | – |
| archive:bank | pass | pass | pass | – | – | – | – |
| archive:research | pass | pass | pass | – | – | – | – |
| archive:payments | pass | pass | pass | – | – | – | – |
| archive:meetings | pass | pass | pass | – | – | – | – |
| archive:minutes | pass | pass | pass | – | – | – | – |
| archive:votes | pass | pass | pass | – | – | – | – |
| archive:elections | pass | pass | pass | – | – | – | – |
| archive:governance | pass | pass | pass | – | – | – | – |
| archive:documents | pass | pass | pass | – | – | – | – |
| archive:calendar | pass | pass | pass | – | – | – | – |
| archive:events | pass | pass | pass | – | – | – | – |
| archive:households | pass | pass | pass | – | – | – | – |
| archive:issues | pass | pass | pass | – | – | – | – |
| archive:bids | pass | pass | pass | – | – | – | – |
| archive:finance | pass | pass | – | – | – | – | – |
| archive:work | pass | pass | – | – | – | – | – |
| archive:members | pass | pass | – | – | – | – | – |

## Forms

| Role | Tool | Form | Result | Detail |
|---|---|---|---|---|
| resident | team | Send to the board inbox (to_position,subject,body) | pass | saved and shown · POST /api/team/messages |
| admin | team | Send to the board inbox (to_position,subject,body) | pass | saved and shown · POST /api/team/messages |
| board | team | Send to the board inbox (to_position,subject,body) | pass | saved and shown · POST /api/team/messages |
| admin | team | Save (member_name,contact_phone,contact_email,) | pass | saved and shown · PUT /api/officeholders/3e6dca98-2994-4631-9def-76e0d7a7156d |
| board | team | Save (member_name,contact_phone,contact_email,) | pass | saved and shown · POST /api/officeholders |
| resident | payments | Save new password (current_password,new_password,repeat_pas) | skip | password form: would change the test account's password |
| resident | payments | Save (fund,payment_method,amount,payment_year,) | info | no request sent (client-side form) · Select Community events when linking a specific event. |
| resident | issues | Submit to board (title,category,location,description,file) | pass | saved; Issue submitted for next-meeting review. Receipt: 781dcad0-fb1a-4ad5-aeda-a6ee84435f7d · POST /api/issues, POST /api/photos |
| admin | team | Save note (board_note) | pass | saved and shown · PUT /api/team/messages/65bd0567-b40c-49a5-972c-c24118c77004 |
| board | team | Save note (board_note) | pass | saved and shown · PUT /api/team/messages/65bd0567-b40c-49a5-972c-c24118c77004 |
| admin | payments | Save new password (current_password,new_password,repeat_pas) | skip | password form: would change the test account's password |
| admin | payments | Save (recipient_name,recipient_identifier,enab) | pass | saved and shown · PUT /api/payment-settings |
| board | payments | Save new password (current_password,new_password,repeat_pas) | skip | password form: would change the test account's password |
| board | payments | Save (fund,payment_method,amount,payment_year,) | info | no request sent (client-side form) · Select Community events when linking a specific event. |
| admin | payments | Save (state,board_note) | pass | saved and shown · PUT /api/payment-reports/b2c4cf24-a857-434c-9ffa-652ed3566404 |
| board | payments | Save (state,board_note) | pass | saved and shown · PUT /api/payment-reports/b2c4cf24-a857-434c-9ffa-652ed3566404 |
| admin | payments | Save (category,location,status,source_url,note) | warn | saved; Source-checked advisory posted with an expiry time. · POST /api/advisories |
| board | payments | Save (category,location,status,source_url,note) | warn | saved; Source-checked advisory posted with an expiry time. · POST /api/advisories |
| admin | summer | Save for everyone (summer-editor) | pass | saved and shown · PUT /api/content/summer-events |
| board | issues | Submit to board (title,category,location,description,file) | pass | saved and shown · POST /api/issues, POST /api/photos |
| resident | volunteers | Save email preference () | pass | saved; Volunteer email opt-in saved. · PUT /api/volunteer-email-preferences |
| admin | issues | Submit to board (title,category,location,description,file) | pass | saved and shown · POST /api/issues, POST /api/photos |
| board | issues | Upload photos (file,caption,credit,consent) | pass | saved and shown · POST /api/photos |
| resident | volunteers | Confirm signup (note) | warn | saved; You are signed up. Your name and note are visible only to you and the board. · PUT /api/volunteers/208c294e-ad7c-461b-9d09-31e19107e458/signup |
| admin | issues | Upload photos (file,caption,credit,consent) | pass | saved and shown · POST /api/photos |
| resident | events | Upload photos (file,caption,credit,consent) | pass | saved and shown · POST /api/photos |
| resident @375px | payments | Save new password (current_password,new_password,repeat_pas) | skip | password form: would change the test account's password |
| resident @375px | payments | Save (fund,payment_method,amount,payment_year,) | info | no request sent (client-side form) · Select Community events when linking a specific event. |
| resident @375px | issues | Submit to board (title,category,location,description,file) | pass | saved; Issue submitted for next-meeting review. Receipt: fdf02f98-b878-431f-bb88-d39736d8faef · POST /api/issues, POST /api/photos |
| board | members | Save (role,household_uid) | pass | saved; Account permissions saved. · PUT /api/members/1f9bf384-9ca1-4497-a181-ea457a1c58fe |
| board | members | Save (household_uid,note) | warn | saved; Property linked to this account. · POST /api/member-households |
| admin | members | Save (role,household_uid) | pass | saved; Account permissions saved. · PUT /api/members/1f9bf384-9ca1-4497-a181-ea457a1c58fe |
| resident | research | Search our documents (research-form) | warn | saved; Records refreshed. · POST /api/research |
| admin | members | Save (household_uid,note) | warn | refused by a rule: POST /api/member-households → 400: {"detail":"That property is already linked to this account."} |
| board | households | Submit memory (title,history_year,story) | pass | saved and shown · POST /api/house-history |
| admin | households | Submit memory (title,history_year,story) | pass | saved and shown · POST /api/house-history |
| resident @375px | volunteers | Save email preference () | pass | saved; Volunteer email opt-out saved. · PUT /api/volunteer-email-preferences |
| resident @375px | volunteers | Confirm signup (note) | warn | saved; You are signed up. Your name and note are visible only to you and the board. · PUT /api/volunteers/de9dbe00-3c1b-47be-b432-46f240ebc6f8/signup |
| resident @375px | message | Send to the board inbox (to_position,subject,body) | warn | saved; the new text is not shown afterwards · POST /api/team/messages |
| resident | bids | Save (contractor,contact,amount,tax_basis,scop) | pass | saved and shown · POST /api/bids |
| resident | bids | Save (file,caption) | pass | saved and shown · POST /api/bids/9ee764f1-7b2c-4ddb-94bd-4cda8e59981a/files |
| board | volunteers | Save private draft (title,category,description,location,task) | pass | saved and shown · POST /api/volunteers |
| board | volunteers | Save email preference () | pass | saved; Volunteer email opt-in saved. · PUT /api/volunteer-email-preferences |
| admin | volunteers | Save private draft (title,category,description,location,task) | pass | saved and shown · POST /api/volunteers |
| admin | volunteers | Save email preference () | pass | saved; Volunteer email opt-in saved. · PUT /api/volunteer-email-preferences |
| board | volunteers | Attach task photo (file) | pass | saved; Photo added to the task draft; location metadata removed. · POST /api/volunteers/36c9b506-e06f-4893-92f4-5de203111cea/photo |
| admin | volunteers | Attach task photo (file) | pass | saved; Photo added to the task draft; location metadata removed. · POST /api/volunteers/36c9b506-e06f-4893-92f4-5de203111cea/photo |
| board | volunteers | Confirm signup (note) | warn | saved; You are signed up. Your name and note are visible only to you and the board. · PUT /api/volunteers/a366dd48-ba72-42eb-a32c-7e9391ad29ff/signup |
| admin | volunteers | Confirm signup (note) | warn | saved; You are signed up. Your name and note are visible only to you and the board. · PUT /api/volunteers/a366dd48-ba72-42eb-a32c-7e9391ad29ff/signup |
| board | events | Next: add the date (title,description) | warn | saved and shown · POST /api/series |
| admin | events | Next: add the date (title,description) | warn | saved and shown · POST /api/series |
| board | events | Save (series_id,supper_year,title,event_date,r) | pass | saved and shown · PUT /api/events/046cf63d-14ba-4d63-a538-0b70755d6d79 |
| admin | events | Save (series_id,supper_year,title,event_date,r) | pass | saved and shown · PUT /api/events/046cf63d-14ba-4d63-a538-0b70755d6d79 |
| admin | votes | Save as draft (decision,meeting_id,amount,emergency,str) | pass | saved and shown · POST /api/votes/classify, POST /api/votes, POST /api/votes/classify |
| admin | votes | Save (document_id,version_label,adopted_on,onl) | pass | saved and shown · PUT /api/voting-procedures, PUT /api/settings/public_facebook_group_note, PUT /api/settings/public_local_sands_note |
| board | meetings | Save (meeting_id,title,description,state,audie) | pass | saved and shown · POST /api/agenda |
| admin | meetings | Save (title,meeting_date,meeting_time,duration) | pass | saved and shown · POST /api/meetings |
| admin | meetings | Save (meeting_id,title,description,state,audie) | pass | saved and shown · POST /api/agenda |
| admin | meetings | Save (zoom_url,reminder_hours) | pass | saved; Zoom link and reminder preference saved. Delivery remains inactive. · PUT /api/meetings/fffa8d39-0db7-4166-91ce-eaf7f4d74c68/access |
| board | governance | Save (member_name,household_uid,term_start,ter) | pass | saved and shown · PUT /api/officeholders/3e6dca98-2994-4631-9def-76e0d7a7156d |
| admin | governance | Save (member_name,household_uid,term_start,ter) | pass | saved and shown · PUT /api/officeholders/3e6dca98-2994-4631-9def-76e0d7a7156d |
| board | governance | Save (title,meeting_date,decision_type,motion,) | pass | saved and shown · POST /api/decisions |
| resident | households | Submit memory (title,history_year,story) | pass | saved and shown · POST /api/house-history |
| admin | governance | Save (title,meeting_date,decision_type,motion,) | pass | saved and shown · POST /api/decisions |
| board | documents | Upload & prepare suggestions (title,category,document_year,description) | pass | saved and shown · POST /api/documents |
| admin | documents | Upload & prepare suggestions (title,category,document_year,description) | pass | saved and shown · POST /api/documents |
| board | documents | Save (privacy) | pass | saved; Document visibility updated. · PUT /api/documents/ef4b4b63-d081-4064-a8c6-3b19fd029153/visibility |
| admin | documents | Save (privacy) | pass | saved; Document visibility updated. · PUT /api/documents/d29ffb95-96c4-4536-8f26-13650f4e4fb4/visibility |
| board | research | Search our documents (research-form) | warn | saved; Records refreshed. · POST /api/research |
| admin | research | Search our documents (research-form) | warn | saved; Records refreshed. · POST /api/research |
| board | bids | Save (title,work_id,scope,location,deadline,st) | pass | saved and shown · POST /api/bid-requests |
| resident | practice | Preview a practice submission (practice-issue) | info | no request sent (client-side form) · PRACTICE ONLY. Fictional examples, not HBA records. Nothing here is uploaded, saved, billed, emailed or published. Switching to the board example does |
| board | bids | Save (contractor,contact,amount,tax_basis,scop) | pass | saved and shown · POST /api/bids |
| admin | bids | Save (title,work_id,scope,location,deadline,st) | pass | saved and shown · POST /api/bid-requests |
| board | bids | Save (state,note) | pass | saved; Review recorded. No contract, payment or budget entry was created. · POST /api/bids/b477c6f8-7195-4702-b642-11297e51e7db/review |
| admin | bids | Save (contractor,contact,amount,tax_basis,scop) | pass | saved and shown · POST /api/bids |
| board | bids | Save (file,caption) | pass | saved and shown · POST /api/bids/85f63563-9e93-4efe-a24c-f6aa0d8a4fd3/files |
| admin | bids | Save (state,note) | pass | saved; Review recorded. No contract, payment or budget entry was created. · POST /api/bids/85f63563-9e93-4efe-a24c-f6aa0d8a4fd3/review |
| admin | bids | Save (file,caption) | pass | saved and shown · POST /api/bids/85f63563-9e93-4efe-a24c-f6aa0d8a4fd3/files |
| resident | sms | Save signup & consent (phone,topics,topics,topics,topics,topics) | info | no request sent (client-side form) · Select at least one topic. |
| board | dues | Update affordability timeline (tl-form) | info | no request sent (client-side form) · 0 of 5 selected projects funded within 2027–2066. Ending project capital: $38. \| Uses the scenario currently displayed below. \| Loading budget simulat |
| admin | dues | Update affordability timeline (tl-form) | info | no request sent (client-side form) · 0 of 5 selected projects funded within 2027–2066. Ending project capital: $38. \| Uses the scenario currently displayed below. \| Loading budget simulat |
| admin | finance | Save transaction (transaction_date,direction,category_code) | pass | saved and shown · POST /api/register |
| admin | finance | Save budget line (category_code,amount,basis,source_note) | pass | saved; Records refreshed. \| Updated 10/29/2026, 9:52:08 AM Eastern. Refreshes every 30 seconds while this view is open. · PUT /api/category-budgets/2026 |
| admin | finance | Confirm household credit (payer_id,household_uid,dues_year,amount,) | warn | refused by a rule: POST /api/dues-receipts → 400: {"detail":"This household was already marked paid outside the receipt ledger. Reconcile the older record before adding a new credit; do not count the same check |
| board | work | Save (title,contractor,location,work_date,desc) | pass | saved and shown · POST /api/work |
| board | work | Save (flag,note) | pass | saved and shown · POST /api/work/e56d5437-0bd2-4e9e-b30b-54b7ca06393a/notes |
| admin | bank | Save account reference (label,last_four) | pass | saved and shown · POST /api/bank/accounts |
| admin | bank | Import for review (period_start,period_end,statement_closin) | info | no request sent (client-side form) · Missing CSV column: posted_date |
| admin | bank | Publish member summary (period_end,statement,confirm) | pass | saved and shown · POST /api/bank/summaries |
| admin | work | Save (title,contractor,location,work_date,desc) | pass | saved and shown · POST /api/work |
| admin | work | Save (flag,note) | pass | saved and shown · POST /api/work/9aa58b8f-4b39-4a60-a1b2-edc5a3ee453a/notes |
| board | practice | Preview a practice submission (practice-issue) | info | no request sent (client-side form) · PRACTICE ONLY. Fictional examples, not HBA records. Nothing here is uploaded, saved, billed, emailed or published. Switching to the board example does |
| board | sms | Save signup & consent (phone,topics,topics,topics,topics,topics) | info | no request sent (client-side form) · Select at least one topic. |
| board | sms | Save draft only (category,message) | pass | saved and shown · POST /api/sms/drafts |
| admin | practice | Preview a practice submission (practice-issue) | info | no request sent (client-side form) · PRACTICE ONLY. Fictional examples, not HBA records. Nothing here is uploaded, saved, billed, emailed or published. Switching to the board example does |
| admin | sms | Save signup & consent (phone,topics,topics,topics,topics,topics) | info | no request sent (client-side form) · Select at least one topic. |
| admin | sms | Save draft only (category,message) | pass | saved and shown · POST /api/sms/drafts |
| admin | archive:newsletter | Save draft (title,issue_date,issue_precision,body) | pass | saved and shown · POST /api/newsletters |
| board | archive:meetings | Save (title,meeting_date,meeting_time,duration) | pass | saved and shown · POST /api/meetings |
| board | archive:meetings | Save (zoom_url,reminder_hours) | pass | saved; Zoom link and reminder preference saved. Delivery remains inactive. · PUT /api/meetings/8a3339c9-6583-4deb-94cb-3d707cec2c99/access |
| admin | archive:minutes | Save draft (meeting_id,title,meeting_date,meeting_ti) | pass | saved and shown · POST /api/minutes |
| board | archive:votes | Save as draft (decision,meeting_id,amount,emergency,str) | warn | saved; the new text is not shown afterwards · POST /api/votes/classify |

## Flows and access checks

| Role | Check | Result | Detail |
|---|---|---|---|
| admin | sign-in: sign in and dashboard loads | pass |  |
| board | sign-in: sign in and dashboard loads | pass |  |
| resident | sign-in: sign in and dashboard loads | pass |  |
| resident | dashboard: board-only tools hidden from residents | pass |  |
| board-as-resident | sign-in: sign in and dashboard loads | pass |  |
| board-as-resident | view switch: Resident view hides board tools in the member app | pass | portal bar: Resident view preview |
| board-as-resident | view switch: Board view brings the board tools back | pass | appmap, bank, budget, dues, finance, members, work |
| board | slow connection: dashboard shows the board account when its script loads late | pass |  |
| pending | sign-in: pending account sees the waiting page | pass | Photograph · Hamilton Beach after a shower, shared by a resident  Hamilton Beach Association  Welcome back.  Sign in to view the map, island history and associa |
| pending | access: pending account cannot read the archive API | pass | HTTP 403 |
| pending | access: opening /app/ directly shows no member data | pass | blocked |
| resident @375px | sign-in: sign in and dashboard loads | pass |  |
| resident @375px | dashboard: board-only tools hidden from residents | pass |  |
| admin @375px | sign-in: sign in and dashboard loads | pass |  |
| resident | sign-in: sign in and dashboard loads | pass |  |
| resident | archive:meetings: 1 of 1 board-made item(s) visible to a resident | info | visible: E2E 10290940 boa archive:meetings 34 |
| resident | archive:minutes: 0 of 1 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | archive:newsletter: 0 of 1 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | bank: 2 item(s) made by the board | info | tool is board-only |
| resident | bids: 0 of 6 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | documents: 2 of 2 board-made item(s) visible to a resident | info | visible: E2E 10290940 boa documents 21, E2E 10290940 adm documents 26 |
| resident | events: 3 of 4 board-made item(s) visible to a resident | info | visible: E2E 10290940 boa events 16, E2E 10290940 adm events 17, E2E 10290940 adm events 18 |
| resident | finance: 1 item(s) made by the board | info | tool is board-only |
| resident | governance: 1 of 4 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm governance 24 |
| resident | households: 2 of 2 board-made item(s) visible to a resident | info | visible: E2E 10290940 boa households 11, E2E 10290940 adm households 12 |
| resident | issues: 0 of 4 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | meetings: 1 of 3 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm meetings 21 |
| resident | payments: 2 of 3 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm payments 4, E2E 10290940 boa payments 5 |
| resident | sms: 0 of 2 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | summer: 1 of 1 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm summer 7 |
| resident | team: 2 of 6 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm team 2, E2E 10290940 boa team 2 |
| resident | volunteers: 0 of 2 board-made item(s) visible to a resident | info | none visible (expected for board-only records; check drafts) |
| resident | votes: 1 of 2 board-made item(s) visible to a resident | info | visible: E2E 10290940 adm votes 20 |
| resident | work: 4 item(s) made by the board | info | tool is board-only |

## Failures (0)


## Controls clicked inside tools

3238 clicks across 199 tool visits. Skipped by design: delete/remove, approve/reject, sign out, password changes, sending texts, certifying votes, hiding tools, switching views (each has its own check above). Confirmation prompts were answered Cancel.

## Seed data (through the API)

| Step | Result | Detail |
|---|---|---|
| sign up board@hba.test | pass | HTTP 200 {"message":"Check your email to confirm your address, then sign in. Your request then goes to the board for approval; you will see a waiting screen until a boar |
| sign up pending@hba.test | pass | HTTP 200 {"message":"Check your email to confirm your address, then sign in. Your request then goes to the board for approval; you will see a waiting screen until a boar |
| approve board@ as board | pass |  |
| link resident@ to a household | pass |  |
| event series | pass |  |
| events | pass |  |
| meetings | pass |  |
| agenda item | pass |  |
| minutes (with PDF, approved) | pass |  |
| newsletter (with PDF, published) | pass |  |
| votes (advisory poll + capital motion) | pass |  |
| volunteer task (published, resident signed up) | pass |  |
| check register entries | pass |  |
| dues statuses | pass |  |
| payment report (resident) | pass |  |
| bid request + bid | pass |  |
| issue (resident) | pass |  |
| contractor work + note | pass |  |
| document upload | pass |  |
| event photo (resident upload, board publishes) | pass |  |
| household story (resident) | pass |  |
| message to a governor (resident) | pass |  |
| storm memory (resident) | pass |  |
| officeholder | pass |  |

## Link check

Internal: 1997 references — 181 resolve, 0 broken, 0 workstation paths in data files, 1816 record scans (shipped separately in hba-portal-record-scans.zip). 2 built at run time from templates were not checked statically (the walkthrough exercises them).


External: 420 links — 418 answer, 2 refuse automated checks (401/403/429), 0 fail.

- warn: https://onlinelibrary.wiley.com/doi/10.1002/esp.5784 (HTTP 403) — in private-app/sand-school/learn.html
- warn: https://onlinelibrary.wiley.com/doi/pdf/10.1002/esp.1527 (HTTP 403) — in private-app/sand-school/learn.html

Options: (none)
