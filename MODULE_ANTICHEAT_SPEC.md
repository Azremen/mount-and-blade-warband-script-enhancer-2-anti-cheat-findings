# WSE2 Anti-Cheat — Module System Reference

This document describes the current WSE2 Module System integration alongside
its decision framework. The implementation lives in
`napoleonic-wars-anti-cheat/`; when this document and the source differ, the
source is authoritative.

---

## 1. Multi-Signal Decision Logic & Threat Matrix

### A. Deterministic vs. Statistical Violations

1. **Deterministic Violations (Zero-Tolerance / Immediate Action)**
   - **Seed Mismatch (`type == 16`)**: Client modified random seed. An honest client never produces a mismatch.
   - **Action**: Immediate confirmed verdict + high-priority server/admin alert. The player is only
     banned when `enforcement_mode == acm_enforce`; in silent mode the event is logged, not banned.
     Independent of `enforcement_mode`, the GUID is also added to
     `anticheat_seed_mismatch_blacklist.json` and permanently denied admission on every future join
     (see sections 2 and 4) — this does not expire and is not a `ban_player` call, since it must
     survive a `ban_player` ban expiring or being lifted.

2. **Heuristic / Statistical Violations (Multi-Signal Scoring)**
   - **Auto-Block (`type == 14`)**:
     - *Sub-Signal 1 — Match Rate (`value >= 90`)*: Rolling block direction match rate hit 90%+.
     - *Sub-Signal 2 — Offscreen Blocks (`value >= 6`)*: Player blocked attacks coming from outside 140° view cone 6+ times in the sample window.
     - *Sub-Signal 3 — Feint Follows (`value >= 8`)*: Player followed 8+ feints within 120ms.
     - **Confirmed Verdict Rules**:
       - `detections >= 8` + live `autoblock_match_pct >= 85`.
       - `detections >= 8` + repeated offscreen crossings + a match-rate spike or feint-follow crossing.
       - Repeated offscreen crossings alone remain **SUSPECTED**, so they alert the console/log but do not auto-ban without corroboration.
     - **Noise / False-Positive Filter**:
       - If final `autoblock_match_pct < 65%` AND `autoblock_reaction_ms > 500ms`, classify as **NOISE / LUCKY HUMAN** before suspected/confirmed autoblock rules.
     - **Alert minimums**:
       - `min_detections_suspected=6`: fewer detections are logged but do not generate suspected alerts.
       - `min_detections_watchlist=6`: the watchlist branch also requires `spikes_cnt` to reach
         `max_matchrate_spikes` (default `2`); one detection short of that count does not create an alert.
  - **Client Clock Skew / Speedhack (`type == 11`)**:
   - *Positive Skew (`time_skew_max_pct >= 10%` in at least 2 detections)*: Client running fast.
     `acs_time_skew_max` is a session maximum, so it does not fall back down between events; the
     `min_clock_skew_detections=2` gate therefore requires two separate skew detection events while the
     session maximum stays at or above the threshold, not two independent high readings.
     - *Negative Skew (`time_skew_stall_pct`)*: Lag / frame stalls / alt-tab. **Must be ignored** to prevent banning laggy players.

## 2. Module System Headers and Constants

Anti-cheat trigger, detection, statistic, and mode constants are declared in
`header_triggers_addon.py`, which is imported by `header_triggers.py`.
Project-owned threat levels, player slots, thresholds, and reason codes are in
`module_constants.py`. There is no `header_anticheat.py`.

```python
# module_constants.py
########################################################
##  WSE2 ANTI-CHEAT SLOTS     ##########################
########################################################

slot_player_cheat_threat_level        = 150
slot_player_cheat_total_detections    = 151
slot_player_cheat_offscreen_count     = 152
slot_player_cheat_matchrate_spikes    = 153
slot_player_cheat_feint_follows       = 154
slot_player_cheat_clock_skew_count    = 155
slot_player_cheat_seed_mismatches     = 156
slot_player_cheat_autoblock_detections = 158

threat_level_none       = 0
threat_level_noise      = 1
threat_level_watchlist  = 2
threat_level_suspected  = 3
threat_level_confirmed  = 4

ac_conf_max_offscreen_allowed    = 3
ac_conf_max_matchrate_spikes     = 2
ac_conf_min_detections_watchlist = 6
ac_conf_min_detections_suspected = 6
ac_conf_min_detections_confirmed = 8
ac_conf_history_window_seconds   = 1800
ac_conf_clock_skew_threshold_pct = 10
ac_conf_min_clock_skew_detections  = 2
ac_conf_noise_max_match_pct      = 65
ac_conf_noise_min_reaction_ms    = 500
ac_conf_sustained_match_pct      = 85

ac_reason_seed_mismatch           = 1
ac_reason_sustained_autoblock     = 2
ac_reason_repeated_offscreen      = 3
ac_reason_matchrate_watchlist     = 4
ac_reason_speedhack               = 5
ac_reason_multisignal_autoblock   = 6
```

### JSON Configuration Files

Keep the five JSON files in the server module directory. They intentionally use
separate dictionaries: `anticheat_config.json` contains thresholds and
enforcement settings, `anticheat_admin_guids.json` contains only admin GUID
flags, `anticheat_player_whitelist.json` contains normal-player GUID flags,
`anticheat_player_history.json` contains short-lived GUID-based detection
history, and `anticheat_seed_mismatch_blacklist.json` contains permanently
blacklisted GUIDs from confirmed seed mismatches.

```json
// anticheat_config.json
{
  "enforcement_mode": 1,
  "temp_ban_seconds": 3600,
  "history_window_seconds": 1800,
  "player_whitelist_admission_enabled": 1,
  "max_offscreen_allowed": 3,
  "max_matchrate_spikes": 2,
  "min_detections_watchlist": 6,
  "min_detections_suspected": 6,
  "min_detections_confirmed": 8,
  "clock_skew_threshold_pct": 10,
  "min_clock_skew_detections": 2,
  "noise_max_match_pct": 65,
  "noise_min_reaction_ms": 500,
  "sustained_match_pct": 85
}
```

`anticheat_player_history.json` is a module-managed, GUID-keyed runtime history file. On every
anti-cheat event it stores the accumulated detection counters and the current UNIX time. When a
player reconnects within `history_window_seconds` (default `1800`), the counters are restored before
the next detection is evaluated. Because the elapsed time is measured with UNIX time rather than the
mission timer, a map change or server restart does not reset the reconnect window. History remains
eligible for restoration for up to 30 minutes across those boundaries, but older history expires.

```json
// anticheat_admin_guids.json
{
  "admin_guid_1": 2575888,
  "admin_name_1": "Azremen",
  "admin_guid_2": 2289446,
  "admin_name_2": "63rd_General_Eternal"
}
```

The admin file is a flat dictionary, not an `admins` array. The module iterates its keys with
`try_for_dict_keys`, selects keys beginning with `admin_guid_`, derives the matching
`admin_name_N` key, and compares the integer value with `player_get_unique_id`. The module creates
the file with `script_create_default_admin_guid_file` if it is missing or empty.

```json
// anticheat_player_whitelist.json
{
  "player_guid_1": 2575888,
  "player_name_1": "Azremen",
  "player_guid_2": 2289446,
  "player_name_2": "63rd_General_Eternal"
}
```

The player whitelist is one flat dictionary, like the admin GUID file. The module reads this single
file on every join, so edits apply while the server is running. The default entries are Azremen
(`2575888`) and 63rd_General_Eternal (`2289446`). A matching GUID allows the player to join; it does not bypass
anti-cheat detections, alerts, kicks, or bans. An absent GUID denies admission when the admission
switch is enabled. This system does not
grant admin rights and is not a replacement for `anticheat_admin_guids.json`.

`player_whitelist_admission_enabled=1` is the default-on entry gate. When enabled, every
joining player, including an admin, must have a GUID entry in `anticheat_player_whitelist.json` or is
sent an in-game rejection message and immediately kicked. Set it to `0` to let all players join while
keeping anti-cheat enforcement active for every player.

```json
// anticheat_seed_mismatch_blacklist.json
{
  "blacklist_2226106": 1,
  "blacklist_name_2226106": "63rd_lebrun",
  "blacklist_time_2226106": 1758409200
}
```

Keyed by GUID rather than a numbered index (`blacklist_{guid}`, `blacklist_name_{guid}`,
`blacklist_time_{guid}`), this file starts empty and is only ever appended to at runtime by
`script_cf_add_seed_mismatch_blacklist`, called from `on_cheat_detected`'s seed-mismatch case. A
GUID never needs to be removed by the module itself; an admin can hand-edit the file to lift an entry.
Unlike `ban_player`, an entry here has no expiry and does not depend on `enforcement_mode` — every
join is checked against it, in silent mode too, and it overrides the player whitelist: a blacklisted
GUID is denied even if it is also present in `anticheat_player_whitelist.json`.

---

## 3. Trigger Interception (`module_mission_templates.py`)

```python
multiplayer_server_anticheat = (
  ti_on_cheat_detected, 0, 0, [],
  [
    (store_trigger_param, ":player_no", 1),
    (store_trigger_param, ":detection_type", 2),
    (store_trigger_param, ":value", 3),
    (store_trigger_param, ":threshold", 4),
    # script_on_cheat_detected sets reg0 to 1 only for detection types it
    # scores; unhandled types leave reg0 at 0 so native WSE2 action still runs.
    (call_script, "script_on_cheat_detected",
     ":player_no", ":detection_type", ":value", ":threshold"),
  ])

multiplayer_server_ensure_anticheat_json = (
  ti_before_mission_start, 0, ti_once, [],
  [
    (call_script, "script_ensure_admin_guid_file"),
    (call_script, "script_ensure_player_whitelist_file"),
    (call_script, "script_ensure_seed_mismatch_blacklist_file"),
    # script_cf_cache_anticheat_config calls script_ensure_anticheat_config itself.
    (call_script, "script_cf_cache_anticheat_config"),
    (call_script, "script_ensure_anticheat_player_history"),
  ])
```

Both triggers are entries in `mm_multiplayer_common`, so every mission
template using that shared list receives the initialization and detection
handler. `module_triggers.py` does not host this feature.

`script_cf_cache_anticheat_config` reads `anticheat_config.json` once per
mission and copies every value into `$g_ac_*` globals (see section 6). Every
other anti-cheat script reads these globals instead of the JSON file, so a
config edit — including `enforcement_mode` — takes effect on the next mission
start, not instantly. This is a separate switch from the native
`set_anticheat_mode`/`iMode` console command described in
`ANTICHEAT_SERVER_GUIDE.md`: that native mode changes live, but the module
suppresses native action for every type it scores itself, so it has no effect
on this module's own `ban_player` call in `cf_anticheat_enforce`.

`cf_cache_anticheat_config` also sets `$g_ac_config_cached = 1` as its last
step. Until it runs once (i.e. before the first `ti_before_mission_start` of
a fresh server process completes), `$g_ac_player_whitelist_admission_enabled`
reads as its uninitialized default of `0`, which would otherwise mean "no
whitelist required" during that startup window even though the documented
JSON default is `1` (required). The player-join admission check (section 4)
treats `$g_ac_config_cached == 0` as "require whitelist" to fail safe instead
of fail open during that window.

---

## 4. Player Join Admission (`module_scripts.py`)

The whitelist gate is implemented inside
`script_multiplayer_server_player_joined_common`. It runs only on the
dedicated server for non-server player slots. A denied player is logged,
notified, stripped of admin status if necessary, and kicked. A permitted
player has GUID history restored before the normal initial-information and
admin-protection scripts run.

```python
(try_begin),
  (multiplayer_is_server),
  (neq, ":player_no", 0),

  (assign, ":player_allowed", 1),
  (player_get_unique_id, ":player_guid", ":player_no"),
  (call_script, "script_cf_player_guid_is_seed_blacklisted", ":player_guid"),
  (assign, ":is_seed_blacklisted", reg0),
  (try_begin),
    (eq, ":is_seed_blacklisted", 1),
    (assign, ":player_allowed", 0),
  (else_try),
    (assign, ":admission_enabled", "$g_ac_player_whitelist_admission_enabled"),
    (try_begin),
      (eq, "$g_ac_config_cached", 0), # config not cached yet this boot; fail safe to whitelist-required
      (assign, ":admission_enabled", 1),
    (try_end),
    (try_begin),
      (eq, ":admission_enabled", 1),
      (call_script, "script_cf_player_guid_is_whitelisted", ":player_guid"),
      (assign, ":player_allowed", reg0),
    (try_end),
  (try_end),
  (try_begin),
    (eq, ":player_allowed", 0),
    (str_store_player_username, s2, ":player_no"),
    (assign, reg1, ":player_guid"),
    (try_begin),
      (eq, ":is_seed_blacklisted", 1),
      (str_store_string, s3, "str_ac_seed_blacklist_join_denied"),
      (str_store_string, s4, "@[AC-BLACKLIST] {s3}: {s2} (GUID: {reg1})"),
      (server_add_message_to_log, s4),
      (multiplayer_send_string_to_player,
       ":player_no", multiplayer_event_return_inter_admin_chat,
       "str_ac_seed_blacklist_join_denied_player"),
    (else_try),
      (str_store_string, s3, "str_ac_whitelist_join_denied"),
      (str_store_string, s4, "@[AC-WHITELIST] {s3}: {s2} (GUID: {reg1})"),
      (server_add_message_to_log, s4),
      (multiplayer_send_string_to_player,
       ":player_no", multiplayer_event_return_inter_admin_chat,
       "str_ac_whitelist_join_denied_player"),
    (try_end),
    (try_begin),
      (player_is_admin, ":player_no"),
      (player_set_is_admin, ":player_no", 0),
    (try_end),
    (kick_player, ":player_no"),
  (else_try),
    (call_script, "script_cf_restore_anticheat_player_history", ":player_no"),
    (call_script, "script_multiplayer_send_initial_information", ":player_no"),
    (call_script, "script_multiplayer_server_protect_admin_password", ":player_no"),
  (try_end),
(try_end),
```

The seed-mismatch blacklist check runs first and, if it matches, skips the
whitelist check entirely — a blacklisted GUID cannot be let back in by also
being on the whitelist. After the permitted branch, the same join script checks
`script_cf_json_admin_guid_contains`. A player who is not in
`anticheat_admin_guids.json` has native admin status removed and the removal
is written to the server log. The player whitelist therefore controls entry,
while the separate admin dictionary controls which GUIDs retain admin status.

---

## 5. Anti-Cheat Strings (`module_strings.py`)

The join-admission and alert scripts use these string records from the hardwired
prefix of `module_strings.py`:

```python
("ac_reason_seed_mismatch", "Seed mismatch exploit"),
("ac_reason_sustained_autoblock", "Sustained auto-block"),
("ac_reason_repeated_offscreen", "Repeated offscreen auto-block"),
("ac_reason_matchrate_watchlist", "Auto-block match-rate watchlist"),
("ac_reason_speedhack", "Client clock speedhack"),
("ac_reason_multisignal_autoblock", "Auto-block multi-signal suspicion"),
("ac_whitelist_join_denied", "Connection denied by player whitelist"),
("ac_whitelist_join_denied_player", "You are not on the player whitelist."),
("ac_seed_blacklist_join_denied", "Connection denied: permanently blacklisted for seed mismatch"),
("ac_seed_blacklist_join_denied_player", "You are permanently blocked from this server (seed validation failure)."),
```

The corresponding generated IDs in `ID_strings.py` are:

```python
str_ac_reason_seed_mismatch         = 4
str_ac_reason_sustained_autoblock   = 5
str_ac_reason_repeated_offscreen    = 6
str_ac_reason_matchrate_watchlist   = 7
str_ac_reason_speedhack             = 8
str_ac_reason_multisignal_autoblock = 9
str_ac_whitelist_join_denied        = 10
str_ac_whitelist_join_denied_player = 11
str_ac_seed_blacklist_join_denied        = 12
str_ac_seed_blacklist_join_denied_player = 13
```

---

## 6. Module System Evaluation & Enforcement Scripts (`module_scripts.py`)

The records below are a decision-logic reference. The actual source appends
the named scripts directly to `scripts = [...]`; it does not define an
`anticheat_scripts` list. The source also has a few implementation details
called out after this block.

```python
from header_operations import *
from header_common import *
from module_constants import *

anticheat_scripts = [

  # ============================================================================
  # Script cf_cache_anticheat_config
  # Called once per mission (ti_before_mission_start) after ensure_anticheat_config.
  # Caches every anticheat_config.json value into $g_ac_* globals so
  # on_cheat_detected/cf_eval_player_threat/cf_anticheat_enforce/
  # cf_restore_anticheat_player_history never touch disk per-event. A config
  # edit takes effect on the next mission start, not instantly.
  # ============================================================================
  ("cf_cache_anticheat_config",
   [
     (call_script, "script_ensure_anticheat_config"),
     (dict_create, ":config_dict"),
     (str_store_string, s0, "@anticheat_config"),
     (dict_load_file_json, ":config_dict", s0, 0),
     (str_store_string, s1, "@enforcement_mode"),
     (dict_get_int, "$g_ac_enforcement_mode", ":config_dict", s1, acm_silent),
     (str_store_string, s1, "@temp_ban_seconds"),
     (dict_get_int, "$g_ac_temp_ban_seconds", ":config_dict", s1, 3600),
     # ban_player has no duration arg; the native engine reads the temp-ban
     # length from this option instead (see cf_anticheat_enforce below).
     (server_set_anticheat_option, aco_auto_temp_ban_seconds, "$g_ac_temp_ban_seconds"),
     (str_store_string, s1, "@history_window_seconds"),
     (dict_get_int, "$g_ac_history_window_seconds", ":config_dict", s1, ac_conf_history_window_seconds),
     (str_store_string, s1, "@player_whitelist_admission_enabled"),
     (dict_get_int, "$g_ac_player_whitelist_admission_enabled", ":config_dict", s1, 1),
     (str_store_string, s1, "@max_offscreen_allowed"),
     (dict_get_int, "$g_ac_max_offscreen_allowed", ":config_dict", s1, ac_conf_max_offscreen_allowed),
     (str_store_string, s1, "@min_detections_watchlist"),
     (dict_get_int, "$g_ac_min_detections_watchlist", ":config_dict", s1, ac_conf_min_detections_watchlist),
     (str_store_string, s1, "@min_detections_suspected"),
     (dict_get_int, "$g_ac_min_detections_suspected", ":config_dict", s1, ac_conf_min_detections_suspected),
     (str_store_string, s1, "@max_matchrate_spikes"),
     (dict_get_int, "$g_ac_max_matchrate_spikes", ":config_dict", s1, ac_conf_max_matchrate_spikes),
     (str_store_string, s1, "@min_detections_confirmed"),
     (dict_get_int, "$g_ac_min_detections_confirmed", ":config_dict", s1, ac_conf_min_detections_confirmed),
     (str_store_string, s1, "@clock_skew_threshold_pct"),
     (dict_get_int, "$g_ac_clock_skew_threshold_pct", ":config_dict", s1, ac_conf_clock_skew_threshold_pct),
     (str_store_string, s1, "@min_clock_skew_detections"),
     (dict_get_int, "$g_ac_min_clock_skew_detections", ":config_dict", s1, ac_conf_min_clock_skew_detections),
     (str_store_string, s1, "@noise_max_match_pct"),
     (dict_get_int, "$g_ac_noise_max_match_pct", ":config_dict", s1, ac_conf_noise_max_match_pct),
     (str_store_string, s1, "@noise_min_reaction_ms"),
     (dict_get_int, "$g_ac_noise_min_reaction_ms", ":config_dict", s1, ac_conf_noise_min_reaction_ms),
     (str_store_string, s1, "@sustained_match_pct"),
     (dict_get_int, "$g_ac_sustained_match_pct", ":config_dict", s1, ac_conf_sustained_match_pct),
     (assign, "$g_ac_config_cached", 1), # lets the join gate fail safe before this has run once
   ]),

  # ============================================================================
  # Script: script_cf_player_guid_is_seed_blacklisted / script_cf_add_seed_mismatch_blacklist
  # Seed mismatch is deterministic, so an offender is blacklisted by GUID forever,
  # independent of any ban_player duration or admin unban. Keyed by GUID
  # (blacklist_{guid}), not a numbered index, so no counter bookkeeping is needed.
  # ============================================================================
  ("cf_player_guid_is_seed_blacklisted",
   [
     (store_script_param, ":guid", 1),
     (call_script, "script_ensure_seed_mismatch_blacklist_file"),
     (dict_create, ":blacklist_dict"),
     (str_store_string, s0, "@anticheat_seed_mismatch_blacklist"),
     (dict_load_file_json, ":blacklist_dict", s0, 0),
     (assign, reg1, ":guid"),
     (str_store_string, s1, "@blacklist_{reg1}"),
     (dict_get_int, ":is_blacklisted", ":blacklist_dict", s1, 0),
     (assign, reg0, ":is_blacklisted"),
   ]),

  ("cf_add_seed_mismatch_blacklist",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_ensure_seed_mismatch_blacklist_file"),
     (dict_create, ":blacklist_dict"),
     (str_store_string, s0, "@anticheat_seed_mismatch_blacklist"),
     (dict_load_file_json, ":blacklist_dict", s0, 0),
     (player_get_unique_id, ":guid", ":player_no"),
     (assign, reg1, ":guid"),
     (str_store_string, s1, "@blacklist_{reg1}"),
     (dict_get_int, ":already_blacklisted", ":blacklist_dict", s1, 0),
     (try_begin),
       (eq, ":already_blacklisted", 0),
       (dict_set_int, ":blacklist_dict", s1, 1),
       (str_store_player_username, s2, ":player_no"),
       (str_store_string, s1, "@blacklist_name_{reg1}"),
       (dict_set_str, ":blacklist_dict", s1, s2),
       (get_time, ":current_time"),
       (str_store_string, s1, "@blacklist_time_{reg1}"),
       (dict_set_int, ":blacklist_dict", s1, ":current_time"),
       (dict_save_json, ":blacklist_dict", s0),
       (str_store_string, s3, "@[AC-BLACKLIST] Permanently blacklisted GUID {reg1} ({s2}) after seed mismatch"),
       (server_add_message_to_log, s3),
     (try_end),
   ]),

  # ============================================================================
  # Script: script_cf_json_admin_guid_contains
  # Returns 1 in reg0 when the player GUID exists in the admin JSON dictionary.
  # Returns the matching admin name in s7.
  # ============================================================================
  ("cf_json_admin_guid_contains",
   [
     (store_script_param, ":guid", 1),
     (call_script, "script_ensure_admin_guid_file"),
     (dict_create, ":admin_dict"),
     (str_store_string, s0, "@anticheat_admin_guids"),
     (dict_load_file_json, ":admin_dict", s0, 0),

     # Admin records use separate keys: admin_guid_N and admin_name_N.
     (assign, reg0, 0),
     (str_store_string, s7, "@Unknown"),
     (try_for_dict_keys, s10, ":admin_dict"),
       (str_starts_with, s10, "@admin_guid_"),
       (dict_get_int, ":admin_guid", ":admin_dict", s10, -1),
       (str_store_string, s9, "@admin_name_"),
       (str_store_replace, s8, s10, "@admin_guid_", s9),
       (try_begin),
         (eq, ":guid", ":admin_guid"),
         (dict_get_str, s7, ":admin_dict", s8),
         (str_store_trim, s7, s7),
         (assign, reg0, 1),
         (break_loop),
       (try_end),
     (try_end),
   ]),

  # ============================================================================
  # Script: script_on_cheat_detected
  # Receives all ti_on_cheat_detected parameters from the trigger.
  # ============================================================================
  ("on_cheat_detected",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":type", 2),
     (store_script_param, ":value", 3),
     (store_script_param, ":threshold", 4),
     (assign, reg0, 0), # unhandled types fall through to native WSE2 action
     (try_begin),
       (player_is_active, ":player_no"),
       (try_begin),
         (this_or_next|eq, ":type", acd_seed_mismatch),
         (this_or_next|eq, ":type", acd_auto_block),
         (eq, ":type", acd_time_skew),
         # total_detections only counts scored types, so it never drifts from what history saves
         (player_get_slot, ":detections", ":player_no", slot_player_cheat_total_detections),
         (val_add, ":detections", 1),
         (player_set_slot, ":player_no", slot_player_cheat_total_detections, ":detections"),
       (try_end),

       # -----------------------------------------------------------------------
       # CASE 1: Seed Mismatch (Deterministic)
       # -----------------------------------------------------------------------
       (try_begin),
         (eq, ":type", acd_seed_mismatch),
         (assign, reg0, 1),
         (player_get_slot, ":seed_mismatches", ":player_no", slot_player_cheat_seed_mismatches),
         (val_add, ":seed_mismatches", 1),
         (player_set_slot, ":player_no", slot_player_cheat_seed_mismatches, ":seed_mismatches"),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_seed_mismatch),
         (call_script, "script_cf_add_seed_mismatch_blacklist", ":player_no"),
         (call_script, "script_cf_save_anticheat_player_history", ":player_no"),

       # -----------------------------------------------------------------------
       # CASE 2: Auto-Block Detection Sub-Signals
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":type", acd_auto_block),
         (assign, reg0, 1), # module owns every acd_auto_block event, even sub-threshold ones
         (ge, ":value", ":threshold"),
         (player_get_slot, ":autoblock_detections", ":player_no", slot_player_cheat_autoblock_detections),
         (val_add, ":autoblock_detections", 1),
         (player_set_slot, ":player_no", slot_player_cheat_autoblock_detections, ":autoblock_detections"),
         (try_begin),
           # Threshold 6 identifies the offscreen signal, including values such as 7/6 and 12/6.
           (eq, ":threshold", 6),
           (player_get_slot, ":count", ":player_no", slot_player_cheat_offscreen_count),
           (val_add, ":count", 1),
           (player_set_slot, ":player_no", slot_player_cheat_offscreen_count, ":count"),
         (else_try),
           # Threshold 8 identifies the feint-follow signal.
           (eq, ":threshold", 8),
           (player_get_slot, ":count", ":player_no", slot_player_cheat_feint_follows),
           (val_add, ":count", 1),
           (player_set_slot, ":player_no", slot_player_cheat_feint_follows, ":count"),
         (else_try),
           # Threshold 90 identifies the rolling match-rate signal.
           (eq, ":threshold", 90),
           (player_get_slot, ":count", ":player_no", slot_player_cheat_matchrate_spikes),
           (val_add, ":count", 1),
           (player_set_slot, ":player_no", slot_player_cheat_matchrate_spikes, ":count"),
         (try_end),
         (call_script, "script_cf_eval_player_threat", ":player_no", acd_auto_block),
         (call_script, "script_cf_save_anticheat_player_history", ":player_no"),

       # -----------------------------------------------------------------------
       # CASE 3: Client Clock Skew / Speedhack
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":type", acd_time_skew),
         (assign, reg0, 1), # module owns every acd_time_skew event, even sub-threshold ones
         (set_fixed_point_multiplier, 1), # acs_* stats must be read as raw ints, not scaled by another script's multiplier
         (player_get_anticheat_stat, ":max_skew", ":player_no", acs_time_skew_max),
         (assign, ":clock_skew_threshold", "$g_ac_clock_skew_threshold_pct"),
         (ge, ":max_skew", ":clock_skew_threshold"),
         (player_get_slot, ":count", ":player_no", slot_player_cheat_clock_skew_count),
         (val_add, ":count", 1),
         (player_set_slot, ":player_no", slot_player_cheat_clock_skew_count, ":count"),
         (call_script, "script_cf_eval_player_threat", ":player_no", acd_time_skew),
         (call_script, "script_cf_save_anticheat_player_history", ":player_no"),
       (try_end),
     (try_end),
   ]),

  # ============================================================================
  # Script: script_cf_eval_player_threat
  # Heuristic Scoring & False-Positive Filter Logic. All thresholds come from
  # the $g_ac_* globals cached by cf_cache_anticheat_config (no disk I/O here).
  # ============================================================================
  ("cf_eval_player_threat",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":detection_type", 2),
     (assign, ":min_detections", "$g_ac_min_detections_confirmed"),
     (assign, ":max_matchrate_spikes", "$g_ac_max_matchrate_spikes"),
     (assign, ":max_offscreen", "$g_ac_max_offscreen_allowed"),
     (assign, ":min_detections_watchlist", "$g_ac_min_detections_watchlist"),
     (assign, ":min_detections_suspected", "$g_ac_min_detections_suspected"),
     (assign, ":clock_skew_threshold", "$g_ac_clock_skew_threshold_pct"),
     (assign, ":min_clock_skew_detections", "$g_ac_min_clock_skew_detections"),
     (assign, ":noise_max_match", "$g_ac_noise_max_match_pct"),
     (assign, ":noise_min_reaction", "$g_ac_noise_min_reaction_ms"),
     (assign, ":sustained_match_pct", "$g_ac_sustained_match_pct"),

     # Fetch Accumulated Slot Counters, plus the player's current threat level
     # so no rule below can downgrade it (see EVALUATION RULEs 1, 5, 6, 7).
     (player_get_slot, ":autoblock_detections", ":player_no", slot_player_cheat_autoblock_detections),
     (player_get_slot, ":offscreen", ":player_no", slot_player_cheat_offscreen_count),
     (player_get_slot, ":spikes", ":player_no", slot_player_cheat_matchrate_spikes),
     (player_get_slot, ":feints", ":player_no", slot_player_cheat_feint_follows),
     (player_get_slot, ":skew_count", ":player_no", slot_player_cheat_clock_skew_count),
     (player_get_slot, ":current_threat", ":player_no", slot_player_cheat_threat_level),

     # Fetch Live Summary Stats
     (set_fixed_point_multiplier, 1), # acs_* stats must be read as raw ints, not scaled by another script's multiplier
     (player_get_anticheat_stat, ":match_pct", ":player_no", acs_autoblock_match),
     (player_get_anticheat_stat, ":reaction_ms", ":player_no", acs_autoblock_reaction_ms),
     (player_get_anticheat_stat, ":max_skew", ":player_no", acs_time_skew_max),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 1: Noise Filter
       # -----------------------------------------------------------------------
      (try_begin),
        (eq, ":detection_type", acd_auto_block),
        (lt, ":match_pct", ":noise_max_match"),
         (gt, ":reaction_ms", ":noise_min_reaction"),
         (gt, threat_level_noise, ":current_threat"), # threat level never downgrades
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_noise),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 2: High detection count + high live match rate = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":detection_type", acd_auto_block),
         (ge, ":autoblock_detections", ":min_detections"),
         (ge, ":match_pct", ":sustained_match_pct"),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_sustained_autoblock),

       # -----------------------------------------------------------------------
        # EVALUATION RULE 3: Repeated offscreen + a separate corroborating signal = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":detection_type", acd_auto_block),
         (ge, ":autoblock_detections", ":min_detections"),
         (ge, ":offscreen", ":max_offscreen"),
         (this_or_next|gt, ":spikes", 0),
         (gt, ":feints", 0),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_sustained_autoblock),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 4: Speedhack (Clock Skew) Positive Skew = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":detection_type", acd_time_skew),
         (gt, ":skew_count", 0),
         (ge, ":skew_count", ":min_clock_skew_detections"),
         (ge, ":max_skew", ":clock_skew_threshold"),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_speedhack),

       # -----------------------------------------------------------------------
       # EVALUATION RULE 5: Repeated Offscreen Crossings = SUSPECTED
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":detection_type", acd_auto_block),
         (ge, ":autoblock_detections", ":min_detections_suspected"),
         (ge, ":offscreen", ":max_offscreen"),
         (gt, threat_level_suspected, ":current_threat"), # threat level never downgrades
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_suspected),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_repeated_offscreen),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 6: Multi-Subsignal Crossings = SUSPECTED
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":detection_type", acd_auto_block),
         (ge, ":autoblock_detections", ":min_detections_suspected"),
         (gt, ":offscreen", 0),
         (gt, ":spikes", 0),
         (gt, ":feints", 0),
         (gt, threat_level_suspected, ":current_threat"), # threat level never downgrades
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_suspected),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_multisignal_autoblock),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 7: Configured Match-Rate Spike Threshold = WATCHLIST
       # -----------------------------------------------------------------------
       (else_try),
        (eq, ":detection_type", acd_auto_block),
        (ge, ":autoblock_detections", ":min_detections_watchlist"),
        (ge, ":spikes", ":max_matchrate_spikes"),
         (gt, threat_level_watchlist, ":current_threat"), # threat level never downgrades
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_watchlist),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_matchrate_watchlist),

     (try_end),
   ]),

  # ============================================================================
  # Script: script_cf_notify_admins
  # Logs alert strings and displays the same message.
  # ============================================================================
  ("cf_notify_admins",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":reason_code", 2),
     (player_get_unique_id, ":guid", ":player_no"),
     (str_store_player_username, s12, ":player_no"),
     (assign, reg1, ":guid"),
     (player_get_slot, ":threat", ":player_no", slot_player_cheat_threat_level),
     (assign, reg2, ":threat"),
     (str_store_string, s13, "str_no_string"), # default for an unmapped reason code
     (try_begin),
       (eq, ":reason_code", ac_reason_seed_mismatch),
       (str_store_string, s13, "str_ac_reason_seed_mismatch"),
     (else_try),
       (eq, ":reason_code", ac_reason_sustained_autoblock),
       (str_store_string, s13, "str_ac_reason_sustained_autoblock"),
     (else_try),
       (eq, ":reason_code", ac_reason_repeated_offscreen),
       (str_store_string, s13, "str_ac_reason_repeated_offscreen"),
     (else_try),
       (eq, ":reason_code", ac_reason_speedhack),
       (str_store_string, s13, "str_ac_reason_speedhack"),
     (else_try),
       (eq, ":reason_code", ac_reason_multisignal_autoblock),
       (str_store_string, s13, "str_ac_reason_multisignal_autoblock"),
     (else_try),
       (eq, ":reason_code", ac_reason_matchrate_watchlist),
       (str_store_string, s13, "str_ac_reason_matchrate_watchlist"),
     (try_end),
     (str_store_string, s3, "@[AC-ALERT] Suspect: {s12} (GUID: {reg1}) | Threat: {reg2} | Reason: {s13}"),
     (server_add_message_to_log, s3),
     (display_message, s3),
   ]),

  # ============================================================================
  # Script: script_cf_is_designated_admin_guid
  # Check if player unique ID matches whitelisted referee / admin GUIDs
  # ============================================================================
  ("cf_is_designated_admin_guid",
   [
     (store_script_param, ":player_no", 1),
     (player_get_unique_id, ":guid", ":player_no"),

     (assign, ":is_admin", 0),
     (call_script, "script_cf_json_admin_guid_contains", ":guid"),
     (assign, ":is_admin", reg0),
     
     (assign, reg0, ":is_admin"),
   ]),

  # ============================================================================
  # Script: reconnect-resistant, GUID-keyed detection history.
  # Called after a player passes admission; only restores same-mission history
  # that was written within history_window_seconds. Uses get_time (UNIX time),
  # not store_mission_timer_a, so the reconnect window survives a map change.
  # ============================================================================
  ("cf_restore_anticheat_player_history",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_ensure_anticheat_player_history"),
     (dict_create, ":history_dict"),
     (str_store_string, s0, "@anticheat_player_history"),
     (dict_load_file_json, ":history_dict", s0, 0),
     (assign, ":history_window", "$g_ac_history_window_seconds"),
     (player_get_unique_id, ":guid", ":player_no"),
     (assign, reg1, ":guid"),
     (str_store_string, s1, "@history_last_{reg1}"),
     (dict_get_int, ":last_time", ":history_dict", s1, -1),
     (get_time, ":current_time"), # UNIX time; unlike store_mission_timer_a this does not reset on map change
     (store_sub, ":elapsed", ":current_time", ":last_time"),
     (try_begin),
       (ge, ":last_time", 0),
       (ge, ":elapsed", 0),
       (le, ":elapsed", ":history_window"),
       (str_store_string, s1, "@history_total_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_total_detections, ":value"),
       (str_store_string, s1, "@history_autoblock_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_autoblock_detections, ":value"),
       (str_store_string, s1, "@history_offscreen_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_offscreen_count, ":value"),
       (str_store_string, s1, "@history_spikes_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_matchrate_spikes, ":value"),
       (str_store_string, s1, "@history_feints_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_feint_follows, ":value"),
       (str_store_string, s1, "@history_skew_{reg1}"),
       (dict_get_int, ":value", ":history_dict", s1, 0),
       (player_set_slot, ":player_no", slot_player_cheat_clock_skew_count, ":value"),
     (try_end),
   ]),

  ("cf_save_anticheat_player_history",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_ensure_anticheat_player_history"),
     (dict_create, ":history_dict"),
     (str_store_string, s0, "@anticheat_player_history"),
     (dict_load_file_json, ":history_dict", s0, 0),
     (player_get_unique_id, ":guid", ":player_no"),
     (assign, reg1, ":guid"),
     (get_time, ":current_time"), # UNIX time; unlike store_mission_timer_a this does not reset on map change
     (str_store_string, s1, "@history_last_{reg1}"),
     (dict_set_int, ":history_dict", s1, ":current_time"),
     (str_store_string, s1, "@history_total_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_total_detections),
     (dict_set_int, ":history_dict", s1, ":value"),
     (str_store_string, s1, "@history_autoblock_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_autoblock_detections),
     (dict_set_int, ":history_dict", s1, ":value"),
     (str_store_string, s1, "@history_offscreen_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_offscreen_count),
     (dict_set_int, ":history_dict", s1, ":value"),
     (str_store_string, s1, "@history_spikes_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_matchrate_spikes),
     (dict_set_int, ":history_dict", s1, ":value"),
     (str_store_string, s1, "@history_feints_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_feint_follows),
     (dict_set_int, ":history_dict", s1, ":value"),
     (str_store_string, s1, "@history_skew_{reg1}"),
     (player_get_slot, ":value", ":player_no", slot_player_cheat_clock_skew_count),
     (dict_set_int, ":history_dict", s1, ":value"),
     (dict_save_json, ":history_dict", s0),
   ]),

  # ============================================================================
  # Script: script_cf_player_guid_is_whitelisted
  # Returns 1 in reg0 when the shared whitelist dictionary contains the GUID.
  # ============================================================================
  ("cf_player_guid_is_whitelisted",
   [
     (store_script_param, ":guid", 1),
     (dict_create, ":whitelist_dict"),
     (str_store_string, s0, "@anticheat_player_whitelist"),
     (dict_load_file_json, ":whitelist_dict", s0, 0),
     (assign, reg0, 0),
     (try_for_dict_keys, s10, ":whitelist_dict"),
       (str_starts_with, s10, "@player_guid_"),
       (dict_get_int, ":whitelist_guid", ":whitelist_dict", s10, -1),
       (eq, ":guid", ":whitelist_guid"),
       (assign, reg0, 1),
       (break_loop),
     (try_end),
   ]),

  # ============================================================================
  # Script: script_cf_anticheat_enforce
  # Writes the alert, then bans confirmed players in enforce mode.
  # ============================================================================
  ("cf_anticheat_enforce",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":reason_code", 2),
     (call_script, "script_cf_notify_admins", ":player_no", ":reason_code"),
     (assign, ":mode", "$g_ac_enforcement_mode"),
     (try_begin),
       (eq, ":mode", acm_enforce),
       # ban_player's 3rd arg is the reporting admin's player_no (0 = server), not a duration;
       # temp-ban length comes from the native aco_auto_temp_ban_seconds option (see cf_cache_anticheat_config).
       (ban_player, ":player_no", 1, 0),
     (try_end),
   ]),
]
```

---

## 7. Current Source Behavior

1. **Mission start**: `multiplayer_server_ensure_anticheat_json` creates the
  admin GUID, player whitelist, configuration, and history files when absent
  or empty, then `script_cf_cache_anticheat_config` loads `anticheat_config.json`
  once and caches every value into `$g_ac_*` globals (including pushing
  `temp_ban_seconds` into the native `aco_auto_temp_ban_seconds` server option),
  finishing by setting the `$g_ac_config_cached` sentinel to `1`.
2. **Join and restore**: `script_multiplayer_server_player_joined_common` first
  denies any GUID present in `anticheat_seed_mismatch_blacklist.json`
  unconditionally (this check cannot be overridden by the whitelist), then
  enforces `$g_ac_player_whitelist_admission_enabled` (the cached config
  value, not a per-join disk read) unless `$g_ac_config_cached` is still `0`
  (fresh server boot, first mission not yet cached), in which case it fails
  safe and requires the whitelist regardless of the JSON default. A permitted
  player restores recent GUID history before normal join initialization
  proceeds. The same script also resets every `slot_player_cheat_*` counter to
  zero for the joining player slot (in `script_multiplayer_init_player_slots`,
  which runs before the history restore), so a reused slot number from a
  previous disconnect cannot leak one player's threat level/detection counts
  onto a new player.
3. **Detection**: `multiplayer_server_anticheat` forwards all four engine
  parameters to `script_on_cheat_detected` and sets `reg0` to `1` to suppress
  native WSE2 action.
4. **Sub-signals**: Auto-block only counts an event when `value >= threshold`.
  Thresholds `6`, `8`, and `90` increment offscreen, feint, and match-rate
  counters respectively. `slot_player_cheat_total_detections` only increments
  for the three scored types, while `slot_player_cheat_autoblock_detections`
  is used for autoblock scoring so seed/skew events cannot contaminate
  autoblock thresholds. Time skew counts only when the configured
  `clock_skew_threshold_pct` is reached.
5. **Evaluation**: The first matching branch in
  `script_cf_eval_player_threat` wins, gated by `:detection_type` so an
  unrelated event cannot trigger another signal's branch: noise (autoblock
  only), then confirmed match-rate/corroborated offscreen (autoblock) or
  sustained skew (time skew), then suspected offscreen/multi-signal
  (autoblock), and finally watchlist spike (autoblock). Every branch except
  the three CONFIRMED ones (already the maximum level) first checks the
  player's current threat level and refuses to apply a lower one, so threat
  level can only ever go up during a session.
6. **Persistence**: `script_cf_save_anticheat_player_history` writes total,
  autoblock, offscreen, spike, feint, skew, and current-time values after every
  scored event, using `get_time` (UNIX time) rather than the mission timer, so
  the reconnect window is not reset by a map change. Restore rejects history
  with a negative elapsed time or one older than `history_window_seconds`.
7. **Alert and enforcement**: `script_cf_notify_admins` writes the formatted
  alert to the server log and calls `display_message`. Enforcement calls
  `ban_player` only when the cached `$g_ac_enforcement_mode == acm_enforce`
  (`2`); the temp-ban duration comes from the native `aco_auto_temp_ban_seconds`
  option set at mission start, not from `ban_player`'s arguments.

### Resolved Behavior and Validation Gaps

- Seed mismatches now increment `slot_player_cheat_seed_mismatches` before
  immediate enforcement.
- The detection handler reads `clock_skew_threshold_pct` from the cached
  config global, matching the evaluator.
- `max_matchrate_spikes` is read from config and is the minimum number of
  match-rate spikes required for the watchlist branch.
- `max_offscreen_allowed`, `min_detections_confirmed`, `min_detections_suspected`,
  and `min_detections_watchlist` are inclusive "at least N" gates (`ge`); reaching
  the configured value triggers the branch, it is not a ceiling that only trips
  one event past it.
- Rule 2 (sustained autoblock) reads its match-rate requirement from the
  configurable `sustained_match_pct` (default `85`) instead of a hardcoded value.
- `cf_notify_admins` defaults its alert string to `str_no_string` before the
  reason-code chain and matches `ac_reason_matchrate_watchlist` explicitly, so
  an unmapped reason code no longer gets silently mislabeled as a watchlist alert.
- Noise classification is evaluated before confirmed/suspected autoblock
  rules, so low-match/slow-reaction sessions cannot bypass the noise filter.
- The join path initializes `:player_guid` before the admission switch, so
  disabling admission does not invalidate the later admin-GUID check.
- A non-empty whitelist is preserved; `ensure_player_whitelist_file` nests its
  `dict_is_empty` recreate-default check inside the `dict_load_file_json`
  success branch (matching `ensure_admin_guid_file`'s pattern), so a populated
  file is no longer silently overwritten with the two default GUIDs on every
  mission start.
- `multiplayer_init_player_slots` now clears all 8 `slot_player_cheat_*`
  counters for the joining player slot, so a slot number reused after a
  disconnect no longer inherits the previous occupant's threat level or
  detection counts; `cf_restore_anticheat_player_history` (which runs after
  this reset, later in the same join flow) still overwrites these zeros with
  the correct values if the new player's own GUID has valid recent history.
- Admin GUID entries are used for admin authorization. They are not recipients
  of targeted anti-cheat notifications.
- Previously, the trigger suppressed native WSE2 action for every detection
  type unconditionally, so types `10` (aim snap), `12` (spread luck), `13`
  (attack cadence), `15` (auto attack), and `17` (aim lead) were silently
  absorbed with no scoring and no native fallback. This is fixed: the trigger
  now only suppresses native action for the types the module scores (`14`,
  `11`, `16`); unhandled types leave `reg0` at `0` so the native WSE2 kick/ban
  pipeline still runs for them. The module still does not add its own
  sub-signal scoring for those five types.
- `enforcement_mode=2` has not been validated against a live ban in the
  available logs. Keep enforcement opt-in until a controlled test confirms the
  `ban_player` path and configured duration.
- `reg0` is now set to `1` as soon as the event's type matches
  `acd_auto_block`/`acd_time_skew`/`acd_seed_mismatch`, before the branch's own
  internal sub-threshold gate (`ge, ":value", ":threshold"` /
  `ge, ":max_skew", ":clock_skew_threshold"`) is evaluated. Previously `reg0`
  was only set after that gate passed, so an event of a type the module does
  handle, but that fails the module's own accumulation gate, fell through to
  native WSE2 action - bypassing the module's own `enforcement_mode` even in
  silent mode. Native fallback is now reserved strictly for the five
  completely unscored types (`10`, `12`, `13`, `15`, `17`). None of
  `cf_anticheat_enforce`, `cf_eval_player_threat`, or `cf_notify_admins`
  (all called from inside this same `try_begin` after `reg0` is set) ever
  assign to `reg0` themselves, so the suppression flag reliably survives
  until the trigger reads it back.
- `set_fixed_point_multiplier` is set to `1` immediately before every
  `player_get_anticheat_stat` read of `acs_autoblock_match`,
  `acs_autoblock_reaction_ms`, and `acs_time_skew_max`. The multiplier is
  global, mutable state shared with every other script in the module (several
  presentation and scene-prop scripts set it to `100` or `1000`), so a stat
  read without first pinning the multiplier would be comparing an unknown
  unit against the plain-integer thresholds (`65`, `500`, `10`, `85`) used
  throughout this module. `ANTICHEAT_SERVER_GUIDE.md`'s documented ranges
  (e.g. `autoblock_match_pct` 50-85 honest / 95-100 bot) confirm these three
  stats are plain percent/ms values, not fixed-point-scaled, but pinning the
  multiplier removes the dependency on that assumption entirely. There is no
  corresponding "restore previous multiplier" step afterward because this
  WSE2 build has no `get_fixed_point_multiplier` getter to read a prior value
  from (it exists only as a commented-out line in `header_operations.py`);
  leaving the multiplier at `1`, the documented engine default, is the safest
  achievable outcome.
- `script_cf_save_anticheat_player_history` (a full JSON load + save of the
  history file) only runs for the three types the module scores
  (`acd_seed_mismatch`, `acd_auto_block`, `acd_time_skew`), not on every
  `ti_on_cheat_detected` firing. The five unscored types don't touch any
  slot counter, so saving history for them was a pure I/O cost with nothing
  new to persist. Config values used during scoring and enforcement are read
  once per mission by `cf_cache_anticheat_config` rather than from disk on
  every event.
- `ban_player`'s 3rd argument is the reporting admin/referee `player_no` (`0`
  = server), not a ban duration - this matches every other `ban_player` call
  site in the codebase. `cf_anticheat_enforce` previously passed the
  configured `temp_ban_seconds` value there, which had no effect on ban
  length. The real duration for a `value=1` (temporary) ban comes from the
  native `aco_auto_temp_ban_seconds` server option (`ANTICHEAT_SERVER_GUIDE.md`'s
  `iAutoTempBanSeconds` INI key), which `cf_cache_anticheat_config` now sets
  via `server_set_anticheat_option` once per mission.
- The native `set_anticheat_mode`/`iMode` console switch (`ANTICHEAT_SERVER_GUIDE.md`
  section 2) and this module's own `anticheat_config.json` → `enforcement_mode`
  key are two independent switches that share the same `1`/`2` (silent/enforce)
  values, which invites confusion. Changing the native mode at the console
  takes effect immediately, but has no effect on the module's own
  `cf_anticheat_enforce` → `ban_player` call, since the module suppresses
  native action for every type it scores itself. There is no console/chat
  command in this build to force `cf_cache_anticheat_config` to re-run
  mid-mission; a JSON `enforcement_mode` change only takes effect on the next
  map. This is documented behavior (see section 3), not a bug, but it is an
  easy operational mistake to run `set_anticheat_mode 2` and assume the
  module's own bans are now live.
- Fail-open window: before `cf_cache_anticheat_config` runs for the first time
  in a fresh server process, `$g_ac_player_whitelist_admission_enabled` reads
  as the engine's uninitialized default (`0`), which would otherwise mean "no
  whitelist required" even though the documented JSON default is `1`
  (required). Fixed: `cf_cache_anticheat_config` now sets a `$g_ac_config_cached`
  sentinel to `1` as its last step, and the join-admission check in
  `script_multiplayer_server_player_joined_common` treats
  `$g_ac_config_cached == 0` as "require the whitelist", failing safe instead
  of fail open during that window. The equivalent gap in
  `cf_restore_anticheat_player_history` (`$g_ac_history_window_seconds` reading
  `0` before the first cache) was not changed: it only makes history restore
  never match (`elapsed <= 0` is effectively unreachable), which fails safe
  already — a legitimate reconnect in that narrow window just doesn't get its
  history restored, it does not bypass anything.
- `multiplayer_server_ensure_anticheat_json` called `script_ensure_anticheat_config`
  directly and then immediately called `script_cf_cache_anticheat_config`,
  which calls `script_ensure_anticheat_config` itself as its first step. Fixed
  by removing the redundant standalone call; `cf_cache_anticheat_config` still
  guarantees the config file exists before it reads it.
- Seed mismatch previously relied only on `ban_player`/`aco_auto_temp_ban_seconds`
  for enforcement, both of which are time-limited and both of which do
  nothing at all in silent mode. Since seed mismatch is deterministic (an
  honest client can never trigger it), `on_cheat_detected` now also calls
  `cf_add_seed_mismatch_blacklist`, which writes the GUID to
  `anticheat_seed_mismatch_blacklist.json` unconditionally — regardless of
  `enforcement_mode` and with no expiry. The join gate in
  `script_multiplayer_server_player_joined_common` checks this file before the
  player whitelist and denies admission outright on a match, so the entry
  survives a temp-ban expiring, `enforcement_mode` being silent, or the GUID
  also being present in `anticheat_player_whitelist.json`.

