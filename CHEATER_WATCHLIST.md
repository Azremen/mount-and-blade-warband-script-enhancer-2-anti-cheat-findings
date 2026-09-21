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
| `63rd_Rec_Fiszek` | `1098052` | Autoblock | Across two separate server sessions, triggered all three autoblock sub-signals at least once each (offscreen, match-rate `90/90`, feint-follow `8/8`); final offscreen snapshot `4`. |
| `Asassins_Wilhelm` | `2508655` | Autoblock | Single session; one match-rate crossing (`90/90`) and a final offscreen snapshot of `4`, above the honest 0-2 ceiling. |
| `87th_Irish_LnCpl_Wolk` | `2026867` | Autoblock | 5 detections in 78 min (`12.09.2026`); match-rate spikes reaching `92/90` and `95/90`, plus feint-follow (`8/8`) and offscreen (`6/6`). |
| `87th_Irish_Mus_GROMOBOY` | `2563664` | Autoblock | 3 detections in 81 min (`12.09.2026`); match-rate spikes reaching `100/90` and `90/90`, plus offscreen (`6/6`). |
| `87th_Irish_LtCol_Khizar` | `2484596` | Autoblock | 4 detections in 21 min (`12.09.2026`); match-rate spike reaching `95/90`, plus 3x offscreen (`6/6`). |
| `Nr31[FKR]_KFwb_Arkan` | `2116360` | Autoblock | 3 type `14` offscreen crossings (`10/6`, `6/6`, `6/6`) in `63rd Server/server_log_16.09.2026.txt`. |

## Offscreen-related observations

The table below is a GUID-based inventory of type `14` offscreen threshold crossings (`threshold=6`)
for non-test accounts in the available `63rd Server` logs. Credited testers and the test sponsor are
excluded. It is a detector inventory, not a list of confirmed cheaters. The match-rate and feint columns
show other type `14` sub-signals found for the same GUID.

A player using an FOV setting above the default may see attacks that the detector classifies as outside
its assumed view cone. Higher-than-default FOV can therefore produce offscreen detections without proving
autoblock. Confirmation requires independent corroboration such as match-rate or feint-follow crossings,
owner confirmation, or other reliable evidence.

GUID `1832685` used the name `63rd_lebrun`, but it is not linked to confirmed GUID `2226106` merely
because the nickname matches. It produced 4 type `14` detections (2 offscreen, 1 match-rate, and 1
feint-follow), below the 8-detection confirmation threshold. Its final summary reported
`autoblock_match_pct=7`, `autoblock_reaction_ms=564`, `autoblock_offscreen=0`, and
`autoblock_feints=0`. Under the corrected evaluator, the low match rate and slow reaction
place this profile in the noise-prone observation category rather than the confirmed roster.

| Name(s) seen | Unique ID | Offscreen | Match-rate | Feint-follow | Log date(s) |
|---|---:|---:|---:|---:|---|
| `*_[Legion_SvD]_LJE-MARAT` / `[Legion_SvD]_Mokrif` | `2492046` | 2 | 0 | 0 | `13.09.2026` |
| `[Legion_SvD]_Chell00212` | `2593302` | 4 | 0 | 1 | `13.09.2026` |
| `[Legion_Svd]_Fuhrer_GIORGI` | `2433518` | 2 | 0 | 0 | `13.09.2026` |
| `[Legion_SvD]_Hm` / `108th_Rodina_Mat_Saratova` | `2031011` | 13 | 0 | 1 | `13.09.2026`, `14.09.2026` |
| `[Legion_SvD]_k_La_Furia_Roja` / `9th_Rus_Mjr_karpik_` | `1342193` | 6 | 0 | 0 | `13.09.2026`, `14.09.2026` |
| `[Legion_SvD]_Maj_Evil_Xomik` | `2491664` | 3 | 1 | 1 | `13.09.2026` |
| `[Legion_SvD]_ZeroTwo` / `108th_Saratov_02` / `9th_ZeroTwo` | `2298580` | 13 | 1 | 2 | `13.09.2026`, `14.09.2026` |
| `[Legion_SvD]Amelie_Lampard` | `2557146` | 2 | 1 | 1 | `13.09.2026` |
| `[LegionSvD]_Igorrr_` / `9th_Rus_efr_ISOctober` | `2583313` | 3 | 0 | 1 | `13.09.2026`, `14.09.2026` |
| `[Legion-SvD]Verhovna_rada` | `2040869` | 1 | 1 | 0 | `13.09.2026` |
| `108th[OG]SPIDI` / `63rd_Rec_Maxitan[ChmoPetuh]` / `63rd_Rec_SPIDI` | `2441522` | 3 | 1 | 1 | `13.09.2026`, `14.09.2026` |
| `108th_KurdCommunist` / `9th_AdrianHepard` | `2448918` | 6 | 0 | 0 | `14.09.2026` |
| `108th_Osian` | `2492309` | 2 | 0 | 0 | `14.09.2026` |
| `108th_Saratov_Artem` / `63rd_Artem` | `2445527` | 9 | 0 | 1 | `14.09.2026` |
| `108th_Saratov_Boeboba` | `2225407` | 1 | 0 | 0 | `14.09.2026` |
| `Asassins_Ceed` / `108th_Saratov_Messi` / `9_BOPOH` | `1738245` | 14 | 0 | 0 | `14.09.2026` |
| `12th_CplFoP_Movement` | `1269742` | 1 | 0 | 1 | `15.09.2026` |
| `12th_GOAT_Flo` | `9318` | 7 | 0 | 0 | `15.09.2026` |
| `12th_Greg_Gorgo` | `372274` | 4 | 0 | 0 | `15.09.2026` |
| `12th_LCpl_Denis` | `635181` | 2 | 0 | 0 | `15.09.2026` |
| `12th_LtCol_Nova` | `1637460` | 1 | 0 | 0 | `15.09.2026` |
| `12th_OG_Lefty` | `1389481` | 1 | 0 | 0 | `15.09.2026` |
| `12th_rec_Luke` | `1594268` | 3 | 0 | 0 | `15.09.2026` |
| `12th_Rundeen` | `2283886` | 3 | 0 | 0 | `15.09.2026` |
| `12th_Sjt_Jake` | `2189042` | 2 | 1 | 1 | `15.09.2026` |
| `12th_Slut_Jack` | `1153761` | 1 | 0 | 0 | `15.09.2026` |
| `63rd_AntiDi` | `1979846` | 1 | 0 | 1 | `14.09.2026` |
| `63rd_blowjob` | `1589927` | 7 | 0 | 0 | `11.09.2026`, `13.09.2026` |
| `63rd_Bluzbek` | `1146243` | 3 | 0 | 1 | `15.09.2026` |
| `63rd_Bob` | `2560835` | 4 | 1 | 0 | `13.09.2026`, `14.09.2026` |
| `63rd_Cpl_fatihmehmet` | `1928336` | 1 | 0 | 0 | `12.09.2026` |
| `63rd_GJack` | `2087362` | 1 | 0 | 0 | `16.09.2026` |
| `63rd_Gren_Ingemard` | `2551450` | 1 | 1 | 0 | `11.09.2026` |
| `63rd_gren_jack` / `63rd_jack` / `63rd_lazsiken_jack` | `1724198` | 8 | 1 | 0 | `14.09.2026`, `16.09.2026` |
| `63rd_Gren_SteeL` / `63rd_SteeL` | `2065478` | 13 | 0 | 2 | `14.09.2026`-`16.09.2026` |
| `63rd_Kgm_Nedim` | `395164` | 10 | 2 | 0 | `14.09.2026`, `16.09.2026` |
| `63rd_lebrun` | `1832685` | 2 | 1 | 1 | `13.09.2026` |
| `63rd_lenox` / `LenoX` | `2226106` | 18 | 3 | 0 | `11.09.2026`, `14.09.2026` |
| `63rd_Ozbeki` | `1513490` | 2 | 1 | 1 | `15.09.2026` |
| `63rd_Pwt_Klaused` | `1524719` | 1 | 1 | 0 | `16.09.2026` |
| `63rd_Rec_Fiszek` | `1098052` | 10 | 0 | 1 | `11.09.2026`, `14.09.2026` |
| `63rd_Zeyden` | `1556384` | 3 | 0 | 0 | `15.09.2026` |
| `87th_Irish_Gren_TalatPashaa` | `2484125` | 4 | 1 | 0 | `12.09.2026` |
| `87th_Irish_Gren_Warwilk` | `1882337` | 1 | 0 | 0 | `12.09.2026` |
| `87th_Irish_LnCpl_Wolk` | `2026867` | 2 | 2 | 1 | `12.09.2026` |
| `87th_Irish_LtCol_Khizar` | `2484596` | 3 | 1 | 0 | `12.09.2026` |
| `87th_Irish_Merc_nuBo_O6oLoHb` | `2289436` | 3 | 0 | 0 | `12.09.2026` |
| `87th_Irish_Mus_GROMOBOY` | `2563664` | 1 | 2 | 0 | `12.09.2026` |
| `87th_Irish_Pvt_Fexius` | `2584760` | 5 | 0 | 0 | `12.09.2026` |
| `9th_BARARARARARARARABLUD` | `2238437` | 3 | 1 | 1 | `14.09.2026` |
| `9th_Bieber` | `1235888` | 3 | 1 | 0 | `14.09.2026` |
| `9th_IMAM_ALI_ALLAX_ISLAM` | `2429903` | 4 | 0 | 0 | `14.09.2026` |
| `KloryTear` | `2122761` | 3 | 0 | 0 | `11.09.2026` |
| `Nr31[FKR]_Albert_Epstein` / `Nr31[FKR]_Ujg_SiGmaSvin` | `2300331` | 7 | 1 | 1 | `16.09.2026` |
| `Nr31[FKR]_Hptm_BIBA` | `2498648` | 1 | 0 | 0 | `16.09.2026` |
| `Nr31[FKR]_KFwb_Arkan` | `2116360` | 3 | 0 | 0 | `16.09.2026` |
| `Nr31[FKR]_Kpl_Fonifon` | `2523481` | 1 | 0 | 0 | `16.09.2026` |
| `Nr31[FKR]_Lt_Generadier` | `2525779` | 2 | 1 | 0 | `16.09.2026` |
| `Nr31[FKR]_Maj_GodyX` | `2515702` | 3 | 4 | 0 | `16.09.2026` |
| `Nr31[FKR]_StObJg_Ben` | `1282828` | 2 | 0 | 0 | `16.09.2026` |
| `Nr31[FKR]_StObjg_BlBA` | `2552880` | 1 | 0 | 1 | `16.09.2026` |
| `Nr31[FKR]_UJg_MrRifleman` | `2570456` | 8 | 1 | 2 | `16.09.2026` |

Note: confirmed GUID `2226106` was initially reported as speedhack + autoblock, but the developer's investigation
confirmed his tool never touches the game clock, so the speedhack label has been removed for this
account; his confirmed cheat is autoblock only, on solid type `14` evidence.

Note: `ayzox`'s speedhack case did not produce a type `11` (clock skew) detection at the time this
log was captured. The developer has since root-caused and fixed the clock-skew detector (see
`CHEAT_TEST_FINDINGS.md`, "Consequence for calibration"): `ayzox`'s case was a genuine miss caused by
an old, too-loose threshold (now fixed and lowered).
(auto block) evidence above.

## Special Thanks

Special thanks to the anti-cheat testers and sponsor who helped validate the
detector during calibration:

- `63rd_OZBEK`
- `63rd_Kurdishim_Abo` (primarily known as `Fred`)
- `63rd_Rgl_ramadan_baighara`
- `63rd_Col_Edward` / `63rd_BOZBEK`
- `63rd_General_Eternal`

## Maintenance

When a new session is reviewed:

1. Add newly confirmed cheaters to the top table with the cheat type and source log.
2. Include the supporting log or review source when adding a confirmed account.
3. Never merge a "cleared" account back into suspicion without citing new detection evidence.
4. Keep this file's names/IDs in sync with `CHEAT_TEST_FINDINGS.md`; that file remains the source of
   full evidence and reasoning, this file is the short-form roster.
