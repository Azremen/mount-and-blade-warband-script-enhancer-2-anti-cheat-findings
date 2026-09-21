# Cheater Watchlist

Confirmed cheaters from real (non-test) sessions. See `CHEAT_TEST_FINDINGS.md`
for the full log evidence behind each entry.

## Confirmed cheaters

| Name(s) seen | Unique ID | Cheat type | Source |
|---|---|---|---|
| `63rd_lebrun` | `2226106` | Autoblock | Owner confirmed; `Assassins Server/server_log_11.09.2026.txt` |
| `Assassins_ayzox` | `2527452` | Speedhack + autoblock | Owner confirmed; `Assassins Server/server_log_11.09.2026.txt` |
| `63rd_blowjob` | `1589927` | Autoblock | Owner confirmed; 6 further offscreen detections in `63rd Server/server_log_13.09.2026.txt` corroborate the verdict. |
| `108th_KurdCommunist` / `9th_AdrianHepard` | `2448918` | Autoblock | Owner confirmed; 5 type `14` detections with repeated offscreen signals in `63rd Server/server_log_14.09.2026.txt`. |
| `63rd_lenox` | `2226106` | Autoblock | 18 detections in one session; final `autoblock_match_pct=100`, with repeated match-rate and offscreen signals. Same GUID as the earlier confirmed `63rd_lebrun` account. |
| `108th_Rodina_Mat_Saratova` | `2031011` | Autoblock | 6 detections with repeated offscreen signals; final match rate `82%`, reaction `240 ms`. Same GUID as the earlier `[Legion_SvD]_Hm` account. |
| `108th_Saratov_02` | `2298580` | Autoblock | 7 detections and repeated offscreen alerts; final match rate `32%`, reaction `1435 ms`. |
| `[Legion_SvD]_Hm` | `2031011` | Autoblock | 8 offscreen detections in 39 min (`13.09.2026`); automation marked this account threat level 4. |
| `63rd_lebrun` | `1832685` | Autoblock | Different account from confirmed `63rd_lebrun` (`2226106`): 4 detections in 19 min, including offscreen, feint-follow, and match-rate `90/90` signals. |
| `63rd_Rec_Fiszek` | `1098052` | Autoblock | Across two separate server sessions, triggered all three autoblock sub-signals at least once each (offscreen, match-rate `90/90`, feint-follow `8/8`); final offscreen snapshot `4`. |
| `Asassins_Wilhelm` | `2508655` | Autoblock | Single session; one match-rate crossing (`90/90`) and a final offscreen snapshot of `4`, above the honest 0-2 ceiling. |
| `87th_Irish_LnCpl_Wolk` | `2026867` | Autoblock | 5 detections in 78 min (`12.09.2026`); match-rate spikes reaching `92/90` and `95/90`, plus feint-follow (`8/8`) and offscreen (`6/6`). |
| `87th_Irish_Mus_GROMOBOY` | `2563664` | Autoblock | 3 detections in 81 min (`12.09.2026`); match-rate spikes reaching `100/90` and `90/90`, plus offscreen (`6/6`). |
| `87th_Irish_LtCol_Khizar` | `2484596` | Autoblock | 4 detections in 21 min (`12.09.2026`); match-rate spike reaching `95/90`, plus 3x offscreen (`6/6`). |
| `Nr31[FKR]_KFwb_Arkan` | `2116360` | Autoblock | 3 type `14` offscreen crossings (`10/6`, `6/6`, `6/6`) in `63rd Server/server_log_16.09.2026.txt`. |

## Offscreen-related observations

The accounts below produced repeated offscreen autoblock signals. They remain in the confirmed table
above because that table records the current project verdicts, but offscreen evidence must not be
treated as conclusive on its own.

A player using an FOV setting above the default may see attacks that the detector classifies as outside
its assumed view cone. Higher-than-default FOV can therefore produce offscreen detections without proving
autoblock. Confirmation requires independent corroboration such as match-rate or feint-follow crossings,
owner confirmation, or other reliable evidence.

| Name(s) seen | Unique ID | Offscreen evidence |
|---|---|---|
| `[Legion_SvD]_Hm` / `108th_Rodina_Mat_Saratova` | `2031011` | 8 offscreen detections on `13.09.2026`; later sessions used the same GUID. |
| `108th_Saratov_02` | `2298580` | 7 detections with repeated offscreen alerts. |
| `Nr31[FKR]_KFwb_Arkan` | `2116360` | 3 offscreen threshold crossings: `10/6`, `6/6`, and `6/6`. |

Note: `lebrun` was initially reported as speedhack + autoblock, but the developer's investigation
confirmed his tool never touches the game clock, so the speedhack label has been removed for this
account; his confirmed cheat is autoblock only, on solid type `14` evidence.

Note: `ayzox`'s speedhack case did not produce a type `11` (clock skew) detection at the time this
log was captured. The developer has since root-caused and fixed the clock-skew detector (see
`CHEAT_TEST_FINDINGS.md`, "Consequence for calibration"): `ayzox`'s case was a genuine miss caused by
an old, too-loose threshold (now fixed and lowered).
(auto block) evidence above.

## Special Thanks

Special thanks to `63rd_OZBEK`, `63rd_Kurdishim_Abo` (primarily known as `Fred`), and
`63rd_Rgl_ramadan_baighara` for serving as anti-cheat testers, and to
`63rd_General_Eternal` for sponsoring their testing work.

## Maintenance

When a new session is reviewed:

1. Add newly confirmed cheaters to the top table with the cheat type and source log.
2. Include the supporting log or review source when adding a confirmed account.
3. Never merge a "cleared" account back into suspicion without citing new detection evidence.
4. Keep this file's names/IDs in sync with `CHEAT_TEST_FINDINGS.md`; that file remains the source of
   full evidence and reasoning, this file is the short-form roster.
