# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from header_triggers import *
from module_constants import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags.
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
# 
####################################################################################################################

pilgrim_disguise = []
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian

multiplayer_server_log_player_leave = (
  ti_on_player_exit, 0, 0, [(multiplayer_is_server),],
  [ 
    (store_trigger_param_1, ":player_no"),
	
    (try_begin),
      (player_is_active,":player_no"),
      (str_store_player_username, s1, ":player_no"),
      (player_get_unique_id, reg13, ":player_no"),
      
      (server_add_message_to_log,"str_player_left_server_s1_reg13"),
    (try_end),
    
    (troop_set_slot, "trp_welcomed_players", ":player_no", 0),
  ])
  
# Trigger Param 1: agent id
# Trigger Param 2: horse agent id
multiplayer_server_mount_horse = (
  ti_on_agent_mount, 0, 0, [(multiplayer_is_server),],
  [ 
    (store_trigger_param_2, ":horse_id"),
	
    (try_begin),
      (agent_is_active,":horse_id"),
      (agent_is_alive,":horse_id"),
      (neg|agent_is_human,":horse_id"),
      
      (agent_clear_scripted_mode,":horse_id"),
    (try_end),
  ]) 

# Trigger Param 1: agent id
# Trigger Param 2: horse agent id
multiplayer_server_dismount_horse = (
  ti_on_agent_dismount, 0, 0, [(multiplayer_is_server),],
  [ 
    (store_trigger_param_2, ":horse_id"),
	
    (try_begin),
      (agent_is_active,":horse_id"),
      (agent_is_alive,":horse_id"),
      (neg|agent_is_human,":horse_id"),
      
      (agent_get_position,pos2,":horse_id"),
      (agent_set_scripted_destination,":horse_id",pos2,1,1),
    (try_end),
  ]) 
  
multiplayer_server_kill_stray_horses = (
  33.3, 0, 0, [(multiplayer_is_server),],
  [    
    (try_begin), # auto kill horses
      (eq,"$g_auto_horse",1),
      
      (try_for_agents, ":cur_agent"),
        (agent_is_active, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (neg|agent_is_human, ":cur_agent"), # is a horse

        (neg|agent_slot_eq,":cur_agent",slot_agent_royale_horse,1), # royale horses never get killed.
        
        (agent_get_slot, ":alone", ":cur_agent", slot_agent_alone),
        (agent_get_rider, ":rider_agent_id", ":cur_agent"),
        (try_begin),
          (lt, ":rider_agent_id", 0),
          (agent_get_item_id,":horse_kind", ":cur_agent"),
          
          (assign,":alone_time_allowance",5), # Horse 3 minutes alone
          (try_begin),
            (this_or_next|item_slot_eq,":horse_kind",slot_item_multiplayer_item_class, multi_item_class_type_horse_cannon),
            (item_slot_eq,":horse_kind",slot_item_multiplayer_item_class, multi_item_class_type_horse_howitzer),
            (assign,":alone_time_allowance",40), # horse 20 minutes alone 
          (try_end),
          
          (try_begin),
            (ge,":alone",":alone_time_allowance"),
            (agent_set_hit_points, ":cur_agent", 0, 1),
            (agent_deliver_damage_to_agent, ":cur_agent", ":cur_agent"),
          (else_try),
            (val_add, ":alone", 1),
            (agent_set_slot, ":cur_agent", slot_agent_alone, ":alone"),
          (try_end),
        (else_try),
          (gt,":alone",0), # not anymore alone reset slot.
          (agent_set_slot, ":cur_agent", slot_agent_alone, 0),
        (try_end),
      (try_end),
    (try_end),
  ])

multiplayer_server_auto_ff = (  #patch1115 46/17
  0.5, 0, 0, [(multiplayer_is_server),
               (gt,"$g_auto_FF", 0),
               ],
  [
   (try_begin),
    (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
    (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
    (neq, "$g_multiplayer_game_type", multiplayer_game_type_scene_making),
    (try_begin),
      (eq,"$g_auto_FF_2", 0),
      (assign, ":ok", 0),
      (store_mission_timer_a, ":current_time"),
      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_commander),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_king),#this mode doesn't show a round timer, but it does activate when it should
        (eq,"$g_multiplayer_game_type", multiplayer_game_type_battle),
        (eq, "$g_round_ended", 0),
        (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
        (ge, ":seconds_past_in_round", "$g_auto_FF"),
        (assign, ":ok", 1),
      (else_try),#these modes dont have rounds but have FF
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
        (eq,"$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
        (store_sub, ":seconds_past_in_round", ":current_time", "$g_match_start_time"),
        (ge, ":seconds_past_in_round", "$g_auto_FF"),
        (assign, ":ok", 1),
      (try_end),
      (eq, ":ok", 1),
      (try_begin),
        (server_get_friendly_fire, ":ff_1"),
        (neq, ":ff_1", 1),
        (server_set_friendly_fire, 1),
      (try_end),
      (try_begin),
        (server_get_melee_friendly_fire, ":ff_2"),
        (neq, ":ff_2", 1),
        (server_set_melee_friendly_fire, 1),
      (try_end),
      (str_store_string, s4, "str_FF_turn_on"),
      (call_script, "script_multiplayer_broadcast_message"),
      (assign, "$g_auto_FF_2", 1),
    (else_try),
      (eq, "$g_auto_FF_2", 1),
      (assign, ":ok", 0),
      (store_mission_timer_a, ":current_time"),
      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_commander),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_king),#this mode doesn't show a round timer, but it does activate when it should
        (eq,"$g_multiplayer_game_type", multiplayer_game_type_battle),
        (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
        (lt, ":seconds_past_in_round", "$g_auto_FF"),
        (gt, "$g_round_start_time", -1),
        (assign, ":ok", 1),
      (else_try),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
        (eq,"$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
        (store_sub, ":seconds_past_in_round", ":current_time", "$g_match_start_time"),
        (lt, ":seconds_past_in_round", "$g_auto_FF"),
        (gt, "$g_match_start_time", -1),
        (assign, ":ok", 1),
      (try_end),
      (eq, ":ok", 1),
      (try_begin),
        (server_get_friendly_fire, ":ff_1"),
        (neq, ":ff_1", 0),
        (server_set_friendly_fire, 0),
      (try_end),
      (try_begin),
        (server_get_melee_friendly_fire, ":ff_2"),
        (neq, ":ff_2", 0),
        (server_set_melee_friendly_fire, 0),
      (try_end),
      (assign,"$g_auto_FF_2", 0),
      (assign, reg60, "$g_auto_FF"),
      (str_store_string, s4, "str_FF_turn_on_when"),
      (call_script, "script_multiplayer_broadcast_message"),
    (try_end),
    
    
    (try_begin),
      (neq,"$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
      (neq,"$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
      (neq,"$g_multiplayer_game_type", multiplayer_game_type_headquarters),
      (eq, "$g_round_ended", 1),
      (eq, "$g_auto_FF_2", 1),
      (try_begin),
        (server_get_friendly_fire, ":ff_1"),
        (neq, ":ff_1", 0),
        (server_set_friendly_fire, 0),
      (try_end),
      (try_begin),
        (server_get_melee_friendly_fire, ":ff_2"),
        (neq, ":ff_2", 0),
        (server_set_melee_friendly_fire, 0),
      (try_end),
      (assign,"$g_auto_FF_2", 0),
      (assign, reg60, "$g_auto_FF"),
      (str_store_string, s4, "str_FF_turn_on_when_2"),
      (call_script, "script_multiplayer_broadcast_message"),
    (try_end),
    
  (try_end),
  
  ])
  
multiplayer_server_tp_revived_players = (  #patch1115 46/17
  0.32, 0, 0, [(multiplayer_is_server),
               (eq,"$g_should_tp", 1),],
  [    
   (try_begin),
    (assign,":agents_to_tp",0),
    (try_for_players, ":player_no", "$g_ignore_server"),
      (player_is_active,":player_no"),
      
      (player_slot_eq, ":player_no", slot_player_revive_pos, 1),
      (val_add,":agents_to_tp",1), # ammount waiting to tp
      
      (player_get_agent_id, ":player_agent_id", ":player_no"),
      (agent_is_active,":player_agent_id"),
      (agent_is_alive, ":player_agent_id"), # do it when hes alive.
      
      (player_get_slot, ":x_coor", ":player_no", slot_player_death_pos_x),
      (player_get_slot, ":y_coor", ":player_no", slot_player_death_pos_y),
      (player_get_slot, ":z_coor", ":player_no", slot_player_death_pos_z),
  
      (try_begin),
        (gt,":x_coor",0), # added this check just in case to check if slots are properly set.
        (gt,":y_coor",0),
        
        (set_fixed_point_multiplier,100),
        (init_position, pos9),
        (position_set_x, pos9, ":x_coor"),
        (position_set_y, pos9, ":y_coor"),
        (position_set_z, pos9, ":z_coor"),    
        
        (assign, ":agent_to_move", ":player_agent_id"),
        (agent_get_horse, ":horse_agent", ":agent_to_move"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (assign, ":agent_to_move", ":horse_agent"),
        (try_end),
        (agent_set_position, ":agent_to_move", pos9), # move the agent
      (try_end),
      # always set to 0
      (player_set_slot, ":player_no", slot_player_revive_pos, 0),
      (val_sub,":agents_to_tp",1), # take him off he got respawned.
    (try_end),
    
    (le,":agents_to_tp",0),
    (assign,"$g_should_tp", 0),
   (try_end),
  ])

multiplayer_server_turn_fan_blades = (
  5.11, 0, 0, [(this_or_next|neg|multiplayer_is_dedicated_server),(neg|game_in_multiplayer_mode),],
  [
    (try_for_range,":fan_type", "spr_windmill_fan_turning", "spr_mm_cannon_aim_platform"),
      (try_for_prop_instances, ":instance_id", ":fan_type", somt_object),
        #(scene_prop_slot_eq, ":instance_id", scene_prop_slot_in_use, 1), # ball is in use.
        
        (prop_instance_get_position, pos16, ":instance_id"),
        (position_rotate_y, pos16, 90),
        (prop_instance_animate_to_position, ":instance_id", pos16, 522),
      (try_end),
    (try_end),
  ])
  
multiplayer_server_move_church_bell = (
  1.5, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
      (try_for_prop_instances, ":instance_id", "spr_mm_build_church_bellmov", somt_object),
     
        (scene_prop_get_slot,":bell_state",":instance_id",scene_prop_slot_time), #6
        (is_between,":bell_state",1,7),
        (val_sub,":bell_state",1),
        (scene_prop_set_slot,":instance_id",scene_prop_slot_time,":bell_state"),
        
        (assign,":rotation",0),
        (try_begin),
          (eq,":bell_state",5),
          (assign,":rotation",25),
          (assign,":time",150),
          (prop_instance_get_position, pos56, ":instance_id"),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_church_bell"),
        (else_try),
          (eq,":bell_state",4),
          (assign,":rotation",-50),
          (assign,":time",300),
        (else_try),
          (eq,":bell_state",2),
          (assign,":rotation",50),
          (assign,":time",300),
        (else_try),
          (eq,":bell_state",0),
          (assign,":rotation",-25),
          (assign,":time",150),
        (try_end),
        (neq,":rotation",0),
        (prop_instance_get_position, pos10, ":instance_id"),
        (position_rotate_y,pos10,":rotation"),
        (prop_instance_animate_to_position,":instance_id",pos10,":time"),
      (try_end),
  ])

multiplayer_server_sail_ship = (
  0.51, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
  
      # (set_fixed_point_multiplier,100),
      # (try_for_range, ":player_no", 0, 256),
        # (player_is_active,":player_no"),
        # (player_get_agent_id, ":cur_agent", ":player_no"),
       # (agent_is_active,":cur_agent"),
       # (agent_get_speed, pos14, ":cur_agent"),
       # (position_get_y,reg22,pos14),
       
       # (display_message,"@Cur speed: {reg22}"),
     # (try_end),
     
    (set_fixed_point_multiplier,100),
    
    (try_for_range,":ship_type", "spr_mm_ship", "spr_door_destructible"),
      (try_for_prop_instances, ":instance_id", ":ship_type", somt_object),
        (scene_prop_slot_eq, ":instance_id", scene_prop_slot_in_use, 1), # ship is in use.
        (neg|scene_prop_slot_eq, ":instance_id", scene_prop_slot_bounces, 1), # abuse bounces for destroyed
        
        (scene_prop_get_slot,":cur_y_vel",":instance_id", scene_prop_slot_y_value),
        (scene_prop_get_slot,":cur_control_agent",":instance_id",scene_prop_slot_controller_agent),
        
        #(assign,":orig_y_vel",":cur_y_vel"),
        
        (try_begin),
          (neq,":cur_y_vel",0), # not zero bleed the speed.
          (val_mul,":cur_y_vel",95), # 90% bleed each second
          (val_div,":cur_y_vel",100),
        (try_end),

        (scene_prop_get_slot,":rudder_instance",":instance_id",scene_prop_slot_child_prop1),
        (prop_instance_is_valid,":rudder_instance"),
        
        (assign,":rot_change",0),
        (try_begin),
          (gt, ":cur_control_agent", -1), #PATCH1115 fix 5/1
          
          (assign,":agent_is_ok",0),
          (try_begin),
            (agent_is_active, ":cur_control_agent"),
            (agent_is_alive, ":cur_control_agent"),
            
            (prop_instance_get_position, pos10, ":rudder_instance"),
            (agent_get_position, pos11, ":cur_control_agent"),
            (get_distance_between_positions,":dist",pos10,pos11),
            
            (assign,":dist_to_check",300),
            (try_begin),
              (eq,":ship_type","spr_mm_ship_schooner"),
              (assign,":dist_to_check",600),
            (try_end),
            (le,":dist",":dist_to_check"),
            
            (assign,":agent_is_ok",1),
          (else_try),
            (call_script,"script_set_agent_controlling_prop",":instance_id",":cur_control_agent",0),
          (try_end),
          (eq,":agent_is_ok",1),
          
          (agent_get_slot,":cur_command",":cur_control_agent",slot_agent_current_command),
          (is_between, ":cur_command", ship_commands_begin, ship_commands_end),
          
          # Reset the slot
          (agent_set_slot, ":cur_control_agent", slot_agent_current_command, 0),
      
          (assign,":speed_change",20),
          (assign,":max_speed",170),
          (try_begin),
            (eq,":ship_type","spr_mm_ship_longboat_1_mast"),
            
            (assign,":speed_change",22),
            (assign,":max_speed",210),
          (else_try),
            (eq,":ship_type","spr_mm_ship_longboat_2_mast"),
            
            (assign,":speed_change",25),
            (assign,":max_speed",240),
          (else_try),
            (eq,":ship_type","spr_mm_ship_schooner"),
            
            (assign,":speed_change",16),
            (assign,":max_speed",360),
          (try_end),
          (store_mul,":speed_change_min",":speed_change",-1),
          (store_mul,":max_speed_min",":max_speed",-1),
          (val_mul,":max_speed_min",50),
          (val_div,":max_speed_min",100),
          
          # Assigning speed change
          (try_begin),
            (this_or_next|eq,":cur_command",ship_command_forward_left),
            (this_or_next|eq,":cur_command",ship_command_forward_right),
            (eq,":cur_command",ship_command_forward),
            (val_add,":cur_y_vel",":speed_change"),
            (try_begin),
              (gt,":cur_y_vel",":max_speed"),
              (assign,":cur_y_vel",":max_speed"),
            (try_end),
          (else_try),
            (this_or_next|eq,":cur_command",ship_command_back_left),
            (this_or_next|eq,":cur_command",ship_command_back_right),
            (eq,":cur_command",ship_command_back),
            
            
            # (assign,reg22,":cur_y_vel"),
            # (assign,reg23,":speed_change_min"),
            # (assign,reg24,":max_speed_min"),
            # (display_message,"@cur_y_vel: {reg22}, speed_change_min: {reg23}, max_speed_min: {reg24}"),
            
            
            (val_add,":cur_y_vel",":speed_change_min"),
            (try_begin),
              (lt,":cur_y_vel",":max_speed_min"),
              (assign,":cur_y_vel",":max_speed_min"),
            (try_end),
          (try_end),
          
          # Assigning rotation change
          
          (assign,":rot_change_value",7),
          (try_begin),
            (eq,":ship_type","spr_mm_ship_schooner"),
            
            (assign,":rot_change_value",4),
            
            (is_between, ":cur_y_vel", -200,201),
            (assign,":rot_change_value",3),
            
            (is_between, ":cur_y_vel", -100,101),
            (assign,":rot_change_value",2),
            
            (is_between, ":cur_y_vel", -50,51),
            (assign,":rot_change_value",1),
          (try_end),
          (store_mul,":rot_change_value_min",":rot_change_value",-1),
          
          (try_begin),
            (this_or_next|eq,":cur_command",ship_command_forward_right),
            (this_or_next|eq,":cur_command",ship_command_back_right),
            (eq,":cur_command",ship_command_right),
            (val_add,":rot_change",":rot_change_value_min"),
          (else_try),
            (this_or_next|eq,":cur_command",ship_command_forward_left),
            (this_or_next|eq,":cur_command",ship_command_back_left),
            (eq,":cur_command",ship_command_left),
            (val_add,":rot_change",":rot_change_value"),
          (try_end),
        (try_end),
        
        (neq,":cur_y_vel",0),

        (scene_prop_get_slot,":ship_hit_detect_prop",":instance_id",scene_prop_slot_child_prop2),
        (prop_instance_is_valid,":ship_hit_detect_prop"),
        
        (scene_prop_get_slot,":ship_hit_detect_back_prop",":instance_id",scene_prop_slot_child_prop3),
        (prop_instance_is_valid,":ship_hit_detect_back_prop"),

        # (try_begin), # from forwards to backwards
          # (ge,":orig_y_vel",0),
          # (lt,":cur_y_vel",0),
          
          # (prop_instance_get_position, pos10, ":instance_id"),
          # (position_move_y,pos10,-600),
          # (prop_instance_stop_animating,":ship_hit_detect_prop"),
          # (prop_instance_set_position,":ship_hit_detect_prop",pos10),
          
          # (scene_prop_set_slot,":ship_hit_detect_prop", scene_prop_slot_y_value,-600), # back
        # (else_try), # else backwards to forwards
          # (le,":orig_y_vel",0),
          # (gt,":cur_y_vel",0),
          
          # (prop_instance_get_position, pos10, ":instance_id"),
          # (position_move_y,pos10,240),
          # (prop_instance_stop_animating,":ship_hit_detect_prop"),
          # (prop_instance_set_position,":ship_hit_detect_prop",pos10),
           
          # (scene_prop_set_slot,":ship_hit_detect_prop", scene_prop_slot_y_value,240), # front
        # (try_end),
        
        
        (assign,":is_colliding_this_direction",0),
        (try_begin),
          (neq,":cur_y_vel",0),
          
          (assign,":y_ground_check_movement",70),
          (try_begin),
            (eq,":ship_type","spr_mm_ship_schooner"),
            (try_begin),
              (gt,":cur_y_vel",0), # forwards
              (assign,":y_offset_value",700),
            (else_try),
              (assign,":y_offset_value",-2000),
              (val_mul,":y_ground_check_movement",-1),
            (try_end),
          (else_try),
            (try_begin),
              (gt,":cur_y_vel",0), # forwards
              (assign,":y_offset_value",240),
            (else_try),
              (assign,":y_offset_value",-600),
              (val_mul,":y_ground_check_movement",-1),
            (try_end),
          (try_end),

          (set_fixed_point_multiplier,100),
          
          # ground detect
          (prop_instance_get_position, pos10, ":instance_id"),
          (position_move_y,pos10,":y_offset_value"),

          (try_begin),
            (position_get_x,":detect_x",pos10),
            (position_get_y,":detect_y",pos10),
            (this_or_next|lt,":detect_x","$g_scene_min_x"),
            (this_or_next|gt,":detect_x","$g_scene_max_x"),
            (this_or_next|lt,":detect_y","$g_scene_min_y"),
            (gt,":detect_y","$g_scene_max_y"),
        
            (assign,":is_colliding_this_direction",1),
          (else_try),
            (try_begin),
              (copy_position,pos11,pos10),
              (position_move_y,pos11,":y_ground_check_movement"),
              (position_set_z_to_ground_level,pos11),
              (position_get_z,":cur_z_height",pos11),
              (gt,":cur_z_height","$g_scene_water_level"),
              (assign,":is_colliding_this_direction",1),
            (else_try),
              (copy_position,pos11,pos10),
              (position_move_x,pos11,100), # 90
              (position_set_z_to_ground_level,pos11),
              (position_get_z,":cur_z_height",pos11),
              (gt,":cur_z_height","$g_scene_water_level"),
              (assign,":is_colliding_this_direction",1),
            (else_try),
              (copy_position,pos11,pos10),
              (position_move_x,pos11,-100),
              (position_set_z_to_ground_level,pos11),
              (position_get_z,":cur_z_height",pos11),
              (gt,":cur_z_height","$g_scene_water_level"),
              (assign,":is_colliding_this_direction",1),
            (try_end),
          (try_end),
          
          (eq,":is_colliding_this_direction",0),
          
          (try_begin),
            (gt,":cur_y_vel",0), # forwards
            (try_begin),
              (prop_instance_intersects_with_prop_instance, ":ship_hit_detect_prop", -1), #give second scene_prop_id as -1 to check all scene props.
              #cannot check polygon-to-polygon physics models, but can check any other combinations between sphere, capsule and polygon physics models.
              
            #  (display_message,"@hit_detect_front"),
               
              (assign,":is_colliding_this_direction",1),
            (try_end),
          (else_try),         
            #(this_or_next|prop_instance_intersects_with_prop_instance, ":rudder_instance", -1), 
            (prop_instance_intersects_with_prop_instance, ":ship_hit_detect_back_prop", -1), 
            #(display_message,"@hit_detect_rudder"),
            
            (assign,":is_colliding_this_direction",1),
          (try_end),
        (try_end),
        
        (try_begin),
          (eq,":is_colliding_this_direction",1),
          (neq,":cur_y_vel",0),
          
          (assign,":cur_y_vel",0),
         # (display_message,"@Collision!"),
        (try_end),
        
        (try_begin),
          (eq,":cur_y_vel",0),
          (assign,":rot_change",0),
        (try_end),
        
        (prop_instance_get_position, pos57, ":instance_id"),
        
        (position_move_y, pos57, ":cur_y_vel"),
        (position_rotate_z, pos57, ":rot_change"),
        
        (call_script, "script_prop_instance_animate_to_position_with_childs", ":instance_id", 100,0,0),
        # Store new speed
        (scene_prop_set_slot, ":instance_id", scene_prop_slot_y_value, ":cur_y_vel"),

        
        # if we have rotation, rotate rudder a bit difirent for sexy effects. :D
        (neq,":rot_change",0),
        (val_mul,":rot_change",-4),
        
        (scene_prop_get_slot,":y_value",":rudder_instance",scene_prop_slot_y_value),
        (position_move_y,pos57,":y_value"),
        (position_rotate_z, pos57, ":rot_change"),
        (call_script, "script_prop_instance_animate_to_position_with_childs", ":rudder_instance", 100,0,0),
      (try_end),
    (try_end),
 ])
  
multiplayer_client_control_ship = (
  0, 0, 0.25, [(neg|multiplayer_is_dedicated_server),
              (eq, "$g_currently_controlling_object", 1),              
              (is_between,"$g_cur_control_prop_kind", "spr_mm_ship", "spr_door_destructible"),
              (this_or_next|key_is_down, key_up),
              (this_or_next|key_is_down, key_down),
              (this_or_next|key_is_down, key_left),
              (key_is_down, key_right),
           ],
  [
    # (store_mission_timer_a, ":current_time"),
    # (store_sub, ":elapsed_time", ":current_time", "$g_last_steer_command_at"),
    
    # (ge, ":elapsed_time", 1), # last use more then x seconds ago. 
    
    (assign,":command",-1),
    (try_begin),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
      (assign,":command",ship_command_forward_left),
    (else_try),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
      (assign,":command",ship_command_forward_right),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
      (assign,":command",ship_command_back_left),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
      (assign,":command",ship_command_back_right),
    (else_try),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
      (assign,":command",ship_command_forward),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
      (assign,":command",ship_command_back),
    (else_try),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
      (assign,":command",ship_command_left),
    (else_try),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
      (assign,":command",ship_command_right),
    (try_end),
    
    # ship_command_forward       
    # ship_command_back          
    # ship_command_left          
    # ship_command_right         
    # ship_command_forward_left  
    # ship_command_forward_right 
    # ship_command_back_left     
    # ship_command_back_right    
    
    (gt,":command",-1),
    (multiplayer_send_2_int_to_server,multiplayer_event_send_control_command,command_type_ship,":command"),
    
    #(store_mission_timer_a, "$g_last_steer_command_at"),
  ])

multiplayer_server_drag_limber = (
0.25, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [  
    (try_for_prop_instances, ":instance_id", "spr_mm_limber_wood", somt_temporary_object),
      (scene_prop_get_slot,":cur_control_agent",":instance_id",scene_prop_slot_carrier_agent),
      (ge, ":cur_control_agent", 0),
      
      (assign,":agent_is_ok",0),
      (try_begin),
        (agent_is_active, ":cur_control_agent"),
        (agent_is_alive, ":cur_control_agent"),
        (assign,":agent_is_ok",1),
      (else_try), # The agent died... lets set some vars on this one.
        (scene_prop_set_slot,":instance_id",scene_prop_slot_carrier_agent,-1),
        
        (store_mission_timer_a,":cur_time"),
        (scene_prop_set_slot,":instance_id",scene_prop_slot_spawned_at,":cur_time"),
        
        (prop_instance_get_animation_target_position,pos12,":instance_id"),
        (position_set_z_to_ground_level,pos12),
        (position_move_z,pos12,-30),
        (position_move_y,pos12,-18),
        (position_rotate_x,pos12,-22),
        (prop_instance_animate_to_position,":instance_id",pos12,100),
      (try_end),
      (eq,":agent_is_ok",1),
      
      (scene_prop_get_slot,":wheels_instance",":instance_id",scene_prop_slot_child_prop1),
      (scene_prop_get_slot,":cannon_instance",":instance_id",scene_prop_slot_child_prop2),
      (try_begin),
        (prop_instance_is_valid,":cannon_instance"),
        (scene_prop_get_slot,":cannon_wheels_instance",":cannon_instance",scene_prop_slot_child_prop1),
      (try_end),
      
      # if this limber has wheels
      (prop_instance_is_valid,":wheels_instance"),
      
      (set_fixed_point_multiplier, 1000),
      (agent_get_position, pos11, ":cur_control_agent"),
      (position_get_rotation_around_z,":z_rot_temp",pos11),
      
      (agent_get_speed, pos14, ":cur_control_agent"),
      (position_get_y,":agent_speed",pos14),
      
      (assign,":continue",1),
      (try_begin),
        (agent_get_slot,":old_zrot",":cur_control_agent",slot_agent_last_rotz),
        
        (try_begin),
          (eq,":agent_speed",0), # same speed now
          (eq,":z_rot_temp",":old_zrot"), # same rot.
          (agent_get_slot,":samecount",":cur_control_agent",slot_agent_last_speed_same_count),
          (try_begin),
            (gt,":samecount",2), # 2 times same shit.
            (assign,":continue",0),
          (else_try),
            (val_add,":samecount",1),
            (agent_set_slot, ":cur_control_agent", slot_agent_last_speed_same_count, ":samecount"),
          (try_end),
        (else_try),
          (agent_set_slot, ":cur_control_agent", slot_agent_last_speed_same_count, 0),
        (try_end),
        
        (agent_set_slot, ":cur_control_agent", slot_agent_last_rotz, ":z_rot_temp"),
      (try_end),
      (eq,":continue",1),
      
      # (try_begin),
        # (eq,":agent_speed",0), # no movement...
        # (position_get_rotation_around_z,":z_rot_temp",pos11),
        # (prop_instance_get_position, pos13, ":instance_id"),
        # (position_get_rotation_around_z,":prop_z_rot_temp",pos13),
        # (eq,":prop_z_rot_temp",":z_rot_temp"),
        # (assign,":continue",0),
      # (try_end),
       
      
      # max speed 2907  old:  2766
        # (assign, reg0, ":agent_speed"),
        # (str_store_string, s4, "@agent_speed: {reg0}"),
        # (call_script, "script_multiplayer_broadcast_message"),
      
      (store_mul,":agent_speed_wheel",":agent_speed",-1), # inverse
      (store_div,":limber_wheel_speed",":agent_speed_wheel",64), # make it realistic for front wheels
      (store_div,":cannon_wheel_speed",":agent_speed_wheel",76), # make it realistic for cannon wheels
      
      # From the agent position (flat on ground middle of horse) only save the Z rot and origin.
      (position_get_rotation_around_z,":z_rot",pos11),
      (init_position,pos12),
      (position_copy_origin,pos12,pos11),
      (position_rotate_z,pos12,":z_rot"),
      
      # move above ground. (for proper get_distance_to_ground checks)
      (scene_prop_get_slot,":z_offset",":instance_id",scene_prop_slot_z_value),
      (position_move_z,pos12,":z_offset"),
      
      # copy it over to 14 for later use, now just use 12 for getting rotations.
      (copy_position,pos14,pos12),
      
      # move from middle of horse to center where wheels should be.
      (scene_prop_get_slot,":y_offset",":wheels_instance",scene_prop_slot_y_value),
      (position_move_y, pos12,":y_offset"),
      
      # march to left wheel and get height there.
      (position_move_x,pos12,-60),
      (position_get_distance_to_ground_level, ":left_height_to_terrain", pos12),
      (val_div,":left_height_to_terrain",10), # due to fixed point at 1000
      
      # march to right wheel and get height there.
      (position_move_x,pos12,120),
      (position_get_distance_to_ground_level, ":right_height_to_terrain", pos12),
      (val_div,":right_height_to_terrain",10), # due to fixed point at 1000
      
      # march back to center
      # (position_rotate_z,pos12,180),
      # (position_move_y,pos12,60),
      # (position_rotate_z,pos12,-90),
      
      # calculate
      (store_sub,":height_difference",":left_height_to_terrain",":right_height_to_terrain"),
     
      (store_div,":combined_height",":height_difference",2),
      (try_begin),
        (gt,":combined_height",0),
        (val_mul,":combined_height",-1),
      (try_end),      

      (val_mul,":height_difference",1000), # make it fixed point
      (store_div,":deg_value2",":height_difference",120),  # 120 is distance between the two wheels.
      (store_atan,":deg_value2",":deg_value2"), # get the angle
      (val_div,":deg_value2",1000),
      (val_mul,":deg_value2",-1),

      
      # combine the two heights and get the angle between them combined and the horse position.
      (store_add,":height_to_terrain",":left_height_to_terrain",":right_height_to_terrain"),
      (val_div,":height_to_terrain",2), 
      
      # some weird fix i forgot why.      
      (val_mul,":combined_height",46),
      (val_div,":combined_height",100),
      (val_add,":height_to_terrain",":combined_height"),
      
      (store_sub,":height_difference",":height_to_terrain",":z_offset"),
      (val_mul,":height_difference",1000), # make it fixed point
      (store_div,":deg_value",":height_difference",":y_offset"),
      (store_atan,":deg_value",":deg_value"), # get the angle
      (val_div,":deg_value",1000),
      (val_mul,":deg_value",-1),
      
      # Tweaking for slope, (wheels are round so should "float" a bit when on angle so their not into ground)
      (try_begin),
        (lt,":deg_value",0),
        (val_mul,":deg_value",108), # 108 %
        (val_div,":deg_value",100),
      (else_try),
        (gt,":deg_value",0),
        (val_mul,":deg_value",92), # 92 %
        (val_div,":deg_value",100),
      (try_end),
      
      # move it up, rotate it, move it down (or a bit sideways that is...)
      # 50 cm is the bars height above the center of liberwood.
      (position_move_z,pos14,50),
      (position_rotate_y,pos14,":deg_value2"),
      (position_move_z,pos14,-50),
      
      # Do a slight Z change due to the bars otherwise sticking into the horse.
      # (try_begin),
        # (neq,":deg_value2",0),

        # (store_div,":deg_value2_div",":deg_value2",8),
        # (position_rotate_z,pos14,":deg_value2_div"),
        
        # (val_add,":z_rot",":deg_value2_div"),
      # (try_end),
      (scene_prop_get_slot,":previous_z_rot",":instance_id",scene_prop_slot_z_extra),
      (scene_prop_set_slot,":instance_id",scene_prop_slot_z_extra,":z_rot"),
      
      (position_rotate_x,pos14,":deg_value"),
      
      # And finally move the wood to this rotated position.
      (prop_instance_animate_to_position, ":instance_id", pos14, 28),
      
      # move from middle of horse to center where wheels should be.
      (position_move_y, pos14,":y_offset"),
      
      # overwrite the 12 we temporary used.
      (copy_position,pos12,pos14),
      
      # reset pos14 its X rotation for the weels (they store their own rotation and rotate with it.)
      (position_get_rotation_around_x,":parent_x_rot",pos14),
      (val_mul,":parent_x_rot",-1),
      (position_rotate_x,pos14,":parent_x_rot"),
      
      (scene_prop_get_slot,":x_rot",":wheels_instance",scene_prop_slot_x_extra),
      (val_add,":x_rot",":limber_wheel_speed"),
      (try_begin),
        (gt,":x_rot",360),
        (val_sub,":x_rot",360),
      (try_end),
      (scene_prop_set_slot,":wheels_instance",scene_prop_slot_x_extra,":x_rot"),
      (position_rotate_x,pos14,":x_rot"),
      
      (prop_instance_animate_to_position, ":wheels_instance", pos14, 28),
      
      
      # if we have a cannon and wheels, go on.
      (prop_instance_is_valid,":cannon_instance"),
      (prop_instance_is_valid,":cannon_wheels_instance"),
      
      (store_sub,":diffirence_z_old_new",":previous_z_rot",":z_rot"),
      
      (try_begin),
        (gt,":diffirence_z_old_new",300),
        (val_sub,":diffirence_z_old_new",360),
      (else_try),
        (lt,":diffirence_z_old_new",-300),
        (val_add,":diffirence_z_old_new",360),
      (try_end),
      
      # calculate percent speed
      (val_mul,":agent_speed",100),
      (val_div,":agent_speed",2907), # speed/max speed
      
      # calc difirence * percent speed
      (val_mul,":diffirence_z_old_new",":agent_speed"),
      (val_div,":diffirence_z_old_new",100),
      
      (scene_prop_get_slot,":previous_z_rot",":cannon_instance",scene_prop_slot_z_extra),
      (store_sub,":diffirence_z_object",":previous_z_rot",":z_rot"),
      
      (try_begin),
        (gt,":diffirence_z_object",300),
        (val_sub,":diffirence_z_object",360),
      (else_try),
        (lt,":diffirence_z_object",-300),
        (val_add,":diffirence_z_object",360),
      (try_end),
       
      (try_begin),
        (neq,":agent_speed",0),
        (val_mul, ":agent_speed", 40), 
        (val_div, ":agent_speed", 100), # value * 40 / 100 = - 40% of the speed
        (store_mul,":sub_dif",":diffirence_z_object",":agent_speed"),

        (try_begin),
          (is_between, ":sub_dif", -100, 101),
          (eq,":diffirence_z_old_new",0),
          (assign,":diffirence_z_object",0),
        (else_try),
          (val_div,":sub_dif",100),
          (val_sub,":diffirence_z_object",":sub_dif"),
        (try_end),
      (try_end),

      (val_add,":diffirence_z_object",":diffirence_z_old_new"),
       
      (try_begin),
        (gt,":diffirence_z_object",40),
        (assign,":diffirence_z_object",40),
      (else_try),
        (lt,":diffirence_z_object",-40),
        (assign,":diffirence_z_object",-40),
      (try_end),
      
      # move a bit up so the wedge is on the spike of the limber.
      (scene_prop_get_slot,":cannon_z_offset",":cannon_instance",scene_prop_slot_z_value),
      (position_move_z,pos12,":cannon_z_offset"),
      (store_add,":total_z_offset",":z_offset",6),
      
      # Reset pos12 rotations except Z, so we have a fresh pos12 to use.
      (store_mul,":deg_value2_min",":deg_value2",-1),
      (store_mul,":deg_value_min",":deg_value",-1),
      (position_rotate_x,pos12,":deg_value_min"),
      (position_rotate_y,pos12,":deg_value2_min"),
      
      # Rotate to the difirence calculated.
      (position_rotate_z,pos12,":diffirence_z_object"),
      (val_add,":diffirence_z_object",":z_rot"),
      (scene_prop_set_slot,":cannon_instance",scene_prop_slot_z_extra,":diffirence_z_object"),
      
      (copy_position,pos14,pos12),
      
      # move to wheels position.
      (scene_prop_get_slot,":y_offset",":cannon_wheels_instance",scene_prop_slot_y_value),
      (position_move_y, pos12,":y_offset"),
      
      # march to left wheel and get height there.
      (position_move_x,pos12,-72),
      (position_get_distance_to_ground_level, ":left_height_to_terrain", pos12),
      (val_div,":left_height_to_terrain",10), # due to fixed point at 1000
      
      # march to right wheel and get height there.
      (position_move_x,pos12,144),
      (position_get_distance_to_ground_level, ":right_height_to_terrain", pos12),
      (val_div,":right_height_to_terrain",10), # due to fixed point at 1000
      

      # calculate
      (store_sub,":height_difference",":left_height_to_terrain",":right_height_to_terrain"),
     
      (store_div,":combined_height",":height_difference",2),
      (try_begin),
        (gt,":combined_height",0),
        (val_mul,":combined_height",-1),
      (try_end),      

      (val_mul,":height_difference",1000), # make it fixed point
      (store_div,":deg_value2",":height_difference",120),  # 120 is distance between the two wheels.
      (store_atan,":deg_value2",":deg_value2"), # get the angle
      (val_div,":deg_value2",1000),
      (val_mul,":deg_value2",-1),

      
      # combine the two heights and get the angle between them combined and the horse position.
      (store_add,":height_to_terrain",":left_height_to_terrain",":right_height_to_terrain"),
      (val_div,":height_to_terrain",2), 
      
      # some weird fix i forgot why.
      (val_mul,":combined_height",44),
      (val_div,":combined_height",100),
      (val_add,":height_to_terrain",":combined_height"),
      
      (store_sub,":height_difference",":height_to_terrain",":total_z_offset"),
      (val_mul,":height_difference",1000), # make it fixed point
      (store_div,":deg_value",":height_difference",":y_offset"),
      (store_atan,":deg_value",":deg_value"), # get the angle
      (val_div,":deg_value",1000),
      (val_mul,":deg_value",-1),
      
      # Tweaking for slope, (wheels are round so should "float" a bit when on angle so their not into ground)
      (try_begin),
        (lt,":deg_value",0),
        (val_mul,":deg_value",108), # 108 %
        (val_div,":deg_value",100),
      (else_try),
        (gt,":deg_value",0),
        (val_mul,":deg_value",92), # 92 %
        (val_div,":deg_value",100),
      (try_end),
      
      (position_rotate_y,pos14,":deg_value2"),
      (position_rotate_x,pos14,":deg_value"),

      (prop_instance_animate_to_position, ":cannon_instance", pos14, 28),
      
      
      # Wheels.
      # move from middle of spike to the wheel position on limber.
      (position_move_y, pos14,":y_offset"),
      
      # reset pos14 its X rotation for the weels (they store their own rotation and rotate with it.)
      (position_get_rotation_around_x,":parent_x_rot",pos14),
      (val_mul,":parent_x_rot",-1),
      (position_rotate_x,pos14,":parent_x_rot"),

      (scene_prop_get_slot,":x_rot",":cannon_wheels_instance",scene_prop_slot_x_extra),
      (val_add,":x_rot",":cannon_wheel_speed"),
      (try_begin),
        (gt,":x_rot",360),
        (val_sub,":x_rot",360),
      (try_end),
      (scene_prop_set_slot,":cannon_wheels_instance",scene_prop_slot_x_extra,":x_rot"),
      (position_rotate_x,pos14,":x_rot"),
      
      (prop_instance_animate_to_position, ":cannon_wheels_instance", pos14, 28),
    (try_end),
  ])
  
multiplayer_client_control_cannon = (
  0, 0, 1, [ # Execute conditions.
             (neg|multiplayer_is_dedicated_server),
             (eq, "$g_currently_controlling_object", 1),
             (this_or_next|game_key_clicked, gk_attack),
             (game_key_clicked, gk_defend),
             (is_between,"$g_cur_control_prop_kind", mm_cannon_wood_types_begin,mm_cannon_wood_types_end),
           ],
  [
    (assign,":command",-1),
    (try_begin),
      (game_key_clicked, gk_defend),
      (assign,":command",cannon_command_stop_aim),
    (else_try),
      (game_key_clicked, gk_attack),
      (assign,":command",cannon_command_fire),
    (try_end),
  
    (gt,":command",-1),
    (try_begin),
      (game_in_multiplayer_mode),
      (multiplayer_send_2_int_to_server,multiplayer_event_send_control_command,command_type_cannon,":command"),
    (else_try),
      (call_script,"script_client_get_my_agent"),
      (call_script,"script_handle_agent_control_command",reg0,command_type_cannon,":command"),
    (try_end),
  ])
    
multiplayer_client_voicecommands = (
  0, 0, 1, [ # Execute conditions.
             (neg|multiplayer_is_dedicated_server),
             (game_key_clicked, gk_character_window),
           ],
  [
  
    # (try_begin),
      # (assign,":0_count",0),
      # (assign,":1_count",0),
      # (assign,":2_count",0),
      # (assign,":3_count",0),
      # (assign,":4_count",0),
      # (assign,":5_count",0),
      # (assign,":6_count",0),
      # (assign,":7_count",0),
      # (assign,":8_count",0),
      # (assign,":9_count",0),
      # (try_for_range,":value",0,100000),
        # (call_script,"script_store_vince_random_in_range", 0, 10),
        # #(store_random_in_range,reg0,0,10),
        
        # (try_begin),
          # (eq,reg0,0),
          # (val_add,":0_count",1),
        # (else_try),
          # (eq,reg0,1),
          # (val_add,":1_count",1),
        # (else_try),
          # (eq,reg0,2),
          # (val_add,":2_count",1),
        # (else_try),
          # (eq,reg0,3),
          # (val_add,":3_count",1),
        # (else_try),
          # (eq,reg0,4),
          # (val_add,":4_count",1),
        # (else_try),
          # (eq,reg0,5),
          # (val_add,":5_count",1),
        # (else_try),
          # (eq,reg0,6),
          # (val_add,":6_count",1),
        # (else_try),
          # (eq,reg0,7),
          # (val_add,":7_count",1),
        # (else_try),
          # (eq,reg0,8),
          # (val_add,":8_count",1),
        # (else_try),
          # (eq,reg0,9),
          # (val_add,":9_count",1),
        # (try_end),
      # (try_end),
      
      # (assign,reg0,":0_count"),
      # (assign,reg1,":1_count"),
      # (assign,reg2,":2_count"),
      # (assign,reg3,":3_count"),
      # (assign,reg4,":4_count"),
      # (assign,reg5,":5_count"),
      # (assign,reg6,":6_count"),
      # (assign,reg7,":7_count"),
      # (assign,reg8,":8_count"),
      # (assign,reg9,":9_count"),
        # (display_message,"@0_count: {reg0} 1_count: {reg1} 2_count: {reg2} 3_count: {reg3} 4_count: {reg4} 5_count: {reg5} 6_count: {reg6} 7_count: {reg7} 8_count: {reg8} 9_count: {reg9} "),
      
       # # (try_for_range,":value",0,20),
         # # (store_random_in_range,":resulting_random",0,10),
         # # (assign,reg0,":resulting_random"),
         # # (display_message,"@CWB randomvalue: {reg0}"),
       # # (try_end),
      
    # (try_end),
  
    (store_mission_timer_a, ":current_time"),
    (store_sub, ":elapsed_time", ":current_time", "$g_last_voice_command_at"),
    
    (call_script, "script_client_get_my_agent"),
    (assign, ":player_agent", reg0),
    
    (agent_is_active,":player_agent"),
    (agent_is_alive, ":player_agent"), # Still alive?
    
    (try_begin),
      (call_script,"script_cf_agent_is_playing_music",":player_agent"), # when playing music dont do anything.
    (else_try),
      (call_script,"script_cf_agent_is_playing_piano",":player_agent"), # when playing music dont do anything.
      
    (else_try),
      (agent_get_troop_id, ":player_troop_id", ":player_agent"),
      
      (troop_get_slot,":player_troop_rank",":player_troop_id",slot_troop_rank),
       
      (assign, ":wait_time", "$g_time_between_voice_commands"), # change later.
      (try_begin),
        (this_or_next|eq, ":player_troop_rank", mm_rank_sergeant),
        (this_or_next|eq, ":player_troop_rank", mm_rank_officer),
        (eq, ":player_troop_rank", mm_rank_general),
        (assign, ":wait_time", "$g_time_between_voice_commands_officer"),
      (try_end),
      
      (val_add,":wait_time",5), # add two due to lag...  changed to 5.
      (gt, ":elapsed_time", ":wait_time"), # last command more then x seconds ago. 

      # not in some presentation?
      (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
      (neg|is_presentation_active, "prsnt_game_multiplayer_admin_panel"),
      (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
      (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"), #custom_chat:
      
      (assign, ":voice_type", -1),
      (try_begin),
        (game_key_clicked, gk_character_window),
        (assign, ":voice_type", voice_type_cry),
        
        #TEST
        #(agent_set_damage_modifier, ":player_agent", 1000), # value is in percentage, 100 is default
        #(agent_set_accuracy_modifier, ":player_agent", 1000), # value is in percentage, 100 is default, value can be between [0..1000]
        #(agent_set_speed_modifier, ":player_agent", 1000), # value is in percentage, 100 is default, value can be between [0..1000]
        #(agent_set_reload_speed_modifier, ":player_agent", 1000), # value is in percentage, 100 is default, value can be between [0..1000]
        #(agent_set_use_speed_modifier, ":player_agent", 1000), # value is in percentage, 100 is default, value can be between [0..1000]
        #(display_message,"@Your battle cry inspires you!"),
        #TEST
      (try_end),

      (try_begin),
        (gt, ":voice_type", -1),
       
        (try_begin),
          (game_in_multiplayer_mode),
          (multiplayer_send_2_int_to_server,multiplayer_event_send_player_action,player_action_voice,":voice_type"),
        (else_try),
          (call_script,"script_multiplayer_server_agent_play_voicecommand", ":player_agent",":voice_type"),
        (try_end),
        
        (store_mission_timer_a, "$g_last_voice_command_at"),
      (try_end),
    (try_end),
  ])

multiplayer_server_order_voicecommands = (
  ti_on_order_issued, 0, 0.1, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode)],
  [
    (store_trigger_param_1,":order"),
    (store_trigger_param_2,":agent_id"),
    
    # (assign,reg22,":order"),
    # (display_message,"@order: {reg22}"),
    
    (try_begin),
      (agent_is_active,":agent_id"),
      (agent_is_alive,":agent_id"),
      
      (try_begin),
        (call_script,"script_cf_agent_is_playing_music",":agent_id"), # when playing music dont do anything.
      (else_try),
        (call_script,"script_cf_agent_is_playing_piano",":agent_id"),
      
      (else_try),
        
        (assign, ":voice_type", -1),
        (try_begin),
          (eq, ":order", mordr_fire_at_my_command),
          (assign, ":voice_type", voice_type_comm_present),
        (else_try),
          (is_between, ":order", mordr_all_fire_now,mordr_form_1_row),
          (assign, ":voice_type", voice_type_comm_fire),
        (else_try),
          (eq, ":order", mordr_charge),
          (assign, ":voice_type", voice_type_comm_charge),
        (else_try),
          (eq, ":order", mordr_advance),
          (assign, ":voice_type", voice_type_comm_advance),
        (else_try),
          (this_or_next|eq, ":order", mordr_hold),
          (eq, ":order", mordr_stand_ground),
          (assign, ":voice_type", voice_type_comm_hold),
        (else_try),
          (eq, ":order", mordr_fire_at_will),
          (assign, ":voice_type", voice_type_comm_fire_at_will),
        (else_try),
          (eq, ":order", mordr_follow),
          (assign, ":voice_type", voice_type_comm_on_me),
        (else_try),
          (eq, ":order", mordr_fall_back),
          (assign, ":voice_type", voice_type_comm_fall_back),
        (else_try),
          (eq, ":order", mordr_use_ranged_weapons),
          (assign, ":voice_type", voice_type_comm_ready),
        (try_end),
        
        (gt, ":voice_type", -1),

        (call_script,"script_multiplayer_server_agent_play_voicecommand", ":agent_id",":voice_type"),
      (try_end),
    (try_end),
  ])
  
multiplayer_server_aim_cannon  = (
  0.5, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode)],
  [  
    (set_fixed_point_multiplier, 100),
    (try_for_range,":cannon_type", mm_cannon_wood_types_begin, mm_cannon_wood_types_end),
      (try_for_prop_instances, ":instance_id", ":cannon_type", somt_temporary_object),
        (scene_prop_get_slot,":cur_control_agent",":instance_id",scene_prop_slot_controller_agent),
        
        (agent_is_active, ":cur_control_agent"),
        
        (prop_instance_get_position, pos10, ":instance_id"),
        
        (assign,":agent_is_ok",0),
        (try_begin),
          (agent_is_alive, ":cur_control_agent"),
        
          (agent_get_horse,":horse",":cur_control_agent"),
          (eq,":horse",-1),          
          
          (agent_get_position, pos11, ":cur_control_agent"),
          
          (get_distance_between_positions,":dist",pos10,pos11),
          (le, ":dist", 600),
          
          (assign,":agent_is_ok",1),
        (else_try),
          (call_script,"script_stop_agent_controlling_cannon",":instance_id",":cur_control_agent"),
        (try_end),
        
        (eq,":agent_is_ok",1),
        
        (store_mission_timer_a,":cur_time"),
        (scene_prop_set_slot,":instance_id",scene_prop_slot_spawned_at,":cur_time"),
        
        # (try_begin),
          # (call_script, "script_prop_instance_find_first_child_of_type", ":instance_id", "spr_mm_cannon_aim_platform"),
          # (prop_instance_is_valid,reg0),
          # (neg|scene_prop_has_agent_on_it, reg0, ":cur_control_agent"),
          ####(call_script,"script_stop_agent_controlling_cannon",":instance_id",":cur_control_agent"),
          # (prop_instance_get_position,pos9,reg0),
          # (agent_set_position,":cur_control_agent",pos9),
        # (try_end),
        
        # Handle firing first, else handle aiming.
        (agent_get_slot,":cur_command",":cur_control_agent",slot_agent_current_command),
        (try_begin),
          (eq,":cur_command",cannon_command_fire),
          
          (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
          (try_begin),
            (eq,":cur_time",1), # already been once then fire it! :)
            
            (call_script,"script_fire_cannon",":instance_id",":cur_control_agent"),
            
            (agent_set_slot, ":cur_control_agent", slot_agent_current_command, 0),
            (assign,":cur_time",0),
          (else_try),
            (val_add,":cur_time",1),
          (try_end),
          
          (scene_prop_set_slot,":instance_id", scene_prop_slot_time, ":cur_time"),
        (else_try),
          
          (copy_position,pos19,pos10),
          (agent_get_look_position, pos11, ":cur_control_agent"),
          (copy_position,pos23,pos11),
          (position_rotate_z, pos11, 90),
          
          (try_begin),
            (eq,":cannon_type","spr_mm_cannon_mortar_wood"),
            
            (call_script,"script_search_for_first_ground_from_direction_to_angle"),
            (assign,":agent_y_rot",reg0),
          (else_try),
            (position_get_rotation_around_y,":agent_y_rot",pos11),
          (try_end),
          
          #(get_distance_between_positions,":dist",pos10,pos11),
          (try_begin),
            # (gt, ":dist", 500),
            
            # (call_script,"script_stop_agent_controlling_cannon",":instance_id",":cur_control_agent"),
          # (else_try),
            (call_script,"script_cannon_instance_get_barrel",":instance_id"),
            (assign,":barrel_instance",reg0),

           # (position_rotate_z, pos11, 90), # Rotate because the agent front is Y axis but for cannons it is the X axis.. lol..
           # 
            (position_get_rotation_around_z,":agent_z_rot",pos11),
          #   (position_get_rotation_around_y,":agent_y_rot",pos11),
            (position_get_rotation_around_z,":prop_z_rot",pos10),
            
                        
            (assign,":prop_y_rot",0),
            (assign,":can_y_rot",0),
            (try_begin),
              (prop_instance_is_valid,":barrel_instance"), # patch1115 18/23
              
              (prop_instance_get_position,pos12,":barrel_instance"),
              (position_get_rotation_around_y,":prop_y_rot",pos12),
              
              (position_get_rotation_around_y,":can_y_rot",pos10),
            (else_try),
              (position_get_rotation_around_y,":prop_y_rot",pos10),
            (try_end),
            
            (store_sub,":diffirence_z",":agent_z_rot",":prop_z_rot"),
            (store_sub,":diffirence_y",":agent_y_rot",":prop_y_rot"),
            
            (try_begin),
              (gt,":diffirence_z",180),
              (val_sub,":diffirence_z",360),
            (else_try),
              (lt,":diffirence_z",-180),
              (val_add,":diffirence_z",360),
            (try_end),
            
            (try_begin),
              (gt,":diffirence_y",180),
              (val_sub,":diffirence_y",360),
            (else_try),
              (lt,":diffirence_y",-180),
              (val_add,":diffirence_y",360),
            (try_end),
            
            (try_begin),
              (gt,":diffirence_z",4),
              (assign,":diffirence_z",4),
            (else_try),
              (lt,":diffirence_z",-4),
              (assign,":diffirence_z",-4),
            (try_end),
            
            (try_begin),
              (gt,":diffirence_y",2),
              (assign,":diffirence_y",2),
            (else_try),
              (lt,":diffirence_y",-2),
              (assign,":diffirence_y",-2),
            (try_end),
            
            # Limit cannon Z rot if applicable
            (scene_prop_get_slot,":z_rotation_limit",":instance_id",scene_prop_slot_z_rotation_limit),
            (try_begin),
              (gt, ":z_rotation_limit", 0),

              (scene_prop_get_slot,":prop_z_rot_offset",":instance_id",scene_prop_slot_z_rot),
              
              (store_add,":new_prop_z_rot_offset",":prop_z_rot_offset",":diffirence_z"),# Add the change towards the current rotation.
              (store_mul,":z_rotation_limit_min",":z_rotation_limit",-1),
              
              (try_begin),
                (gt,":new_prop_z_rot_offset",":z_rotation_limit"),
                (assign,":prop_z_rot_offset",":z_rotation_limit"),
                (store_sub,":res_diffirence_z",":new_prop_z_rot_offset",":prop_z_rot_offset"),
                (val_sub,":diffirence_z",":res_diffirence_z"),
              (else_try),
                (lt,":new_prop_z_rot_offset",":z_rotation_limit_min"),
                (assign,":prop_z_rot_offset",":z_rotation_limit_min"),
                (store_sub,":res_diffirence_z",":new_prop_z_rot_offset",":prop_z_rot_offset"),
                (val_sub,":diffirence_z",":res_diffirence_z"),
              (else_try),
                (assign,":prop_z_rot_offset",":new_prop_z_rot_offset"),
              (try_end),
              
              (scene_prop_set_slot,":instance_id",scene_prop_slot_z_rot,":prop_z_rot_offset"), 
            (try_end),

            (position_rotate_z,pos10,":diffirence_z"),
            (copy_position,pos57,pos10),

            (try_begin),
              (prop_instance_is_valid,":barrel_instance"), #patch1115 18/24
              
              (call_script, "script_prop_instance_animate_to_position_with_childs", ":instance_id", 53,":barrel_instance",0),
   
              (scene_prop_get_slot,":xvalue",":barrel_instance",scene_prop_slot_x_value),
              (scene_prop_get_slot,":yvalue",":barrel_instance",scene_prop_slot_y_value),
              (scene_prop_get_slot,":zvalue",":barrel_instance",scene_prop_slot_z_value),
              (position_move_x, pos57,":xvalue"),
              (position_move_y, pos57,":yvalue"),
              (position_move_z, pos57,":zvalue"),
                           
              (val_sub,":prop_y_rot",":can_y_rot"), 
              (try_begin),
                (lt,":prop_y_rot",0),
                (val_add,":prop_y_rot",360),
              (try_end),
              (val_add,":prop_y_rot",":diffirence_y"),# Add the change towards the current rotation.

              (try_begin),
                (neq,":cannon_type","spr_mm_cannon_mortar_wood"),
                (try_begin), # limit barrel rotations
                  (is_between,":prop_y_rot",180,340), # upper limit
                  (assign,":prop_y_rot",340),
                (else_try),
                  (is_between,":prop_y_rot",19,180), # down limit
                  (assign,":prop_y_rot",18),
                (try_end),
              (try_end),
              
              (position_rotate_y,pos57,":prop_y_rot"),
              
              (scene_prop_set_slot,":barrel_instance",scene_prop_slot_y_rot,":prop_y_rot"), # store rotation to keep barrel in same direction :3
              
              (call_script, "script_prop_instance_animate_to_position_with_childs", ":barrel_instance", 53,0,0),
            (else_try),
              (position_rotate_y,pos57,":diffirence_y"),
              (call_script, "script_prop_instance_animate_to_position_with_childs", ":instance_id", 53,0,0),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
  ])

multiplayer_server_cannonball_flight = (
  0.125, 0, 0, [ (this_or_next|multiplayer_is_server),
                (neg|game_in_multiplayer_mode),
              ],
  [
    (set_fixed_point_multiplier, 100),
    
    (try_for_range,":cannonball_type", "spr_mm_cannonball_code_only_6pd", "spr_mm_cannon_12pdr_wood"),
      (try_for_prop_instances, ":ball_instance_id", ":cannonball_type", somt_temporary_object),
        (scene_prop_slot_eq, ":ball_instance_id", scene_prop_slot_in_use, 1), # ball is in use.

        (scene_prop_get_slot,":cur_x_vel",":ball_instance_id", scene_prop_slot_x_value),
        (scene_prop_get_slot,":cur_y_vel",":ball_instance_id", scene_prop_slot_y_value),
        (scene_prop_get_slot,":cur_z_vel",":ball_instance_id", scene_prop_slot_z_value),
        (scene_prop_get_slot,":time",":ball_instance_id", scene_prop_slot_time),
        (scene_prop_get_slot,":ammo_type",":ball_instance_id", scene_prop_slot_ammo_type),
        (scene_prop_get_slot,":user_agent",":ball_instance_id", scene_prop_slot_user_agent),
        
        (prop_instance_get_position, pos33, ":ball_instance_id"),
        (position_get_z, ":ball_z",pos33),
        
        # (assign,reg22,":cur_x_vel"),
        # (assign,reg23,":cur_y_vel"),
        # (assign,reg24,":cur_z_vel"),
        # (display_message,"@cur_x_vel: {reg22}  cur_y_vel: {reg23}  cur_z_vel: {reg24}"),
        
        (assign,":move",1),
        (assign,":check_walls",1),
        (assign,":check_agents",1),
        (copy_position,pos35,pos33),
        (copy_position,pos26,pos35),


        (try_begin),
          (gt,":time",0),
          
          (copy_position,pos34,pos33),
          (position_set_z_to_ground_level,pos34),
          (position_get_z,":ground_z",pos34),
          (val_add, ":ground_z", 10), 
          
          (this_or_next|lt,":ball_z", "$g_scene_water_level"),
          (lt,":ball_z", ":ground_z"),
          
          # Reset all rotations on pos34 except z
          (position_get_rotation_around_z, ":z_rot", pos34),
          (position_copy_origin,pos47,pos34),
          (init_position,pos34),
          (position_copy_origin,pos34,pos47),
          (position_rotate_z,pos34,":z_rot"),
          
          (try_begin), # Hitting the water?
            (lt,":ball_z", "$g_scene_water_level"), # we are underwater
            
            (gt,":ball_z", ":ground_z"), # we are undrerwater and not underground
            
            (scene_prop_slot_eq, ":ball_instance_id", scene_prop_slot_displayed_particle, 0), # shown the water effect already?
            (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_displayed_particle, 1),
            (copy_position,pos60,pos34), # pos60 is particle pos
            (position_set_z,pos60,"$g_scene_water_level"), # 0 = water level.
            
            (call_script,"script_multiplayer_server_play_hit_effect",cannon_hit_effect_event_type_water_ball, 0),
          (try_end),
         
          (lt,":ball_z", ":ground_z"),
          
          (assign,":clean_it_up",0),
          (try_begin),
            (this_or_next|eq,":ammo_type",cannon_ammo_type_shell),
            (this_or_next|eq,":ammo_type",cannon_ammo_type_bomb),
            (eq,":ammo_type",cannon_ammo_type_rocket),
            
            (copy_position,pos47,pos34),
            (call_script,"script_cannon_explosion_on_position",1,":ammo_type",":user_agent"),
            
            (assign,":clean_it_up",1),
          (else_try),
            (eq,":ammo_type",cannon_ammo_type_round),
            
            (call_script, "script_cannon_ball_hit_ground", ":ball_instance_id", ":cur_x_vel",":cur_z_vel"),
            (assign, ":cur_x_vel", reg0),
            (assign, ":cur_z_vel", reg1),
            (assign, ":clean_it_up", reg2),
          (try_end),
          
          (try_begin),
            (eq,":clean_it_up",1),
            
            (call_script, "script_clean_up_prop_instance", ":ball_instance_id"),
            
            (assign,":time",-1),
            (assign,":move",0),
            (assign,":check_walls",0),
            (assign,":check_agents",0),
          (try_end),
          
        (else_try),
          (assign, ":modulus", ":time"),
          
          (try_begin),
            (eq,":ammo_type",cannon_ammo_type_rocket),
            
            (val_mod, ":modulus", 2), # move and check once in 2 times (0.25 seconds)
          (else_try),
            (val_mod, ":modulus", 4), # move and check once in 4 times (0.5 seconds)
          (try_end),
          
          (gt, ":modulus", 0), # If not right mod result dont move. (1 == second value it will return so always move first pass :) )
          (assign,":move",0), # Dont move/check stuff just for ground detection...
        (try_end),

        # Copy ball pos when needed
        (store_mul,":z_offset_calc",":cur_z_vel",10000),
        (try_begin),
          (neq,":cur_x_vel",0),
          (val_div,":z_offset_calc",":cur_x_vel"),       
        (else_try),
          (val_div,":z_offset_calc",10000),      
        (try_end),
        
        (store_div,":x_movement",":cur_x_vel",2),
        (store_div,":y_movement",":cur_y_vel",2),
        (store_div,":z_movement",":cur_z_vel",2),
        
        (position_move_x,pos35,":x_movement"),
        (position_move_y,pos35,":y_movement"),
        (position_move_z,pos35,":z_movement"),
        
          
        (try_begin),
          (eq,":move",1),
          (set_fixed_point_multiplier, 100),
          
          (position_get_x,":ball_x",pos33),
          (position_get_y,":ball_y",pos33),
          
          (try_begin),
            (this_or_next|lt,":ball_x","$g_scene_min_x"),
            (this_or_next|gt,":ball_x","$g_scene_max_x"),
            (this_or_next|lt,":ball_y","$g_scene_min_y"),
            (gt,":ball_y","$g_scene_max_y"),
            
            (call_script, "script_clean_up_prop_instance", ":ball_instance_id"),
            (assign,":time",-1),
            (assign,":move",0),
            (assign,":check_walls",0),
            (assign,":check_agents",0),
          (else_try),
            # Animate first
            
            # (assign,reg29,":cur_x_vel"),
            # (assign,reg30,":cur_z_vel"),
            # (assign,reg31,":cur_y_vel"),
            # (display_message,"@at move;  cur_x_vel: {reg29}  cur_z_vel: {reg30}  cur_y_vel: {reg31}"),
            
            (position_move_x,pos33,":cur_x_vel"),
            (position_move_y,pos33,":cur_y_vel"),
            (position_move_z,pos33,":cur_z_vel"),
            
            (try_begin),
              (eq,":ammo_type",cannon_ammo_type_rocket),
              (try_begin),
                (ge,":time", 4),
                (store_random_in_range,":rand_z",-4,4),
                (position_rotate_z,pos33,":rand_z"),
                (store_random_in_range,":rand_y",-4,4),
                (position_rotate_y,pos33,":rand_y"),
              (try_end),
              (prop_instance_animate_to_position, ":ball_instance_id", pos33, 28),
            (else_try),
              (prop_instance_animate_to_position, ":ball_instance_id", pos33, 53),
            (try_end),
            
            (try_begin),
              (eq,":ammo_type",cannon_ammo_type_rocket),
              (try_begin),
                (le,":time", 28),
                (val_add, ":cur_x_vel", 150),
              (else_try),
                (val_mul, ":cur_x_vel", 99), 
                (val_div, ":cur_x_vel", 100), # value * 99 / 100 = - 99% of speed due to friction per 0.5 sec so 2% friction per second
              (try_end),
              (try_begin),
                (gt,":time",4),
                (val_sub,":cur_z_vel", 59), 
              (try_end),
            (else_try),
              # Then apply gravity and friction
              ## -196 cm per second so # 0.981 per half
              (val_sub,":cur_z_vel", 118), 
              (val_max,":cur_z_vel",-1700),
              (val_mul, ":cur_x_vel", 99), 
              (val_div, ":cur_x_vel", 100), # value * 99 / 100 = - 99% of speed due to friction per 0.5 sec so 2% friction per second
            (try_end),
            
            (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_x_value, ":cur_x_vel"),
            (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_y_value, ":cur_y_vel"),
            (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_z_value, ":cur_z_vel"),
          (try_end),
        (try_end),
        
        (val_add,":time",1),
        (scene_prop_set_slot, ":ball_instance_id", scene_prop_slot_time, ":time"),
        
        (eq,":move",1), # Only check stuff when just moved.
        
        
        (assign,":hitted_wall_x_dist",":cur_x_vel"),
                
        (try_begin), # destroy those bloody walls bitch..
          #(gt,":time",0),
          (eq,":check_walls",1), # not the first time so dont destroy your defence walls..
          (assign,":min_dist",9999999999),
          (assign,":hitted_wall_instance",-1),
          #(assign,":hitted_length_div2",0),
          (assign,":hitted_wall_kind",-1),
          (assign,":hitted_wall_power",3),
          (assign,":hitted_distance_ball_wall",0),
          (store_mul,":cur_x_vel_min",":cur_x_vel",-1),
          (try_for_range,":wall_type",mm_destructible_props_begin,mm_destructible_props_end),
            
            (assign,":wall_power", 3),
            #(try_begin),
             # (this_or_next|is_between, ":wall_type", "spr_mm_stakes","spr_mm_destructible_pioneer_builds_end"), #patch1115 fix 35/1 removed
             # (eq,":wall_type","spr_mm_dummy"),
            #  (assign,":wall_power",1),
           # (try_end),
            
            (try_for_prop_instances, ":wall_id", ":wall_type"),
              (prop_instance_get_position, pos40, ":wall_id"),
              
              (scene_prop_get_slot,":max_length",":wall_id", scene_prop_slot_destruct_max_length),
              (store_add,":cur_x_vel_awall", ":x_movement", ":max_length"),
              
              # only get shit that is close to this ball middle position.
              (get_distance_between_positions, ":distance_ball_wall", pos35, pos40),
              (le, ":distance_ball_wall", ":cur_x_vel_awall"),
              
              # We are close enough, optimization done, lets get the real stuff about this prop.
              (call_script,"script_get_prop_center",":wall_id"),
              (eq,reg1,1), # is ok :)
              (scene_prop_get_slot,":cur_wall_height",":wall_id",scene_prop_slot_destruct_wall_height),
              (scene_prop_get_slot,":cur_wall_width",":wall_id",scene_prop_slot_destruct_wall_width),
              (scene_prop_get_slot,":cur_wall_length",":wall_id",scene_prop_slot_destruct_wall_length),

              (assign,":cur_wall_width_usa",":cur_wall_width"),
              
              (copy_position,pos40,pos42), 
              
              (set_fixed_point_multiplier, 1000),
              # resize for the angle of wall
              (get_angle_between_positions, ":rotation", pos33, pos40),
              # get length
              (store_cos, ":cos_of_rotation", ":rotation"),
              (try_begin), # make it positive if needed
                (lt, ":cos_of_rotation", 0),
                (val_mul, ":cos_of_rotation", -1),
              (try_end),
              (val_mul,":cur_wall_length",":cos_of_rotation"),
              (val_div, ":cur_wall_length", 1000),
              # get width
              (store_sub, ":cos_of_rotation", 1000, ":cos_of_rotation"), # get remainder
              (val_mul,":cur_wall_width",":cos_of_rotation"),
              (val_div, ":cur_wall_width", 1000),
              
              # Put length + width together
              (val_add, ":cur_wall_length", ":cur_wall_width"),
              
              
              # prepare vars for compare against ball pos
              (set_fixed_point_multiplier, 100),
              (store_div, ":length_div2", ":cur_wall_length", 2),
              (store_div, ":height_div2", ":cur_wall_height", 2),
              (store_mul, ":length_div2_min", ":length_div2", -1),
              (store_mul, ":height_div2_min", ":height_div2", -1),              
              
              (position_transform_position_to_local,pos45,pos26,pos40),
              (position_get_x,":x_value",pos45),
              (position_get_y,":y_value",pos45),
              (position_get_z,":z_value",pos45),
              
              (is_between,":y_value",":length_div2_min",":length_div2"), # Length 
              (is_between,":x_value",-50,":cur_x_vel"), #  50 cm before and speed after the path of the ball. (due to lag..)
              
              (store_mul,":z_offset",":z_offset_calc",":x_value"),
              (val_div,":z_offset",10000), # zoffset is clear.
              (val_add,":height_div2",":z_offset"),
              (val_add,":height_div2_min",":z_offset"),
              
              (is_between,":z_value",":height_div2_min",":height_div2"), # height
              
              # is hit.
              # then, check if its the closest one, using agent position due to you want to hit the first thing comming from x direction.
              (try_begin),
                (agent_is_active,":user_agent"),
                (agent_get_position,pos56,":user_agent"),
                (get_distance_between_positions, ":distance_ball_wall", pos56, pos40),
              (try_end),
              (this_or_next|eq,":hitted_wall_instance",-1),
              (lt,":distance_ball_wall",":min_dist"),
              (assign,":min_dist",":distance_ball_wall"),
              (assign,":hitted_wall_instance",":wall_id"),
              (assign,":hitted_wall_x_dist",":x_value"),
              #(assign,":hitted_length_div2",":length_div2"),
              (store_div,":hitted_width_div2", ":cur_wall_width_usa", 2),
              (assign,":hitted_wall_kind",":wall_type"),
              (assign,":hitted_wall_power",":wall_power"),
              
              (copy_position,pos45,pos33),
              (position_move_x,pos45,":cur_x_vel_min"),
              (get_distance_between_positions, ":hitted_distance_ball_wall", pos45, pos40),
              (copy_position,pos47,pos40),
            (try_end),
          (try_end),
          

          (try_begin), # we have something hit.
           # (gt,":hitted_wall_instance", -1),
            (prop_instance_is_valid,":hitted_wall_instance"), #patch1115 18/25
            
            (copy_position,pos45,pos33),
            (position_move_x,pos45,":cur_x_vel_min"),
            
            
            # copy ball to a temp pos. (for its rotations.
            
            #            85%
            # (val_mul,":hitted_length_div2",85),
            # (val_div,":hitted_length_div2",100),
            
            (val_sub,":hitted_distance_ball_wall",":hitted_width_div2"),
            (position_move_x,pos45,":hitted_distance_ball_wall"),
            
            (position_get_z,":wall_middle_z",pos47),
            
            (store_random_in_range,":random_z_add",-100,101),
            (val_add,":wall_middle_z",":random_z_add"),
            
            (position_set_z,pos45,":wall_middle_z"),
            #(position_rotate_y,pos45,90),
            
            
            # place wall xyz into the rotation of ball.
            #(position_copy_origin,pos45,pos47),
            # flip the position
            # (position_rotate_x,pos45,180),
            # (position_move_x,pos45,":hitted_length_div2"),
            (copy_position,pos47,pos45),
            
            (try_begin),
              (this_or_next|eq,":ammo_type",cannon_ammo_type_shell),
              (this_or_next|eq,":ammo_type",cannon_ammo_type_bomb),
              (eq,":ammo_type",cannon_ammo_type_rocket),
              
              (call_script,"script_cannon_explosion_on_position",0,":ammo_type",":user_agent"),
              
              (call_script, "script_clean_up_prop_instance", ":ball_instance_id"), # clean up ball
              (assign,":check_agents",0),
            (else_try),
              (eq,":ammo_type",cannon_ammo_type_round),
              
              (try_begin),
                (this_or_next|is_between, ":hitted_wall_kind", "spr_fortnew", "spr_mm_new_wall_1_1"), #patch1115 fix 38/1
                (eq, ":hitted_wall_kind", "spr_mm_ship_schooner"),  
                (call_script,"script_deliver_damage_to_prop",":hitted_wall_instance",201, 1, ":user_agent"),
              (else_try),
                (call_script,"script_deliver_damage_to_prop",":hitted_wall_instance",201, 0, ":user_agent"),
              (try_end),
              
              (scene_prop_get_slot,":ball_times_hit",":ball_instance_id", scene_prop_slot_times_hit),
              (val_add, ":ball_times_hit", ":hitted_wall_power"),
              
              (try_begin),
                (ge, ":ball_times_hit", 3),
                #Clean up ball
                (call_script, "script_clean_up_prop_instance", ":ball_instance_id"),
               # (assign,":check_agents",0),
              (else_try),
                # hit something, loosing speed.
                (val_mul, ":cur_x_vel", 90), 
                (val_div, ":cur_x_vel", 100), # value * 90 / 100 = - 90% speed left
                (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_x_value, ":cur_x_vel"),
                (scene_prop_set_slot,":ball_instance_id", scene_prop_slot_times_hit, ":ball_times_hit"),
              (try_end),
            (try_end),
          (try_end),
        (try_end), 
        #(gt,":time",1),
        (eq, ":check_agents", 1),
	    	(neq,":ammo_type",cannon_ammo_type_bomb),
        (set_fixed_point_multiplier, 100),
        
        
        # get the Z offset by knowing the Z mov per x mov. (fixed point * 10000)
        
        (assign,":myhorseid",-1),
        (try_begin),
          (agent_is_active, ":user_agent"),
          (agent_get_horse,":myhorseid",":user_agent"),
        (try_end),
        
        

        (store_add,":check_range",":x_movement",120),
        

        
        (try_for_agents, ":cur_agent",pos35,":check_range"),
          (eq, ":check_agents", 1),
          (agent_is_active, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_position, pos40, ":cur_agent"),
          
          (assign,":z_mov",90),
          (assign,":z_size",90),
          (assign,":y_width",70),
          (assign,":whores",-1),
          (try_begin),
            (agent_is_human,":cur_agent"),
            (try_begin),
              (agent_get_horse,":whores",":cur_agent"),
              (gt,":whores",-1),
              (assign,":z_mov",130),
              (assign,":z_size",80),
            (else_try),
              (agent_get_animation,":cur_anim",":cur_agent",0),
              (eq,":cur_anim","anim_stand_to_crouch"),
              (assign,":z_mov",50),
              (assign,":z_size",50),
            (try_end),
          (else_try), # horse.
          
            (assign,":y_width",150),
            (assign,":cur_wall_width",70),
            
            # resize for the angle of horse
            (set_fixed_point_multiplier, 1000),
            (get_angle_between_positions, ":rotation", pos33, pos40),
            (store_cos, ":cos_of_rotation", ":rotation"),
            (try_begin), # make it positive if needed
              (lt, ":cos_of_rotation", 0),
              (val_mul, ":cos_of_rotation", -1),
            (try_end),
            (val_mul,":y_width",":cos_of_rotation"),
            (val_div, ":y_width", 1000),
            
            (store_sub, ":sin_of_rotation", 1000, ":cos_of_rotation"), # get remainder
            (val_mul,":cur_wall_width",":sin_of_rotation"),
            (val_div, ":cur_wall_width", 1000),

            # Put length + width together
            (val_add, ":y_width", ":cur_wall_width"),
            (set_fixed_point_multiplier, 100),
            
            (assign,":z_mov",110),
            (assign,":z_size",110),
          (try_end),
          
          (position_move_z,pos40,":z_mov"),
          
          (position_transform_position_to_local,pos45,pos26,pos40),
          (position_get_x,":x_value",pos45),
          (position_get_y,":y_value",pos45),
          (position_get_z,":z_value",pos45),
          
          (assign,":x_min",-50),
          (try_begin),
            (le,":time",1),
            (this_or_next|eq,":cur_agent",":user_agent"),
            (eq,":myhorseid",":user_agent"),
            (assign,":x_min",":hitted_wall_x_dist"),
          (try_end),
          
          (is_between,":x_value",":x_min",":hitted_wall_x_dist"), # 0.5 meters after + speed before the path of the ball.
          
          (store_add,":y_test",":y_width",1),
          (store_mul,":min_y_test",":y_test",-1),
          
          (is_between,":y_value",":min_y_test",":y_test"), # width 50 cm each side so a meter wide we hit him
          
         
          
          (store_add,":z_test",":z_size",15),
          (store_mul,":min_z_test",":z_test",-1),
          (val_add,":z_test",20),
          (store_mul,":z_offset",":z_offset_calc",":x_value"),
          (val_div,":z_offset",10000), # zoffset is clear.
          (val_add,":z_test",":z_offset"),
          (val_add,":min_z_test",":z_offset"),
          
          
          # (assign,reg21,":cur_agent"),
           # (assign,reg22,":x_value"),
           # (assign,reg24,":z_value"),
           # (assign,reg25,":cur_x_vel"),
           # (assign,reg27,":cur_z_vel"),
           # (assign,reg28,":z_offset"),
           
           # (display_message,"@cur_agent:{reg21}  x_value: {reg22}  z_value: {reg24}  ball_x_vel: {reg25}  ball_z_vel: {reg27}  z_offset: {reg28}"),
          
          
          (is_between,":z_value",":min_z_test",":z_test"),#,-110,121), # height 2 meter man + 20 for correction
          
          
          (try_begin),
            (this_or_next|eq,":ammo_type",cannon_ammo_type_shell),
            (eq,":ammo_type",cannon_ammo_type_rocket),
            (copy_position,pos47,pos40),
            
            (call_script,"script_cannon_explosion_on_position",0,":ammo_type",":user_agent"),
            
            (call_script, "script_clean_up_prop_instance", ":ball_instance_id"), # clean up ball
            (assign, ":check_agents", 0),
          (else_try),
            (eq,":ammo_type",cannon_ammo_type_round),
          
            (assign, ":killer_agent", 0),
            (try_begin),
              (agent_is_active,":user_agent"),
              (assign, ":killer_agent", ":user_agent"),
            (else_try),
              (assign, ":killer_agent", ":cur_agent"),
            (try_end),
            #(agent_set_hit_points, ":cur_agent", 0, 1),
            #(agent_deliver_damage_to_agent, ":killer_agent", ":cur_agent", 1),
            (agent_deliver_damage_to_agent_advanced, ":unused", ":killer_agent", ":cur_agent", 200,"itm_cannon_ball_dummy"),
            (particle_system_burst,"psys_cannon_blood",pos40,100),
            (particle_system_burst,"psys_cannon_blood_2",pos40,100),
                                 
            # Play hitsound
            (copy_position,pos56,pos40),
            (call_script,"script_multiplayer_server_play_sound_at_position","snd_cannon_hit"),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
  ])
    
multiplayer_server_drowning = (   # Drowning and wet powder script
  1.1, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
    (set_fixed_point_multiplier, 100),
    (try_for_agents, ":cur_agent"),
      (agent_is_active,":cur_agent"),
      (agent_is_alive,":cur_agent"),
      (agent_get_position,pos16,":cur_agent"),
      (position_get_z,":cur_z",pos16),
      
      (lt,":cur_z","$g_scene_water_level"), # optimizee
      
      (agent_get_animation,":cur_anim",":cur_agent",0),
      (try_begin),
        (eq,":cur_anim","anim_stand_to_crouch"),
        (val_sub,":cur_z",56),
      (else_try),
        (agent_get_horse, ":agent_horse", ":cur_agent"),
        (agent_is_active, ":agent_horse"), #PATCH1115 fix 5/2
        (agent_is_alive,":agent_horse"),
        (val_add,":cur_z",80),
      (try_end),
      
      (store_sub,":test_water_level","$g_scene_water_level",104),
      (try_begin),
        (lt,":cur_z",":test_water_level"),
        (agent_unequip_item,":cur_agent","itm_bullets"),
        (agent_unequip_item,":cur_agent","itm_pistol_ammo"),
      (try_end),
      
      (agent_get_slot, ":underwater_time", ":cur_agent", slot_agent_underwater_time),
      (store_sub,":test_water_level","$g_scene_water_level",160),
      (try_begin),
        (lt,":cur_z",":test_water_level"),
        
        (try_begin), # stop music if underwater.
          (call_script,"script_cf_agent_is_playing_music",":cur_agent"),
          (call_script,"script_multiplayer_server_agent_stop_music", ":cur_agent"),
        (try_end),
        
        (val_sub,":underwater_time",1),
        (try_begin),
          (try_begin),
            (agent_slot_eq,":cur_agent",slot_agent_underwater_now,0),
            (agent_set_slot, ":cur_agent", slot_agent_underwater_now, 1),
          (try_end),
          (eq, ":underwater_time", 0),
          (store_agent_hit_points, ":current_hp_perc", ":cur_agent", 0),
          (val_sub, ":current_hp_perc", 5),
          (agent_set_hit_points,":cur_agent", ":current_hp_perc", 0),
          (agent_deliver_damage_to_agent, ":cur_agent", ":cur_agent", 1,"itm_drown_dummy"),
          (try_begin),
            (gt,":current_hp_perc",0), # play some hit sounds :)
            
            # pos56 is sound pos.
            (copy_position,pos56,pos16),
            (try_begin), 
              (neg|agent_is_human,":cur_agent"),
              (call_script,"script_multiplayer_server_play_sound_at_agent","snd_neigh",":cur_agent"),
            (else_try),
              (call_script,"script_multiplayer_server_play_sound_at_position","snd_drown"),
            (try_end),
          (try_end),
        (else_try),
          (agent_set_slot, ":cur_agent", slot_agent_underwater_time, ":underwater_time"),
        (try_end),
      (else_try),
        (lt, ":underwater_time", 8),
        
        (try_begin), # comming up.
          (agent_slot_eq,":cur_agent",slot_agent_underwater_now,1),
          (agent_set_slot, ":cur_agent", slot_agent_underwater_now, 0),
          (agent_is_human,":cur_agent"),
          (copy_position,pos56,pos16),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_come_up"),
        (try_end),
        
        (val_add, ":underwater_time", 4),
        (agent_set_slot, ":cur_agent", slot_agent_underwater_time, ":underwater_time"),
      (try_end),
    (try_end),
  ])
  
multiplayer_client_drowning = (   # Drowning sound for client
  0.5, 0, 0, [(neg|multiplayer_is_dedicated_server)],
  [
    (set_fixed_point_multiplier, 100),
    
    # (assign,":max_id",0),
    # (try_for_agents,":agentid"),
      # (gt,":agentid",":max_id"),
      # (assign,":max_id",":agentid"),
    # (try_end),
    # (assign,reg25,":max_id"),
    # (display_message,"@max_id: {reg25}"),
    
    # (try_begin),
      # (multiplayer_get_my_player,":my_player"),
      # (player_is_active,":my_player"),
      # (player_get_agent_id,":my_agent",":my_player"),
      # (agent_is_active,":my_agent"),
      # (agent_is_alive,":my_agent"),
      
      # (agent_get_position,pos9,":my_agent"),
      # (set_fixed_point_multiplier,100),
      # (position_get_x,reg22,pos9),
      # (position_get_y,reg23,pos9),
      # (position_get_z,reg24,pos9),
    
      # (display_message,"@CurX: {reg22}  CurY: {reg23}  CurZ: {reg24}"),
     
    # (try_end),
    
    
    # (assign,":max_propid",0),
    # (assign,":objectcount",0),
    # (assign,":max_scale",0),
    # (assign,":prop_kind",-1),
    
    # (try_for_range,":prop_type", "spr_invalid_object", "spr_scene_props_end"),
      # (try_for_prop_instances, ":cur_instance_id", ":prop_type"),
        # (val_add,":objectcount",1),
        
        # (try_begin),
          # (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_is_scaled,1), # is scaled.
           
          # (assign,":old_max_scale",":max_scale"),
          
          # (scene_prop_get_slot,":x_scale",":cur_instance_id",scene_prop_slot_x_scale),
          # (try_begin),
            # (gt,":x_scale",":max_scale"),
            # (assign,":max_scale",":x_scale"),
            # (prop_instance_get_scene_prop_kind, ":prop_kind", ":cur_instance_id"),
          # (try_end),
          # (scene_prop_get_slot,":y_scale",":cur_instance_id",scene_prop_slot_y_scale),
          # (try_begin),
            # (gt,":y_scale",":max_scale"),
            # (assign,":max_scale",":y_scale"),
            # (prop_instance_get_scene_prop_kind, ":prop_kind", ":cur_instance_id"),
          # (try_end),
          # (scene_prop_get_slot,":z_scale",":cur_instance_id",scene_prop_slot_z_scale),
          # (try_begin),
            # (gt,":z_scale",":max_scale"),
            # (assign,":max_scale",":z_scale"),
            # (prop_instance_get_scene_prop_kind, ":prop_kind", ":cur_instance_id"),
          # (try_end),
          
          # (neq,":old_max_scale",":max_scale"),
          
          # (val_clamp,":x_scale",0,65535),
          # (val_clamp,":y_scale",0,65535),
          # (val_clamp,":z_scale",0,32767),
          
          # # pack
          # (assign,":sendvar1",":cur_instance_id"),
          # (val_lshift, ":sendvar1", 16), 
          # (val_add,":sendvar1",":x_scale"),
          # (assign,":sendvar2",":z_scale"),
          # (val_lshift, ":sendvar2", 16), 
          # (val_add,":sendvar2",":y_scale"),
          
          # # unpack
          # (store_and,":new_x_scale",":sendvar1",65535),
          # (store_and,":new_y_scale",":sendvar2",65535),
          # (val_rshift, ":sendvar1", 16), 
          # (assign,":new_instance",":sendvar1"),
          # (val_rshift, ":sendvar2", 16), 
          # (assign,":new_z_scale",":sendvar2"),
          
          # (this_or_next|neq,":new_instance",":cur_instance_id"),
          # (this_or_next|neq,":new_x_scale",":x_scale"),
          # (this_or_next|neq,":new_y_scale",":y_scale"),
          # (neq,":new_z_scale",":z_scale"),
          
          # (assign,reg22,":new_instance"),
          # (assign,reg23,":cur_instance_id"),
          # (assign,reg24,":new_x_scale"),
          # (assign,reg25,":x_scale"),
          # (assign,reg26,":new_y_scale"),
          # (assign,reg27,":y_scale"),
          # (assign,reg28,":new_z_scale"),
          # (assign,reg29,":z_scale"),
          # (display_message,"@error! new_instance:{reg22} cur_instance_id:{reg23} new_x_scale:{reg24} x_scale:{reg25} new_y_scale:{reg26} y_scale:{reg27} new_z_scale:{reg28} z_scale:{reg29}"),
        # (try_end),
        
        # (gt,":cur_instance_id",":max_propid"),
        # (assign,":max_propid",":cur_instance_id"),
      # (try_end),
    # (try_end),
    
    # (assign,reg22,":max_propid"),
    # (assign,reg23,":objectcount"),
    # (assign,reg24,":max_scale"),
    # (assign,reg25,":prop_kind"),
    # (display_message,"@max_propid: {reg22}  objectcount: {reg23}   max_scale: {reg24}   prop_kind: {reg25}"),
    
    
    (call_script, "script_client_get_my_agent"),
    (assign,":player_agent",reg0),
    
    (try_begin),
      (agent_is_active,":player_agent"),
      (agent_is_alive,":player_agent"),
      
      (agent_get_position,pos16,":player_agent"),
      (position_get_z,":agent_z",pos16),
      
      # performance check
      (lt,":agent_z","$g_scene_water_level"),
      
      (agent_get_animation,":cur_anim",":player_agent",0),
      (try_begin),
        (eq,":cur_anim","anim_stand_to_crouch"),
        (val_sub,":agent_z",56),
      (else_try),
        (agent_get_horse, ":agent_horse", ":player_agent"),
        (gt, ":agent_horse", 0),
        (val_add,":agent_z",80),
      (try_end),
      
      (store_sub,":test_water_level","$g_scene_water_level",160),
      
      (try_begin),
        (lt,":agent_z",":test_water_level"),
        (try_begin),
          (eq, "$g_client_drown_sound_channel", -1),
          (play_sound,"snd_underwater_noise"),
          (store_last_sound_channel, "$g_client_drown_sound_channel"),
        (try_end),
      (else_try),
        (gt, "$g_client_drown_sound_channel", -1),
        (stop_sound_channel, "$g_client_drown_sound_channel"),
        (assign,"$g_client_drown_sound_channel",-1),
      (try_end),
    (try_end),
  ])
    
multiplayer_client_music_and_sapper = ( # Also for Sapper construction # and rocket placement.
  0, 0, 0, [(neg|multiplayer_is_dedicated_server),(game_key_clicked, gk_defend),], #gk_party_window
  [
    (try_begin),
      (call_script, "script_client_get_my_agent"),
      (assign, ":player_agent", reg0),
      
      (agent_is_active,":player_agent"),
      (agent_is_alive, ":player_agent"), # Still alive?
      
      (try_begin), # stop playing piano
        (call_script,"script_cf_agent_is_playing_piano",":player_agent"),

        (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_music, music_type_stop),
      (else_try),
        (call_script,"script_cf_agent_is_taking_a_shit",":player_agent"),
        
        (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_music, music_type_stop),
      (else_try),
        (call_script,"script_cf_agent_is_surrendering",":player_agent"),
        
        (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_surrender, music_type_stop),
      (else_try),
        (agent_get_troop_id,":player_troop",":player_agent"),
        
        (troop_get_slot,":player_class",":player_troop",slot_troop_class),
        (troop_get_slot,":player_rank",":player_troop",slot_troop_rank),

        (agent_get_wielded_item,":item_id",":player_agent",0),
        (ge, ":item_id", 0),
         
        (try_begin),
          (eq,":player_class",multi_troop_class_mm_sapper),
          (is_between,":item_id","itm_construction_hammer","itm_shovel"), #Hammer
          (neg|is_presentation_active, "prsnt_multiplayer_construct"),
          (start_presentation,"prsnt_multiplayer_construct"),
        (else_try),
          (eq,":player_rank",mm_rank_musician),
        
          (is_between, ":item_id", "itm_drumstick_right", "itm_bullets"), # an instrument
     
          (try_begin),
            (call_script,"script_cf_agent_is_playing_music",":player_agent"),
            (neg|is_presentation_active, "prsnt_multiplayer_music"),
            
            (try_begin),
              (store_mission_timer_a,":cur_time"),
              (store_sub, ":elapsed_time", ":cur_time", "$g_started_playing_music_at"),
              
              (lt,":elapsed_time",2),
            (else_try),
              (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_music, music_type_stop),
            (try_end),
          (else_try),
            (neg|is_presentation_active, "prsnt_multiplayer_music"),
            (start_presentation,"prsnt_multiplayer_music"),
          (try_end),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_rocket),
          
          (eq,":item_id", "itm_rocket_placement"),
          
          (multiplayer_send_int_to_server, multiplayer_event_send_player_action, player_action_place_rocket),
        (try_end),
      (try_end),
    (try_end),
  ])

multiplayer_client_surrender = (
  0, 0.5, 0.1, [
  (neg|multiplayer_is_dedicated_server),
  (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
  (neg|is_presentation_active, "prsnt_game_multiplayer_admin_panel"),
  (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"), #custom_chat:
  (game_key_clicked,gk_party_window),
  
  (try_begin),
    (call_script,"script_client_get_my_agent"),
    (assign,":agent_id",reg0),
    (agent_is_active,":agent_id"),
    (agent_is_alive,":agent_id"),
    (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_surrender,music_type_start),
    
    (multiplayer_send_2_int_to_server,multiplayer_event_send_player_action,player_action_voice,voice_type_surrender),
  (try_end),
  ],
  [
    (try_begin),
      (call_script,"script_client_get_my_agent"),
      (assign,":agent_id",reg0),
      (agent_is_active,":agent_id"),
      (agent_is_alive,":agent_id"),
      (multiplayer_send_2_int_to_server, multiplayer_event_send_player_action, player_action_surrender,music_type_start),
      
    (try_end),
  ])
  

multiplayer_server_bonuses = ( # Officer and flag Bonuses
  4.31, 0, 0, [(multiplayer_is_server),(eq,"$g_bonuses_enabled",1)],
  [
    (set_fixed_point_multiplier,100),
  
    (store_mul,":bonus_value_10",10,"$g_bonus_strength"),
    (val_div,":bonus_value_10",100),
    (store_mul,":bonus_value_5",5,"$g_bonus_strength"),
    (val_div,":bonus_value_5",100),
    (store_mul,":bonus_value_3",3,"$g_bonus_strength"),
    (val_div,":bonus_value_3",100),
    
    (store_mul,":max_search_range","$g_bonus_range",150),# to meters + 50%
     
    (try_for_players, ":player_id", "$g_ignore_server"),
      (player_is_active, ":player_id"),
      (player_get_agent_id, ":player_agent_id", ":player_id"),
    #(try_for_agents, ":player_agent_id"),
      (agent_is_active,":player_agent_id"),
      (agent_is_alive, ":player_agent_id"),
      #(agent_is_human,":player_agent_id"),
      (agent_get_troop_id,":player_troop_id",":player_agent_id"),
      (troop_get_slot,":player_class",":player_troop_id",slot_troop_class_type),
      (troop_get_slot,":player_rank",":player_troop_id",slot_troop_rank),
      
      (this_or_next|eq,":player_rank",mm_rank_ranker), #Only apply bonuses to rankers
      #Cavalry and skirmishers might get speed bonuses that apply to all ranks
      (this_or_next|eq,":player_class",multi_troop_class_mm_cavalry),
      (this_or_next|eq,":player_class",multi_troop_class_mm_artillery),#lets allow all the arty units to have the bonus  hotfix
      (eq,":player_class",multi_troop_class_mm_skirmisher),
      
      (agent_get_team,":player_team",":player_agent_id"),
      (agent_get_position,pos27,":player_agent_id"), #pos27 holds player position
      
      (assign,":affected_by_num_captains",0),
      (assign,":affected_by_num_flags",0),
      (assign,":affected_by_num_sergeants",0),
      (assign,":affected_by_num_musicians",0),
      (assign,":affected_by_num_generals",0),
      # (try_for_players, ":player_id_2", "$g_ignore_server"),
        # (player_is_active, ":player_id_2"),
        # (player_get_agent_id, ":cur_agent", ":player_id_2"),'
      (try_for_agents, ":cur_agent",pos27,":max_search_range"), 
        (agent_is_active,":cur_agent"),
        (agent_is_alive,":cur_agent"),
        (agent_is_human,":cur_agent"),
        
        (agent_get_team,":cur_team",":cur_agent"),
        (eq,":cur_team",":player_team"),
        
        
        (agent_get_position,pos4,":cur_agent"),
        (get_distance_between_positions_in_meters,":dist",pos4,pos27),
        
        (agent_get_troop_id,":cur_troop",":cur_agent"),
        (troop_get_slot,":cur_agent_rank",":cur_troop",slot_troop_rank),
				(troop_get_slot,":cur_agent_class",":cur_troop",slot_troop_class_type),
        (assign,":max_range","$g_bonus_range"),
				
        (try_begin), # for generals and cav, add moar.  cav fight more spread out, so extra range will help
				  (eq,":cur_agent_class",multi_troop_class_mm_cavalry),
					(this_or_next|eq,":cur_agent_rank",mm_rank_officer),	
					(this_or_next|eq,":cur_agent_rank",mm_rank_sergeant),
          (eq,":cur_agent_rank",mm_rank_musician),					
					(val_mul,":max_range",12),
          (val_div,":max_range",10),

			  (else_try),
          (eq,":cur_agent_rank",mm_rank_general), 

          (val_mul,":max_range",15),
          (val_div,":max_range",10),				  
        (try_end),
        (le,":dist",":max_range"),
        
        #(troop_get_slot,":cur_agent_class",":cur_troop",slot_troop_class_type),
        
        (this_or_next|eq,":cur_agent_class",":player_class"), #Only affected by same class
        (eq,":cur_agent_rank",mm_rank_general),               #Or generals
        
        (try_begin),
          (eq,":cur_agent_rank",mm_rank_officer),
          (val_add,":affected_by_num_captains",1),
        (else_try),
          (eq,":cur_agent_rank",mm_rank_musician),
          (call_script,"script_cf_agent_is_playing_music",":cur_agent"),
          (val_add,":affected_by_num_musicians",1),
        (else_try),
          (eq,":cur_agent_rank",mm_rank_general),
          (val_add,":affected_by_num_generals",1),
        (else_try),
          (agent_get_wielded_item,":item_id",":cur_agent",0),
          (ge,":item_id",0),
          (item_slot_eq,":item_id",slot_item_multiplayer_item_class, multi_item_class_type_flag),
          (val_add,":affected_by_num_flags",1),
        (else_try),
          (eq,":cur_agent_rank",mm_rank_sergeant),
          (val_add,":affected_by_num_sergeants",1),
        (try_end),
      (try_end),    
      
      (assign,":mod_damage",100),
      (assign,":mod_accuracy",100),
      (assign,":mod_speed",100),
      (assign,":mod_speed_2",100),
      (assign,":mod_reload_speed",100),
      (assign,":mod_use_speed",100),
      (try_begin),
        (gt,":affected_by_num_captains",0),
        (try_begin),
          (this_or_next|eq,":player_class",multi_troop_class_mm_infantry),
          (eq,":player_class",multi_troop_class_mm_skirmisher),
          (eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_5"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_3"),
          (try_end),
          (val_add,":mod_accuracy",":bonus_value"),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_cavalry),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_3"),
          (try_end),
          (val_add,":mod_speed_2",":bonus_value"),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_artillery),
          #(eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_5"),
          (try_end),
          (val_add,":mod_use_speed",":bonus_value"),
        (try_end),
      (try_end),
      (try_begin),
        (gt,":affected_by_num_flags",0),
        (try_begin),
          (this_or_next|eq,":player_class",multi_troop_class_mm_infantry),
          (eq,":player_class",multi_troop_class_mm_cavalry),
          (eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_5"),
          (try_end),
          (val_add,":mod_damage",":bonus_value"),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_skirmisher),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_5"),
          (try_end),
          (val_add,":mod_speed",":bonus_value"),
        (try_end),
      (else_try),
        (gt,":affected_by_num_sergeants",0),
        (try_begin),
          (this_or_next|eq,":player_class",multi_troop_class_mm_infantry),
          (eq,":player_class",multi_troop_class_mm_cavalry),
          (eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_5"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_3"),
          (try_end),
          (val_add,":mod_damage",":bonus_value"),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_skirmisher),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_5"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_3"),
          (try_end),
          (val_add,":mod_speed",":bonus_value"),
        (try_end),
      (try_end),
      (try_begin),
        (gt,":affected_by_num_musicians",0),
        (try_begin),
          (this_or_next|eq,":player_class",multi_troop_class_mm_infantry),
          (eq,":player_class",multi_troop_class_mm_skirmisher),
          (eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_musicians",1), #More than 1 musician
            (val_add,":bonus_value",":bonus_value_5"), #50% more bonus
          (try_end),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_5"),
          (try_end),
          (val_add,":mod_reload_speed",":bonus_value"),
        (else_try),
          (eq,":player_class",multi_troop_class_mm_cavalry),
          (eq,":player_rank",mm_rank_ranker),
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_generals",0),
            (val_add,":bonus_value",":bonus_value_5"),
          (try_end),
          (val_add,":mod_damage",":bonus_value"),
        (try_end),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":player_agent_id", slot_agent_cur_damage_modifier, ":mod_damage"),
        (agent_set_damage_modifier, ":player_agent_id", ":mod_damage"), # value is in percentage, 100 is default
        (agent_set_slot, ":player_agent_id", slot_agent_cur_damage_modifier, ":mod_damage"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":player_agent_id", slot_agent_cur_accuracy_modifier, ":mod_accuracy"),
        (agent_set_accuracy_modifier, ":player_agent_id", ":mod_accuracy"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":player_agent_id", slot_agent_cur_accuracy_modifier, ":mod_accuracy"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":player_agent_id", slot_agent_cur_reload_speed_modifier, ":mod_reload_speed"),
        (agent_set_reload_speed_modifier, ":player_agent_id", ":mod_reload_speed"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":player_agent_id", slot_agent_cur_reload_speed_modifier, ":mod_reload_speed"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":player_agent_id", slot_agent_cur_use_speed_modifier, ":mod_use_speed"),
        (agent_set_use_speed_modifier, ":player_agent_id", ":mod_use_speed"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":player_agent_id", slot_agent_cur_use_speed_modifier, ":mod_use_speed"),
      (try_end), 
      (try_begin), #Apply speed bonuses to the horse of mounted players
        (agent_get_horse,":horse",":player_agent_id"),
        (gt,":horse",-1),
        (try_begin),
          #(neg|agent_slot_eq, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
          #(agent_set_speed_modifier, ":horse", ":mod_speed_2"),
          #(agent_set_slot, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
					(neg|agent_slot_eq, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
          (agent_set_horse_speed_factor, ":player_agent_id", ":mod_speed_2"),
          (agent_set_slot, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
        (try_end),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":player_agent_id", slot_agent_god_mode, 1),
        (neg|agent_slot_eq,":player_agent_id",slot_agent_base_speed_mod,55),# walking
				(neg|agent_slot_eq,":player_agent_id",slot_agent_base_speed_mod,":mod_speed"),
        #(neg|agent_slot_eq, ":player_agent_id", slot_agent_cur_speed_modifier, ":mod_speed"),
        (agent_set_speed_modifier, ":player_agent_id", ":mod_speed"), # value is in percentage, 100 is default, value can be between [0..1000]
        #(agent_set_slot, ":player_agent_id", slot_agent_cur_speed_modifier, ":mod_speed"),
				(agent_set_slot, ":player_agent_id", slot_agent_base_speed_mod, ":mod_speed"),
      (try_end),
    (try_end),
  ])


# Trigger Param 1: damage inflicted agent_id
# Trigger Param 2: damage dealer agent_id
# Trigger Param 3: inflicted damage
# Register 0: damage dealer item_id
# Position Register 0: position of the blow
#                      rotation gives the direction of the blow
# Trigger result: if returned result is greater than or equal to zero, inflicted damage is set to the value specified by the module.
# this trigger is called server only apparently after testing lol.. just added checks to make sure. ( you know warband patches.. :P )
multiplayer_server_agent_hit_common = (
  ti_on_agent_hit, 0, 0, [(this_or_next|multiplayer_is_server), 
                          (neg|game_in_multiplayer_mode),],
  [
    (store_trigger_param_1,":hit_agent_no"),
    (assign,":item_id",reg0),

    # patch1115 surgeon begin
    (try_begin),
      (eq, ":item_id", "itm_bandages"),
      (store_trigger_param_2,":attacker_agent_no"),
     # (store_trigger_param_3,":damage"),      
      # send to clients is handled in this script.      
      (call_script,"script_server_handle_bandages_hit",":hit_agent_no",":attacker_agent_no"),#":damage",":item_id"),
      (set_trigger_result, 0), # bandages do no damage
    #(else_try),
    #  #training weapon damage reduction
    #  #optional server side feature. uncomment this to reduce damage dealt by training weapons. Damage reduction is done
    #  #by script here so that the training weapon can have the exact same stats and behaviour as the original weapon.
    #  (this_or_next|eq, ":item_id", "itm_training_officer_sword"),
    #  (this_or_next|eq, ":item_id", "itm_training_heavy_sword"),
    #  (this_or_next|eq, ":item_id", "itm_training_light_sabre"),
    #  (eq, ":item_id", "itm_training_musket"),
    #  (store_trigger_param_2, ":attacker_agent_no"),
    #  (agent_is_active, ":attacker_agent_no"),
    #  (neq, ":hit_agent_no", ":attacker_agent_no"), # not hitting yourself.
    #  (agent_is_active, ":hit_agent_no"),
    #  (agent_is_alive, ":hit_agent_no"),
    #  (store_trigger_param_3, ":damage"),
    #  #only do 12.5% (100% / 8) of the damage
    #  (store_div, ":reduced_damage", ":damage", 8),
    #  (assign, reg0, ":reduced_damage"),
    #  (set_trigger_result, ":reduced_damage"),
    (else_try),
    # patch1115 surgeon end, dont forget try end on end of trigger ;D 
       
        #No Rambo
       (try_begin), 
         (eq, "$g_multiplayer_game_type", multiplayer_game_type_commander),
         (eq, "$g_no_rambo", 1),
         
         (store_trigger_param_2,":attacker_agent_no"), 
         (agent_is_active,":attacker_agent_no"),
         (agent_get_player_id,":attacker_player",":attacker_agent_no"), 
         (player_is_active,":attacker_player"), 
         
         (agent_get_position,pos3,":attacker_agent_no"),
         (assign,":has_nearby_allies",0),
         (assign,":num_bots_left",0),
         (assign,":new_rambo_range",0),
				 (assign, ":closest_pos", 999999),
         (try_for_agents,":near_agent"),
           (eq,":has_nearby_allies",0),
           (neq,":near_agent",":attacker_agent_no"),
           (agent_is_active,":near_agent"),
           (agent_is_human,":near_agent"),
           (agent_is_alive,":near_agent"),
           (agent_get_group,":agent_group",":near_agent"),
           (eq,":agent_group",":attacker_player"), #In our squad
           (val_add,":num_bots_left",1),
           (agent_get_position,pos4,":near_agent"),
           (get_distance_between_positions_in_meters,":dist",pos4,pos3),
					 #(try_begin),
					 (lt,":dist",":closest_pos"),
					 (assign, ":closest_pos", ":dist"),
					 (lt,":dist","$g_no_rambo_range"),
					 (assign, ":has_nearby_allies", 1),
					 #(try_end),
					(try_end), 
         #(try_end),
				 #(try_begin),#hotfix
						(eq,":has_nearby_allies",0),
						(try_begin),
							 (gt,":num_bots_left",3),
							 (le,":closest_pos","$g_no_rambo_range"),
							 (assign,":has_nearby_allies",1),
						 (else_try),
							 (le,":num_bots_left",3),
							 (gt,":num_bots_left",0),
							 (store_mul, ":new_rambo_range", "$g_no_rambo_range", 15),
							 (val_div, ":new_rambo_range", 10),
							 (le,":closest_pos",":new_rambo_range"),
							 (assign,":has_nearby_allies",1),
						 (else_try),#(try_begin),
							 (eq,":num_bots_left",0),
							 (assign,":has_nearby_allies",1),
						  (try_end),
					 #(try_end),
           #(gt,":num_bots_left",3), #If player is almost last alive in squad, ignore this
           (eq,":has_nearby_allies",0),
           (set_trigger_result, 0), #Do no damage
           #Warn player he did no damage
           (multiplayer_send_2_int_to_player, ":attacker_player", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_no_rambo_warning"),
        # (try_end),
       (else_try), #Don't continue if we did no damage
        
        (agent_is_active,":hit_agent_no"),
        
        (try_begin),
          (neq, "$g_multiplayer_game_type", multiplayer_game_type_commander), #Let's not have this much fun, shall we?
          (gt,"$g_chance_of_falling_off_horse",0),
          # first check if even have horse.
          (agent_get_horse,":horse",":hit_agent_no"),
          (agent_is_active,":horse"),
          (agent_is_alive,":hit_agent_no"),
           
          (store_trigger_param_3,":damage"),
          (ge,":damage",10),
           
          (neg|agent_is_non_player,":hit_agent_no"), #Only do this to players
          (neg|agent_slot_eq,":hit_agent_no",slot_agent_has_fallen_off_horse,1), #Apparently there's some bug if you fall off twice

          (store_random_in_range,":random",0,100),
          (lt,":random","$g_chance_of_falling_off_horse"),
           
          (store_random_in_range,":anim",0,2),
          (val_add,":anim","anim_rider_fall_right_2"),
          (agent_set_animation,":hit_agent_no",":anim"),
          (agent_set_slot,":hit_agent_no",slot_agent_has_fallen_off_horse,1), #Apparently there's some bug if you fall off twice
          (agent_clear_scripted_mode,":horse"),
          (agent_start_running_away,":horse"),
        (try_end),
        
        (try_begin),
          (gt,"$g_damage_from_horse_dying",0),
          (neg|agent_is_human,":hit_agent_no"), #Horse
          (agent_get_rider,":rider",":hit_agent_no"),
          
          (agent_is_active,":rider"),
          (agent_is_alive,":rider"),
          
          (store_trigger_param_3,":damage"),
          (store_agent_hit_points,":hit_points",":hit_agent_no",1),
          (val_sub,":hit_points",":damage"),
          (le,":hit_points",0),
          
          (store_trigger_param_2,":attacker_agent_no"),
          (store_random_in_range,":damage_to_rider",10,20),
          (val_mul,":damage_to_rider","$g_damage_from_horse_dying"),
          (val_div,":damage_to_rider",100),
          
          (try_begin),
            (eq,":item_id",-1),
            (assign,":item_id","itm_russian_peasant_knife"),
          (try_end),
          (agent_deliver_damage_to_agent_advanced,":damage", ":attacker_agent_no", ":rider", ":damage_to_rider", ":item_id"),
         
          # gets called automatically.
          # (agent_get_troop_id,":troop_no",":rider"),
          # (troop_slot_eq,":troop_no",slot_troop_rank,mm_rank_musician),
           
          # (call_script,"script_multiplayer_server_agent_stop_music", ":rider"),
        (try_end),
        
        (try_begin),
          (agent_slot_ge,":hit_agent_no",slot_agent_current_control_prop,0), # we are controlling a prop.
          (try_begin),
            (agent_get_slot,":prop_instance",":hit_agent_no",slot_agent_current_control_prop),
            (prop_instance_is_valid,":prop_instance"),
            (prop_instance_get_scene_prop_kind,":prop_kind",":prop_instance"),
            (try_begin),
              (is_between,":prop_kind",mm_cannon_wood_types_begin,mm_cannon_wood_types_end),
              (call_script,"script_stop_agent_controlling_cannon",":prop_instance",":hit_agent_no"),
            (else_try),
              (call_script,"script_set_agent_controlling_prop",":prop_instance",":hit_agent_no",0),
            (try_end),
          (try_end),
        (else_try),
          (agent_slot_ge,":hit_agent_no",slot_agent_used_prop_instance,0),
          
          (call_script,"script_multiplayer_server_agent_stop_music",":hit_agent_no"),
        (else_try),
          #  (call_script, "script_cf_agent_is_playing_music", ":hit_agent_no"), # is playing
          # if we have a musician just to be sure call stop music.
          (agent_get_troop_id,":troop_no",":hit_agent_no"),
          (troop_slot_eq,":troop_no",slot_troop_rank,mm_rank_musician),
          
          (call_script,"script_multiplayer_server_agent_stop_music",":hit_agent_no"),
        (try_end),
        
        
        #patch1115
        # horsies. clear their scripted mode.
        (try_begin),
          (neg|agent_is_human,":hit_agent_no"),
          
          (agent_get_rider, ":rider_agent_id", ":hit_agent_no"),
          (lt, ":rider_agent_id", 0),
          (agent_get_item_id,":horse_kind", ":hit_agent_no"),
          
          (neg|item_slot_eq,":horse_kind",slot_item_multiplayer_item_class, multi_item_class_type_horse_cannon),
          (neg|item_slot_eq,":horse_kind",slot_item_multiplayer_item_class, multi_item_class_type_horse_howitzer),
          (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),
          
          (agent_clear_scripted_mode,":hit_agent_no"),
        (try_end),
        
        #patch1115 fix 41/1 change begin 
        (multiplayer_is_dedicated_server), # only dedi logs shit.
        
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_duel),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_deathmatch),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),
        
        (store_trigger_param_2,":attacker_agent_no"),       
        (agent_is_active, ":attacker_agent_no"),
        (neq, ":hit_agent_no", ":attacker_agent_no"), # not hitting yourself.
        (neg|agent_is_non_player, ":attacker_agent_no"), # attacker must always be player
        (agent_get_team, ":attacker_agent_team", ":attacker_agent_no"),
        
        (try_begin), #human hit stuff.
          (agent_is_human, ":hit_agent_no"), 
          (try_begin),
            (neg|agent_is_non_player, ":hit_agent_no"), # guy hit is a player?
            (agent_get_team, ":hit_team", ":hit_agent_no"),
            (eq, ":attacker_agent_team", ":hit_team"), # same team only.
            
            (store_trigger_param_3,":damage"),
            (ge, ":damage", 1), # doing any dmg?
            
            (store_agent_hit_points, ":hit_points", ":hit_agent_no", 1),
            (lt, ":damage", ":hit_points"), # only wounding, killing is handled somewhere else. :D
            
            (agent_get_player_id,":hit_agent_player", ":hit_agent_no"),
            (player_is_active,":hit_agent_player"), 	   
            (agent_get_player_id,":attacker_agent_player", ":attacker_agent_no"),
            (player_is_active, ":attacker_agent_player"),
           
            (str_store_player_username, s1, ":attacker_agent_player"),
            (str_store_player_username, s2, ":hit_agent_player"),
            
            (assign, reg60, ":damage"),

            (server_add_message_to_log,"str_teamwounded_s1_s2"),
           # (assign, reg60, ":damage"),  #shouldnt need this now that its in one message
           # (server_add_message_to_log,"str_delivered_damage"),
          (try_end),
        (else_try), #horse hit stuff 
          (agent_get_rider, ":agent_rider_no",":hit_agent_no"),
          (agent_is_active,":agent_rider_no"), # even have a rider?
          (neq, ":agent_rider_no", ":attacker_agent_no"), # not hitting your own horse.
          (neg|agent_is_non_player, ":agent_rider_no"), # rider of hitted horse is a player?
          (agent_get_team, ":hit_team", ":agent_rider_no"),
          (eq, ":attacker_agent_team", ":hit_team"), # same team only.
          
          (store_trigger_param_3,":damage"),
          (ge, ":damage", 1), # doing any dmg?
          
          (store_agent_hit_points, ":hit_points", ":hit_agent_no", 1),
          
          (agent_get_player_id,":hit_rider_player", ":agent_rider_no"),
          (player_is_active,":hit_rider_player"),
          (agent_get_player_id,":attacker_agent_player", ":attacker_agent_no"),
          (player_is_active, ":attacker_agent_player"),
        
          (str_store_player_username, s1, ":attacker_agent_player"),
          (str_store_player_username, s2, ":hit_rider_player"),
          
          (try_begin), # wounding horse
            (lt, ":damage", ":hit_points"),
            
            (assign, reg60, ":damage"), 
            (server_add_message_to_log,"str_teamwounded_s1_s2_horse"),
            
            #(server_add_message_to_log,"str_delivered_damage"), #shouldnt need this now that its in one message
          (else_try), #killing Horse
            (server_add_message_to_log,"str_teamkilled_s1_s2_horse"),
          (try_end),
        (try_end),
        #patch1115 41/1 change end
        
      (try_end),
    (try_end),
    ##drinking bottle break script
    ##optional server side feature. uncomment this to enable breaking bottles
    #(try_begin),
    #  (eq, ":item_id", "itm_drinking_bottle_melee"),
    #  (store_trigger_param_2, ":attacker_agent_no"),
    #  (assign, ":end_cond", ek_head),
    #  (try_for_range, ":equipment_slot", ek_item_0, ":end_cond"),
    #    (agent_get_item_slot, ":cur_item_id", ":attacker_agent_no", ":equipment_slot"),
    #    (this_or_next|eq, ":cur_item_id", "itm_drinking_bottle_melee"),
    #    (eq, ":cur_item_id", "itm_drinking_bottle"),
    #    (val_add, ":equipment_slot", 1),
    #    (agent_unequip_item, ":attacker_agent_no", ":cur_item_id", ":equipment_slot"),
    #    (agent_equip_item, ":attacker_agent_no", "itm_brokenbottle", ":equipment_slot"),
    #    (agent_set_wielded_item, ":attacker_agent_no", "itm_brokenbottle"),
    #    (call_script, "script_multiplayer_server_play_sound_at_agent", "snd_glass_break", ":attacker_agent_no"),
    #    (assign, ":end_cond", 0),
    #  (try_end),
    #(try_end),
    ##end drinking bottle break script
  ])

multiplayer_agent_wield_item_common = (
  ti_on_item_wielded, 0, 0, [
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode)],
  [
    (store_trigger_param_1,":agent_id"),
    (store_trigger_param_2,":item_id"),
    
    (try_begin),
      (gt,":item_id",-1),
      (try_begin),
        (call_script,"script_cf_agent_is_playing_piano",":agent_id"),
        
        (call_script,"script_multiplayer_server_agent_stop_music", ":agent_id"),
      (else_try),
        (call_script,"script_cf_agent_is_taking_a_shit",":agent_id"),
        
        (call_script,"script_multiplayer_server_agent_stop_music", ":agent_id"),
      (else_try),
        (call_script,"script_cf_agent_is_surrendering",":agent_id"),
        
        (set_fixed_point_multiplier,100),
        (try_begin),
          (agent_slot_eq, ":agent_id", slot_agent_god_mode, 1),
          (agent_set_speed_modifier,":agent_id", 350),
          (agent_set_slot,":agent_id",slot_agent_base_speed_mod,350),
          (agent_set_horse_speed_factor, ":agent_id", 100),
        (else_try),
          (agent_set_speed_modifier,":agent_id", 100),
          (agent_set_slot,":agent_id",slot_agent_base_speed_mod,100),
          (agent_set_horse_speed_factor, ":agent_id", 100),
        (try_end),
      (try_end),
    (try_end),
  ])
 
multiplayer_agent_unwield_item_common = (
  ti_on_item_unwielded, 0.1, 0, [
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode)],
  [
    (store_trigger_param_1,":agent_no"),
    (store_trigger_param_2,":item_id"),
      
    (try_begin),
      (gt,":item_id",-1),
      (this_or_next|item_slot_eq,":item_id",slot_item_multiplayer_item_class, multi_item_class_type_flag), #always use item classes!!!
      (eq,":item_id","itm_rocket_placement"),
      
      (agent_is_active,":agent_no"),
      (neg|agent_is_non_player, ":agent_no"),  #patch1115 fix43/11
      (agent_get_position,pos25,":agent_no"),
      (position_move_y,pos25,30),
      (try_begin),
        (neq,":item_id","itm_rocket_placement"), # dont rotate up for the rocketplacement
        
        (agent_get_horse, ":agent_horse", ":agent_no"),
        (try_begin),
          (gt, ":agent_horse", -1), #PATCH1115 fix 5/3
          (position_move_x,pos25,50),
        (else_try),
          (position_move_z,pos25,36),
        (try_end),
        
        (position_rotate_x,pos25,90),
      (try_end),
      (set_spawn_position,pos25),
      (spawn_item,":item_id",0,300), # remove after 5 minutes
      
      (assign, ":end_cond", ek_head),
      (try_for_range,":equipment_slot",ek_item_0,":end_cond"),  #patch1115 change begin fix 1/2
        (agent_get_item_slot, ":cur_item_id", ":agent_no", ":equipment_slot"),
        (eq,":cur_item_id",":item_id"),
        (val_add,":equipment_slot",1),
        (agent_unequip_item, ":agent_no", ":item_id", ":equipment_slot"),
        (assign,":end_cond",0),
      (try_end), #patch1115 1/2 change end
      
      #(agent_unequip_item,":agent_no",":item_id"),
    (else_try),
      (call_script, "script_cf_agent_is_playing_music", ":agent_no"), # is playing
      
      (call_script,"script_multiplayer_server_agent_stop_music",":agent_no"),
    (try_end),
  ])

multiplayer_client_spyglass = (
  0, 0, 1, [
  (neg|multiplayer_is_dedicated_server),
  (game_key_is_down,gk_defend),
  ],
  [
    (neg|is_presentation_active,"prsnt_spyglass_dummy"),
    (neg|is_presentation_active,"prsnt_drinking"),
    (call_script,"script_client_get_my_agent"),
    (assign,":agent_id",reg0),
    (agent_is_active,":agent_id"),
    (agent_is_alive,":agent_id"),
    (agent_get_wielded_item,":item_id",":agent_id",0),
    (try_begin),
      (eq,":item_id","itm_spyglass"),
      (start_presentation,"prsnt_spyglass_dummy"),
    (else_try),
      #drinking
      #(call_script, "script_multiplayer_agent_drinking_get_animation", ":item_id"),
      (this_or_next|eq, ":item_id", "itm_drinking_cup"),
      (this_or_next|eq, ":item_id", "itm_drinking_tea_cup"),
      (this_or_next|eq, ":item_id", "itm_drinking_tea_cup_plate"),
      (eq, ":item_id", "itm_drinking_bottle"),
      (start_presentation, "prsnt_drinking"),
      #end drinking
    (try_end),
  ])

##optional server side feature. uncomment this to enable idle animations after wielding an item like cup or cane
##also remember to uncomment the 3 refernces to multiplayer_server_start_idle_animation below
#multiplayer_server_start_idle_animation = (
#  0, 1, 0, [
#  (multiplayer_is_dedicated_server),
#  ],
#  [
#    (try_for_agents, ":agent_id"),
#      (agent_is_active, ":agent_id"),
#      (agent_is_alive, ":agent_id"),
#      (agent_is_human, ":agent_id"),
#      (agent_get_wielded_item, ":item_id", ":agent_id", 0),
#      (assign, ":animation_id", -1),
#      (assign, ":cur_animation_id", -1),
#      (try_begin),
#        (eq, ":item_id", "itm_cane"),
#        (agent_get_animation, ":cur_animation_id", ":agent_id", 1),
#        (assign, ":animation_id", "anim_cane_idle"),
#      (else_try),
#        # disable the animation on switching to melee mode, so the weapon can be used
#        (eq, ":item_id", "itm_cane_melee"),
#        (agent_get_animation, ":cur_animation_id", ":agent_id", 1),
#        (eq, ":cur_animation_id", "anim_cane_idle"),
#        (assign, ":animation_id", "anim_drum_end"),
#      (else_try),
#        (eq, ":item_id", "itm_drinking_cup"),
#        (agent_get_animation, ":cur_animation_id", ":agent_id", 1),
#        # make sure we are not currently drinking
#        (call_script, "script_multiplayer_agent_drinking_get_animation", ":item_id"),
#        (neq, ":cur_animation_id", reg0),
#        (assign, ":animation_id", "anim_drinking_cup_idle"),
#      (else_try),
#        (this_or_next|eq, ":item_id", "itm_drinking_tea_cup"),
#        (eq, ":item_id", "itm_drinking_tea_cup_plate"),
#        (agent_get_animation, ":cur_animation_id", ":agent_id", 1),
#        # make sure we are not currently drinking
#        (call_script, "script_multiplayer_agent_drinking_get_animation", ":item_id"),
#        (neq, ":cur_animation_id", reg0),
#        (assign, ":animation_id", "anim_drinking_tea_idle"),
#      (try_end),
#      (gt, ":animation_id", -1),
#      (neq, ":cur_animation_id", ":animation_id"),
#      (agent_set_animation, ":agent_id", ":animation_id", 1),
#    (try_end),
#  ])

multiplayer_client_walking = (
  0, 0, 0.1, [
  (neg|multiplayer_is_dedicated_server),
  (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
  (neg|is_presentation_active, "prsnt_game_multiplayer_admin_panel"),
  (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"), #custom_chat:
  
  (game_key_clicked,gk_zoom),
  ],
  [
    (try_begin),
      (neg|is_zoom_disabled),
      (multiplayer_get_my_player, ":player_id"),
      (player_is_active, ":player_id"),
      (multiplayer_send_int_to_server, multiplayer_event_send_player_action, player_action_has_cheat),
    (else_try),
      (call_script,"script_client_get_my_agent"),
      (assign,":agent_id",reg0),
      (agent_is_active,":agent_id"),
      (agent_is_alive,":agent_id"),
      (multiplayer_send_int_to_server, multiplayer_event_send_player_action, player_action_toggle_walk),
    (try_end),
  ])
  
#custom_keys: start
    # This trigger allows server modders to implement custom actions for directional keys.
    # Delay of 0.25 seconds is both low and high enough to make this trigger
    # usable for both key held down and key clicked types of events.
    # Server modders who want longer cooldown can implement their own server side timer.
    # Help for modders: for example use, search for player_action_key_right_held in module_scripts.py
    # To enable, set mod_variable_custom_direction_keys to 1 in module_scripts.py and send to players
multiplayer_client_custom_directional_keys = (
  0, 0, 0.25, [
  (neg|multiplayer_is_dedicated_server),
  (eq, "$g_enable_custom_directional_keys", 1),
        # Disallow if controlling ships,
        # in order to avoid control conflict and unneeded sending to server.       
  (neg|is_between,"$g_cur_control_prop_kind", "spr_mm_ship", "spr_door_destructible"),
  (this_or_next|key_is_down, key_up),
  (this_or_next|key_is_down, key_down),
  (this_or_next|key_is_down, key_left),
  (key_is_down, key_right),
  ],
  [
    (try_begin),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_up_left_held),
    (else_try),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_up_right_held),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_down_left_held),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_down_right_held),
    (else_try),
      (key_is_down, key_up),
      (neg|key_is_down, key_down),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_up_held),
    (else_try),
      (key_is_down, key_down),
      (neg|key_is_down, key_up),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_down_held),
    (else_try),
      (key_is_down, key_left),
      (neg|key_is_down, key_right),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_left_held),
    (else_try),
      (key_is_down, key_right),
      (neg|key_is_down, key_left),
        (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_right_held),
    (try_end),

  ])  

    # To enable, set mod_variable_enable_action_v to 1 in module_scripts.py and send to players
multiplayer_client_custom_action_v = (
  0, 0, 1.0, [
  (neg|multiplayer_is_dedicated_server),
  (eq, "$g_enable_action_v", 1),
  (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
  (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"),
  (key_clicked,key_v),
  ],
  [
    (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_v),
  ])  
    # To enable, set mod_variable_enable_action_b to 1 in module_scripts.py and send to players
multiplayer_client_custom_action_b = (
  0, 0, 1.0, [
  (neg|multiplayer_is_dedicated_server),
  (eq, "$g_enable_action_b", 1),
  (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
  (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"),
  (key_clicked,key_b),
  ],
  [
    (multiplayer_send_int_to_server,multiplayer_event_send_player_action,player_action_key_b),
  ])
  
#custom_keys: end
  
multiplayer_server_disallow_multiple_firearms = (
  ti_on_item_picked_up, 0, 0, [(this_or_next|multiplayer_is_server),
                               (neg|game_in_multiplayer_mode),
                              ],
  [
    (store_trigger_param_1,":agent_id"),
    (store_trigger_param_2,":picked_item_id"),
    
    # Disallow multiple firearms!
    (try_begin),
      (eq,"$g_allow_multiple_firearms",0),
      (call_script, "script_multiplayer_server_disallow_multiple_firearms_on_pickup", ":agent_id", ":picked_item_id"),
    (try_end),
    
    (try_begin), # Flags?  #patch1115 change begin fix 1/1
      (gt,":picked_item_id",-1),
      (this_or_next|item_slot_eq,":picked_item_id",slot_item_multiplayer_item_class, multi_item_class_type_flag), #always use item classes!!!
      (eq,":picked_item_id","itm_rocket_placement"),
      
      (store_trigger_param_1,":agent_id"),
      
      (agent_is_active,":agent_id"),

      (assign,":item_found",0),
      (assign,":first_remove",1),
      (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head),
        (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slot"),
        
        (gt,":item_id",-1), # even have a item there?
                
        (this_or_next|item_slot_eq,":item_id",slot_item_multiplayer_item_class, multi_item_class_type_flag), #always use item classes!!!
        (eq,":item_id","itm_rocket_placement"),        
        
        (val_add,":equipment_slot",1),
        (agent_unequip_item, ":agent_id", ":item_id", ":equipment_slot"),
        (assign,":should_remove",1),
        (try_begin),
          (eq,":picked_item_id",":item_id"),
          (eq,":item_found",0),
          (assign,":item_found",1),
          (assign,":should_remove",0),
        (try_end),
        
        (eq,":should_remove",1), 
        
        (try_begin),
          (eq,":first_remove",1),
          
          (assign,":first_remove",0),
          # init the position only once...
          (agent_get_position,pos37,":agent_id"),
          (position_move_z,pos37,10),
          (set_spawn_position,pos37),
        (try_end),
         
        (try_begin),  
          (spawn_item,":item_id",0,300), # remove after 5 minutes   
        (try_end), 
      (try_end),
	  (agent_equip_item,":agent_id",":picked_item_id"),
      (agent_set_wielded_item,":agent_id",":picked_item_id"), # set the weapon wielded.
    (try_end),   #patch1115 change end
    
  ])
  
multiplayer_server_bird_spawn_common = (
  ti_after_mission_start, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
    (store_current_scene,":cur_scene"),
    (is_between,":cur_scene", "scn_random_multi_plain_medium", "scn_mp_custom_map_1"),
    
    (store_random_in_range,":num_birds_to_spawn",0,4),
    (try_for_range,":unused",0,":num_birds_to_spawn"),
      (store_random_in_range,":entry",0,64),
      (entry_point_get_position,pos49,":entry"),
      (set_fixed_point_multiplier,100),
      (position_set_z,pos49,9000),
      
      (call_script, "script_find_or_create_scene_prop_instance", "spr_mm_bird", 0, 0, 0),
	  # (assign,":new_in",reg0),
	  # (prop_instance_is_valid,":new_in"),
	  # (scene_prop_set_slot,":new_in",scene_prop_slot_in_use,1),
    (try_end),
  ])
  
multiplayer_server_move_bird_common = (
  5.55, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
    (set_fixed_point_multiplier,100),
    
    (scene_prop_get_num_instances, ":num_instances", "spr_mm_bird"),
    (try_for_range,":prop_no",0,":num_instances"),
      (scene_prop_get_instance,":bird_id","spr_mm_bird",":prop_no"),
    #(try_for_prop_instances, ":bird_id", "spr_mm_bird"),
      #(assign,":bird_id",":bird_id"),
      (scene_prop_slot_eq,":bird_id", scene_prop_slot_in_use, 1),
      
      (prop_instance_get_position, pos23, ":bird_id"),
      
      (try_begin),
        (store_random_in_range,":play_sound",0,100),
        (lt,":play_sound",5),
        (copy_position,pos56,pos23),
        (call_script, "script_multiplayer_server_play_sound_at_position", "snd_ambient_buzzard"),
      (try_end),
      
      (store_random_in_range,":rotation_angle",-50,51),
      (position_rotate_z,pos23,":rotation_angle"),
      (position_move_y,pos23,500,0),#2500
      (prop_instance_animate_to_position, ":bird_id", pos23, 560),#2000
    (try_end),
  ])

multiplayer_thunder_server = (
  5.29, 0, 0, [ #Server side thunder storm check every 5 sec
  (this_or_next|multiplayer_is_server),
  (neg|game_in_multiplayer_mode),
  (gt,"$g_thunder_type",0), 
  ],
  [
    (store_random_in_range,":thunder_roll",0,200),#Thunder dice roll
    (ge,"$g_thunder_strength",":thunder_roll"), #At highest value (100), 50% chance of thunder strike
    (store_random_in_range,":thunder_delay",0,10000),#Thunder delay in ms
    (try_begin),
      (multiplayer_is_server),
      (try_for_players, ":cur_player", "$g_ignore_server"),
        (player_is_active,":cur_player"),
        (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_thunder, ":thunder_delay"),
      (try_end),
    (else_try),
      (neg|game_in_multiplayer_mode),
      (call_script,"script_lighting_strike",":thunder_delay"),
    (try_end),
  ])
  
multiplayer_thunder_lightning_client = (
  0, 0, 0.3, [(neg|multiplayer_is_dedicated_server),(is_between,"$g_thunder_state",1,3)], #Client side thunder storm lightning check
  [
    (try_begin),
      (eq,"$g_thunder_state",1),
      (store_random_in_range, ":flash_distance", 90, 130),
      (set_fog_distance, ":flash_distance", 0xFFFFFF),
      #(mission_cam_animate_to_screen_color,0xB0FFFFFF,75),
    (else_try),
      (eq,"$g_thunder_state",2),
      (set_fog_distance, "$g_fog_distance", "$g_fog_colour"),
      #(mission_cam_animate_to_screen_color,0x00FFFFFF,75),
    (try_end),
    (val_add,"$g_thunder_state",1),
  ])
  
multiplayer_thunder_sound_client = (
  0.13, 0, 0, [
  (neg|multiplayer_is_dedicated_server),
  (eq,"$g_thunder_state",3),
  (store_mission_timer_a_msec,":cur_time"),
  (ge,":cur_time","$g_thunder_at_time"),
  ], #Client side thunder storm sound check
  [
    (play_sound,"snd_thunder"),
    (assign,"$g_thunder_state",0),
  ])
  
multiplayer_mission_end_common = (
  ti_on_multiplayer_mission_end, 0, 0, [(neg|multiplayer_is_dedicated_server),],
  [
    (assign,"$g_last_refresh_at",0),
    
    (try_for_agents, ":cur_agent"),
      (agent_is_active,":cur_agent"),
      (agent_stop_sound,":cur_agent"),
    (try_end),
  ])
  
# Vincenzo begin
multiplayer_client_send_admin_message = (
  0, 0.05, 0, [(neg|multiplayer_is_dedicated_server),
               (this_or_next|key_clicked,key_u),
			         (key_clicked,key_i),
               
               (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
               (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"), #custom_chat:
               
               (try_begin),
                 (key_clicked,key_u),
                 (assign,"$g_admin_chat_type",admin_chat_type_everyone),
               (else_try),
                 (key_clicked,key_i),
                 (assign,"$g_admin_chat_type",admin_chat_type_inter),
               (try_end),
               ],
  [  
    (multiplayer_get_my_player, ":cur_player"),
    (player_is_active,":cur_player"),
    (player_is_admin, ":cur_player"),
    
    (neg|player_is_busy_with_menus, ":cur_player"),
    (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
    (neg|is_presentation_active, "prsnt_game_multiplayer_admin_panel"),
    (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
    
    (start_presentation, "prsnt_multiplayer_admin_chat"),
  ])
 # Vincenzo end

#custom_chat:
multiplayer_client_send_custom_chat = (
  0, 0.05, 0, [(neg|multiplayer_is_dedicated_server),
               (eq, "$g_enable_custom_chat", 1),
               (key_clicked,key_o), 
               (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
               (neg|is_presentation_active, "prsnt_multiplayer_custom_chat"), #custom_chat:
               ],
  [  
    (multiplayer_get_my_player, ":cur_player"),
    (player_is_active,":cur_player"),
    
    (neg|player_is_busy_with_menus, ":cur_player"),
    (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
    (neg|is_presentation_active, "prsnt_game_multiplayer_admin_panel"),
    (neg|is_presentation_active, "prsnt_multiplayer_admin_chat"),
    
    (start_presentation, "prsnt_multiplayer_custom_chat"),
  ])
 
# Vincenzo change seconds

multiplayer_server_cleanup_props = (
  13.22, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
    (store_mission_timer_a,":cur_time"),
    
    # Crators remove after 2 minutes. 
    (try_for_range,":prop_type", "spr_mm_crator_small", "spr_mm_wallgate"),
      (try_for_prop_instances, ":cur_instance_id", ":prop_type", somt_temporary_object),
        (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_is_spawned,1), # a spawned crator.
        (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_in_use,1), # and in use.
        
        (scene_prop_get_slot,":spawned_at",":cur_instance_id", scene_prop_slot_spawned_at),
        (store_sub,":time_difirence",":cur_time",":spawned_at"),
        (gt,":time_difirence",120), #(2 * 60 = 120)
        
        (call_script, "script_clean_up_prop_instance", ":cur_instance_id"),
      (try_end),
    (try_end),
        
    # Horse limbers without horse remove after 2 minutes.
    (try_for_prop_instances, ":cur_instance_id", "spr_mm_limber_wood", somt_temporary_object),
      (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_is_spawned,1), # a spawned crator.
      (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_in_use,1), # and in use.
      (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_carrier_agent,-1), # and has no horse attached.
      
      (scene_prop_get_slot,":spawned_at",":cur_instance_id", scene_prop_slot_spawned_at), # gets reset with new time every time when dragged.
      (store_sub,":time_difirence",":cur_time",":spawned_at"),
      (gt,":time_difirence",120), #(2 * 60 = 120)
      
      (scene_prop_get_slot,":wheels_instance",":cur_instance_id", scene_prop_slot_child_prop1),
      (scene_prop_get_slot,":cannon_instance",":cur_instance_id", scene_prop_slot_child_prop2),
      (try_begin),
        (prop_instance_is_valid,":cannon_instance"),
        (call_script,"script_unlimber_cannon_from_horse",":cannon_instance"), # cannon unlimber button instance ID is passed here.
      (try_end),
      
      (call_script, "script_clean_up_prop_instance", ":cur_instance_id"),
      (call_script, "script_clean_up_prop_instance", ":wheels_instance"),
    (try_end),
    
    
    (try_for_range,":ship_type", "spr_mm_ship", "spr_door_destructible"),
      (try_for_prop_instances, ":cur_instance_id", ":ship_type", somt_object),  
        (prop_instance_get_variation_id,":usable_boat",":cur_instance_id"),
        (eq,":usable_boat",1),
        (assign, ":should_reset", 0),  #patch1115 fix 37/1
        
        (try_begin),
          (scene_prop_get_slot, ":bounce", ":cur_instance_id", scene_prop_slot_bounces),
          (eq, ":bounce", 1),
          (scene_prop_set_slot,":cur_instance_id",scene_prop_slot_controller_agent,-1),
          (scene_prop_get_slot,":left_control_at",":cur_instance_id", scene_prop_slot_time_left),
          (store_sub,":time_difirence",":cur_time",":left_control_at"),
          (gt,":time_difirence",60), #(1 * 60 = 60)

          
          (assign, ":should_reset", 1),
          (assign,":reset",1),
        (else_try),
          (scene_prop_get_slot,":cur_control_agent",":cur_instance_id",scene_prop_slot_controller_agent),
          (neg|agent_is_active,":cur_control_agent"),
        
          (scene_prop_get_slot,":left_control_at",":cur_instance_id", scene_prop_slot_time_left),
          (neq,":left_control_at",0),
          (store_sub,":time_difirence",":cur_time",":left_control_at"),
          (gt,":time_difirence",180), #(3 * 60 = 180)
        
          (assign, ":should_reset", 1),
          (assign,":reset",1),
          (try_for_agents,":cur_agent"),
            (agent_is_active,":cur_agent"),
            (scene_prop_has_agent_on_it, ":cur_instance_id", ":cur_agent"),
            (assign,":reset",0),
            (assign, ":should_reset", 0),
          (try_end),          
        (try_end),
        
        (eq,":reset",1),
        (eq, ":should_reset", 1),
        # reset boat
        (prop_instance_get_starting_position,pos57,":cur_instance_id"),
        (store_add,":boatheight","$g_scene_water_level",20),
        (position_set_z, pos57, ":boatheight"), # set to water level.
        (call_script, "script_prop_instance_animate_to_position_with_childs", ":cur_instance_id", 0,0,0),
        
        (scene_prop_set_slot, ":cur_instance_id", scene_prop_slot_bounces, 0),
        (scene_prop_set_slot, ":cur_instance_id", scene_prop_slot_y_value, 0),
        
        (try_begin),
          (call_script,"script_get_default_health_for_prop_kind",":ship_type"),
          (assign,":max_health",reg1),
          (assign,":health",reg2),
          
          (scene_prop_set_slot,":cur_instance_id",scene_prop_slot_health,":health"),
          (scene_prop_set_slot,":cur_instance_id",scene_prop_slot_max_health,":max_health"),
          (prop_instance_enable_physics, ":cur_instance_id", 1), # this is needed to reset the colision mesh on the prop if it is destroyed.
          (scene_prop_set_hit_points, ":cur_instance_id", ":max_health"),
          (scene_prop_set_cur_hit_points, ":cur_instance_id", ":health"), #patch1115 fix 37/1 end      
        (try_end),
      (try_end),
    (try_end),
    
    # clean up un-used spawned arty.
    (try_begin),
      (gt,"$g_spawn_with_artillery",0),
      
      # only in respawn modes
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_commander),
      (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),

      (try_for_range,":cannon_type", mm_cannon_types_begin, mm_cannon_types_end),
        (try_for_prop_instances, ":cur_instance_id", ":cannon_type", somt_temporary_object),
          (scene_prop_slot_eq,":cur_instance_id",scene_prop_slot_is_spawned,1), # a spawned cannon
         
          (scene_prop_get_slot,":cannon_wood",":cur_instance_id", scene_prop_slot_replaced_by), # and its replacement
          
          (prop_instance_is_valid,":cannon_wood"), # we have a valid prop.
          
          (scene_prop_get_slot,":spawned_at",":cannon_wood", scene_prop_slot_spawned_at),
          (store_sub,":time_difirence",":cur_time",":spawned_at"),
          (gt,":time_difirence",360), #(6 * 60 = 360)
          
          (call_script, "script_clean_up_prop_instance_with_childs", ":cannon_wood"), # clean cannon
          (call_script,"script_reset_prop_slots",":cur_instance_id"), # reset parent (ready for re-use)
        (try_end),
      (try_end),
    (try_end),
  ])

multiplayer_client_show_raindrops = (
0.1, 0, 0, [(neg|multiplayer_is_dedicated_server),
             (eq,"$g_rain_type",1),
            ],
  [
    (mission_cam_get_position, pos17),
    (set_fixed_point_multiplier,100),
    (position_get_distance_to_ground_level,":dist",pos17),
    (le, ":dist",1500),
    
    (position_get_rotation_around_z,":z_rot",pos17),
    (position_get_rotation_around_y,":y_rot",pos17),
    (init_position,pos18),
    (position_copy_origin,pos18,pos17),
    (position_rotate_z,pos18,":z_rot"),
    (position_rotate_y,pos18,":y_rot"),
    #(position_set_z,pos18,3000),
    (position_set_z_to_ground_level, pos18),
    
    
    # (try_begin),
      # (game_key_is_down, gk_character_window),
      # (copy_position,pos19,pos18),
      ##cur pos
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
      
      ##left pos
      # (position_move_x,pos19,1800),
      # (position_set_z_to_ground_level, pos19),
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
      
      ##right pos
      # (position_move_x,pos19,-3600),
      # (position_set_z_to_ground_level, pos19),
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
      
      # (position_move_x,pos19,1800),
      
      
      ##forward pos
      # (position_move_y,pos19,1700),
      # (position_set_z_to_ground_level, pos19),
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
      
      ##left pos
      # (position_move_x,pos19,1800),
      # (position_set_z_to_ground_level, pos19),
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
      
      ##right pos
      # (position_move_x,pos19,-3600),
      # (position_set_z_to_ground_level, pos19),
      # (set_spawn_position,pos19),
      # (spawn_scene_prop,"spr_ctf_flag_kingdom_1"),
    # (try_end),
    
    # (assign,reg25,"$g_rain_amount"),
    # (display_message,"@g_rain_amount:{reg25}"),
    
    (position_move_z, pos18, 4000),
    
    (store_mul,":loop_count","$g_rain_amount",15), # 15% of rain ammount 
    (val_div,":loop_count",100),
    (try_for_range, ":cur_loop", 0, ":loop_count"),# 50 #"$g_rain_amount" / 10
      (store_random_in_range, ":random_y_movement", -50, 1700), # 3450 # determine forward movement

      (try_begin),
        (lt,":random_y_movement",300),
        (store_add,":x_mov_range_max",":random_y_movement",200),
      (else_try),
        (store_add,":x_mov_range_max",":random_y_movement",100),
      (try_end),
      (store_mul, ":x_mov_range_min",":x_mov_range_max",-1),
      
      # (assign,reg22,":random_y_movement"),
      # (assign,reg23,":x_mov_range_max"),
      # (display_message,"@ random_y_movement: {reg22}    x_mov_range_max: {reg23}"),
      
      (store_random_in_range, ":random_x_movement",":x_mov_range_min", ":x_mov_range_max"), # ,-1500,1501),#   # 1750
      (copy_position,pos19,pos18),
      (position_move_x, pos19, ":random_x_movement"),
      (position_move_y, pos19, ":random_y_movement"),
      (position_set_z_to_ground_level, pos19), # set to ground again.
      (position_get_z, ":cur_z_val", pos19),
      (try_begin),
        (gt, ":cur_z_val", "$g_scene_water_level"), # above water level
        (particle_system_burst_no_sync, "psys_mm_rain_drop", pos19, 1),
      (else_try),
        (lt, ":cur_z_val", "$g_scene_water_level"), # under water level.
        (store_mod,":modulus",":cur_loop",2),
        (eq, ":modulus", 0), # only do waves half the times the normal drops.

        (position_set_z, pos19, "$g_scene_water_level"), # set to water level.
        (particle_system_burst_no_sync, "psys_mm_rain_wave", pos19, 1),
      (try_end),
    (try_end),
  ])

multiplayer_server_on_item_dropped = (
  ti_on_item_dropped, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode)],
  [
    (store_trigger_param_2, ":item_id"),
    
    (try_begin),
      (gt,":item_id",-1),
      
      (store_trigger_param_1, ":agent_no"),
      (agent_is_active,":agent_no"),
      
      (try_begin),
        (item_slot_eq,":item_id",slot_item_multiplayer_item_class, multi_item_class_type_flag), #always use item classes!!!
        (store_trigger_param_3, ":dropped_prop"),
        (prop_instance_get_position, pos25, ":dropped_prop"),
        
        (agent_get_horse, ":agent_horse", ":agent_no"),
        (try_begin),
          (gt, ":agent_horse", -1), #PATCH1115 fix 5/4
          (position_move_x,pos25,50),
        (else_try),
          (position_move_y,pos25,36),
        (try_end),
        (position_rotate_x, pos25, 90),
        (prop_instance_set_position, ":dropped_prop", pos25),
        (scene_prop_set_prune_time, ":dropped_prop", 300), # 5 minutes
      (else_try),
        (eq, ":item_id", "itm_cannon_lighter"),
        (agent_slot_ge,":agent_no",slot_agent_current_control_prop,0), # we are controlling a prop.
        (try_begin),
          (agent_get_slot,":prop_instance",":agent_no",slot_agent_current_control_prop),
          (prop_instance_is_valid,":prop_instance"),
          (prop_instance_get_scene_prop_kind,":prop_kind",":prop_instance"),
          (try_begin),
            (is_between,":prop_kind",mm_cannon_wood_types_begin,mm_cannon_wood_types_end),
            (call_script,"script_stop_agent_controlling_cannon",":prop_instance",":agent_no"),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
  ])
  
multiplayer_server_generate_build_points = (
20, 0, 0, [(multiplayer_is_server)],
  [
    (try_begin),
      (assign,":value_changed",0),
      (try_begin),
        (lt,"$g_team_1_build_points","$g_team_1_max_build_points"),
        (val_add,"$g_team_1_build_points",1),
        (assign,":value_changed",1),
      (try_end),
      
      (try_begin),
        (lt,"$g_team_2_build_points","$g_team_2_max_build_points"),
        (val_add,"$g_team_2_build_points",1),
        (assign,":value_changed",1),
      (try_end),   
      
      (try_begin),
        (eq,":value_changed",1),
        
        (call_script,"script_multiplayer_server_send_build_points"),
      (try_end),
    (try_end),
  ])
  
multiplayer_server_spawn_bots = (
  0.1, 0, 0, [ (multiplayer_is_server),
               (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
               (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
               (gt, ":total_req", 0),
             ],
  [
    (try_begin),
      (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),

      (store_mission_timer_a, ":round_time"),
      (val_sub, ":round_time", "$g_round_start_time"),
      
      (assign, ":rounded_game_first_round_time_limit_past", 1),
      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

        (lt, ":round_time", 20),
        
        (team_get_score, ":team_1_score", 0),
        (team_get_score, ":team_2_score", 1),

        (store_add, ":current_round", ":team_1_score", ":team_2_score"),
        (eq, ":current_round", 0),

        (assign, ":rounded_game_first_round_time_limit_past", 0),
      (try_end),
    
      (eq, ":rounded_game_first_round_time_limit_past", 1),
    
      (store_random_in_range, ":random_req", 0, ":total_req"),
      (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
      
      (assign, ":selected_team", 1),
      (try_begin),
        (lt, ":random_req", 0),
        #add to team 1
        (assign, ":selected_team", 0),
      (try_end),

      (assign, ":look_only_actives", 1),
      (try_begin),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),

        (le, ":round_time", 20),
        
        (assign, ":look_only_actives", 0),
      (try_end),
    
      (call_script, "script_multiplayer_find_bot_troop_and_group_for_spawn", ":selected_team", ":look_only_actives"),
      (assign, ":selected_troop", reg0),
      (assign, ":selected_group", reg1),

      (team_get_faction, ":team_faction", ":selected_team"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (assign, ":number_of_active_players_wanted_bot", 0),

      (assign,":player_end_cond",multiplayer_player_loops_end),
      (try_for_range, ":player_no", "$g_player_loops_begin", ":player_end_cond"),
        (player_is_active, ":player_no"),
        (player_get_team_no, ":player_team_no", ":player_no"),
        (eq, ":selected_team", ":player_team_no"),

        (assign, ":ai_wanted", 0),
        (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
        (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
          (player_slot_ge, ":player_no", ":bot_type_wanted_slot", 1),
          (assign, ":ai_wanted", 1),
          (assign, ":end_cond", 0), 
        (try_end),

        (ge, ":ai_wanted", 1),

        (val_add, ":number_of_active_players_wanted_bot", 1),
        (assign,":player_end_cond",0),
      (try_end),

      (try_begin),
        (this_or_next|ge, ":selected_group", 0),
        (eq, ":number_of_active_players_wanted_bot", 0),

        (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
        (assign, ":is_horseman", 0),
        (try_begin),
          (ge, ":has_item", 0),
          (assign, ":is_horseman", 1),
        (try_end),

        (try_begin),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

          (try_begin),
            (lt, ":round_time", 20), #at start of game spawn at base entry point
            (try_begin),
              (eq, ":selected_team", 0),
              (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 1, ":is_horseman"), 
            (else_try),
              (assign, reg0, multi_initial_spawn_point_team_2),
            (try_end),
          (else_try),
            (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
          (try_end),
        (else_try),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
      
          (try_begin),
            (eq, ":selected_team", 0),
            (assign, reg0, 0),
          (else_try),
            (assign, reg0, 32),
          (try_end),
        (else_try),
          (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
        (try_end),
      
        (store_current_scene, ":cur_scene"),
        (modify_visitors_at_site, ":cur_scene"),
        (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", ":selected_group"),
        (assign, "$g_multiplayer_ready_for_spawning_agent", 0),

        (try_begin),
          (eq, ":selected_team", 0),
          (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
        (else_try),
          (eq, ":selected_team", 1),
          (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
        (try_end),
      (try_end),
    (try_end),    
    ])

multiplayer_server_manage_bots = (
  3.18, 0, 0, [(multiplayer_is_server),],
  [
    (try_for_agents, ":cur_agent"),
      (agent_is_active, ":cur_agent"),
      (agent_is_non_player, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_get_group, ":agent_group", ":cur_agent"),
      (try_begin),
        (neg|player_is_active, ":agent_group"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (else_try),
        (player_get_team_no, ":leader_team_no", ":agent_group"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (neq, ":leader_team_no", ":agent_team"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (try_end),
    (try_end),
    ])
# Vincenzo change seconds
multiplayer_server_check_polls = (
  3.34, 5, 0,
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_poll_running", 1),
    (eq, "$g_multiplayer_poll_ended", 0),
    (store_mission_timer_a, ":mission_timer"),
    (store_add, ":total_votes", "$g_multiplayer_poll_no_count", "$g_multiplayer_poll_yes_count"),
    (this_or_next|eq, ":total_votes", "$g_multiplayer_poll_num_sent"),
    (gt, ":mission_timer", "$g_multiplayer_poll_end_time"),
    (call_script, "script_cf_multiplayer_evaluate_poll"),
    ],
  [
    (assign, "$g_multiplayer_poll_running", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_poll_to_show", 0), #change map
      (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_poll_value_to_show", 1),
      (call_script, "script_game_set_multiplayer_mission_end"),
    (try_end),
    ])
    
multiplayer_server_check_end_map = ( 
  1.06, 0, 0, [(multiplayer_is_server),],
  [
    #checking for restarting the map  #patch1115 end music here?
    (assign, ":end_map", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
      (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
    
      (try_begin),
        (eq, "$g_round_ended", 1),

        (store_mission_timer_a, ":seconds_past_till_round_ended"),
        (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
        (store_sub, ":multiplayer_respawn_period_minus_one", "$g_multiplayer_respawn_period", 1),
        (ge, ":seconds_past_till_round_ended", ":multiplayer_respawn_period_minus_one"),
  
        (store_mission_timer_a, ":mission_timer"),    
        (try_begin),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (assign, ":reduce_amount", 90),
        (else_try),
          (assign, ":reduce_amount", 120),
        (try_end),
    
        (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
        (store_sub, ":game_max_seconds_min_n_seconds", ":game_max_seconds", ":reduce_amount"), #when round ends if there are 60 seconds to map change time then change map without completing exact map time.
        (gt, ":mission_timer", ":game_max_seconds_min_n_seconds"),
	
        (assign, ":end_map", 1),
      (try_end),
      
      (eq, ":end_map", 1),
    (else_try),
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_king), #king of the hill mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #battle mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #siege mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #in headquarters mod game cannot limited by time, only can be limited by score.
      (store_mission_timer_a, ":mission_timer"),
      (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
      (gt, ":mission_timer", ":game_max_seconds"),
		  
      (assign, ":end_map", 1),
    (else_try),
      #assuming only 2 teams in scene
      (team_get_score, ":team_1_score", 0),
      (team_get_score, ":team_2_score", 1),
      # Vincenzo begin
      (store_add, ":rounds", ":team_1_score", ":team_2_score"),
      # Vincenzo end
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #for not-headquarters mods    conquest
        (try_begin),
          (this_or_next|ge, ":team_1_score", "$g_multiplayer_game_max_points"),
          (ge, ":team_2_score", "$g_multiplayer_game_max_points"),

          (assign, ":end_map", 1),
        (try_end),
        # Vincenzo begin
        (try_begin),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_king),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
          (ge, ":rounds", "$g_multiplayer_game_max_points"),

          (assign, ":end_map", 1),
        (try_end),
        # Vincenzo end
      (else_try),
        (assign, ":at_least_one_player_is_at_game", 0),
        (assign,":num_players",multiplayer_player_loops_end),
        (try_for_range, ":player_no", "$g_player_loops_begin", ":num_players"),
          (player_is_active, ":player_no"),
          (player_get_agent_id, ":agent_id", ":player_no"),
          (ge, ":agent_id", 0),
          (neg|agent_is_non_player, ":agent_id"),
          (assign, ":at_least_one_player_is_at_game", 1),
          (assign, ":num_players", 0),
        (try_end),
    
        (eq, ":at_least_one_player_is_at_game", 1),

        #(this_or_next|le, ":team_1_score", 0), #in headquarters game ends only if one team has 0 score.
        #(le, ":team_2_score", 0),
        
        #BEAVER NEW; don't end map until confirm to allow winner announcement to show.
        (eq,"$g_conquest_map_end_confirm",1),
		  
        (assign, ":end_map", 1),
      (try_end),
    (try_end),
    (try_begin),
      (eq, ":end_map", 1),
      
      (try_begin),
        (gt,"$g_auto_FF", 0),
        (server_set_friendly_fire, 0),
        (server_set_melee_friendly_fire, 0),
				(assign, reg60, "$g_auto_FF"),
        (str_store_string, s4, "str_FF_turn_on_when_2"),
        (call_script, "script_multiplayer_broadcast_message"),
      (try_end),
        

		  (call_script, "script_multiplayer_server_stop_music_at_map_change"),#patch1115 fix 2/4

      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
      (call_script, "script_game_set_multiplayer_mission_end"),           
    (try_end),
    ])

multiplayer_once_at_the_first_frame = (
  0, 0, ti_once, [(neg|multiplayer_is_dedicated_server),], [
    (start_presentation, "prsnt_multiplayer_welcome_message"),
    ])

multiplayer_battle_window_opened = (
  ti_battle_window_opened, 0, 0, [(neg|multiplayer_is_dedicated_server),], [
    (try_begin),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_team_deathmatch),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_headquarters),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_capture_the_flag),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_siege),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_battle),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_king),
      (eq,"$g_multiplayer_game_type",multiplayer_game_type_commander),
      (start_presentation, "prsnt_multiplayer_team_score_display"),
    (try_end),
    (try_begin),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_team_deathmatch),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_headquarters),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_capture_the_flag),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_siege),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_king),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_commander),
      (eq,"$g_multiplayer_game_type",multiplayer_game_type_battle),
      (start_presentation, "prsnt_multiplayer_bonus_icons"),
    (try_end),
    (try_begin),
      (eq,"$g_multiplayer_game_type",multiplayer_game_type_capture_the_flag),
      (start_presentation, "prsnt_multiplayer_flag_projection_display"),
    (try_end),
    (try_begin),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_siege),
      (this_or_next|eq,"$g_multiplayer_game_type",multiplayer_game_type_battle),
      (eq,"$g_multiplayer_game_type",multiplayer_game_type_commander),
      (start_presentation, "prsnt_multiplayer_round_time_counter"),
    (try_end),
    (try_begin),
      (neq,"$g_artillery_available_on_map",0),
      (start_presentation, "prsnt_multiplayer_artillery_icons"),
    (try_end),
    (start_presentation, "prsnt_multiplayer_beacon_player"),
    (start_presentation, "prsnt_multiplayer_medic_icons"), 
    ])

multiplayer_server_explosives  = (
  1, 0, 0, [(this_or_next|multiplayer_is_server),(neg|game_in_multiplayer_mode),],
  [
    (try_for_range,":explosive_type", mm_explosive_props_begin, mm_explosive_props_end),
      (try_for_prop_instances, ":instance_id", ":explosive_type"),
        #(scene_prop_slot_eq, ":instance_id", scene_prop_slot_in_use, 1),
        
        (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
        (gt,":cur_time",0),
        (val_sub,":cur_time",1),
        
        (prop_instance_get_position, pos47, ":instance_id"), 
        (try_begin),
          (le,":cur_time",0),
          
          (scene_prop_get_slot,":agent_id",":instance_id",scene_prop_slot_user_agent),
          
          (call_script, "script_clean_up_prop_instance", ":instance_id"),
          
          (call_script,"script_explosion_at_position",":agent_id",270,370), # Input: shooter_agent_no, max_damage points, range in cm
        (else_try),
          (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
          (set_fixed_point_multiplier,100),
          (position_move_z,pos47,80),
          (particle_system_burst, "psys_explosives_fuse_smoke", pos47, 60),
        (try_end),
      (try_end),
    (try_end),
  ])

multiplayer_play_sounds_and_particles  = (
  1, 0, 0, [(neg|multiplayer_is_dedicated_server)],
  [
    #Particles
    #begin
    (try_for_prop_instances, ":instance_id", "spr_mm_watersplash", somt_object), #Name of prop
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (val_sub,":cur_time",1),
      (try_begin),
        (le,":cur_time",0),
        (prop_instance_get_position, pos47, ":instance_id"),
        (particle_system_burst_no_sync, "psys_game_water_splash_2", pos47, 100), #particle name
        (store_random_in_range,":cur_time",2,3), #Seconds until next particle
      (try_end),
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
    (try_end),
    
    (try_for_prop_instances, ":instance_id", "spr_mm_ambient_insects", somt_object),  #Name of prop
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (val_sub,":cur_time",1),
      (try_begin),
        (le,":cur_time",0),
        (prop_instance_get_position, pos47, ":instance_id"),
        (particle_system_burst_no_sync, "psys_mm_bug_fly_1", pos47, 100), #particle name
        (store_random_in_range,":cur_time",8,14), #Seconds until next particle
      (try_end),
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
    (try_end),
    
    (try_for_prop_instances, ":instance_id", "spr_mm_ambient_insects1", somt_object),  #Name of prop
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (val_sub,":cur_time",1),
      (try_begin),
        (le,":cur_time",0),
        (prop_instance_get_position, pos47, ":instance_id"),
        (particle_system_burst_no_sync, "psys_mm_bug_fly_2", pos47, 100), #particle name
        (store_random_in_range,":cur_time",8,14), #Seconds until next particle
      (try_end),
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
    (try_end),
    
    (try_for_prop_instances, ":instance_id", "spr_mm_ambient_insects2", somt_object),  #Name of prop
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (val_sub,":cur_time",1),
      (try_begin),
        (le,":cur_time",0),
        (prop_instance_get_position, pos47, ":instance_id"),
        (particle_system_burst_no_sync, "psys_mm_bug_fly_3", pos47, 100), #particle name
        (store_random_in_range,":cur_time",8,14), #Seconds until next particle
      (try_end),
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
    (try_end),
    #end
    
    #Sounds
    #begin
    (try_for_prop_instances, ":instance_id", "spr_ambience_sound_local_crow", somt_object),  #Name of prop
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (val_sub,":cur_time",1),
      (try_begin),
        (le,":cur_time",0),
        (prop_instance_get_position, pos56, ":instance_id"),
        (play_sound_at_position, "snd_ambient_crow", pos56),#sound name
        (store_random_in_range,":cur_time",10,61), #Seconds until next sound
      (try_end),
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"),
    (try_end),
    #end
  ])
   
     
common_battle_init_banner = (
  ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
  ])


common_custom_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (neq, "$g_battle_result", 0),
      (call_script, "script_custom_battle_end"),
      (finish_mission),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ])

custom_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 2),
    (neg|main_hero_fallen, 0),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign, "$g_battle_won",1),
    (assign, "$g_battle_result", 1),
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission, 1),
    ])

custom_battle_check_defeat_condition = (
  1, 4, ti_once,
  [
    (main_hero_fallen),
    (assign,"$g_battle_result",-1),
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission),
    ])

common_battle_victory_display = (
  10, 0, 0, [(eq,"$g_battle_won",1),],
  [
    (display_message,"str_msg_battle_won"),
  ])


common_custom_battle_question_answered = (
   ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_custom_battle_end"),
     (finish_mission),
     ])


common_music_situation_update = (
  30, 0, 0, [],
  [
    (call_script, "script_combat_music_set_situation_with_culture"),
    ])

common_battle_order_panel = (
  0, 0, 0, [(neg|multiplayer_is_dedicated_server),],
  [
    (game_key_clicked, gk_view_orders),
    (neg|is_presentation_active, "prsnt_battle"),
    (start_presentation, "prsnt_battle"),
    ])

common_battle_order_panel_tick = (
  0.1, 0, 0, [(is_presentation_active, "prsnt_battle"),],
  [
    (call_script, "script_update_order_panel_statistics_and_map"),
    ])


common_inventory_not_available = (
  ti_inventory_key_pressed, 0, 0,
  [
    (display_message, "str_cant_use_inventory_now"),
    ], [])

multiplayer_server_anticheat = (
  ti_on_cheat_detected, 0, 0, [],
  [
    (store_trigger_param, ":player_no", 1),
    (store_trigger_param, ":detection_type", 2),
    (store_trigger_param, ":value", 3),
    (store_trigger_param, ":threshold", 4),
    # script_on_cheat_detected sets reg0 to 1 only for detection types it scores;
    # unhandled types leave reg0 at 0 so the native WSE2 engine still acts on them.
    (call_script, "script_on_cheat_detected", ":player_no", ":detection_type", ":value", ":threshold"),
  ])

multiplayer_server_ensure_anticheat_json = (
  ti_before_mission_start, 0, ti_once, [],
  [
    (call_script, "script_ensure_admin_guid_file"),
    (call_script, "script_ensure_player_whitelist_file"),
    (call_script, "script_ensure_anticheat_config"),
    (call_script, "script_cf_cache_anticheat_config"),
    (call_script, "script_ensure_anticheat_player_history"),
  ])




  #MM Multiplayer Commons
mm_multiplayer_common = [
  multiplayer_server_ensure_anticheat_json,
  multiplayer_server_anticheat,
  multiplayer_server_log_player_leave,
  multiplayer_server_mount_horse,
  multiplayer_server_dismount_horse,
  multiplayer_server_kill_stray_horses,
  multiplayer_server_aim_cannon,
  multiplayer_server_cannonball_flight,
  multiplayer_server_drowning,
  multiplayer_server_turn_fan_blades,
  multiplayer_server_move_church_bell,
  multiplayer_server_cleanup_props,
  multiplayer_server_explosives,
  multiplayer_server_order_voicecommands,
  multiplayer_server_drag_limber,
  multiplayer_server_move_bird_common,
  multiplayer_server_bird_spawn_common,
  multiplayer_server_sail_ship,
  multiplayer_thunder_server,
  multiplayer_server_on_item_dropped,
  multiplayer_server_disallow_multiple_firearms,
  multiplayer_server_tp_revived_players, #patch1115 46/18
  #multiplayer_server_auto_ff,
  multiplayer_server_agent_hit_common,
  multiplayer_agent_wield_item_common,
  multiplayer_agent_unwield_item_common,
  
  multiplayer_thunder_lightning_client,
  multiplayer_thunder_sound_client,
  multiplayer_client_drowning,
  multiplayer_client_control_ship,
  multiplayer_client_voicecommands,
  multiplayer_client_send_admin_message,
  #multiplayer_server_start_idle_animation,
  multiplayer_client_spyglass,
  multiplayer_client_walking,
  multiplayer_client_music_and_sapper,
  multiplayer_client_control_cannon,
  multiplayer_client_show_raindrops,
  multiplayer_play_sounds_and_particles,
  multiplayer_battle_window_opened,
  multiplayer_client_surrender,
  multiplayer_client_custom_directional_keys, #custom_keys:
  multiplayer_client_custom_action_v, #custom_keys:
  multiplayer_client_custom_action_b, #custom_keys:
  multiplayer_client_send_custom_chat #custom_chat:
  ]
  
mission_templates = [
  (
    "town_default",0,-1,
    "Default town visit",
    [],     
     [],
  ),

# This template is used in party encounters and such.
# 
  (
    "conversation_encounter",0,-1,
    "Conversation_encounter",
    [],
    [],
  ),
  
#----------------------------------------------------------------
#mission templates before this point are hardwired into the game.
#-----------------------------------------------------------------

  (
    "tutorial",mtf_battle_mode,-1,
    "You enter the training ground.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      
      (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      #MM
      multiplayer_server_drowning,
      multiplayer_server_aim_cannon,
      multiplayer_server_cannonball_flight,
      multiplayer_server_turn_fan_blades,
      multiplayer_server_explosives,
      multiplayer_server_drag_limber,
      multiplayer_server_move_bird_common,
      multiplayer_server_bird_spawn_common,
      #multiplayer_server_start_idle_animation,
      multiplayer_client_spyglass,
      multiplayer_client_control_cannon,
      multiplayer_play_sounds_and_particles,
      
      (ti_tab_pressed, 0, 0, [],
       [
        (try_begin),
          (lt, "$g_tutorial_state", 24),
          (question_box, "@Leave?"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
        
      common_inventory_not_available,
        
      (ti_before_mission_start, 0, 0, [],
       [

        (assign,"$g_tutorial_state",0),
        (assign,"$g_tutorial_target_hit",0),
        (assign,"$g_tutorial_targets_destroyed",0),
        (assign,"$g_is_tutorial",1),
        (assign, "$g_pointer_arrow_height_adder", 100),
        
        (call_script, "script_multiplayer_mm_before_mission_start_common"),
        
        (scene_set_day_time, 12),
         ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
          (entry_point_get_position,pos5,20),
          (set_spawn_position, pos5),
          (spawn_item, "itm_british_brown_bess", 0),
          
          (entry_point_get_position,pos5,40),
          (set_spawn_position, pos5),
          (spawn_agent,"trp_manual_dummy"),
          (assign, "$g_tutorial_dummy_agent", reg0),
          
          (get_player_agent_no,":player_agent"),
          (agent_equip_item,":player_agent","itm_bullets"),
          
          (call_script, "script_multiplayer_mm_after_mission_start_common"),
          
          (scene_set_day_time, 12),
         ]),

      common_battle_init_banner,
      
      (0, 0, 0,
       [
         (call_script, "script_iterate_pointer_arrow"),
         ], []),

      (0, 1, ti_once, [(eq,"$g_tutorial_state",0)],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_1"),
        (assign,"$g_tutorial_state",1),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_1"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",1)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_1"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",1),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos1,":player_agent"),
        (get_distance_between_positions_in_meters,":dist",pos1,pos0),
        (le,":dist",3),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_2"),
        (assign,"$g_tutorial_state",2),
        #Clean up arrow
        (assign, "$g_pointer_arrow_height_adder", -1000),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_2"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",2)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_2"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",2),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_british_brown_bess"),
      ],
      [
      #  (tutorial_message_set_background, 1),
      #  (tutorial_message,"str_tutorial_info_3"),
        (assign,"$g_tutorial_state",3),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_3"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",3)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_3"),
      ]),
      
      (0, 1, ti_once, [
        (eq,"$g_tutorial_state",3),
        (eq,"$g_tutorial_target_hit",0),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_british_brown_bess"),
        (assign,":is_loaded",1), 
        (try_for_range,":equipment_slot",ek_item_0,ek_head),
          (agent_get_item_slot, ":item_id", ":player_agent", ":equipment_slot"),
          (eq,":item_id","itm_british_brown_bess"),
          (agent_get_item_cur_ammo, ":is_loaded", ":player_agent", ":equipment_slot"),
        (try_end),
        (eq,":is_loaded",0), 
      ],
      [
        (eq,"$g_tutorial_state",3),
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_4"),
        (assign,"$g_tutorial_state",4),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_4"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",4)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_4"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",4),
        (eq,"$g_tutorial_target_hit",1),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_5"),
        (assign,"$g_tutorial_path",1),
        (assign,"$g_tutorial_state",5),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_5"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",3),
        (eq,"$g_tutorial_target_hit",1),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_6"),
        (assign,"$g_tutorial_path",2),
        (assign,"$g_tutorial_state",5),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_6"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",5)],
      [
        (tutorial_message_set_background, 1),
        (try_begin),
          (eq, "$g_tutorial_path",1),
          (tutorial_message,"str_tutorial_info_5"),
        (else_try),
          (eq, "$g_tutorial_path",2),
          (tutorial_message,"str_tutorial_info_6"),
        (try_end),
      ]),
      
      (0, 0, ti_once, [
        (eq,"$g_tutorial_state",5),
      ],
      [
        #Initialise arrow
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (entry_point_get_position, pos0, 1),
        (position_set_z_to_ground_level, pos0),
        (prop_instance_stop_animating,":prop_instance"),
        (prop_instance_set_position, ":prop_instance", pos0),
        (assign, "$g_pointer_arrow_height_adder", 10),
        
        #Remove barrier
        (scene_prop_get_num_instances,":num_instances","spr_mm_player_limiter_move_1"),
        (try_for_range,":prop_no",0,":num_instances"),
          (scene_prop_get_instance, ":prop_instance", "spr_mm_player_limiter_move_1", ":prop_no"),
          (prop_instance_get_position, pos2, ":prop_instance"),
          (position_move_z,pos2,-1000),
          (prop_instance_set_position, ":prop_instance", pos2),
        (try_end),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",5),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos1,":player_agent"),
        (get_distance_between_positions_in_meters,":dist",pos1,pos0),
        (le,":dist",3),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_7"),
        (assign,"$g_tutorial_state",6),
        #Clean up arrow
        (assign, "$g_pointer_arrow_height_adder", -1000),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_7"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",6)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_7"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",6),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_british_brown_bess_melee"),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_8"),
        (assign,"$g_tutorial_state",7),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_8"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",7)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_8"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",7),
        (get_player_agent_no,":player_agent"),
        (agent_get_animation,":anim_id",":player_agent",0),
        (eq,":anim_id","anim_stand_to_crouch"),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_9"),
        (assign,"$g_tutorial_state",8),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_9"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",8)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_9"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",8),
        (get_player_agent_no,":player_agent"),
        (agent_get_animation,":anim_id",":player_agent",0),
        (neq,":anim_id","anim_stand_to_crouch"),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_10"),
        (assign,"$g_tutorial_state",9),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_10"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",9)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_10"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",9),
        (eq,"$g_tutorial_targets_destroyed",4),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_11"),
        (assign,"$g_tutorial_state",10),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_11"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",10)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_11"),
      ]),
      
      (0, 3, ti_once, [
        (eq,"$g_tutorial_state",10),
      ],
      [
        (entry_point_get_position,pos5,3),
        (set_spawn_position, pos5),
        (spawn_horse, "itm_lightdragoon_horse_britain_1", 0),
        
        #Initialise arrow
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (entry_point_get_position, pos0, 3),
        (position_set_z_to_ground_level, pos0),
        (prop_instance_stop_animating,":prop_instance"),
        (prop_instance_set_position, ":prop_instance", pos0),
        (assign, "$g_pointer_arrow_height_adder", 120),
        
        #(get_player_agent_no,":player_agent"),
        #(agent_unequip_item,":player_agent","itm_british_infantry_ranker"),
        #(agent_unequip_item,":player_agent","itm_french_voltigeur_officer_pants"),
        #(agent_unequip_item,":player_agent","itm_33_stovepipe"),
        #(agent_unequip_item,":player_agent","itm_british_brown_bess"),
        #(agent_unequip_item,":player_agent","itm_bullets"),
        #(agent_equip_item,":player_agent","itm_british_light_dragoon"),
        #(agent_equip_item,":player_agent","itm_british_light_dragoon_pants"),
        #(agent_equip_item,":player_agent","itm_british_lightdragoon_shako_ranker"),
        #(agent_equip_item,":player_agent","itm_br_cavalry_gloves_short"),
        #(agent_equip_item,":player_agent","itm_british_carbine"),
        #(agent_equip_item,":player_agent","itm_bullets"),
        #(agent_equip_item,":player_agent","itm_british_light_cav_sabre"),
        #(agent_set_wielded_item,":player_agent","itm_british_carbine",0),
        #(entry_point_get_position,pos3,2),
        #(agent_set_position,":player_agent",pos3),
        
        (troop_clear_inventory, "$g_player_troop"),
        (troop_add_item, "$g_player_troop","itm_british_light_dragoon",0),
        (troop_add_item, "$g_player_troop","itm_british_light_dragoon_pants",0),
        (troop_add_item, "$g_player_troop","itm_british_lightdragoon_shako_ranker",0),
        (troop_add_item, "$g_player_troop","itm_br_cavalry_gloves_short",0),
        #(troop_add_item, "$g_player_troop","itm_british_carbine",0),
        #(troop_add_item, "$g_player_troop","itm_bullets",0),
        #(troop_add_item, "$g_player_troop","itm_british_light_cav_sabre",0),
        (troop_equip_items, "$g_player_troop"),
        (store_current_scene, ":cur_scene"),
        (modify_visitors_at_site, ":cur_scene"),
        (add_visitors_to_current_scene, 2, "$g_player_troop", 1),
        
        (assign,"$g_tutorial_targets_destroyed",0),
        
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_12"),
        (assign,"$g_tutorial_state",11),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_12"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",11)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_12"),
      ]),
      
      (0, 0.5, ti_once, [(eq,"$g_tutorial_state",11)],
      [
        (get_player_agent_no,":player_agent"),
        (agent_equip_item,":player_agent","itm_british_carbine"),
        (agent_equip_item,":player_agent","itm_bullets"),
        (agent_equip_item,":player_agent","itm_british_light_cav_sabre"),
        (agent_set_wielded_item,":player_agent","itm_british_carbine",0),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",11),
        (get_player_agent_no,":player_agent"),
        (agent_get_horse,":horse",":player_agent"),
        (gt,":horse",-1),
      ],
      [ 
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_13"),
        (assign,"$g_tutorial_state",12),
        #Initialise arrow
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (entry_point_get_position, pos0, 4),
        (position_set_z_to_ground_level, pos0),
        (prop_instance_stop_animating,":prop_instance"),
        (prop_instance_set_position, ":prop_instance", pos0),
        (assign, "$g_pointer_arrow_height_adder", 10),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_13"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",12)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_13"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",12),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos1,":player_agent"),
        (get_distance_between_positions_in_meters,":dist",pos1,pos0),
        (le,":dist",2),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_14"),
        (assign,"$g_tutorial_target_hit",0),
        (assign,"$g_tutorial_state",13),
        #Clean up arrow
        (assign, "$g_pointer_arrow_height_adder", -1000),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_14"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",13)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_14"),
      ]),
      
      (0, 1, ti_once, [
        (eq,"$g_tutorial_state",13),
        (eq,"$g_tutorial_target_hit",0),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_british_carbine"),
        (assign,":is_loaded",1), 
        (try_for_range,":equipment_slot",ek_item_0,ek_head),
          (agent_get_item_slot, ":item_id", ":player_agent", ":equipment_slot"),
          (eq,":item_id","itm_british_carbine"),
          (agent_get_item_cur_ammo, ":is_loaded", ":player_agent", ":equipment_slot"),
        (try_end),
        (eq,":is_loaded",0), 
      ],
      [
        (eq,"$g_tutorial_state",13),
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_15"),
        (assign,"$g_tutorial_state",14),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_15"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",14)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_15"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",14),
        (eq,"$g_tutorial_target_hit",1),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_16"),
        (assign,"$g_tutorial_state",15),
        (assign, "$g_tutorial_path",1),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_16"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",13),
        (eq,"$g_tutorial_target_hit",1),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_17"),
        (assign,"$g_tutorial_state",15),
        (assign, "$g_tutorial_path",2),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_17"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",15)],
      [
        (tutorial_message_set_background, 1),
        (try_begin),
          (eq, "$g_tutorial_path",1),
          (tutorial_message,"str_tutorial_info_16"),
        (else_try),
          (eq, "$g_tutorial_path",2),
          (tutorial_message,"str_tutorial_info_17"),
        (try_end),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",15),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_british_light_cav_sabre"),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_18"),
        (assign,"$g_tutorial_state",16),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_18"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",16)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_18"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",16),
        (eq,"$g_tutorial_targets_destroyed",6),
      ],
      [
        #(tutorial_message_set_background, 1),
        #(tutorial_message,"str_tutorial_info_19"),
        (assign,"$g_tutorial_state",17),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_19"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",17)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_19"),
      ]),
      
      (0, 7, ti_once, [
        (eq,"$g_tutorial_state",17),
      ],
      [
        #Initialise arrow
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (entry_point_get_position, pos0, 6),
        (position_set_z_to_ground_level, pos0),
        (prop_instance_stop_animating,":prop_instance"),
        (prop_instance_set_position, ":prop_instance", pos0),
        (assign, "$g_pointer_arrow_height_adder", 120),
        
        (get_player_agent_no,":player_agent"),
        (agent_get_horse,":horse",":player_agent"),
        (try_begin),
          (gt,":horse",-1),
          (agent_start_running_away, ":horse"),
          (agent_fade_out,":horse"),
        (try_end),
        (troop_clear_inventory, "$g_player_troop"),
        (troop_add_item, "$g_player_troop","itm_british_artillery_ranker",0),
        (troop_add_item, "$g_player_troop","itm_french_voltigeur_officer_pants",0),
        (troop_add_item, "$g_player_troop","itm_british_artillery_shako_ranker",0),
        (troop_add_item, "$g_player_troop","itm_ramrod",0),
        (troop_add_item, "$g_player_troop","itm_cannon_lighter",0),
        (troop_equip_items, "$g_player_troop"),
        (store_current_scene, ":cur_scene"),
        (modify_visitors_at_site, ":cur_scene"),
        (add_visitors_to_current_scene, 5, "$g_player_troop", 1),

        (assign,"$g_tutorial_state",18),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_20"),
      ]),
      
      (0, 0, 0, [
        (is_between,"$g_tutorial_state",18,25),
        (neg|is_presentation_active, "prsnt_multiplayer_artillery_icons"),
      ],
      [
        (start_presentation, "prsnt_multiplayer_artillery_icons"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",18)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_20"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",18),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (this_or_next|eq,":item_id","itm_cannon_cartridge_round"),
        (eq,":item_id","itm_cannon_cartridge_canister"),
      ],
      [
        (assign,"$g_tutorial_state",19),
        #Clean up arrow
        (assign, "$g_pointer_arrow_height_adder", -1000),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_21"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",19)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_21"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",19),
        (get_player_agent_no,":player_agent"),
        (agent_get_wielded_item,":item_id",":player_agent",0),
        (eq,":item_id","itm_ramrod"),
      ],
      [
        (assign,"$g_tutorial_state",20),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_22"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",20)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_22"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",20),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (assign,":close",999999),
        (scene_prop_get_num_instances,":num","spr_mm_aim_button"),
        (try_for_range,":inst",0,":num"),
          (scene_prop_get_instance,":instance_no","spr_mm_aim_button",":inst"),
          (prop_instance_get_position,pos3,":instance_no"),
          (get_distance_between_positions_in_meters,":dist",pos2,pos3),
          (lt,":dist",":close"),
          (assign,":close",":dist"),
          (assign,":instance_id",":instance_no"),
        (try_end), 
        (call_script,"script_cannon_child_find_cannon_instance",":instance_id"),
        (assign,":cannon_instance",reg0),
        (scene_prop_get_slot,":just_fired",":cannon_instance",scene_prop_slot_is_loaded),
        (eq,":just_fired",1),
      ],
      [
        (assign,"$g_tutorial_state",21),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_23"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",21)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_23"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",21),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (assign,":close",999999),
        (scene_prop_get_num_instances,":num","spr_mm_aim_button"),
        (try_for_range,":inst",0,":num"),
          (scene_prop_get_instance,":instance_no","spr_mm_aim_button",":inst"),
          (prop_instance_get_position,pos3,":instance_no"),
          (get_distance_between_positions_in_meters,":dist",pos2,pos3),
          (lt,":dist",":close"),
          (assign,":close",":dist"),
          (assign,":instance_id",":instance_no"),
        (try_end), 
        (call_script,"script_cannon_child_find_cannon_instance",":instance_id"),
        (assign,":cannon_instance",reg0),
        (scene_prop_get_slot,":just_fired",":cannon_instance",scene_prop_slot_just_fired),
        (eq,":just_fired",0),
      ],
      [
        (assign,"$g_tutorial_state",22),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_24"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",22)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_24"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",22),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (assign,":close",999999),
        (scene_prop_get_num_instances,":num","spr_mm_aim_button"),
        (try_for_range,":inst",0,":num"),
          (scene_prop_get_instance,":instance_no","spr_mm_aim_button",":inst"),
          (prop_instance_get_position,pos3,":instance_no"),
          (get_distance_between_positions_in_meters,":dist",pos2,pos3),
          (lt,":dist",":close"),
          (assign,":close",":dist"),
          (assign,":instance_id",":instance_no"),
        (try_end), 
        (call_script,"script_cannon_child_find_cannon_instance",":instance_id"),
        (assign,":cannon_instance",reg0),
        (scene_prop_get_slot,":control_agent",":cannon_instance",scene_prop_slot_controller_agent),
        (eq,":control_agent",":player_agent"),
      ],
      [
        (assign,"$g_tutorial_state",23),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_25"),
      ]),
      
      (0, 0, 0, [(eq,"$g_tutorial_state",23)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_tutorial_info_25"),
      ]),
      
      (0, 0.5, ti_once, [
        (eq,"$g_tutorial_state",23),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (assign,":close",999999),
        (scene_prop_get_num_instances,":num","spr_mm_aim_button"),
        (try_for_range,":inst",0,":num"),
          (scene_prop_get_instance,":instance_no","spr_mm_aim_button",":inst"),
          (prop_instance_get_position,pos3,":instance_no"),
          (get_distance_between_positions_in_meters,":dist",pos2,pos3),
          (lt,":dist",":close"),
          (assign,":close",":dist"),
          (assign,":instance_id",":instance_no"),
        (try_end), 
        (call_script,"script_cannon_child_find_cannon_instance",":instance_id"),
        (assign,":cannon_instance",reg0),
        (scene_prop_get_slot,":just_fired",":cannon_instance",scene_prop_slot_just_fired),
        (eq,":just_fired",1),
      ],
      [
        (assign,"$g_tutorial_state",24),
        (tutorial_message_set_background, 1),
        (agent_stop_sound,"$g_tutorial_dummy_agent"),
        (agent_play_sound,"$g_tutorial_dummy_agent","snd_tutorial_voice_26"),
        (tutorial_message,"str_tutorial_info_26"),
      ]),
      
      ### TESTING TRIGGER
      (0, 0, 1, [(key_clicked,key_m)],
      [
        (val_add,"$g_tutorial_state",1),
      ]),
      
    ],
  ),
  
  (
    "quick_battle_battle",mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      
      (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      #MM
      #multiplayer_server_aim_cannon,multiplayer_cannon,,multiplayer_kneel,
      #multiplayer_server_drowning,
      multiplayer_client_voicecommands,
      multiplayer_server_order_voicecommands,
      #multiplayer_server_start_idle_animation,
      multiplayer_client_spyglass,
      #multiplayer_client_drowning,
    
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         
         (store_random_in_range, ":randomized_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomized_addition_courage"), 
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (agent_get_team,":agent_team",":agent_no"),
         (try_begin),
           (eq,":agent_team",0),
           (store_sub,":division_no",":entry_no",1),
           (agent_set_division,":agent_no",":division_no"),
         (else_try),
           (eq,":agent_team",1),
           (store_sub,":division_no",":entry_no",11),
           (agent_set_division,":agent_no",":division_no"),
         (try_end),
         
         #Replaced by entry_no trigger param
         #(call_script,"script_custom_battle_assign_agent_division",":agent_no"),
         ]),
      		 
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        #(call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),
 		 
     # (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
     #  [
     #   (start_presentation,"prsnt_new_order_stuff"),
     #  ]),
  		 
     # (0, 0, 1, [], #Volley fire
     #  [
     #   (call_script, "script_volley_fire"),
     #  ]),
       
      (0, 0, ti_once, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
     # (0, 0, ti_once, [],
     #   [
     #    (try_for_range,":unused",0,20),
     #     (init_position,pos1),
     #     (set_spawn_position,pos1),
     #     (spawn_scene_prop,"spr_formation_locator"),
     #    (try_end),
     #  
     #    #Order team 1 Army
     #    (assign,":entry_no",1),
     #    (try_for_range,":division",0,9),
     #      (troop_get_slot,":troop_value","trp_custom_battle_dummy",":division"),
     #      (gt,":troop_value",0),
     #      (entry_point_get_position,pos4,":entry_no"),
     #      #(team_give_order, 0, ":division", mordr_hold),
     #      #(team_set_order_position, 0, ":division", pos4),
     #      (scene_prop_get_instance,":instance","spr_formation_locator",":division"),
     #      (prop_instance_animate_to_position,":instance",pos4,0),
     #      (val_add,":entry_no",1),
     #    (try_end),
     #  
     #    #Order team 2 Army
     #    (assign,":entry_no",11),
     #    (try_for_range,":division",0,9),
     #     (store_add,":division_slot",":division",10),
     #     (troop_get_slot,":troop_value","trp_custom_battle_dummy",":division_slot"),
     #     (gt,":troop_value",0),
     #     (entry_point_get_position,pos4,":entry_no"),
     #     #(team_give_order, 1, ":division", mordr_hold),
     #     #(team_set_order_position, 1, ":division", pos4),
     #     (scene_prop_get_instance,":instance","spr_formation_locator",":division_slot"),
     #     (prop_instance_animate_to_position,":instance",pos4,0),
     #     (val_add,":entry_no",1),
     #    (try_end),
     #    ]),
         
     # (0, 0, 0,
     #  [
     #    (call_script, "script_iterate_pointer_arrow"),
     #    ], []),
         
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,

      (ti_before_mission_start, 0, 0, [],
       [
         (assign,":fog_colour",0xFFFFFF),
          # Day Time
         (try_begin),
           (eq,"$g_quick_battle_day_time_value",0),
           (scene_set_day_time, 7),
           (assign,":fog_colour",0xEDE3D6),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",1),
           (scene_set_day_time, 12),
           (assign,":fog_colour",0xFBFBFB),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",2),
           (scene_set_day_time, 18),
           (assign,":fog_colour",0xEDE3D6),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",3),
           (scene_set_day_time, 1),
           (assign,":fog_colour",0xBFBFBF),
         (try_end),
         
         # Fog
         (try_begin),
           (eq,"$g_quick_battle_fog_value",1),
           (set_fog_distance, 200, ":fog_colour"),
         (else_try),
           (eq,"$g_quick_battle_fog_value",2),
           (set_fog_distance, 100, ":fog_colour"),
         (else_try),
           (eq,"$g_quick_battle_fog_value",3),
           (set_fog_distance, 50, ":fog_colour"),
         (try_end),
         
         # Rain
         (try_begin),
           (gt,"$g_quick_battle_rain_value",0),
           (assign,":rain_type",1), #Rain
           (try_begin),
             (store_current_scene,":cur_scene"),
             (eq,":cur_scene","scn_quick_battle_scene_2"),
             (assign,":rain_type",2), #Snow
           (try_end),
           (set_rain,":rain_type","$g_quick_battle_rain_value"),
           (set_global_cloud_amount, 100),
         (try_end),
         
         (call_script,"script_custom_battle_set_division_names"),
         
         (try_for_range,":division",0,9),
           (store_add,":slot",slot_team1_unit_use_weapon,":division"),
           (troop_set_slot,"trp_ai_tactics_dummy",":slot",unit_use_firearms),
           (store_add,":slot",slot_team2_unit_use_weapon,":division"),
           (troop_set_slot,"trp_ai_tactics_dummy",":slot",unit_use_firearms),
         (try_end),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
        # Fog needs to be set both before and after mission start...
         (assign,":fog_colour",0xFFFFFF),
         (try_begin),
           (eq,"$g_quick_battle_day_time_value",0),
           (assign,":fog_colour",0xEDE3D6),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",1),
           (assign,":fog_colour",0xFBFBFB),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",2),
           (assign,":fog_colour",0xEDE3D6),
         (else_try),
           (eq,"$g_quick_battle_day_time_value",3),
           (assign,":fog_colour",0xA0A0A0),
         (try_end),
         
         (try_begin),
           (eq,"$g_quick_battle_fog_value",1),
           (set_fog_distance, 200, ":fog_colour"),
         (else_try),
           (eq,"$g_quick_battle_fog_value",2),
           (set_fog_distance, 100, ":fog_colour"),
         (else_try),
           (eq,"$g_quick_battle_fog_value",3),
           (set_fog_distance, 50, ":fog_colour"),
         (try_end),
         
          (assign,"$g_last_tactic_change_at",0),
          
        # (init_position,pos1),
        # (set_spawn_position,pos1),
        # (spawn_scene_prop,"spr_pointer_arrow"),
        # (assign,"$g_hold_position_arrow_instance",reg0),
        # (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         
         #(call_script,"script_custom_battle_set_division_names"),
         ]),

      common_battle_init_banner,
      
      (0, 0, ti_once, [],
        [
          (assign, "$g_battle_result", 0),
          (call_script, "script_combat_music_set_situation_with_culture"),
         ]),
       
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
      
      #AI Triggers
      (0, 2, ti_once, [
          #(store_mission_timer_a,":mission_time"),(ge,":mission_time",2),
          ],
       [(call_script, "script_select_battle_tactic"),
        (call_script, "script_battle_tactic_init"),
        #(call_script, "script_battle_calculate_initial_powers"), #deciding run away method changed and that line is erased
        ]),
      
      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [ (store_mission_timer_a,":mission_time"),
                  (ge,":mission_time",25),  
                ], 
        [
          (try_for_agents, ":agent_no"),
            (agent_is_active,":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),               
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
        ]), #controlling courage score and if needed deciding to run away for each agent

      (5, 2, 0, [
          #(store_mission_timer_a,":mission_time"),

          #(ge,":mission_time",2),
          
          (call_script, "script_battle_tactic_apply"),
          ], []), #applying battle tactic

      (1, 0, 0, [],
        [
          (try_for_range,":division",0,9),
            (try_begin),
              (eq,"$ai_team_1",0),
              (store_add,":slot",slot_team1_unit_use_weapon,":division"),
            (else_try),
              (store_add,":slot",slot_team2_unit_use_weapon,":division"),
            (try_end),
            (troop_get_slot,":use_weapon_type","trp_ai_tactics_dummy",":slot"),
            (try_begin),
              (eq,":use_weapon_type",unit_use_melee),
              (team_give_order, "$ai_team_1", ":division", wordr_use_melee_weapons),
            (else_try),
              (team_give_order, "$ai_team_1", ":division", wordr_use_any_weapon),
            (try_end),
          (try_end),
          
          (try_begin),
            (ge, "$ai_team_2", 0),
            (try_for_range,":division",0,9),
              (try_begin),
                (eq,"$ai_team_2",0),
                (store_add,":slot",slot_team1_unit_use_weapon,":division"),
              (else_try),
                (store_add,":slot",slot_team2_unit_use_weapon,":division"),
              (try_end),
              (troop_get_slot,":use_weapon_type","trp_ai_tactics_dummy",":slot"),
              (try_begin),
                (eq,":use_weapon_type",unit_use_melee),
                (team_give_order, "$ai_team_2", ":division", wordr_use_melee_weapons),
              (else_try),
                (team_give_order, "$ai_team_2", ":division", wordr_use_any_weapon),
              (try_end),
            (try_end),
          (try_end),
         ]),
         
      #common_battle_order_panel,
      #common_battle_order_panel_tick,

    ],
  ),



    (
    "multiplayer_dm",mtf_battle_mode,-1, #deathmatch mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ 
      
      multiplayer_server_check_polls, multiplayer_server_generate_build_points,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
                                                                        # to be able to edit maps without damaging any headquarters flags ext.
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/1

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [         
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
      
      (1, 0, 0, [(multiplayer_is_server),],
       [
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1.07, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0.1, 0, 0, [(multiplayer_is_server),
                   (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
                   (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
                   (gt, ":total_req", 0),],
       [
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
         #checking for restarting the map
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           
           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
			
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),],
       [
			   (assign, "$g_round_ended", 0),
			   (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
         #MM
         #(call_script, "script_multiplayer_mm_reset_stuff_after_round"),
			 ]
			 ),
			 
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),

    (
    "multiplayer_tdm",mtf_battle_mode,-1, #team_deathmatch mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,
      
      multiplayer_server_check_polls, multiplayer_server_generate_build_points,
      multiplayer_server_bonuses, multiplayer_server_auto_ff,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_match_start_time", 0),
         (try_end),
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/2
		 

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         #adding 1 score points to killer agent's team. (special for "headquarters" and "team deathmatch" mod)
         (try_begin),
           (agent_is_active,":dead_agent_no"),
           (agent_is_active,":killer_agent_no"),
           (agent_is_human, ":dead_agent_no"),
           (agent_is_human, ":killer_agent_no"),
           (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
           (lt, ":killer_agent_team", multi_team_spectator), #0 or 1 is ok
           (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (team_get_score, ":team_score", ":killer_agent_team"),
           (val_add, ":team_score", 1),
           (team_set_score, ":killer_agent_team", ":team_score"),
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 1, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1.07, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),
      
      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

			(1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),],
       [
			   (assign, "$g_round_ended", 0),
			   (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
         #MM
         #(call_script, "script_multiplayer_mm_reset_stuff_after_round"),
			 ]
			 ),
			 
      (30, 0, 0, [(multiplayer_is_server),],
       [
         #auto team balance control in every 20 seconds (tdm)
         (call_script, "script_check_team_balance"),
         ]),

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),
  
  (
    "multiplayer_hq", mtf_battle_mode,-1, #headquarters mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,
      
      multiplayer_server_check_polls, multiplayer_server_generate_build_points,
      multiplayer_server_bonuses, multiplayer_server_auto_ff,

      (0, 0, 5, [ #Conquest bots - update every 5 sec
                  (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0),],
       [
        (try_for_agents,":agent"),
          (agent_is_active,":agent"),
          (agent_is_alive,":agent"),
          (agent_is_human,":agent"),
          (agent_is_non_player,":agent"),
          
          (agent_get_slot,":agent_behaviour",":agent",slot_agent_behaviour),
          (neq,":agent_behaviour",bot_type_skirmish),
          
          (agent_get_team,":team",":agent"),
          (val_add,":team",1),
          (agent_get_position,pos27,":agent"),
          
          (agent_get_slot,":flag_target",":agent",slot_agent_flag_target),
          (try_begin),
            (gt,":flag_target",-1),
            (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_target"),
            (assign,":continue",0),
            (try_begin),
              (eq,":agent_behaviour",bot_type_defender),
              (troop_slot_eq, "trp_multiplayer_data", ":cur_flag_slot", ":team"), #Defenders go to friendly flags
              (assign,":continue",1),
            (else_try),
              (neg|troop_slot_eq, "trp_multiplayer_data", ":cur_flag_slot", ":team"), #Flag belongs to other team
              (assign,":continue",1),
            (try_end),
            (eq,":continue",1),
          (else_try),
            (assign,":flag_opt_1",-1),
            (assign,":min_distance",100000),
            (assign,":first_flag",1),
            (try_for_range,":flag_no",0,"$g_number_of_flags"), #Try for flags
              (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
              (assign,":continue",0),
              (try_begin),
                (eq,":agent_behaviour",bot_type_attacker),
                (neg|troop_slot_eq, "trp_multiplayer_data", ":cur_flag_slot", ":team"), #Flag belongs to other team
                (assign,":continue",1),
              (else_try),
                (eq,":agent_behaviour",bot_type_defender),
                (troop_slot_eq, "trp_multiplayer_data", ":cur_flag_slot", ":team"), #Defenders go to friendly flags
                (assign,":continue",1),
              (try_end),
              (eq,":continue",1),
              (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
              (prop_instance_get_position, pos28, ":pole_id"),
              (get_distance_between_positions,":distance",pos27,pos28),
              (lt,":distance",":min_distance"),
              (assign,":min_distance",":distance"),
              (try_begin),
                (eq,":first_flag",1),
                (assign,":flag_opt_2",":flag_no"),
                (assign,":first_flag",0),
              (else_try),
                (assign,":flag_opt_2",":flag_opt_1"),
              (try_end),
              (assign,":flag_opt_1",":flag_no"),
            (try_end),
            (gt,":flag_opt_1",-1),
            (store_random_in_range,":option",0,2),
            (try_begin),
              (eq,":option",0),
              (assign,":destination_flag",":flag_opt_1"),
            (else_try),
              (assign,":destination_flag",":flag_opt_2"),
            (try_end),
            (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":destination_flag"), 
            (prop_instance_get_position, pos28, ":pole_id"),
            (agent_set_scripted_destination,":agent",pos28,1),
          (try_end),
        (try_end),
       ]),
       
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
         (try_begin), #For bots
           (multiplayer_is_server),
           (agent_is_non_player,":agent_no"),
           (agent_set_slot,":agent_no",slot_agent_flag_target,-1),
           
           (store_random_in_range,":percentage",0,100), #Random percentage
           (try_begin),
             (lt,":percentage",70), #70 percent attackers
             (agent_set_slot,":agent_no",slot_agent_behaviour,bot_type_attacker),
           #(else_try),
           #  (lt,":percentage",95), #25 percent defenders
           #  (agent_set_slot,":agent_no",slot_agent_behaviour,bot_type_defender),
           (else_try), #The rest are randomers :P
             (agent_set_slot,":agent_no",slot_agent_behaviour,bot_type_skirmish),
           (try_end),
         (try_end),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (store_mul, ":initial_hq_score", "$g_multiplayer_game_max_points", 10000),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_match_start_time", 0),
         (try_end),
         (assign, "$g_score_team_1", ":initial_hq_score"),
         (assign, "$g_score_team_2", ":initial_hq_score"),
         
         (try_begin),
           (scene_prop_get_num_instances, ":num_instances", "spr_mm_additional_conquest_points"),
           (gt,":num_instances",0),
           (scene_prop_get_instance,":instance_id","spr_mm_additional_conquest_points",0),
           (prop_instance_get_variation_id, ":team_no", ":instance_id"),
           (is_between,":team_no",0,2),
           (prop_instance_get_variation_id_2, ":extra_points", ":instance_id"), #In display score
           (gt,":extra_points",0),
           (store_sqrt,":extra_points_multiplier","$g_multiplayer_game_max_points"), #More than 300 max points give a minor increase, lower gives a minor decrease
           (val_mul,":extra_points_multiplier",2),
           (val_sub,":extra_points_multiplier",34),
           (val_add,":extra_points_multiplier","$g_multiplayer_point_gained_from_flags"), #The % Points gained from flags directly affects the additional score
           (val_mul,":extra_points_multiplier",100),  #Default = 10000, in real score.
           (val_mul,":extra_points",":extra_points_multiplier"),
           (try_begin),
             (eq,":team_no",0),
             (val_add, "$g_score_team_1", ":extra_points"),
           (else_try),
             (eq,":team_no",1),
             (val_add, "$g_score_team_2", ":extra_points"),
           (try_end),
         (try_end),

         (try_for_range, ":cur_flag_slot", multi_data_flag_owner_begin, multi_data_flag_owner_end),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
         (try_end),
           
         (try_begin),
           (multiplayer_is_server),
           (try_for_range, ":cur_flag_slot", multi_data_flag_pull_code_begin, multi_data_flag_pull_code_end),
             (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
           (try_end),
         (try_end),

         (call_script, "script_multiplayer_init_mission_variables"),

         (try_begin),
           (multiplayer_is_server),
           (team_set_score, 0, "$g_multiplayer_game_max_points"),
           (team_set_score, 1, "$g_multiplayer_game_max_points"),
         (try_end),
         
         #MM
         (assign,"$g_conquest_map_end_confirm",0),
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),         
         (set_spawn_effector_scene_prop_kind, 0, "$team_1_flag_scene_prop"), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to $team_1_flag_scene_prop
         (set_spawn_effector_scene_prop_kind, 1, "$team_2_flag_scene_prop"), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to $team_2_flag_scene_prop
         (server_add_message_to_log,"str_map_changed"), #patch1115 fix 3/3
         
         (scene_prop_get_num_instances, ":num_instances_of_red_headquarters_flag", "spr_headquarters_flag_red"),
         (scene_prop_get_num_instances, ":num_instances_of_blue_headquarters_flag", "spr_headquarters_flag_blue"),
         (scene_prop_get_num_instances, ":num_instances_of_gray_headquarters_flag", "spr_headquarters_flag_gray"),  
         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           (assign, "$g_number_of_flags", 0),
           
           # get base flag custom name ids
           (assign, ":flag1_name", -1),
           (assign, ":flag2_name", -1),
           (try_for_prop_instances, ":instance_id", "spr_headquarters_base_flag_names", somt_object),
             (prop_instance_get_variation_id, ":name1", ":instance_id"),
             (prop_instance_get_variation_id_2, ":name2", ":instance_id"),
             
             (try_begin),
               (gt, ":name1", 0),
               (store_sub, ":flag1_name", ":name1", 1),
             (try_end),
             
             (try_begin),
               (gt, ":name2", 0),
               (store_sub, ":flag2_name", ":name2", 1),
             (try_end),
           (try_end),
         
           #place base flags
           (entry_point_get_position, pos1, multi_base_point_team_1),
           (entry_point_get_position, pos3, multi_base_point_team_1),

           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),           
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),           
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_flag_gray_code_only", 0),           
         
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 1),
           
           (troop_set_slot, "trp_flag_custom_strings_dummy", "$g_number_of_flags", ":flag1_name"), # set flag custom name
           
           (val_add, "$g_number_of_flags", 1),

           (entry_point_get_position, pos2, multi_base_point_team_2),
           (entry_point_get_position, pos3, multi_base_point_team_2),
         
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_flag_gray_code_only", 0),                    
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 2),
           
           (troop_set_slot, "trp_flag_custom_strings_dummy", "$g_number_of_flags", ":flag2_name"), # set flag custom name
           
           (val_add, "$g_number_of_flags", 1),

           (call_script,"script_multiplayer_initalise_flags_common"),
           
         (else_try),
           #these three lines both used in calculation of $g_number_of_flags and below part removing of initially placed flags
           (assign, "$g_number_of_flags", 2),
           (val_add, "$g_number_of_flags", ":num_instances_of_red_headquarters_flag"),
           (val_add, "$g_number_of_flags", ":num_instances_of_blue_headquarters_flag"),
           (val_add, "$g_number_of_flags", ":num_instances_of_gray_headquarters_flag"),         
         (try_end),

         #remove initially placed flags
         (try_for_range, ":flag_no", 0, ":num_instances_of_red_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_red", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),
         (try_for_range, ":flag_no", 0, ":num_instances_of_blue_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_blue", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),
         (try_for_range, ":flag_no", 0, ":num_instances_of_gray_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),

         (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
           (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", 0),
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
       ]),         

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         #adding 1 score points to killer agent's team. (special for "headquarters" and "team deathmatch" mod)
         (try_begin),
           (agent_is_active,":dead_agent_no"),
           (agent_is_active,":killer_agent_no"),
           (agent_is_human, ":dead_agent_no"),
           (agent_is_human, ":killer_agent_no"),
           (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
           (lt, ":killer_agent_team", multi_team_spectator), #0 or 1 is ok
           (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
           (lt, ":dead_agent_team", multi_team_spectator), #0 or 1 is ok
           
           (team_get_score, ":team_score", ":dead_agent_team"),
           (val_sub, ":team_score", 1),
           (val_max, ":team_score", 0), # dont allow negative value.
           (call_script, "script_team_set_score", ":dead_agent_team", ":team_score"),
           #(assign,"$g_team_score_is_changed",1),
           
           # The rest only for da server
           (multiplayer_is_server),
           
           (try_begin),
             (eq, ":dead_agent_team", 0),
             (val_sub, "$g_score_team_1", 10000), 
             (val_max, "$g_score_team_1", 0), # dont allow negative value.
           (else_try),
             (val_sub, "$g_score_team_2", 10000), 
             (val_max, "$g_score_team_1", 0), # dont allow negative value.
           (try_end),
           
           # Vincenzo begin
           (agent_get_player_id, ":dead_player", ":dead_agent_no"),
           (player_is_active,":dead_player"),
           
           (store_mission_timer_a, ":current_time"),
           (store_sub, ":respawntime", ":current_time", "$g_hq_last_spawn_wave"),
           (store_sub, ":respawntime_left", "$g_multiplayer_respawn_period", ":respawntime"),
           
           (multiplayer_send_int_to_player, ":dead_player", multiplayer_event_return_respawn_period, ":respawntime_left"),
           # Vincenzo end
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
      [
        #trigger for (a) counting seconds of flags being owned by their owners & (b) to calculate seconds past after that flag's pull message has shown          
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          #part a: counting seconds of flags being owned by their owners
          (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owned_seconds", "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot"),
          (val_add, ":cur_flag_owned_seconds", 1),
          (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", ":cur_flag_owned_seconds"),
          #part b: to calculate seconds past after that flag's pull message has shown
          (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
          (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
          (try_begin),
            (ge, ":cur_flag_pull_code", 100),
            (lt, ":cur_flag_pull_message_seconds_past", 25),
            (val_add, ":cur_flag_pull_code", 1),
            (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":cur_flag_pull_code"),
          (try_end),
        (try_end),        
      ]),               
      # Vincenzo change seconds
      (1.06, 0, 0, [(multiplayer_is_server),], #if this trigger takes lots of time in the future and make server machine runs headqurters mod
                    #very slow with lots of players make period of this trigger 1 seconds, but best is 0. Currently
                    #we are testing this mod with few players and no speed program occured.
      [
        #main trigger which controls which agent is moving/near which flag.
        (set_fixed_point_multiplier,100),
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),
        
          (assign, ":number_of_agents_around_flag_team_1", 0),
          (assign, ":number_of_agents_around_flag_team_2", 0),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.

          # REMOVED TO ALLOW BOTS TO CAPTURE FLAGS
          #(try_for_range, ":player_no", 0, ":num_players"),
          #  (player_is_active, ":player_no"),
          #  (player_get_agent_id, ":cur_agent", ":player_no"),
          #  (ge, ":cur_agent", 0),
          (try_for_agents,":cur_agent",pos3,601),
            (agent_is_active,":cur_agent"),
            (agent_is_human,":cur_agent"),
            #/Added above
            (agent_is_alive, ":cur_agent"),
            (agent_get_team, ":cur_agent_team", ":cur_agent"),
            (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
            (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),
            (get_sq_distance_between_position_heights, ":squared_height_dist", pos3, pos1),
            (val_add, ":squared_dist", ":squared_height_dist"),
            # Vincenzo begin
            (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags + 900),
            # Vincenzo end
            (try_begin),
              (eq, ":cur_agent_team", 0),
              (val_add, ":number_of_agents_around_flag_team_1", 1),
            (else_try),
              (eq, ":cur_agent_team", 1),
              (val_add, ":number_of_agents_around_flag_team_2", 1),
            (try_end),
          (try_end),

          (try_begin),
            (this_or_next|neq, ":old_team_1_agent_count", ":number_of_agents_around_flag_team_1"),
            (neq, ":old_team_2_agent_count", ":number_of_agents_around_flag_team_2"),

            (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

            (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
            (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
            (store_div, ":cur_flag_puller_team_last", ":cur_flag_pull_code", 100),

            (try_begin),        
              (assign, ":continue", 0),
              (try_begin),
                (neq, ":cur_flag_owner", 1),
                (eq, ":old_team_1_agent_count", 0),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 1),
                (assign, ":continue", 1),
              (else_try),
                (neq, ":cur_flag_owner", 2),
                (eq, ":old_team_2_agent_count", 0),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 2),
                (assign, ":continue", 1),
              (try_end),
 
              (eq, ":continue", 1),

              (store_mul, ":puller_team_multiplied_by_100", ":puller_team", 100),
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":puller_team_multiplied_by_100"),

              (this_or_next|neq, ":cur_flag_puller_team_last", ":puller_team"),
              (ge, ":cur_flag_pull_message_seconds_past", 25),

              (store_mul, ":flag_code", ":puller_team", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_is_pulling, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------     
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_is_pulling, ":flag_code"),
              (try_end),
              
              # Vincenzo begin
              (this_or_next|eq, ":flag_no", 0),
              (eq, ":flag_no", 1),
              
              (assign, ":cur_faction", 0),
              (try_begin),
                (eq, ":flag_no", 0),
                (assign, ":cur_faction", "$g_multiplayer_team_1_faction"),
                (assign, ":cur_faction_nr", 1),
                #(str_store_faction_name, s1, "$g_multiplayer_team_1_faction"), # faction 1
              (else_try),
                (assign, ":cur_faction", "$g_multiplayer_team_2_faction"),
                (assign, ":cur_faction_nr", 2),
                #(str_store_faction_name, s1, "$g_multiplayer_team_2_faction"), # faction 2
              (try_end),
              
              (val_sub, ":cur_faction", "fac_britain"),
              (val_add, ":cur_faction", "str_kingdom_1_adjective"),
              (str_store_string, s1, ":cur_faction"),
              
              (try_begin),
                (eq, ":puller_team", ":cur_faction_nr"),
                (str_store_string, s4, "str_server_hq_base_retake_s1"),
              (else_try),
                (str_store_string, s4, "str_server_hq_base_attack_s1"),
              (try_end),
              
              (call_script, "script_multiplayer_broadcast_message"), # Broadcast message
              # Vincenzo end
            (try_end),

            (try_begin),
              (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
              (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),        
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
              #for only server itself----------------------------
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (assign, ":new_flag_owner", -1),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.            

          (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

          (try_begin),
            (try_begin),
              (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 1),
              (eq, ":flag_visibility", 0),
              (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 2),
              (eq, ":flag_visibility", 0),                    
              (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),        
              (assign, ":cur_shown_flag", 0),
            (try_end),

            #flag_id holds shown flag after this point
            (prop_instance_get_position, pos1, ":flag_id"), #pos1 holds gray/red/blue (current shown) flag position.

            (try_begin),
              (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),        
              # Vincenzo begin              
              (lt, ":squared_dist", multi_headquarters_distance_sq_to_change_flag + 500), #if distance is less than 2 meters
              # Vincenzo end
              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 2),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (neq, ":cur_shown_flag", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 0),
              (try_end),
            (else_try),
              (neq, ":cur_flag_owner", ":cur_shown_flag"),      
              (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),        
              (ge, ":squared_dist", multi_headquarters_distance_sq_to_set_flag), #if distance is more equal than 9 meters

              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (eq, ":cur_shown_flag", 1),
                (assign, ":new_flag_owner", 1),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":cur_shown_flag", 2),
                (assign, ":new_flag_owner", 2),
                (assign, ":new_shown_flag", 2),
              (try_end),        
            (try_end),
          (try_end),
        
          (try_begin),
            (ge, ":new_flag_owner", 0),
            (this_or_next|neq, ":new_flag_owner", ":cur_flag_owner"),
            (neq, ":cur_shown_flag", ":new_shown_flag"),

            (try_begin),
              (neq, ":cur_flag_owner", 0),
              (eq, ":new_flag_owner", 0),
              (try_begin),
                (eq, ":cur_flag_owner", 1),
                (assign, ":neutralizer_team", 2),
              (else_try),
                (eq, ":cur_flag_owner", 2),
                (assign, ":neutralizer_team", 1),
              (try_end),
              (store_mul, ":flag_code", ":neutralizer_team", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_neutralized, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------       
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_neutralized, ":flag_code"),
              (try_end),              
            (try_end),
        
            (try_begin),
              (neq, ":cur_flag_owner", ":new_flag_owner"),
              (neq, ":new_flag_owner", 0),
              (store_mul, ":flag_code", ":new_flag_owner", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_captured, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------     
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_captured, ":flag_code"),
              (try_end),              
            (try_end),

            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_set_num_agents_around_flag", ":flag_no", ":cur_flag_players_around"),
            #for only server itself-----------------------------------------------------------------------------------------------
            #(assign, ":number_of_total_players", 0),
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":cur_flag_players_around"),
              #(val_add, ":number_of_total_players", 1),
            (try_end),

            (store_mul, ":owner_code", ":new_flag_owner", 100),
            (val_add, ":owner_code", ":new_shown_flag"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_change_flag_owner", ":flag_no", ":owner_code"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":flag_no", ":owner_code"),          
            (try_end),

            (try_begin),
              (neq, ":new_flag_owner", 0),

              (try_begin),
                (eq, ":new_flag_owner", 1),
                (assign, ":number_of_players_around_flag", ":number_of_agents_around_flag_team_1"),
              (else_try),
                (assign, ":number_of_players_around_flag", ":number_of_agents_around_flag_team_2"),
              (try_end),

              (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
              (troop_get_slot, ":current_flag_owned_seconds", "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot"),              
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", 0),

              (val_min, ":current_flag_owned_seconds", 360), #360 seconds is max time for hq, this will limit money awarding by (180 x total_number_of_players)

              (try_begin),                                # MM - Changed scoring to different values to always award players with score points for capturing flags
                (le, ":number_of_players_around_flag", 2), # If 1 or 2 players, give 3 points each
                (assign, ":score_award_per_player", 3),
              (else_try),
                (le, ":number_of_players_around_flag", 5), # If 3, 4 or 5 players, give 2 points each
                (assign, ":score_award_per_player", 2),
              (else_try),
                (assign, ":score_award_per_player", 1), # Else give 1 point no matter how many players are capturing the flag
              (try_end),

              (prop_instance_get_position, pos3, ":pole_id"),
              
              (try_for_players, ":player_no", "$g_ignore_server"),
                (player_is_active, ":player_no"),
                (player_get_agent_id, ":cur_agent", ":player_no"),
                (agent_is_active,":cur_agent"),
                (agent_get_team, ":cur_agent_team", ":cur_agent"),
                (val_add, ":cur_agent_team", 1),
                (eq, ":cur_agent_team", ":new_flag_owner"),
                
                (agent_get_position, pos1, ":cur_agent"),  
                (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),
                (get_sq_distance_between_position_heights, ":squared_height_dist", pos3, pos1),
                (val_add, ":squared_dist", ":squared_height_dist"),
                # Vincenzo begin
                (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags + 900),        
                # Vincenzo end                
                (player_get_score, ":player_score", ":player_no"), #give score to player which helped flag to be owned by new_flag_owner team 
                (val_add, ":player_score", ":score_award_per_player"),
                (player_set_score, ":player_no", ":player_score"),                            
              (try_end),
            (try_end),
          (try_end),
        (try_end),
        ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
        #trigger for increasing score in each second.
        
        #First check if their are actually any players. 
        #Instead of doing that in the middle of the code, and do nothing if there aren't...
        (assign, ":any_active_players", 0),
        (assign, ":end_cond", multiplayer_player_loops_end),
        (try_for_range, ":player_no", "$g_player_loops_begin", ":end_cond"),
          (player_is_active, ":player_no"),
          (assign, ":any_active_players", 1),
          (assign, ":end_cond", 0),
        (try_end),
        (eq, ":any_active_players", 1),
        #So there are players, now we can continue calculating score
          
        (assign, ":number_of_team_1_flags", 0),
        (assign, ":number_of_team_2_flags", 0),

        #(assign, ":owned_flag_value", 0),        
        (assign, ":not_owned_flag_value", 0),
        
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

          (scene_prop_get_instance, ":flag_of_team_1", "$team_1_flag_scene_prop", ":flag_no"),
          (scene_prop_get_instance, ":flag_of_team_2", "$team_2_flag_scene_prop", ":flag_no"),
        
          (try_begin), #Team bases are worth 2 flags
            (this_or_next|eq, "$g_base_flag_team_1", ":flag_of_team_1"),
            (eq, "$g_base_flag_team_2", ":flag_of_team_2"),
            (assign, ":flag_value", 2),
          (else_try), #Normal flags are worth, well, 1 flag...
            (assign, ":flag_value", 1),
          (try_end),
        
          (try_begin),
            (eq, ":cur_flag_owner", 1),
            (val_add, ":number_of_team_1_flags", ":flag_value"),
            #(val_add, ":owned_flag_value", ":flag_value"),
          (else_try),
            (eq, ":cur_flag_owner", 2),
            (val_add, ":number_of_team_2_flags", ":flag_value"),
            #(val_add, ":owned_flag_value", ":flag_value"),
          (else_try),
            (val_add, ":not_owned_flag_value", ":flag_value"),
          (try_end),
        (try_end),
        
        # Vincenzo begin
        (try_begin),  # No flags for either team?
          (this_or_next|eq, ":number_of_team_1_flags", 0),
          (eq, ":number_of_team_2_flags", 0),
          
          (try_begin),
            (eq, ":number_of_team_1_flags", 0),
            (assign,":team_with_no_flags",0),
          (else_try),
            (eq, ":number_of_team_2_flags", 0),
            (assign,":team_with_no_flags",1),
          (try_end),
          
          #Checking if team with no flags has alive players
          (assign, ":end_cond",multiplayer_player_loops_end),
          (assign, ":at_least_one_alive_of_losing", 0),
          (try_for_range, ":player_no", "$g_player_loops_begin", ":end_cond"),
            (player_is_active, ":player_no"),
            (player_get_team_no, ":player_team", ":player_no"),
            
            (eq,":player_team",":team_with_no_flags"),
            
            (player_get_agent_id, ":player_agent_id", ":player_no"),
            (gt, ":player_agent_id", -1),
            (agent_is_active,":player_agent_id"),
            (agent_is_alive, ":player_agent_id"),
            (assign, ":at_least_one_alive_of_losing", 1), #At least one alive
            (assign, ":end_cond", 0),
          (try_end),
          
          (eq, ":at_least_one_alive_of_losing", 0), #No flags and no one is alive - the team loses
          (try_begin),
            (eq, ":team_with_no_flags", 0),
            (assign, "$g_score_team_1", 0),
          (else_try),
            (eq, ":team_with_no_flags", 1),
            (assign, "$g_score_team_2", 0),
          (try_end),
        (else_try), #Both teams have flags and/or players left
          (try_begin), #Calculate team 1 score loss
            (gt, "$g_score_team_1", 200000), #Once team reaches 20 points, stop auto-lowering score
            
            (store_mul,":flag_value_multiplier",50,"$g_multiplayer_point_gained_from_flags"), #Default: 50x100 = 5000
            (store_mul,":allied_flag_weight",":number_of_team_1_flags",":flag_value_multiplier"),
            (store_mul,":enemy_flag_weight",":number_of_team_2_flags",":flag_value_multiplier"),
            (store_mul,":neutral_flag_weight",":not_owned_flag_value",":flag_value_multiplier"),
            
            #Formula: (their_flag_weight - our_flag_weight) / 3 + neutral_flag_weight / 20
            (store_sub,":sub_score",":enemy_flag_weight",":allied_flag_weight"),
            (val_div,":sub_score",3),
            (store_div,":neutral_flag_weight",":neutral_flag_weight",20),
            (val_add,":sub_score",":neutral_flag_weight"),
            
            (val_max,":sub_score",0),#Can't get gain points...
            
            (val_sub, "$g_score_team_1", ":sub_score"), #And subtract the value from our score
          (try_end),
          
          (try_begin), #Calculate team 2 score loss
            (gt, "$g_score_team_2", 200000), #Once team reaches 20 points, stop auto-lowering score
            
            (store_mul,":flag_value_multiplier",50,"$g_multiplayer_point_gained_from_flags"), #Default: 50x100 = 5000
            (store_mul,":allied_flag_weight",":number_of_team_2_flags",":flag_value_multiplier"),
            (store_mul,":enemy_flag_weight",":number_of_team_1_flags",":flag_value_multiplier"),
            (store_mul,":neutral_flag_weight",":not_owned_flag_value",":flag_value_multiplier"),
            
            #Formula: (their_flag_weight - our_flag_weight) / 3 + neutral_flag_weight / 20
            (store_sub,":sub_score",":enemy_flag_weight",":allied_flag_weight"),
            (val_div,":sub_score",3),
            (store_div,":neutral_flag_weight",":neutral_flag_weight",20),
            (val_add,":sub_score",":neutral_flag_weight"),
            
            (val_max,":sub_score",0),#Can't get gain points...
            
            (val_sub, "$g_score_team_2", ":sub_score"), #And subtract the value from our score
          (try_end),
        (try_end),
        
        #Transfering real score into display score:
        (store_div, ":team_new_score_1", "$g_score_team_1", 10000),
        (try_begin),
          (lt, ":team_new_score_1", 0),
          (assign, ":team_new_score_1", 0),
        (try_end),
        (store_div, ":team_new_score_2", "$g_score_team_2", 10000),
        (try_begin),
          (lt, ":team_new_score_2", 0),
          (assign, ":team_new_score_2", 0),
        (try_end),
        
        #Assigning new scores:
        (team_get_score, ":team_score_1", 0),
        (team_get_score, ":team_score_2", 1),
        (try_begin),
          (this_or_next|neq, ":team_new_score_1", ":team_score_1"),
          (neq, ":team_new_score_2", ":team_score_2"), # Value is changed..
           
          (call_script, "script_team_set_score", 0, ":team_new_score_1"),
          (call_script, "script_team_set_score", 1, ":team_new_score_2"),
          (try_for_players, ":player_no", 1),
            (player_is_active, ":player_no"),
            (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, ":team_new_score_1", ":team_new_score_2"),
          (try_end),
        (try_end),
      ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
         # Vincenzo begin
         (store_mission_timer_a, ":current_time"),
         (store_sub, ":respawntime", ":current_time", "$g_hq_last_spawn_wave"),
        
         (this_or_next|le, "$g_hq_last_spawn_wave", "$g_multiplayer_respawn_period"),
         (gt, ":respawntime", "$g_multiplayer_respawn_period"),
         
         (assign,":flags_team_1",1),
         (assign,":flags_team_2",11),
         (assign,":end_cond","$g_number_of_flags"),
         (try_for_range,":flag_no",0,":end_cond"),
            (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
            (try_begin),
              (eq, ":cur_flag_owner", 1), # team 1
              (troop_set_slot, "trp_flags_owned_dummy", ":flags_team_1", ":flag_no"), # Store in slot number the flag_no
              (val_add,":flags_team_1",1),
            (else_try),
              (eq, ":cur_flag_owner", 2), # team 2
              (troop_set_slot, "trp_flags_owned_dummy", ":flags_team_2", ":flag_no"), # Store in slot number the flag_no
              (val_add,":flags_team_2",1),
            (try_end),
         (try_end),
         
         # Store team 1 spawns
         (assign, ":entrypoints_team_1", 1),
         (assign,":entrypoints_count_team_1",0),
         (assign, ":end_cond", ":flags_team_1"),
         (try_for_range,":flag_no",1,":end_cond"),
           (troop_get_slot, ":cur_flag_id", "trp_flags_owned_dummy", ":flag_no"),
           (call_script, "script_multiplayer_server_hq_get_entrypoints_for_flag",":cur_flag_id",":entrypoints_team_1"),
           (assign, ":entrypoints_team_1", reg0),
           (val_add, ":entrypoints_count_team_1", reg1),
         (try_end),
         
         # Store team 2 spawns
         (assign, ":entrypoints_team_2", 101),
         (assign,":entrypoints_count_team_2",0),
         (assign, ":end_cond", ":flags_team_2"),
         (try_for_range, ":flag_no", 11, ":end_cond"),
           (troop_get_slot, ":cur_flag_id", "trp_flags_owned_dummy", ":flag_no"),
           (call_script, "script_multiplayer_server_hq_get_entrypoints_for_flag",":cur_flag_id",":entrypoints_team_2"),
           (assign, ":entrypoints_team_2", reg0),
           (val_add, ":entrypoints_count_team_2", reg1),
         (try_end),
         # Vincenzo end
         
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           
           #(assign,":not_selecting_flag",1),
           #(try_begin),
           #  (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
           #  (store_sub,":time_dif",":current_time",":player_join_time"),
           #  (le,":time_dif",10), # first 10 seconds give a new player chance to select a flag.
           #  (player_is_busy_with_menus, ":player_no"),
           #  (assign,":not_selecting_flag",0),
           #(try_end),
           
           #(eq,":not_selecting_flag",1), # always spawn since he might have the flag presentation open..
           (neg|player_is_busy_with_menus, ":player_no"), #had enough of this retarded thing constantly spawning me as the wrong troop because I don't have time to change.

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           # Vincenzo begin
           (assign, ":has_flags", 0),
           (try_begin),
             (eq, ":player_team", 0),
             (assign, ":player_team_entrypoints", ":entrypoints_team_1"),
             (assign, ":player_team_entrypoints_count", ":entrypoints_count_team_1"),
             (assign, ":start_point", 1),
             (try_begin),
               (gt, ":flags_team_1", 1),
               (assign, ":has_flags", 1),
             (try_end),
           (else_try),
             (assign, ":player_team_entrypoints", ":entrypoints_team_2"),
             (assign, ":player_team_entrypoints_count", ":entrypoints_count_team_2"),
             (assign, ":start_point", 101),
             (try_begin),
               (gt, ":flags_team_2", 11),
               (assign, ":has_flags", 1),
             (try_end),
           (try_end),
           
           (eq, ":has_flags", 1), # More then 0 flags are owned, if not stop trying to spawn this agent.
           # Vincenzo end
           
           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
             # Vincenzo begin
               # (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               # (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
             # Vincenzo end
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
         
          
           # Vincenzo begin
           #(assign,":should_spawn",1),
           (try_begin),
             (gt,":player_team_entrypoints_count",0), # More then 0 entry points are found.
             
             (try_begin),
               #(troop_get_slot,":value","trp_conquest_spawn_dummy",":player_no"),
               (player_get_slot,":flag_id",":player_no",slot_player_selected_flag),
               (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_id"),
               (troop_get_slot, ":current_owner", "trp_multiplayer_data", ":cur_flag_slot"),
               (store_add,":player_team_plus_1",":player_team",1),
               
               # (assign,reg4,":value"),
               # (assign,reg3,":player_team_plus_1"),
               # (assign,reg2,":current_owner"),
               # (str_store_string,s4,"@Selected Flag Owner: {reg2} Player Team plus 1: {reg3} Flag value: {reg4}"),
               # (call_script, "script_multiplayer_broadcast_message"),
               
               (eq,":player_team_plus_1",":current_owner"), # we have a flaggy for us selected =)
               
               (store_mul,":current_flag_slot",":flag_id",50),  # each 50 slots containt entry points for a flag.
               (troop_get_slot, ":entry_point_count", "trp_entrypoints_per_flag_dummy", ":current_flag_slot"),
               (val_add,":current_flag_slot",1),
               (val_add,":entry_point_count",":current_flag_slot"),
               #(val_add,":entry_point_count",1),
               
               (store_random_in_range, ":spawn_entry_no", ":current_flag_slot", ":entry_point_count"),
               (troop_get_slot, ":entry_point", "trp_entrypoints_per_flag_dummy", ":spawn_entry_no"),
               
                # (assign,reg1,":flag_id"),
                # (assign,reg2,":entry_point_count"),
                # (assign,reg3,":spawn_entry_no"),
                # (assign,reg4,":current_flag_slot"),
                # (assign,reg5,":entry_point"),
                # (str_store_string,s4,"@flag_id:{reg1}  current_flag_slot+1:{reg4}  entry_point_count:{reg2}  spawn_entry_no:{reg3} thats entry_point:{reg5}"),
                # (call_script, "script_multiplayer_broadcast_message"),
             (else_try),
               (store_random_in_range, ":spawn_entry_no", ":start_point", ":player_team_entrypoints"),
               (troop_get_slot, ":entry_point", "trp_entrypoints_dummy", ":spawn_entry_no"),
             (try_end),
             
             (assign, reg0, ":entry_point"), # assign that bitch =)
           (else_try), 
              
              #  (str_store_player_username, s9, ":player_no"),
              # (assign, reg9, ":spawn_near_flag"),
              # (str_store_string, s4, "@WARNING! NO ENTRY POINT FOUND FOR PLAYER: {s9}"),
              # (call_script, "script_multiplayer_broadcast_message"), # Broadcast message
             (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
             (try_begin),
               (ge, ":has_item", 0),
               (assign, ":is_horseman", 1),
             (else_try),
               (assign, ":is_horseman", 0),
             (try_end),
             # No entry points found, cryface bad shitty sucky map, just run the native spawn code I guess :(
             (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (try_end),
           # Vincenzo end
           
           #(eq,":should_spawn",1),
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         
         # Vincenzo begin
         (store_mission_timer_a, "$g_hq_last_spawn_wave"),
         # Vincenzo end
         ]),

      (1.07, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), #new died (< g_multiplayer_respawn_period) so will be counted too
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

 
      # Beaver added end mission code
      (1, 0, 5, [ (this_or_next|eq,"$g_conquest_map_end_confirm",0),
                  (eq,"$g_conquest_map_end_confirm",2),
                ],
       [
         (store_mission_timer_a,":timer"),
         (gt,":timer",10),
         (try_begin),
           (eq,"$g_conquest_map_end_confirm",0),
           (team_get_score,":team_1_score", 0),
           (team_get_score,":team_2_score", 1),
           (this_or_next|le, ":team_1_score", 0),
           (le, ":team_2_score", 0),
           (try_begin),
             (neg|multiplayer_is_dedicated_server),
             (start_presentation,"prsnt_message_conquest_round_ended"),
           (try_end),
           (assign,"$g_conquest_map_end_confirm",2),
         (else_try),
           (eq,"$g_conquest_map_end_confirm",2),
           (assign,"$g_conquest_map_end_confirm",1),
         (try_end),
       ]),        
         
      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

      # Vincenzo change seconds
      (30, 0, 0, [(multiplayer_is_server),],
       [
         #auto team balance control in every 30 seconds (hq)
         (call_script, "script_check_team_balance"),
       ]),

      multiplayer_server_check_end_map,
        
      (0, 0, 0, [(neg|multiplayer_is_dedicated_server),(key_clicked,key_m)],
       [
         (try_begin),
           (neg|is_presentation_active,"prsnt_conquest_flag_select"),
           (start_presentation,"prsnt_conquest_flag_select"),
         (try_end),
         ]),
         
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),

    (
    "multiplayer_cf",mtf_battle_mode,-1, #capture_the_flag mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      
      (64,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (65,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls, multiplayer_server_generate_build_points,
      multiplayer_server_bonuses, multiplayer_server_auto_ff,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (try_begin),
           (multiplayer_is_server),
           (store_current_scene, ":cur_scene"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_plain_medium"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_plain_large"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_steppe_medium"),
           (eq, ":cur_scene", "scn_random_multi_steppe_large"),
           (entry_point_get_position, pos3, 0),
           (entry_point_set_position, 64, pos3),
           (entry_point_get_position, pos1, 32),
           (entry_point_set_position, 65, pos1),
         (try_end),
         
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_match_start_time", 0),
         (try_end),

         (assign, "$flag_1_at_ground_timer", 0),
         (assign, "$flag_2_at_ground_timer", 0),
         
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/4
       
         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),

           (entry_point_get_position, pos3, multi_base_point_team_1),
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),
         
           (entry_point_get_position, pos3, multi_base_point_team_2),
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),         

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         #when an agent dies which carrying a flag, assign flag position to current position with
         #ground level z and do not change it again according to dead agent's any coordinate/rotation.
         (try_begin),                                 
           (multiplayer_is_server),
           
           (agent_is_human, ":dead_agent_no"),
           
           (agent_get_attached_scene_prop, ":attached_scene_prop", ":dead_agent_no"),
           (ge, ":attached_scene_prop", 0), #moved from above after auto-set position

           
           (call_script, "script_set_attached_scene_prop", ":dead_agent_no", -1,0,0,0),
           (agent_set_horse_speed_factor, ":dead_agent_no", 100),

           
           (prop_instance_get_position, pos3, ":attached_scene_prop"), #moved from above to here after auto-set position
           (position_set_z_to_ground_level, pos3), #moved from above to here after auto-set position
           (prop_instance_set_position, ":attached_scene_prop", pos3), #moved from above to here after auto-set position

           (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
           (try_begin),
             (eq, ":dead_agent_team", 0),
             (assign, ":dead_agent_rival_team", 1),
           (else_try),
             (assign, ":dead_agent_rival_team", 0),
           (try_end),
           (team_set_slot, ":dead_agent_rival_team", slot_team_flag_situation, 2), #2-flag at ground
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_set_team_flag_situation", ":dead_agent_rival_team", 2),
           #for only server itself-----------------------------------------------------------------------------------------------         
           (try_for_players, ":player_no", 1),
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":dead_agent_rival_team", 2), #flag at ground
           (try_end),    
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),], #returning flag if it is not touched by anyone in 60 seconds
       [
         (try_for_range, ":team_no", 0, 2),           
           (try_begin),
             (team_slot_eq, ":team_no", slot_team_flag_situation, 2),

             (assign, ":flag_team_no", -1),
         
             (try_begin),
               (eq, ":team_no", 0),
               (val_add, "$flag_1_at_ground_timer", 1),
               (ge, "$flag_1_at_ground_timer", multi_max_seconds_flag_can_stay_in_ground),
               (assign, ":flag_team_no", 0),
             (else_try),
               (val_add, "$flag_2_at_ground_timer", 1),
               (ge, "$flag_2_at_ground_timer", multi_max_seconds_flag_can_stay_in_ground), 
               (assign, ":flag_team_no", 1),
             (try_end),

             (try_begin),
               (ge, ":flag_team_no", 0),

               (try_begin),
                 (eq, ":flag_team_no", 0),
                 (assign, "$flag_1_at_ground_timer", 0),
               (else_try),
                 (eq, ":flag_team_no", 1),
                 (assign, "$flag_2_at_ground_timer", 0),
               (try_end),
         
               #cur agent returned his own flag to its default position!
               (team_set_slot, ":flag_team_no", slot_team_flag_situation, 0), #0-flag at base

               #return team flag to its starting position.
               #for only server itself-----------------------------------------------------------------------------------------------
               (call_script, "script_set_team_flag_situation", ":flag_team_no", 0),
               #for only server itself-----------------------------------------------------------------------------------------------         
               (try_for_players, ":player_no", 1),
                 (player_is_active, ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":flag_team_no", 0),
               (try_end),

               (scene_prop_get_instance, ":flag_red_id", "$team_1_flag_scene_prop", 0),
               (scene_prop_get_instance, ":flag_blue_id", "$team_2_flag_scene_prop", 0),

               (assign, ":team_1_flag_id", ":flag_red_id"),
               (assign, ":team_1_base_entry_id", multi_base_point_team_1),

               (assign, ":team_2_flag_id", ":flag_blue_id"),
               (assign, ":team_2_base_entry_id", multi_base_point_team_2),

               #return team flag to its starting position.
               (try_begin),
                 (eq, ":flag_team_no", 0),
                 (entry_point_get_position, pos5, ":team_1_base_entry_id"), #moved from above to here after auto-set position
                 (prop_instance_set_position, ":team_1_flag_id", pos5), #moved from above to here after auto-set position
               (else_try),
                 (entry_point_get_position, pos5, ":team_2_base_entry_id"), #moved from above to here after auto-set position
                 (prop_instance_set_position, ":team_2_flag_id", pos5), #moved from above to here after auto-set position
               (try_end),

               #(team_get_faction, ":team_faction", ":flag_team_no"),
               #(str_store_faction_name, s1, ":team_faction"),
               #(tutorial_message_set_position, 500, 500),
               #(tutorial_message_set_size, 30, 30),
               #(tutorial_message_set_center_justify, 1),
               #(tutorial_message, "str_s1_returned_flag", 0xFFFFFFFF, 5),

               (store_mul, ":minus_flag_team_no", ":flag_team_no", -1),
               (val_sub, ":minus_flag_team_no", 1),

               #for only server itself
               (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_returned_home, ":minus_flag_team_no"), 
 
               #no need to send also server here
               (try_for_players, ":player_no", 1),
                 (player_is_active, ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_returned_home, ":minus_flag_team_no"),
               (try_end),
             (try_end),
           (else_try),
             (try_begin),
               (eq, ":team_no", 0),
               (assign, "$flag_1_at_ground_timer", 0),
             (else_try),
               (assign, "$flag_2_at_ground_timer", 0),         
             (try_end),
           (try_end),
         (try_end),           
         ]),
         
      (1, 0, 0, [(multiplayer_is_server),],
       [
         # Vincenzo begin
         
         # Store team 1 spawns
         (entry_point_get_position, pos62, multi_base_point_team_1), # pos62 is search pos.
         (assign, ":entrypoints_team_1", 1),
         (call_script, "script_multiplayer_server_hq_get_entrypoints_for_flag",-1,":entrypoints_team_1"),
         (assign, ":entrypoints_team_1", reg0),
         (assign, ":entrypoints_count_team_1", reg1),
         
         # Store team 2 spawns
         (entry_point_get_position, pos62, multi_base_point_team_2), # pos62 is search pos.
         (assign, ":entrypoints_team_2", 101),
         (call_script, "script_multiplayer_server_hq_get_entrypoints_for_flag",-1,":entrypoints_team_2"),
         (assign, ":entrypoints_team_2", reg0),
         (assign, ":entrypoints_count_team_2", reg1),
         # Vincenzo end
         
         
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),
           
           # Vincenzo begin
           (try_begin),
             (eq, ":player_team", 0),
             (assign, ":player_team_entrypoints", ":entrypoints_team_1"),
             (assign, ":player_team_entrypoints_count", ":entrypoints_count_team_1"),
             (assign, ":start_point", 1),
           (else_try),
             (assign, ":player_team_entrypoints", ":entrypoints_team_2"),
             (assign, ":player_team_entrypoints_count", ":entrypoints_count_team_2"),
             (assign, ":start_point", 101),
           (try_end),
           # Vincenzo end
           
           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           
           # Vincenzo begin
           (try_begin),
             (gt,":player_team_entrypoints_count",0),
             
             (store_random_in_range, ":spawn_entry_no", ":start_point", ":player_team_entrypoints"),
             (troop_get_slot, ":entry_point", "trp_entrypoints_dummy", ":spawn_entry_no"),
             
             (assign, reg0, ":entry_point"), # assign that bitch =)
           (else_try),
             # No entry points found, cryface bad shitty sucky map, just run the native spawn code I guess :(
             (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
             (try_begin),
               (ge, ":has_item", 0),
               (assign, ":is_horseman", 1),
             (else_try),
               (assign, ":is_horseman", 0),
             (try_end),
             
             (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (try_end),
           # Vincenzo end
           
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1.07, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), #new died (< g_multiplayer_respawn_period) so will be counted too
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,
      
      # Vincenzo change seconds
      (1, 0, 0, [(multiplayer_is_server)], #control any agent captured flag or made score.
       [
         (scene_prop_get_instance, ":flag_red_id", "$team_1_flag_scene_prop", 0),
         (prop_instance_get_position, pos1, ":flag_red_id"), #hold position of flag of team 1 (red flag) at pos1

         (scene_prop_get_instance, ":flag_blue_id", "$team_2_flag_scene_prop", 0),
         (prop_instance_get_position, pos2, ":flag_blue_id"), #hold position of flag of team 2 (blue flag) at pos2                          

         (try_for_agents, ":cur_agent"),
           (agent_is_human, ":cur_agent"), #horses cannot take flag
           (agent_is_alive, ":cur_agent"),
           (neg|agent_is_non_player, ":cur_agent"), #for now bots cannot take flag or return flags to home.
           (agent_get_horse, ":cur_agent_horse", ":cur_agent"),
           (eq, ":cur_agent_horse", -1), #horseman cannot take flag
           (agent_get_attached_scene_prop, ":attached_scene_prop", ":cur_agent"),
         
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_agent_team", 0),
             (assign, ":cur_agent_rival_team", 1),
           (else_try),
             (assign, ":cur_agent_rival_team", 0),
           (try_end),

           (try_begin),
             (eq, ":cur_agent_team", 0), 
             (assign, ":our_flag_id", ":flag_red_id"),
             (assign, ":our_base_entry_id", multi_base_point_team_1),
           (else_try), 
             (assign, ":our_flag_id", ":flag_blue_id"),
             (assign, ":our_base_entry_id", multi_base_point_team_2),
           (try_end),

           (agent_get_position, pos3, ":cur_agent"),
           (prop_instance_get_position, pos4, ":our_flag_id"),
           (get_distance_between_positions, ":dist", pos3, pos4),
           (team_get_slot, ":cur_agent_flag_situation", ":cur_agent_team", slot_team_flag_situation),
         
           (try_begin), #control if agent can return his own flag to default position
             (eq, ":cur_agent_flag_situation", 2), #if our flag is at ground
             (lt, ":dist", 100), #if this agent is near to his team's own flag

             #cur agent returned his own flag to its default position!
             (team_set_slot, ":cur_agent_team", slot_team_flag_situation, 0), #0-flag at base

             #return team flag to its starting position.
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_team", 0),
             #for only server itself----------------------------------------------------------------------------------------------- 
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_team", 0),
             (try_end),

             #return team flag to its starting position.
             (entry_point_get_position, pos5, ":our_base_entry_id"), #moved from above to here after auto-set position
             (prop_instance_set_position, ":our_flag_id", pos5), #moved from above to here after auto-set position

             (try_begin), #give 1 score points to player which returns his/her flag to team base
               (multiplayer_is_server),
               (neg|agent_is_non_player, ":cur_agent"),
               (agent_get_player_id, ":cur_agent_player_id", ":cur_agent"),
               (player_get_score, ":cur_agent_player_score", ":cur_agent_player_id"),
               (val_add, ":cur_agent_player_score", multi_capture_the_flag_score_flag_returning),
               (player_set_score, ":cur_agent_player_id", ":cur_agent_player_score"),
             (try_end),

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_returned_flag", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_returned_home, ":cur_agent"), 

             #no need to send also server here
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_returned_home, ":cur_agent"),
             (try_end),         
           (try_end),
                   
           (try_begin), #control if agent carries flag and made score
             (neq, ":attached_scene_prop", -1), #if not agent is carrying anything
             
             (try_begin),
               (eq, ":cur_agent_team", 0), 
               (assign, ":rival_flag_id", ":flag_blue_id"),
               (assign, ":rival_base_entry_id", multi_base_point_team_2),
             (else_try), 
               (assign, ":rival_flag_id", ":flag_red_id"),
               (assign, ":rival_base_entry_id", multi_base_point_team_1),
             (try_end),
             
             (eq, ":attached_scene_prop", ":rival_flag_id"), #if agent is carrying rival flag
             (eq, ":cur_agent_flag_situation", 0), #if our flag is at home position         
             (lt, ":dist", 100), #if this agent (carrying rival flag) is near to his team's own

             #cur_agent's team is scored!#
             (team_get_score, ":cur_agent_team_score", ":cur_agent_team"), #this agent's team scored
             (val_add, ":cur_agent_team_score", 1),
             (team_set_score, ":cur_agent_team", ":cur_agent_team_score"),

             #(team_set_score, ":cur_agent_team", ":cur_agent_team_score"),

             (try_begin), #give 5 score points to player which connects two flag and make score to his/her team
               (multiplayer_is_server),
               (neg|agent_is_non_player, ":cur_agent"),
               (agent_get_player_id, ":cur_agent_player_id", ":cur_agent"),
               (player_get_score, ":cur_agent_player_score", ":cur_agent_player_id"),
               (val_add, ":cur_agent_player_score", "$g_multiplayer_point_gained_from_capturing_flag"),
               (player_set_score, ":cur_agent_player_id", ":cur_agent_player_score"),
             (try_end),
         
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_team_set_score", ":cur_agent_team", ":cur_agent_team_score"),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_begin),
               (eq,":cur_agent_team",0),
               (assign, ":team_1_score", ":cur_agent_team_score"),
               (team_get_score, ":team_2_score", 1),
             (else_try),
               (assign, ":team_2_score", ":cur_agent_team_score"),
               (team_get_score, ":team_1_score", 0),
             (try_end),
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, ":team_1_score", ":team_2_score"),
             (try_end),

             (agent_set_attached_scene_prop, ":cur_agent", -1),             
             (team_set_slot, ":cur_agent_rival_team", slot_team_flag_situation, 0), #0-flag at base

             
             (call_script, "script_set_attached_scene_prop", ":cur_agent", -1,0,0,0),
             (agent_set_horse_speed_factor, ":cur_agent", 100),

             
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_rival_team", 0),
             #for only server itself-----------------------------------------------------------------------------------------------         
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_rival_team", 0),
             (try_end),

             #return rival flag to its starting position
             (entry_point_get_position, pos5, ":rival_base_entry_id"), #moved from above to here after auto-set position
             (prop_instance_set_position, ":rival_flag_id", pos5), #moved from above to here after auto-set position

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(player_get_agent_id, ":my_player_agent", ":my_player_no"),
             #(try_begin),
             #  (ge, ":my_player_agent", 0),
             #  (agent_get_team, ":my_player_team", ":my_player_agent"),
             #  (try_begin),
             #    (eq, ":my_player_team", ":cur_agent_team"),
             #    (assign, ":text_font_color", 0xFF33DDFF),
             #  (else_try),
             #    (assign, ":text_font_color", 0xFFFF0000),
             #  (try_end),
             #(else_try),
             #  (assign, ":text_font_color", 0xFFFFFFFF),
             #(try_end),    
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_captured_flag", ":text_font_color", 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_capture_the_flag_score, ":cur_agent"), 
             
             #no need to send to also server here
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_capture_the_flag_score, ":cur_agent"),
             (try_end),
           (try_end),
         
           (eq, ":attached_scene_prop", -1), #agents carrying other scene prop cannot take flag.
           (agent_get_position, pos3, ":cur_agent"),
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_agent_team", 0), #if this agent is from team 1, look its distance to blue flag.
             (get_distance_between_positions, ":dist", pos2, pos3),
             (assign, ":rival_flag_id", ":flag_blue_id"),
           (else_try), #if this agent is from team 2, look its distance to red flag.
             (get_distance_between_positions, ":dist", pos1, pos3),
             (assign, ":rival_flag_id", ":flag_red_id"),
           (try_end),

           (try_begin),  #control if agent stole enemy flag
             (le, ":dist", 100),
             (neg|team_slot_eq, ":cur_agent_rival_team", slot_team_flag_situation, 1), #if flag is not already stolen.
             
             (agent_set_attached_scene_prop, ":cur_agent", ":rival_flag_id"),
             (agent_set_attached_scene_prop_x, ":cur_agent", 20),
             (agent_set_attached_scene_prop_z, ":cur_agent", 50),

             (try_begin),
               (eq, ":cur_agent_team", 0),
               (assign, "$flag_1_at_ground_timer", 0),
             (else_try),
               (eq, ":cur_agent_team", 1),
               (assign, "$flag_2_at_ground_timer", 0),
             (try_end),

             #cur_agent stole rival team's flag!
             (team_set_slot, ":cur_agent_rival_team", slot_team_flag_situation, 1), #1-stolen flag
                      

             (call_script, "script_set_attached_scene_prop", ":cur_agent", ":rival_flag_id",17,-11,14),                            
             (agent_set_horse_speed_factor, ":cur_agent", 60),                                                                     

         
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_rival_team", 1),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_rival_team", 1),
             (try_end),

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_taken_flag", 0xFFFFFFFF, 5), 

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_capture_the_flag_stole, ":cur_agent"), 

             #no need to send also server here
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_capture_the_flag_stole, ":cur_agent"),
             (try_end),         
           (try_end),
         (try_end),         
         ]),
      
      # Vincenzo change seconds
      (30, 0, 0, [(multiplayer_is_server),],
       [
         #auto team balance control in every 10 seconds (cf)
         (call_script, "script_check_team_balance"),
         ]),

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),

    (
    "multiplayer_sg",mtf_battle_mode,-1, #siege
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls, multiplayer_server_generate_build_points,
      multiplayer_server_bonuses, multiplayer_server_auto_ff,
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),

         (try_begin),
           (multiplayer_is_server),
           (this_or_next|player_is_active, ":player_no"),
           (eq, ":player_no", 0),
           (store_mission_timer_a, ":round_time"),
           (val_sub, ":round_time", "$g_round_start_time"),
           
           (set_fixed_point_multiplier,1),
           # example roundtime 15 mins, 900 seconds.
           (try_begin),
             (store_mul,":time_check_value","$g_multiplayer_round_max_seconds",10), # 10% = 90 = 1.5 mins
             (val_div,":time_check_value",100),
             (lt, ":round_time", ":time_check_value"),
             (assign, ":number_of_respawns_spent", 0),
           (else_try),
             (store_mul,":time_check_value","$g_multiplayer_round_max_seconds",20), # 20% = 180 = 3 mins, loose first life.
             (val_div,":time_check_value",100),
             (lt, ":round_time", ":time_check_value"),
             (assign, ":number_of_respawns_spent", 1),
           (else_try),
             (store_mul,":time_check_value","$g_multiplayer_round_max_seconds",50), # 50% = 450 = 7.5 mins, loose two lives.
             (val_div,":time_check_value",100),
             (lt, ":round_time", ":time_check_value"),
             (assign, ":number_of_respawns_spent", 2),
           (else_try),
             (store_mul,":time_check_value","$g_multiplayer_round_max_seconds",80), # 80% = 720 = 12 mins, loose three lives.
             (val_div,":time_check_value",100),
             (lt, ":round_time", ":time_check_value"),
             (assign, ":number_of_respawns_spent", 3),
           (else_try),
             (assign, ":number_of_respawns_spent", "$g_multiplayer_number_of_respawn_count"),
           (try_end),
           (set_fixed_point_multiplier,100),

           (player_set_slot, ":player_no", slot_player_spawn_count, ":number_of_respawns_spent"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_spent, ":number_of_respawns_spent"),
         (try_end),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_siege),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (try_begin),
           (multiplayer_is_server),
           (try_for_range, ":cur_flag_slot", multi_data_flag_pull_code_begin, multi_data_flag_pull_code_end),
             (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
           (try_end),
         (try_end),
         (assign, "$g_my_spawn_count", 0),
      
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (assign, "$g_flag_is_not_ready", 0),

         #(call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/5
         
         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_number_of_flags", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           #place base flags
           (entry_point_get_position, pos1, multi_siege_flag_point),
           (set_spawn_position, pos1),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),         
           (position_move_z, pos1, multi_headquarters_pole_height),         
           (set_spawn_position, pos1),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 1),
         (try_end),
         (val_add, "$g_number_of_flags", 1),
         
         (try_for_players, ":player_no", "$g_ignore_server"),
           (store_mission_timer_a, ":player_last_team_select_time"),         
           (player_set_slot, ":player_no", slot_player_last_team_select_time, ":player_last_team_select_time"),
         (try_end),

         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),

         # (try_begin), # so it starts counting after the first guy spawned.
           # (le, "$g_round_start_time", 0),
           
           # (store_mission_timer_a, ":cur_mission_time"),
           # (le,":cur_mission_time",60),
           
           # (assign,"$g_round_start_time",":cur_mission_time"),
         # (try_end),
         
         (try_begin), # For players not for dedicated shitheads
           (neg|multiplayer_is_dedicated_server),
           (try_begin),
             (multiplayer_get_my_player, ":my_player_no"),
             (ge, ":my_player_no", 0),
             (player_get_agent_id, ":my_agent_id", ":my_player_no"),
             (eq, ":my_agent_id", ":agent_no"),

             (try_begin),#if my initial team still not initialized, find and assign its value.
               (ge, ":my_agent_id", 0),
               (lt, "$my_team_at_start_of_round", 0),
               
               (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
             (try_end),

             (val_add, "$g_my_spawn_count", 1),
             (try_begin),
               (ge, "$g_my_spawn_count", "$g_multiplayer_number_of_respawn_count"),
               (gt, "$g_multiplayer_number_of_respawn_count", 0),
               (player_get_team_no, ":my_player_team_no", ":my_player_no"),
               (eq, ":my_player_team_no", 0),
               (assign, "$g_my_spawn_count", 999),
             (try_end),
           (try_end),
           
           (try_begin),
             (neg|multiplayer_is_server), # Client side only moves.
             (try_begin),
               (eq, "$g_round_ended", 1),
               (assign, "$g_round_ended", 0),
               (assign, "$g_my_spawn_count", 0),

               #initialize scene object slots at start of new round at clients.
               (call_script, "script_initialize_all_scene_prop_slots"),

               #these lines are done in only clients at start of each new round.
               (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
               (call_script, "script_initialize_objects_clients"),
               #end of lines
             (try_end),  
           (try_end),         
         (try_end),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (agent_is_active,":my_agent_id"),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin),
           (multiplayer_is_server),
           (neg|agent_is_non_player, ":dead_agent_no"),
           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (player_set_slot, ":dead_agent_player_id", slot_player_spawned_this_round, 0),
         (try_end),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),
         
         
      #Vincenzo change seconds
      (1.06, 0, 0, [ (multiplayer_is_server),
                  (eq, "$g_round_ended", 0),
                ], 
                    #if this trigger takes lots of time in the future and make server machine runs siege mod
                    #very slow with lots of players make period of this trigger 1 seconds, but best is 0. Currently
                    #we are testing this mod with few players and no speed problem occured.
      [
        #main trigger which controls which agent is moving/near which flag.
        (set_fixed_point_multiplier,100),
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.
          
          (assign, ":number_of_agents_around_flag_team_1", 0),
          (assign, ":number_of_agents_around_flag_team_2", 0),
          # (try_for_players, ":player_no", "$g_ignore_server"),
            # (player_is_active, ":player_no"),
            # (player_get_agent_id, ":cur_agent", ":player_no"),
          (try_for_agents,":cur_agent",pos3,601), # 6 meters search range
            (agent_is_active,":cur_agent"),
            (agent_is_human,":cur_agent"),
            (agent_is_alive, ":cur_agent"),
            (agent_get_team, ":cur_agent_team", ":cur_agent"),
            (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
            (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),
            (get_sq_distance_between_position_heights, ":squared_height_dist", pos3, pos1),
            (val_add, ":squared_dist", ":squared_height_dist"),
            (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
            (try_begin),
              (eq, ":cur_agent_team", 0),
              (val_add, ":number_of_agents_around_flag_team_1", 1),
            (else_try),
              (eq, ":cur_agent_team", 1),
              (val_add, ":number_of_agents_around_flag_team_2", 1),
            (try_end),
          (try_end),

          (try_begin),
            (this_or_next|neq, ":old_team_1_agent_count", ":number_of_agents_around_flag_team_1"),
            (neq, ":old_team_2_agent_count", ":number_of_agents_around_flag_team_2"),

            (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
            (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
            (store_div, ":cur_flag_puller_team_last", ":cur_flag_pull_code", 100),

            (try_begin),        
              (eq, ":old_team_2_agent_count", 0),
              (gt, ":number_of_agents_around_flag_team_2", 0),
              (eq, ":number_of_agents_around_flag_team_1", 0),
              (assign, ":puller_team", 2),

              (store_mul, ":puller_team_multiplied_by_100", ":puller_team", 100),
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":puller_team_multiplied_by_100"),

              (this_or_next|neq, ":cur_flag_puller_team_last", ":puller_team"),
              (ge, ":cur_flag_pull_message_seconds_past", 25),

              (store_mul, ":flag_code", ":puller_team", 100),
              (val_add, ":flag_code", ":flag_no"),
            (try_end),

            (try_begin),
              (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
              (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),        
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (eq, "$g_round_ended", 0), #if round still continues and any team did not sucseed yet
          (eq, "$g_flag_is_not_ready", 0), #if round still continues and any team did not sucseed yet
        
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),
        
          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.            

          (try_begin),
            (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),

            #flag_id holds shown flag after this point
            (prop_instance_get_position, pos1, ":flag_id"), #pos1 holds gray/red/blue (current shown) flag position.
            (try_begin),
              (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),        
              (lt, ":squared_dist", multi_headquarters_distance_sq_to_change_flag), #if distance is less than 2 meters
              
              (eq, ":old_team_1_agent_count", 0),
              
              (prop_instance_is_animating, ":is_animating", ":flag_id"),
              (eq, ":is_animating", 1),

              #end of round, attackers win
              (assign, "$g_winner_team", 1),
              (prop_instance_stop_animating, ":flag_id"),        
        
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_draw_this_round", "$g_winner_team"),
              (server_add_message_to_log,"str_round_changed"), #patch1115  siege fix 4/1
              #for only server itself-----------------------------------------------------------------------------------------------
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
              (try_end),

              (assign, "$g_flag_is_not_ready", 1),
            (try_end),        
          (try_end),
        (try_end),
        ]),

      (0, 0, 0, [(neg|multiplayer_is_dedicated_server),], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),

      # Vincenzo begin copied this for server with less checks.
      (1.03, 0, 0, [(multiplayer_is_dedicated_server)], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),
      # Vincenzo end
      # Vincenzo change seconds
      (1.07, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),
                 (eq, "$g_flag_is_not_ready", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds")],
       [
         (assign, ":flag_no", 0),
         (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
         (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
         (store_mod, ":team_2_agent_count_around_flag", ":current_owner_code", 100),

         (try_begin),
           (eq, ":team_2_agent_count_around_flag", 0),
         
           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),
           (assign, "$g_flag_is_not_ready", 1),
        
           (assign, "$g_winner_team", 0),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           (server_add_message_to_log,"str_round_changed"), #patch1115 siege fix 4/2
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_players, ":player_no", 1),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),
         (try_end),
         ]),          

      (1, 0, 0, [(multiplayer_is_server),],
      [
        #trigger for calculating seconds past after that flag's pull message has shown          
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
          (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
          (try_begin),
            (ge, ":cur_flag_pull_code", 100),
            (lt, ":cur_flag_pull_message_seconds_past", 25),
            (val_add, ":cur_flag_pull_code", 1),
            (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":cur_flag_pull_code"),
          (try_end),
        (try_end),        
      ]),                      

      (1.02, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         # Vincenzo begin
         # teamswap
         (try_begin),
           (eq,"$g_auto_swap",1), # Auto Swap enabled.
           
           (str_clear, s2),
           (str_store_string, s4, "str_swap_all_s2"),
           
           (call_script, "script_multiplayer_broadcast_message"),
           
           (team_get_score, ":team_1_score", 0),
           (team_get_score, ":team_2_score", 1),
           (team_set_score, 0, ":team_2_score"),
           (team_set_score, 1, ":team_1_score"),           
           
           (try_for_players, ":cur_player", "$g_ignore_server"),
             (player_is_active, ":cur_player"),
             
             (call_script, "script_multiplayer_server_swap_player", ":cur_player"),
             
             (neq,":cur_player",0),
             (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_set_team_score, ":team_2_score", ":team_1_score"),
           (try_end),
         (try_end),         
         # Vincenzo end
       
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (try_for_players, ":cur_player", "$g_ignore_server"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),                      
               (try_for_players, ":player_no", "$g_ignore_server"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (call_script,"script_multiplayer_server_send_player_score_kill_death", ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),     
                 (try_end),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),
             
             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here                           
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           (player_set_slot, ":player_no", slot_player_spawned_at_siege_round, 0),
           (store_mission_timer_a, ":player_last_team_select_time"),         
           (player_set_slot, ":player_no", slot_player_last_team_select_time, ":player_last_team_select_time"),
           
           # AoN
           (neq,":player_no",0),
           (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_before_round_end),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1), 
        
         (call_script, "script_multiplayer_mm_reset_stuff_after_round_before_clear"),
        
         #clear scene and end round
         (multiplayer_clear_scene),
         
         #assigning everbody's spawn counts to 0
         (assign, "$g_my_spawn_count", 0),
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawn_count, 0),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_spent, 0),
         (try_end),

         (call_script, "script_initialize_objects"),

         #initialize moveable object positions
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
        

         #initialize flag coordinates (move up the flag at pole)
         (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
           (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
           (prop_instance_get_position, pos1, ":pole_id"),
           (position_move_z, pos1, multi_headquarters_pole_height),
           (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
           (prop_instance_stop_animating, ":flag_id"),
           (prop_instance_set_position, ":flag_id", pos1),
         (try_end),
         
         (assign, "$g_round_ended", 0),
         
         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start time for clients
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999),
         (try_end),            

         (assign, "$g_flag_is_not_ready", 0),
         
         #MM
         (call_script, "script_multiplayer_mm_reset_stuff_after_round"),
       ]),
           
      (1.04, 0, 0, [(multiplayer_is_server),],
       [ 
         (store_mission_timer_a, ":round_time"),
         (val_sub, ":round_time", "$g_round_start_time"),
         
         (assign, ":num_active_players_in_team_0", 0),
         (assign, ":num_active_players_in_team_1", 0),
         (assign, ":num_active_players", 0),
         
         (assign,":num_players",multiplayer_player_loops_end),
         (try_for_range, ":cur_player", "$g_player_loops_begin", ":num_players"),
           (player_is_active, ":cur_player"),

           (player_get_team_no, ":cur_player_team", ":cur_player"),
           (try_begin),
             (eq, ":cur_player_team", 0),
             (val_add, ":num_active_players_in_team_0", 1),
           (else_try),
             (eq, ":cur_player_team", 1),
             (val_add, ":num_active_players_in_team_1", 1),
           (try_end),

           (val_add, ":num_active_players", 1),
           
           (gt,":num_active_players",2),
           (gt,":num_active_players_in_team_0", 0),
           (gt,":num_active_players_in_team_1", 0),
           
           (assign,":num_players",0), # stop looping
         (try_end),
        
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
           
           (neg|player_is_busy_with_menus, ":player_no"),
           
           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),
           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),
           (player_get_agent_id, ":player_agent", ":player_no"), #new added for siege mod
         
           (assign, ":spawn_new", 0), 

           (try_begin),
             (eq, "$g_round_ended", 0),
         
             (try_begin), #addition for siege mod to allow players spawn more than once (begin)
               (lt, ":player_agent", 0), 
              
               (try_begin), #new added begin, to avoid siege-crack (rejoining of defenders when they die)
                 (eq, ":player_team", 0), 
                 
                 (player_get_slot, ":player_last_team_select_time", ":player_no", slot_player_last_team_select_time),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":elapsed_time", ":current_time", ":player_last_team_select_time"),
                 
                 (assign, ":player_team_respawn_period", "$g_multiplayer_respawn_period"), 
                 (val_add, ":player_team_respawn_period", multiplayer_siege_mod_defender_team_extra_respawn_time), #new added for siege mod
                 (lt, ":elapsed_time", ":player_team_respawn_period"),

                 #(store_sub, ":round_time", ":current_time", "$g_round_start_time"),
                 (ge, ":round_time", multiplayer_new_agents_finish_spawning_time),
                 (gt, ":num_active_players", 2),
                 (store_mul, ":multipication_of_num_active_players_in_teams", ":num_active_players_in_team_0", ":num_active_players_in_team_1"),
                 (neq, ":multipication_of_num_active_players_in_teams", 0),

                 (assign, ":spawn_new", 0),
               (else_try), #new added end         
                 (assign, ":spawn_new", 1),
               (try_end),
             (else_try), 
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"), 
               (assign, ":player_team_respawn_period", "$g_multiplayer_respawn_period"), 
               (try_begin), 
                 (eq, ":player_team", 0), 
                 (val_add, ":player_team_respawn_period", multiplayer_siege_mod_defender_team_extra_respawn_time), 
               (try_end), 
               (this_or_next|gt, ":elapsed_time", ":player_team_respawn_period"), 
               (player_slot_eq, ":player_no", slot_player_spawned_at_siege_round, 0), 
               (assign, ":spawn_new", 1),
             (try_end), 
           (try_end), #addition for siege mod to allow players spawn more than once (end)

           (eq, ":spawn_new", 1),

           (player_get_slot, ":spawn_count", ":player_no", slot_player_spawn_count),

           (try_begin),
             (gt, "$g_multiplayer_number_of_respawn_count", 0),
             (try_begin),
               (eq, ":player_team", 0),
               (ge, ":spawn_count", "$g_multiplayer_number_of_respawn_count"),
               (assign, ":spawn_new", 0),
             (else_try),
               (eq, ":player_team", 1),      
               (ge, ":spawn_count", 999),
               (assign, ":spawn_new", 0),
             (try_end),
           (try_end),

           (eq, ":spawn_new", 1),

           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (val_add, ":spawn_count", 1),

           (try_begin),
             (ge, ":spawn_count", "$g_multiplayer_number_of_respawn_count"),
             (gt, "$g_multiplayer_number_of_respawn_count", 0),
             (eq, ":player_team", 0),
             (assign, ":spawn_count", 999),
           (try_end),
           
           (player_set_slot, ":player_no", slot_player_spawn_count, ":spawn_count"),
           

           (try_begin),
             (lt, ":round_time", 30), #at start of round spawn at base entry point (only attackers)
             (eq, ":player_team", 1),
             (assign, ":entry_no", multi_initial_spawn_point_team_2),
           (else_try),
             (eq, ":player_team", 0), #Defenders
             (store_random_in_range, ":entry_no", 0, 32), # Spawn at random defender spawn (0-31)      
           (else_try),
             (eq, ":player_team", 1), #Attackers
             (store_random_in_range, ":entry_no", 32, 64), # Spawn at random attacker spawn (32-63)    
           (try_end),

           (player_spawn_new_agent, ":player_no", ":entry_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
           (player_set_slot, ":player_no", slot_player_spawned_at_siege_round, 1),         
         (try_end),
         ]),

      (1.08, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                  (store_mission_timer_a, ":mission_timer"),
                  (ge, ":mission_timer", 2)                
                ], #do this in every new frame, but not at the same time
       [
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      multiplayer_server_spawn_bots, 
      multiplayer_server_manage_bots, 

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),

    (
    "multiplayer_bt",mtf_battle_mode,-1, #battle mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,
      multiplayer_server_bonuses,
			multiplayer_server_auto_ff,
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_battle),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),

         (try_begin),
           (multiplayer_is_server),
           (assign, "$server_mission_timer_while_player_joined", 0),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/6
		
     
         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),

           (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
           (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
         (try_begin), # so it starts counting after the first guy spawned.
           (le, "$g_round_start_time", 0),
           
           (store_mission_timer_a, ":cur_mission_time"),
           (le,":cur_mission_time",60),
           
           (assign,"$g_round_start_time",":cur_mission_time"),
         (try_end),
         
         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (try_begin),
             (lt, "$my_team_at_start_of_round", 0),
             (multiplayer_get_my_player, ":my_player_no"),
             (ge, ":my_player_no", 0),
             (player_get_agent_id, ":my_agent_id", ":my_player_no"),
             (eq, ":my_agent_id", ":agent_no"),
             (ge, ":my_agent_id", 0),
             (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
           (try_end),
           (try_begin),
             (neg|multiplayer_is_server),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
             (try_begin),
               (eq, "$g_team_balance_next_round", 1),
               (assign, "$g_team_balance_next_round", 0),
             (try_end),
           (try_end),  
         (try_end),         
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin), #count players and if round ended understand this
           (agent_is_active, ":dead_agent_no"),
           (agent_is_human, ":dead_agent_no"),
           
           (assign, ":team1_living_players", 0),
           (assign, ":team2_living_players", 0),
           (assign,":continue_loop",1),
           (try_for_agents, ":cur_agent"),
             (eq,":continue_loop",1),
             (agent_is_active, ":cur_agent"),
             (agent_is_human, ":cur_agent"),         
             (agent_is_alive, ":cur_agent"),  
             (agent_get_team, ":cur_agent_team", ":cur_agent"),
             (try_begin),
               (eq, ":cur_agent_team", 0),
               (val_add, ":team1_living_players", 1),
             (else_try),
               (eq, ":cur_agent_team", 1),
               (val_add, ":team2_living_players", 1),
             (try_end),
             # Break loop.
             (gt, ":team1_living_players", 0),
             (gt, ":team2_living_players", 0),
             (assign,":continue_loop",0),
           (try_end),  
           
           (try_begin),         
             (eq, "$g_round_ended", 0),

             (this_or_next|eq, ":team1_living_players", 0),
             (eq, ":team2_living_players", 0),                
             (assign, reg0, "$g_multiplayer_respawn_period"),
             
             (assign, "$g_winner_team", -1),
             (try_begin),
               (eq, ":team1_living_players", 0),
               (try_begin),
                 (neq, ":team2_living_players", 0),
                 (assign, "$g_winner_team", 1),
               (try_end),
             (else_try),
               (neq, ":team1_living_players", 0),
              
               (assign, "$g_winner_team", 0),
             (try_end),
             
             (try_begin),
               (gt,"$g_winner_team",-1),
               (team_get_score, ":winner_team_score", "$g_winner_team"),
               (val_add, ":winner_team_score", 1),
               (team_set_score, "$g_winner_team", ":winner_team_score"),
             (try_end),
			 
             (server_add_message_to_log,"str_round_changed"), # battle  patch1115 fix 4/6
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, "$g_winner_team"),
             
             (store_mission_timer_a, "$g_round_finish_time"),
             (assign, "$g_round_ended", 1),
           (try_end),
         (try_end),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),
      
      #Beacon last player if less than 3 min round time
      (3.72, 0, 0, [(neg|multiplayer_is_dedicated_server), 
                 (eq, "$g_round_ended", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (val_add, ":seconds_past_in_round", 180), #3 min before round end
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds"),
                 (this_or_next|eq,"$g_beaconed_player_team_1",-1),
                 (eq,"$g_beaconed_player_team_2",-1),
                 ],
       [                         
         (assign,":last_player_alive_team_1",-1),
         (assign,":last_player_alive_team_2",-1),
         (assign,":num_players_team_1",0),
         (assign,":num_players_team_2",0),
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_get_agent_id,":agent_id",":player_no"),
           (agent_is_active,":agent_id"),
           (agent_is_alive,":agent_id"),
           (agent_get_team,":team",":agent_id"),
           (try_begin),
             (eq,":team",0),
             (assign,":last_player_alive_team_1",":player_no"),
             (val_add,":num_players_team_1",1),
           (else_try),
             (eq,":team",1),
             (assign,":last_player_alive_team_2",":player_no"),
             (val_add,":num_players_team_2",1),
           (try_end),
         (try_end),
         (this_or_next|eq,":num_players_team_1",1),
         (eq,":num_players_team_2",1),
         (try_begin),#hotfix
           (eq,":num_players_team_1",1),
           (assign,"$g_beaconed_player_team_1",":last_player_alive_team_1"),
         (try_end),
         (try_begin),
           (eq,":num_players_team_2",1),
           (assign,"$g_beaconed_player_team_2",":last_player_alive_team_2"),
         (try_end),
        ]),   
        
      (1, 0, 0, [(multiplayer_is_server), 
                 (eq, "$g_round_ended", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds"),
                 ],
       [ #round time is up
         (store_mission_timer_a, "$g_round_finish_time"),                          
         (assign, "$g_round_ended", 1),
         (assign, "$g_winner_team", -1),
    
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_draw_this_round", "$g_winner_team"),
         (server_add_message_to_log,"str_round_changed"), # battle  patch1115 fix 4/7
         #for only server itself-----------------------------------------------------------------------------------------------
         (try_for_players, ":player_no", 1),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
		  # (call_script, "script_multiplayer_server_stop_sound_at_end_of_round", ":player_no"),  # didnt work?
         (try_end),
        ]),          

                
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         # Vincenzo begin
         # teamswap
         (try_begin),
           (eq,"$g_auto_swap",1), # Auto Swap enabled.
           (team_get_score, ":team_1_score", 0),
           (team_get_score, ":team_2_score", 1),
           
           (store_add, ":rounds", ":team_1_score", ":team_2_score"),
           (assign, ":max_rounds", "$g_multiplayer_game_max_points"),
           (convert_to_fixed_point, ":max_rounds"),
           (store_div, ":maxrounds_div2", ":max_rounds", 2),
           (convert_from_fixed_point, ":maxrounds_div2"),
           
           (eq, ":rounds", ":maxrounds_div2"),
           
           (str_clear, s2),
           (str_store_string, s4, "str_swap_all_s2"),
           
           (call_script, "script_multiplayer_broadcast_message"),
           
           (team_set_score, 0, ":team_2_score"),
           (team_set_score, 1, ":team_1_score"),
           
           (try_for_players, ":cur_player", "$g_ignore_server"),
             (player_is_active, ":cur_player"),
             
             (call_script, "script_multiplayer_server_swap_player", ":cur_player"),
             
             (neq,":cur_player",0),
             (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_set_team_score, ":team_2_score", ":team_1_score"),
           (try_end),
         (try_end),         
         # Vincenzo end
       
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (try_for_players, ":cur_player", "$g_ignore_server"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             #(eq, "$g_team_balance_next_round", 1), #control if at pre round players are warned about team change.

             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),                         
               (try_for_players, ":player_no", "$g_ignore_server"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (call_script,"script_multiplayer_server_send_player_score_kill_death",":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here                      
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           
           # AoN
           (neq,":player_no",0),
           (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_before_round_end),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_mm_reset_stuff_after_round_before_clear"),
         
         #clear scene and end round
         (multiplayer_clear_scene),

         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         
         #initialize moveable object positions
         (call_script, "script_initialize_objects"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
                  
         (assign, "$g_round_ended", 0), 

         (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
         (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 

         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start times for clients
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
         #MM
         (call_script, "script_multiplayer_mm_reset_stuff_after_round"),
       ]),

      (0, 0, 0, [(neg|multiplayer_is_dedicated_server)], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),
       
      (1.16, 0, 0, [(multiplayer_is_dedicated_server)], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),
           
      (1.02, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),],
       [
         (store_add, ":total_bots", "$g_multiplayer_num_bots_team_1", "$g_multiplayer_num_bots_team_2"),
         (store_mission_timer_a, ":round_time"),
         (val_sub, ":round_time", "$g_round_start_time"),
         
         (assign,":continue",0),
         (try_begin),         
           (lt, ":round_time", multiplayer_new_agents_finish_spawning_time),
           (assign,":continue",1),
         (else_try),
           (gt,":total_bots",0),
           (eq, "$g_multiplayer_player_respawn_as_bot", 1),
           (assign,":continue",1),
         (try_end),
         (eq,":continue",1),
         
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),
           (try_begin),
             (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
             (lt, ":round_time", multiplayer_new_agents_finish_spawning_time),
             
             (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
             (lt, ":player_team", multi_team_spectator),

             (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
             (ge, ":player_troop", 0),

             (try_begin),
               (eq, ":player_team", 0),
               (assign, ":entry_no", multi_initial_spawn_point_team_1),
             (else_try),
               (eq, ":player_team", 1),
               (assign, ":entry_no", multi_initial_spawn_point_team_2),
             (try_end),
             (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
             (player_spawn_new_agent, ":player_no", ":entry_no"),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
           (else_try), #spawning as a bot (if option ($g_multiplayer_player_respawn_as_bot) is 1)
             (eq, "$g_multiplayer_player_respawn_as_bot", 1),
             (gt,":total_bots",0),
             
             (player_get_agent_id, ":player_agent", ":player_no"),
             (ge, ":player_agent", 0),
             (neg|agent_is_alive, ":player_agent"),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
             (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),

             (call_script, "script_find_most_suitable_bot_to_control", ":player_no"),
             (assign,":bot_agent",reg0),
             (gt,":bot_agent",-1),
             
             (player_control_agent, ":player_no", ":bot_agent"),

             (player_get_slot, ":num_spawns", ":player_no", slot_player_spawned_this_round),
             (val_add, ":num_spawns", 1),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, ":num_spawns"),
           (try_end),
         (try_end),
         ]),

      multiplayer_server_spawn_bots, 
      multiplayer_server_manage_bots, 

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),
 
 
  ("multiplayer_cb",mtf_battle_mode,-1, #commander battle mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,
      multiplayer_server_auto_ff,
			
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_commander),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),

         (try_begin),
           (multiplayer_is_server),
           (assign, "$server_mission_timer_while_player_joined", 0),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         
         #Reset squad size at new map start incase it was auto-lowered before and some players have left
         (try_begin),
           (multiplayer_is_server),
           (neq, "$g_prev_squad_size_limit", "$g_squad_size_limit"),
           (assign, "$g_squad_size_limit", "$g_prev_squad_size_limit"),
         (try_end),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/7

         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         
         
         #Auto-lower squad-size if too many players
         (try_begin),
           (multiplayer_is_server),
           (assign,":num_players",0),
           (try_for_players, ":player_no", "$g_ignore_server"),
             (player_is_active,":player_no"),
             (val_add,":num_players",1),
           (try_end),
           (store_mul,":average_num_bots","$g_squad_size_limit",":num_players"),
           (gt,":average_num_bots","$g_max_num_bots"), #Try not to have too many bots
           (store_div,"$g_squad_size_limit","$g_max_num_bots",":num_players"),
           (assign,reg1,"$g_squad_size_limit"),
           (str_store_string, s0, "@SERVER"),
           (str_store_string, s4, "str_admin_set_squad_size_s0_reg1"),
           (assign, ":mod_variable", mod_variable_squad_size),
           (try_for_players, ":cur_player", 1),
             (player_is_active, ":cur_player"),
             (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_mod_variable, ":mod_variable", "$g_squad_size_limit"),
           (try_end),
           (call_script, "script_multiplayer_broadcast_message"),
         (try_end),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         
         (agent_is_active, ":agent_no"),
         
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
        #patch1115 fix 43/7 start 
        (assign, ":remove_weapons", -1),
        (try_begin),
          (agent_is_non_player,":agent_no"),
          (agent_is_human,":agent_no"),
          (agent_get_group, ":agent_group", ":agent_no"),
          (player_is_active, ":agent_group"),
        
          (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
          (troop_get_slot,":agent_class",":agent_troop_id",slot_troop_rank),
          (troop_get_slot,":musician_type",":agent_troop_id",slot_troop_rank_type),
         
          (try_begin), 			
            (gt, ":musician_type", -1),		
          
            (try_begin), #musician / blower
              (eq, ":musician_type", 1),
              (player_slot_eq, ":agent_group", slot_player_musician_spawned, 0),
              (player_set_slot, ":agent_group", slot_player_musician_spawned, ":agent_no"),
              (assign, ":remove_weapons", 1),					
            (else_try), #drummer
              (eq, ":musician_type", 2),
              (player_slot_eq, ":agent_group", slot_player_drummer_spawned, 0),
              (player_set_slot, ":agent_group", slot_player_drummer_spawned, ":agent_no"),
              (assign, ":remove_weapons", 1),					
            (try_end), 				
          (else_try), #sergeant
            (player_slot_eq, ":agent_group", slot_player_flag_spawned, 0),
            (eq, ":agent_class", mm_rank_sergeant),			
            (player_set_slot, ":agent_group", slot_player_flag_spawned, ":agent_no"),
            (assign, ":remove_weapons", 1),		
          (try_end),      
          
          (try_begin),    #we have to assign each thing thing indiv for flags otherwise they may not spawn with it.  
            (eq, ":remove_weapons", 1),
          #(assign, ":special_item", -1),
            (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head), 
              (agent_get_item_slot, ":item_id1", ":agent_no", ":equipment_slot"),
              (gt,":item_id1",-1), # even have an item there?
              (agent_unequip_item,":agent_no",":item_id1", ":equipment_slot"),					
            (try_end), 
          
            (troop_get_inventory_capacity,":inv_cap",":agent_troop_id"),
            (try_for_range,":inv_slot",0,":inv_cap"), 
              (troop_get_inventory_slot,":item_id",":agent_troop_id",":inv_slot"),
              (gt,":item_id",-1),
              
              (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
              (is_between,":item_class",multi_item_class_type_sword,multi_item_class_type_horse), #Some kind of weapon or similar equipment
              
              (agent_equip_item, ":agent_no", ":item_id"),          
              (try_begin),
                (this_or_next|eq,":item_class",multi_item_class_type_flag),
                (eq,":item_class",multi_item_class_type_instrument),
                (agent_set_wielded_item, ":agent_no", ":item_id"),
              (try_end),
            (try_end),
          (try_end),   
            # Not sure why on earth this thing is needed, but why don't we just equip whatever we have in our inventory?
         (try_end), #patch1115 fix 43/7 end 
         
         (try_begin),
           (neg|agent_is_non_player,":agent_no"),
           (agent_get_player_id, ":player_team_no", ":agent_no"),
           (set_show_messages, 0),
           (team_give_order, ":player_team_no", grc_everyone, mordr_follow),
           (team_give_order, ":player_team_no", grc_cavalry, mordr_mount), #Mount cavalry...
           (player_set_slot, ":player_team_no", slot_player_bot_order, 0),
           (set_show_messages, 1),
         (try_end),
         
         (try_begin), # so it starts counting after the first guy spawned.
           (le, "$g_round_start_time", 0),
           
           (store_mission_timer_a, ":cur_mission_time"),
           (le,":cur_mission_time",60),
           
           (assign,"$g_round_start_time",":cur_mission_time"),
         (try_end),
         
         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (try_begin),
             (lt, "$my_team_at_start_of_round", 0),
             (multiplayer_get_my_player, ":my_player_no"),
             (ge, ":my_player_no", 0),
             (player_get_agent_id, ":my_agent_id", ":my_player_no"),
             (eq, ":my_agent_id", ":agent_no"),
             (ge, ":my_agent_id", 0),
             (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
           (try_end),
           (try_begin),
             (neg|multiplayer_is_server),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
             (try_begin),
               (eq, "$g_team_balance_next_round", 1),
               (assign, "$g_team_balance_next_round", 0),
             (try_end),
           (try_end),  
         (try_end),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin), #count players and if round ended understand this.
           (agent_is_active, ":dead_agent_no"),
           (agent_is_human, ":dead_agent_no"),
           
           (assign, ":team1_living_players", 0),
           (assign, ":team2_living_players", 0),
           (assign,":continue_loop",1),
           (try_for_agents, ":cur_agent"),
             (eq,":continue_loop",1),
             (agent_is_active, ":cur_agent"),
             (agent_is_human, ":cur_agent"),         
             (agent_is_alive, ":cur_agent"),  
             (agent_get_team, ":cur_agent_team", ":cur_agent"),
             (try_begin),
               (eq, ":cur_agent_team", 0),
               (val_add, ":team1_living_players", 1),
             (else_try),
               (eq, ":cur_agent_team", 1),
               (val_add, ":team2_living_players", 1),
             (try_end),
             # Break loop.
             (gt, ":team1_living_players", 0),
             (gt, ":team2_living_players", 0),
             (assign,":continue_loop",0),
           (try_end),  
           
           (try_begin),         
             (eq, "$g_round_ended", 0),

             (this_or_next|eq, ":team1_living_players", 0),
             (eq, ":team2_living_players", 0),        
             (assign, reg0, "$g_multiplayer_respawn_period"),
             
             (assign, "$g_winner_team", -1),
             (try_begin),
               (eq, ":team1_living_players", 0),
               (try_begin),
                 (neq, ":team2_living_players", 0),
                 (assign, "$g_winner_team", 1),
               (try_end),
             (else_try),
               (neq, ":team1_living_players", 0),
              
               (assign, "$g_winner_team", 0),
             (try_end),
             
             (try_begin),
               (gt,"$g_winner_team",-1),
               (team_get_score, ":winner_team_score", "$g_winner_team"),
               (val_add, ":winner_team_score", 1),
               (team_set_score, "$g_winner_team", ":winner_team_score"),
             (try_end),
             
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, "$g_winner_team"),
             (server_add_message_to_log,"str_round_changed"),#patch1115 commander fix 4/3
             (store_mission_timer_a, "$g_round_finish_time"),
             (assign, "$g_round_ended", 1),
           (try_end),
         (try_end),        
         ]),
              
              
      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),
      
	  (ti_on_player_exit, 0, 0, [],
		[
		 # remove squad of leaving player
		 (store_trigger_param_1, ":player_no"),
     (player_is_active,":player_no"),
     (player_get_team_no, ":player_team", ":player_no"),
     (call_script,"script_on_commander_leave_or_team_switch",":player_no",":player_team"),
		 ]),
     
      (1, 0, 0, [(multiplayer_is_server), 
                 (eq, "$g_round_ended", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds"),
                 ],
       [ #round time is up
         (store_mission_timer_a, "$g_round_finish_time"),                          
         (assign, "$g_round_ended", 1),
         (assign, "$g_winner_team", -1),
    
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_draw_this_round", "$g_winner_team"),
         (server_add_message_to_log,"str_round_changed"), #patch1115 commander fix 4/4
         #for only server itself-----------------------------------------------------------------------------------------------
         (try_for_players, ":player_no", 1),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
         (try_end),
        ]),          

                
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (try_for_players, ":cur_player", "$g_ignore_server"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             #(eq, "$g_team_balance_next_round", 1), #control if at pre round players are warned about team change.

             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),                            
               (try_for_players, ":player_no", "$g_ignore_server"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (call_script,"script_multiplayer_server_send_player_score_kill_death", ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),    
                 (try_end),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here
             #(multiplayer_get_my_player, ":my_player_no"),                          
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           
           # AoN
           (neq,":player_no",0),
           (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_before_round_end),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_mm_reset_stuff_after_round_before_clear"),
         
         #clear scene and end round
         (multiplayer_clear_scene),

         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         
         #initialize moveable object positions
         (call_script, "script_initialize_objects"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
                  
         (assign, "$g_round_ended", 0), 

         (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
         (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 

         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start times for clients
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
         #MM
         (call_script, "script_multiplayer_mm_reset_stuff_after_round"),
        
        
         #Auto-lower squad-size if too many players
         (try_begin),
           (multiplayer_is_server),
           (assign,":num_players",0),
           (try_for_players, ":player_no", "$g_ignore_server"),
             (player_is_active,":player_no"),
             (val_add,":num_players",1),
           (try_end),
           (store_mul,":average_num_bots","$g_squad_size_limit",":num_players"),
           (gt,":average_num_bots",600), #Try not to have more than 600 bots
           (store_div,"$g_squad_size_limit",600,":num_players"),
           (assign,reg1,"$g_squad_size_limit"),
           (str_store_string, s0, "@SERVER"),
           (str_store_string, s4, "str_admin_set_squad_size_s0_reg1"),
           (assign, ":mod_variable", mod_variable_squad_size),
           (try_for_players, ":cur_player", 1),
             (player_is_active, ":cur_player"),
             (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_mod_variable, ":mod_variable", "$g_squad_size_limit"),
           (try_end),
           (call_script, "script_multiplayer_broadcast_message"),
         (try_end),
       ]),

      (0, 0, 0, [(neg|multiplayer_is_dedicated_server)], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),
       
      (1.03, 0, 0, [(multiplayer_is_dedicated_server)], #if there is nobody in any teams do not reduce round time.
       [
         (call_script,"script_multiplayer_reset_round_time_if_no_agents"),
       ]),
       
      (1.07, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),],
       [
         #(store_add, ":total_bots", "$g_multiplayer_num_bots_team_1", "$g_multiplayer_num_bots_team_2"),
         (store_mission_timer_a, ":round_time"),
         (val_sub, ":round_time", "$g_round_start_time"),
         
         (assign,":continue",0),
         (try_begin),         
           (lt, ":round_time", multiplayer_new_agents_finish_spawning_time),
           (assign,":continue",1),
         (else_try),
           (eq, "$g_multiplayer_player_respawn_as_bot", 1),
           (assign,":continue",1),
         (try_end),
         (eq,":continue",1),
         
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"), 
           (try_begin),
             (neg|player_is_busy_with_menus, ":player_no"),
             (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
             (lt, ":round_time", multiplayer_new_agents_finish_spawning_time), #lt
             
             (lt, ":player_team", multi_team_spectator),  #if player is currently spectator do not spawn his agent

             (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
             (ge, ":player_troop", 0),

             (try_begin),
               (eq, ":player_team", 0),
               (assign, ":entry_no", multi_initial_spawn_point_team_1),
             (else_try),
               (eq, ":player_team", 1),
               (assign, ":entry_no", multi_initial_spawn_point_team_2),
             (try_end),
             (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
             (player_spawn_new_agent, ":player_no", ":entry_no"),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
				
             #Spawn Player Squad
             (player_get_slot,":selected_bot_type",":player_no",slot_player_bot_type_wanted),
             #(call_script,"script_commander_get_squad_size",":player_no"),
             #(assign,":num_bots",reg0),
             (call_script,"script_scale_num_bots_after_troop_type",":selected_bot_type","$g_squad_size_limit"),
             (assign,":num_bots",reg0),
             (store_current_scene, ":cur_scene"),
             (modify_visitors_at_site, ":cur_scene"),
             (add_visitors_to_current_scene, ":entry_no", ":selected_bot_type", ":num_bots", ":player_team", ":player_no"),
             
             #find proper specialist bot types for troop types  #patch1115 43/10 start
             (assign, ":bot_type_musician", -1),
             (assign, ":bot_type_drummer", -1),
             (assign, ":bot_type_flag", -1),


             (try_begin),
               (store_sub, ":try_for_specialist", ":player_troop", 1),
               (try_begin),
                 (troop_slot_eq,":try_for_specialist",slot_troop_rank,mm_rank_sergeant),
                 (assign, ":bot_type_flag", ":try_for_specialist"),
               (try_end),
               (store_add, ":try_for_specialist", ":player_troop", 1),
               (try_begin),
                 (troop_slot_eq,":try_for_specialist",slot_troop_rank,mm_rank_musician),
                 (assign, ":bot_type_musician", ":try_for_specialist"),
                 (store_add, ":try_for_specialist", ":try_for_specialist", 1),
                 (try_begin),
                   (troop_slot_eq,":try_for_specialist",slot_troop_rank,mm_rank_musician),
                   (assign, ":bot_type_drummer", ":try_for_specialist"),
                 (try_end),
               (try_end),
             (try_end),

             #fifer:
             (try_begin),
              (gt, ":bot_type_musician", 0),
              (add_visitors_to_current_scene, ":entry_no", ":bot_type_musician", 1, ":player_team", ":player_no"),
              #(player_set_slot, ":player_no", slot_player_musician_spawned, ":bot_type_musician"),
             (try_end),
             #drummer:
             (try_begin),
              (gt, ":bot_type_drummer", 0),
              (add_visitors_to_current_scene, ":entry_no", ":bot_type_drummer", 1, ":player_team", ":player_no"),
              #(player_set_slot, ":player_no", slot_player_drummer_spawned, ":bot_type_drummer"),
             (try_end),
             #flag:
             (try_begin),
              (gt, ":bot_type_flag", 0),
              (add_visitors_to_current_scene, ":entry_no", ":bot_type_flag", 1, ":player_team", ":player_no"),
              #(player_set_slot, ":player_no", slot_player_flag_spawned, ":bot_type_flag"),
             (try_end),  #patch1115 43/10 end
             
             #To ensure any balancing bots becomes the same squad even if player changes bot type before balancing kicks in
             (player_set_slot,":player_no",slot_player_bot_type_spawned,":selected_bot_type"),
        
           (else_try), #Spawn additional bots to balance team at the end of spawning time
             (eq,"$g_scale_squad_size",1),
             (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1), #Only add bots for spawned players
             (eq, ":round_time", multiplayer_new_agents_finish_spawning_time), #lt
             
             (lt, ":player_team", multi_team_spectator),  #if player is currently spectator do not spawn bots for him...
             (player_get_agent_id, ":player_agent", ":player_no"),
             (ge, ":player_agent", 0),
             (agent_is_active,":player_agent"),
             (agent_is_alive,":player_agent"),  #Only spawn bots for alive players...

             (try_begin),
               (eq, ":player_team", 0),
               (assign, ":entry_no", multi_initial_spawn_point_team_1),
             (else_try),
               (eq, ":player_team", 1),
               (assign, ":entry_no", multi_initial_spawn_point_team_2),
             (try_end),
             
             (call_script,"script_commander_get_additional_bots",":player_no"),
             (assign,":num_bots",reg0),
             (gt,":num_bots",0),
             (player_get_slot,":selected_bot_type",":player_no",slot_player_bot_type_spawned),
             (is_between,":selected_bot_type",multiplayer_ai_troops_begin,multiplayer_ai_troops_end), #Bot has to be valid
             (call_script,"script_scale_num_bots_after_troop_type",":selected_bot_type",":num_bots"),
             (assign,":num_bots",reg0),
             (store_current_scene, ":cur_scene"),
             (modify_visitors_at_site, ":cur_scene"),
             (add_visitors_to_current_scene, ":entry_no", ":selected_bot_type", ":num_bots", ":player_team", ":player_no"),
             
           (else_try), #spawning as a bot (if option ($g_multiplayer_player_respawn_as_bot) is 1)
             (neg|player_is_busy_with_menus, ":player_no"),
             (eq, "$g_multiplayer_player_respawn_as_bot", 1),
             
             (assign,":continue",0),
             (player_get_agent_id, ":player_agent", ":player_no"),
             (try_begin),
               (agent_is_active, ":player_agent"),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign,":continue",1),
             (else_try), #If player is dead too long (busy with menus) agent becomes inactive.
               (neg|agent_is_active, ":player_agent"), #No active agent
               (player_slot_ge, ":player_no", slot_player_spawned_this_round, 1), #But has actually spawned before
               (assign,":continue",1), #Then continue
             (try_end),
             (eq,":continue",1),
             
             (player_get_slot, ":x_coor", ":player_no", slot_player_death_pos_x),
             (player_get_slot, ":y_coor", ":player_no", slot_player_death_pos_y),
             (player_get_slot, ":z_coor", ":player_no", slot_player_death_pos_z),

             (set_fixed_point_multiplier,100),
             (init_position, pos3),
             (position_set_x, pos3, ":x_coor"),
             (position_set_y, pos3, ":y_coor"),
             (position_set_z, pos3, ":z_coor"),

             (player_get_slot, ":player_musician", ":player_no", slot_player_musician_spawned), #patch1115 43/19 begin bot #respawn
             (player_get_slot, ":player_drummer", ":player_no", slot_player_drummer_spawned),
             (player_get_slot, ":player_nco", ":player_no", slot_player_flag_spawned),
             
             (assign,":bot_agent",-1),
             (assign,":min_distance",999999),
             (assign, ":bob",-1),
             (try_for_agents,":cur_agent"),
               (agent_is_active,":cur_agent"),
               (agent_is_human,":cur_agent"),
               (agent_is_alive,":cur_agent"),
               (agent_get_team,":agent_team",":cur_agent"),
               (eq,":agent_team",":player_team"),
               (agent_get_group,":agent_group",":cur_agent"),
               (eq,":agent_group",":player_no"),
               
               (neq, ":cur_agent", ":player_nco"),
               (neq, ":cur_agent", ":player_drummer"),
               (neq, ":cur_agent", ":player_musician"),
               (agent_get_position, pos1, ":cur_agent"),
               (get_distance_between_positions, ":dist", pos3, pos1),
               (lt,":dist",":min_distance"),
               (assign,":bot_agent",":cur_agent"),               
               (assign, ":bob",1),
             (try_end),
             
             (try_begin),
               (eq, ":bob",-1),
               (try_for_agents,":cur_agent"),
                (agent_is_active,":cur_agent"),
                (agent_is_human,":cur_agent"),
                (agent_is_alive,":cur_agent"),
                (agent_get_team,":agent_team",":cur_agent"),
                (eq,":agent_team",":player_team"),
                (agent_get_group,":agent_group",":cur_agent"),
                (eq,":agent_group",":player_no"),
                
                (this_or_next|eq, ":cur_agent", ":player_nco"),
                (this_or_next|eq, ":cur_agent", ":player_drummer"),
                (eq, ":cur_agent", ":player_musician"),
                (agent_get_position, pos1, ":cur_agent"),
                (get_distance_between_positions, ":dist", pos3, pos1),
                (lt,":dist",":min_distance"), 
                (assign,":bot_agent",":cur_agent"),  
              (try_end),
             (try_end),
             #(call_script, "script_find_most_suitable_bot_to_control", ":player_no"),
             #(assign,":bot_agent",reg0),
             (gt,":bot_agent",-1),
             
             (player_control_agent, ":player_no", ":bot_agent"),
             
              # patch1115 43/19 end
 
             #Replace any fake weapons with real
             (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head),
               (agent_get_item_slot, ":item_id", ":bot_agent", ":equipment_slot"),
               (gt,":item_id",-1), # even have an item there?
               (try_begin),
                 (eq,":item_id","itm_french_briquet_garde_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_french_briquet_garde_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_french_briquet_garde", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_french_briquet_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_french_briquet_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_french_briquet", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_russian_briquet_1807_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_russian_briquet_1807_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_russian_briquet_1807", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_russian_briquet_1807_black_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_russian_briquet_1807_black_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_russian_briquet_1807_black", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_russian_briquet_1807_black_blackbelt_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_russian_briquet_1807_black_blackbelt_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_russian_briquet_1807_black_blackbelt", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_russian_briquet_1807_landwehr_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_russian_briquet_1807_landwehr_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_russian_briquet_1807_landwehr", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_russian_peasant_axe_landwehr_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_russian_peasant_axe_landwehr_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_russian_peasant_axe_landwehr", ":equipment_slot"),
               (else_try),
                 (eq,":item_id","itm_austrian_infantry_briquet_fake"),
                 (agent_unequip_item, ":bot_agent", "itm_austrian_infantry_briquet_fake", ":equipment_slot"),
                 (agent_equip_item, ":bot_agent", "itm_austrian_infantry_briquet", ":equipment_slot"),
               (try_end),
             (try_end),
             
             (player_get_slot, ":num_spawns", ":player_no", slot_player_spawned_this_round),
             (val_add, ":num_spawns", 1),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, ":num_spawns"),
           (try_end),
         (try_end),
         ]),
         
        (3.1, 0, 0, [(multiplayer_is_server),  #PATCH1115 fix 43/12 start  #music #Dunno if we want to runs this more often? It should be pretty light. Have to test and see how it feels I suppose
                 
                 #??????????????????????????????
                 #(this_or_next|eq, "$g_round_ended", 1), #Why on earth would this run AFTER round is over??????
                 (eq, "$g_round_ended", 0),
                 #??????????????????????????????
                 
                (assign,":musician_not_playing",0),
                 
                (try_for_players, ":player_no", "$g_ignore_server"),
                  (eq,":musician_not_playing",0), #Just finish this loop if we found someone, could change the loop but I guess this is still more efficient as there are very few players in this mode
                  (player_is_active, ":player_no"),

                  (player_get_team_no, ":player_team", ":player_no"), #we need to make sure this only runs on those who have a team
                  (lt, ":player_team", multi_team_spectator),

                  (player_get_troop_id, ":troop_no", ":player_no"), #we need to make sure they have a troops selected
                  (ge, ":troop_no", 0),
                 
                  (player_slot_ge, ":player_no", slot_player_spawned_this_round, 1),
                
                  (player_get_slot, ":player_musician", ":player_no", slot_player_musician_spawned),   
                  (gt, ":player_musician", 0), #If we have no musician spawned, just stop here, there won't be a drummer either
                  
                  (try_begin), 
                    (agent_is_active,":player_musician"),
                    (agent_is_alive, ":player_musician"),
                    (agent_is_non_player, ":player_musician"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                      
                    (agent_get_animation,":cur_anim",":player_musician",1), #Was 0
                    
                    (try_begin),
                      (neg|is_between,":cur_anim","anim_drum","anim_drum_end"), # Can play music but isn't
                      (assign,":musician_not_playing",1),
                    (else_try),
                      #Is currently playing music!
                      (agent_get_slot, ":track_end_time", ":player_musician", slot_agent_track_ends_at),
                      (store_mission_timer_a,":cur_time"),
                      (ge,":cur_time",":track_end_time"), #But the track has ended, so we're playing silent music!
                      
                      (assign,":musician_not_playing",1),
                    (try_end),
                  (try_end),
                  
                  (eq,":musician_not_playing",0), #Still no musician not playing, check "drummer" too (probably a fifer at this point)
                  (player_get_slot, ":player_musician", ":player_no", slot_player_drummer_spawned),
                  (gt, ":player_musician", 0), #If we have no secondary musician spawned, just stop here
                
                  (try_begin), 
                    (agent_is_active,":player_musician"),
                    (agent_is_alive, ":player_musician"),
                    (agent_is_non_player, ":player_musician"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                      
                    (agent_get_animation,":cur_anim",":player_musician",1), #Was 0
                    
                    (try_begin),
                      (neg|is_between,":cur_anim","anim_drum","anim_drum_end"), # Can play music but isn't
                      (assign,":musician_not_playing",1),
                    (else_try),
                      #Is currently playing music!
                      (agent_get_slot, ":track_end_time", ":player_musician", slot_agent_track_ends_at),
                      (store_mission_timer_a,":cur_time"),
                      (ge,":cur_time",":track_end_time"), #But the track has ended, so we're playing silent music!
                      
                      (assign,":musician_not_playing",1),
                      
                      (agent_set_animation,":player_musician","anim_drum_end",1), #Stop animation
                      (agent_stop_sound,":player_musician"), #Just to be safe
                    (try_end),
                  (try_end),
                                     
                (try_end),
              
              (eq,":musician_not_playing",1), #There's a musician that can play somewhere, but isn't, run the play code
          ],
          [
                #Okay, time to run all this again...
                (try_for_players, ":player_no", "$g_ignore_server"),
                  (player_is_active, ":player_no"),

                  (player_get_team_no, ":player_team", ":player_no"), #we need to make sure this only runs on those who have a team
                  (lt, ":player_team", multi_team_spectator),

                  (player_get_troop_id, ":troop_no", ":player_no"), #we need to make sure they have a troops selected
                  (ge, ":troop_no", 0),
                 
                  (player_slot_ge, ":player_no", slot_player_spawned_this_round, 1),
                
                  (player_get_slot, ":player_musician", ":player_no", slot_player_musician_spawned),   
                  (gt, ":player_musician", 0), #If we have no musician spawned, just stop here, there won't be a drummer either
                  
                  (assign,":player_musician2",-1), #Just if we don't have one, this is needed later
                  
                  (assign,":musician_not_playing",0),
                  (try_begin), 
                    (agent_is_active,":player_musician"),
                    (agent_is_alive, ":player_musician"),
                    (agent_is_non_player, ":player_musician"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                      
                    (agent_get_animation,":cur_anim",":player_musician",1), #Was 0
                    
                    (try_begin),
                      (neg|is_between,":cur_anim","anim_drum","anim_drum_end"), # Can play music but isn't
                      (assign,":musician_not_playing",1),
                    (else_try),
                      #Is currently playing music!
                      (agent_get_slot, ":track_end_time", ":player_musician", slot_agent_track_ends_at),
                      (store_mission_timer_a,":cur_time"),
                      (ge,":cur_time",":track_end_time"), #But the track has ended, so we're playing silent music!
                      
                      (assign,":musician_not_playing",1),
                    (try_end),
                  (try_end),
                  (try_begin), 
                    (eq,":musician_not_playing",0), #Still no musician not playing, check "drummer" too (probably a fifer at this point)
                    (player_get_slot, ":player_musician2", ":player_no", slot_player_drummer_spawned),
                    (gt, ":player_musician2", 0), #If we have no secondary musician spawned, just stop here
                    
                    (agent_is_active,":player_musician2"),
                    (agent_is_alive, ":player_musician2"),
                    (agent_is_non_player, ":player_musician2"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician2", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                      
                    (agent_get_animation,":cur_anim",":player_musician2",1), #Was 0
                    
                    (try_begin),
                      (neg|is_between,":cur_anim","anim_drum","anim_drum_end"), # Can play music but isn't
                      (assign,":musician_not_playing",1),
                    (else_try),
                      #Is currently playing music!
                      (agent_get_slot, ":track_end_time", ":player_musician2", slot_agent_track_ends_at),
                      (store_mission_timer_a,":cur_time"),
                      (ge,":cur_time",":track_end_time"), #But the track has ended, so we're playing silent music!
                      
                      (assign,":musician_not_playing",1),
                    (try_end),
                  (try_end),
                  
                  (eq,":musician_not_playing",1), #Okay, this player has some musician that can play, but isn't, so let's fix that!
                  
                  #Let's find out how many tracks we have, shall we?
                  (assign,":num_tunes",0),
                  (team_get_faction,":player_faction",":player_team"),
                  (try_begin),
                    (this_or_next|eq,":item_id","itm_drumstick_right"), #Drums and flutes have the same amount of tracks, so can run the same check for them!
                    (this_or_next|eq,":item_id","itm_flute"),
                    (eq,":item_id","itm_bagpipe"), #We're also checking bagpipes here, cause Highland drummer is here!
                    (try_begin),
                      (eq,":player_faction","fac_britain"),
                      (try_begin),
                        (player_get_agent_id, ":agent_player", ":player_no"),
                        (agent_get_troop_id,":troop_id",":agent_player"), #We're Britain, so check if we're Highlanders
                        #(this_or_next|eq,":troop_id","trp_british_highlander_drum"), 
                        (eq,":troop_id","trp_british_highlander_ai"),
                        (store_sub,":num_tunes",drum_sounds_highland_end,drum_sounds_highland_begin),
                      #(else_try),
                       # (agent_get_troop_id,":troop_id2",":player_musician2"), #We're Britain, so check if we're Highlanders
                        #(eq,":troop_id2","trp_british_highlander_drum"),
                       # (store_sub,":num_tunes",drum_sounds_highland_end,drum_sounds_highland_begin),
                      (else_try),
                        (store_sub,":num_tunes",drum_sounds_britain_end,drum_sounds_britain_begin), #Not Highlander, get normal tunes amount
                      (try_end),
                    (else_try),
                      (this_or_next|eq,":player_faction","fac_rhine"), #Rhine has French tunes
                      (eq,":player_faction","fac_france"),
                      (store_sub,":num_tunes",drum_sounds_france_end,drum_sounds_france_begin),
                    (else_try),
                      (eq,":player_faction","fac_prussia"),
                      (store_sub,":num_tunes",drum_sounds_prussia_end,drum_sounds_prussia_begin),
                    (else_try),
                      (eq,":player_faction","fac_russia"),
                      (store_sub,":num_tunes",drum_sounds_russia_end,drum_sounds_russia_begin),
                    (else_try),
                      (eq,":player_faction","fac_austria"),
                      (store_sub,":num_tunes",drum_sounds_austria_end,drum_sounds_austria_begin),
                    (try_end),
                  (else_try),
                    (is_between,":item_id","itm_horn","itm_bagpipe"), #Okay, check for horn and trumpet tracks
                    (try_begin),
                      (eq,":player_faction","fac_britain"),
                      (store_sub,":num_tunes",bugle_sounds_britain_end,bugle_sounds_britain_begin),
                    (else_try),
                      (eq,":player_faction","fac_france"),
                      (store_sub,":num_tunes",bugle_sounds_france_end,bugle_sounds_france_begin),
                    (else_try),
                      (eq,":player_faction","fac_prussia"),
                      (store_sub,":num_tunes",bugle_sounds_prussia_end,bugle_sounds_prussia_begin),
                    (else_try),
                      (eq,":player_faction","fac_russia"),
                      (store_sub,":num_tunes",bugle_sounds_russia_end,bugle_sounds_russia_begin),
                    (else_try),
                      (eq,":player_faction","fac_austria"),
                      (store_sub,":num_tunes",bugle_sounds_austria_end,bugle_sounds_austria_begin),
                    (else_try),
                      (eq,":player_faction","fac_rhine"),
                      (store_sub,":num_tunes",bugle_sounds_france_end,bugle_sounds_france_begin),
                      (val_add,":num_tunes",1), #Adding first track from Prussia
                    (try_end),
                  (try_end),
                  
                  (neq,":num_tunes",0), #If we someone still has zero tunes, something went wrong - ABORT MISSION
            
                  (store_random_in_range, ":random_tune", 0, ":num_tunes"), #Pick a random tune for us
                  
                  (try_begin), #Let's see if musician 1 is valid for this
                    (agent_is_active,":player_musician"),
                    (agent_is_alive, ":player_musician"),
                    (agent_is_non_player, ":player_musician"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                    
                    #We don't care if this guy is already playing a valid tune if the other guy isn't - we want them to play the same
                    #We also don't need to stop any currently playing music, the script here will take care of that for us
                    (call_script, "script_multiplayer_server_agent_play_music", ":player_musician", ":random_tune", 0),
                  (try_end),
                  
                  (try_begin),
                    (player_get_slot, ":player_musician2", ":player_no", slot_player_drummer_spawned), #In case we haven't gotten this guy yet
                    (neq,":player_musician2",-1), #We do have a secondary musician, let's see if they're also valid
                    (agent_is_active,":player_musician2"),
                    (agent_is_alive, ":player_musician2"),
                    (agent_is_non_player, ":player_musician2"),
                      
                    (agent_get_wielded_item, ":item_id", ":player_musician2", 0),
                    (gt,":item_id",-1),
                    (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                    (eq,":item_class",multi_item_class_type_instrument), #Has an instrument equipped - doesn't matter which, those are bots
                    
                    #We don't care if this guy is already playing a valid tune if the other guy isn't - we want them to play the same
                    #We also don't need to stop any currently playing music, the script here will take care of that for us
                    (call_script, "script_multiplayer_server_agent_play_music", ":player_musician2", ":random_tune", 0),
                  (try_end),
                  
                (try_end),
		
	   ]), #PATCH1115 fix 43/12 end

      (5.11, 1, 0, [(multiplayer_is_server)],
       [
        (try_begin),
          (store_mission_timer_a, ":time"),
          (store_sub, ":elapsed_time", ":time", "$g_round_start_time"),
          (ge, ":elapsed_time", 10),
          
          (assign,":num_players_team_1",0),#relying alone on time to give orders is meh.  not perfect.  this should work better
          (assign,":num_players_team_2",0),
          (try_for_players, ":agent_group_leader", "$g_ignore_server"),
           (player_is_active, ":agent_group_leader"),
           (player_get_agent_id,":agent_id",":agent_group_leader"),
           (agent_is_active,":agent_id"),
           (agent_is_alive,":agent_id"),
           (agent_get_team,":team",":agent_id"),
           (try_begin),
             (eq,":team",0),
             (val_add,":num_players_team_1",1),
           (else_try),
             (eq,":team",1),
             (val_add,":num_players_team_2",1),
           (try_end),
         (try_end),
         (ge,":num_players_team_1",1),
         (ge,":num_players_team_2",1),
          
         (try_for_players, ":agent_group_leader", "$g_ignore_server"),
           (player_is_active,":agent_group_leader"),
            
           (player_slot_eq, ":agent_group_leader", slot_player_bot_order, 0),
            
           (player_get_agent_id, ":player_agent_id", ":agent_group_leader"),
           (agent_is_active,":player_agent_id"),
           (agent_is_alive,":player_agent_id"),
            
           (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_musician_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (neq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_instrument),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
          
          #Musician 2
          (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_drummer_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (neq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_instrument),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
          
          #Flag
          (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_flag_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (neq,":item_class",multi_item_class_type_flag),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_flag),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
            #(set_show_messages, 0),
            #(team_give_order, ":player_no", grc_everyone, mordr_use_melee_weapons),#Make them have flags out
            #(team_give_order, ":player_no", grc_everyone, mordr_fire_at_will),#Make them have flags out
            #(team_give_order, ":player_no", grc_everyone, mordr_use_blunt_weapons),
            #(set_show_messages, 1),
            (player_set_slot, ":agent_group_leader", slot_player_bot_order, 1),
          (try_end),
        (try_end),
      ]),
      
 #    multiplayer_server_bonuses_cb = ( # Officer and flag Bonuses #patch1115 43/16 begin
  (4.31, 0, 0, [(multiplayer_is_server),(eq,"$g_bonuses_enabled",1)],
  [
    (set_fixed_point_multiplier,100),
  
    (store_mul,":bonus_value_10",10,"$g_bonus_strength"), 
    (val_div,":bonus_value_10",100),
    (store_mul,":bonus_value_5",5,"$g_bonus_strength"), 
    (val_div,":bonus_value_5",100),
  
    (try_for_agents, ":agent"),
      (agent_is_active,":agent"),
      (agent_is_alive, ":agent"), 
      (agent_is_human, ":agent"), 
      (agent_get_group, ":agent_group_leader", ":agent"),
      (gt,":agent_group_leader",-1),
      (player_is_active, ":agent_group_leader"),
      (player_get_agent_id, ":leader", ":agent_group_leader"),
      (agent_is_active,":leader"),      
      (agent_get_troop_id, ":player_troop_id", ":leader"),
      
      (troop_get_slot,":agent_class",":player_troop_id",slot_troop_class_type),
      
      (player_get_slot, ":player_musician", ":agent_group_leader", slot_player_musician_spawned),
      (player_get_slot, ":player_drummer", ":agent_group_leader", slot_player_drummer_spawned),
      (player_get_slot, ":player_nco", ":agent_group_leader", slot_player_flag_spawned),
      
      (assign,":affected_by_num_captains",0),
      (assign,":affected_by_num_flags",0),
      (assign,":affected_by_num_sergeants",0),
      (assign,":affected_by_num_musicians",0),
      
      (try_begin),
        (gt, ":player_musician", 0),
        (agent_is_active,":player_musician"),
        (agent_is_alive, ":player_musician"), 
        #(assign,":affected_by_num_musicians",1),
        (val_add,":affected_by_num_musicians",1), #lets make it so more than musician adds a stronger bonus
      (try_end),
      
      (try_begin),
        (gt, ":player_drummer", 0),
        (agent_is_active,":player_drummer"),  #drummers are just drummers, the above is fluts, pipers, and horns
        (agent_is_alive, ":player_drummer"),
        #(assign,":affected_by_num_musicians",1),
        (val_add,":affected_by_num_musicians",1), #lets make it so more than musician adds a stronger bonus
      (try_end),
      
      (try_begin),
        (gt, ":player_nco", 0),        
        (agent_is_active,":player_nco"),
        (agent_is_alive, ":player_nco"),
        (try_begin),
          (neq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":affected_by_num_flags",1),
        (else_try),
          (assign,":affected_by_num_sergeants",1), 
        (try_end),
      (try_end),
      
      (try_begin),
        (agent_is_alive, ":leader"),
        (troop_get_slot,":agent_group_leader_rank",":player_troop_id",slot_troop_rank),
        (eq,":agent_group_leader_rank",mm_rank_officer),
        (assign,":affected_by_num_captains",1),   
      (try_end),
            
      (assign,":mod_damage",100),
      (assign,":mod_accuracy",100),
      (assign,":mod_speed",100),
      (assign,":mod_speed_2",100),
      (assign,":mod_reload_speed",100),
      (assign,":mod_use_speed",100),
      (try_begin),
        (gt,":affected_by_num_captains",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":bonus_value",":bonus_value_5"),
          (val_add,":mod_accuracy",":bonus_value"),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_10"),
          (val_add,":mod_speed_2",":bonus_value"),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_artillery),
          (assign,":bonus_value",":bonus_value_10"),
          (val_add,":mod_use_speed",":bonus_value"),
        (try_end),
      (else_try),
        (eq,":affected_by_num_captains",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":mod_accuracy",100),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          (assign,":mod_speed_2",100),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_artillery),
          (assign,":mod_use_speed",100),
        (try_end),
      (try_end),
      (try_begin),
        (gt,":affected_by_num_flags",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          (assign,":bonus_value",":bonus_value_10"),
          (val_add,":mod_damage",":bonus_value"),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_10"),
          (val_add,":mod_speed",":bonus_value"),
         # (assign, ":is_bob_good", 1),
        (try_end),     
      (else_try),
        (gt,":affected_by_num_sergeants",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          (assign,":bonus_value",":bonus_value_5"),
          (val_add,":mod_damage",":bonus_value"),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          #This bonus apply to non-rankers as well
          (assign,":bonus_value",":bonus_value_5"),
          (val_add,":mod_speed",":bonus_value"),
        (try_end),      
      (try_end),
      (try_begin),
        (eq,":affected_by_num_sergeants",0),
        (eq,":affected_by_num_flags",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          (assign,":mod_damage",100),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":mod_speed",100),
          #(eq, ":is_bob_good", 1),
        (try_end),
      (try_end),  
      (try_begin),
        (gt,":affected_by_num_musicians",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":bonus_value",":bonus_value_10"),
          (try_begin),
            (gt,":affected_by_num_musicians",1), #More than 1 musician
            (val_add,":bonus_value",":bonus_value_5"), #50% more bonus       
          (try_end),
          (val_add,":mod_reload_speed",":bonus_value"),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_cavalry),        
          (assign,":bonus_value",":bonus_value_10"),
          (val_add,":mod_damage",":bonus_value"),         
        (try_end),
      (else_try),
        (eq,":affected_by_num_musicians",0),
        (try_begin),
          (this_or_next|eq,":agent_class",multi_troop_class_mm_infantry),
          (eq,":agent_class",multi_troop_class_mm_skirmisher),
          (assign,":mod_reload_speed",100),
        (else_try),
          (eq,":agent_class",multi_troop_class_mm_cavalry),
          (assign,":mod_damage",100),
        (try_end),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":agent", slot_agent_cur_damage_modifier, ":mod_damage"),
        (agent_set_damage_modifier, ":agent", ":mod_damage"), # value is in percentage, 100 is default
        (agent_set_slot, ":agent", slot_agent_cur_damage_modifier, ":mod_damage"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":agent", slot_agent_cur_accuracy_modifier, ":mod_accuracy"),
        (agent_set_accuracy_modifier, ":agent", ":mod_accuracy"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":agent", slot_agent_cur_accuracy_modifier, ":mod_accuracy"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":agent", slot_agent_cur_reload_speed_modifier, ":mod_reload_speed"),
        (agent_set_reload_speed_modifier, ":agent", ":mod_reload_speed"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":agent", slot_agent_cur_reload_speed_modifier, ":mod_reload_speed"),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":agent", slot_agent_cur_use_speed_modifier, ":mod_use_speed"),
        (agent_set_use_speed_modifier, ":agent", ":mod_use_speed"), # value is in percentage, 100 is default, value can be between [0..1000]
        (agent_set_slot, ":agent", slot_agent_cur_use_speed_modifier, ":mod_use_speed"),
      (try_end), 
      (try_begin), #Apply speed bonuses to the horse of mounted players
        (agent_get_horse,":horse",":agent"),
        (gt,":horse",-1),
        (try_begin),
          #(neg|agent_slot_eq, ":horse", slot_agent_cur_speed_modifier, ":mod_speed"),
         # (agent_set_speed_modifier, ":horse", ":mod_speed"),
          #(agent_set_slot, ":horse", slot_agent_cur_speed_modifier, ":mod_speed"),
          (neg|agent_slot_eq, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
          (agent_set_horse_speed_factor, ":agent", ":mod_speed_2"),
          (agent_set_slot, ":horse", slot_agent_cur_speed_modifier, ":mod_speed_2"),
        (try_end),
      (try_end),
      (try_begin),
        (neg|agent_slot_eq, ":agent", slot_agent_god_mode, 1),
        (neg|agent_slot_eq,":agent",slot_agent_base_speed_mod,55),
        (neg|agent_slot_eq, ":agent", slot_agent_cur_speed_modifier, ":mod_speed"),
        (agent_set_speed_modifier, ":agent", ":mod_speed"), # value is in percentage, 100 is default, value can be between [0..1000] # player_agent_id
        (agent_set_slot, ":agent", slot_agent_cur_speed_modifier, ":mod_speed"),
      (try_end),
    (try_end),
  ]), #patch1115 43/16 end
  
      (ti_on_order_issued, 0, 0, [(multiplayer_is_server)], #orders  #patch1115 fix 43/18 start
      [ 
        (store_trigger_param_1,":order"),
        (store_trigger_param_2,":agent2"),
        
        #(try_for_agents, ":agent"),
        (try_begin),
          (agent_is_active,":agent2"),
          #(agent_is_alive, ":agent"),
          #(agent_is_human, ":agent"), 
          
          #(agent_get_group, ":agent_group_leader", ":agent"),
          #(gt,":agent_group_leader",-1),
          #(player_is_active, ":agent_group_leader"),
          (agent_get_player_id, ":agent_group_leader", ":agent2"),
          (player_is_active, ":agent_group_leader"),
         # (eq, ":leader", ":agent2"),
         
          (assign,":order_type",-1),
          (try_begin),
            (this_or_next|eq, ":order", mordr_charge),
            (eq, ":order", mordr_use_melee_weapons),
            (assign,":order_type",0),
          (else_try),
            #(this_or_next|eq, ":order", mordr_hold),
            #(this_or_next|eq, ":order", mordr_follow),
            (this_or_next|eq, ":order", mordr_use_any_weapon),
            (eq, ":order", mordr_fire_at_will),
            (assign,":order_type",1),
          (try_end),
          (neq,":order_type",-1),
          
          #Musician 1
          (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_musician_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (eq,":order_type",0),
              (eq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slot"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (neq,":item_class",multi_item_class_type_instrument),            
                (agent_set_wielded_item, ":agent_id", ":item_id"), 
              (try_end), 
            (else_try),
              (eq,":order_type",1),
              (neq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_instrument),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
          
          #Musician 2
          (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_drummer_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (eq,":order_type",0),
              (eq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slot"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (neq,":item_class",multi_item_class_type_instrument),            
                (agent_set_wielded_item, ":agent_id", ":item_id"), 
              (try_end), 
            (else_try),
              (eq,":order_type",1),
              (neq,":item_class",multi_item_class_type_instrument),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_instrument),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
          
          #Flag
          (try_begin),
            (player_get_slot, ":agent_id", ":agent_group_leader", slot_player_flag_spawned),
            (agent_is_active,":agent_id"),
            (agent_is_alive, ":agent_id"),
            (agent_is_human, ":agent_id"), 
            (agent_is_non_player,":agent_id"),
            (agent_get_wielded_item, ":item_id", ":agent_id", 0),
            (gt,":item_id",-1),
            (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
            (try_begin),
              (eq,":order_type",0),
              (eq,":item_class",multi_item_class_type_flag),
              (try_for_range_backwards,":equipment_slot",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slot"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (neq,":item_class",multi_item_class_type_flag),            
                (agent_set_wielded_item, ":agent_id", ":item_id"), 
              (try_end), 
            (else_try),
              (eq,":order_type",1),
              (neq,":item_class",multi_item_class_type_flag),
              (try_for_range_backwards,":equipment_slott",ek_item_0,ek_head),
                (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slott"),        
                (gt,":item_id",-1),            
                (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
                (eq,":item_class",multi_item_class_type_flag),    
                (agent_set_wielded_item, ":agent_id", ":item_id"),            
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      ]),  #patch1115 fix 43/18 end
      
      
   (ti_on_order_issued, 0, 0, [(eq, "$g_no_line_inf_spread", 1)], #orders  #patch1115 fix 63/1 start
      [ 
        (store_trigger_param_1,":order"),
        (store_trigger_param_2,":agent2"),
        
        (assign,":order_type",-1),
        (try_begin),
          (agent_is_active,":agent2"),
          (agent_get_player_id, ":agent_group_leader", ":agent2"),
          (player_is_active, ":agent_group_leader"),
          
          (player_get_slot, ":formation_change", ":agent_group_leader", slot_player_formation_change),
          
          (agent_get_troop_id, ":player_troop_id", ":agent2"),
          (troop_get_slot,":agent_class",":player_troop_id",slot_troop_class_type),
          (this_or_next|eq, ":agent_class", multi_troop_class_mm_infantry),
          (eq, ":agent_class", multi_troop_class_mm_grenadier),
          
          
          (try_begin),
            (eq, ":order", mordr_spread_out),
            (assign,":order_type",0),
          (else_try),
            (eq, ":order", mordr_stand_closer),
            (assign,":order_type",1),
          (try_end),
        (try_end),
          (gt, ":order_type",-1),
          
         
         (try_begin),
         # (multiplayer_is_server),#we are changing what we want out of this. time to rewrite
         # (try_begin),
            (eq,":order_type",0),
            (eq, ":formation_change", 0),
            (team_give_order, ":agent_group_leader", grc_everyone, mordr_stand_closer),
            (player_set_slot, ":agent_group_leader", slot_player_formation_change_2, 1),
          (else_try),
            (eq,":order_type",0),
            (eq, ":formation_change", 1),
            (player_set_slot, ":agent_group_leader", slot_player_formation_change, 0),
          (else_try),
            (eq,":order_type",1),
            (eq, ":formation_change", 0),
            (player_set_slot, ":agent_group_leader", slot_player_formation_change, 1),
            (player_set_slot, ":agent_group_leader", slot_player_formation_change_2, 0),
         # (try_end),
        (try_end),
        
         (try_begin),
           (neg|multiplayer_is_dedicated_server),
          (try_begin),
            (player_slot_eq, ":agent_group_leader", slot_player_formation_change_2, 1),
            (call_script, "script_client_get_my_agent"),
            (assign,":my_agent",reg0),
            (eq, ":my_agent", ":agent2"),
            (display_message, "str_line_inf_spread"),
          (try_end),
        (try_end),
                 
           ]), #patch1115 fix 63/1 end
           
      #multiplayer_server_spawn_bots, 
      #multiplayer_server_manage_bots, 

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
         
         # 18
         
      ] + mm_multiplayer_common,
  ),

    
    (
    "multiplayer_duel",mtf_battle_mode,-1, #duel mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      multiplayer_server_check_polls,  multiplayer_server_generate_build_points,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_duel),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         #make everyone see themselves as allies, no friendly fire
         (team_set_relation, 0, 0, 1),
         (team_set_relation, 0, 1, 1),
         (team_set_relation, 1, 1, 1),
         (mission_set_duel_mode, 1),
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
                                                                        # to be able to edit maps without damaging any headquarters flags ext. 
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
       ]),
      
      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (call_script, "script_initialize_all_scene_prop_slots"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/8
         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin),
           (call_script,"script_client_get_my_agent"),
           (assign,":player_agent",reg0),
           (agent_is_active, ":player_agent"),
           (agent_slot_ge, ":player_agent", slot_agent_in_duel_with, 0),
           (try_begin),
             (eq, ":dead_agent_no", ":player_agent"),
             (display_message, "str_you_have_lost_a_duel"),
           (else_try),
             (agent_slot_eq, ":player_agent", slot_agent_in_duel_with, ":dead_agent_no"),
             (display_message, "str_you_have_won_a_duel"),
           (try_end),
         (try_end),
         (try_begin),
           (agent_slot_ge, ":dead_agent_no", slot_agent_in_duel_with, 0),
           (agent_get_slot, ":duelist_agent_no", ":dead_agent_no", slot_agent_in_duel_with),
           (agent_set_slot, ":dead_agent_no", slot_agent_in_duel_with, -1),
           (try_begin),
             (agent_is_active, ":duelist_agent_no"),
             (agent_set_slot, ":duelist_agent_no", slot_agent_in_duel_with, -1),
             (agent_clear_relations_with_agents, ":duelist_agent_no"),
             (try_begin),
               (agent_get_player_id, ":duelist_player_no", ":duelist_agent_no"),
               (neg|player_is_active, ":duelist_player_no"), #might be AI
               (agent_force_rethink, ":duelist_agent_no"),
             (try_end),
           (try_end),
         (try_end),
         
         # Vincenzo begin
         # Won duel, set health to 100%
         (try_begin),
           (multiplayer_is_server),
           (agent_is_active,":killer_agent_no"),
           (agent_is_active,":dead_agent_no"),
           (agent_is_human,":dead_agent_no"),
           
           (agent_set_hit_points, ":killer_agent_no", 100, 0), # Heal the player
           
           (agent_refill_ammo,":killer_agent_no"), # and refill ammo.
           
           (agent_get_horse, ":horse_agent", ":killer_agent_no"),
           (agent_is_active,":horse_agent"),
           (agent_set_hit_points, ":horse_agent", 100, 0), # Heal the Horse
         (try_end),
         # Vincenzo end
         ]),
				 
				  (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),],
       [
			   (assign, "$g_round_ended", 0),
			   (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
         #MM
         #(call_script, "script_multiplayer_mm_reset_stuff_after_round"),
			 ]),
			 
      
      (1, 0, 0, [(multiplayer_is_server),],
       [
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0.1, 0, 0, [ (multiplayer_is_server),
                  (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
                  (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
                  (gt, ":total_req", 0),
                ],
       [
         (try_begin),
           (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
           
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
         
         #checking for restarting the map
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),

           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

			 
      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),

      (1, 0, 0, [],
       [
         (store_mission_timer_a, ":mission_timer"),
         (store_sub, ":duel_start_time", ":mission_timer", 3),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_slot_ge, ":cur_agent", slot_agent_in_duel_with, 0),
           (agent_get_slot, ":duel_time", ":cur_agent", slot_agent_duel_start_time),
           (ge, ":duel_time", 0),
           (le, ":duel_time", ":duel_start_time"),
           (agent_set_slot, ":cur_agent", slot_agent_duel_start_time, -1),
           (agent_get_slot, ":opponent_agent", ":cur_agent", slot_agent_in_duel_with),
           (agent_is_active, ":opponent_agent"),
           (agent_add_relation_with_agent, ":cur_agent", ":opponent_agent", -1),
           (agent_force_rethink, ":cur_agent"),
         (try_end),
         ]),
      ] + mm_multiplayer_common,
  ),
  
  (
    "multiplayer_kh", mtf_battle_mode,-1, #king of the hill mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,
      
      multiplayer_server_check_polls, multiplayer_server_generate_build_points,
      multiplayer_server_bonuses, multiplayer_server_auto_ff,
       
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (try_begin),
             (lt, "$my_team_at_start_of_round", 0),
             (multiplayer_get_my_player, ":my_player_no"),
             (ge, ":my_player_no", 0),
             (player_get_agent_id, ":my_agent_id", ":my_player_no"),
             (eq, ":my_agent_id", ":agent_no"),
             (ge, ":my_agent_id", 0),
             (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
           (try_end),
           (try_begin),
             (neg|multiplayer_is_server),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
             (try_begin),
               (eq, "$g_team_balance_next_round", 1),
               (assign, "$g_team_balance_next_round", 0),
             (try_end),
           (try_end),  
         (try_end),  
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_king),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
		 
         (try_begin),
           (multiplayer_is_server),
           (try_for_range, ":cur_flag_slot", multi_data_flag_pull_code_begin, multi_data_flag_pull_code_end),
             (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
           (try_end),
         (try_end),
         
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (assign, "$g_flag_is_not_ready", 0),
		 
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
		 
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),         
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/9
         
         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
		 
         (assign, "$g_number_of_flags", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           #place base flags
           (entry_point_get_position, pos1, 90), #multi_siege_flag_point),
           (set_spawn_position, pos1),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),         
           (position_move_z, pos1, multi_headquarters_pole_height),         
           (set_spawn_position, pos1),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0), 
           (set_spawn_position, pos1),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0), 
           (set_spawn_position, pos1),
           (spawn_scene_prop, "spr_headquarters_flag_gray_code_only", 0),
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 0),
           (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", 0),
		   
		   (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", "$g_number_of_flags"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 0),
           (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", "$g_number_of_flags"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 0),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", "$g_number_of_flags"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 1),
         (try_end),
         (val_add, "$g_number_of_flags", 1),
		 
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
       ]),         

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (neg|multiplayer_is_dedicated_server),
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (agent_is_active,":my_agent_id"),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),
         
         (try_begin),
           (multiplayer_is_server),
           (neg|agent_is_non_player, ":dead_agent_no"),
           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (player_set_slot, ":dead_agent_player_id", slot_player_spawned_this_round, 0),
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
      [
        #trigger for (a) counting seconds of flags being owned by their owners & (b) to calculate seconds past after that flag's pull message has shown          
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          #part a: counting seconds of flags being owned by their owners
          (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owned_seconds", "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot"),
          (val_add, ":cur_flag_owned_seconds", 1),
          (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", ":cur_flag_owned_seconds"),
          #part b: to calculate seconds past after that flag's pull message has shown
          (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
          (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
          (try_begin),
            (ge, ":cur_flag_pull_code", 100),
            (lt, ":cur_flag_pull_message_seconds_past", 25),
            (val_add, ":cur_flag_pull_code", 1),
            (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":cur_flag_pull_code"),
          (try_end),
        (try_end),        
      ]),               
	  
      # Vincenzo change seconds
      (1.07, 0, 0, [(multiplayer_is_server),], #if this trigger takes lots of time in the future and make server machine runs headqurters mod
                    #very slow with lots of players make period of this trigger 1 seconds, but best is 0. Currently
                    #we are testing this mod with few players and no speed program occured.
      [
        #main trigger which controls which agent is moving/near which flag.
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),
        
          (assign, ":number_of_agents_around_flag_team_1", 0),
          (assign, ":number_of_agents_around_flag_team_2", 0),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.

          # REMOVED TO ALLOW BOTS TO CAPTURE FLAGS
          #(try_for_range, ":player_no", 0, ":num_players"),
          #  (player_is_active, ":player_no"),
          #  (player_get_agent_id, ":cur_agent", ":player_no"),
          #  (ge, ":cur_agent", 0),
          (set_fixed_point_multiplier,100),
          (try_for_agents,":cur_agent",pos3,901),
            (agent_is_active,":cur_agent"),
            (agent_is_human,":cur_agent"),
            #/Added above
            (agent_is_alive, ":cur_agent"),
            (agent_get_team, ":cur_agent_team", ":cur_agent"),
            (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
            (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),
            (get_sq_distance_between_position_heights, ":squared_height_dist", pos3, pos1),
            (val_add, ":squared_dist", ":squared_height_dist"),
            # Vincenzo begin
            (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags + 900),
            # Vincenzo end
            (try_begin),
              (eq, ":cur_agent_team", 0),
              (val_add, ":number_of_agents_around_flag_team_1", 1),
            (else_try),
              (eq, ":cur_agent_team", 1),
              (val_add, ":number_of_agents_around_flag_team_2", 1),
            (try_end),
          (try_end),

          (try_begin),
            (this_or_next|neq, ":old_team_1_agent_count", ":number_of_agents_around_flag_team_1"),
            (neq, ":old_team_2_agent_count", ":number_of_agents_around_flag_team_2"),

            (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

            (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
            #(troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
            #(store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
            #(store_div, ":cur_flag_puller_team_last", ":cur_flag_pull_code", 100),

            (try_begin),        
              (assign, ":continue", 0),
              (try_begin),
                (neq, ":cur_flag_owner", 1),
                (eq, ":old_team_1_agent_count", 0),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 1),
                (assign, ":continue", 1),
              (else_try),
                (neq, ":cur_flag_owner", 2),
                (eq, ":old_team_2_agent_count", 0),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 2),
                (assign, ":continue", 1),
              (try_end),
 
              (eq, ":continue", 1),

              (store_mul, ":puller_team_multiplied_by_100", ":puller_team", 100),
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":puller_team_multiplied_by_100"),
            (try_end),
			
            (try_begin),
              (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
              (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),        
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
              #for only server itself----------------------------
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (assign, ":new_flag_owner", -1),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos3, ":pole_id"), #pos3 holds pole position.            

          (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

          (try_begin),
            (try_begin),
              (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 1),
              (eq, ":flag_visibility", 0),
              (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 2),
              (eq, ":flag_visibility", 0),                    
              (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),        
              (assign, ":cur_shown_flag", 0),
            (try_end),

            #flag_id holds shown flag after this point
            (prop_instance_get_position, pos1, ":flag_id"), #pos1 holds gray/red/blue (current shown) flag position.

            (try_begin),
              (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),        
              # Vincenzo begin              
              (lt, ":squared_dist", multi_headquarters_distance_sq_to_change_flag + 500), #if distance is less than 2 meters
              # Vincenzo end
              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 2),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (neq, ":cur_shown_flag", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 0),
              (try_end),
            (else_try),
              (neq, ":cur_flag_owner", ":cur_shown_flag"),      
              (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),        
              (ge, ":squared_dist", multi_headquarters_distance_sq_to_set_flag), #if distance is more equal than 9 meters

              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (eq, ":cur_shown_flag", 1),
                (assign, ":new_flag_owner", 1),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":cur_shown_flag", 2),
                (assign, ":new_flag_owner", 2),
                (assign, ":new_shown_flag", 2),
              (try_end),        
            (try_end),
          (try_end),
        
          (try_begin),
            (ge, ":new_flag_owner", 0),
            (this_or_next|neq, ":new_flag_owner", ":cur_flag_owner"),
            (neq, ":cur_shown_flag", ":new_shown_flag"),

            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_set_num_agents_around_flag", ":flag_no", ":cur_flag_players_around"),
            #for only server itself-----------------------------------------------------------------------------------------------
            #(assign, ":number_of_total_players", 0),
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":cur_flag_players_around"),
              #(val_add, ":number_of_total_players", 1),
            (try_end),

            (store_mul, ":owner_code", ":new_flag_owner", 100),
            (val_add, ":owner_code", ":new_shown_flag"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_change_flag_owner", ":flag_no", ":owner_code"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":flag_no", ":owner_code"),          
            (try_end),

            (try_begin),
              (neq, ":new_flag_owner", 0),

              #Award players that captured the flag with points
              (prop_instance_get_position, pos3, ":pole_id"),
              (try_for_players, ":player_no", "$g_ignore_server"),
                (player_is_active, ":player_no"),
                (player_get_agent_id, ":cur_agent", ":player_no"),
                (agent_is_active,":cur_agent"),
                (agent_get_team, ":cur_agent_team", ":cur_agent"),
                (val_add, ":cur_agent_team", 1),
                (eq, ":cur_agent_team", ":new_flag_owner"),
                
                (agent_get_position, pos1, ":cur_agent"),  
                (get_sq_distance_between_positions, ":squared_dist", pos3, pos1),
                (get_sq_distance_between_position_heights, ":squared_height_dist", pos3, pos1),
                (val_add, ":squared_dist", ":squared_height_dist"),
                # Vincenzo begin
                (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags + 900),        
                # Vincenzo end                
                (player_get_score, ":player_score", ":player_no"), #give score to player which helped flag to be owned by new_flag_owner team 
                (val_add, ":player_score", 5), #Gain 5 points for capturing the flag
                (player_set_score, ":player_no", ":player_score"),                            
              (try_end),

              
              #And end the round!
              (try_begin),
                (eq, ":new_flag_owner", 1),
                (assign, "$g_winner_team", 0),
              (else_try),
                (assign, "$g_winner_team", 1),
              (try_end),

              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_draw_this_round", "$g_winner_team"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (try_for_players, ":player_no", 1),
                (player_is_active, ":player_no"),
                (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
        ]),

      (1, 0, 0, [(multiplayer_is_server),(eq, "$g_round_ended", 0)],
       [ 
         (store_mission_timer_a, ":round_time"),
         (val_sub, ":round_time", "$g_round_start_time"),
        
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
           
           (neg|player_is_busy_with_menus, ":player_no"),
           
           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),
           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),
           (player_get_agent_id, ":player_agent", ":player_no"), #new added for siege mod
         
           (assign, ":spawn_new", 0),
           (try_begin),
			 (player_slot_eq,":player_no",slot_player_first_spawn,1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),

           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
           

           (try_begin),
             (eq, ":player_team", 0), #Defenders
             (assign, ":entry_no", 22), # Spawn at entry 22
           (else_try),
             (eq, ":player_team", 1), #Attackers
             (assign, ":entry_no", 44), # Spawn at entry 44
           (try_end),

           (player_spawn_new_agent, ":player_no", ":entry_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
         (try_end),
         ]),

      (1.06, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), #new died (< g_multiplayer_respawn_period) so will be counted too
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),
         
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         # Vincenzo begin
         # teamswap
         (try_begin),
           (eq,"$g_auto_swap",1), # Auto Swap enabled.
           
           (str_clear, s2),
           (str_store_string, s4, "str_swap_all_s2"),
           
           (call_script, "script_multiplayer_broadcast_message"),
           
           (team_get_score, ":team_1_score", 0),
           (team_get_score, ":team_2_score", 1),
           (team_set_score, 0, ":team_2_score"),
           (team_set_score, 1, ":team_1_score"),           
           
           (try_for_players, ":cur_player", "$g_ignore_server"),
             (player_is_active, ":cur_player"),
             
             (call_script, "script_multiplayer_server_swap_player", ":cur_player"),
             
             (neq,":cur_player",0),
             (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_set_team_score, ":team_2_score", ":team_1_score"),
           (try_end),
         (try_end),         
         # Vincenzo end
       
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (try_for_players, ":cur_player", "$g_ignore_server"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),                      
               (try_for_players, ":player_no", "$g_ignore_server"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (call_script,"script_multiplayer_server_send_player_score_kill_death",":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),
             
             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here                           
             (try_for_players, ":player_no", 1),
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           (player_set_slot, ":player_no", slot_player_first_spawn, 1),
           
           # AoN
           (neq,":player_no",0),
           (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_before_round_end),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1), 
        
         (call_script, "script_multiplayer_mm_reset_stuff_after_round_before_clear"),
        
         #clear scene and end round
         (multiplayer_clear_scene),

         (call_script, "script_initialize_objects"),

         #initialize moveable object positions
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
        

         #initialize flag coordinates (move up the flag at pole)
         (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         
            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_set_num_agents_around_flag", ":flag_no", 0),
            #for only server itself-----------------------------------------------------------------------------------------------
            #(assign, ":number_of_total_players", 0),
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", 0),
              #(val_add, ":number_of_total_players", 1),
            (try_end),
            
            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_change_flag_owner", ":flag_no", 0),
            #for only server itself-----------------------------------------------------------------------------------------------
            (try_for_players, ":player_no", 1),
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":flag_no", 0),          
            (try_end),
            
            
           (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
           (prop_instance_get_position, pos1, ":pole_id"),
           (position_move_z, pos1, multi_headquarters_pole_height),
           (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
           (prop_instance_stop_animating, ":flag_id"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 0),
           (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
           (prop_instance_stop_animating, ":flag_id"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 0),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
           (prop_instance_stop_animating, ":flag_id"),
           (prop_instance_set_position, ":flag_id", pos1),
           (scene_prop_set_visibility, ":flag_id", 1),
         (try_end),
         
         (assign, "$g_round_ended", 0),
         
         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start time for clients
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999),
         (try_end),            

         (assign, "$g_flag_is_not_ready", 0),
         
         #MM
         (call_script, "script_multiplayer_mm_reset_stuff_after_round"),
       ]),
           
      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

      multiplayer_server_check_end_map,
         
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),


    ("multiplayer_br",mtf_battle_mode,-1, #battle royale mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [ 
      
      multiplayer_server_check_polls, multiplayer_server_generate_build_points,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_royale),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
                                                                        # to be able to edit maps without damaging any headquarters flags ext.
         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (server_add_message_to_log,"str_map_changed"),#patch1115 fix 3/1

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         #MM
         (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [         
         (neg|multiplayer_is_dedicated_server),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
      
      (1, 0, 0, [(multiplayer_is_server),],
       [
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1.07, 0, 0, [ (multiplayer_is_server),
                  (this_or_next|gt,"$g_multiplayer_num_bots_team_1",0),
                  (gt,"$g_multiplayer_num_bots_team_2",0), # are there any bots? :p
                ], #do this in every new frame, but not at the same time
       [
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_active, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0.1, 0, 0, [(multiplayer_is_server),
                   (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
                   (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
                   (gt, ":total_req", 0),],
       [
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [(multiplayer_is_server),],
       [
         #checking for restarting the map
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           
           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ] + mm_multiplayer_common,
  ),

  (
    "multiplayer_cm",mtf_battle_mode,-1, # Scene making mode.
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
    
      # (0, 0, 3, [(key_is_down,key_left_control),(key_clicked,key_n),],
       # [
        # (rebuild_shadow_map),
         # ]),
         
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_scene_making),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),

         #MM
         (call_script, "script_multiplayer_mm_before_mission_start_common"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
         (call_script, "script_multiplayer_generate_weather"),
         #MM
        # (call_script, "script_multiplayer_mm_after_mission_start_common"),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [(neg|multiplayer_is_dedicated_server),],
       [
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
      
      (1, 0, 0, [(multiplayer_is_server),],
       [
         (try_for_players, ":player_no", "$g_ignore_server"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),
  
  

## SINGLE PLAYER MISSIONS ##
  
   ("sp_campaign_vienna",mtf_battle_mode,-1,"Vienna Bridge",     #VIENNA Battle
    [
      #France - player
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]), #Player Spawn
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troop Spawn
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion Spawn
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Allies Spawn
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Allies location 2
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Player location
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troops location
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion location
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Allies location 1
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Marshal spawn
      #Austria - enemy
      (10,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 1 Spawn
      (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 2 Spawn
      (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Bridge head point
      (13,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Negotiators Spawn
      (14,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 1 Location
      (15,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 2 Location
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Hussars Spawn
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Arty Spawn
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Bridge Guard Spawn
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Bridge Guard Spawn
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Bridge Guard Spawn
      #Extra
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Player target location
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Objective 2 player start location
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Artillery location
     ],
    [
    
    (ti_before_mission_start, 0, 0, [],
      [
        #Set up weather and daytime
        (scene_set_day_time,12),
        #(set_rain,1,0), #No more damn rain...
        #(set_fog_distance,150,0xEDE3D6),
        
        #Adding inital troops
        (modify_visitors_at_site,"scn_sp_vienna"),
        
        #French
        (add_visitors_to_current_scene,1,"trp_french_old_guard_ai",40),
        
        #Insert player companions here
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          (troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,2,":cur_companion",1),
        (try_end),
        
        #Allies
        (add_visitors_to_current_scene,3,"trp_french_old_guard_ai",14),
        
        #Lannes
        #(add_visitors_to_current_scene,9,"trp_quick_battle_troop_france_2",1),
        #Murat
        #(add_visitors_to_current_scene,9,"trp_quick_battle_troop_france_3",1),
        
        #Austrians (currently Russians...)
        #Lines
        (add_visitors_to_current_scene,10,"trp_russian_infantry_ai",18),
        (add_visitors_to_current_scene,11,"trp_russian_infantry_ai",18),
        #Negotiators
        (add_visitors_to_current_scene,13,"trp_russian_infantry_ai",10),
        (add_visitors_to_current_scene,13,"trp_russian_infantry_officer",2),
        #Arty
        (add_visitors_to_current_scene,17,"trp_russian_arty",3),
        (add_visitors_to_current_scene,17,"trp_russian_arty_officer",1),
        
        (try_for_range,":value",0,20),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",20,40),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",40,60),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",60,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",80,100),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",100,120),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        
        #No order for Bridge guards, Marshals or Arty officer
        (troop_set_slot,"trp_custom_battle_dummy",103,mm_order_none),
        (troop_set_slot,"trp_custom_battle_dummy",115,mm_order_none),
        (troop_set_slot,"trp_custom_battle_dummy",117,mm_order_none),
        
        (call_script,"script_sp_common_before_mission_start"),
      
        (team_set_relation,0,1,0), #Teams are neutral at start (won't attack each other)
      
        #For skipping the initial cutscene
        (assign,"$g_guards_spawned",0),
        (assign,"$g_cut_scene_skipped",0),
        (assign,"$g_player_discovered",0),
        
        (assign,"$g_battle_won",0),
        (assign, "$g_mission_state", 0),
        ## Mission states ##
        # 0 - Begin cut scene
        # 1 - Clear the bridge
        # 2 - Clear complete, hide on other side of river
        # 3 - Cut scene 2
        # 4 - Defeat the artillery
        # 5 - Cut scene 3
        # 6 - Defeat the Austrian counter attack
        # 7 - Battle Won
      ]),
        
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         #(agent_get_troop_id, ":troop_id", ":agent_no"),         
         (agent_get_team,":agent_team",":agent_no"),
         #(troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         (assign,":initial_courage_score",3000), #Just give everyone the same for now
         
         (store_random_in_range, ":randomised_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomised_addition_courage"),
         (try_begin),
           (eq,":agent_team",0),
           (val_mul, ":initial_courage_score", "$g_global_morale_modifier"),
           (val_div, ":initial_courage_score", 10),
         (try_end),
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (try_begin),
           (eq,":entry_no",1),
           (agent_set_division,":agent_no",0), #Player bots
         (else_try),
           (eq,":entry_no",2),
           (agent_set_division,":agent_no",1), #Player companions
         (else_try),
           (eq,":entry_no",3),
           (agent_set_division,":agent_no",2), #Allies
         (else_try),
           (eq,":entry_no",9),
           (agent_set_division,":agent_no",3), #Marshals
           (agent_get_troop_id,":troop_id",":agent_no"),
           (try_begin),
             #(eq,":troop_id","trp_quick_battle_troop_france_2"), #Lannes
             (assign,"$g_marshal_lannes_agent",":agent_no"),
           (else_try),
             #(eq,":troop_id","trp_quick_battle_troop_france_3"), #Murat
             (assign,"$g_marshal_murat_agent",":agent_no"),
           (try_end),
         (else_try),
           (eq,":entry_no",10),
           (agent_set_division,":agent_no",0), #Line 1
         (else_try),
           (eq,":entry_no",11),
           (agent_set_division,":agent_no",1), #Line 2
         (else_try),
           (eq,":entry_no",13),
           (agent_get_troop_id,":troop_id",":agent_no"),
           (try_begin),
             (eq,":troop_id","trp_russian_infantry_officer"),
             (agent_set_division,":agent_no",6), #Officers
           (else_try),
             (agent_set_division,":agent_no",2), #Guards
           (try_end),
         (else_try),
           (eq,":entry_no",16),
           (agent_set_division,":agent_no",3), #Hussars
         (else_try),
           (eq,":entry_no",17),
           (try_begin),
             (eq,":troop_id","trp_russian_arty_officer"),
             (agent_set_division,":agent_no",5), #Officer
             (assign,"$g_enemy_commander_agent_1",":agent_no"),
           (else_try),
             (agent_set_division,":agent_no",4), #Artillery rankers
           (try_end),
         (else_try),
           (is_between,":entry_no",18,21),
           (agent_set_division,":agent_no",7), #Bridge Guards
           (entry_point_get_position,pos2,":entry_no"),
           (position_rotate_z,pos2,180),
           (agent_set_scripted_destination,":agent_no",pos2),
           (agent_set_slot,":agent_no",slot_agent_state,1),
           (agent_get_troop_id,":troop_id",":agent_no"),
           (troop_get_inventory_capacity,":inv_cap",":troop_id"),
           (try_for_range,":inv_slot",0,":inv_cap"),
             (troop_get_inventory_slot,":item_id",":troop_id",":inv_slot"),
             (gt,":item_id",-1),
             (item_get_type,":item_type",":item_id"),
             (eq,":item_type",itp_type_crossbow),
             (agent_set_wielded_item,":agent_no",":item_id"),
             (assign,":inv_cap",0),
           (try_end),
         (try_end),
         
         (try_begin),
           #(agent_get_troop_id,":troop_id",":agent_no"),
           #(this_or_next|eq,":troop_id","trp_russian_infantry_ai"),
           #(this_or_next|eq,":troop_id","trp_russian_grenadier_ai"),
           #(this_or_next|eq,":troop_id","trp_french_old_guard_ai"),
           #(this_or_next|eq,":troop_id","trp_quick_battle_troop_france_2"),
           #(eq,":troop_id","trp_quick_battle_troop_france_3"),
           (agent_set_speed_limit,":agent_no",5),
         (try_end),
         
         (call_script, "script_correct_num_troops_in_formation", ":agent_no", 1), #Because I'm lazy ;D
         ]),
      		 
      (0, 0, ti_once, [],
        [
         (try_for_range,":unused",0,20),
          (init_position,pos1),
          (set_spawn_position,pos1),
          (spawn_scene_prop,"spr_formation_locator"),
          (scene_prop_set_visibility,reg0,0),
         (try_end),
         
         (entry_point_get_position,pos4,1),
         (scene_prop_get_instance,":instance","spr_formation_locator",0),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,2),
         (scene_prop_get_instance,":instance","spr_formation_locator",1),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,3),
         (scene_prop_get_instance,":instance","spr_formation_locator",2),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,9),
         (scene_prop_get_instance,":instance","spr_formation_locator",3),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,10),
         (scene_prop_get_instance,":instance","spr_formation_locator",10),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,11),
         (scene_prop_get_instance,":instance","spr_formation_locator",11),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,13),
         (scene_prop_get_instance,":instance","spr_formation_locator",12),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,16),
         (scene_prop_get_instance,":instance","spr_formation_locator",13),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,17),
         (scene_prop_get_instance,":instance","spr_formation_locator",14),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,13),
         (position_move_y,pos4,300,0),
         (position_set_z_to_ground_level,pos4),
         (scene_prop_get_instance,":instance","spr_formation_locator",16),
         (prop_instance_animate_to_position,":instance",pos4,0),
         
         (try_for_range,":formation_slot_no",40,52),
           (troop_set_slot,"trp_custom_battle_dummy",":formation_slot_no",mm_order_column),
         (try_end),
            
         ]),
         
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        (call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),
        
        (call_script, "script_sp_process_death_for_battle_results", ":dead_agent_no", ":killer_agent_no"),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),


      (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
       [
        (start_presentation,"prsnt_new_order_stuff"),
       ]),
  		 
      (0, 0, 1, [], #Volley fire
       [
        (call_script, "script_volley_fire"),
       ]),
       
      (0, 0, 1, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
         #(set_fog_distance,150,0xEDE3D6),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_2",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_2",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_3",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_3",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_4",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_4",0),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_pointer_arrow"),
         (assign,"$g_hold_position_arrow_instance",reg0),
         (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         
         
         (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
         (try_for_range,":prop_no",0,":num_instances"),
           (scene_prop_get_instance,":prop_id","spr_mm_sp_crate_explosive",":prop_no"),
           (scene_prop_set_slot,":prop_id",scene_prop_slot_is_active,1),
         (try_end),
         ]),

      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",25),     
          (try_for_agents, ":agent_no"),
            (agent_is_active, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
              
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      common_battle_order_panel,
      common_battle_order_panel_tick,
      
      common_battle_victory_display,
      
    ## Mission states ##
    # 0 - Begin cut scene
    # 1 - Clear the bridge
    # 2 - Clear complete, hide on other side of river
    # 3 - Cut scene 2
    # 4 - Defeat the artillery
    # 5 - Cut scene 3
    # 6 - Defeat the Austrian counter attack
    # 7 - Battle Won
    
      (0, 0, 1, [  #Allow skipping the cut scene by pressing "m" (for testing purposes)
        (key_clicked,key_m),
        (eq, "$g_mission_state", 0),
      ],
      [
        (assign,"$g_cut_scene_skipped",1),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (entry_point_get_position,pos2,12),
        (position_move_z,pos2,900),
        (position_rotate_z,pos2,-90),
        (position_move_y,pos2,-5000,0),
        (position_move_x,pos2,8000,0),
        (position_rotate_x,pos2,-20),
        (mission_cam_set_position,pos2),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",500),
      ],
      [
        #Quickly deploy everyone via teleport to avoid problems
        (try_for_range,":team",0,2),
          (try_for_range,":division",0,9),
            (call_script,"script_deploy_division_via_teleport",":team",":division"),
          (try_end),
        (try_end),
        #And equip them with weapons
        (try_for_agents,":agent"),
          (agent_is_active, ":agent"),
          (agent_get_troop_id,":troop_id",":agent"),
          (troop_get_inventory_capacity,":inv_cap",":troop_id"),
          (try_for_range,":inv_slot",0,":inv_cap"),
            (troop_get_inventory_slot,":item_id",":troop_id",":inv_slot"),
            (gt,":item_id",-1),
            (item_get_type,":item_type",":item_id"),
            (eq,":item_type",itp_type_crossbow),
            (agent_set_wielded_item,":agent",":item_id"),
            (assign,":inv_cap",0),
          (try_end),
        (try_end),
        #Start moving Austrian troops across the bridge
        (entry_point_get_position,pos4,14),
        (scene_prop_get_instance,":instance","spr_formation_locator",10),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,15),
        (scene_prop_get_instance,":instance","spr_formation_locator",11),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (start_presentation,"prsnt_singleplayer_cutscene_bars"),
      ]),
      
      # Shows a bird's eye view of the river with Austrian units crossing the bridges
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",1000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 3000),
        (mission_cam_get_position,pos2),
        (position_move_z,pos2,-150),
        (position_move_y,pos2,400,0),
        (mission_cam_animate_to_position,pos2,15000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",1200),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_1"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",15000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        #Start moving the French troops towards the bridge
        (entry_point_get_position,pos4,6),
        (scene_prop_get_instance,":instance","spr_formation_locator",0),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,8),
        (scene_prop_get_instance,":instance","spr_formation_locator",2),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      # Shows the French advancing
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",16000)],
      [
        #Move Austrians lines into position right away
        (call_script,"script_deploy_division_via_teleport",1,0),
        (call_script,"script_deploy_division_via_teleport",1,1),
        #Continue the cutscene
        (entry_point_get_position,pos2,3),
        (position_move_z,pos2,400),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-500,0),
        (position_rotate_x,pos2,-25),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",16500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_2"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",21000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (add_visitors_to_current_scene,18,"trp_russian_grenadier_ai",1),
        (add_visitors_to_current_scene,19,"trp_russian_grenadier_ai",1),
        (add_visitors_to_current_scene,20,"trp_russian_grenadier_ai",1),
        (assign,"$g_guards_spawned",1),
      ]),
      
      # Shows explosive barrels and Austrians
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",22000)],
      [
        (entry_point_get_position,pos2,11),
        (position_move_z,pos2,300),
        (position_rotate_z,pos2,-90),
        (position_move_y,pos2,-300,0),
        (position_rotate_x,pos2,-15),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2500),
        (entry_point_get_position,pos2,12),
        (position_move_z,pos2,300),
        (position_rotate_z,pos2,-90),
        (position_move_y,pos2,-300,0),
        (position_rotate_x,pos2,-15),
        (mission_cam_animate_to_position,pos2,10000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",22500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_3"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",31000)],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
      ]),
      
      # Shows Murat and Lannes looking over the river.
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",32000)],
      [
        (entry_point_get_position,pos2,9),
        (position_move_z,pos2,300),
        (position_move_y,pos2,-300,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",32500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_4"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",37000),
      ],
      [
        (tutorial_message,-1),
      ]),
      
      # Shows Murat and Lannes moving.
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",38000)],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_5"),
        #(tutorial_message_set_position, 500, 100),
        (entry_point_get_position,pos2,12),
        (agent_set_scripted_destination,"$g_marshal_lannes_agent",pos2,0),
        (agent_set_scripted_destination,"$g_marshal_murat_agent",pos2,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",42000)],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (entry_point_get_position,pos4,12),
        (scene_prop_get_instance,":instance","spr_formation_locator",2),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      # Player's character walking into view and hiding behind a bush
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",44000)],
      [
        (entry_point_get_position,pos2,5),
        (position_move_z,pos2,300),
        (position_move_y,pos2,-300,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",44300),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_vienna_6"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",47000)],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (assign,"$g_show_cutscene_bars",0),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (assign,":continue",0),
      (try_begin),
        (eq,"$g_cut_scene_skipped",1),
        (assign,":continue",1),
      (else_try),
        (store_mission_timer_a_msec,":mt"),
        (gt,":mt",48200),
        (assign,":continue",1),
      (try_end),
      (eq,":continue",1),
      ],
      [ 
        (assign,"$g_show_cutscene_bars",0),
        (try_begin),  #If cut scene was skipped guards might not be spawned - if so, spawn them here
          (neq,"$g_guards_spawned",1),
          (add_visitors_to_current_scene,18,"trp_russian_grenadier_ai",1),
          (add_visitors_to_current_scene,19,"trp_russian_grenadier_ai",1),
          (add_visitors_to_current_scene,20,"trp_russian_grenadier_ai",1),
        (try_end),
        #Teleport troops to starting positions
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",2),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (troop_set_slot,"trp_custom_battle_dummy",42,mm_order_line),
        (entry_point_get_position,pos4,6),
        (scene_prop_get_instance,":instance","spr_formation_locator",0),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,7),
        (scene_prop_get_instance,":instance","spr_formation_locator",1),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,14),
        (scene_prop_get_instance,":instance","spr_formation_locator",10),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,15),
        (scene_prop_get_instance,":instance","spr_formation_locator",11),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (try_for_range,":team",0,2),
          (try_for_range,":division",0,9),
            (call_script,"script_deploy_division_via_teleport",":team",":division"),
          (try_end),
        (try_end),
        (entry_point_get_position,pos4,4),
        (position_move_y,pos4,300,0),
        (position_move_x,pos4,-100,0),
        (agent_set_scripted_destination,"$g_marshal_murat_agent",pos4,0),
        (agent_get_horse,":horse","$g_marshal_murat_agent"),
        (agent_set_position,":horse",pos4),
        (position_move_x,pos4,200,0),
        (agent_set_scripted_destination,"$g_marshal_lannes_agent",pos4,0),
        (agent_get_horse,":horse","$g_marshal_lannes_agent"),
        (agent_set_position,":horse",pos4),
        (entry_point_get_position,pos4,5),
        (get_player_agent_no,":player_agent"),
        (agent_set_position,":player_agent",pos4),
        #Start the mission
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (assign, "$g_mission_state", 1),# 1 - Clear the bridge
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Clear the bridge of all powder crates while the marshals are negotiating.^Take care not to be discovered by the guards."),
        (assign, "$g_projection_state", 4),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
        (assign,"$g_singleplayer_progress_counter_max_value",":num_instances"),
        (assign,"$g_singleplayer_progress_counter_string_id","str_vienna_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign,"$g_player_discovered",0),
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_is_non_player,":cur_agent"),
          (agent_get_team,":team_no",":cur_agent"),
          (eq,":team_no",1),
          (agent_get_division,":division",":cur_agent"),
          (eq,":division",7), #Bridge guards
          (agent_add_relation_with_agent, ":player_agent", ":cur_agent", -1), #So player can kill the guards...
        (try_end),
      ]),
          
      (0, 0, 0, [(eq, "$g_mission_state", 1),],  #Mark nearby crates with target locator
      [
        (init_position,pos1),
        (init_position,pos2),
        (init_position,pos3),
        (init_position,pos4),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos7,":player_agent"),
        (assign,":min_distance_1",99999),
        (assign,":min_distance_2",99999),
        (assign,":min_distance_3",99999),
        (assign,":min_distance_4",99999),
        (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
        (assign,":num_crates_left",0),
        (try_for_range,":prop_no",0,":num_instances"),
          (scene_prop_get_instance,":prop_id","spr_mm_sp_crate_explosive",":prop_no"),
          (scene_prop_slot_eq,":prop_id",scene_prop_slot_is_active,1),
          (prop_instance_get_position,pos8,":prop_id"),
          (get_distance_between_positions,":distance",pos7,pos8),
          (try_begin),
            (lt,":distance",":min_distance_1"),
            (assign,":min_distance_4",":min_distance_3"),
            (assign,":min_distance_3",":min_distance_2"),
            (assign,":min_distance_2",":min_distance_1"),
            (assign,":min_distance_1",":distance"),
            (copy_position,pos4,pos3),
            (copy_position,pos3,pos2),
            (copy_position,pos2,pos1),
            (copy_position,pos1,pos8),
          (else_try),
            (lt,":distance",":min_distance_2"),
            (assign,":min_distance_4",":min_distance_3"),
            (assign,":min_distance_3",":min_distance_2"),
            (assign,":min_distance_2",":distance"),
            (copy_position,pos4,pos3),
            (copy_position,pos3,pos2),
            (copy_position,pos2,pos8),
          (else_try),
            (lt,":distance",":min_distance_3"),
            (assign,":min_distance_4",":min_distance_3"),
            (assign,":min_distance_3",":distance"),
            (copy_position,pos4,pos3),
            (copy_position,pos3,pos8),
          (else_try),
            (lt,":distance",":min_distance_4"),
            (assign,":min_distance_4",":distance"),
            (copy_position,pos4,pos8),
          (try_end),
          (val_add,":num_crates_left",1),
        (try_end),
        (try_begin),
          (gt,":num_crates_left",0),
          (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos1,0), 
          (try_begin),
            (gt,":num_crates_left",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos2,0),
            (try_begin),
              (gt,":num_crates_left",2),
              (prop_instance_animate_to_position,"$g_objectives_locator_instance_3",pos3,0),
              (try_begin),
                (gt,":num_crates_left",3),
                (prop_instance_animate_to_position,"$g_objectives_locator_instance_4",pos4,0),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
        (store_sub,":num_crates_cleared",":num_instances",":num_crates_left"),
        (assign,"$g_singleplayer_progress_counter_cur_value",":num_crates_cleared"),
        (assign,":cur_projection_state",":num_crates_left"),
        (try_begin),
          (gt,":cur_projection_state",4),
          (assign,":cur_projection_state",4),
        (try_end),
        (assign, "$g_projection_state",":cur_projection_state"),
        (try_begin),
          (eq,":num_crates_cleared",":num_instances"), #All crates cleared - continue
          (assign, "$g_mission_state", 2), # 2 - Clear complete, hide on other side of river(tutorial_message_set_background, 1),
          (tutorial_message_set_background, 1),
          (tutorial_message,"@The bridge has been successfully cleared, well done!^Now hide on the other Austrian side of the river and wait for the negotiations to conclude."),
          (assign, "$g_singleplayer_progress_counter_mode", -1),
          (assign, "$g_projection_state", 1),
          (start_presentation,"prsnt_singleplayer_objective_projection_display"),
          (entry_point_get_position,pos1,21),
          (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos1,0),
        (try_end),
      ]),
      
      (1, 0, 0, [(eq, "$g_mission_state", 1)],#Checking if crates are on bridge  
      [
        (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
        (try_for_range,":prop_no",0,":num_instances"),
          (scene_prop_get_instance,":prop_id","spr_mm_sp_crate_explosive",":prop_no"),
          (scene_prop_slot_eq,":prop_id",scene_prop_slot_is_active,1),
          (prop_instance_get_position,pos8,":prop_id"),
          (position_get_z,":z",pos8),
          (lt,":z",50),
          (scene_prop_set_slot,":prop_id",scene_prop_slot_is_active,0),
        (try_end),
      ]),
      
      (1, 0, 0, [  #Marching Guards back and forth
      (lt, "$g_mission_state", 3),
      ],
      [
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_is_non_player,":cur_agent"),
          (agent_get_team,":team_no",":cur_agent"),
          (eq,":team_no",1),
          (agent_get_division,":division",":cur_agent"),
          (eq,":division",7), #Bridge guards
          (agent_slot_eq,":cur_agent",slot_agent_state,1),
          
          (agent_get_position,pos5,":cur_agent"),
          (agent_get_scripted_destination,pos6,":cur_agent"),
          (get_distance_between_positions,":distance",pos5,pos6),
          (lt,":distance",200),
          (position_rotate_z,pos6,180),
          (position_move_y,pos6,2000,0),
          (agent_set_scripted_destination,":cur_agent",pos6,0),
        (try_end),
      ]),
      
    (1, 0, 0, [(is_between, "$g_mission_state", 1, 3)],  #Stealth!
    [
      (try_for_agents,":cur_agent"),
        (agent_is_active,":cur_agent"),
        (agent_is_alive,":cur_agent"),
        (agent_is_non_player,":cur_agent"),
        (agent_get_team,":team_no",":cur_agent"),
        (eq,":team_no",1),
        (agent_get_division,":division",":cur_agent"),
        (eq,":division",7), #Bridge guards
        
        (agent_get_look_position,pos5,":cur_agent"),
        (position_move_z,pos5,180),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos6,":player_agent"),
        #(agent_get_animation,":cur_anim",":player_agent",0),
        (try_begin),
          #(eq,":cur_anim","anim_kneeling"),
          (position_move_z,pos6,130),
        (else_try),
          (position_move_z,pos6,180),
        (try_end),
        (try_begin),
          (get_distance_between_positions_in_meters,":distance",pos5,pos6),
          (lt,":distance",20),
          (neg|position_is_behind_position,pos6,pos5),
          (position_has_line_of_sight_to_position,pos5,pos6),
          (agent_set_slot,":cur_agent",slot_agent_state,0),
          (agent_clear_scripted_mode,":cur_agent"),
          (agent_add_relation_with_agent, ":cur_agent", ":player_agent", -1), #Enemies
          (eq,"$g_player_discovered",0),
          (assign,"$g_player_discovered",1),
          (display_message,"@You've been discovered! Quickly kill the guard before he raises the alarm!",0xF00000),
        (try_end),
      (try_end),
    ]),
      
      (0, 15, 2, [
        (eq,"$g_mission_state",1),
        (eq,"$g_player_discovered",1),
      ],
      [
        (try_begin),
          (eq,"$g_mission_state",1),
          (eq,"$g_player_discovered",1),
          (get_player_agent_no,":player_agent"),
          (agent_is_alive,":player_agent"),
          (assign,":bridge_guards_alive_and_following_player",0),
          (try_for_agents,":cur_agent"),
            (agent_is_active,":cur_agent"),
            (agent_is_alive,":cur_agent"),
            (agent_is_non_player,":cur_agent"),
            (agent_get_team,":team_no",":cur_agent"),
            (eq,":team_no",1),
            (agent_get_division,":division",":cur_agent"),
            (eq,":division",7), #Bridge guards
            (agent_slot_eq,":cur_agent",slot_agent_state,0),
            (val_add,":bridge_guards_alive_and_following_player",1),
          (try_end),
          (gt,":bridge_guards_alive_and_following_player",0),
          (try_for_agents,":cur_agent"),
            (agent_is_active,":cur_agent"),
            (agent_add_relation_with_agent,":cur_agent",":player_agent",0),
          (try_end),
          (assign, "$g_projection_state", 0),
          (tutorial_message,-1),
          (assign, "$g_singleplayer_progress_counter_mode", -1),
          (mission_cam_set_mode, 1),
          (mission_cam_clear_target_agent),
          (mission_cam_set_screen_color, 0xFF000000),
          (entry_point_get_position,pos2,11),
          (position_move_z,pos2,300),
          (position_rotate_z,pos2,-90),
          (position_move_y,pos2,-300,0),
          (position_rotate_x,pos2,-15),
          (mission_cam_set_position,pos2),
          (mission_cam_animate_to_screen_color, 0x00000000, 2500),
          (entry_point_get_position,pos2,12),
          (position_move_z,pos2,300),
          (position_rotate_z,pos2,-90),
          (position_move_y,pos2,-300,0),
          (position_rotate_x,pos2,-15),
          (mission_cam_animate_to_position,pos2,14000),
          (assign,"$g_player_discovered",2),
          (assign,"$g_cur_crate",0),
        (else_try),
          (eq,"$g_player_discovered",1),
          (assign,"$g_player_discovered",0),
        (try_end),
      ]),
      
      (0.5, 0, 0, [
        (eq,"$g_mission_state",1),
        (eq,"$g_player_discovered",2),
      ],
      [
        (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
        (try_begin),
          (lt,"$g_cur_crate",":num_instances"),
          (try_begin),
            (scene_prop_get_instance,":prop_id","spr_mm_sp_crate_explosive","$g_cur_crate"),
            (scene_prop_slot_eq,":prop_id",scene_prop_slot_is_active,1),
            (prop_instance_get_position,pos3,":prop_id"),
            (copy_position,pos47,pos3),
            (position_move_z,pos3,500),
            (prop_instance_set_position,":prop_id",pos3),
            (prop_instance_animate_to_position,":prop_id",pos3),
            (call_script,"script_explosion_at_position",-1,300,400),
          (try_end),
        (else_try),
          (eq,"$g_cur_crate",":num_instances"),
          (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (else_try),
          (val_add,":num_instances",4),
          (eq,"$g_cur_crate",":num_instances"),
          (finish_mission,0),
        (try_end),
        (val_add,"$g_cur_crate",1),
      ]),
      
      (1, 0, ti_once, [#Checking if player has reached destination
      (eq, "$g_mission_state", 2),
      (entry_point_get_position,pos1,21),
      (get_player_agent_no,":player_agent"),
      (agent_get_position,pos2,":player_agent"),
      (get_distance_between_positions,":dist",pos1,pos2),
      (lt,":dist",150),
      ],
      [
        (assign, "$g_projection_state", 0),
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
        (assign, "$g_mission_state", 3),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",500),
      ],
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",700),
      ],
      [
        (agent_get_position,pos2,"$g_marshal_lannes_agent"),
        (position_move_z,pos2,240),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-200,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (start_presentation,"prsnt_singleplayer_cutscene_bars"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",1000),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Lannes: '... Yes, that is correct, a truce was already signed. The war is over.'"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5500),
      ],
      [
        (try_for_agents,":agent"),
          (agent_is_active,":agent"),
          (agent_is_alive,":agent"),
          (agent_get_team,":team",":agent"),
          (eq,":team",1),
          (agent_get_division,":division",":agent"),
          (eq,":division",6),
          (assign,":officer",":agent"),
        (try_end),
        (agent_get_position,pos2,":officer"),
        (position_move_z,pos2,180),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-200,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5800),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Austrian Officer: 'Uhh.. Ok... Hey! What is that? The powder crates on the bridge are gone! We've been tricked! Attack!'"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",10000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",10500),
      ],
      [     
        #Setting things up for a brawl...
        (team_set_relation,0,1,-1), #Teams are enemies
        (try_for_agents,":cur_agent"), #Ensure the Marshals aren't fighting and/or killed...
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (neq,":cur_agent","$g_marshal_lannes_agent"),
          (neq,":cur_agent","$g_marshal_murat_agent"),
          (agent_add_relation_with_agent,":cur_agent","$g_marshal_lannes_agent",0),
          (agent_add_relation_with_agent,":cur_agent","$g_marshal_murat_agent",0),
          (agent_add_relation_with_agent,"$g_marshal_lannes_agent",":cur_agent",0),
          (agent_add_relation_with_agent,"$g_marshal_murat_agent",":cur_agent",0),
        (try_end),
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_division,":division",":cur_agent"),
          (eq,":division",2), #Both teams use the same division for guards...
          (agent_get_wielded_item,":item_id",":cur_agent",0),
          (ge,":item_id",0),
          (item_get_type,":item_type",":item_id"),
          (eq,":item_type",itp_type_crossbow),
          (agent_unequip_item,":cur_agent",":item_id"),
          (val_add,":item_id",1),
          (agent_equip_item,":cur_agent",":item_id"),
          (agent_set_wielded_item,":cur_agent",":item_id"),   #A brawl, not a shooting match
        (try_end),
        (troop_set_slot,"trp_custom_battle_dummy",102,mm_order_charge), #Charge the guards
        (troop_set_slot,"trp_custom_battle_dummy",112,mm_order_charge),
        #Setting up mission camera
        (entry_point_get_position,pos2,13),
        (position_move_y,pos2,400,0),
        (position_rotate_z,pos2,90),
        (position_move_y,pos2,-700,0),
        (position_move_z,pos2,400),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 500),
      ]),
      
      (ti_on_agent_hit, 0, 0,  [  #People shouldn't die so fast in cut scenes
      (this_or_next|eq, "$g_mission_state", 3),
      (eq, "$g_mission_state", 5),
      ],
      [
        #(store_trigger_param_1,":attacker_agent"),
        (store_trigger_param_2,":hit_agent"),
        (store_trigger_param_3,":damage"),
        (try_begin),
          (get_player_agent_no,":player_agent"),
          (eq,":hit_agent",":player_agent"),  #Ensure player can't be killed during cut scenes
          (set_trigger_result,0),
        (else_try),
          (val_div,":damage",10), #Only deal 10% damage during cut scene
          (set_trigger_result,":damage"),
        (try_end),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",14000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",14500),
      ],
      [
        (entry_point_get_position,pos2,6),
        (position_move_z,pos2,180),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-200,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",14800),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@French Soldier: 'Look, a fight! We must help our comrades. Quickly, cross the bridge!'"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",19000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
        (entry_point_get_position,pos4,12),
        (scene_prop_get_instance,":instance","spr_formation_locator",1),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (position_move_y,pos4,500,0),
        (scene_prop_get_instance,":instance","spr_formation_locator",0),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",19500),
      ],
      [
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_team,":team",":cur_agent"),
          (eq,":team",0),
          (agent_get_division,":division",":cur_agent"),
          (is_between,":division",0,2),
          (agent_set_speed_limit,":cur_agent",100),
        (try_end),
        (entry_point_get_position,pos2,19),
        (position_move_z,pos2,500),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",22000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",22500),
      ],
      [
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_is_human,":cur_agent"),
          (agent_get_troop_id,":troop_id",":cur_agent"),
          (eq,":troop_id","trp_russian_arty_officer"),
          (assign,":target_agent",":cur_agent"),
        (try_end),
        (agent_get_position,pos2,":target_agent"),
        (position_move_z,pos2,180),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-200,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",23300),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Artillery Captain: 'The French are trying to cross the bridge. Man the guns!'"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",26000),
      ],
      [
        (tutorial_message,-1),
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
        (entry_point_get_position,pos4,23),
        (scene_prop_get_instance,":instance","spr_formation_locator",14),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (troop_set_slot,"trp_custom_battle_dummy",54,mm_order_skirmish),
        (position_move_x,pos4,500,0),
        (try_begin),
          (agent_is_active,"$g_enemy_commander_agent_1"),
          (agent_set_scripted_destination,"$g_enemy_commander_agent_1",pos4),
        (try_end),
        (entry_point_get_position,pos2,22),
        (get_player_agent_no,":player_agent"),
        (agent_set_position,":player_agent",pos2),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",26500),
      ],
      [
        (mission_cam_set_mode, 0),
        (assign,"$g_show_cutscene_bars",0),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Prevent the Austrian artillery from firing on the French crossing the bridge."),
        (assign, "$g_projection_state", 4),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (assign, "$g_mission_state", 4), # 4 - Defeat the artillery
        (troop_set_slot,"trp_custom_battle_dummy",103,mm_order_retreat),
      ]),
      
      (0, 0, 0, [
      (eq, "$g_mission_state", 4), #Projection display
      ],
      [
        (assign,":cur_projection",1),
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_team,":team",":cur_agent"),
          (eq,":team",1),
          (agent_get_division,":division",":cur_agent"),
          (is_between,":division",4,6),
          (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
          (try_begin),
            (eq,":cur_projection",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos1,0), 
          (else_try),
            (eq,":cur_projection",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos1,0), 
          (else_try),
            (eq,":cur_projection",3),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_3",pos1,0), 
          (else_try),
            (eq,":cur_projection",4),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_4",pos1,0), 
          (try_end),
          (val_add,":cur_projection",1),
        (try_end),
        (val_sub,":cur_projection",1),
        (assign, "$g_projection_state", ":cur_projection"),
        (try_begin),
          (eq,":cur_projection",0),
          (tutorial_message,-1),
        (try_end),
      ]),
      
      (1, 0, ti_once, [
      (eq, "$g_mission_state", 4),
      (call_script,"script_division_get_average_position",0,0),
      (copy_position,pos1,pos0),
      (entry_point_get_position,pos2,12),
      (get_distance_between_positions,":dist",pos1,pos2),
      (lt,":dist",3000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 500),
        (tutorial_message,-1),
        (assign, "$g_projection_state", 0),
        (assign, "$g_mission_state", 5), # 5 - Cut scene 3
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [ # Cut scene 3
      (eq, "$g_mission_state", 5),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",500),
      ],
      [
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_team,":team",":cur_agent"),
          (eq,":team",1),
          (agent_get_division,":division",":cur_agent"),
          (is_between,":division",0,2),
          (agent_set_speed_limit,":cur_agent",100),
        (try_end),
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (entry_point_get_position,pos2,14),
        (position_move_z,pos2,300),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-800,0),
        (mission_cam_set_position,pos2),
        (entry_point_get_position,pos2,15),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,180),
        (position_move_y,pos2,-500,0),
        (mission_cam_animate_to_position,pos2,5000),
        (start_presentation,"prsnt_singleplayer_cutscene_bars"),
        (entry_point_get_position,pos4,12),
        (scene_prop_get_instance,":instance","spr_formation_locator",10),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (scene_prop_get_instance,":instance","spr_formation_locator",11),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 5),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",1200),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@The Austrians are launching a counter-attack!"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 5),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",4300),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [ # Cut scene 3 end
      (eq, "$g_mission_state", 5),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5500),
      ],
      [
        (mission_cam_set_mode, 0),
        (assign,"$g_show_cutscene_bars",0),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Fight back the Austrian counter-attack!"),
        (assign, "$g_mission_state", 6), # 6 - Defeat the Austrian counter attack
        (assign,"$g_hussars_spawned",0),
      ]),
        
      (0, 0, 3, [(eq, "$g_mission_state", 6)],  #Charge lines when enemy close
      [
        (try_for_range,":division",0,2),
          (store_add,":division_slot",110,":division"),
          (troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_hold),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",1000),
          (lt,":min_dist",300),
          (team_give_order,1,":division",mordr_charge),
          (try_for_agents,":cur_agent"),
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",1),
            (agent_get_division,":agent_div",":cur_agent"),
            (eq,":agent_div",":division"), 
            (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
            #Cancel scripted destination for charge:
            (agent_clear_scripted_mode,":cur_agent"),
          (try_end),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_charge),
        (try_end),
      ]),
      
      (1, 0, 0, [(eq, "$g_mission_state", 6)],  #If a formation is broken, don't let it reform again
      [
        (try_for_range,":division",0,8),
          (assign,":continue",1),
          (try_begin),
            (eq,":division",3), #Hussars spawn later, so make sure they don't start by routing...
            (eq,"$g_hussars_spawned",0),
            (assign,":continue",0),
          (try_end),
          (eq,":continue",1),
          (store_add,":division_slot",30,":division"),
          (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
          (le,":num_troops_in_division",0),
          (store_add,":division_slot",110,":division"),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_retreat),
        (try_end),
      ]),
      
      (0, 0, ti_once, [  #Spawn hussars once the Austrians start wavering
      (eq, "$g_mission_state", 6),
      (assign,":total_troops_left",0),
      (try_for_range,":division",0,8),
        (neq,":division",3),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (val_add,":total_troops_left",":num_troops_in_division"),
      (try_end),
      (le,":total_troops_left",30), #Roughly half of the Austrians left
      ],
      [
        (add_visitors_to_current_scene,16,"trp_russian_hussar_ai",12),
        (team_give_order,1,3,mordr_charge),
        (try_for_agents,":cur_agent"),
          (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
          (agent_is_alive,":cur_agent"),
          (agent_get_team,":agent_team",":cur_agent"),
          (eq,":agent_team",1),
          (agent_get_division,":agent_div",":cur_agent"),
          (eq,":agent_div",3), 
          (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
          #Cancel scripted destination for charge:
          (agent_clear_scripted_mode,":cur_agent"),
        (try_end),
        (troop_set_slot,"trp_custom_battle_dummy",113,mm_order_charge),
        (assign,"$g_hussars_spawned",1),
      ]),
      
      (1, 0, ti_once, [  # Checking Win Condition
      (eq, "$g_mission_state", 6),
      (assign,":enemy_defeated",1),
      (try_for_range,":division",0,8),
        (eq,":enemy_defeated",1),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (gt,":num_troops_in_division",0),
        (assign,":enemy_defeated",0),
      (try_end),
      (eq,":enemy_defeated",1),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@The brigde is now under firm French control. Well done!"),
        (assign, "$g_mission_state", 7), # 7 - Battle Won
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 7),], 
      [
        (assign,"$g_battle_won",1),
      ]),
      
    (ti_tab_pressed, 0, 0, [],
      [
        (try_begin),
          (eq, "$g_mission_state", 7), #Battle won
          (val_add,"$g_finished_missions",1),
          (assign,"$g_finished_sub_missions",0),
          (finish_mission,0),
        (else_try),
          (question_box,"str_confirm_quit_mission"),
        (try_end),
      ]),
    (ti_question_answered, 0, 0, [],
      [
        (store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (start_presentation,"prsnt_singleplayer_mission_results"),
        (finish_mission,0),
      ]),
    
      (1, 4, ti_once, [(main_hero_fallen),(neq,"$g_player_discovered",2),],
      [
        (finish_mission,0),
      ]),

    ],
  ),

   ("sp_campaign_austerlitz_1",mtf_battle_mode,-1,"Austerlitz 1",     #AUSTERLITZ Battle 1st part
    [
      #France - player and ally
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]), #Player Spawn
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troop Spawn
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]), #Companion Spawn
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Messenger 1 Spawn
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Messenger way point 1
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Reinforcements Spawn
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Player location if climbing in
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion location if climbing in
      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Messenger spawn at the end
      #Russia - enemy
      (9,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon ranker
      (10,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon officer
      (11,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon ranker
      (12,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (13,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (14,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (15,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (16,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (17,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (18,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Cannon Guard
      (19,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Line 1 Spawn
      (20,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (21,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (22,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (23,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (24,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (25,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (26,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (27,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (28,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (29,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (30,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (31,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (32,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (33,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (34,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (35,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (36,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (37,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (38,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (39,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (40,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (41,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (42,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (43,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (44,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (45,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Market Guard
      (46,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Wave 1 Spawn
      (47,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Wave 2 Spawn
      (48,mtef_visitor_source|mtef_team_1,0,0,1,[]), #Wave 3 Spawn
     ],
    [
    
    (ti_before_mission_start, 0, 0, [],
      [
        #Set up weather and daytime
        (scene_set_day_time,9),
        #(set_rain,1,0), #No more damn rain...
        #(set_fog_distance,150,0xEDE3D6),
        
        #Adding inital troops
        (modify_visitors_at_site,"scn_sp_sokolniz"),
        
        #French
        (add_visitors_to_current_scene,1,"trp_french_infantry2_ai",40),
        
        #Insert player companions here
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          (troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,2,":cur_companion",1),
        (try_end),
        
        #Allies
        #(add_visitors_to_current_scene,3,"trp_french_voltigeur_ai",4), #Small group of retreating light inf instead of messenger
        
        #Russians
        #Artillery
        (add_visitors_to_current_scene,9,"trp_russian_arty",1),
        (add_visitors_to_current_scene,10,"trp_russian_arty_officer",1),
        (add_visitors_to_current_scene,11,"trp_russian_arty",1),
        (try_for_range,":entry_no",12,19),
          (add_visitors_to_current_scene,":entry_no","trp_russian_infantry_ai",1),
        (try_end),
        #Line
        (add_visitors_to_current_scene,19,"trp_russian_infantry_ai",18),
        #Market Defenders
        (try_for_range,":entry_no",20,28),
          (add_visitors_to_current_scene,":entry_no","trp_russian_infantry_rifle_ai",1),
        (try_end),
        (try_for_range,":entry_no",28,46),
          (add_visitors_to_current_scene,":entry_no","trp_russian_infantry_ai",1),
        (try_end),
        
        (try_for_range,":value",0,20),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",20,40),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",40,60),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",60,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",80,100),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",100,120),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        
        #No order for Messenger, Artillery or Market Guards
        (troop_set_slot,"trp_custom_battle_dummy",104,mm_order_none),
        (troop_set_slot,"trp_custom_battle_dummy",111,mm_order_none),
        (troop_set_slot,"trp_custom_battle_dummy",112,mm_order_none),
        
        (try_for_range,":value",70,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",mm_order_fireatwill),
        (try_end),
        
        (call_script,"script_sp_common_before_mission_start"),
      
        #Mission specific variables
        (assign,"$g_ladder_used",0),
        
        (eq,"$g_ladder_used",0),  # remove warning :p

        (assign,"$g_battle_won",0),
        (assign, "$g_mission_state", 0),
        ## Mission states ##
        # 0 - Begin cut scene
        # 1 - Capture the Village
        # 2 - Reinforcements cut scene
        # 3 - Defend the village
        # 4 - End cut scene
        # 5 - Battle Won
      ]),
        
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         #(agent_get_troop_id, ":troop_id", ":agent_no"),         
         (agent_get_team,":agent_team",":agent_no"),
         #(troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         (assign,":initial_courage_score",3000), #Just give everyone the same for now
         
         (store_random_in_range, ":randomised_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomised_addition_courage"),
         (try_begin),
           (eq,":agent_team",0),
           (val_mul, ":initial_courage_score", "$g_global_morale_modifier"),
           (val_div, ":initial_courage_score", 10),
         (try_end),
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (try_begin),
           (eq,":entry_no",1),
           (agent_set_division,":agent_no",0), #Player bots
         (else_try),
           (eq,":entry_no",2),
           (agent_set_division,":agent_no",1), #Player companions
         (else_try),
           (eq,":entry_no",3),
           (agent_set_division,":agent_no",3), #Light Inf guys
         (else_try),
           (eq,":entry_no",5),
           (agent_set_division,":agent_no",2), #Reinforcements
         (else_try),
           (eq,":entry_no",8),
           (agent_set_division,":agent_no",4), #Messenger at end
         (else_try),
           (eq,":entry_no",19),
           (agent_set_division,":agent_no",0), #Line 1
         (else_try),
           (is_between,":entry_no",9,19),
           (agent_set_division,":agent_no",1), #Artillery guys
         (else_try),
           (is_between,":entry_no",20,46),
           (agent_set_division,":agent_no",2), #Market defenders
         (else_try),
           (eq,":entry_no",46),
           (agent_set_division,":agent_no",3), #Wave 1
         (else_try),
           (eq,":entry_no",47),
           (agent_set_division,":agent_no",4), #Wave 2
         (else_try),
           (eq,":entry_no",48),
           (agent_set_division,":agent_no",5), #Wave 3
         (try_end),
         
         (call_script, "script_correct_num_troops_in_formation", ":agent_no", 1), #Because I'm lazy ;D
         ]),
      		 
      (0, 0, ti_once, [],
        [
         (try_for_range,":unused",0,20),
          (init_position,pos1),
          (set_spawn_position,pos1),
          (spawn_scene_prop,"spr_formation_locator"),
          (scene_prop_set_visibility,reg0,0),
         (try_end),
         
         (entry_point_get_position,pos4,1),
         (scene_prop_get_instance,":instance","spr_formation_locator",0),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,2),
         (scene_prop_get_instance,":instance","spr_formation_locator",1),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,3),
         (scene_prop_get_instance,":instance","spr_formation_locator",3),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,5),
         (scene_prop_get_instance,":instance","spr_formation_locator",2),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,8),
         (scene_prop_get_instance,":instance","spr_formation_locator",4),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,19),
         (scene_prop_get_instance,":instance","spr_formation_locator",10),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,46),
         (scene_prop_get_instance,":instance","spr_formation_locator",13),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,47),
         (scene_prop_get_instance,":instance","spr_formation_locator",14),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,48),
         (scene_prop_get_instance,":instance","spr_formation_locator",15),
         (prop_instance_animate_to_position,":instance",pos4,0),
         
         (try_for_range,":formation_slot_no",40,42),
           (troop_set_slot,"trp_custom_battle_dummy",":formation_slot_no",mm_order_column),
         (try_end),
            
         ]),
         
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        (call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),
        
        (call_script, "script_sp_process_death_for_battle_results", ":dead_agent_no", ":killer_agent_no"),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),


      (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
       [
        (start_presentation,"prsnt_new_order_stuff"),
       ]),
  		 
      (0, 0, 1, [], #Volley fire
       [
        (call_script, "script_volley_fire"),
       ]),
       
      (0, 0, 1, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
         #(set_fog_distance,150,0xEDE3D6),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_2",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_2",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_3",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_3",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_4",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_4",0),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_pointer_arrow"),
         (assign,"$g_hold_position_arrow_instance",reg0),
         (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         
         
         (scene_prop_get_num_instances,":num_instances","spr_mm_sp_crate_explosive"),
         (try_for_range,":prop_no",0,":num_instances"),
           (scene_prop_get_instance,":prop_id","spr_mm_sp_crate_explosive",":prop_no"),
           (scene_prop_set_slot,":prop_id",scene_prop_slot_is_active,1),
         (try_end),
         ]),

      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",25),     
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
              
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      common_battle_order_panel,
      common_battle_order_panel_tick,
      
      common_battle_victory_display,
      
    ## Mission states ##
    # 0 - Begin cut scene
    # 1 - Capture the Village
    # 2 - Reinforcements cut scene
    # 3 - Defend the village
    # 4 - End cut scene
    # 5 - Battle Won
      
      (0, 0, ti_once, [ # Cut scene 1
      (eq, "$g_mission_state", 0),
      ],
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",500),
      ],
      [
        #Quickly deploy everyone via teleport to avoid problems
        (try_for_range,":team",0,2),
          (try_for_range,":division",0,9),
            (call_script,"script_deploy_division_via_teleport",":team",":division"),
          (try_end),
        (try_end),
        (start_presentation,"prsnt_singleplayer_cutscene_bars"),
        (entry_point_get_position,pos2,3),
        (position_move_z,pos2,1000),
        (position_move_y,pos2,100,0),
        (position_move_x,pos2,1500,0),
        (position_rotate_z,pos2,180),
        (mission_cam_set_position,pos2),
        (position_move_x,pos2,-3000,0),
        (mission_cam_animate_to_position,pos2,10000),
        (mission_cam_animate_to_screen_color, 0x00000000, 1500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",700),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_austerlitz_1_1"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",9000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",3),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",10000),
      ],
      [
        (mission_cam_set_mode, 0),
        (assign,"$g_show_cutscene_bars",0),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Capture the village of Sokolnitz from the Russians!"),
        (assign, "$g_mission_state", 1),
      ]),
      
      (1, 0, ti_once, [  # Checking Win Condition
      (eq, "$g_mission_state", 1),
      (assign,":enemy_defeated",1),
      (try_for_range,":division",0,8),
        (eq,":enemy_defeated",1),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (gt,":num_troops_in_division",0),
        (assign,":enemy_defeated",0),
      (try_end),
      (eq,":enemy_defeated",1),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"@You have captured the village, excellent work!"),
        (assign, "$g_mission_state", 5), # 7 - Battle Won
      ]),
        
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",510000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",3),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",510000),
      ],
      [
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (position_move_z,pos2,230),
        (position_move_y,pos2,-100,0),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",510500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_austerlitz_1_2"),
      ]),
      
      (0, 0, ti_once, [ # Cut scene 1 end
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",55500),
      ],
      [
        (mission_cam_set_mode, 0),
        (assign,"$g_show_cutscene_bars",0),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Fight back the Austrian counter-attack!"),
        (assign, "$g_mission_state", 1), # 6 - Defeat the Austrian counter attack
        (assign,"$g_hussars_spawned",0),
      ]),
        
      (0, 0, ti_once, [(eq, "$g_mission_state", 5),], 
      [
        (assign,"$g_battle_won",1),
      ]),
      
    (ti_tab_pressed, 0, 0, [],
      [
        (try_begin),
          (eq, "$g_mission_state", 5), #Battle won
          (val_add,"$g_finished_missions",1),
          (assign,"$g_finished_sub_missions",0),
          (finish_mission,0),
        (else_try),
          (question_box,"str_confirm_quit_mission"),
        (try_end),
      ]),
    (ti_question_answered, 0, 0, [],
      [
        (store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (start_presentation,"prsnt_singleplayer_mission_results"),
        (finish_mission,0),
      ]),
    
      (1, 4, ti_once, [(main_hero_fallen)],
      [
        (finish_mission,0),
      ]),
    ],
  ),
  
   ("sp_campaign_austerlitz_1_old",mtf_battle_mode,-1,"Austerlitz 1",     #AUSTERLITZ Battle 1st part
    [
      #France - player
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]), #Player Spawn
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troop Spawn
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion Spawn
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Reinforcements Spawn
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      #France - ally
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Messenger Spawn
      #Russia - enemy
      (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Defense Unit 1 Spawn
      (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Defense Unit 2 Spawn
      (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Defense Unit 3 Spawn
      (9,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave 1,3,5,7,9 Spawn
      (10,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave 2,4,6,8,10 Spawn
      (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave 1,3... Location
      (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave 2,4... Location
      
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Player Final Location
     ],
    [
    
    (ti_before_mission_start, 0, 0, [],
      [
        #Set up weather and daytime
        (scene_set_day_time,11),
        (set_rain,1,0),
        #(set_fog_distance,90,0xEDE3D6),
        
        #Adding inital troops
        (modify_visitors_at_site,"scn_sp_sokolniz"),
        
        #French
        (add_visitors_to_current_scene,1,"trp_french_infantry2_ai",35),
        #Insert player companions here
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          (troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,2,":cur_companion",1),
        (try_end),
        
        #Ally
        (add_visitors_to_current_scene,5,"trp_french_hussar_ai",1),
        
        #Russians
        (add_visitors_to_current_scene,6,"trp_russian_infantry_ai",25),
        (add_visitors_to_current_scene,7,"trp_russian_infantry_rifle_ai",20),
        (add_visitors_to_current_scene,8,"trp_russian_grenadier_ai",25),
        
        (try_for_range,":value",0,20),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",20,40),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",40,60),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",60,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",80,100),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",100,120),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
          
        (call_script,"script_sp_common_before_mission_start"),
      
        (assign,"$g_battle_won",0),
        (assign, "$g_mission_state", 0),
        ## Mission states ##
        # 0 - Begin cut scene
        # 1 - Capture Village
        # 2-3 - Defend the village against wave 1-2
        # 4 - Reinforcements cutscene
        # 5-7 - Defend the village against wave 3-5
        # 8 - Reinforcments cutscene
        # 9-11 - Defend the village against wave 6-8
        # 12 - Reinforcments cutscene
        # 13-14 - Defend the village against wave 9-10
        # 15 - Cut scene
        # 16 - Ride away
        # 17 - Battle won
      ]),
        
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         #(agent_get_troop_id, ":troop_id", ":agent_no"),         
         (agent_get_team,":agent_team",":agent_no"),
         #(troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         (assign,":initial_courage_score",3000), #Just give everyone the same for now
         
         (store_random_in_range, ":randomised_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomised_addition_courage"),
         (try_begin),
           (eq,":agent_team",0),
           (val_mul, ":initial_courage_score", "$g_global_morale_modifier"),
           (val_div, ":initial_courage_score", 10),
         (try_end),
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (try_begin),
           (eq,":entry_no",1),
           (agent_set_division,":agent_no",0), #Player bots
         (else_try),
           (eq,":entry_no",2),
           (agent_set_division,":agent_no",1), #Player companions
         (else_try),
           (eq,":entry_no",3),
           (agent_get_troop_id,":troop_id",":agent_no"),
           (try_begin),
             (eq,":troop_id","trp_french_infantry_ai"),
             (agent_set_division,":agent_no",2), #Player reinforcements
           (else_try),
             (eq,":troop_id","trp_french_voltigeur_ai"),
             (agent_set_division,":agent_no",3), #Player reinforcements
           (else_try),
             (eq,":troop_id","trp_french_infantry2_ai"),
             (agent_set_division,":agent_no",4), #Player reinforcements
           (else_try),
             (agent_set_division,":agent_no",6), #Messenger2
             (assign,"$g_messenger_agent_2",":agent_no"),
           (try_end),
         (else_try),
           (eq,":entry_no",5),
           (agent_set_division,":agent_no",5), #Messenger
           (assign,"$g_messenger_agent_1",":agent_no"),
         (else_try),
           (eq,":entry_no",6),
           (agent_set_division,":agent_no",0), #Defensive unit 1
         (else_try),
           (eq,":entry_no",7),
           (agent_set_division,":agent_no",1), #Defensive unit 2
         (else_try),
           (eq,":entry_no",8),
           (agent_set_division,":agent_no",2), #Defensive unit 3
         (else_try),
           (eq,":entry_no",9),
           (agent_set_division,":agent_no",3), #Odd Waves
         (else_try),
           (eq,":entry_no",10),
           (agent_set_division,":agent_no",4), #Even Waves
         (try_end),
         
         (try_begin),
           (agent_get_team,":team_no",":agent_no"),
           (eq,":team_no",1),
           (agent_set_speed_limit,":agent_no",5),
         (try_end),
         
         (call_script, "script_correct_num_troops_in_formation", ":agent_no", 1), #Because I'm lazy ;D
         ]),
      		 
      (0, 0, ti_once, [],
        [
         (try_for_range,":unused",0,20),
          (init_position,pos1),
          (set_spawn_position,pos1),
          (spawn_scene_prop,"spr_formation_locator"),
          (scene_prop_set_visibility,reg0,0),
         (try_end),
         
         (entry_point_get_position,pos4,1),
         (scene_prop_get_instance,":instance","spr_formation_locator",0),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,2),
         (scene_prop_get_instance,":instance","spr_formation_locator",1),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,3),
         (scene_prop_get_instance,":instance","spr_formation_locator",2),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,5),
         (scene_prop_get_instance,":instance","spr_formation_locator",5),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,6),
         (scene_prop_get_instance,":instance","spr_formation_locator",10),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,7),
         (scene_prop_get_instance,":instance","spr_formation_locator",11),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,8),
         (scene_prop_get_instance,":instance","spr_formation_locator",12),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,9),
         (scene_prop_get_instance,":instance","spr_formation_locator",13),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,10),
         (scene_prop_get_instance,":instance","spr_formation_locator",14),
         (prop_instance_animate_to_position,":instance",pos4,0),
         
         (troop_set_slot,"trp_custom_battle_dummy",51,mm_order_skirmish),
            
         ]),
         
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        (call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),
        
        (call_script, "script_sp_process_death_for_battle_results", ":dead_agent_no", ":killer_agent_no"),
        
        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),


      (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
       [
        (start_presentation,"prsnt_new_order_stuff"),
       ]),
  		 
      (0, 0, 1, [], #Volley fire
       [
        (call_script, "script_volley_fire"),
       ]),
       
      (0, 0, 1, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
         #(set_fog_distance,90,0xEDE3D6), #Fog needs setting after mission start
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_2",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_2",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_3",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_3",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_4",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_4",0),
        
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_pointer_arrow"),
         (assign,"$g_hold_position_arrow_instance",reg0),
         (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         ]),

      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
            (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",25),          
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      common_battle_order_panel,
      common_battle_order_panel_tick,
      
    common_battle_victory_display,
      
      (0, 0, 5, [],  #Bots fire when enemy close
      [
        (try_for_range,":division",0,5),
          (store_add,":division_slot",70,":division"),
          (neg|troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",8000),
          (lt,":min_dist",3000),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
        (try_end),
        (try_for_range,":division",0,5),
          (store_add,":division_slot",110,":division"),
          (troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_hold),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",1000),
          (lt,":min_dist",300),
          (team_give_order,1,":division",mordr_charge),
          (try_for_agents,":cur_agent"),
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",1),
            (agent_get_division,":agent_div",":cur_agent"),
            (eq,":agent_div",":division"), 
            (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
            #Cancel scripted destination for charge:
            (agent_clear_scripted_mode,":cur_agent"),
          (try_end),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_charge),
        (try_end),
      ]),
      
      ## Mission states ##
      # 0 - Begin cut scene
      # 1 - Capture Village
      # 2-3 - Defend the village against wave 1-2
      # 4 - Reinforcements cutscene
      # 5-7 - Defend the village against wave 3-5
      # 8 - Reinforcments cutscene
      # 9-11 - Defend the village against wave 6-8
      # 12 - Reinforcments cutscene
      # 13-14 - Defend the village against wave 9-10
      # 15 - Cut scene
      # 16 - Ride away
      # 17 - Battle won
        
      (0, 0, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 3000),
        (entry_point_get_position,pos2,1),
        (position_move_z,pos2,1000),
        (position_move_x,pos2,4000),
        (position_move_y,pos2,8000),
        (mission_cam_set_position,pos2),
        (entry_point_get_position,pos2,1),
        (position_move_z,pos2,1500),
        (position_move_x,pos2,-8000),
        (position_move_y,pos2,10000),
        (position_rotate_z,pos2,-20),
        (mission_cam_animate_to_position,pos2,15000),
        (assign,"$g_cutscene_state",0),
      ]),
      
      (0, 0.1, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_austerlitz_1_1"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",13000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 2000),
        (tutorial_message,-1),
      ]),

      (0, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",13000),],  #Move messenger to player
      [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position,pos4,":player_agent"),
        (position_move_x,pos4,200),
        (scene_prop_get_instance,":instance","spr_formation_locator",5),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",15000),
      ],
      [
        (entry_point_get_position,pos2,0),
        (position_move_z,pos2,300),
        (position_move_y,pos2,-200),
        (position_rotate_z,pos2,60),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",15200),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_austerlitz_1_2"),
      ]),
      
      (0, 0, ti_once, [
        (eq, "$g_mission_state", 0),
        (store_mission_timer_a_msec,":mt"),
        (gt,":mt",15000),
        (agent_get_position,pos4,"$g_messenger_agent_1"),
        (scene_prop_get_instance,":instance","spr_formation_locator",5),
        (prop_instance_get_position,pos5,":instance"),
        (get_distance_between_positions,":dist",pos4,pos5),
        (lt,":dist",300),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_austerlitz_1_3"),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
        (assign,"$g_cutscene_state",1),
      ]),
             
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (eq,"$g_cutscene_state",1),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",16000),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",4000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
        (store_add,":division_slot",100,5),
        (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_retreat), #Remove the messenger from the map
        (agent_start_running_away,"$g_messenger_agent_1"),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (eq,"$g_cutscene_state",1),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",16000),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5000),
      ],
      [
        (mission_cam_set_mode, 0),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (assign, "$g_mission_state", 1),# 1 - Capture Village
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Capture the village of Sokolnitz from the Russian Army"),
        (assign, "$g_projection_state", 3),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
      ]),
      
      (0, 0, 0, [(eq, "$g_mission_state", 1),], 
      [
        (assign,":num_defenders",0),
        (try_for_range,":division",0,3),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_defenders",1),
          (try_begin),
            (eq,":num_defenders",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (else_try),
            (eq,":num_defenders",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos0,0), #Follow attckers with target locator
          (else_try),
            (eq,":num_defenders",3),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_3",pos0,0), #Follow attckers with target locator
          (try_end),
        (try_end),
        (assign,"$g_projection_state",":num_defenders"),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 1),
      (assign,":continue",1),
      (assign,":defenders_gone",0),
      (try_for_range,":division",0,3),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (try_begin),
          (gt,":num_troops_in_division",0),
          (assign,":continue",0),
        (else_try),
          (val_add,":defenders_gone",1),
        (try_end),
      (try_end),
      #(assign,"$g_singleplayer_progress_counter_cur_value",":squares_gone"),
      (eq,":continue",1),
      ], 
      [
        (assign, "$g_mission_state", 2), # 2 - Defend the village against wave 1
        (assign, "$g_wave_location",1),
        (add_visitors_to_current_scene,9,"trp_russian_infantry_ai",20),
        (entry_point_get_position,pos4,9),
        (scene_prop_get_instance,":instance","spr_formation_locator",13),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,10),
        (scene_prop_get_instance,":instance","spr_formation_locator",14),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (assign,"$g_wave_move",1),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Hold the village at all costs against the Russian counter-attacks."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",10),
        (assign,"$g_singleplayer_progress_counter_string_id","str_austerlitz_1_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 2),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
      ]),
          
      (0, 0, 0, [(is_between, "$g_mission_state", 2,15),], 
      [
        (assign,":num_defenders",0),
        (try_for_range,":division",3,5),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_defenders",1),
          (try_begin),
            (eq,":num_defenders",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (else_try),
            (eq,":num_defenders",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos0,0), #Follow attckers with target locator
          (try_end),
        (try_end),
        (try_begin),
          (eq,":num_defenders",0),
          (assign,":num_defenders",1),
        (try_end),
          (assign,"$g_projection_state",":num_defenders"),
      ]),
      
      (5, 0, 3, [
        (eq,"$g_wave_move",1),
      ], 
      [
        (entry_point_get_position,pos4,11),
        (scene_prop_get_instance,":instance","spr_formation_locator",13),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,12),
        (scene_prop_get_instance,":instance","spr_formation_locator",14),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (assign,"$g_wave_move",0),
      ]),
      
      (3, 0, 0, [
      (is_between, "$g_mission_state", 2,15),
      (neq,"$g_mission_state",7),
      (neq,"$g_mission_state",10),
      (neq,"$g_mission_state",13),
      (try_begin),
        (eq, "$g_wave_location",1),
        (assign,":division",3),
      (else_try),
        (assign,":division",4),
      (try_end),
      (store_add,":division_slot",30,":division"),
      (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
      (le,":num_troops_in_division",0),
      ], 
      [
        (val_add, "$g_singleplayer_progress_counter_cur_value", 1),
        (val_add, "$g_mission_state", 1),
        (entry_point_get_position,pos4,9),
        (scene_prop_get_instance,":instance","spr_formation_locator",13),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (entry_point_get_position,pos4,10),
        (scene_prop_get_instance,":instance","spr_formation_locator",14),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (assign,"$g_wave_move",1),
        (try_begin),
          (eq, "$g_wave_location",1),
          (assign, "$g_wave_location",0),
          (assign, ":entry_no", 10),
        (else_try),
          (assign, "$g_wave_location",1),
          (assign, ":entry_no", 9),
        (try_end),
        (try_begin),
          (this_or_next|eq, "$g_mission_state", 3),
          (this_or_next|eq, "$g_mission_state", 6),
          (this_or_next|eq, "$g_mission_state", 9),
          (eq, "$g_mission_state", 10),
          (add_visitors_to_current_scene,":entry_no","trp_russian_infantry_ai",20),
        (else_try),
          (this_or_next|eq, "$g_mission_state", 5),
          (this_or_next|eq, "$g_mission_state", 7),
          (eq, "$g_mission_state", 13),
          (add_visitors_to_current_scene,":entry_no","trp_russian_infantry_ai",25),
        (else_try),
          (this_or_next|eq, "$g_mission_state", 4),
          (eq, "$g_mission_state", 12),
          (add_visitors_to_current_scene,":entry_no","trp_russian_foot_guard_ai",25),
        (else_try),
          (eq, "$g_mission_state", 15), # 15 - Cut scene
          (tutorial_message,-1),
          (assign, "$g_singleplayer_progress_counter_mode", -1),
          (assign, "$g_projection_state", 0),
          (add_visitors_to_current_scene,3,"trp_french_hussar_ai",1),
        (try_end),
      ]),
      
      (0, 0, 0, [
          (this_or_next|eq, "$g_mission_state", 7),
          (this_or_next|eq, "$g_mission_state", 10),
          (eq, "$g_mission_state", 13),
          ],
      [
        (try_begin),
          (eq, "$g_mission_state", 7),
          (assign,":troop_id","trp_french_infantry_ai"),
          (assign,":amount",30),
          (assign,":division",2),
        (else_try),
          (eq, "$g_mission_state", 10),
          (assign,":troop_id","trp_french_voltigeur_ai"),
          (assign,":amount",20),
          (assign,":division",3),
        (else_try),
          (eq, "$g_mission_state", 13),
          (assign,":troop_id","trp_french_infantry2_ai"),
          (assign,":amount",30),
          (assign,":division",4),
        (try_end),
        (add_visitors_to_current_scene,3,":troop_id",":amount"), #Spawn reinforcements
        (val_add,"$g_mission_state",1),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",":division"),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (1, 0, ti_once, [(eq, "$g_mission_state", 15),],  #Move messenger to player
      [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position,pos4,":player_agent"),
        (position_move_x,pos4,200),
        (scene_prop_get_instance,":instance","spr_formation_locator",6),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [
        (eq, "$g_mission_state", 15),
        (agent_get_position,pos4,"$g_messenger_agent_2"),
        (scene_prop_get_instance,":instance","spr_formation_locator",6),
        (prop_instance_get_position,pos5,":instance"),
        (get_distance_between_positions,":dist",pos4,pos5),
        (lt,":dist",300),
      ],  #Skip dialouge for now - Need proper trigger later
      [
        (assign, "$g_mission_state", 16),# 16 - Ride away
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Go to meet the Emperor"),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (entry_point_get_position,pos5,13),
        (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos5,0), #Set target locator
        (store_add,":division_slot",100,6),
        (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_retreat), #Remove the messenger from the map
        (agent_start_running_away,"$g_messenger_agent_2"),
      ]),
      
      (1, 0, ti_once, [
        (eq, "$g_mission_state", 16),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos4,":player_agent"),
        (entry_point_get_position,pos5,13),
        (get_distance_between_positions,":dist",pos4,pos5),
        (lt,":dist",200),
      ], 
      [
        (assign, "$g_mission_state", 17), # 17 - Battle Won
        (tutorial_message,-1),
        (assign, "$g_projection_state", 0),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 17),], 
      [
        (assign,"$g_battle_won",1),
      ]),
      
    (ti_tab_pressed, 0, 0, [],
      [
        (try_begin),
          (eq, "$g_mission_state", 17), #Battle won 
          (val_add,"$g_finished_missions",1),
          (assign,"$g_finished_sub_missions",0),
          #(val_add,"$g_finished_sub_missions",1),
          (finish_mission,0),
        (else_try),
          (question_box,"str_confirm_quit_mission"),
        (try_end),
      ]),
    (ti_question_answered, 0, 0, [],
      [
        (store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
      ]),
    
      (1, 4, ti_once, [(main_hero_fallen),],
      [
        (finish_mission,0),
      ]),
    
    ],
  ),

  
   ("sp_campaign_dresden_1",mtf_battle_mode,-1,"Dresden 1",     #DRESDEN Battle 1st part
    [
      #France - player
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]), #Player Spawn
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troop Spawn
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion Spawn
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Ally spawn
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Ally location
      #Russia - enemy
      (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wall unit 1
      (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wall unit 2
      (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave spawn
      (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Wave Location
      (9,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #"Random" attackers spawn
     ],
    [
    
    (ti_before_mission_start, 0, 0, [],
      [
        #Set up weather and daytime
        (scene_set_day_time,15),
        (set_rain,1,60),
        #(set_fog_distance,100,0xFFFFFF),
        
        #Adding inital troops
        (modify_visitors_at_site,"scn_sp_dresden1"),
        
        #French
        (add_visitors_to_current_scene,1,"trp_french_infantry_ai",30),
        #Insert player companions here 
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          (troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,2,":cur_companion",1),
        (try_end),
        
        #French Allies
        (add_visitors_to_current_scene,3,"trp_french_infantry2_ai",25,2),
        
        #Russians
        (add_visitors_to_current_scene,5,"trp_russian_grenadier_ai",15),
        (add_visitors_to_current_scene,6,"trp_russian_grenadier_ai",15),
        
        (try_for_range,":value",0,20),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",20,40),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",40,60),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",60,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",80,100),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",100,120),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
      
        (call_script,"script_sp_common_before_mission_start"),
      
        (assign,"$g_battle_won",0),
        (assign, "$g_mission_state", 0),
        ## Mission states ##
        # 0 - Begin cut scene
        # 1 - Defeat Russians on Walls
        # 2 - Cut scene 2
        # 3 - Help your allies
        # 4 - Cut scene 3
        # 5-8 - Waves 1-4
        # 9 - Reinforcments Cut scene
        # 10 - Wave 5
        # 11 - Attack remaining Russians
        # 12 - Battle Won
      ]),
        
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         #(agent_get_troop_id, ":troop_id", ":agent_no"),         
         (agent_get_team,":agent_team",":agent_no"),
         #(troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         (assign,":initial_courage_score",3000), #Just give everyone the same for now
         
         (store_random_in_range, ":randomised_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomised_addition_courage"),
         (try_begin),
           (eq,":agent_team",0),
           (val_mul, ":initial_courage_score", "$g_global_morale_modifier"),
           (val_div, ":initial_courage_score", 10),
         (try_end),
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (try_begin),
           (eq,":entry_no",1),
           (agent_set_division,":agent_no",0), #Player bots
         (else_try),
           (eq,":entry_no",2),
           (agent_set_division,":agent_no",1), #Player companions
         (else_try),
           (eq,":entry_no",3),
           (agent_get_troop_id,":troop_id",":agent_no"),
           (try_begin),
            (eq,":troop_id","trp_french_infantry2_ai"),
            (agent_set_division,":agent_no",2), #Allied troops
           (else_try),
            (agent_set_division,":agent_no",3), #Reinforcements
           (try_end),
         (else_try),
           (eq,":entry_no",5),
           (agent_set_division,":agent_no",0), #Wall unit 1
         (else_try),
           (eq,":entry_no",6),
           (agent_set_division,":agent_no",1), #Wall unit 2
         (else_try),
           (eq,":entry_no",7),
           (agent_set_division,":agent_no",2), #Wave spawn
         (else_try),
           (eq,":entry_no",9),
           (agent_set_division,":agent_no",3), #Random guys
         (try_end),
         
         (try_begin),
           (agent_get_team,":team_no",":agent_no"),
           (eq,":team_no",1),
           (agent_set_speed_limit,":agent_no",5),
         (try_end),
         
         (call_script, "script_correct_num_troops_in_formation", ":agent_no", 1), #Because I'm lazy ;D
         ]),
      		 
      (0, 0, ti_once, [],
        [
         (try_for_range,":unused",0,20),
          (init_position,pos1),
          (set_spawn_position,pos1),
          (spawn_scene_prop,"spr_formation_locator"),
          (scene_prop_set_visibility,reg0,0),
         (try_end),
         
         (entry_point_get_position,pos4,1),
         (scene_prop_get_instance,":instance","spr_formation_locator",0),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,2),
         (scene_prop_get_instance,":instance","spr_formation_locator",1),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,3),
         (scene_prop_get_instance,":instance","spr_formation_locator",2),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,5),
         (scene_prop_get_instance,":instance","spr_formation_locator",10),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,6),
         (scene_prop_get_instance,":instance","spr_formation_locator",11),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,7),
         (scene_prop_get_instance,":instance","spr_formation_locator",12),
         (prop_instance_animate_to_position,":instance",pos4,0),
            
         ]),
         
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        (call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),
        
        (call_script, "script_sp_process_death_for_battle_results", ":dead_agent_no", ":killer_agent_no"),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),


      (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
       [
        (start_presentation,"prsnt_new_order_stuff"),
       ]),
  		 
      (0, 0, 1, [], #Volley fire
       [
        (call_script, "script_volley_fire"),
       ]),
       
      (0, 0, 1, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
         #(set_fog_distance,100,0xFFFFFF), #Fog needs setting after mission start
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_2",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_2",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_3",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_3",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_4",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_4",0),
        
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_pointer_arrow"),
         (assign,"$g_hold_position_arrow_instance",reg0),
         (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         ]),

      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
            (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",25),          
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      common_battle_order_panel,
      common_battle_order_panel_tick,
      
    common_battle_victory_display,
      
      (0, 0, 5, [],  #Bots fire when enemy close
      [
        (try_for_range,":division",0,3),
          (store_add,":division_slot",70,":division"),
          (neg|troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",8000),
          (lt,":min_dist",3000),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
        (try_end),
        (try_for_range,":division",0,4),
          (store_add,":division_slot",110,":division"),
          (troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_hold),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",1000),
          (lt,":min_dist",300),
          (team_give_order,1,":division",mordr_charge),
          (try_for_agents,":cur_agent"),
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",1),
            (agent_get_division,":agent_div",":cur_agent"),
            (eq,":agent_div",":division"), 
            (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
            #Cancel scripted destination for charge:
            (agent_clear_scripted_mode,":cur_agent"),
          (try_end),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_charge),
        (try_end),
      ]),
      
      ## Mission states ##
      # 0 - Begin cut scene
      # 1 - Defeat Russians on Walls
      # 2 - Cut scene 2
      # 3 - Help your allies
      # 4 - Cut scene 3
      # 5-8 - Waves 1-4
      # 9 - Reinforcments Cut scene
      # 10 - Wave 5
      # 11 - Attack remaining Russians
      # 12 - Battle Won
        
      (0, 0, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 8000),
        (entry_point_get_position,pos2,1),
        (position_move_z,pos2,1000),
        (position_move_y,pos2,100),
        (position_rotate_z,pos2,90),
        (mission_cam_set_position,pos2),
        (entry_point_get_position,pos2,5),
        (position_move_z,pos2,1500),
        (position_rotate_z,pos2,150),
        (position_move_y,pos2,300),
        (mission_cam_animate_to_position,pos2,25000),
      ]),
      
      (0, 0.1, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_1_1"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",12000),
      ],
      [
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",12500),
      ],
      [
        (tutorial_message,"str_cutscene_dresden_1_2"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",23500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1500),
        (tutorial_message,-1),
      ]),
      
      (5, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",25000),
      ],  #Skip cutscenes for now
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",2),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Recapture the city walls from the Russians."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",30),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_1_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 2),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (assign, "$g_mission_state", 1),# 1 - Defeat Russians on Walls
      ]),
      
      (0, 0, 0, [(eq, "$g_mission_state", 1),], 
      [
        (assign,":num_attackers",0),
        (try_for_range,":division",0,2),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_attackers",1),
          (try_begin),
            (eq,":num_attackers",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (else_try),
            (eq,":num_attackers",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos0,0), #Follow attckers with target locator
          (try_end),
        (try_end),
        (assign,"$g_projection_state",":num_attackers"),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 1),
      (assign,":total_troops",0),
      (try_for_range,":division",0,2),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (val_add,":total_troops",":num_troops_in_division"),
      (try_end),
      (store_sub,":troops_defeated",30,":total_troops"),
      (assign,"$g_singleplayer_progress_counter_cur_value",":troops_defeated"),
      (le,":total_troops",0),
      ], 
      [
        (assign, "$g_mission_state", 2), # 2 - Cut scene 2
        (assign, "$g_singleplayer_progress_counter_mode", -1),
        (assign,"$g_projection_state",0),
        (add_visitors_to_current_scene,9,"trp_russian_infantry_ai",40),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",13),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (troop_set_slot,"trp_custom_battle_dummy",102,mm_order_charge),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 2),],  #Cutscene 2
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (entry_point_get_position,pos2,4),
        (position_move_y,pos2,2000),
        (position_rotate_z,pos2,90),
        (position_move_z,pos2,1500),
        (position_move_y,pos2,-5000),
        (mission_cam_set_position,pos2),
        (position_move_z,pos2,-1000),
        (position_move_y,pos2,3000),
        (mission_cam_animate_to_position,pos2,5000),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 2),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",250),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_1_3"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 2),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",4500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
      ]),
      
      (5, 0, ti_once, [
      (eq, "$g_mission_state", 2),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5550),
      ],
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Help your allies drive back the Russians."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",40),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_1_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (assign, "$g_mission_state", 3),# 3 - Help your allies
      ]),
      
      (0, 0, 0, [(eq, "$g_mission_state", 3),], 
      [
        (assign,":num_attackers",0),
        (try_for_range,":division",3,4),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_attackers",1),
          (try_begin),
            (eq,":num_attackers",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (try_end),
        (try_end),
        (assign,"$g_projection_state",":num_attackers"),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 3),
      (assign,":total_troops",0),
      (try_for_range,":division",3,4),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (val_add,":total_troops",":num_troops_in_division"),
      (try_end),
      (store_sub,":troops_defeated",40,":total_troops"),
      (assign,"$g_singleplayer_progress_counter_cur_value",":troops_defeated"),
      (le,":total_troops",0),
      ], 
      [
        (assign, "$g_mission_state", 4), # 4 - Cut scene 3
        (add_visitors_to_current_scene,7,"trp_russian_infantry_ai",20),
        
        (try_for_agents,":cur_agent"),     #Put allies under player command from this point
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",2),
            (agent_set_team,":cur_agent",0),
        (try_end),
        
        (assign,"$g_projection_state",0),
        (assign, "$g_singleplayer_progress_counter_mode", -1),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 4),],  #Cutscene 3
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (entry_point_get_position,pos2,9),
        #(entry_point_get_position,pos3,7),
        #(get_angle_between_positions,":rotation",pos2,pos3),
        (position_rotate_z,pos2,180),
        (position_move_z,pos2,1500),
        (position_move_y,pos2,5000),
        (mission_cam_set_position,pos2),
        (position_move_z,pos2,-1000),
        (position_move_y,pos2,3000),
        (mission_cam_animate_to_position,pos2,7000),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 3
      (eq, "$g_mission_state", 4),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",250),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_1_4"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 3
      (eq, "$g_mission_state", 4),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
      ]),
      
      (5, 0, ti_once, [
      (eq, "$g_mission_state", 4),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",6500),],
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Defend the gate against Russian attacks."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",5),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_1_2"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (assign,"$g_wave_move",1),
        (assign, "$g_mission_state", 5), # 5-8 - Waves 1-4
      ]),
      
      (0, 0, 0, [(is_between, "$g_mission_state", 5,9),], 
      [
        (assign,":num_attackers",0),
        (try_for_range,":division",2,3),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_attackers",1),
          (try_begin),
            (eq,":num_attackers",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (try_end),
        (try_end),
      ]),
      
      (5, 0, 3, [
        (eq,"$g_wave_move",1),
      ], 
      [
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",12),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (assign,"$g_wave_move",0),
        (troop_set_slot,"trp_custom_battle_dummy",112,mm_order_hold),
        (troop_set_slot,"trp_custom_battle_dummy",72,mm_order_holdfire),
      ]),
      
      (3, 0, 2, [
      (is_between, "$g_mission_state", 5,11),
      (neq,"$g_mission_state",9),
      (store_add,":division_slot",30,2),
      (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
      (le,":num_troops_in_division",0),
      ], 
      [
        (val_add, "$g_singleplayer_progress_counter_cur_value", 1),
        (val_add, "$g_mission_state", 1),
        (entry_point_get_position,pos4,7),
        (scene_prop_get_instance,":instance","spr_formation_locator",12),
        (prop_instance_animate_to_position,":instance",pos4,0),
        (assign,"$g_wave_move",1),
        (try_begin),
          (eq, "$g_mission_state", 6),
          (add_visitors_to_current_scene,7,"trp_russian_infantry_ai",20),
        (else_try),
          (this_or_next|eq, "$g_mission_state", 7),
          (eq, "$g_mission_state", 8),
          (add_visitors_to_current_scene,7,"trp_russian_infantry_ai",25),
        (else_try),
          (eq, "$g_mission_state", 9),
          (add_visitors_to_current_scene,7,"trp_russian_foot_guard_ai",30),
        (else_try),
          (eq, "$g_mission_state", 11), # 11 - Attack remaining Russians
          (tutorial_message,-1),
          (assign, "$g_singleplayer_progress_counter_mode", -1),
          (assign,"$g_projection_state",0),
          (assign,"$g_wave_move",0),
          (add_visitors_to_current_scene,7,"trp_russian_infantry_ai",40),
        (try_end),
      ]),
      
      (0, 0, ti_once, [
          (eq, "$g_mission_state", 9),
          ],
      [
        (add_visitors_to_current_scene,3,"trp_french_infantry_ai",30), #Spawn reinforcements
        #(val_add,"$g_mission_state",1),
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",3),
        (prop_instance_animate_to_position,":instance",pos4,0),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 9),],  #Cutscene 4
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (entry_point_get_position,pos2,3),
        (position_move_y,pos2,5000),
        (position_rotate_z,pos2,180),
        (position_move_z,pos2,1500),
        (mission_cam_set_position,pos2),
        (position_move_z,pos2,-1000),
        (position_move_y,pos2,2000),
        (mission_cam_animate_to_position,pos2,5000),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 4
      (eq, "$g_mission_state", 9),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",250),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_1_5"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 4
      (eq, "$g_mission_state", 9),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",4500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 4
      (eq, "$g_mission_state", 9),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (assign,"$g_mission_state",10),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Defend the gate against Russian attacks."),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 11),],  #Cutscene 5
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        #(entry_point_get_position,pos3,7),
        #(get_angle_between_positions,":rotation",pos2,pos3),
        (position_rotate_z,pos2,180),
        (position_move_z,pos2,1500),
        (position_move_y,pos2,5000),
        (mission_cam_set_position,pos2),
        (position_move_z,pos2,-1000),
        (position_move_y,pos2,3000),
        (mission_cam_animate_to_position,pos2,7000),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 5
      (eq, "$g_mission_state", 11),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",250),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_1_6"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 5
      (eq, "$g_mission_state", 11),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",5800),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [  #Attack Russians order
      (eq, "$g_mission_state", 11),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",7000),
      ],
      [
        (mission_cam_animate_to_screen_color, 0x00000000, 1000),
        (mission_cam_set_mode, 0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Sally out and rout the remaining Russians."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",50),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_1_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
      ]),
      
      (0, 0, 0, [(is_between, "$g_mission_state", 5,12),], 
      [
        (assign,":num_attackers",0),
        (try_for_range,":division",2,3),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_attackers",1),
          (try_begin),
            (eq,":num_attackers",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow attackers with target locator
          (try_end),
        (try_end),
        (try_begin),
          (le,":num_attackers",0),
          (assign,":num_attackers",1),
        (try_end),
        (assign,"$g_projection_state",":num_attackers"),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 11),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",7000),
      (assign,":total_troops",0),
      (try_for_range,":division",2,3),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (val_add,":total_troops",":num_troops_in_division"),
      (try_end),
      (store_sub,":troops_defeated",40,":total_troops"),
      (assign,"$g_singleplayer_progress_counter_cur_value",":troops_defeated"),
      (le,":total_troops",0),
      ], 
      [
        (assign, "$g_mission_state", 12), # 12 - Battle Won
        (assign, "$g_singleplayer_progress_counter_mode", -1),
        (assign, "$g_projection_state", 0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@The assault has been broken! Vive la France!"),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 12),], 
      [
        (assign,"$g_battle_won",1),
      ]),
      
    (ti_tab_pressed, 0, 0, [],
      [
        (try_begin),
          (eq, "$g_mission_state", 12), #Battle won
          (val_add,"$g_finished_sub_missions",1),
          (finish_mission,0),
        (else_try),
          (question_box,"str_confirm_quit_mission"),
        (try_end),
      ]),
    (ti_question_answered, 0, 0, [],
      [
        (store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
      ]),
    
      (1, 4, ti_once, [(main_hero_fallen),],
      [
        (finish_mission,0),
      ]),
    
    ],
  ),

  
   ("sp_campaign_dresden_2",mtf_battle_mode,-1,"Dresden 2",     #DRESDEN Battle 2nd part
    [
      #France - player
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Player Spawn
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Troop Spawn
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Companion Spawn
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Reinforcements Spawn
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]), #Mission Help Spawn
      #Austria - enemy
      (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Commander Spawn
      (7,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Square 1 Spawn
      (9,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Square 2 Spawn
      (10,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Square 3 Spawn
      (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Square 4 Spawn
      (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 1 Spawn
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]), #Line 2 Spawn
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
    
    (ti_before_mission_start, 0, 0, [],
      [
        #Set up weather and daytime
        (scene_set_day_time,18),
        (set_rain,1,60),
        #(set_fog_distance,150,0xEDE3D6),
        
        #Adding inital troops
        (modify_visitors_at_site,"scn_sp_dresden2"),
        
        #French
        (add_visitors_to_current_scene,1,"trp_french_dragoon_ai",30),
        
        #Insert player companions here
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          (troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,2,":cur_companion",1),
        (try_end),
        
        #Austrians (currently Russians...)
        (add_visitors_to_current_scene,6,"trp_russian_infantry_officer",1),
        (add_visitors_to_current_scene,8,"trp_russian_infantry_ai",20),
        (add_visitors_to_current_scene,9,"trp_russian_infantry_ai",20),
        (add_visitors_to_current_scene,10,"trp_russian_infantry_ai",20),
        (add_visitors_to_current_scene,11,"trp_russian_infantry_ai",20),
        
        (try_for_range,":value",0,20),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",20,40),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",40,60),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",60,80),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",80,100),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
        (try_for_range,":value",100,120),
          (troop_set_slot,"trp_custom_battle_dummy",":value",0),
        (try_end),
      
        (call_script,"script_sp_common_before_mission_start"),
      
        (assign,"$g_battle_won",0),
        (assign, "$g_mission_state", 0),
        ## Mission states ##
        # 0 - Begin cut scene
        # 1 - Catch commander
        # 2 - Break Squares
        # 3 - Cut scene 2
        # 4 - Attack lines
        # 5 - Battle Won
      ]),
        
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":entry_no"),
         
         (agent_is_human,":agent_no"),
         (agent_is_non_player,":agent_no"),
         #(agent_get_troop_id, ":troop_id", ":agent_no"),         
         (agent_get_team,":agent_team",":agent_no"),
         #(troop_get_slot,":initial_courage_score",":troop_id",slot_troop_initial_morale),
         (assign,":initial_courage_score",3000), #Just give everyone the same for now
         
         (store_random_in_range, ":randomised_addition_courage", 0, 1000), #average : 500
         (val_add, ":initial_courage_score", ":randomised_addition_courage"),
         (try_begin),
           (eq,":agent_team",0),
           (val_mul, ":initial_courage_score", "$g_global_morale_modifier"),
           (val_div, ":initial_courage_score", 10),
         (try_end),
         
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         (agent_set_slot, ":agent_no", slot_agent_is_running_away, 0),
         
         (try_begin),
           (eq,":entry_no",1),
           (agent_set_division,":agent_no",0), #Player bots
         (else_try),
           (eq,":entry_no",2),
           (agent_set_division,":agent_no",1), #Player companions
         (else_try),
           (eq,":entry_no",3),
           (agent_set_division,":agent_no",2), #Player reinforcements
         (else_try),
           (eq,":entry_no",5),
           (agent_set_division,":agent_no",3), #Mission help
         (else_try),
           (eq,":entry_no",6),
           (agent_set_division,":agent_no",0), #Enemy Commander
           (assign,"$g_enemy_commander_agent_1",":agent_no"),
         (else_try),
           (eq,":entry_no",8),
           (agent_set_division,":agent_no",1), #Square 1
         (else_try),
           (eq,":entry_no",9),
           (agent_set_division,":agent_no",2), #Square 2
         (else_try),
           (eq,":entry_no",10),
           (agent_set_division,":agent_no",3), #Square 3
         (else_try),
           (eq,":entry_no",11),
           (agent_set_division,":agent_no",4), #Square 4
         (else_try),
           (eq,":entry_no",16),
           (agent_set_division,":agent_no",5), #Line 1
         (else_try),
           (eq,":entry_no",17),
           (agent_set_division,":agent_no",6), #Line 2
         (try_end),
         
         (try_begin),
           (agent_get_troop_id,":troop_id",":agent_no"),
           (eq,":troop_id","trp_russian_infantry_ai"),
           (agent_set_speed_limit,":agent_no",5),
         (try_end),
         
         (call_script, "script_correct_num_troops_in_formation", ":agent_no", 1), #Because I'm lazy ;D
         ]),
      		 
      (0, 0, ti_once, [],
        [
         (try_for_range,":unused",0,20),
          (init_position,pos1),
          (set_spawn_position,pos1),
          (spawn_scene_prop,"spr_formation_locator"),
          (scene_prop_set_visibility,reg0,0),
         (try_end),
         
         (entry_point_get_position,pos4,1),
         (scene_prop_get_instance,":instance","spr_formation_locator",0),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,2),
         (scene_prop_get_instance,":instance","spr_formation_locator",1),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,3),
         (scene_prop_get_instance,":instance","spr_formation_locator",2),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,5),
         (scene_prop_get_instance,":instance","spr_formation_locator",3),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,6),
         (scene_prop_get_instance,":instance","spr_formation_locator",10),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,8),
         (scene_prop_get_instance,":instance","spr_formation_locator",11),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,9),
         (scene_prop_get_instance,":instance","spr_formation_locator",12),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,10),
         (scene_prop_get_instance,":instance","spr_formation_locator",13),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,11),
         (scene_prop_get_instance,":instance","spr_formation_locator",14),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,16),
         (scene_prop_get_instance,":instance","spr_formation_locator",15),
         (prop_instance_animate_to_position,":instance",pos4,0),
         (entry_point_get_position,pos4,17),
         (scene_prop_get_instance,":instance","spr_formation_locator",16),
         (prop_instance_animate_to_position,":instance",pos4,0),
         
         (try_for_range,":square_slot_no",51,55),
           (troop_set_slot,"trp_custom_battle_dummy",":square_slot_no",mm_order_square),
         (try_end),
            
         ]),
         
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        
        (call_script, "script_correct_num_troops_in_formation", ":dead_agent_no", -1),
        
        (call_script, "script_sp_process_death_for_battle_results", ":dead_agent_no", ":killer_agent_no"),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),


      (0, 0, 1, [(key_clicked,key_f4),(neg|is_presentation_active,"prsnt_new_order_stuff")], #New orders
       [
        (start_presentation,"prsnt_new_order_stuff"),
       ]),
  		 
      (0, 0, 1, [], #Volley fire
       [
        (call_script, "script_volley_fire"),
       ]),
       
      (0, 0, 1, [], #Forming up troops
       [
        (call_script, "script_custom_battle_deployment"),
       ]),
         
      (ti_after_mission_start, 0, 0, [],
       [
         #(set_fog_distance,150,0xEDE3D6),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_2",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_2",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_3",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_3",0),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_4",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_4",0),
         
         (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_pointer_arrow"),
         (assign,"$g_hold_position_arrow_instance",reg0),
         (scene_prop_set_visibility,"$g_hold_position_arrow_instance",0),
         ]),

      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",25),     
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
              
            (call_script, "script_decide_run_away_or_not", ":agent_no"), #, ":mission_time" removed
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      common_battle_order_panel,
      common_battle_order_panel_tick,
      
    common_battle_victory_display,
    
    #(5, 0, ti_once, [],
      #[
     # (try_for_agents,":agent_no"),
     #   (agent_get_troop_id,":troop_id",":agent_no"),
     #   (eq,":troop_id","trp_russian_infantry_officer"),
      #  (mission_cam_set_mode,1),
      #  (mission_cam_set_target_agent, ":agent_no", 0),
     # (try_end),
     # ]),
    #(9, 0, ti_once, [],
    #  [
       # (mission_cam_clear_target_agent),
       # (mission_cam_set_mode,0),
    #  ]),
      
      (0, 0, 5, [],  #Bots fire when enemy close
      [
        (try_for_range,":division",0,7),
          (store_add,":division_slot",70,":division"),
          (neg|troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",8000),
          (lt,":min_dist",3000),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_fireatwill),
        (try_end),
        
        (try_for_range,":division",1,5),
          (store_add,":division_slot",110,":division"),
          (troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_hold),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",500),
          (lt,":min_dist",100),
          (team_give_order,1,":division",mordr_charge),
          (try_for_agents,":cur_agent"),
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",1),
            (agent_get_division,":agent_div",":cur_agent"),
            (eq,":agent_div",":division"), 
            (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
            #Cancel scripted destination for charge:
            (agent_clear_scripted_mode,":cur_agent"),
          (try_end),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_charge),
        (try_end),
        
        (try_for_range,":division",5,7),
          (store_add,":division_slot",110,":division"),
          (troop_slot_eq,"trp_custom_battle_dummy",":division_slot",mm_order_hold),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (copy_position,pos1,pos0),
          (call_script, "script_get_closest3_distance_of_enemies_at_pos1", 1, 1),
          (assign, ":avg_dist", reg0),
          (assign, ":min_dist", reg1),
          (this_or_next|lt,":avg_dist",1000),
          (lt,":min_dist",300),
          (team_give_order,1,":division",mordr_charge),
          (try_for_agents,":cur_agent"),
            (agent_is_human,":cur_agent"), #Run a bunch of agent checks...
            (agent_is_alive,":cur_agent"),
            (agent_get_team,":agent_team",":cur_agent"),
            (eq,":agent_team",1),
            (agent_get_division,":agent_div",":cur_agent"),
            (eq,":agent_div",":division"), 
            (agent_slot_eq,":cur_agent",slot_agent_is_running_away,0),
            #Cancel scripted destination for charge:
            (agent_clear_scripted_mode,":cur_agent"),
          (try_end),
          (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_charge),
        (try_end),
      ]),
      
    ## Mission states ##
    # 0 - Begin cut scene
    # 1 - Catch commander
    # 2 - Break Squares
    # 3 - Cut scene 2
    # 4 - Attack lines
    # 5 - Battle Won
    
      (0, 0, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (start_presentation,"prsnt_singleplayer_cutscene_bars"),
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 8000),
        (entry_point_get_position,pos2,16),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,150),
        (mission_cam_set_position,pos2),
        (entry_point_get_position,pos2,4),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,-70),
        (mission_cam_animate_to_position,pos2,15000),
      ]),
      
      (0, 0.1, ti_once, [(eq, "$g_mission_state", 0),],  #Cutscene 1
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_1"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",13500),
      ],
      [
        (mission_cam_animate_to_screen_color, 0xFF000000, 1500),
        (tutorial_message,-1),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",15000),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_2"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",23000)],
      [
        (entry_point_get_position,pos2,10),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,220),
        (position_move_x,pos2,-500,0),
        (position_move_y,pos2,-500,0),
        (position_rotate_x,pos2,-25),
        (mission_cam_set_position,pos2),
        (mission_cam_animate_to_screen_color, 0x00000000, 2500),
        (tutorial_message,-1),
        (entry_point_get_position,pos2,8),
        (position_move_z,pos2,1000),
        (position_rotate_z,pos2,30),
        (position_move_x,pos2,-1000,0),
        (position_move_y,pos2,-1000,0),
        (position_rotate_x,pos2,-25),
        (mission_cam_animate_to_position,pos2,10000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",23500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_3"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",34000)],
      [
        (tutorial_message,-1),
        (entry_point_get_position,pos2,6),
        (position_move_z,pos2,300),
        (position_rotate_z,pos2,-180),
        (position_move_y,pos2,-500,0),
        (mission_cam_animate_to_position,pos2,3500),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",36000),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_4"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 1
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",42000)],
      [
        (tutorial_message,-1),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (position_move_z,pos2,250),
        (mission_cam_animate_to_position,pos2,1000),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 0),
      (store_mission_timer_a_msec,":mt"),
      (gt,":mt",42900),
      ],
      [
        (assign,"$g_show_cutscene_bars",0),
        (mission_cam_set_mode, 0),
        (assign, "$g_mission_state", 1),# 1 - Catch commander
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Catch the Austrian commander before he reaches the Austrian squares!"),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
      ]),
          
      (0, 0, ti_once, [(eq, "$g_mission_state", 1),], 
      [
        (entry_point_get_position,pos4,7),
        (scene_prop_get_instance,":instance","spr_formation_locator",10),
        (prop_instance_animate_to_position,":instance",pos4,0), #Start run Austrian commander to this position
      ]),
       
      (0, 0, 0, [(eq, "$g_mission_state", 1),], 
      [
        (agent_get_position,pos5,"$g_enemy_commander_agent_1"),
        (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos5,0), #Follow commander with target locator
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 1), #Kill commander or he reach destination
      (assign,":continue",0),
      (try_begin),
        (agent_get_position,pos6,"$g_enemy_commander_agent_1"), #Commander reaching destination
        (entry_point_get_position,pos4,7),
        (get_distance_between_positions,":dist",pos4,pos6),
        (lt,":dist",200),
        (assign,":continue",1),
        (assign,"$g_objective_1_result",0),
      (else_try),
        (neg|agent_is_alive,"$g_enemy_commander_agent_1"), #Commander killed
        (assign,":continue",1),
        (assign,"$g_objective_1_result",1),
      (try_end),
      (eq,":continue",1),
      ], 
      [
        (assign, "$g_mission_state", 2),# 2 - Break Squares
        (assign, "$g_projection_state", 4),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Break the Austrian squares by either killing them or making them all rout."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",4),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_2_1"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
      ]),
      
      (0, 0, 0, [(eq, "$g_mission_state", 2),], 
      [
        (assign,":num_squares",0),
        (try_for_range,":division",1,5),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_squares",1),
          (try_begin),
            (eq,":num_squares",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow square with target locator
          (else_try),
            (eq,":num_squares",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos0,0), #Follow square with target locator
          (else_try),
            (eq,":num_squares",3),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_3",pos0,0), #Follow square with target locator
          (else_try),
            (eq,":num_squares",4),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_4",pos0,0), #Follow square with target locator
          (try_end),
        (try_end),
        (assign,"$g_projection_state",":num_squares"),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 2),], 
      [
        (eq,"$g_objective_1_result",1), #Commander dead
        (assign,":entry_no",12),
        (try_for_range,":division",11,15),
          (entry_point_get_position,pos4,":entry_no"),
          (scene_prop_get_instance,":instance","spr_formation_locator",":division"),
          (prop_instance_animate_to_position,":instance",pos4,0), #Retreat squares
          (val_add,":entry_no",1),
        (try_end),
        (try_for_agents,":agent_no"),
          (agent_is_active,":agent_no"), #Run a bunch of agent checks...
          (agent_is_human,":agent_no"),
          (agent_is_alive,":agent_no"),
          (agent_get_team,":agent_team",":agent_no"),
          (eq,":agent_team",1),
          (agent_get_division,":agent_division",":agent_no"),
          (is_between,":agent_division",1,5),
          (agent_get_slot,":agent_courage",":agent_no",slot_agent_courage_score),
          (val_div,":agent_courage",2),
          (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage"), 
        (try_end),
      ]),
      
    #  (1, 0, ti_once, [(eq, "$g_mission_state", 2),
    #                   (eq,"$g_objective_1_result",1),
    #                   (assign,":continue",1),
    #                   (try_for_agents,":agent_no"),
    #                    (eq,":continue",1),
    #                    (agent_is_active,":agent_no"), #Run a bunch of agent checks...
    #                    (agent_is_human,":agent_no"),
    #                    (agent_is_alive,":agent_no"), 
    #                    (agent_slot_eq,":agent_no",slot_agent_is_running_away,0),
    #                    
    #                    (agent_get_troop_id,":troop_id",":agent_no"),
    #                    (eq,":troop_id","trp_russian_infantry_ai"),
    #                    (agent_get_position,pos6,":agent_no"),
    #                    (agent_get_scripted_destination,pos7,":agent_no"),
    #                    (get_distance_between_positions,":dist",pos6,pos7),
    #                    (gt,":dist",400),
    #                    (assign,":continue",0),
    #                   (try_end),
    #                   (eq,":continue",1),
    #                   ], 
    #  [
    #    (try_for_range,":division",1,5),
    #      (store_add,":division_slot",110,":division"),
    #      (troop_set_slot,"trp_custom_battle_dummy",":division_slot",mm_order_retreat),
    #      (team_give_order,1,":division",mordr_retreat),
    #    (try_end),
    #  ]),
      
      (1, 0, ti_once, [
      (eq, "$g_mission_state", 2),
      (assign,":continue",1),
      (assign,":squares_gone",0),
      (try_for_range,":division",1,5),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (try_begin),
          (gt,":num_troops_in_division",0),
          (assign,":continue",0),
        (else_try),
          (val_add,":squares_gone",1),
        (try_end),
      (try_end),
      (assign,"$g_singleplayer_progress_counter_cur_value",":squares_gone"),
      (eq,":continue",1),
      ], 
      [
        (assign, "$g_mission_state", 3), # 3 - Cut scene 2
        (tutorial_message,-1),
        (assign, "$g_singleplayer_progress_counter_mode", -1),
        (assign,"$g_projection_state",0),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 3),],
      [
        (add_visitors_to_current_scene,16,"trp_russian_infantry_ai",25), #Spawn ze lines
        (add_visitors_to_current_scene,17,"trp_russian_infantry_ai",25),
        
        (add_visitors_to_current_scene,3,"trp_french_dragoon_ai",20), #And ze reinforcements
        
        (add_visitors_to_current_scene,5,"trp_french_dragoon_ai",20), #And extra mission help...
        
        (scene_prop_get_instance,":instance","spr_formation_locator",0),
        (call_script,"script_division_get_average_position",0,0),
        (copy_position,pos53,pos0),
        (call_script,"script_team_get_average_position_of_enemies",0),
        (copy_position,pos52,pos0),
        (get_angle_between_positions, ":rotation", pos53, pos52),
        (position_rotate_z,pos53,":rotation",0),
        (prop_instance_animate_to_position,":instance",pos53,0),
        (troop_set_slot,"trp_custom_battle_dummy",100,mm_order_hold),
        
        (scene_prop_get_instance,":instance","spr_formation_locator",1),
        (call_script,"script_division_get_average_position",0,1),
        (copy_position,pos53,pos0),
        (call_script,"script_team_get_average_position_of_enemies",0),
        (copy_position,pos52,pos0),
        (get_angle_between_positions, ":rotation", pos53, pos52),
        (position_rotate_z,pos53,":rotation",0),
        (prop_instance_animate_to_position,":instance",pos53,0),
        (troop_set_slot,"trp_custom_battle_dummy",101,mm_order_hold),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 3),],  #Cutscene 2
      [
        (mission_cam_set_mode, 1),
        (mission_cam_clear_target_agent),
        (mission_cam_set_screen_color, 0xFF000000),
        (mission_cam_animate_to_screen_color, 0x00000000, 8000),
        (entry_point_get_position,pos2,16),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,150),
        (position_move_y,pos2,-2000),
        (mission_cam_set_position,pos2),
        (entry_point_get_position,pos2,4),
        (position_move_z,pos2,500),
        (position_rotate_z,pos2,-70),
        (mission_cam_animate_to_position,pos2,15000),
        (store_mission_timer_a_msec,"$g_cut_scene_start"),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",500),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_5"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",13000),
      ],
      [
        (tutorial_message,-1),
        (entry_point_get_position,pos2,4),
        (position_move_z,pos2,2000),
        (position_rotate_z,pos2,-180),
        (mission_cam_animate_to_position,pos2,2000),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",13250),
      ],
      [
        (tutorial_message_set_background, 1),
        (tutorial_message,"str_cutscene_dresden_2_6"),
        #(tutorial_message_set_position, 500, 100),
      ]),
      
      (0, 0, ti_once, [  #Cutscene 2
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",18000),
      ],
      [
        (tutorial_message,-1),
        (get_player_agent_no,":player_agent"),
        (agent_get_position,pos2,":player_agent"),
        (position_move_z,pos2,250),
        (mission_cam_animate_to_position,pos2,1000),
      ]),
      
      (0, 0, ti_once, [
      (eq, "$g_mission_state", 3),
      (store_mission_timer_a_msec,":mt"),
      (val_sub,":mt","$g_cut_scene_start"),
      (gt,":mt",16900)
      ],
      [
        (mission_cam_set_mode, 0),
        (assign, "$g_mission_state", 4),# 4 - Attack lines
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Attack the lines guarding the village and destroy or rout them."),
        (assign, "$g_singleplayer_progress_counter_mode", 2),
        (assign,"$g_singleplayer_progress_counter_cur_value",0),
        (assign,"$g_singleplayer_progress_counter_max_value",2),
        (assign,"$g_singleplayer_progress_counter_string_id","str_dresden_2_2"),
        (start_presentation,"prsnt_singleplayer_progress_counter"),
        (assign, "$g_projection_state", 2),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
      ]),
      
      (0, 0, 0, [(eq, "$g_mission_state", 4),], 
      [
        (assign,":num_lines",0),
        (try_for_range,":division",5,7),
          (call_script,"script_division_get_average_position", 1, ":division"),
          (gt,reg0,0),
          (val_add,":num_lines",1),
          (try_begin),
            (eq,":num_lines",1),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos0,0), #Follow line with target locator
          (else_try),
            (eq,":num_lines",2),
            (prop_instance_animate_to_position,"$g_objectives_locator_instance_2",pos0,0), #Follow line with target locator
          (try_end),
        (try_end),
        (assign,"$g_projection_state",":num_lines"),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 4),], 
      [
        (entry_point_get_position,pos4,4),
        (scene_prop_get_instance,":instance","spr_formation_locator",2),  
        (prop_instance_animate_to_position,":instance",pos4,0), #Move reinforcements
        (position_move_x,pos4,4000),
        (position_set_z_to_ground_level,pos4),
        (scene_prop_get_instance,":instance","spr_formation_locator",3),  
        (prop_instance_animate_to_position,":instance",pos4,0), #Move mission help
        
        (entry_point_get_position,pos4,18),
        (scene_prop_get_instance,":instance","spr_formation_locator",16),  
        (prop_instance_animate_to_position,":instance",pos4,0), #And move Austrians...
      ]),
      
      (1, 0, ti_once, [
      (eq, "$g_mission_state", 4),
      (assign,":continue",1),
      (assign,":lines_gone",0),
      (try_for_range,":division",5,7),
        (store_add,":division_slot",30,":division"),
        (troop_get_slot,":num_troops_in_division","trp_custom_battle_dummy",":division_slot"),
        (try_begin),
          (gt,":num_troops_in_division",0),
          (assign,":continue",0),
        (else_try),
          (val_add,":lines_gone",1),
        (try_end),
      (try_end),
      (assign,"$g_singleplayer_progress_counter_cur_value",":lines_gone"),
      (eq,":continue",1),
      ], 
      [
        (assign, "$g_mission_state", 5), # 5 - Battle Won
        (assign,"$g_projection_state",0),
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Vive l'Empereur! La Victoire est a Nous!"),
      ]),
      
      (0, 0, ti_once, [(eq, "$g_mission_state", 5),], 
      [
        (assign,"$g_battle_won",1),
      ]),
      
    (ti_tab_pressed, 0, 0, [],
      [
        (try_begin),
          (eq, "$g_mission_state", 5), #Battle won
          (val_add,"$g_finished_missions",1),
          (assign,"$g_finished_sub_missions",0),
          (finish_mission,0),
        (else_try),
          (question_box,"str_confirm_quit_mission"),
        (try_end),
      ]),
    (ti_question_answered, 0, 0, [],
      [
        (store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (start_presentation,"prsnt_singleplayer_mission_results"),
        (finish_mission,0),
      ]),
    
      (1, 4, ti_once, [(main_hero_fallen),],
      [
        (finish_mission,0),
      ]),

    ],
  ),

#Idea6
#
#Spawn points:
#
#French side:
#
#0  - Player Spawn
#1  - (Player) Bots Spawn
#2  - Nappy Spawn
#3  - Nappy Guards Spawn
#4  - Rapp Spawn
#5  - Rapp Location
#6  - Cannon 1
#7  - Cannon 2
#8  - Cannon 3
#
#Russian Side:
#
#3  - Russian Cav Charging 1
#4  - Russian Cav Charging 2
#5  - Russian Cav Counter-attacking
#6  - Russian Cav Counter-attacking location


(
    "camp_1",0,-1,
    "Camp Visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
   (9,mtef_visitor_source,af_override_horse,0,1,[]),
   (10,mtef_visitor_source,af_override_horse,0,1,[]),
   (11,mtef_visitor_source,af_override_horse,0,1,[]),
   (12,mtef_visitor_source,af_override_horse,0,1,[]),
   (13,mtef_visitor_source,0,0,1,[]),
   (14,mtef_scene_source,0,0,1,[]),
   (15,mtef_scene_source,0,0,1,[]),
   (16,mtef_visitor_source,af_override_horse,0,1,[]),
   (17,mtef_visitor_source,af_override_horse,0,1,[]),
   (18,mtef_visitor_source,af_override_horse,0,1,[]),
   (19,mtef_visitor_source,af_override_horse,0,1,[]),
   (20,mtef_visitor_source,af_override_horse,0,1,[]),
   (21,mtef_visitor_source,af_override_horse,0,1,[]),
   (22,mtef_visitor_source,af_override_horse,0,1,[]),
	 (23,mtef_visitor_source,af_override_horse,0,1,[]), #guard
   (24,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (25,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (26,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (27,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (28,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (29,mtef_visitor_source,af_override_horse,0,1,[]),
	 (30,mtef_visitor_source,af_override_horse,0,1,[]),
	 (31,mtef_visitor_source,af_override_horse,0,1,[]),
   (32,mtef_visitor_source,af_override_horse,0,1,[]),
	 (33,mtef_visitor_source,af_override_horse,0,1,[]),
	 (34,mtef_visitor_source,af_override_horse,0,1,[]),
	 (35,mtef_visitor_source,af_override_horse,0,1,[]),
	 (36,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (37,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (38,mtef_visitor_source,af_override_horse,0,1,[]),
	 (39,mtef_visitor_source,af_override_horse,0,1,[]),
   (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
   (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [


      (ti_before_mission_start, 0, 0, [],
      [
        (assign, "$g_main_attacker_agent", 0),
	  ]),
    
      (1, 0, ti_once, 
      [],
      [

        (call_script, "script_init_town_walker_agents"),

          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),

      ]),

      (ti_before_mission_start, 0, 0, 
      [], 
      [
        (scene_set_day_time,7),
      
        #Insert player companions here
        (assign,":entry_no",1),
        (try_for_range, ":cur_companion",companions_begin, companions_end),
          (lt,":entry_no",10),
          (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
          #(troop_slot_eq, ":cur_companion", slot_troop_active_this_mission, 1),
          (add_visitors_to_current_scene,":entry_no",":cur_companion",1),
          (val_add,":entry_no",1),
        (try_end),
        
        (try_for_range,":entry_no",10,20),
          (store_random_in_range,":random",0,3),
          (try_begin), 
            (eq,":random",0),
            (add_visitors_to_current_scene,":entry_no","trp_walker_peasant_male",1),
          (else_try), 
            (eq,":random",1),
            (add_visitors_to_current_scene,":entry_no","trp_walker_peasant_female",1),
          (else_try), 
            (eq,":random",2),
            (add_visitors_to_current_scene,":entry_no","trp_walker_peasant_male",1),
            (add_visitors_to_current_scene,":entry_no","trp_walker_peasant_female",1),
          (try_end),
        (try_end),
        (try_for_range,":entry_no",20,27),
          (add_visitors_to_current_scene,":entry_no","trp_walker_french_infantry",1),
        (try_end),
        (try_for_range,":entry_no",27,31),
          (add_visitors_to_current_scene,":entry_no","trp_walker_french_voltigeur",1),
        (try_end),
        (try_for_range,":entry_no",31,35),
          (add_visitors_to_current_scene,":entry_no","trp_walker_french_hussar",1),
        (try_end),
        (try_for_range,":entry_no",35,37),
          (add_visitors_to_current_scene,":entry_no","trp_walker_french_officer",1),
        (try_end),
        
        (add_visitors_to_current_scene,9,"trp_camp_armorer",1),
        (add_visitors_to_current_scene,10,"trp_camp_weaponsmith",1),
        (add_visitors_to_current_scene,12,"trp_camp_horse_merchant",1),
        (add_visitors_to_current_scene,12,"trp_walker_messenger",1),
        
        (call_script,"script_sp_camp_set_merchandise"), #Should not be called here later
      ]),
      
      (ti_after_mission_start, 0, 0, 
      [], 
      [
        (init_position,pos1),
         (set_spawn_position,pos1),
         (spawn_scene_prop,"spr_objectives_locator"),
         (assign,"$g_objectives_locator_instance_1",reg0),
         (scene_prop_set_visibility,"$g_objectives_locator_instance_1",0),
         
        (tutorial_message_set_background, 1),
        (tutorial_message,"@Talk to the messenger for your next mission."),
        (assign, "$g_projection_state", 1),
        (start_presentation,"prsnt_singleplayer_objective_projection_display"),
       # (entry_point_get_position,pos5,10),
        #(prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos5,0), #Set target locator
      
      ]),
      
      (0, 0, 0,
      [],
      [
        (try_begin),
          (neg|is_presentation_active,"prsnt_singleplayer_objective_projection_display"),
          (start_presentation,"prsnt_singleplayer_objective_projection_display"),
        (try_end),
      
        (eq, "$g_projection_state", 1),
        (try_for_agents,":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_get_troop_id,":cur_troop",":cur_agent"),
          (eq, ":cur_troop","trp_walker_messenger"),
          (agent_get_position,pos5,":cur_agent"),
          (prop_instance_animate_to_position,"$g_objectives_locator_instance_1",pos5,0), #Set target locator
        (try_end),
      ]),
      
      (ti_inventory_key_pressed, 0, 0,
      [

          (display_message, "str_cant_use_inventory_now"),

      ], 
      []),
       
      (ti_tab_pressed, 0, 0,
      [

          (mission_enable_talk),
          (set_trigger_result,1),

      ], 
      []),

      (ti_on_leave_area, 0, 0,
      [

          (assign,"$g_leave_town",1),

      ], 
      [

        (mission_enable_talk),
      ]),            

     (0, 0, ti_once, 
     [], 
     [
       (call_script, "script_town_init_doors", 0),
     ]),

	(3, 0, 0, 
	[
	  (call_script, "script_tick_town_walkers")
	], 
	[]),
	
	
	
   (3, 0, 0, 
   [     
     (main_hero_fallen, 0),
   ],	  
   [
   
	   (set_trigger_result,1),

   ]),
	

  ]),

]
