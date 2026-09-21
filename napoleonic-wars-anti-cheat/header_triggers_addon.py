# WSE2 trigger and anti-cheat additions.

# Anti-cheat engine trigger.
ti_on_cheat_detected = -114.0
# Trigger Param 1: player no
# Trigger Param 2: detection type (acd_*)
# Trigger Param 3: measured value (fixed point where the statistic is a float)
# Trigger Param 4: the threshold that was exceeded, in the same unit
# Trigger Result: if set to a nonzero value the engine takes no action at all - no kick, no ban -
#                 and the module is expected to handle the detection itself

# Detection types (ti_on_cheat_detected parameter 2).
acd_flood            = 1
acd_invalid_input    = 2
acd_address_mismatch = 3
acd_packet_no_jump   = 4
acd_aim_snap         = 10
acd_time_skew        = 11
acd_spread_luck      = 12
acd_attack_cadence   = 13
acd_auto_block       = 14
acd_auto_attack      = 15
acd_seed_mismatch    = 16
acd_aim_lead         = 17
acd_client_module    = 20
acd_client_thread    = 21
acd_client_hook      = 22
acd_client_signature = 23
acd_client_text_hash = 24
acd_module_report    = 100

# Anti-cheat statistics (player_get_anticheat_stat).
acs_detections               = 0
acs_seed_mismatches          = 1
acs_time_skew_ratio          = 2
acs_time_skew_windows        = 3
acs_max_aim_speed            = 4
acs_aim_snaps                = 5
acs_spread_mean              = 6
acs_spread_shots             = 7
acs_melee_attacks_in_window  = 8
acs_ranged_attacks_in_window = 9
acs_autoblock_samples        = 10
acs_autoblock_match          = 11
acs_autoblock_reaction_ms    = 12
acs_autoblock_feint_follows  = 13
acs_autoblock_offscreen      = 14
acs_autoattack_samples       = 15
acs_autoattack_open_rate     = 16
acs_autoattack_reaction_ms   = 17
acs_autoattack_feint_follows = 18
acs_autoattack_chambers      = 19
acs_autoattack_chamber_rate  = 20
acs_aimlead_hard_shots       = 21
acs_aimlead_err_deg          = 22
acs_aimlead_flat_ratio       = 23
acs_time_skew_max            = 24
acs_time_skew_stall          = 25

# Anti-cheat server options (server_get/set_anticheat_option).
aco_mode                      = 0
aco_kick_on_detection         = 1
aco_exempt_admins             = 2
aco_auto_temp_ban_seconds     = 3
aco_report_cooldown           = 4
aco_validate_seed             = 10
aco_server_authoritative_seed = 11
aco_seed_mismatch_max         = 12

# Anti-cheat modes.
acm_off     = 0
acm_silent  = 1
acm_enforce = 2
