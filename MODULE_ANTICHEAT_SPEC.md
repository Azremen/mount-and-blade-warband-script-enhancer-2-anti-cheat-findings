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
   - **Action**: Immediate automated ban or kick + high-priority server/admin alert.

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
       - `min_detections_watchlist=6`: a single match-rate crossing does not create a watchlist alert.
  - **Client Clock Skew / Speedhack (`type == 11`)**:
   - *Positive Skew (`time_skew_max_pct >= 10%` in at least 2 detections)*: Client running fast. One isolated positive sample is not enough for automatic confirmation; repeated positive skew is required.
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
slot_player_cheat_last_detection_time = 157

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

ac_reason_seed_mismatch           = 1
ac_reason_sustained_autoblock     = 2
ac_reason_repeated_offscreen      = 3
ac_reason_matchrate_watchlist     = 4
ac_reason_speedhack               = 5
ac_reason_multisignal_autoblock   = 6
```

### JSON Configuration Files

Keep the four JSON files in the server module directory. They intentionally use
separate dictionaries: `anticheat_config.json` contains thresholds and
enforcement settings, `anticheat_admin_guids.json` contains only admin GUID
flags, `anticheat_player_whitelist.json` contains normal-player GUID flags, and
`anticheat_player_history.json` contains short-lived GUID-based detection history.

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
  "noise_min_reaction_ms": 500
}
```

`anticheat_player_history.json` is a module-managed, GUID-keyed runtime history file. On every
anti-cheat event it stores the accumulated detection counters and the current mission time. When a
player reconnects within `history_window_seconds` (default `1800`), the counters are restored before
the next detection is evaluated. A map change resets the mission timer, so old history is not carried
into a new match. This prevents reconnects from resetting a current-match detection pattern without
making historical detections permanent.

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
    (call_script, "script_on_cheat_detected",
     ":player_no", ":detection_type", ":value", ":threshold"),
    (assign, reg0, 1),
  ])

multiplayer_server_ensure_anticheat_json = (
  ti_before_mission_start, 0, ti_once, [],
  [
    (call_script, "script_ensure_admin_guid_file"),
    (call_script, "script_ensure_player_whitelist_file"),
    (call_script, "script_ensure_anticheat_config"),
    (call_script, "script_ensure_anticheat_player_history"),
  ])
```

Both triggers are entries in `mm_multiplayer_common`, so every mission
template using that shared list receives the initialization and detection
handler. `module_triggers.py` does not host this feature.

---

## 4. Module System Evaluation & Enforcement Scripts (`module_scripts.py`)

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
  # Script 0: script_cf_json_admin_guid_contains
  # Returns 1 in reg0 when the player GUID exists in the admin JSON dictionary.
  # Returns the matching admin name in s7.
  # ============================================================================
  ("cf_json_admin_guid_contains",
   [
     (store_script_param, ":guid", 1),
     (call_script, "script_ensure_admin_guid_file"),
     (dict_create, ":admin_guids_dict"),
     (str_store_string, s0, "@anticheat_admin_guids"),
     (dict_load_file_json, ":admin_guids_dict", s0, 0),

     # Iterate admin_guid_N keys; the corresponding admin_name_N is used for log context.
     (assign, reg0, 0),
     (str_store_string, s7, "@Unknown"),
     (try_for_dict_keys, s10, ":admin_guids_dict"),
       (str_starts_with, s10, "@admin_guid_"),
       (dict_get_int, ":admin_guid", ":admin_guids_dict", s10, -1),
       (str_store_string, s9, "@admin_name_"),
       (str_store_replace, s8, s10, "@admin_guid_", s9),
       (try_begin),
         (eq, ":guid", ":admin_guid"),
         (dict_get_str, s7, ":admin_guids_dict", s8),
         (str_store_trim, s7, s7),
         (assign, reg0, 1),
         (break_loop),
       (try_end),
     (try_end),
   ]),

  # ============================================================================
  # Script 1: script_on_cheat_detected
  # Receives all ti_on_cheat_detected parameters from the trigger.
  # ============================================================================
  ("on_cheat_detected",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":type", 2),
     (store_script_param, ":value", 3),
     (store_script_param, ":threshold", 4),

     (try_begin),
       (player_is_active, ":player_no"),

       (player_get_slot, ":total_dets", ":player_no", slot_player_cheat_total_detections),
       (val_add, ":total_dets", 1),
       (player_set_slot, ":player_no", slot_player_cheat_total_detections, ":total_dets"),

       # -----------------------------------------------------------------------
       # CASE 1: Seed Mismatch (Deterministic)
       # -----------------------------------------------------------------------
       (try_begin),
         (eq, ":type", acd_seed_mismatch),
         
         (player_get_slot, ":seed_fails", ":player_no", slot_player_cheat_seed_mismatches),
         (val_add, ":seed_fails", 1),
         (player_set_slot, ":player_no", slot_player_cheat_seed_mismatches, ":seed_fails"),
         
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_seed_mismatch),

       # -----------------------------------------------------------------------
       # CASE 2: Auto-Block Detection Sub-Signals
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":type", acd_auto_block),
         
         (try_begin),
           # Threshold 6 identifies the offscreen signal, including values such as 7/6 and 12/6.
           (eq, ":threshold", 6),
           (player_get_slot, ":offscreen_cnt", ":player_no", slot_player_cheat_offscreen_count),
           (val_add, ":offscreen_cnt", 1),
           (player_set_slot, ":player_no", slot_player_cheat_offscreen_count, ":offscreen_cnt"),
         (else_try),
           # Threshold 8 identifies the feint-follow signal.
           (eq, ":threshold", 8),
           (player_get_slot, ":feint_cnt", ":player_no", slot_player_cheat_feint_follows),
           (val_add, ":feint_cnt", 1),
           (player_set_slot, ":player_no", slot_player_cheat_feint_follows, ":feint_cnt"),
         (else_try),
           # Threshold 90 identifies the rolling match-rate signal.
           (eq, ":threshold", 90),
           (player_get_slot, ":spike_cnt", ":player_no", slot_player_cheat_matchrate_spikes),
           (val_add, ":spike_cnt", 1),
           (player_set_slot, ":player_no", slot_player_cheat_matchrate_spikes, ":spike_cnt"),
         (try_end),

         # Evaluate threat after sub-signal update
         (call_script, "script_cf_eval_player_threat", ":player_no"),

       # -----------------------------------------------------------------------
       # CASE 3: Client Clock Skew / Speedhack
       # -----------------------------------------------------------------------
       (else_try),
         (eq, ":type", acd_time_skew),
         
         (player_get_anticheat_stat, ":max_skew", ":player_no", acs_time_skew_max),
         (ge, ":max_skew", ac_conf_clock_skew_threshold_pct),
         (player_get_slot, ":skew_cnt", ":player_no", slot_player_cheat_clock_skew_count),
         (val_add, ":skew_cnt", 1),
         (player_set_slot, ":player_no", slot_player_cheat_clock_skew_count, ":skew_cnt"),
         (call_script, "script_cf_eval_player_threat", ":player_no"),

       (try_end),
       # Persist counters after every event so reconnects do not reset this match's evidence.
       (call_script, "script_cf_save_anticheat_player_history", ":player_no"),
     (try_end),
   ]),

  # ============================================================================
  # Script 2: script_cf_eval_player_threat
  # Heuristic Scoring & False-Positive Filter Logic
  # ============================================================================
  ("cf_eval_player_threat",
   [
     (store_script_param, ":player_no", 1),

     (call_script, "script_ensure_anticheat_config"),
     (dict_create, ":config_dict"),
     (str_store_string, s0, "@anticheat_config"),
     (dict_load_file_json, ":config_dict", s0, 0),
     
     (try_begin),
       (player_is_active, ":player_no"),
       
       # Fetch Live Summary Stats
      (player_get_anticheat_stat, ":match_pct", ":player_no", acs_autoblock_match),
      (player_get_anticheat_stat, ":reaction_ms", ":player_no", acs_autoblock_reaction_ms),
      (player_get_anticheat_stat, ":max_skew", ":player_no", acs_time_skew_max),
       
       # Fetch Accumulated Slot Counters
       (player_get_slot, ":total_dets", ":player_no", slot_player_cheat_total_detections),
       (player_get_slot, ":offscreen_cnt", ":player_no", slot_player_cheat_offscreen_count),
       (player_get_slot, ":spikes_cnt", ":player_no", slot_player_cheat_matchrate_spikes),
       (player_get_slot, ":feint_cnt", ":player_no", slot_player_cheat_feint_follows),
       (player_get_slot, ":skew_cnt", ":player_no", slot_player_cheat_clock_skew_count),

       # Read evaluation thresholds from anticheat_config.json.
       (str_store_string, s0, "@max_offscreen_allowed"),
       (dict_get_int, ":max_offscreen_allowed", ":config_dict", s0, ac_conf_max_offscreen_allowed),
       (str_store_string, s0, "@min_detections_watchlist"),
       (dict_get_int, ":min_detections_watchlist", ":config_dict", s0, ac_conf_min_detections_watchlist),
       (str_store_string, s0, "@min_detections_suspected"),
       (dict_get_int, ":min_detections_suspected", ":config_dict", s0, ac_conf_min_detections_suspected),
       (str_store_string, s0, "@min_detections_confirmed"),
       (dict_get_int, ":min_detections_confirmed", ":config_dict", s0, ac_conf_min_detections_confirmed),
       (str_store_string, s0, "@clock_skew_threshold_pct"),
       (dict_get_int, ":clock_skew_threshold_pct", ":config_dict", s0, ac_conf_clock_skew_threshold_pct),
       (str_store_string, s0, "@min_clock_skew_detections"),
       (dict_get_int, ":min_clock_skew_detections", ":config_dict", s0, ac_conf_min_clock_skew_detections),
       (str_store_string, s0, "@noise_max_match_pct"),
       (dict_get_int, ":noise_max_match_pct", ":config_dict", s0, ac_conf_noise_max_match_pct),
       (str_store_string, s0, "@noise_min_reaction_ms"),
       (dict_get_int, ":noise_min_reaction_ms", ":config_dict", s0, ac_conf_noise_min_reaction_ms),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 1: High detection count + high live match rate = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":total_dets", ":min_detections_confirmed"),
         (ge, ":match_pct", 85),
         
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_sustained_autoblock),

       # -----------------------------------------------------------------------
        # EVALUATION RULE 2: Repeated offscreen + a separate corroborating signal = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":total_dets", ":min_detections_confirmed"),
         (ge, ":offscreen_cnt", ":max_offscreen_allowed"),
         (this_or_next|gt, ":spikes_cnt", 0),
         (gt, ":feint_cnt", 0),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_sustained_autoblock),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 3: Speedhack (Clock Skew) Positive Skew = CONFIRMED
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":skew_cnt", ":min_clock_skew_detections"),
         (ge, ":max_skew", ":clock_skew_threshold_pct"),
         
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_confirmed),
         (call_script, "script_cf_anticheat_enforce", ":player_no", ac_reason_speedhack),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 4: Noise Filter
       # -----------------------------------------------------------------------
       (else_try),
         (lt, ":match_pct", ":noise_max_match_pct"),
         (gt, ":reaction_ms", ":noise_min_reaction_ms"),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_noise),

       # -----------------------------------------------------------------------
       # EVALUATION RULE 5: Repeated Offscreen Crossings = SUSPECTED
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":total_dets", ":min_detections_suspected"),
         (ge, ":offscreen_cnt", ":max_offscreen_allowed"),
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_suspected),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_repeated_offscreen),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 6: Multi-Subsignal Crossings = SUSPECTED
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":total_dets", ":min_detections_suspected"),
         (gt, ":offscreen_cnt", 0),
         (gt, ":spikes_cnt", 0),
         (gt, ":feint_cnt", 0),
         
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_suspected),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_multisignal_autoblock),

       # -----------------------------------------------------------------------
      # EVALUATION RULE 7: Single Match-Rate Spike = WATCHLIST
       # -----------------------------------------------------------------------
       (else_try),
         (ge, ":total_dets", ":min_detections_watchlist"),
         (gt, ":spikes_cnt", 0),
         
         (player_set_slot, ":player_no", slot_player_cheat_threat_level, threat_level_watchlist),
         (call_script, "script_cf_notify_admins", ":player_no", ac_reason_matchrate_watchlist),

       (try_end),
     (try_end),
   ]),

  # ============================================================================
  # Script 3: script_cf_notify_admins
  # Logs alert strings and displays the same message.
  # ============================================================================
  ("cf_notify_admins",
   [
     (store_script_param, ":suspect_no", 1),
     (store_script_param, ":reason_code", 2),
     
     (player_get_unique_id, ":unique_id", ":suspect_no"),
     (str_store_player_username, s1, ":suspect_no"),
     (assign, reg1, ":unique_id"),
     
     (player_get_slot, ":threat_lvl", ":suspect_no", slot_player_cheat_threat_level),
     (assign, reg2, ":threat_lvl"),

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
       (str_store_string, s13, "str_ac_reason_matchrate_watchlist"),
     (try_end),
     (str_store_string, s3, "@[AC-ALERT] Suspect: {s1} (GUID: {reg1}) | Threat: {reg2} | Reason: {s13}"),

    # Current source also calls display_message after writing this log record.
     (server_add_message_to_log, s3),
   ]),

  # ============================================================================
  # Script 4: script_cf_is_designated_admin_guid
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
  # Script 5: reconnect-resistant, GUID-keyed detection history.
  # Called after a player passes admission; only restores same-mission history
  # that was written within history_window_seconds.
  # ============================================================================
  ("cf_restore_anticheat_player_history",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_ensure_anticheat_player_history"),
     (call_script, "script_ensure_anticheat_config"),
     (dict_create, ":history_dict"),
     (str_store_string, s0, "@anticheat_player_history"),
     (dict_load_file_json, ":history_dict", s0, 0),
     (player_get_unique_id, ":guid", ":player_no"),
     (assign, reg1, ":guid"),
     (str_store_string, s1, "@history_last_{reg1}"),
     (dict_get_int, ":last_time", ":history_dict", s1, -1),
     (store_mission_timer_a, ":current_time"),
     (store_sub, ":elapsed", ":current_time", ":last_time"),
     (try_begin),
       (ge, ":last_time", 0),
       (ge, ":elapsed", 0), # Reject data from an earlier map after timer reset.
       (le, ":elapsed", ":history_window"),
       # Load history_total/offscreen/spikes/feints/skew_{GUID} into player slots.
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
     (store_mission_timer_a, ":current_time"),
     (str_store_string, s1, "@history_last_{reg1}"),
     (dict_set_int, ":history_dict", s1, ":current_time"),
     # Save the total/offscreen/spikes/feints/skew player-slot counters under this GUID.
     (dict_save_json, ":history_dict", s0),
   ]),

  # ============================================================================
  # Script 6: script_cf_player_guid_is_whitelisted
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
  # Script 7: script_cf_anticheat_enforce
  # Writes the alert, then bans confirmed players in enforce mode.
  # ============================================================================
  ("cf_anticheat_enforce",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":reason_code", 2),

     (player_get_unique_id, ":unique_id", ":player_no"),
     (str_store_player_username, s1, ":player_no"),
     (assign, reg1, ":unique_id"),

     (call_script, "script_cf_notify_admins", ":player_no", ":reason_code"),

     (call_script, "script_ensure_anticheat_config"),
     (dict_create, ":config_dict"),
     (str_store_string, s0, "@anticheat_config"),
     (dict_load_file_json, ":config_dict", s0, 0),
     (str_store_string, s0, "@enforcement_mode"),
     (dict_get_int, ":ac_mode", ":config_dict", s0, acm_silent),
     (str_store_string, s0, "@temp_ban_seconds"),
     (dict_get_int, ":ban_seconds", ":config_dict", s0, 3600),
     
     (try_begin),
       (eq, ":ac_mode", 2), # Enforce Mode
       (ban_player, ":player_no", 1, ":ban_seconds"),
     (try_end),
   ]),
]
```

---

## 5. Current Source Behavior

1. **Mission start**: `multiplayer_server_ensure_anticheat_json` creates the
  admin GUID, player whitelist, configuration, and history files when absent
  or empty.
2. **Join and restore**: `script_multiplayer_server_player_joined_common`
  enforces `player_whitelist_admission_enabled`; a permitted player restores
  same-mission GUID history before normal join initialization proceeds.
3. **Detection**: `multiplayer_server_anticheat` forwards all four engine
  parameters to `script_on_cheat_detected` and sets `reg0` to `1` to suppress
  native WSE2 action.
4. **Sub-signals**: Auto-block only counts an event when `value >= threshold`.
  Thresholds `6`, `8`, and `90` increment offscreen, feint, and match-rate
  counters respectively. Time skew counts only when `acs_time_skew_max >= 10`.
5. **Evaluation**: The first matching branch in
  `script_cf_eval_player_threat` wins: confirmed match-rate/corroborated
  offscreen/sustained skew, then noise, suspected offscreen/multi-signal, and
  finally watchlist spike.
6. **Persistence**: `script_cf_save_anticheat_player_history` writes total,
  offscreen, spike, feint, skew, and mission-time values after every handled
  event. Restore rejects history with a negative elapsed mission time or one
  older than `history_window_seconds`.
7. **Alert and enforcement**: `script_cf_notify_admins` currently writes the
  formatted alert to the server log and calls `display_message`. Enforcement
  calls `ban_player` only when JSON `enforcement_mode == acm_enforce` (`2`).

### Source Differences from the Earlier Pseudo-Code

- `slot_player_cheat_seed_mismatches` is declared but the current
  `script_on_cheat_detected` does not increment it for a seed mismatch.
- The detection handler uses the compiled clock-skew default (`10`) while the
  evaluator reads `clock_skew_threshold_pct` from JSON.
- `max_matchrate_spikes` is written to the default config but is not read by
  the current threat-evaluation script.
- Admin GUID entries are used for admin authorization. They are not recipients
  of targeted anti-cheat notifications.
- The current whitelist ensure script recreates the default file after a
  successful non-empty load because its outer `else_try` is reached when
  `dict_is_empty` fails. This is current behavior, not the intended live-edit
  behavior described above.
