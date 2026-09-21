# -*- coding: cp1252 -*-
from header_common import *
from header_scene_props import *
from header_operations import *
from header_triggers import *
from header_sounds import *
from module_constants import *
import string

####################################################################################################################
#  Each scene prop record contains the following fields:
#  1) Scene prop id: used for referencing scene props in other files. The prefix spr_ is automatically added before each scene prop id.
#  2) Scene prop flags. See header_scene_props.py for a list of available flags
#  3) Mesh name: Name of the mesh.
#  4) Physics object name:
#  5) Triggers: Simple triggers that are associated with the scene prop
####################################################################################################################

#MM
check_mm_on_destroy_window_trigger = (ti_on_scene_prop_destroy,
  [
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),

      (store_trigger_param_1, ":instance_id"),      
      (prop_instance_is_valid,":instance_id"),
      (prop_instance_get_scene_prop_kind,":prop_kind",":instance_id"),
      (prop_instance_get_position,pos49,":instance_id"),
      
      (copy_position,pos56,pos49),
      (position_move_z,pos56,140),
      (particle_system_burst, "psys_bottle_break", pos56, 10),
      (call_script, "script_multiplayer_server_play_sound_at_position", "snd_glass_break"),
      
      (assign,":prop_to_spawn",-1),
      (try_begin),
        (eq,":prop_kind","spr_mm_window1"),
        (assign,":prop_to_spawn","spr_mm_window1d"),
      (else_try),
        (eq,":prop_kind","spr_mm_window2"),
        (assign,":prop_to_spawn","spr_mm_window2d"),
      (else_try),
        (eq,":prop_kind","spr_mm_window1_poor"),
        (assign,":prop_to_spawn","spr_mm_window1d_poor"),
      (else_try),
        (eq,":prop_kind","spr_mm_window2_poor"),
        (assign,":prop_to_spawn","spr_mm_window2d_poor"),
      (else_try),
        (eq,":prop_kind","spr_mm_window3"),
        (assign,":prop_to_spawn","spr_mm_window3d"),
      (else_try),
        (eq,":prop_kind","spr_mm_window4"),
        (assign,":prop_to_spawn","spr_mm_window4d"),
      (else_try),
        (eq,":prop_kind","spr_mm_window3_poor"),
        (assign,":prop_to_spawn","spr_mm_window3d_poor"),
      (else_try),
        (eq,":prop_kind","spr_mm_window4_poor"),
        (assign,":prop_to_spawn","spr_mm_window4d_poor"),
      (try_end),
      
      (try_begin),
        (scene_prop_slot_eq, ":instance_id", scene_prop_slot_is_scaled, 1), # is scaled.
        (scene_prop_get_slot,":x_scale",":instance_id",scene_prop_slot_x_scale),
        (scene_prop_get_slot,":y_scale",":instance_id",scene_prop_slot_y_scale),
        (scene_prop_get_slot,":z_scale",":instance_id",scene_prop_slot_z_scale),
        (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 0, 1, ":x_scale",":y_scale",":z_scale"),
      (else_try),
        (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 0, 0),
      (try_end),
      (assign,":destroyed_prop",reg0),
      
      (scene_prop_set_slot, ":destroyed_prop", scene_prop_slot_replacing, ":instance_id"),
      
      (scene_prop_get_slot,":wall_instance",":instance_id", scene_prop_slot_parent_prop),
      (try_begin),
        (prop_instance_is_valid,":wall_instance"),
        (scene_prop_set_slot,":destroyed_prop",scene_prop_slot_parent_prop,":wall_instance"),
        
        (scene_prop_set_slot,":wall_instance",scene_prop_slot_child_prop1,":destroyed_prop"),
      (try_end),
      
      (call_script, "script_clean_up_prop_instance", ":instance_id"),
    (try_end),
  ])


check_mm_use_cannon_prop_start_trigger = (ti_on_scene_prop_start_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),
    
    (call_script, "script_multiplayer_server_check_if_can_use_button", ":agent_id", ":instance_id"),
    (eq, reg0, 1),
    
    (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
     
    (assign, ":anim_id", -1),
    (try_begin),
      (is_between, ":scene_prop_id", mm_unlimber_button_types_begin, mm_unlimber_button_types_end), 
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_limber_button"),
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_aim_button"),
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_load_rocket_button"),
      (assign, ":anim_id", "anim_rocket_load"),
    (else_try),
      (is_between,":scene_prop_id","spr_mm_load_cartridge_button","spr_mm_reload_button"), # Load something button
      (assign, ":anim_id", "anim_cannon_load"),
      (try_begin),
        (agent_get_slot, ":frizzle_times", ":agent_id", slot_agent_frizzle_times),
        (val_add,":frizzle_times",1),
        (agent_set_slot, ":agent_id", slot_agent_frizzle_times, ":frizzle_times"),
        (try_begin),
          (le,":frizzle_times",3), # only 2 times before calling it off
          # pos56 is sound pos.
          (prop_instance_get_position,pos56,":instance_id"),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_cannon_ball"),
        (try_end),
      (try_end),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_reload_button"),
      (assign, ":anim_id", "anim_cannon_reload"),
      (try_begin),
        (agent_get_slot, ":frizzle_times", ":agent_id", slot_agent_frizzle_times),
        (val_add,":frizzle_times",1),
        (agent_set_slot, ":agent_id", slot_agent_frizzle_times, ":frizzle_times"),
        (try_begin),
          (le,":frizzle_times",3), # only 2 times before calling it off
          # pos56 is sound pos.
          (prop_instance_get_position,pos56,":instance_id"),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_ramrod"),
        (try_end),
      (try_end),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_round_button"),
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_shell_button"),
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_canister_button"),
      #(assign, ":anim_id", "anim_"),
    (else_try),
      (eq, ":scene_prop_id", "spr_mm_bomb_button"),
      #(assign, ":anim_id", "anim_"),
    (try_end),
    
    (try_begin),
      (gt,":anim_id",-1),
      # stop current anim
      (agent_set_animation, ":agent_id", "anim_cannon_end", 1),
      (agent_set_animation_progress, ":agent_id", 100),
      # and play new
      (agent_set_animation, ":agent_id", ":anim_id", 1),
    (try_end),
  ])

check_mm_use_cannon_prop_end_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),
    
    (call_script, "script_multiplayer_server_check_if_can_use_button", ":agent_id", ":instance_id"),
    (eq, reg0, 1),
    
    (agent_set_slot,":agent_id", slot_agent_frizzle_times,0), # Reset frizzles
    
    (call_script, "script_use_item", ":instance_id", ":agent_id"),
   ])

check_mm_use_cannon_prop_cancel_trigger = (ti_on_scene_prop_cancel_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),

    (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
    
    (try_begin),
      (this_or_next|is_between,":scene_prop_id","spr_mm_load_cartridge_button","spr_mm_reload_button"),
      (eq, ":scene_prop_id", "spr_mm_reload_button"),
      (agent_set_animation, ":agent_id", "anim_cannon_end", 1),
    (try_end),
  ])
  
check_item_use_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),
    
    #for only server itself-----------------------------------------------------------------------------------------------
    (call_script, "script_use_item", ":instance_id", ":agent_id"),
    #for only server itself-----------------------------------------------------------------------------------------------                          
    (try_for_players, ":player_no", 1),
      (player_is_active, ":player_no"),
      (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_use_item, ":instance_id", ":agent_id"),
    (try_end),
  ])
  
check_cannon_animation_finished_trigger = (ti_on_scene_prop_animation_finished,
  [
    (store_trigger_param_1, ":instance_id"),
    
    (try_begin),
      (prop_instance_is_valid, ":instance_id"),
      
      (scene_prop_slot_eq, ":instance_id", scene_prop_slot_just_pushed_back, 1), # Just has been pushed back by player.
      (scene_prop_set_slot,":instance_id",scene_prop_slot_just_pushed_back,0),
      
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
      
      (call_script,"script_cannon_instance_get_barrel",":instance_id"), # then activate the aim button.
      (call_script, "script_prop_instance_find_first_child_of_type", reg0, "spr_mm_aim_button"),
      (call_script,"script_set_prop_child_active",reg0),
    (try_end),
  ])

check_cannon_wheels_animation_finished_trigger = (ti_on_scene_prop_animation_finished,
  [
    (store_trigger_param_1, ":instance_id"),
    
    (try_begin),
      (prop_instance_is_valid, ":instance_id"),
      (scene_prop_slot_eq, ":instance_id", scene_prop_slot_just_pushed_back, 1), # Just has been pushed back by player.
      (scene_prop_set_slot,":instance_id",scene_prop_slot_just_pushed_back,0),
      
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
      
      (scene_prop_get_slot,reg0,":instance_id", scene_prop_slot_parent_prop),
      (call_script,"script_cannon_instance_get_barrel",reg0), # then activate the aim button.
      (call_script, "script_prop_instance_find_first_child_of_type", reg0, "spr_mm_aim_button"),
      (call_script,"script_set_prop_child_active",reg0),
    (try_end),
  ])
  
check_common_teleport_door_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),

    (try_begin),
      (agent_is_active,":agent_id"),
      (agent_is_alive,":agent_id"),
      (prop_instance_is_valid,":instance_id"),
      
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
    
      (prop_instance_get_variation_id, ":teleport_id", ":instance_id"),

      (assign,":found_dest_instance_id", -1),
      (try_for_range,":door_type","spr_door_teleport_vertical","spr_door_teleport_props_end"),
        (try_for_prop_instances, ":cur_instance_id", ":door_type", somt_object),
          (eq,":found_dest_instance_id", -1), # not found yet.
          (neq, ":cur_instance_id", ":instance_id"),
          
          (prop_instance_get_variation_id, ":dest_teleport_id", ":cur_instance_id"),
          (eq, ":teleport_id", ":dest_teleport_id"),
          
          (assign, ":found_dest_instance_id", ":cur_instance_id"),
        (try_end),
      (try_end),

      (try_begin),
        (prop_instance_is_valid,":found_dest_instance_id"),
        
        (prop_instance_get_position, pos1, ":found_dest_instance_id"),
        (try_begin),
          (prop_instance_get_scene_prop_kind, ":door_kind", ":found_dest_instance_id"),
          (eq, ":door_kind", "spr_door_teleport_vertical"),
          (position_move_y, pos1, -150),
          (position_move_x, pos1, -50),
          (agent_set_position, ":agent_id", pos1),
        (else_try),
          (agent_set_position, ":agent_id", pos1),
        (try_end),
      (try_end),
  (try_end),
  ])
  
check_sally_door_use_trigger_double = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),
    
    (scene_prop_slot_ge,":instance_id",scene_prop_slot_health,1),
    
    (agent_get_position, pos1, ":agent_id"),
    (prop_instance_get_starting_position, pos2, ":instance_id"),
    
    (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

    (try_begin),
      #out doors like castle sally door can be opened only from inside, if door coordinate is behind your coordinate. Also it can be closed from both sides.
      
      #(prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
      
      (prop_instance_get_variation_id,":combined_val",":instance_id"),
      #(store_div, ":reversed_rotation", ":combined_val", 10),
      (store_mod, ":owner_team", ":combined_val", 10),
      
      #(assign, ":can_open_door", 0),
      # (try_begin),
        # (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        
        #(prop_instance_get_variation_id_2,":reversed_rotation",":instance_id"),
        # (try_begin),
          # (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
          # (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
          # (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
          # (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
          
          # (try_begin),
            # (eq,":reversed_rotation",1),
            # (neg|position_is_behind_position, pos1, pos2),
            # (assign, ":can_open_door", 1),
          # (else_try),
            # (position_is_behind_position, pos1, pos2),
            # (assign, ":can_open_door", 1),
          # (try_end),
        # (else_try),  
          # (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
          # (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
          # (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
          # (eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
          # (try_begin),
            # (eq,":reversed_rotation",1),
            # (position_is_behind_position, pos1, pos2),
            # (assign, ":can_open_door", 1),
          # (else_try),
            # (neg|position_is_behind_position, pos1, pos2),
            # (assign, ":can_open_door", 1),
          # (try_end),
        # (try_end),
      # (else_try),
        (assign, ":can_open_door", 1),
      #(try_end),
      
      (try_begin),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_deathmatch),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_duel),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_king),
        #(prop_instance_get_variation_id,":owner_team",":instance_id"),
        (is_between,":owner_team",1,3), # either 1 or 2
        (val_sub,":owner_team",1), # 1 = team1   2 = team2  however teams are 0 and 1 so sub 1.
        
        (agent_get_team, ":agent_team", ":agent_id"),
        (neq, ":agent_team", ":owner_team"),
        (assign,":can_open_door",0),
      (try_end),
      
      # pos56 is sound pos.
      (copy_position,pos56,pos2),
      (try_begin),
        (eq, ":can_open_door", 0), # cant open door so play lock sound.
        (try_begin),
          (store_mission_timer_a,":cur_time"),
          (agent_get_slot,":sound_at",":agent_id",slot_agent_last_sound_at),
          (store_sub,":elapsed_time",":cur_time",":sound_at"),
          
          (ge,":elapsed_time",1), # 1 second or more.
          
          (agent_set_slot, ":agent_id", slot_agent_last_sound_at, ":cur_time"),
          
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_lock"),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":opened_or_closed", 1),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_close"),
        (else_try),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_open"),
        (try_end),
      
        #for only server itself-----------------------------------------------------------------------------------------------
        (call_script, "script_use_item", ":instance_id", ":agent_id"),
        #for only server itself-----------------------------------------------------------------------------------------------                        
        (try_for_players, ":player_no", 1),
          (player_is_active, ":player_no"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_use_item, ":instance_id", ":agent_id"),
        (try_end),
      (try_end),
    (try_end),
  ])

check_sally_door_use_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),

    (scene_prop_slot_ge,":instance_id",scene_prop_slot_health,1),
    
    (agent_get_position, pos1, ":agent_id"),
    (prop_instance_get_starting_position, pos2, ":instance_id"),
    
    (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
    (prop_instance_get_variation_id,":combined_val",":instance_id"),
    #(store_div, ":reversed_rotation", ":combined_val", 10),
    (store_mod, ":owner_team", ":combined_val", 10),
    
    (try_begin),
      #out doors like castle sally door can be opened only from inside, if door coordinate is behind your coordinate. Also it can be closed from both sides.
      
      (assign,":can_open_door",1),
      (try_begin),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_deathmatch),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_duel),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_king),
        #(prop_instance_get_variation_id,":owner_team",":instance_id"),
        (is_between,":owner_team",1,3), # either 1 or 2
        (val_sub,":owner_team",1), # 1 = team1   2 = team2  however teams are 0 and 1 so sub 1.
        
        (agent_get_team, ":agent_team", ":agent_id"),
        (neq, ":agent_team", ":owner_team"),
        (assign,":can_open_door",0),
      (try_end),
      # (try_begin),
        # (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        
        ##(prop_instance_get_variation_id_2,":reversed_rotation",":instance_id"),
        # (try_begin),
          # (eq,":reversed_rotation",1),
          # (position_is_behind_position, pos1, pos2),
          # (assign,":can_open_door",0),
        # (else_try),
          # (neg|position_is_behind_position, pos1, pos2),
          # (assign,":can_open_door",0),
        # (try_end),
      # (try_end),
      
      # pos56 is sound pos.
      (copy_position,pos56,pos2),
      (try_begin),
        (eq, ":can_open_door", 0), # cant open door so play lock sound.
        (try_begin),
          (store_mission_timer_a,":cur_time"),
          (agent_get_slot,":sound_at",":agent_id",slot_agent_last_sound_at),
          (store_sub,":elapsed_time",":cur_time",":sound_at"),
          
          (ge,":elapsed_time",1), # 1 second or more.
          
          (agent_set_slot, ":agent_id", slot_agent_last_sound_at, ":cur_time"),
          
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_lock"),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":opened_or_closed", 1),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_close"),
        (else_try),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_open"),
        (try_end),
        
        #for only server itself-----------------------------------------------------------------------------------------------
        (call_script, "script_use_item", ":instance_id", ":agent_id"),
        #for only server itself-----------------------------------------------------------------------------------------------                            
        (try_for_players, ":player_no", 1),
          (player_is_active, ":player_no"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_use_item, ":instance_id", ":agent_id"),
        (try_end),
      (try_end),
    (try_end),
  ])

check_castle_door_use_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),

    (scene_prop_slot_ge,":instance_id",scene_prop_slot_health,1),
    
    (agent_get_position, pos1, ":agent_id"),
    (prop_instance_get_starting_position, pos2, ":instance_id"),
    
    (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
    (prop_instance_get_variation_id,":combined_val",":instance_id"),
    #(store_div, ":reversed_rotation", ":combined_val", 10),
    (store_mod, ":owner_team", ":combined_val", 10),
    
    (try_begin),
      (ge, ":agent_id", 0),
      (agent_get_team, ":agent_team", ":agent_id"),

      (assign,":can_open_door",1),
      #(try_begin),
        #(eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        ##in doors like castle room doors can be opened from both sides, but only defenders can open these doors. Also it can be closed from both sides.
        #(neq, ":agent_team", 0),
        #(assign,":can_open_door",0),
     # (else_try),
        #(prop_instance_get_variation_id,":owner_team",":instance_id"),
      (try_begin),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_deathmatch),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_duel),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_royale),
        (neq,"$g_multiplayer_game_type",multiplayer_game_type_king),
        (is_between,":owner_team",1,3), # either 1 or 2
        (val_sub,":owner_team",1), # 1 = team1   2 = team2  however teams are 0 and 1 so sub 1.
        
        (neq, ":agent_team", ":owner_team"),
        (assign,":can_open_door",0),
      (try_end),
      
      # pos56 is sound pos.
      (copy_position,pos56,pos2),
      (try_begin),
        (eq, ":can_open_door", 0), # cant open door so play lock sound.
        (try_begin),
          (store_mission_timer_a,":cur_time"),
          (agent_get_slot,":sound_at",":agent_id",slot_agent_last_sound_at),
          (store_sub,":elapsed_time",":cur_time",":sound_at"),
          
          (ge,":elapsed_time",1), # 1 second or more.
          
          (agent_set_slot, ":agent_id", slot_agent_last_sound_at, ":cur_time"),
          
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_lock"),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":opened_or_closed", 1),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_close"),
        (else_try),
          (call_script,"script_multiplayer_server_play_sound_at_position","snd_door_open"),
        (try_end),
        
        #for only server itself-----------------------------------------------------------------------------------------------
        (call_script, "script_use_item", ":instance_id", ":agent_id"),
        #for only server itself-----------------------------------------------------------------------------------------------                           
        (try_for_players, ":player_no", 1),
          (player_is_active, ":player_no"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_use_item, ":instance_id", ":agent_id"),
        (try_end),
      (try_end),
    (try_end),
  ])

check_ladder_animate_trigger = (ti_on_scene_prop_is_animating,
  [      
    (store_trigger_param_1, ":instance_id"),
    (store_trigger_param_2, ":remaining_time"),
    (try_begin),
      (neg|multiplayer_is_dedicated_server),
      (prop_instance_is_valid, ":instance_id"),
      
      (call_script, "script_check_creating_ladder_dust_effect", ":instance_id", ":remaining_time"),
    (try_end),
  ])

check_ladder_animation_finish_trigger = (ti_on_scene_prop_animation_finished,
  [
    (store_trigger_param_1, ":instance_id"),
    
    (try_begin),
      (prop_instance_is_valid, ":instance_id"),

      (prop_instance_enable_physics, ":instance_id", 1),
    (try_end),
  ])

check_common_object_hit_trigger = (ti_on_scene_prop_hit,
  [
    (store_trigger_param_1, ":instance_no"),       
    (store_trigger_param_2, ":damage"),
     
    (set_trigger_result,0), #Don't deal any normal damage to the prop

    (set_fixed_point_multiplier, 1),
    (position_get_x, ":agent_id", pos2),
    (set_fixed_point_multiplier, 100),
    (agent_is_active,":agent_id"),
    (agent_is_alive, ":agent_id"),
    
    (agent_get_wielded_item,":item_id",":agent_id",0),
    (try_begin),
      (this_or_next|eq,":item_id","itm_sapper_axe_rus"),
      (this_or_next|eq,":item_id","itm_sapper_axe"),
      (this_or_next|eq,":item_id","itm_russian_peasant_axe"),
      (eq,":item_id","itm_russian_peasant_2handed_axe"),
      (val_mul,":damage",3),
    (else_try),
      (eq,":item_id","itm_construction_hammer"),
      (assign,":damage",-25),
    (try_end),
    
    # apply dmg
    (scene_prop_get_hit_points, ":hit_points", ":instance_no"),
    (scene_prop_get_slot,":max_health",":instance_no",scene_prop_slot_max_health),
    (val_sub,":hit_points",":damage"),
    (val_max,":hit_points", 0), # Make sure we have no value under 0.
    (val_min,":hit_points", ":max_health"),
    (scene_prop_set_cur_hit_points, ":instance_no", ":hit_points"),
    (scene_prop_set_slot,":instance_no",scene_prop_slot_health,":hit_points"),
    
    (try_begin),
      (gt, ":hit_points", 0),
      (play_sound, "snd_dummy_hit"),
    (else_try),
      (neg|multiplayer_is_server),
      (play_sound, "snd_dummy_destroyed"),
    (try_end),

    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),

      (particle_system_burst, "psys_dummy_smoke", pos1, 3),
      (particle_system_burst, "psys_dummy_straw", pos1, 10),
    (try_end),
  ])

check_common_door_destroy_trigger = (ti_on_scene_prop_destroy,
  [
    (play_sound, "snd_dummy_destroyed"),
    
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),

      (store_trigger_param_1, ":instance_no"),      
      (store_trigger_param_2, ":attacker_agent_no"),

      (set_fixed_point_multiplier, 100),
      (prop_instance_get_position, pos1, ":instance_no"),
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
      
      (try_begin),
        (eq,":prop_kind","spr_mm_restroom_door"),
        
        (position_rotate_z,pos1,90),
      (try_end),

      (assign, ":rotate_side", 88),
      (try_begin),
        (ge, ":attacker_agent_no", 0),
        (agent_get_position, pos2, ":attacker_agent_no"),
        (try_begin),
          (position_is_behind_position, pos2, pos1),
          (val_mul, ":rotate_side", -1),
        (try_end),
      (try_end),
    
      (init_position, pos3),
      
      (try_begin),
        (ge, ":rotate_side", 0),
        (position_move_y, pos3, -100),
      (else_try),
        (position_move_y, pos3, 100),
      (try_end),
      
      (position_move_x, pos3, -50),
      (position_transform_position_to_parent, pos4, pos1, pos3),
      (position_move_z, pos4, 100),
      (position_get_distance_to_ground_level, ":height_to_terrain", pos4),
      (val_sub, ":height_to_terrain", 100),
      (assign, ":z_difference", ":height_to_terrain"),
      #(assign, reg0, ":z_difference"),
      #(display_message, "@{!}z dif : {reg0}"),
      (val_div, ":z_difference", 3),

      (try_begin),
        (ge, ":rotate_side", 0),
        (val_add, ":rotate_side", ":z_difference"),
      (else_try),
        (val_sub, ":rotate_side", ":z_difference"),
      (try_end),
      
      (try_begin),
        (eq,":prop_kind","spr_mm_restroom_door"),
        
        (position_rotate_z,pos1,-90),
        (position_rotate_y, pos1, ":rotate_side"),
      (else_try),
        (position_rotate_x, pos1, ":rotate_side"),
      (try_end),
      
      (prop_instance_animate_to_position, ":instance_no", pos1, 70), #animate to position 1 in 0.7 second
    (try_end),
  ])

check_common_constructible_props_destroy_trigger = (ti_on_scene_prop_destroy,
  [
    (play_sound, "snd_dummy_destroyed"),
    
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),

      (store_trigger_param_1, ":instance_no"),
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
      (scene_prop_get_slot,":attacker_agent_id",":instance_no",scene_prop_slot_last_hit_by),
      
      (prop_instance_get_position, pos49, ":instance_no"),            
      
      (particle_system_burst, "psys_dummy_straw", pos49, 20),
      (particle_system_burst, "psys_dummy_smoke", pos49, 50),

      (call_script, "script_clean_up_prop_instance", ":instance_no"),
      
      (store_add,":cost_index",construct_costs_offset,":prop_kind"),
      (val_sub,":cost_index",mm_construct_props_begin),
      (troop_get_slot,":prop_cost","trp_track_select_dummy",":cost_index"),
      (val_sub,":prop_cost",1), #Return prop cost -1 build points when deconstructing
      
      (agent_is_active,":attacker_agent_id"),
      (agent_get_team,":team_no",":attacker_agent_id"),
      (try_begin),
        (eq,":team_no",0),
        (val_add,"$g_team_1_build_points",":prop_cost"),
      (else_try),
        (val_add,"$g_team_2_build_points",":prop_cost"),
      (try_end),     
      
      (call_script,"script_multiplayer_server_send_build_points"),

    (try_end),
  ])
  
check_common_destructible_props_destroy_trigger = (ti_on_scene_prop_destroy,
  [
    (play_sound, "snd_dummy_destroyed"),
    
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),

      (store_trigger_param_1, ":instance_no"),
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
      
      (prop_instance_get_position, pos49, ":instance_no"),            
      
      (particle_system_burst, "psys_dummy_straw", pos49, 20),
      (particle_system_burst, "psys_dummy_smoke", pos49, 50),

      (call_script, "script_clean_up_prop_instance", ":instance_no"),
      
      (assign,":prop_to_spawn",-1),
      (try_begin),
        (eq,":prop_kind","spr_mm_stakes_destructible"),
        (assign,":prop_to_spawn","spr_mm_stakes_construct"),
      (else_try),
        (eq,":prop_kind","spr_mm_stakes2_destructible"),
        (assign,":prop_to_spawn","spr_mm_stakes2_construct"),
      (else_try),
        (eq,":prop_kind","spr_sandbags_destructible"),
        (assign,":prop_to_spawn","spr_sandbags_construct"),
      (else_try),
        (eq,":prop_kind","spr_chevaux_de_frise_tri_destructible"),
        (assign,":prop_to_spawn","spr_chevaux_de_frise_tri_construct"),
      (else_try),
        (eq,":prop_kind","spr_gabiondeploy_destructible"),
        (assign,":prop_to_spawn","spr_gabiondeploy_construct"),
      (else_try),
        (eq,":prop_kind","spr_mm_fence1"),
        (assign,":prop_to_spawn","spr_mm_fence1d"),  
      (try_end),
      
      (gt,":prop_to_spawn",-1),
      
      # Spawn destroyed prop
      (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 0, 0),
    (try_end),
  ])
  
check_common_construction_props_start_use_trigger = (ti_on_scene_prop_start_use,
  [
    (neg|multiplayer_is_dedicated_server),
    (store_trigger_param_1, ":agent_no"),
    #(store_trigger_param_2, ":instance_no"),
    
    (multiplayer_get_my_player,":my_player"),
    (player_get_agent_id,":my_agent_no",":my_player"),
    (eq,":my_agent_no",":agent_no"),
    (try_begin), #Not a sapper
      (agent_get_troop_id,":my_troop_no",":my_agent_no"),
      (troop_get_slot,":troop_class",":my_troop_no",slot_troop_class),
      (neq,":troop_class",multi_troop_class_mm_sapper),
      (str_store_string,s4,"@Only sappers can build structures!"),
      (assign,":colour_code",0xFF0000),
    (else_try), #Is sapper but doesn't have hammer
      (agent_get_wielded_item,":item_id",":my_agent_no",0),
      (neq,":item_id","itm_construction_hammer"),
      (neq,":item_id","itm_construction_hammer_alt"),
      (str_store_string,s4,"@You must equip the hammer to build structures!"),
      (assign,":colour_code",0xFF0000),
    (else_try), #Is sapper with a hammer - consturct enabled
      (eq,":item_id","itm_construction_hammer"),
      (str_store_string,s4,"@Starting construction!"),
      (assign,":colour_code",0xFFFFFF),
    (else_try), #Is sapper with a hammer - deconstruct enabled
      (eq,":item_id","itm_construction_hammer_alt"),
      (str_store_string,s4,"@Starting deconstruction!"),
      (assign,":colour_code",0xFFFFFF),
    (try_end),
    (display_message,s4,":colour_code"),
  ])

check_common_construction_props_use_trigger = (ti_on_scene_prop_use,
  [
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
     
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_no"),
     
      (agent_get_troop_id,":troop_id",":agent_id"),
      (troop_slot_eq,":troop_id",slot_troop_class,multi_troop_class_mm_sapper),
     
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
     
      (agent_get_wielded_item,":item_id",":agent_id",0),
      (try_begin),
        (eq,":item_id","itm_construction_hammer"), #Only constructable with hammer
        
        (prop_instance_get_position, pos49, ":instance_no"),  
        
        (call_script, "script_clean_up_prop_instance", ":instance_no"),

        (assign,":prop_to_spawn",-1),
        (try_begin),
          (eq,":prop_kind","spr_mm_palisadedd"),
          (assign,":prop_to_spawn","spr_mm_palisade"),
        (else_try),
          (eq,":prop_kind","spr_mm_constr_pontoon_short"),
          (assign,":prop_to_spawn","spr_mm_pontoon_bridge_short"),
        (else_try),
          (eq,":prop_kind","spr_mm_constr_pontoon_med"),
          (assign,":prop_to_spawn","spr_mm_pontoon_bridge_med"),
        (else_try),
          (eq,":prop_kind","spr_mm_constr_pontoon_long"),
          (assign,":prop_to_spawn","spr_mm_pontoon_bridge_long"),
        (else_try),
          (eq,":prop_kind","spr_mm_constr_watchtower"),
          (assign,":prop_to_spawn","spr_mm_watchtower"),
        (else_try),
          (eq,":prop_kind","spr_mm_stakes_construct"),
          (assign,":prop_to_spawn","spr_mm_stakes_destructible"),
        (else_try),
          (eq,":prop_kind","spr_mm_stakes2_construct"),
          (assign,":prop_to_spawn","spr_mm_stakes2_destructible"),
        (else_try),
          (eq,":prop_kind","spr_sandbags_construct"),
          (assign,":prop_to_spawn","spr_sandbags_destructible"),
        (else_try),
          (eq,":prop_kind","spr_chevaux_de_frise_tri_construct"),
          (assign,":prop_to_spawn","spr_chevaux_de_frise_tri_destructible"),
        (else_try),
          (eq,":prop_kind","spr_gabiondeploy_construct"),
          (assign,":prop_to_spawn","spr_gabiondeploy_destructible"),
        (else_try),
          (eq,":prop_kind","spr_mm_fence1d"),
          (assign,":prop_to_spawn","spr_mm_fence1"),
        (try_end),
        
        (gt,":prop_to_spawn",-1),
      
        (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 1, 0),
      (else_try),
        (eq,":item_id","itm_construction_hammer_alt"), #Deconstructable with alt hammer
       
        (store_add,":cost_index",construct_costs_offset,":prop_kind"),
        (val_sub,":cost_index",mm_construct_props_begin),
        (troop_get_slot,":prop_cost","trp_track_select_dummy",":cost_index"),
        (val_sub,":prop_cost",1), #Return prop cost -1 build points when deconstructing
        (agent_get_team,":team",":agent_id"),
        (try_begin),
          (eq,":team",0),
          (val_add,"$g_team_1_build_points",":prop_cost"),
        (else_try),
          (eq,":team",1),
          (val_add,"$g_team_2_build_points",":prop_cost"),
        (try_end),
        (call_script,"script_multiplayer_server_send_build_points"),
        
        (call_script, "script_clean_up_prop_instance", ":instance_no"),
      (try_end),
    (try_end),
  ])
  
check_common_constructable_prop_on_hit_trigger = (ti_on_scene_prop_hit,
  [
    (store_trigger_param_1, ":instance_no"),
    (store_trigger_param_2, ":damage"),
    
    (try_begin),
      (prop_instance_is_valid,":instance_no"),
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
      
      (set_trigger_result,0), #Don't deal any normal damage to the prop
     
      (scene_prop_get_hit_points, ":health", ":instance_no"),
      (scene_prop_get_slot,":max_health",":instance_no",scene_prop_slot_max_health),
      
      (set_fixed_point_multiplier, 1),
      (position_get_x, ":agent_id", pos2),
      (set_fixed_point_multiplier, 100),
      (agent_is_active,":agent_id"),
      (agent_is_alive, ":agent_id"),
      
      (assign,":hit_sound","snd_dummy_hit"),
      (assign,":hit_smoke","psys_dummy_smoke"),
      (assign,":hit_particles","psys_dummy_straw"),
      (assign,":hit_smoke_size",3),
      (assign,":hit_particles_size",10),
      (assign,":apply_dmg",1),
      (assign,":update_dmg",1),
      
      (agent_get_wielded_item,":item_id",":agent_id",0),
      (try_begin),
        (this_or_next|eq,":item_id","itm_sapper_axe_rus"),
        (this_or_next|eq,":item_id","itm_sapper_axe"),
        (this_or_next|eq,":item_id","itm_russian_peasant_axe"),
        (eq,":item_id","itm_russian_peasant_2handed_axe"),

        (neq,":prop_kind","spr_earthwork1_destructible"), # not for earth prop.
        
        (val_mul,":damage",2),
      (else_try),
        (eq,":item_id","itm_construction_hammer"), #Only constructable with hammer
        
        (agent_get_troop_id,":troop_id",":agent_id"),
        
        # we has a sappeur :3
        (troop_slot_eq,":troop_id",slot_troop_class,multi_troop_class_mm_sapper),
        
        (neq,":prop_kind","spr_earthwork1_destructible"), # not for earth prop.
        
        (assign,":hit_sound","snd_hammer"),
        (assign,":apply_dmg",0),

        (assign,":old_health",":health"),
        (val_add,":health",25), # 25 hitpoints per hit with hammer.
        (val_min,":health",":max_health"),
        
        (try_begin),
          (eq,":old_health",":health"),
          (assign,":update_dmg",0),
        (try_end),

        (try_begin),
          (ge,":health",":max_health"),
          
          (is_between,":prop_kind","spr_mm_palisadedd","spr_crate_explosive"), # a construction object
          
          (assign,":update_dmg",0),
          
          (this_or_next|multiplayer_is_server), # only on servers.
          (neg|game_in_multiplayer_mode),
       
          (prop_instance_get_position, pos49, ":instance_no"),
          
          (call_script, "script_clean_up_prop_instance", ":instance_no"),
          
          (call_script, "script_get_prop_kind_for_constr_kind", ":prop_kind"),
          (assign,":prop_to_spawn",reg0),
          (assign,":x_offset",reg1),
          (assign,":y_offset",reg2),
          (assign,":z_offset",reg3),
          (assign,":dont_rotate_to_ground",reg4),
          
          (gt,":prop_to_spawn",-1),
          
          (try_begin),
            (eq,":dont_rotate_to_ground",1),
            (init_position,pos37),
            (position_copy_origin,pos37,pos49),
            (position_get_rotation_around_z,":z_rot",pos49),
            (position_rotate_z,pos37,":z_rot"),
            (copy_position,pos49,pos37),
          (try_end),
          
          (position_move_x,pos49,":x_offset"),
          (position_move_y,pos49,":y_offset"),
          (position_move_z,pos49,":z_offset"),
          
          (try_begin),
            (eq,":dont_rotate_to_ground",1),
            (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 0, 0),
          (else_try),
            (call_script, "script_find_or_create_scene_prop_instance", ":prop_to_spawn", 0, 1, 0),
          (try_end),
          (assign,":new_instance_no",reg0),
          # init the new prop slots.
          (call_script,"script_multiplayer_server_initialise_destructable_prop_slots",":new_instance_no",":prop_to_spawn"),
        (try_end),
      (try_end),
     
      (try_begin), # with earth digs we have some specialll stuff.
        (eq,":prop_kind","spr_earthwork1_destructible"),
        
        (assign,":apply_dmg",0),
        
        (try_begin),
          (neq,":item_id","itm_shovel"),
          (neq,":item_id","itm_shovel_undig"),
          (assign,":hit_sound",-1),
          (assign,":hit_smoke",-1),
          (assign,":hit_particles",-1),
        (try_end),
        
        (this_or_next|eq,":item_id","itm_shovel"),
        (eq,":item_id","itm_shovel_undig"),
          
        (assign,":hit_sound","snd_shovel"),
        
        (call_script,"script_move_pioneer_ground",":instance_no",":item_id",":health",":max_health"),
        (assign,":health",reg0),
      (try_end),
      
      (try_begin), # not a pioneer
        (eq,":apply_dmg",1),
        (try_begin), # for construction objects hit by anyone else then pioneers dont do anything.
          (is_between,":prop_kind","spr_mm_palisadedd","spr_mm_stakes_construct"), # a construction object that is not placable by sapper.
          (assign,":hit_sound",-1),
          (assign,":hit_smoke",-1),
          (assign,":hit_particles",-1),
        (else_try), # else apply the damage. (that could mean destroying the placed stuff by sapper!)
          (scene_prop_set_slot,":instance_no",scene_prop_slot_last_hit_by,":agent_id"),
          (val_sub,":health",":damage"),
          (val_max,":health",0),
        (try_end),
      (try_end),
      
      (try_begin),
        (eq,":update_dmg",1),
        (this_or_next|multiplayer_is_server), # only on servers.
        (neg|game_in_multiplayer_mode),
        (scene_prop_set_cur_hit_points, ":instance_no", ":health"),
        (scene_prop_set_slot,":instance_no",scene_prop_slot_health,":health"),
      (try_end),
      
      (try_begin),
        (gt, ":health", 0),
        (try_begin),
          (gt,":hit_sound",-1),
          (play_sound, ":hit_sound"),
        (try_end),
      (else_try),
        (neg|multiplayer_is_server),
        (neq,":prop_kind","spr_earthwork1_destructible"),
        (play_sound, "snd_dummy_destroyed"),
      (try_end),

      (try_begin),
        (neg|multiplayer_is_dedicated_server),
        (try_begin),
          (gt,":hit_smoke",-1),
          (particle_system_burst_no_sync, ":hit_smoke", pos1, ":hit_smoke_size"),
        (try_end),
        
        (try_begin),
          (gt,":hit_particles",-1),
          (particle_system_burst_no_sync, ":hit_particles", pos1, ":hit_particles_size"),
        (try_end),
      (try_end),
    (try_end),
  ])

check_common_earth_on_hit_trigger = (ti_on_scene_prop_hit,
  [
    (set_trigger_result, 0), # do no damage
    
    (set_fixed_point_multiplier, 1),
    (position_get_x, ":agent_id", pos2),
    (ge, ":agent_id", 0),
    (agent_is_alive, ":agent_id"),
    (agent_get_wielded_item,":item_id",":agent_id",0),
    
    (this_or_next|eq,":item_id","itm_shovel"),
    (eq,":item_id","itm_shovel_undig"),
    
    (play_sound, "snd_shovel"),
  
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
      
      (store_trigger_param_1, ":instance_no"),
      (prop_instance_get_scene_prop_kind, ":prop_kind", ":instance_no"),
      
      
      (prop_instance_get_position,pos4,":instance_no"),
      
      (assign,":continue",1),
      
      (try_begin),
        (eq,":prop_kind","spr_mm_tunnel_wall"),
        
        (assign,":keep_searching",1),
        (try_for_prop_instances, ":cur_instance_id", "spr_mm_tunnel_wall", somt_object),
          (neq,":cur_instance_id",":instance_no"),
          (eq,":keep_searching",1),
          (prop_instance_get_position,pos3,":cur_instance_id"),
          (get_distance_between_positions,":distance",pos4,pos3),
          (lt,":distance",100),
    
          (particle_system_burst, "psys_dummy_smoke_big", pos4, 100),
          
          (position_move_z,pos4,-2000,1),
          (prop_instance_animate_to_position, ":instance_no", pos4, 0),
          (prop_instance_animate_to_position, ":cur_instance_id", pos4, 0),
          
          (assign,":keep_searching",0),
          (assign,":continue",0),
        (try_end),
        
        (position_move_y,pos4,-12,0),
      (else_try),
        (position_move_z,pos4,-12,0),
      (try_end),
      
      (eq,":continue",1),
      
      (prop_instance_animate_to_position, ":instance_no", pos4, 6),
      
      (particle_system_burst, "psys_dummy_smoke", pos1, 10),
    (try_end),
  ])
  
check_common_target_hit_trigger = (ti_on_scene_prop_hit,
  [
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
      
      (store_trigger_param_1, ":instance_no"),
      (set_fixed_point_multiplier, 1),
      (position_get_x, ":attacker_agent_id", pos2),
      (set_fixed_point_multiplier, 100),
      
      (agent_is_active,":attacker_agent_id"),
      
      (agent_get_wielded_item,":item_id",":attacker_agent_id",0),
        
      (item_slot_eq,":item_id",slot_item_multiplayer_item_class, multi_item_class_type_gun), #always use item classes!!!
      
      (prop_instance_get_position, pos2, ":instance_no"),
      (agent_get_position, pos3, ":attacker_agent_id"),
      (get_distance_between_positions, ":player_distance", pos3, pos2),
      (position_transform_position_to_local, pos4, pos2, pos1),
      (position_set_y, pos4, 0),
      (position_set_x, pos2, 0),
      (position_set_y, pos2, 0),
      (position_set_z, pos2, 0),
      (get_distance_between_positions, ":target_distance", pos4, pos2),
      (assign, ":point_earned", 43), #Calculating a point between 0-12
      (val_sub, ":point_earned", ":target_distance"),
      (val_mul, ":point_earned", 1299),
      (val_div, ":point_earned", 4300),
      (try_begin),
        (lt, ":point_earned", 0),
        (assign, ":point_earned", 0),
      (try_end),
      #(val_div, ":player_distance", 91), #Converting to yards
      (val_div, ":player_distance", 100), #Let's be international and use meters here (historically correct for France too since 1793...)
      (assign, reg60, ":point_earned"),
      (assign, reg61, ":player_distance"),
      
      (try_begin),
        (game_in_multiplayer_mode),
        
        (agent_get_player_id,":player_id",":attacker_agent_id"),
        (player_is_active,":player_id"),
        
        (multiplayer_send_string_to_player, ":player_id", multiplayer_event_show_server_message, "str_archery_target_hit"),
      (else_try),
        (neg|game_in_multiplayer_mode),
        (call_script, "script_client_get_my_agent"),
        (eq, ":attacker_agent_id", reg0), # Only for myself.
        
        (display_message, "str_archery_target_hit"),
        (try_begin),
          (gt,":point_earned",0),
          (eq,"$g_is_tutorial",1),
          (val_add,"$g_tutorial_target_hit",1),
        (try_end),
      (try_end),
    (try_end),
  ])
    
check_common_dummy_destroy_trigger = (ti_on_scene_prop_destroy,
  [
    (play_sound, "snd_dummy_destroyed"),
    
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
   
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_get_slot,":attacker_agent_id",":instance_no",scene_prop_slot_last_hit_by),
      
      (prop_instance_get_starting_position, pos1, ":instance_no"),
      
      (assign, ":rotate_side", 80),
      (try_begin),
        (agent_is_active,":attacker_agent_id"),
        (agent_get_position, pos2, ":attacker_agent_id"),
        (position_is_behind_position, pos2, pos1),
        (val_mul, ":rotate_side", -1),
      (try_end),
      (position_rotate_x, pos1, ":rotate_side"),
      (prop_instance_animate_to_position, ":instance_no", pos1, 70), #animate to position 1 in 0.7 second
        
      (try_begin),
        (neg|game_in_multiplayer_mode),
        (eq,"$g_is_tutorial",1),
        (val_add,"$g_tutorial_targets_destroyed",1),
      (try_end),
    (try_end),
  ])
    
check_common_dummy_on_hit_trigger = (ti_on_scene_prop_hit,
    [
      (play_sound, "snd_dummy_hit"),
      
      (try_begin),
        (this_or_next|multiplayer_is_server),
        (neg|game_in_multiplayer_mode),
        
        (store_trigger_param_1, ":instance_no"),
        (store_trigger_param_2, ":damage"),
        (set_fixed_point_multiplier, 1),
        (position_get_x, ":attacker_agent_id", pos2),
        (set_fixed_point_multiplier, 100),
        
        (scene_prop_set_slot,":instance_no",scene_prop_slot_last_hit_by,":attacker_agent_id"),
      
        (assign, reg60, ":damage"),
        (val_div, ":damage", 8),
        (prop_instance_get_position, pos2, ":instance_no"),

        (try_begin),
          (agent_is_active,":attacker_agent_id"),
          (agent_get_position, pos3, ":attacker_agent_id"),
          (position_is_behind_position, pos3, pos2),
          (val_mul, ":damage", -1),
        (try_end),
        (position_rotate_x, pos2, ":damage"),
        
        (try_begin),
          (game_in_multiplayer_mode),
          
          (agent_get_player_id,":player_id",":attacker_agent_id"),
          (player_is_active,":player_id"),
          
          (multiplayer_send_string_to_player, ":player_id", multiplayer_event_show_server_message, "str_delivered_damage"),
        (else_try),
          (neg|game_in_multiplayer_mode),
          (call_script, "script_client_get_my_agent"),
          (eq, ":attacker_agent_id", reg0), # Only for myself.
          (display_message, "str_delivered_damage"),
        (try_end),

        (prop_instance_animate_to_position, ":instance_no", pos2, 30), #animate to position 2 in 0.3 second
        
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
      (try_end),
    ])

check_common_explosive_crate_use_trigger = (ti_on_scene_prop_use,
  [
    (store_trigger_param_1, ":agent_id"),
    (store_trigger_param_2, ":instance_id"),
    
    (try_begin),
      (this_or_next|multiplayer_is_server),
      (neg|game_in_multiplayer_mode),
      
      (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
      (le,":cur_time",0),
      (scene_prop_set_slot,":instance_id", scene_prop_slot_time, 5), #Seconds until exploding
      (scene_prop_set_slot,":instance_id", scene_prop_slot_user_agent, ":agent_id"), #User agent
      
      (scene_prop_enable_after_time, ":instance_id", 500),
      
      (prop_instance_get_position,pos56,":instance_id"),
      (call_script,"script_multiplayer_server_play_sound_at_position","snd_crate_fuse"),
    (try_end),
  ])
    
  
scene_props = [
  ("invalid_object",0,"question_mark","0", []),
  ("inventory",sokf_type_container|sokf_place_at_origin,"0","bobaggage", []),
  ("empty", 0, "0", "0", []),
  ("chest_a",sokf_type_container,"chest_gothic","bochest_gothic", []),
  ("container_small_chest",sokf_type_container,"0","bobaggage", []),
  ("container_chest_b",sokf_type_container,"chest_b","bo_chest_b", []),
  ("container_chest_c",sokf_type_container,"chest_c","bo_chest_c", []),
  ("player_chest",sokf_type_container,"player_chest","bo_player_chest", []),
  ("locked_player_chest",0,"player_chest","bo_player_chest", []),

  ("light_sun",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
       (neg|multiplayer_is_dedicated_server),
          (neg|is_currently_night),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_time_of_day,reg(12)),
          (try_begin),
            (is_between,reg(12),5,20),
            (store_mul, ":red", 5 * 200, ":scale"),
            (store_mul, ":green", 5 * 193, ":scale"),
            (store_mul, ":blue", 5 * 180, ":scale"),
          (else_try),
            (store_mul, ":red", 5 * 90, ":scale"),
            (store_mul, ":green", 5 * 115, ":scale"),
            (store_mul, ":blue", 5 * 150, ":scale"),
          (try_end),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 0, 0),
      ]),
    ]),
  ("light",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
      (neg|multiplayer_is_dedicated_server),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 200, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 45, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 10, 30),
      ]),
    ]),
  ("light_red",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
      (neg|multiplayer_is_dedicated_server),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 2 * 170, ":scale"),
          (store_mul, ":green", 2 * 100, ":scale"),
          (store_mul, ":blue", 2 * 30, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 20, 30),
      ]),
    ]),
  ("light_night",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
      (neg|multiplayer_is_dedicated_server),
#          (store_time_of_day,reg(12)),
#          (neg|is_between,reg(12),5,20),
          (is_currently_night, 0),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 160, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 100, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 10, 30),
      ]),
    ]),
  ("torch",0,"torch_a","0",
   [
   (ti_on_init_scene_prop,
    [
    (neg|multiplayer_is_dedicated_server),
        (set_position_delta,0,-35,48),
        (particle_system_add_new, "psys_torch_fire"),
        (particle_system_add_new, "psys_torch_smoke"),
        (particle_system_add_new, "psys_torch_fire_sparks"),

       # (play_sound, "snd_torch_loop", 0),
        
        (set_position_delta,0,-35,56),
        (particle_system_add_new, "psys_fire_glow_1"),
#        (particle_system_emit, "psys_fire_glow_1",9000000),

#second method        
        (get_trigger_object_position, pos2),
        (set_position_delta,0,0,0),
        (position_move_y, pos2, -35),

        (position_move_z, pos2, 55),
        (particle_system_burst, "psys_fire_glow_fixed", pos2, 1),
    ]),
   ]),
  ("torch_night",0,"torch_a","0",
   [
   (ti_on_init_scene_prop,
    [
    (neg|multiplayer_is_dedicated_server),
#        (store_time_of_day,reg(12)),
#        (neg|is_between,reg(12),5,20),
        (is_currently_night, 0),
        (set_position_delta,0,-35,48),
        (particle_system_add_new, "psys_torch_fire"),
        (particle_system_add_new, "psys_torch_smoke"),
        (particle_system_add_new, "psys_torch_fire_sparks"),
        (set_position_delta,0,-35,56),
        (particle_system_add_new, "psys_fire_glow_1"),
        (particle_system_emit, "psys_fire_glow_1",9000000),
     #   (play_sound, "snd_torch_loop", 0),
    ]),
   ]),
#  ("Baggage",sokf_place_at_origin|sokf_entity_body,"package","bobaggage"),
  ("barrier_20m",sokf_invisible|sokf_type_barrier,"barrier_20m","bo_barrier_20m", []),
  ("barrier_16m",sokf_invisible|sokf_type_barrier,"barrier_16m","bo_barrier_16m", []),
  ("barrier_8m" ,sokf_invisible|sokf_type_barrier,"barrier_8m" ,"bo_barrier_8m" , []),
  ("barrier_4m" ,sokf_invisible|sokf_type_barrier,"barrier_4m" ,"bo_barrier_4m" , []),
  ("barrier_2m" ,sokf_invisible|sokf_type_barrier,"barrier_2m" ,"bo_barrier_2m" , []),
  
  ("exit_4m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_4m" ,"bo_barrier_4m" , []),
  ("exit_8m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_8m" ,"bo_barrier_8m" , []),
  ("exit_16m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_16m" ,"bo_barrier_16m" , []),

  ("ai_limiter_2m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_2m" ,"bo_barrier_2m" , []),
  ("ai_limiter_4m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_4m" ,"bo_barrier_4m" , []),
  ("ai_limiter_8m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_8m" ,"bo_barrier_8m" , []),
  ("ai_limiter_16m",sokf_invisible|sokf_type_ai_limiter,"barrier_16m","bo_barrier_16m", []),
  ("Shield",sokf_dynamic,"0","boshield", []),
  ("shelves",0,"shelves","boshelves", []),
  ("table_tavern",0,"table_tavern","botable_tavern", []),
  ("table_castle_a",0,"table_castle_a","bo_table_castle_a", []),
  ("chair_castle_a",0,"chair_castle_a","bo_chair_castle_a", []),

  ("pillow_a",0,"pillow_a","bo_pillow", []),
  ("pillow_b",0,"pillow_b","bo_pillow", []),
  ("pillow_c",0,"pillow_c","0", []),


  ("carpet_with_pillows_a",0,"carpet_with_pillows_a","bo_carpet_with_pillows", []),
  ("carpet_with_pillows_b",0,"carpet_with_pillows_b","bo_carpet_with_pillows", []),
  ("table_round_a",0,"table_round_a","bo_table_round_a", []),
  ("table_round_b",0,"table_round_b","bo_table_round_b", []),
  ("fireplace_b",0,"fireplace_b","bo_fireplace_b", []),
  ("fireplace_c",0,"fireplace_c","bo_fireplace_c", []),

  ("sofa_a",0,"sofa_a","bo_sofa", []),
  ("sofa_b",0,"sofa_b","bo_sofa", []),
  ("ewer_a",0,"ewer_a","bo_ewer_a", []),
  ("end_table_a",0,"end_table_a","bo_end_table_a", []),

  ("boat_destroy",0,"boat_destroy","bo_boat_destroy", []),
  ("destroy_house_a",0,"destroy_house_a","bo_destroy_house_a", []),
  ("destroy_house_b",0,"destroy_house_b","bo_destroy_house_b", []),
  ("destroy_house_c",0,"destroy_house_c","bo_destroy_house_c", []),
  ("destroy_heap",0,"destroy_heap","bo_destroy_heap", []),
  ("destroy_castle_a",0,"destroy_castle_a","bo_destroy_castle_a", []),
  ("destroy_castle_b",0,"destroy_castle_b","bo_destroy_castle_b", []),
  
  ("destroy_castle_c",0,"destroy_castle_c","bo_destroy_castle_c", []),
  
  ("destroy_castle_d",0,"destroy_castle_d","bo_destroy_castle_d", []),
  ("destroy_windmill",0,"destroy_windmill","bo_destroy_windmill", []),
   
  ("destroy_bridge_a",0,"destroy_bridge_a","bo_destroy_bridge_a", []),  
  ("destroy_bridge_b",0,"destroy_bridge_b","bo_destroy_bridge_b", []),    
  
  ("broom",0,"broom","0", []),
  ("garlic",0,"garlic","0", []),
  ("garlic_b",0,"garlic_b","0", []),

  ("destroy_a",0,"destroy_a","0", []),
  ("destroy_b",0,"destroy_b","0", []),



  ("bridge_wooden",0,"bridge_wooden","bo_bridge_wooden", []),
  ("bridge_wooden_snowy",0,"bridge_wooden_snowy","bo_bridge_wooden", []),
  
  ("grave_a",0,"grave_a","bo_grave_a", []),

  
  ("village_house_e",0,"village_house_e","bo_village_house_e", []),
  ("village_house_f",0,"village_house_f","bo_village_house_f", []),
  
 

  ("village_snowy_house_a",0,"village_snowy_house_a","bo_village_snowy_house_a", []),  
  ("village_snowy_house_b",0,"village_snowy_house_b","bo_village_snowy_house_b", []),
  ("village_snowy_house_c",0,"village_snowy_house_c","bo_village_snowy_house_c", []),
  ("village_snowy_house_d",0,"village_snowy_house_d","bo_village_snowy_house_d", []),
  ("village_snowy_house_e",0,"village_snowy_house_e","bo_village_snowy_house_e", []),
  ("village_snowy_house_f",0,"village_snowy_house_f","bo_village_snowy_house_f", []),

  ("carpet_a",0,"carpet_a","0", []),
  ("carpet_b",0,"carpet_b","0", []),
  ("carpet_c",0,"carpet_c","0", []),
  ("carpet_d",0,"carpet_d","0", []),
  ("carpet_e",0,"carpet_e","0", []),
  ("carpet_f",0,"carpet_f","0", []),

  ("awning_a",0,"awning_a","bo_awning", []),
  ("awning_b",0,"awning_b","bo_awning", []),
  ("awning_c",0,"awning_c","bo_awning", []),
  ("awning_long",0,"awning_long","bo_awning_long", []),
  ("awning_long_b",0,"awning_long_b","bo_awning_long", []),
  ("awning_d",0,"awning_d","bo_awning_d", []),


  ("mm_frigate",sokf_static_movement,"frigate","bo_frigate", []),
  
  ("ship",0,"ship","bo_ship", []),

  ("ship_b",0,"ship_b","bo_ship_b", []),
  ("ship_c",0,"ship_c","bo_ship_c", []),



  ("ship_d",0,"ship_d","bo_ship_d", []),

  ("snowy_barrel_a",0,"snowy_barrel_a","bo_snowy_barrel_a", []),
  ("snowy_fence",0,"snowy_fence","bo_snowy_fence", []),
  ("snowy_wood_heap",0,"snowy_wood_heap","bo_snowy_wood_heap", []),

  ("village_snowy_stable_a",0,"village_snowy_stable_a","bo_village_snowy_stable_a", []),


  ("village_straw_house_a",0,"village_straw_house_a","bo_village_straw_house_a", []),
  ("village_stable_a",0,"village_stable_a","bo_village_stable_a", []),
  ("village_shed_a",0,"village_shed_a","bo_village_shed_a", []),


  ("dungeon_door_cell_a",0,"dungeon_door_cell_a","bo_dungeon_door_cell_a", []),
  ("dungeon_door_cell_b",0,"dungeon_door_cell_b","bo_dungeon_door_cell_b", []),
  ("dungeon_door_entry_a",0,"dungeon_door_entry_a","bo_dungeon_door_entry_a", []),
  ("dungeon_door_entry_b",0,"dungeon_door_entry_b","bo_dungeon_door_entry_a", []),
  ("dungeon_door_entry_c",0,"dungeon_door_entry_c","bo_dungeon_door_entry_a", []),
  ("dungeon_door_stairs_a",0,"dungeon_door_stairs_a","bo_dungeon_door_stairs_a", []),
  ("dungeon_door_stairs_b",0,"dungeon_door_stairs_b","bo_dungeon_door_stairs_a", []),
  ("dungeon_bed_a",0,"dungeon_bed_a","0", []),
  ("dungeon_bed_b",0,"dungeon_bed_b","bo_dungeon_bed_b", []),
  ("torture_tool_a",0,"torture_tool_a","bo_torture_tool_a", []),
  ("torture_tool_b",0,"torture_tool_b","0", []),
  ("torture_tool_c",0,"torture_tool_c","bo_torture_tool_c", []),
  ("skeleton_head",0,"skeleton_head","0", []),
  ("skeleton_bone",0,"skeleton_bone","0", []),
  ("skeleton_a",0,"skeleton_a","bo_skeleton_a", []),
  ("dungeon_cell_c",0,"dungeon_cell_c","bo_dungeon_cell_c", []),
  ("salt_a",0,"salt_a","bo_salt_a", []),

  ("tutorial_door_a",sokf_static_movement,"tutorial_door_a","bo_tutorial_door_a", []),

  ("tutorial_door_b",sokf_static_movement,"tutorial_door_b","bo_tutorial_door_b", []),

  ("arena_archery_target_a",0,"arena_archery_target_a","bo_arena_archery_target_a", []),
  ("archery_butt_a",0,"archery_butt","bo_archery_butt", [check_common_target_hit_trigger,]),
  ("archery_target_with_hit_a",0,"arena_archery_target_a","bo_arena_archery_target_a", [check_common_target_hit_trigger,]),
  ("dummy_a",sokf_destructible|sokf_static_movement,"arena_archery_target_b","bo_arena_archery_target_b",   [
   check_common_dummy_destroy_trigger,
   check_common_dummy_on_hit_trigger,
  ]),

  ("band_a",0,"band_a","0", []),

  ("castle_h_stairs_a",sokf_type_ladder,"castle_h_stairs_a","bo_castle_h_stairs_a", []),
  ("castle_h_stairs_b",0,"castle_h_stairs_b","bo_castle_h_stairs_b", []),
  
  ("castle_f_doors_top_a",0,"castle_f_doors_top_a","bo_castle_f_doors_top_a", []),
  
  ("castle_f_stairs_a",sokf_type_ladder,"castle_f_stairs_a","bo_castle_f_stairs_a", []),
  ("castle_f_wall_stairs_a",sokf_type_ladder,"castle_f_wall_stairs_a","bo_castle_f_wall_stairs_a", []),
  ("castle_f_wall_stairs_b",sokf_type_ladder,"castle_f_wall_stairs_b","bo_castle_f_wall_stairs_b", []),
  ("castle_f_wall_way_a",0,"castle_f_wall_way_a","bo_castle_f_wall_way_a", []),
  ("castle_f_wall_way_b",0,"castle_f_wall_way_b","bo_castle_f_wall_way_b", []),
  
  ("castle_g_gate_house_door_a",0,"castle_g_gate_house_door_a","bo_castle_g_gate_house_door_a", []),
  ("castle_g_gate_house_door_b",0,"castle_g_gate_house_door_b","bo_castle_g_gate_house_door_b", []),
 
  ("banner_pole", sokf_static_movement, "banner_pole", "bo_banner_pole", []),


  ("banner_kingdom_a", 0, "banner2", "0", []),
  ("banner_kingdom_b", 0, "banner5", "0", []),
  ("banner_kingdom_c", 0, "banner3", "0", []),
  ("banner_kingdom_d", 0, "banner1", "0", []),
  ("banner_kingdom_e", 0, "banner75", "0", []),
  ("banner_kingdom_f", 0, "banner4", "0", []),

  ("tavern_chair_a",0,"tavern_chair_a","bo_tavern_chair_a", []),
  ("tavern_chair_b",0,"tavern_chair_b","bo_tavern_chair_b", []),
  ("tavern_table_a",0,"tavern_table_a","bo_tavern_table_a", []),
  ("tavern_table_b",0,"tavern_table_b","bo_tavern_table_b", []),
  ("fireplace_a",0,"fireplace_a","bo_fireplace_a", []),
  ("barrel",0,"barrel","bobarrel", []),
  ("bench_tavern",0,"bench_tavern","bobench_tavern", []),
  ("bench_tavern_b",0,"bench_tavern_b","bo_bench_tavern_b", []),
  ("bowl_wood",0,"bowl_wood","0", []),
  ("chandelier_table",0,"chandelier_table","0", []),
  ("chandelier_tavern",0,"chandelier_tavern","0", []),
  ("chest_gothic",0,"chest_gothic","bochest_gothic", []),
  ("chest_b",0,"chest_b","bo_chest_b", []),
  ("chest_c",0,"chest_c","bo_chest_c", []),
  ("counter_tavern",0,"counter_tavern","bocounter_tavern", []),
  ("cup",0,"cup","0", []),
  ("dish_metal",0,"dish_metal","0", []),
  ("gothic_chair",0,"gothic_chair","bogothic_chair", []),
  ("gothic_stool",0,"gothic_stool","bogothic_stool", []),
  ("grate",0,"grate","bograte", []),
  ("jug",0,"jug","0", []),
  ("potlamp",0,"potlamp","0", []),
  ("weapon_rack",0,"weapon_rack","boweapon_rack", []),
  ("weapon_rack_big",0,"weapon_rack_big","boweapon_rack_big", []),
  ("tavern_barrel",0,"barrel","bobarrel", []),
  ("tavern_barrel_b",0,"tavern_barrel_b","bo_tavern_barrel_b", []),
  ("merchant_sign",0,"merchant_sign","bo_tavern_sign", []),
  ("tavern_sign",0,"tavern_sign","bo_tavern_sign", []),
  ("sack",0,"sack","0", []),
  
  ("cupboard_a",0,"cupboard_a","bo_cupboard_a", []),
  ("box_a",0,"box_a","bo_box_a", []),
  ("bucket_a",0,"bucket_a","bo_bucket_a", []),
  ("straw_a",0,"straw_a","0", []),
  ("straw_b",0,"straw_b","0", []),
  ("straw_c",0,"straw_c","0", []),
  ("cloth_a",0,"cloth_a","0", []),
  ("cloth_b",0,"cloth_b","0", []),
  ("mat_a",0,"mat_a","0", []),
  ("mat_b",0,"mat_b","0", []),
  ("mat_c",0,"mat_c","0", []),
  ("mat_d",0,"mat_d","0", []),

  ("wood_a",0,"wood_a","bo_wood_a", []),
  ("wood_b",0,"wood_b","bo_wood_b", []),
  ("wood_heap",0,"wood_heap_a","bo_wood_heap_a", []),
  ("wood_heap_b",0,"wood_heap_b","bo_wood_heap_b", []),
  ("water_well_a",0,"water_well_a","bo_water_well_a", []),
  ("net_a",0,"net_a","bo_net_a", []),
  ("net_b",0,"net_b","0", []),

  ("meat_hook",0,"meat_hook","0", []),
  ("cooking_pole",0,"cooking_pole","0", []),
  ("bowl_a",0,"bowl_a","0", []),
  ("bucket_b",0,"bucket_b","0", []),
  ("washtub_a",0,"washtub_a","bo_washtub_a", []),
  ("washtub_b",0,"washtub_b","bo_washtub_b", []),

  ("table_trunk_a",0,"table_trunk_a","bo_table_trunk_a", []),
  ("chair_trunk_a",0,"chair_trunk_a","bo_chair_trunk_a", []),
  ("chair_trunk_b",0,"chair_trunk_b","bo_chair_trunk_b", []),
  ("chair_trunk_c",0,"chair_trunk_c","bo_chair_trunk_c", []),

  ("table_trestle_long",0,"table_trestle_long","bo_table_trestle_long", []),
  ("table_trestle_small",0,"table_trestle_small","bo_table_trestle_small", []),
  ("chair_trestle",0,"chair_trestle","bo_chair_trestle", []),

  ("wheel",0,"wheel","bo_wheel", []),
  ("ladder",sokf_type_ladder,"ladder","boladder", []),
  ("cart",0,"cart","bo_cart", []),
  ("village_stand",0,"village_stand","bovillage_stand", []),
  ("wooden_stand",0,"wooden_stand","bowooden_stand", []),
  ("table_small",0,"table_small","bo_table_small", []),
  ("table_small_b",0,"table_small_b","bo_table_small_b", []),
  
  ("stone_stairs_a",sokf_type_ladder,"stone_stairs_a","bo_stone_stairs_a", []),
  ("stone_stairs_b",sokf_type_ladder,"stone_stairs_b","bo_stone_stairs_b", []),
  ("railing_a",0,"railing_a","bo_railing_a", []),
  

  ("small_wall_a",0,"small_wall_a","bo_small_wall_a", []),
  ("small_wall_b",0,"small_wall_b","bo_small_wall_b", []),
  ("small_wall_c",0,"small_wall_c","bo_small_wall_c", []),
  ("small_wall_c_destroy",0,"small_wall_c_destroy","bo_small_wall_c_destroy", []),
  ("small_wall_d",0,"small_wall_d","bo_small_wall_d", []),
  ("small_wall_e",0,"small_wall_e","bo_small_wall_d", []),
  ("small_wall_f",0,"small_wall_f","bo_small_wall_f", []),
  ("small_wall_f2",0,"small_wall_f2","bo_small_wall_f2", []),
 
  ("passage_house_a",0,"passage_house_a","bo_passage_house_a", []),
  ("passage_house_b",0,"passage_house_b","bo_passage_house_b", []),
  ("passage_house_c",0,"passage_house_c","bo_passage_house_c", []),
  ("passage_house_d",0,"passage_house_d","bo_passage_house_d", []),
  ("passage_house_c_door",0,"passage_house_c_door","bo_passage_house_c_door", []),

  ("house_roof_door",0,"house_roof_door","bo_house_roof_door", []),

  ("stairs_arch_a",sokf_type_ladder,"stairs_arch_a","bo_stairs_arch_a", []),

  
  ("windmill",0,"windmill","bo_windmill", []),
  ("windmill_fan",0,"windmill_fan","bo_windmill_fan", []),
 


  ("earth_wall_a",0,"earth_wall_a","bo_earth_wall_a", []),
  ("earth_wall_a2",0,"earth_wall_a2","bo_earth_wall_a2", []),
  ("earth_wall_b",0,"earth_wall_b","bo_earth_wall_b", []),
  ("earth_wall_b2",0,"earth_wall_b2","bo_earth_wall_b2", []),
  ("earth_stairs_a",sokf_type_ladder,"earth_stairs_a","bo_earth_stairs_a", []),
  ("earth_stairs_b",sokf_type_ladder,"earth_stairs_b","bo_earth_stairs_b", []),
  ("earth_tower_small_a",0,"earth_tower_small_a","bo_earth_tower_small_a", []),
  ("earth_gate_house_a",0,"earth_gate_house_a","bo_earth_gate_house_a", []),
  ("earth_gate_a",0,"earth_gate_a","bo_earth_gate_a", []),

  ("earth_house_a",0,"earth_house_a","bo_earth_house_a", []),
  ("earth_house_b",0,"earth_house_b","bo_earth_house_b", []),
  ("earth_house_c",0,"earth_house_c","bo_earth_house_c", []),
  ("earth_house_d",0,"earth_house_d","bo_earth_house_d", []),

  

  
  
  
  ("snowy_wall_a",0,"snowy_wall_a","bo_snowy_wall_a", []),

  ("snowy_stand",0,"snowy_stand","bo_snowy_stand", []),

  ("snowy_heap_a",0,"snowy_heap_a","bo_snowy_heap_a", []),
  ("snowy_trunks_a",0,"snowy_trunks_a","bo_snowy_trunks_a", []),

  ("square_stairs_a",0,"square_stairs_a","bo_square_stairs_a", []),

  ("castle_e_stairs_a",0,"castle_e_stairs_a","bo_castle_e_stairs_a", []),
  ("stand_thatched",0,"stand_thatched","bo_stand_thatched", []),
  ("stand_cloth",0,"stand_cloth","bo_stand_cloth", []),

  ("castle_stairs_a",sokf_type_ladder,"castle_stairs_a","bo_castle_stairs_a", []),

  ("castle_drawbridge_open",0,"castle_drawbridges_open","bo_castle_drawbridges_open", []),
  ("castle_drawbridge_closed",0,"castle_drawbridges_closed","bo_castle_drawbridges_closed", []),
  ("spike_group_a",0,"spike_group_a","bo_spike_group_a", []),
  ("spike_a",0,"spike_a","bo_spike_a", []),

  ("stone_ball",0,"stone_ball","0", []),

 
  ("crude_fence",0,"fence","bo_fence", []),
  ("crude_fence_small",0,"crude_fence_small","bo_crude_fence_small", []),
  ("crude_fence_small_b",0,"crude_fence_small_b","bo_crude_fence_small_b", []),
  
  ("ramp_12m",0,"ramp_12m","bo_ramp_12m", []),
  ("ramp_14m",0,"ramp_14m","bo_ramp_14m", []),

  ("siege_ladder_6m",sokf_type_ladder,"siege_ladder_move_6m","bo_siege_ladder_move_6m", []), 
  ("siege_ladder_8m",sokf_type_ladder,"siege_ladder_move_8m","bo_siege_ladder_move_8m", []),
  ("siege_ladder_10m",sokf_type_ladder,"siege_ladder_move_10m","bo_siege_ladder_move_10m", []),
  ("siege_ladder_12m",sokf_type_ladder,"siege_ladder_12m","bo_siege_ladder_12m", []),
  ("siege_ladder_14m",sokf_type_ladder,"siege_ladder_14m","bo_siege_ladder_14m", []),

  ("siege_ladder_move_6m",sokf_type_ladder|sokf_static_movement|spr_use_time(2),"siege_ladder_move_6m","bo_siege_ladder_move_6m", [    
   check_item_use_trigger,
   check_ladder_animate_trigger,
   check_ladder_animation_finish_trigger,
  ]),  

  ("siege_ladder_move_8m",sokf_type_ladder|sokf_static_movement|spr_use_time(2),"siege_ladder_move_8m","bo_siege_ladder_move_8m", [    
   check_item_use_trigger,
   check_ladder_animate_trigger,
   check_ladder_animation_finish_trigger,
  ]),  

  ("siege_ladder_move_10m",sokf_type_ladder|sokf_static_movement|spr_use_time(3),"siege_ladder_move_10m","bo_siege_ladder_move_10m", [    
   check_item_use_trigger,
   check_ladder_animate_trigger,
   check_ladder_animation_finish_trigger,
  ]),  

  ("siege_ladder_move_12m",sokf_type_ladder|sokf_static_movement|spr_use_time(3),"siege_ladder_move_12m","bo_siege_ladder_move_12m", [    
   check_item_use_trigger,
   check_ladder_animate_trigger,
   check_ladder_animation_finish_trigger,
  ]),  

  ("siege_ladder_move_14m",sokf_type_ladder|sokf_static_movement|spr_use_time(4),"siege_ladder_move_14m","bo_siege_ladder_move_14m", [    
   check_item_use_trigger,
   check_ladder_animate_trigger,
   check_ladder_animation_finish_trigger,
  ]),  

  ("portcullis",sokf_static_movement,"portcullis_a","bo_portcullis_a", []),
  ("bed_a",0,"bed_a","bo_bed_a", []),
  ("bed_b",0,"bed_b","bo_bed_b", []),
  ("bed_c",0,"bed_c","bo_bed_c", []),
  ("bed_d",0,"bed_d","bo_bed_d", []),
  ("bed_e",0,"bed_e","bo_bed_e", []),

  ("bed_f",0,"bed_f","bo_bed_f", []),

  ("towngate_door_left",0,"door_g_left","bo_door_left", []),
  ("towngate_door_right",0,"door_g_right","bo_door_right", []),
  ("towngate_rectangle_door_left",0,"towngate_rectangle_door_left","bo_towngate_rectangle_door_left", []),
  ("towngate_rectangle_door_right",0,"towngate_rectangle_door_right","bo_towngate_rectangle_door_right", []),
  
  ("door_screen",0,"door_screen","0", []),
  ("door_a",0,"door_a","bo_door_a", []),
  ("door_b",0,"door_b","bo_door_a", []),
  ("door_c",0,"door_c","bo_door_a", []),
  ("door_d",0,"door_d","bo_door_a", []),
  ("tavern_door_a",0,"tavern_door_a","bo_tavern_door_a", []),
  ("tavern_door_b",0,"tavern_door_b","bo_tavern_door_a", []),
  ("door_e_left",0,"door_e_left","bo_door_left", []),
  ("door_e_right",0,"door_e_right","bo_door_right", []),
  ("door_f_left",0,"door_f_left","bo_door_left", []),
  ("door_f_right",0,"door_f_right","bo_door_right", []),
  ("door_h_left",0,"door_g_left","bo_door_left", []),
  ("door_h_right",0,"door_g_right","bo_door_right", []),
  ("draw_bridge_a",0,"draw_bridge_a","bo_draw_bridge_a", []),
  ("chain_1m",0,"chain_1m","0", []),
  ("chain_2m",0,"chain_2m","0", []),
  ("chain_5m",0,"chain_5m","0", []),
  ("chain_10m",0,"chain_10m","0", []),
  ("bridge_modular_a",0,"bridge_modular_a","bo_bridge_modular_a", []),
  ("bridge_modular_b",0,"bridge_modular_b","bo_bridge_modular_b", []),
  ("church_a",0,"church_a","bo_church_a", []),
  ("church_tower_a",0,"church_tower_a","bo_church_tower_a", []),
  ("stone_step_a",0,"floor_stone_a","bo_floor_stone_a", []),
  ("stone_step_b",0,"stone_step_b","0", []),
  ("stone_step_c",0,"stone_step_c","0", []),
  ("stone_heap",0,"stone_heap","bo_stone_heap", []),
  ("stone_heap_b",0,"stone_heap_b","bo_stone_heap", []),

  ("panel_door_a",0,"house_door_a","bo_house_door_a", []),
  ("panel_door_b",0,"house_door_b","bo_house_door_a", []),
  ("smoke_stain",0,"soot_a","0", []),
  ("brazier_with_fire",0,"brazier","bo_brazier",    [
   (ti_on_scene_prop_init,
    [ 
        (neg|multiplayer_is_dedicated_server),
        (set_position_delta,0,0,85),
        (particle_system_add_new, "psys_brazier_fire_1"),
        (particle_system_add_new, "psys_fire_sparks_1"),

        (set_position_delta,0,0,100),
        (particle_system_add_new, "psys_fire_glow_1"),
        (particle_system_emit, "psys_fire_glow_1",9000000),
    ]),
   ]),

  ("cooking_fire",0,"fire_floor","0",
   [
   (ti_on_scene_prop_init,
    [
        (neg|multiplayer_is_dedicated_server),
        (set_position_delta,0,0,12),
        (particle_system_add_new, "psys_cooking_fire_1"),
        (particle_system_add_new, "psys_fire_sparks_1"),
        (particle_system_add_new, "psys_cooking_smoke"),
        (set_position_delta,0,0,50),
        (particle_system_add_new, "psys_fire_glow_1"),
        (particle_system_emit, "psys_fire_glow_1",9000000),
    ]),
   ]),
  ("cauldron_a",0,"cauldron_a","bo_cauldron_a", []),
  ("fry_pan_a",0,"fry_pan_a","0", []),
  ("tripod_cauldron_a",0,"tripod_cauldron_a","bo_tripod_cauldron_a", []),
  ("tripod_cauldron_b",0,"tripod_cauldron_b","bo_tripod_cauldron_b", []),
  ("open_stable_a",0,"open_stable_a","bo_open_stable_a", []),
  ("open_stable_b",0,"open_stable_b","bo_open_stable_b", []),
  ("plate_a",0,"plate_a","0", []),
  ("plate_b",0,"plate_b","0", []),
  ("plate_c",0,"plate_c","0", []),
  ("lettuce",0,"lettuce","0", []),
  ("hanger",0,"hanger","0", []),
  ("knife_eating",0,"knife_eating","0", []),
  ("colander",0,"colander","0", []),
  ("ladle",0,"ladle","0", []),
  ("spoon",0,"spoon","0", []),
  ("skewer",0,"skewer","0", []),
  ("grape_a",0,"grape_a","0", []),
  ("grape_b",0,"grape_b","0", []),
  ("apple_a",0,"apple_a","0", []),
  ("apple_b",0,"apple_b","0", []),
  ("maize_a",0,"maize_a","0", []),
  ("maize_b",0,"maize_b","0", []),
  ("cabbage",0,"cabbage","0", []),
  ("flax_bundle",0,"raw_flax","0",[]),
  ("olive_plane",0,"olive_plane","0",[]),
  ("grapes_plane",0,"grapes_plane","0",[]),
  ("date_fruit_plane",0,"date_fruit_plane","0",[]),
  ("bowl",0,"bowl_big","0",[]),
  ("bowl_small",0,"bowl_small","0",[]),
  ("dye_blue",0,"raw_dye_blue","0",[]),
  ("dye_red",0,"raw_dye_red","0",[]),
  ("dye_yellow",0,"raw_dye_yellow","0",[]),
  ("basket",0,"basket_small","0",[]),
  ("basket_big",0,"basket_large","0",[]),
  ("basket_big_green",0,"basket_big","0",[]),
  ("leatherwork_frame",0,"leatherwork_frame","0", []),

  ("cabbage_b",0,"cabbage_b","0", []),
  ("bean",0,"bean","0", []),
  ("basket_a",0,"basket_a","bo_basket_a", []),
  ("feeding_trough_a",0,"feeding_trough_a","bo_feeding_trough_a", []),


  ("marrow_a",0,"marrow_a","0", []),
  ("marrow_b",0,"marrow_b","0", []),
  ("squash_plant",0,"marrow_c","0", []),

  ("winch",sokf_static_movement,"winch","bo_winch", []),
  
  ("winch_b",sokf_static_movement|spr_use_time(5),"winch_b","bo_winch", [
   (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),

      #for only server itself-----------------------------------------------------------------------------------------------
      (call_script, "script_use_item", ":instance_id", ":agent_id"),
      #for only server itself-----------------------------------------------------------------------------------------------
      (try_for_players, ":player_no", 1),
        (player_is_active, ":player_no"),
        (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_use_item, ":instance_id", ":agent_id"),
      (try_end),
    ]),
  ]),
  
  ("drawbridge",0,"drawbridge","bo_drawbridge", []),
  ("gatehouse_door_left",sokf_static_movement,"gatehouse_door_left","bo_gatehouse_door_left", []),
  ("gatehouse_door_right",sokf_static_movement,"gatehouse_door_right","bo_gatehouse_door_right", []),

  ("cheese_a",0,"cheese_a","0", []),
  ("cheese_b",0,"cheese_b","0", []),
  ("cheese_slice_a",0,"cheese_slice_a","0", []),
  ("bread_a",0,"bread_a","0", []),
  ("bread_b",0,"bread_b","0", []),
  ("bread_slice_a",0,"bread_slice_a","0", []),
  ("fish_a",0,"fish_a","0", []),
  ("fish_roasted_a",0,"fish_roasted_a","0", []),
  ("chicken_roasted",0,"chicken","0", []),
  ("food_steam",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (set_position_delta,0,0,0),
     (particle_system_add_new, "psys_food_steam"),
    ]),
   ]),
  ########################
  ("city_smoke",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (store_time_of_day,reg(12)),
     (neg|is_between,reg(12),5,20),
     (set_position_delta,0,0,0),
     (particle_system_add_new, "psys_night_smoke_1"),
    ]),
   ]),
    ("city_fire_fly_night",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (store_time_of_day,reg(12)),
     (neg|is_between,reg(12),5,20),
     (set_position_delta,0,0,0),
     (particle_system_add_new, "psys_fire_fly_1"),
    ]),
   ]),
    ("city_fly_day",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_bug_fly_1"),
    ]),
   ]),
    ("flue_smoke_tall",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_flue_smoke_tall"),
    ]),
   ]),
      ("flue_smoke_short",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_flue_smoke_short"),
    ]),
   ]),
      ("moon_beam",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_moon_beam_1"),
     (particle_system_add_new, "psys_moon_beam_paricle_1"),
    ]),
   ]),
    ("fire_small",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_fireplace_fire_small"),
    ]),
   ]),
  ("fire_big",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_fireplace_fire_big"),
    ]),
   ]),
    ("battle_field_smoke",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_war_smoke_tall"),
    ]),
   ]),
      ("Village_fire_big",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_village_fire_big"),
     (set_position_delta,0,0,100),
     (particle_system_add_new, "psys_village_fire_smoke_big"),
    ]),
   ]),
  #########################
  ("candle_a",0,"candle_a","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (set_position_delta,0,0,27),
     (particle_system_add_new, "psys_candle_light"),
    ]),
   ]),
  ("candle_b",0,"candle_b","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (set_position_delta,0,0,25),
     (particle_system_add_new, "psys_candle_light"),
    ]),
   ]),
  ("candle_c",0,"candle_a","0",   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (set_position_delta,0,0,10),
     (particle_system_add_new, "psys_candle_light_small"),
    ]),
   ]),


  ("hook_a",0,"hook_a","0", []),
#  ("window_night",0,"window_night","0", []),
  ("fried_pig",0,"pork","0", []),
  ("village_oven",0,"village_oven","bo_village_oven", []),
  ("dungeon_water_drops",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_dungeon_water_drops"),
    ]),
   ]),
  ("shadow_circle_1",0,"shadow_circle_1","0", []),
  ("shadow_circle_2",0,"shadow_circle_2","0", []),
  ("shadow_square_1",0,"shadow_square_1","0", []),
  ("shadow_square_2",0,"shadow_square_2","0", []),
  ("wheelbarrow",0,"wheelbarrow","bo_wheelbarrow", []),
  ("gourd",sokf_static_movement|sokf_destructible|spr_hit_points(1),"gourd","bo_gourd",
   [
     (ti_on_scene_prop_destroy,
      [
        (try_begin),
          (this_or_next|multiplayer_is_server),
          (neg|game_in_multiplayer_mode),
          
          (store_trigger_param_1, ":instance_no"),
          (set_fixed_point_multiplier,100),
          
          (prop_instance_get_position, pos1, ":instance_no"),
          (particle_system_burst, "psys_gourd_smoke", pos1, 2),
          (particle_system_burst, "psys_gourd_piece_1", pos1, 1),
          (particle_system_burst, "psys_gourd_piece_2", pos1, 5),
          (position_move_z,pos1,-3000),
          (prop_instance_animate_to_position, ":instance_no", pos2, 1),
          (play_sound, "snd_gourd_destroyed"),
        (try_end),
        ]),
     ]),
   ("coconut",sokf_static_movement|sokf_destructible|spr_hit_points(1),"coconut","bo_coconut",
   [
     (ti_on_scene_prop_destroy,
      [
        (try_begin),
          (this_or_next|multiplayer_is_server),
          (neg|game_in_multiplayer_mode),
          
          (store_trigger_param_1, ":instance_no"),
          (set_fixed_point_multiplier,100),
          
          (prop_instance_get_position, pos1, ":instance_no"),
          (particle_system_burst, "psys_gourd_smoke", pos1, 2),
          (particle_system_burst, "psys_gourd_piece_1", pos1, 1),
          (particle_system_burst, "psys_gourd_piece_2", pos1, 5),
          (position_move_z,pos1,-3000),
          (prop_instance_animate_to_position, ":instance_no", pos2, 1),
          (play_sound, "snd_gourd_destroyed"),
        (try_end),
        ]),
     ]),

 ("gourd_spike",sokf_static_movement,"gourd_spike","bo_gourd_spike",[]),

 ("obstacle_fence_1",0,"fence","bo_fence", []),

 ("small_wall_connect_a",0,"small_wall_connect_a","bo_small_wall_connect_a", []),


 ("full_stable_d",0,"full_stable_d","bo_full_stable_d", []),

 ("arabian_house_a",0,"arabian_house_a","bo_arabian_house_a", []),
 ("arabian_house_b",0,"arabian_house_b","bo_arabian_house_b", []),
 ("arabian_house_c",0,"arabian_house_c","bo_arabian_house_c", []),
 ("arabian_house_d",0,"arabian_house_d","bo_arabian_house_d", []),
 ("arabian_house_e",0,"arabian_house_e","bo_arabian_house_e", []),
 ("arabian_house_f",0,"arabian_house_f","bo_arabian_house_f", []),
 ("arabian_house_g",0,"arabian_house_g","bo_arabian_house_g", []),
 ("arabian_house_h",0,"arabian_house_h","bo_arabian_house_h", []),
 ("arabian_house_i",0,"arabian_house_i","bo_arabian_house_i", []),
 
 ("arabian_passage_house_a",0,"arabian_passage_house_a","bo_arabian_passage_house_a", []),
 ("arabian_wall_a",0,"arabian_wall_a","bo_arabian_wall_a", []),
 ("arabian_wall_b",0,"arabian_wall_b","bo_arabian_wall_b", []),
 ("arabian_ground_a",0,"arabian_ground_a","bo_arabian_ground_a", []),
 ("arabian_parterre_a",0,"arabian_parterre_a","bo_arabian_parterre_a", []),
 ("well_shaft",0,"well_shaft","bo_well_shaft", []),
 ("horse_mill",0,"horse_mill","bo_horse_mill", []),
 ("horse_mill_collar",0,"horse_mill_collar","bo_horse_mill_collar", []),
 ("arabian_stable",0,"arabian_stable","bo_arabian_stable", []),
 ("arabian_tent",0,"arabian_tent","bo_arabian_tent", []),
 ("arabian_tent_b",0,"arabian_tent_b","bo_arabian_tent_b", []),
 ("desert_plant_a",0,"desert_plant_a","0", []),

 ("arabian_castle_stairs",sokf_type_ladder,"arabian_castle_stairs","bo_arabian_castle_stairs", []),
 ("arabian_castle_stairs_b",sokf_type_ladder,"arabian_castle_stairs_b","bo_arabian_castle_stairs_b", []),
 ("arabian_castle_stairs_c",sokf_type_ladder,"arabian_castle_stairs_c","bo_arabian_castle_stairs_c", []),

 ("arabian_castle_house_a",0,"arabian_castle_house_a","bo_arabian_castle_house_a", []),
 ("arabian_castle_house_b",0,"arabian_castle_house_b","bo_arabian_castle_house_b", []),


 ("arabian_house_a2",0,"arabian_house_a2","bo_arabian_house_a2", []),
 ("arabian_village_house_a",0,"arabian_village_house_a","bo_arabian_village_house_a", []),
 ("arabian_village_house_b",0,"arabian_village_house_b","bo_arabian_village_house_b", []),
 ("arabian_village_house_c",0,"arabian_village_house_c","bo_arabian_village_house_c", []),
 ("arabian_village_house_d",0,"arabian_village_house_d","bo_arabian_village_house_d", []),

 ("arabian_village_stable",0,"arabian_village_stable","bo_arabian_village_stable", []),
 ("arabian_village_hut",0,"arabian_village_hut","bo_arabian_village_hut", []),
 ("arabian_village_stairs",sokf_type_ladder,"arabian_village_stairs","bo_arabian_village_stairs", []),

 ("stairs_a",sokf_type_ladder,"stairs_a","bo_stairs_a", []),

 ("headquarters_flag_red",sokf_static_movement|sokf_face_player,"mp_flag_red","0", []),
 ("headquarters_flag_blue",sokf_static_movement|sokf_face_player,"mp_flag_blue","0", []),
 ("headquarters_flag_gray",sokf_static_movement|sokf_face_player,"whiteflag","0", []),  

 ("headquarters_flag_red_code_only",sokf_static_movement|sokf_face_player,"mp_flag_red","0", []),
 ("headquarters_flag_blue_code_only",sokf_static_movement|sokf_face_player,"mp_flag_blue","0", []),
 ("headquarters_flag_gray_code_only",sokf_static_movement|sokf_face_player,"whiteflag","0", []),  
 ("headquarters_pole_code_only",sokf_static_movement,"mp_flag_pole","0", [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_flag_loop"),
    ]),]),

 # MM
 ("headquarters_flag_swadian",sokf_static_movement|sokf_face_player,"britflag","0", []),
 ("headquarters_flag_vaegir",sokf_static_movement|sokf_face_player,"frenchie_flag","0", []),
 ("headquarters_flag_khergit",sokf_static_movement|sokf_face_player,"prussiaflag","0", []),
 ("headquarters_flag_nord",sokf_static_movement|sokf_face_player,"russkieflag","0", []),
 ("headquarters_flag_rhodok",sokf_static_movement|sokf_face_player,"austrianflag","0", []),
 ("headquarters_flag_sarranid",sokf_static_movement|sokf_face_player,"censoredconfederateflag","0", []),

 ("glow_a", 0, "glow_a", "0", []),
 ("glow_b", 0, "glow_b", "0", []),

  ("dummy_a_undestructable",sokf_destructible,"arena_archery_target_b","bo_arena_archery_target_b",
   [
     (ti_on_init_scene_prop,
      [
        (store_trigger_param_1, ":instance_no"),
        (scene_prop_set_hit_points, ":instance_no", 10000000),
        ]),
     (ti_on_scene_prop_hit,
      [
        (play_sound, "snd_dummy_hit"),
        (particle_system_burst, "psys_dummy_smoke", pos1, 3),
        (particle_system_burst, "psys_dummy_straw", pos1, 10),
        
        (try_begin),
          (this_or_next|multiplayer_is_server),
          (neg|game_in_multiplayer_mode),
          
          (set_fixed_point_multiplier, 1),
          (position_get_x, ":attacker_agent_id", pos2),
          (set_fixed_point_multiplier, 100),
          
          (store_trigger_param_2, ":damage"),
          
          (assign, reg60, ":damage"),
          (try_begin),
            (game_in_multiplayer_mode),
            
            (agent_get_player_id,":player_id",":attacker_agent_id"),
            (player_is_active,":player_id"),
            
            (multiplayer_send_string_to_player, ":player_id", multiplayer_event_show_server_message, "str_delivered_damage"),
          (else_try),
            (neg|game_in_multiplayer_mode),
            (call_script, "script_client_get_my_agent"),
            (eq, ":attacker_agent_id", reg0), # Only for myself.
            (display_message, "str_delivered_damage"),
          (try_end),
        (try_end),
      ]),
   ]),
 ("cave_entrance_1",0,"cave_entrance_1","bo_cave_entrance_1", []),

  ("pointer_arrow", 0, "pointer_arrow", "0", []),
  ("fireplace_d_interior",0,"fireplace_d","bo_fireplace_d", []),
  ("ship_sail_off",0,"ship_sail_off","bo_ship_sail_off", []),
  ("ship_sail_off_b",0,"ship_sail_off_b","bo_ship_sail_off", []),
  ("ship_c_sail_off",0,"ship_c_sail_off","bo_ship_c_sail_off", []),
  ("ramp_small_a",0,"ramp_small_a","bo_ramp_small_a", []),
 
  ("box_a_dynamic",sokf_static_movement,"box_a","bo_box_a", []), # sokf_moveable|sokf_dynamic_physics

 ("desert_field",0,"desert_field","bo_desert_field", []),

 ("water_river",0,"water_plane","0", []),

 ("harbour_a",0,"harbour_a","bo_harbour_a", []),
 ("sea_foam_a",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
    (neg|multiplayer_is_dedicated_server),
     (particle_system_add_new, "psys_sea_foam_a"),
    ]),
   ]),
   
 
 ("earth_gate_house_b",0,"earth_gate_house_b","bo_earth_gate_house_b", []),

 ("earth_stairs_c",0,"earth_stairs_c","bo_earth_stairs_c", []),
 



  ("barrier_box",sokf_invisible|sokf_type_barrier3d,"barrier_box","bo_barrier_box", []),
  ("barrier_capsule",sokf_invisible|sokf_type_barrier3d,"barrier_capsule","bo_barrier_capsule", []),
  ("barrier_cone" ,sokf_invisible|sokf_type_barrier3d,"barrier_cone" ,"bo_barrier_cone" , []),
  ("barrier_sphere" ,sokf_invisible|sokf_type_barrier3d,"barrier_sphere" ,"bo_barrier_sphere" , []),


 # MM
 ("ctf_flag_kingdom_1", sokf_static_movement, "ctf_flag_britain", "0", []),
 ("ctf_flag_kingdom_2", sokf_static_movement, "ctf_flag_france", "0", []),
 ("ctf_flag_kingdom_3", sokf_static_movement, "ctf_flag_prussia", "0", []),
 ("ctf_flag_kingdom_4", sokf_static_movement, "ctf_flag_russia", "0", []),
 ("ctf_flag_kingdom_5", sokf_static_movement, "ctf_flag_austria", "0", []),
 ("ctf_flag_kingdom_6", sokf_static_movement, "ctf_flag_rhine", "0", []),
 ("ctf_flag_kingdom_7", sokf_static_movement, "ctf_flag_rebel", "0", []),

 ("headquarters_flag_rebel",sokf_static_movement|sokf_face_player,"rebbleflag","0", []),
  ("arabian_lighthouse_a",0,"arabian_lighthouse_a","bo_arabian_lighthouse_a", []),
  ("arabian_ramp_a",0,"arabian_ramp_a","bo_arabian_ramp_a", []),
  ("arabian_ramp_b",0,"arabian_ramp_b","bo_arabian_ramp_b", []),
  
  ("winery_barrel_shelf",0,"winery_barrel_shelf","bo_winery_barrel_shelf", []),
  ("winery_wall_shelf",0,"winery_wall_shelf","bo_winery_wall_shelf", []),
  ("winery_huge_barrel",0,"winery_huge_barrel","bo_winery_huge_barrel", []),
  ("winery_wine_press",0,"winery_wine_press","bo_winery_wine_press", []),
  ("winery_middle_barrel",0,"winery_middle_barrel","bo_winery_middle_barrel", []),
  ("winery_wine_cart_small_loaded",0,"winery_wine_cart_small_loaded","bo_winery_wine_cart_small_loaded", []),
  ("winery_wine_cart_small_empty",0,"winery_wine_cart_small_empty","bo_winery_wine_cart_small_empty", []),
  ("winery_wine_cart_empty",0,"winery_wine_cart_empty","bo_winery_wine_cart_empty", []),
  ("winery_wine_cart_loaded",0,"winery_wine_cart_loaded","bo_winery_wine_cart_loaded", []),

  ("weavery_loom_a",0,"weavery_loom_a","bo_weavery_loom_a", []),

  ("mill_flour_sack", 0,"mill_flour_sack","bo_mill_flour_sack", []),
  ("mill_flour_sack_desk_a", 0,"mill_flour_sack_desk_a","bo_mill_flour_sack_desk_a", []),
  ("mill_flour_sack_desk_b", 0,"mill_flour_sack_desk_b","bo_mill_flour_sack_desk_b", []),


 ("bridge_b",0,"bridge_b","bo_bridge_b", []),
 
("brewery_pool", 0,"brewery_pool","bo_brewery_pool", []),
("brewery_big_bucket", 0,"brewery_big_bucket","bo_brewery_big_bucket", []),
("brewery_bucket_platform_a", 0,"brewery_bucket_platform_a","bo_brewery_bucket_platform_a", []),
("brewery_bucket_platform_b", 0,"brewery_bucket_platform_b","bo_brewery_bucket_platform_b", []),

  ("rope_bridge_15m",0,"rope_bridge_15m","bo_rope_bridge_15m", []),
  
  ("tree_house_guard_a",0,"tree_house_guard_a","bo_tree_house_guard_a", []),
  ("tree_house_guard_b",0,"tree_house_guard_b","bo_tree_house_guard_b", []),
  ("tree_shelter_a",0,"tree_shelter_a","bo_tree_shelter_a", []),
  ("yellow_fall_leafs_a",0,"0","0",[]),
  
 ("rock_bridge_a",0,"rock_bridge_a","bo_rock_bridge_a", []),
 ("suspension_bridge_a",0,"suspension_bridge_a","bo_suspension_bridge_a", []),
 ("mine_a",0,"mine_a","bo_mine_a", []),
  
  

  
################################
######## MM SCENE PROPS ########
################################

    # Weather scene props
    ("mm_weather_time", 0, "0", "0", []), # var1 = time of day 0-23; Default = 15
    ("mm_weather_rain", 0, "0", "0", []), # var1 = rain type 1 = rain 2 = snow, var2 = rain ammount 0-25  
    ("mm_weather_clouds", 0, "0", "0", []), # var1 = cloud ammount 0-100; Default = 30
    ("mm_weather_fog", 0, "0", "0", []), # var1 = fog distance; meters x 10 where fog visibility ends 
    ("mm_weather_thunder", 0, "0", "0", []), # var1 = thunder type: 0 = none 1 = thunder only 2 = thunder & lighting, 
                                             # var2 = thunder frequancy 0-100 ; the higher value the more thunder
    ("mm_weather_wind", 0, "0", "0", []), # var1 = flora_wind_strength in % 0-100; Default = 14
                                          # var2 = water_wind_strength in % 0-100; Default = 14
    # Cannon with horse spawn prop
    ("mm_spawn_with_cannon", 0, "0", "0", []), #  If this prop is in the map, the arty sarges spawn with a cannon attached.
    
    # Cannon with horse spawn prop
    ("mm_spawn_restrictions", 0, "0", "0", []), #  var1 = spawn restriction;  1 = Infantry only, 2 = cav only.
    
    # Snowy ground for groundhits.
    ("mm_snowy_ground", 0, "0", "0", []), #  If this prop is in the map, the particles for ground hits will be snowy style
    
    # Additional Conquest points
    ("mm_additional_conquest_points", 0, "0", "0", []), #  var1 = team_no
                                                        #  var2 = amount of additional points
    # Disable explosives
    ("mm_disable_explosives", 0, "0", "0", []), #  If this prop is in the map, the sappers cannot place explosives. var1 = team limit; 0 = both, 1 = only team1, 2 = only team2
    
    
    # first some trees :3  patch1115 bug fix 42/1 start
    ("mm_tree_aspen1" ,sokf_handle_as_flora,"mm_aspen1" ,"bo_mm_aspen1" , []),
    ("mm_tree_aspen2" ,sokf_handle_as_flora,"mm_aspen2" ,"bo_mm_aspen2" , []),
    ("mm_tree_aspen3" ,sokf_handle_as_flora,"mm_aspen3" ,"bo_mm_aspen3" , []),
    ("mm_tree_aspen4" ,sokf_handle_as_flora,"mm_aspen4" ,"bo_mm_aspen4" , []),
    ("mm_tree_aspen5" ,sokf_handle_as_flora,"mm_aspen5" ,"bo_mm_aspen5" , []),
    ("mm_tree_aspen6" ,sokf_handle_as_flora,"mm_aspen6" ,"bo_mm_aspen6" , []),
    ("mm_tree_aspen7" ,sokf_handle_as_flora,"mm_aspen7" ,"bo_mm_aspen7" , []),
    ("mm_tree_aspen8" ,sokf_handle_as_flora,"mm_aspen8" ,"bo_mm_aspen8" , []),
    ("mm_tree_aspen9" ,sokf_handle_as_flora,"mm_aspen9" ,"bo_mm_aspen9" , []),
    ("mm_tree_aspen10" ,sokf_handle_as_flora,"mm_aspen10" ,"bo_mm_aspen10" , []),
    ("mm_tree_aspen11" ,sokf_handle_as_flora,"mm_aspen11" ,"bo_mm_aspen11" , []),
    ("mm_tree_aspen12" ,sokf_handle_as_flora,"mm_aspen12" ,"bo_mm_aspen12" , []),
    ("mm_tree_aspen13" ,sokf_handle_as_flora,"mm_aspen13" ,"bo_mm_aspen13" , []),
    ("mm_tree_aspen14" ,sokf_handle_as_flora,"mm_aspen14" ,"bo_mm_aspen14" , []),
    ("mm_tree_aspen15" ,sokf_handle_as_flora,"mm_aspen15" ,"bo_mm_aspen15" , []),
    
    ("mm_tree_pine1" ,sokf_handle_as_flora,"mm_pine1" ,"bo_mm_pine1" , []),
    ("mm_tree_pine2" ,sokf_handle_as_flora,"mm_pine2" ,"bo_mm_pine2" , []),
    ("mm_tree_pine3" ,sokf_handle_as_flora,"mm_pine3" ,"bo_mm_pine3" , []),
    ("mm_tree_pine4" ,sokf_handle_as_flora,"mm_pine4" ,"bo_mm_pine4" , []),
    ("mm_tree_pine5" ,sokf_handle_as_flora,"mm_pine5" ,"bo_mm_pine5" , []),
    ("mm_tree_pine6" ,sokf_handle_as_flora,"mm_pine6" ,"bo_mm_pine6" , []),
    ("mm_tree_pine7" ,sokf_handle_as_flora,"mm_pine7" ,"bo_mm_pine7" , []),
    
    ("mm_tree_pine_snowy1" ,sokf_handle_as_flora,"mm_pine1s" ,"bo_mm_pine1s" , []),
    ("mm_tree_pine_snowy2" ,sokf_handle_as_flora,"mm_pine2s" ,"bo_mm_pine2s" , []),
    ("mm_tree_pine_snowy3" ,sokf_handle_as_flora,"mm_pine3s" ,"bo_mm_pine3s" , []),
    ("mm_tree_pine_snowy4" ,sokf_handle_as_flora,"mm_pine4s" ,"bo_mm_pine4s" , []),
    ("mm_tree_pine_snowy5" ,sokf_handle_as_flora,"mm_pine5s" ,"bo_mm_pine5s" , []),
    ("mm_tree_pine_snowy6" ,sokf_handle_as_flora,"mm_pine6s" ,"bo_mm_pine6s" , []),
    ("mm_tree_pine_snowy7" ,sokf_handle_as_flora,"mm_pine7s" ,"bo_mm_pine7s" , []),
    
    ("mm_tree_northern1" ,sokf_handle_as_flora,"mm_northern_tree1" ,"bo_mm_northern_tree1" , []),
    ("mm_tree_northern2" ,sokf_handle_as_flora,"mm_northern_tree2" ,"bo_mm_northern_tree2" , []),
    ("mm_tree_northern3" ,sokf_handle_as_flora,"mm_northern_tree3" ,"bo_mm_northern_tree3" , []),
    ("mm_tree_northern4" ,sokf_handle_as_flora,"mm_northern_tree4" ,"bo_mm_northern_tree4" , []),
    ("mm_tree_northern5" ,sokf_handle_as_flora,"mm_pine_3" ,"bo_mm_pine_3" , []),
    ("mm_tree_northern6" ,sokf_handle_as_flora,"mm_pine_4" ,"bo_mm_pine_4" , []),
    ("mm_tree_northern7" ,sokf_handle_as_flora,"mm_pine_5" ,"bo_mm_pine_5" , []),
    
    ("mm_tree_autumn1" ,sokf_handle_as_flora,"mm_autumn_tree" ,"bo_mm_autumn_tree" , []),
    ("mm_tree_autumn2" ,sokf_handle_as_flora,"mm_autumn_tree1" ,"bo_mm_autumn_tree1" , []),
    ("mm_tree_autumn3" ,sokf_handle_as_flora,"mm_autumn_tree2" ,"bo_mm_autumn_tree2" , []),
    ("mm_tree_autumn4" ,sokf_handle_as_flora,"mm_autumn_tree3" ,"bo_mm_autumn_tree3" , []),
    ("mm_tree_autumn5" ,sokf_handle_as_flora,"mm_autumn_tree4" ,"bo_mm_autumn_tree4" , []),
    
    ("mm_tree_winter1" ,sokf_handle_as_flora,"mm_winter_tree" ,"bo_mm_winter_tree" , []),
    ("mm_tree_winter2" ,sokf_handle_as_flora,"mm_winter_tree1" ,"bo_mm_winter_tree1" , []),
    ("mm_tree_winter3" ,sokf_handle_as_flora,"mm_winter_tree2" ,"bo_mm_winter_tree2" , []),
    ("mm_tree_winter4" ,sokf_handle_as_flora,"mm_winter_tree3" ,"bo_mm_winter_tree3" , []),
    ("mm_tree_winter5" ,sokf_handle_as_flora,"mm_winter_tree4" ,"bo_mm_winter_tree4" , []),
    ("mm_tree_winter6" ,sokf_handle_as_flora,"mm_winter_tree5" ,"bo_mm_winter_tree5" , []),
    ("mm_tree_winter7" ,sokf_handle_as_flora,"mm_winter_tree6" ,"bo_mm_winter_tree6" , []),
    ("mm_tree_winter8" ,sokf_handle_as_flora,"mm_winter_tree7" ,"bo_mm_winter_tree7" , []),
    ("mm_tree_winter9" ,sokf_handle_as_flora,"mm_winter_tree8" ,"bo_mm_winter_tree8" , []),
    ("mm_tree_winter10" ,sokf_handle_as_flora,"mm_winter_tree9" ,"bo_mm_winter_tree9" , []),
    ("mm_tree_winter11" ,sokf_handle_as_flora,"mm_winter_tree10" ,"bo_mm_winter_tree10" , []),
    ("mm_tree_winter12" ,sokf_handle_as_flora,"mm_winter_tree11" ,"bo_mm_winter_tree11" , []),
    ("mm_tree_winter13" ,sokf_handle_as_flora,"mm_winter_tree12" ,"bo_mm_winter_tree12" , []),
    ("mm_tree_winter14" ,sokf_handle_as_flora,"mm_winter_tree13" ,"bo_mm_winter_tree13" , []),
    ("mm_tree_winter15" ,sokf_handle_as_flora,"mm_winter_tree14" ,"bo_mm_winter_tree14" , []),
    ("mm_tree_winter16" ,sokf_handle_as_flora,"mm_winter_tree15" ,"bo_mm_winter_tree15" , []),
    
    ("mm_tree_big1" ,sokf_handle_as_flora,"big_tree_mm" ,"bo_big_tree_mm" , []),
    ("mm_tree_big2" ,sokf_handle_as_flora,"big_tree_mm1" ,"bo_big_tree_mm1" , []),
    ("mm_tree_big3" ,sokf_handle_as_flora,"big_tree_mm2" ,"bo_big_tree_mm2" , []),
    ("mm_tree_big4" ,sokf_handle_as_flora,"big_tree_mm3" ,"bo_big_tree_mm3" , []),
    
    ("mm_tree_vegetation1" ,sokf_handle_as_flora,"mm_vegetation_tree1" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation2" ,sokf_handle_as_flora,"mm_vegetation_tree2" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation3" ,sokf_handle_as_flora,"mm_vegetation_tree3" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation4" ,sokf_handle_as_flora,"mm_vegetation_tree4" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation5" ,sokf_handle_as_flora,"mm_vegetation_tree5" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation6" ,sokf_handle_as_flora,"mm_vegetation_tree6" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation7" ,sokf_handle_as_flora,"mm_vegetation_tree7" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation8" ,sokf_handle_as_flora,"mm_vegetation_tree8" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation9" ,sokf_handle_as_flora,"mm_vegetation_tree9" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation10" ,sokf_handle_as_flora,"mm_vegetation_tree10" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation11" ,sokf_handle_as_flora,"mm_vegetation_tree11" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation12" ,sokf_handle_as_flora,"mm_vegetation_tree12" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation14" ,sokf_handle_as_flora,"mm_vegetation_tree14" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation15" ,sokf_handle_as_flora,"mm_vegetation_tree15" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation2_1" ,sokf_handle_as_flora,"mm_vegetation_tree21" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation2_2" ,sokf_handle_as_flora,"mm_vegetation_tree22" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation2_3" ,sokf_handle_as_flora,"mm_vegetation_tree23" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation2_4" ,sokf_handle_as_flora,"mm_vegetation_tree24" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation2_5" ,sokf_handle_as_flora,"mm_vegetation_tree25" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation2_6" ,sokf_handle_as_flora,"mm_vegetation_tree26" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation2_7" ,sokf_handle_as_flora,"mm_vegetation_tree27" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation2_8" ,sokf_handle_as_flora,"mm_vegetation_tree28" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation2_9" ,sokf_handle_as_flora,"mm_vegetation_tree29" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation2_10" ,sokf_handle_as_flora,"mm_vegetation_tree210" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation2_11" ,sokf_handle_as_flora,"mm_vegetation_tree211" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation2_12" ,sokf_handle_as_flora,"mm_vegetation_tree212" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation2_14" ,sokf_handle_as_flora,"mm_vegetation_tree214" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation2_15" ,sokf_handle_as_flora,"mm_vegetation_tree215" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation3_1" ,sokf_handle_as_flora,"mm_vegetation_tree31" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation3_2" ,sokf_handle_as_flora,"mm_vegetation_tree32" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation3_3" ,sokf_handle_as_flora,"mm_vegetation_tree33" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation3_4" ,sokf_handle_as_flora,"mm_vegetation_tree34" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation3_5" ,sokf_handle_as_flora,"mm_vegetation_tree35" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation3_6" ,sokf_handle_as_flora,"mm_vegetation_tree36" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation3_7" ,sokf_handle_as_flora,"mm_vegetation_tree37" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation3_8" ,sokf_handle_as_flora,"mm_vegetation_tree38" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation3_9" ,sokf_handle_as_flora,"mm_vegetation_tree39" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation3_10" ,sokf_handle_as_flora,"mm_vegetation_tree310" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation3_11" ,sokf_handle_as_flora,"mm_vegetation_tree311" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation3_12" ,sokf_handle_as_flora,"mm_vegetation_tree312" ,"bo_mm_vegetation_tree12" , []),
    #("mm_tree_vegetation3_13" ,sokf_handle_as_flora,"mm_vegetation_tree313" ,"bo_mm_vegetation_tree13" , []),
    ("mm_tree_vegetation3_14" ,sokf_handle_as_flora,"mm_vegetation_tree314" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation3_15" ,sokf_handle_as_flora,"mm_vegetation_tree315" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation7_1" ,sokf_handle_as_flora,"mm_vegetation_tree71" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation7_2" ,sokf_handle_as_flora,"mm_vegetation_tree72" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation7_3" ,sokf_handle_as_flora,"mm_vegetation_tree73" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation7_4" ,sokf_handle_as_flora,"mm_vegetation_tree74" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation7_5" ,sokf_handle_as_flora,"mm_vegetation_tree75" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation7_6" ,sokf_handle_as_flora,"mm_vegetation_tree76" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation7_7" ,sokf_handle_as_flora,"mm_vegetation_tree77" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation7_8" ,sokf_handle_as_flora,"mm_vegetation_tree78" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation7_9" ,sokf_handle_as_flora,"mm_vegetation_tree79" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation7_10" ,sokf_handle_as_flora,"mm_vegetation_tree710" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation7_11" ,sokf_handle_as_flora,"mm_vegetation_tree711" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation7_12" ,sokf_handle_as_flora,"mm_vegetation_tree712" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation7_14" ,sokf_handle_as_flora,"mm_vegetation_tree714" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation7_15" ,sokf_handle_as_flora,"mm_vegetation_tree715" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation8_1" ,sokf_handle_as_flora,"mm_vegetation_tree81" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation8_2" ,sokf_handle_as_flora,"mm_vegetation_tree82" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation8_3" ,sokf_handle_as_flora,"mm_vegetation_tree83" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation8_4" ,sokf_handle_as_flora,"mm_vegetation_tree84" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation8_5" ,sokf_handle_as_flora,"mm_vegetation_tree85" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation8_6" ,sokf_handle_as_flora,"mm_vegetation_tree86" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation8_7" ,sokf_handle_as_flora,"mm_vegetation_tree87" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation8_8" ,sokf_handle_as_flora,"mm_vegetation_tree88" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation8_9" ,sokf_handle_as_flora,"mm_vegetation_tree89" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation8_10" ,sokf_handle_as_flora,"mm_vegetation_tree810" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation8_11" ,sokf_handle_as_flora,"mm_vegetation_tree811" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation8_12" ,sokf_handle_as_flora,"mm_vegetation_tree812" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation8_14" ,sokf_handle_as_flora,"mm_vegetation_tree814" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation8_15" ,sokf_handle_as_flora,"mm_vegetation_tree815" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation9_1" ,sokf_handle_as_flora,"mm_vegetation_tree91" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation9_2" ,sokf_handle_as_flora,"mm_vegetation_tree92" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation9_3" ,sokf_handle_as_flora,"mm_vegetation_tree93" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation9_4" ,sokf_handle_as_flora,"mm_vegetation_tree94" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation9_5" ,sokf_handle_as_flora,"mm_vegetation_tree95" ,"bo_mm_vegetation_tree5" , []),
    ("mm_tree_vegetation9_6" ,sokf_handle_as_flora,"mm_vegetation_tree96" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation9_7" ,sokf_handle_as_flora,"mm_vegetation_tree97" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation9_8" ,sokf_handle_as_flora,"mm_vegetation_tree98" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation9_9" ,sokf_handle_as_flora,"mm_vegetation_tree99" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation9_10" ,sokf_handle_as_flora,"mm_vegetation_tree910" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation9_11" ,sokf_handle_as_flora,"mm_vegetation_tree911" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation9_12" ,sokf_handle_as_flora,"mm_vegetation_tree912" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation9_14" ,sokf_handle_as_flora,"mm_vegetation_tree914" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation9_15" ,sokf_handle_as_flora,"mm_vegetation_tree915" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation10_1" ,sokf_handle_as_flora,"mm_vegetation_tree101" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation10_2" ,sokf_handle_as_flora,"mm_vegetation_tree102" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation10_3" ,sokf_handle_as_flora,"mm_vegetation_tree103" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation10_4" ,sokf_handle_as_flora,"mm_vegetation_tree104" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation10_5" ,sokf_handle_as_flora,"mm_vegetation_tree104" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation10_6" ,sokf_handle_as_flora,"mm_vegetation_tree106" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation10_7" ,sokf_handle_as_flora,"mm_vegetation_tree107" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation10_8" ,sokf_handle_as_flora,"mm_vegetation_tree108" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation10_9" ,sokf_handle_as_flora,"mm_vegetation_tree109" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation10_10" ,sokf_handle_as_flora,"mm_vegetation_tree1010" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation10_11" ,sokf_handle_as_flora,"mm_vegetation_tree1011" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation10_12" ,sokf_handle_as_flora,"mm_vegetation_tree1012" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation10_14" ,sokf_handle_as_flora,"mm_vegetation_tree1014" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation10_15" ,sokf_handle_as_flora,"mm_vegetation_tree1015" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_vegetation11_1" ,sokf_handle_as_flora,"mm_vegetation_tree111" ,"bo_mm_vegetation_tree1" , []),
    ("mm_tree_vegetation11_2" ,sokf_handle_as_flora,"mm_vegetation_tree112" ,"bo_mm_vegetation_tree2" , []),
    ("mm_tree_vegetation11_3" ,sokf_handle_as_flora,"mm_vegetation_tree113" ,"bo_mm_vegetation_tree3" , []),
    ("mm_tree_vegetation11_4" ,sokf_handle_as_flora,"mm_vegetation_tree114" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation11_5" ,sokf_handle_as_flora,"mm_vegetation_tree114" ,"bo_mm_vegetation_tree4" , []),
    ("mm_tree_vegetation11_6" ,sokf_handle_as_flora,"mm_vegetation_tree116" ,"bo_mm_vegetation_tree6" , []),
    ("mm_tree_vegetation11_7" ,sokf_handle_as_flora,"mm_vegetation_tree117" ,"bo_mm_vegetation_tree7" , []),
    ("mm_tree_vegetation11_8" ,sokf_handle_as_flora,"mm_vegetation_tree118" ,"bo_mm_vegetation_tree8" , []),
    ("mm_tree_vegetation11_9" ,sokf_handle_as_flora,"mm_vegetation_tree119" ,"bo_mm_vegetation_tree9" , []),
    ("mm_tree_vegetation11_10" ,sokf_handle_as_flora,"mm_vegetation_tree1110" ,"bo_mm_vegetation_tree10" , []),
    ("mm_tree_vegetation11_11" ,sokf_handle_as_flora,"mm_vegetation_tree1111" ,"bo_mm_vegetation_tree11" , []),
    ("mm_tree_vegetation11_12" ,sokf_handle_as_flora,"mm_vegetation_tree1112" ,"bo_mm_vegetation_tree12" , []),
    ("mm_tree_vegetation11_14" ,sokf_handle_as_flora,"mm_vegetation_tree1114" ,"bo_mm_vegetation_tree14" , []),
    ("mm_tree_vegetation11_15" ,sokf_handle_as_flora,"mm_vegetation_tree1115" ,"bo_mm_vegetation_tree15" , []),
    
    ("mm_tree_palm1" ,sokf_handle_as_flora,"palmb_7" ,"bo_palmb_7" , []),
    ("mm_tree_palm2" ,sokf_handle_as_flora,"palmb_8" ,"bo_palmb_8" , []),
    ("mm_tree_palm3" ,sokf_handle_as_flora,"palmb_9" ,"bo_palmb_9" , []),
    ("mm_tree_palm4" ,sokf_handle_as_flora,"palmb_10" ,"bo_palmb_10" , []),
    ("mm_tree_palm5" ,sokf_handle_as_flora,"palmb_11" ,"bo_palmb_11" , []),
    ("mm_tree_palm6" ,sokf_handle_as_flora,"palmb_12" ,"bo_palmb_12" , []),
    
   # ("mm_trees_end", 0,"0" ,"0" , []),
    
  # patch1115 bug fix 42/1 end
    #insects


#furnitre
 
   #hugo
		
   ("mm_hugo1" ,0,"hugo1" ,"bo_hugo1" , []),
   ("mm_hugo11" ,0,"hugo11" ,"bo_hugo11" , []),
   ("mm_hugo2" ,0,"hugo2" ,"bo_hugo2" , []),
   ("mm_hugo3" ,0,"hugo3" ,"bo_hugo3" , []),
   ("mm_hugo4" ,0,"hugo4" ,"bo_hugo4" , []),
   ("mm_hugo5" ,0,"hugo5" ,"bo_hugo5" , []),
   ("mm_hugo6" ,0,"hugo6" ,"bo_hugo6" , []),
   ("mm_hugo7" ,0,"hugo7" ,"bo_hugo7" , []),
   ("mm_hugo8" ,0,"hugo8" ,"bo_hugo8" , []),
   ("mm_hugo9" ,0,"hugo9" ,"bo_hugo9" , []),
   ("mm_hugo10" ,0,"hugo10" ,"bo_hugo10" , []),
   ("mm_hugo12" ,0,"hugo12" ,"bo_hugo12" , []),
   ("mm_hugo13" ,0,"hugo13" ,"bo_hugo13" , []),
   ("mm_hugo14" ,0,"hugo14" ,"bo_hugo14" , []),

   #camaretthing
   
    ("mm_camaretsurmer" ,0,"camaretsurmer" ,"bo_camaretsurmer" , []),

# furniture

		
   ("mm_cupboardd1" ,0,"mm_cupboard1" ,"bo_mm_cupboard2" , []),
 ("mm_cupboardd2" ,0,"mm_cupboard2" ,"bo_mm_cupboard2" , []),
 ("mm_cupboardd3" ,0,"mm_cupboard3" ,"bo_mm_cupboard3" , []),
 ("mm_cupboardd4" ,0,"mm_cupboard4" ,"bo_mm_cupboard5" , []),
 ("mm_cupboardd5" ,0,"mm_cupboard5" ,"bo_mm_cupboard5" , []),
 ("mm_box_a" ,0,"mm_box_a" ,"bo_mm_box_a" , []),
 ("mm_marrows" ,0,"mm_marrows" ,"0" , []),
 ("mm_kitchentools1" ,0,"mm_kitchentools1" ,"0" , []),
 ("mm_sofa2" ,0,"mm_sofa2" ,"bo_mm_sofa2" , []),
 ("mm_sofa" ,0,"mm_sofa" ,"bo_mm_sofa2" , []),
 ("mm_tree_bench" ,0,"mm_tree_bench" ,"bo_mm_tree_bench" , []),
 ("mm_bedside_table" ,0,"mm_bedside_table" ,"bo_mm_bedside_table" , []),
 ("mm_tablebig4" ,0,"mm_tablebig4" ,"bo_mm_tablebig3" , []),
 ("mm_tablebig3" ,0,"mm_tablebig3" ,"bo_mm_tablebig3" , []),
 ("mm_tablebig2" ,0,"mm_tablebig2" ,"bo_mm_tablebig2" , []),
 ("mm_tablebig1" ,0,"mm_tablebig1" ,"bo_mm_tablebig2" , []),

#newwallsetc

("mauers8" ,0,"mauers8" ,"bo_mauers8" , []),





#newredoubts
("mm_redoubt_modular_corner" ,0,"mm_redoubt_modular_corner" ,"bo_mm_redoubt_modular_corner" , []),
 ("mm_redoubt_modular_endpart" ,0,"mm_redoubt_modular_endpart" ,"bo_mm_redoubt_modular_endpart" , []),
 ("mm_redoubt_modular_straight" ,0,"mm_redoubt_modular_straight" ,"bo_mm_redoubt_modular_straight" , []),
 ("mm_redoubt_modular_straight_d" ,0,"mm_redoubt_modular_straight_d" ,"bo_mm_redoubt_modular_straight_d" , []),
 ("mm_redoubt_modular_straight_d1" ,0,"mm_redoubt_modular_straight_d1" ,"bo_mm_redoubt_modular_straight_d1" , []),



#flora
 
 ("flora_bush_new_3" ,sokf_handle_as_flora,"bush_new_b" ,"0" , []),

 ("flora_flowers1a" ,sokf_handle_as_flora,"grass_bush_amm" ,"0" , []),
 ("flora_flowers1b" ,sokf_handle_as_flora,"grass_bush_bmm" ,"0" , []),
 
 ("flora_flowersa" ,sokf_handle_as_flora,"grass_bush_cmm" ,"0" , []),
 ("flora_flowersb" ,sokf_handle_as_flora,"grass_bush_c2mm" ,"0" , []),
 ("flora_flowersc" ,sokf_handle_as_flora,"grass_bush_c3mm" ,"0" , []),
 ("flora_flowersd" ,sokf_handle_as_flora,"grass_bush_dmm" ,"0" , []),

 ("flora_flowers2a" ,sokf_handle_as_flora,"grass_bush_emm" ,"0" , []),
 ("flora_flowers2b" ,sokf_handle_as_flora,"grass_bush_fmm" ,"0" , []),
 ("flora_flowers2c" ,sokf_handle_as_flora,"grass_bush_gmm" ,"0" , []),
 ("flora_flowers2d" ,sokf_handle_as_flora,"grass_bush_hmm" ,"0" , []),
 ("flora_flowers2e" ,sokf_handle_as_flora,"grass_bush_imm" ,"0" , []),
 ("flora_flowers2f" ,sokf_handle_as_flora,"grass_bush_jmm" ,"0" , []),
 ("flora_flowers2g" ,sokf_handle_as_flora,"grass_bush_kmm" ,"0" , []),
 ("flora_flowers2h" ,sokf_handle_as_flora,"grass_bush_lmm" ,"0" , []),
 ("flora_flowers2i" ,sokf_handle_as_flora,"grass_bush_mmm" ,"0" , []),

 ("flora_mushrooms" ,sokf_handle_as_flora,"mm_mushrooms2" ,"0" , []),

 ("flora_bush_greena" ,sokf_handle_as_flora,"mm_bush" ,"0" , []),
 ("flora_bush_greenb" ,sokf_handle_as_flora,"mm_bush2" ,"0" , []),
 ("flora_bush_greenc" ,sokf_handle_as_flora,"mm_bush3" ,"0" , []),
 ("flora_bush_greend" ,sokf_handle_as_flora,"mm_bush4" ,"0" , []),
 ("flora_bush_greene" ,sokf_handle_as_flora,"mm_bush5" ,"0" , []),
 ("flora_bush_greenf" ,sokf_handle_as_flora,"mm_bush6" ,"0" , []),
 ("flora_bush_greeng" ,sokf_handle_as_flora,"mm_bush7" ,"0" , []),

 ("flora_bush_orangea" ,sokf_handle_as_flora,"mm_bush_new" ,"0" , []),
 ("flora_bush_orangeb" ,sokf_handle_as_flora,"mm_bush_new2" ,"0" , []),
 ("flora_bush_orangec" ,sokf_handle_as_flora,"mm_bush_new3" ,"0" , []),
 ("flora_bush_oranged" ,sokf_handle_as_flora,"mm_bush_new4" ,"0" , []),
 ("flora_bush_orangee" ,sokf_handle_as_flora,"mm_bush_new5" ,"0" , []),
 ("flora_bush_orangef" ,sokf_handle_as_flora,"mm_bush_new6" ,"0" , []),
 ("flora_bush_orangeg" ,sokf_handle_as_flora,"mm_bush_new7" ,"0" , []),

 ("flora_giant_busha" ,sokf_handle_as_flora,"mm_giant_bush" ,"0" , []),
 ("flora_giant_bushb" ,sokf_handle_as_flora,"mm_giant_bush2" ,"0" , []),
 ("flora_giant_bushc" ,sokf_handle_as_flora,"mm_giant_bush3" ,"0" , []),
 ("flora_giant_bushd" ,sokf_handle_as_flora,"mm_giant_bush4" ,"0" , []),
 ("flora_giant_bushe" ,sokf_handle_as_flora,"mm_giant_bush5" ,"0" , []),
 ("flora_giant_bushf" ,sokf_handle_as_flora,"mm_giant_bush6" ,"0" , []),
 ("flora_giant_bushg" ,sokf_handle_as_flora,"mm_giant_bush7" ,"0" , []),

 ("flora_old_busha" ,sokf_handle_as_flora,"mm_giant_bush_new" ,"0" , []),
 ("flora_old_bushb" ,sokf_handle_as_flora,"mm_giant_bush_new2" ,"0" , []),
 ("flora_old_bushc" ,sokf_handle_as_flora,"mm_giant_bush_new3" ,"0" , []),
 ("flora_old_bushd" ,sokf_handle_as_flora,"mm_giant_bush_new4" ,"0" , []),
 ("flora_old_bushe" ,sokf_handle_as_flora,"mm_giant_bush_new5" ,"0" , []),
 ("flora_old_bushf" ,sokf_handle_as_flora,"mm_giant_bush_new6" ,"0" , []),
 ("flora_old_bushg" ,sokf_handle_as_flora,"mm_giant_bush_new7" ,"0" , []),
 
 ("flora_old_bush1a" ,sokf_handle_as_flora,"mm_old_bush" ,"0" , []),
 ("flora_old_bush1b" ,sokf_handle_as_flora,"mm_old_bush2" ,"0" , []),
 ("flora_old_bush1c" ,sokf_handle_as_flora,"mm_old_bush3" ,"0" , []),
 ("flora_old_bush1d" ,sokf_handle_as_flora,"mm_old_bush4" ,"0" , []),
 ("flora_old_bush1e" ,sokf_handle_as_flora,"mm_old_bush5" ,"0" , []),
 ("flora_old_bush1f" ,sokf_handle_as_flora,"mm_old_bush6" ,"0" , []),
 ("flora_old_bush1g" ,sokf_handle_as_flora,"mm_old_bush7" ,"0" , []),

 ("flora_flower_busha" ,sokf_handle_as_flora,"bush_flower" ,"0" , []),
 ("flora_flower_bushb" ,sokf_handle_as_flora,"bush_flower2" ,"0" , []),
 ("flora_flower_bushc" ,sokf_handle_as_flora,"bush_flower3" ,"0" , []),
 ("flora_flower_bushd" ,sokf_handle_as_flora,"bush_flower4" ,"0" , []),
 ("flora_flower_bushe" ,sokf_handle_as_flora,"bush_flower5" ,"0" , []),
 ("flora_flower_bushf" ,sokf_handle_as_flora,"bush_flower6" ,"0" , []),
 ("flora_flower_bushg" ,sokf_handle_as_flora,"bush_flower7" ,"0" , []),  
 ("flora_flower_bushh" ,sokf_handle_as_flora,"bush_flower8" ,"0" , []),
 ("flora_flower_bushi" ,sokf_handle_as_flora,"bush_flower9" ,"0" , []),
 ("flora_flower_bushk" ,sokf_handle_as_flora,"bush_flower11" ,"0" , []),
 ("flora_flower_bushl" ,sokf_handle_as_flora,"bush_flower12" ,"0" , []),
 ("flora_flower_bushm" ,sokf_handle_as_flora,"bush_flower13" ,"0" , []),
 ("flora_flower_bushn" ,sokf_handle_as_flora,"bush_flower14" ,"0" , []),
 ("flora_flower_busho" ,sokf_handle_as_flora,"bush_flower15" ,"0" , []),
 ("flora_flower_bushp" ,sokf_handle_as_flora,"bush_flower16" ,"0" , []),
 ("flora_flower_bushq" ,sokf_handle_as_flora,"bush_flower17" ,"0" , []),
 ("flora_flower_bushr" ,sokf_handle_as_flora,"bush_flower18" ,"0" , []),
 ("flora_flower_bushs" ,sokf_handle_as_flora,"bush_flower19" ,"0" , []),
 ("flora_flower_busht" ,sokf_handle_as_flora,"bush_flower20" ,"0" , []),  

 ("flora_bush_green_newa" ,sokf_handle_as_flora,"bush_new_green1" ,"0" , []),
 ("flora_bush_green_newb" ,sokf_handle_as_flora,"bush_new_green2" ,"0" , []),
 ("flora_bush_green_newc" ,sokf_handle_as_flora,"bush_new_green3" ,"0" , []),
 ("flora_bush_green_newd" ,sokf_handle_as_flora,"bush_new_green4" ,"0" , []),
 ("flora_bush_green_newe" ,sokf_handle_as_flora,"bush_new_green5" ,"0" , []),
 ("flora_bush_green_newf" ,sokf_handle_as_flora,"bush_new_green6" ,"0" , []),
 ("flora_bush_green_newg" ,sokf_handle_as_flora,"bush_new_green7" ,"0" , []),

 ("flora_bush_wintera" ,sokf_handle_as_flora,"mm_bush_winter" ,"0" , []),
 ("flora_bush_winterb" ,sokf_handle_as_flora,"mm_bush_winter2" ,"0" , []),
 ("flora_bush_winterc" ,sokf_handle_as_flora,"mm_bush_winter3" ,"0" , []),
 ("flora_bush_winterd" ,sokf_handle_as_flora,"mm_bush_winter4" ,"0" , []),
 ("flora_bush_wintere" ,sokf_handle_as_flora,"mm_bush_winter5" ,"0" , []),
 ("flora_bush_winterf" ,sokf_handle_as_flora,"mm_bush_winter6" ,"0" , []),
 ("flora_bush_winterg" ,sokf_handle_as_flora,"mm_bush_winter7" ,"0" , []),  
 ("flora_bush_winterh" ,sokf_handle_as_flora,"mm_bush_winter8" ,"0" , []),
 ("flora_bush_winteri" ,sokf_handle_as_flora,"mm_bush_winter9" ,"0" , []),
 ("flora_bush_winterj" ,sokf_handle_as_flora,"mm_bush_winter10" ,"0" , []),  
  
 ("flora_bush_winter2a" ,sokf_handle_as_flora,"mm_bush_winter14" ,"0" , []),
 ("flora_bush_winter2b" ,sokf_handle_as_flora,"mm_bush_winter15" ,"0" , []),
 ("flora_bush_winter2c" ,sokf_handle_as_flora,"mm_bush_winter16" ,"0" , []),
 ("flora_bush_winter2d" ,sokf_handle_as_flora,"mm_bush_winter17" ,"0" , []),

 ("flora_roses" ,sokf_handle_as_flora,"roses" ,"0" , []),  

 ("flora_buddy_planta" ,sokf_handle_as_flora,"buddy_plant" ,"0" , []),  
 ("flora_buddy_plantb" ,sokf_handle_as_flora,"buddy_plant_b" ,"0" , []),  
 
 ("flora_cattail1" ,sokf_handle_as_flora,"cattail1" ,"0" , []),  
 ("flora_cattail2" ,sokf_handle_as_flora,"cattail2" ,"0" , []),  
 ("flora_cattail3" ,sokf_handle_as_flora,"cattail3" ,"0" , []),  
 ("flora_cattail4" ,sokf_handle_as_flora,"cattail4" ,"0" , []),  
 ("flora_cattail5" ,sokf_handle_as_flora,"cattail5" ,"0" , []),  
 ("flora_cattail6" ,sokf_handle_as_flora,"cattail6" ,"0" , []),  
 ("flora_cattail7" ,sokf_handle_as_flora,"cattail7" ,"0" , []),  
 ("flora_lilly1" ,sokf_handle_as_flora,"lilly1" ,"0" , []),  
 
("aagreenscreen" ,0,"greenscreen" ,"0" , []),

   # Spanish buildings
    ("spanish" ,0,"spanish" ,"bo_spanish" , []),
    ("spanish1" ,0,"spanish1" ,"bo_spanish1" , []),
    ("spanish2" ,0,"spanish2" ,"bo_spanish2" , []),
    ("spanish3" ,0,"spanish3" ,"bo_spanish3" , []),
    ("spanish4" ,0,"spanish4" ,"bo_spanish4" , []),
    ("spanish5" ,0,"spanish5" ,"bo_spanish5" , []),
    ("spanish6" ,0,"spanish6" ,"bo_spanish6" , []),
    ("spanish7" ,0,"spanish7" ,"bo_spanish7" , []),
    ("spanish8" ,0,"spanish8" ,"bo_spanish8" , []),
    ("spanish9" ,0,"spanish9" ,"bo_spanish9" , []),
    ("spanish10" ,0,"spanish10" ,"bo_spanish10" , []),
    ("spanish11" ,0,"spanish11" ,"bo_spanish11" , []),
    ("spanish12" ,0,"spanish12" ,"bo_spanish12" , []),
    ("spanish13" ,0,"spanish13" ,"bo_spanish13" , []),
    ("spanish14" ,0,"spanish14" ,"bo_spanish14" , []),
    ("spanish15" ,0,"spanish15" ,"bo_spanish15" , []),
    ("spanish16" ,0,"spanish16" ,"bo_spanish16" , []),
    ("spanishwallcorner" ,0,"spanishwallcorner" ,"bo_spanishwallcorner" , []),
    ("spanishwallgate" ,0,"spanishwallgate" ,"bo_spanishwallgate" , []),


  ("mm_watersplash",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
      (store_trigger_param_1,":instance_id"),
    
      (store_random_in_range,":cur_time",1,3), #0-2 sec until first burst
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"), #Initial time until first particle burst in sec
                                                                               #delete the random and change cur_time to a value
                                                                               #to set this to the same for all props
    ]),
   ]),


  ("mm_ambient_insects2",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
      (store_trigger_param_1,":instance_id"),
    
      (store_random_in_range,":cur_time",1,3), #0-2 sec until first burst
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"), #Initial time until first particle burst in sec
                                                                               #delete the random and change cur_time to a value
                                                                               #to set this to the same for all props
    ]),
   ]),


  ("mm_ambient_insects1",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
      (store_trigger_param_1,":instance_id"),
    
      (store_random_in_range,":cur_time",1,3), #0-2 sec until first burst
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"), #Initial time until first particle burst in sec
                                                                               #delete the random and change cur_time to a value
                                                                               #to set this to the same for all props
    ]),
   ]),


  ("mm_ambient_insects",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
      (store_trigger_param_1,":instance_id"),
    
      (store_random_in_range,":cur_time",1,3), #0-2 sec until first burst
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"), #Initial time until first particle burst in sec
                                                                               #delete the random and change cur_time to a value
                                                                               #to set this to the same for all props
    ]),
   ]),


 # la haye saint
    ("mm_la_haye1" ,0,"la_haye_saint" ,"bo_la_haye_saint" , []),
    ("mm_la_haye2" ,0,"la_haye_saint" ,"bo_la_haye_saint" , []),
    ("mm_la_haye3" ,0,"la_haye_saint2" ,"bo_la_haye_saint2" , []),
    ("mm_la_haye4" ,0,"la_haye_saint3" ,"bo_la_haye_saint3" , []),
    ("mm_la_haye5" ,0,"la_haye_saint4" ,"bo_la_haye_saint4" , []),
    ("mm_la_haye6" ,0,"la_haye_saint5" ,"bo_la_haye_saint5" , []),
    ("mm_la_haye7" ,0,"la_haye_saint6" ,"bo_la_haye_saint6" , []),	


    ("mm_ammunition_depot" ,0,"ammunition_depot" ,"ammunition_depot_collision" , []),
    ("mm_gabion" ,0,"gabion" ,"gabion_collision" , []),
    ("mm_gunnest" ,0,"gunnest" ,"gunnest_collision" , []),
    
    ("mm_gabiondeploy" ,0,"gabiondeploy" ,"bo_gabiondeploy" , []),
        
    #mill

    ("mm_mill2" ,0,"mmmill2" ,"bo_sp_poor_village_houses9" , []),
    
    # New house
    ("mm_house_ornament1" ,0,"1owall" ,"0" , []),
    ("mm_house_ornament2" ,0,"2owall" ,"0" , []),
    
    ("mm_house_stair1" ,0,"stair" ,"bo_stair" , []),
    ("mm_house_stair2" ,0,"stair2" ,"bo_stair2" , []),
    ("mm_house_stair3" ,0,"stair3" ,"bo_stair3" , []),
    
    ("mm_house_basic1" ,0,"formen" ,"bo_formen" , []),
    #("mm_house_basic2" ,0,"formen2" ,"bo_formen2" , []),
    ("mm_house_basic3" ,0,"formen3" ,"bo_formen3" , []),
    ("mm_house_basic4" ,0,"formen4" ,"bo_formen4" , []),
    ("mm_house_basic5" ,0,"formen5" ,"bo_formen5" , []),
    ("mm_house_basic6" ,0,"formen6" ,"bo_formen6" , []),
    ("mm_house_basic7" ,0,"formen7" ,"bo_formen7" , []),
    ("mm_house_basic8" ,0,"formen8" ,"bo_formen8" , []),
    ("mm_house_basic9" ,0,"formen9" ,"bo_formen9" , []),
    ("mm_house_basic10" ,0,"formen10" ,"bo_formen10" , []),
    ("mm_house_basic11" ,0,"formen11" ,"bo_formen11" , []),
    ("mm_house_basic12" ,0,"formen12" ,"bo_formen12" , []),
    ("mm_house_basic13" ,0,"formen13" ,"bo_formen13" , []),
    ("mm_house_basic14" ,0,"formen14" ,"bo_formen14" , []),

     
    ("mm_1housebuild" ,0,"1housebuild" ,"bo_1housebuild" , []),
    ("mm_2housebuild" ,0,"2housebuild" ,"bo_2housebuild" , []),
    ("mm_3housebuild" ,0,"3housebuild" ,"bo_3housebuild" , []),
    ("mm_4housebuild" ,0,"4housebuild" ,"bo_4housebuild" , []),
    ("mm_5housebuild" ,0,"5housebuild" ,"bo_5housebuild" , []),
    ("mm_6housebuild" ,0,"6housebuild" ,"bo_6housebuild" , []),
    ("mm_7housebuild" ,0,"7housebuild" ,"bo_7housebuild" , []),
    ("mm_8housebuild" ,0,"8housebuild" ,"bo_8housebuild" , []),
    ("mm_9housebuild" ,0,"9housebuild" ,"bo_9housebuild" , []),
    ("mm_10housebuild" ,0,"10housebuild" ,"bo_10housebuild" , []),
    ("mm_11housebuild" ,0,"11housebuild" ,"bo_11housebuild" , []),

    ("mm_11_brick_housebuild" ,0,"11_brick_housebuild" ,"bo_11housebuild" , []),

    ("mm_12housebuild" ,0,"12housebuild" ,"bo_12housebuild" , []),
    ("mm_13housebuild" ,0,"13housebuild" ,"bo_13housebuild" , []),
    ("mm_14housebuild" ,0,"14housebuild" ,"bo_14housebuild" , []),
    ("mm_15housebuild" ,0,"15housebuild" ,"bo_15housebuild" , []),
    ("mm_16housebuild" ,0,"16housebuild" ,"bo_16housebuild" , []),
    ("mm_17housebuild" ,0,"17housebuild" ,"bo_17housebuild" , []),
    ("mm_18housebuild" ,0,"18housebuild" ,"bo_18housebuild" , []),
    ("mm_19housebuild" ,0,"19housebuild" ,"bo_19housebuild" , []),
    ("mm_20housebuild" ,0,"20housebuild" ,"bo_20housebuild" , []),

    
    ("new_mm_1housebuild" ,0,"new_1housebuild" ,"bo_1housebuild" , []),
    ("new_mm_2housebuild" ,0,"new_2housebuild" ,"bo_2housebuild" , []),
    ("new_mm_3housebuild" ,0,"new_3housebuild" ,"bo_3housebuild" , []),
    ("new_mm_4housebuild" ,0,"new_4housebuild" ,"bo_4housebuild" , []),
    ("new_mm_5housebuild" ,0,"new_5housebuild" ,"bo_5housebuild" , []),
    ("new_mm_6housebuild" ,0,"new_6housebuild" ,"bo_6housebuild" , []),
    ("new_mm_7housebuild" ,0,"new_7housebuild" ,"bo_7housebuild" , []),
    ("new_mm_8housebuild" ,0,"new_8housebuild" ,"bo_8housebuild" , []),
    ("new_mm_9housebuild" ,0,"new_9housebuild" ,"bo_9housebuild" , []),
    ("new_mm_10housebuild" ,0,"new_10housebuild" ,"bo_10housebuild" , []),
    ("new_mm_11housebuild" ,0,"new_11housebuild" ,"bo_11housebuild" , []),
    ("new_mm_12housebuild" ,0,"new_12housebuild" ,"bo_12housebuild" , []),
    ("new_mm_13housebuild" ,0,"new_13housebuild" ,"bo_13housebuild" , []),
    ("new_mm_14housebuild" ,0,"new_14housebuild" ,"bo_14housebuild" , []),
    ("new_mm_15housebuild" ,0,"new_15housebuild" ,"bo_15housebuild" , []),
    ("new_mm_16housebuild" ,0,"new_16housebuild" ,"bo_16housebuild" , []),
    ("new_mm_17housebuild" ,0,"new_17housebuild" ,"bo_17housebuild" , []),
    ("new_mm_18housebuild" ,0,"new_18housebuild" ,"bo_18housebuild" , []),
    ("new_mm_19housebuild" ,0,"new_19housebuild" ,"bo_19housebuild" , []),
    ("new_mm_20housebuild" ,0,"new_20housebuild" ,"bo_20housebuild" , []),



    ("mm_build_church_tower" ,0,"church_tower" ,"bo_church_tower" , []),
    ("mm_build_church1" ,0,"church_building" ,"bo_church_building" , []),
    ("mm_build_church2" ,0,"church_building1" ,"bo_church_building" , []),

    ("mm_build_church_bell",0,"church_bell" ,"bo_church_bell" , []),
    ("mm_build_church_bellmov",sokf_static_movement,"church_bellmov" ,"0" , []),
    ("mm_build_church_rope",spr_use_time(1),"church_rope" ,"bo_church_rope" , [
     (ti_on_scene_prop_use,
      [
        (this_or_next|multiplayer_is_server),
        (neg|game_in_multiplayer_mode),
        #(store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":rope_instance"),
        (prop_instance_get_position,pos3,":rope_instance"),
        (scene_prop_get_num_instances,":num_bells","spr_mm_build_church_bellmov"),
        (gt,":num_bells",0),
        
        (assign,":max_dist",999999),
        (try_for_prop_instances, ":bell_instance", "spr_mm_build_church_bellmov", somt_object),
          (prop_instance_get_position,pos1,":bell_instance"),
          (get_distance_between_positions,":dist",pos1,pos3),
          (lt,":dist",":max_dist"),
          (assign,":max_dist",":dist"),
          (assign,":use_bell_instance",":bell_instance"),
        (try_end),
        (scene_prop_get_slot,":bell_state",":use_bell_instance",scene_prop_slot_time),
        (neg|is_between,":bell_state",1,7),
        (scene_prop_set_slot,":use_bell_instance",scene_prop_slot_time,6),
      ]),
     ]),



    ("mm_woodenhouse" ,0,"woodenhouse" ,"bo_woodenhouse" , []),
    ("mm_woodensnowhouse" ,0,"woodensnowhouse" ,"bo_woodenhouse" , []),
    ("mm_woodenhouse2story" ,0,"woodenhouse2story" ,"bo_woodenhouse2story" , []),
    ("mm_woodenhouse2story2" ,0,"woodenhouse2story2" ,"bo_woodenhouse2story" , []),
    ("mm_woodenhouse2story3" ,0,"woodenhouse2story3" ,"bo_woodenhouse2story" , []),
    ("mm_woodenhouse2story4" ,0,"woodenhouse2story4" ,"bo_woodenhouse2story" , []),
    ("mm_woodenhouse2storysnowy" ,0,"woodenhouse2storysnowy" ,"bo_woodenhouse2story" , []),
    ("mm_woodenhouse2storysnowy2" ,0,"woodenhouse2storysnowy2" ,"bo_woodenhouse2story" , []),

    #Siege tunnel
    ("mm_tunnel_entrance" ,0,"mmtunnel1" ,"bo_mmtunnel1" , []),
    ("mm_tunnel" ,0,"mmtunnel2" ,"bo_mmtunnel2" , []),

    #iceprops
   ("mm_ice1" ,0,"ice1" ,"bo_ice1" , []),
   ("mm_ice2" ,0,"ice2" ,"bo_ice2" , []),
   ("mm_ice3" ,0,"ice3" ,"bo_ice3" , []),
   ("mm_ice4" ,0,"ice4" ,"bo_ice4" , []),

    
    # Windows.
    ("mm_window1_poor",sokf_static_movement|sokf_destructible,"window1_poor","bo_window1", [check_mm_on_destroy_window_trigger,]),
    ("mm_window2_poor",sokf_static_movement|sokf_destructible,"window2_poor","bo_window2", [check_mm_on_destroy_window_trigger,]),
    ("mm_window1",sokf_static_movement|sokf_destructible,"window1","bo_window1", [check_mm_on_destroy_window_trigger,]),
    ("mm_window2",sokf_static_movement|sokf_destructible,"window2","bo_window2", [check_mm_on_destroy_window_trigger,]),

    ("mm_window1d_poor",sokf_static_movement,"window1d_poor","0", []),
    ("mm_window2d_poor",sokf_static_movement,"window2d_poor","0", []),   
    ("mm_window1d",sokf_static_movement,"window1d","0", []),
    ("mm_window2d",sokf_static_movement,"window2d","0", []),
    
    ("mm_window3_poor",sokf_static_movement|sokf_destructible,"window_old_walls1_poor","bo_window_old_walls", [check_mm_on_destroy_window_trigger,]),
    ("mm_window4_poor",sokf_static_movement|sokf_destructible,"window_repos1_poor","bo_window_repos", [check_mm_on_destroy_window_trigger,]),
    ("mm_window3",sokf_static_movement|sokf_destructible,"window_old_walls1","bo_window_old_walls", [check_mm_on_destroy_window_trigger,]),
    ("mm_window4",sokf_static_movement|sokf_destructible,"window_repos1","bo_window_repos", [check_mm_on_destroy_window_trigger,]),
    
    ("mm_window3d_poor",sokf_static_movement,"window_old_walls1d_poor","0", []),
    ("mm_window4d_poor",sokf_static_movement,"window_repos1d_poor","0", []),   
    ("mm_window3d",sokf_static_movement,"window_old_walls1d","0", []),
    ("mm_window4d",sokf_static_movement,"window_repos1d","0", []),
    
    ("mm_windows_end",0,"0","0", []),

    
    # Destroyable props begin
    
    # New walls
    ("mm_house_wall_1" ,sokf_static_movement,"1wall" ,"bo_1wall" , []),
    ("mm_house_wall_1d" ,sokf_static_movement,"1dwall" ,"bo_1dwall" , []),
    ("mm_house_wall_2" ,sokf_static_movement,"2wall" ,"bo_2wall" , []),
    ("mm_house_wall_2d" ,sokf_static_movement,"2dwall" ,"bo_2dwall" , []),
    ("mm_house_wall_3" ,sokf_static_movement,"3wall" ,"bo_3wall" , []),
    ("mm_house_wall_3d" ,sokf_static_movement,"3dwall" ,"bo_3dwall" , []),
    ("mm_house_wall_4" ,sokf_static_movement,"4wall" ,"bo_4wall" , []),
    ("mm_house_wall_4d" ,sokf_static_movement,"4dwall" ,"bo_4dwall" , []),
    ("mm_house_wall_5" ,sokf_static_movement,"5wall" ,"bo_5wall" , []),
    ("mm_house_wall_5d" ,sokf_static_movement,"5dwall" ,"bo_5dwall" , []),
    ("mm_house_wall_6" ,sokf_static_movement,"6wall" ,"bo_6wall" , []),
    ("mm_house_wall_6d" ,sokf_static_movement,"6dwall" ,"bo_6dwall" , []),
    ("mm_house_wall_7" ,sokf_static_movement,"7wall" ,"bo_7wall" , []),
    ("mm_house_wall_7d" ,sokf_static_movement,"7dwall" ,"bo_7dwall" , []),
    ("mm_house_wall_11" ,sokf_static_movement,"11wall" ,"bo_11wall" , []),
    ("mm_house_wall_11d" ,sokf_static_movement,"11dwall" ,"bo_11dwall" , []),
    ("mm_house_wall_21" ,sokf_static_movement,"21wall" ,"bo_21wall" , []),
    ("mm_house_wall_21d" ,sokf_static_movement,"21dwall" ,"bo_21dwall" , []),
    ("mm_house_wall_31" ,sokf_static_movement,"31wall" ,"bo_31wall" , []),
    ("mm_house_wall_31d" ,sokf_static_movement,"31dwall" ,"bo_31dwall" , []),
    ("mm_house_wall_41" ,sokf_static_movement,"41wall" ,"bo_41wall" , []),
    ("mm_house_wall_41d" ,sokf_static_movement,"41dwall" ,"bo_41dwall" , []),
    ("mm_house_wall_51" ,sokf_static_movement,"51wall" ,"bo_51wall" , []),
    ("mm_house_wall_51d" ,sokf_static_movement,"51dwall" ,"bo_51dwall" , []),
    ("mm_house_wall_61" ,sokf_static_movement,"61wall" ,"bo_61wall" , []),
    ("mm_house_wall_61d" ,sokf_static_movement,"61dwall" ,"bo_61dwall" , []),
    ("mm_house_wall_71" ,sokf_static_movement,"71wall" ,"bo_71wall" , []),
    ("mm_house_wall_71d" ,sokf_static_movement,"71dwall" ,"bo_71dwall" , []),
    
    ("mm_wall1", sokf_static_movement|sokf_dont_move_agent_over, "wall1", "bo_desertWall1" , []),
	  ("mm_wall1d", sokf_static_movement|sokf_dont_move_agent_over, "wall1d", "bo_desertWall1d" , []),
	  ("mm_wall1dd", sokf_static_movement|sokf_dont_move_agent_over, "wall1dd", "bo_desertWall1dd" , []),
    
    ("mm_walldesert1", sokf_static_movement|sokf_dont_move_agent_over, "desertWall1", "bo_desertWall1" , []),
    ("mm_walldesert1d", sokf_static_movement|sokf_dont_move_agent_over, "desertWall1d", "bo_desertWall1d" , []),
    ("mm_walldesert1dd", sokf_static_movement|sokf_dont_move_agent_over, "desertWall1dd", "bo_desertWall1dd" , []),
    
    ("mm_wallwood1", sokf_static_movement|sokf_dont_move_agent_over, "woodWall1", "bo_woodWall1" , []),
    ("mm_wallwood1d", sokf_static_movement|sokf_dont_move_agent_over, "woodWall1d", "bo_woodWall1d" , []),
    ("mm_wallwood1dd", sokf_static_movement|sokf_dont_move_agent_over, "woodWall1dd", "bo_woodWall1dd" , []),
	
    ("mm_wall3", sokf_static_movement|sokf_dont_move_agent_over, "wall3", "wall3_collision" , []),
    ("mm_wall4", sokf_static_movement|sokf_dont_move_agent_over, "wall4", "wall4_collision" , []),
    ("mm_wall5", sokf_static_movement|sokf_dont_move_agent_over, "wall5", "wall5_collision" , []),
  
    ("mm_stockade" ,sokf_static_movement,"stockade" ,"stockade_collision" , []),
    ("mm_stockade_cannon" ,sokf_static_movement,"stockade_cannon" ,"stockade_cannon_collision" , []),
    
    ("mm_palisade", sokf_static_movement, "mmpalisade", "bo_mmpalisade" , []),
    ("mm_palisaded", sokf_static_movement, "mmpalisaded", "bo_mmpalisaded" , []),
    ("mm_sp_poor_bridge1", sokf_static_movement|sokf_dont_move_agent_over, "sp_poor_village_bridge1", "bo_sp_poor_village_bridge1" , []),
    ("mm_pontoon_bridge1", sokf_static_movement|sokf_dont_move_agent_over, "pontoon", "bo_pontoon" , []),
    ("mm_pontoon_bridge2", sokf_static_movement|sokf_dont_move_agent_over, "pontoon2", "bo_pontoon" , []),
    ("mm_earthwork1", sokf_static_movement, "earthwork1", "bo_earthwork1" , []),
    
    ("fortnew", sokf_static_movement|sokf_dont_move_agent_over, "fortnew", "bo_fortnew" , []),
    ("fortnew1", sokf_static_movement|sokf_dont_move_agent_over, "fortnew1", "bo_fortnew" , []),
    ("fortnew2", sokf_static_movement|sokf_dont_move_agent_over, "fortnew2", "bo_fortnew" , []),
    ("fortnew3", sokf_static_movement|sokf_dont_move_agent_over, "fortnew3", "bo_fortnew" , []),
    ("fortnew4", sokf_static_movement|sokf_dont_move_agent_over, "fortnew4", "bo_fortnew" , []),
    ("fortnew5", sokf_static_movement|sokf_dont_move_agent_over, "fortnew5", "bo_fortnew5" , []),
    ("fortnew6", sokf_static_movement|sokf_dont_move_agent_over, "fortnew6", "bo_fortnew6" , []),
    ("fortnew7", sokf_static_movement|sokf_dont_move_agent_over, "fortnew7", "bo_fortnew6" , []),
    ("fortnew8", sokf_static_movement|sokf_dont_move_agent_over, "fortnew8", "bo_fortnew8" , []),

    ("fortnew_1", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_1", "bo_fortnew_1" , []),
    ("fortnew_12", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_12", "bo_fortnew_1" , []),
    ("fortnew_13", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_13", "bo_fortnew_1" , []),
    ("fortnew_14", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_14", "bo_fortnew_1" , []),
    ("fortnew_15", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_15", "bo_fortnew_1" , []),
    ("fortnew_16", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_16", "bo_fortnew_1" , []),
    ("fortnew_17", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_17", "bo_fortnew_17" , []),
    ("fortnew_18", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_18", "bo_fortnew_17" , []),
    ("fortnew_19", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_19", "bo_fortnew_19" , []),
    ("fortnew_110", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_110", "bo_fortnew_110" , []),

    ("fortnew_2", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_2", "bo_fortnew_2" , []),
    ("fortnew_21", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_21", "bo_fortnew_2" , []),
    ("fortnew_22", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_22", "bo_fortnew_2" , []),
    ("fortnew_23", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_23", "bo_fortnew_2" , []),
    ("fortnew_24", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_24", "bo_fortnew_2" , []),
    ("fortnew_25", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_25", "bo_fortnew_2" , []),
    ("fortnew_26", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_26", "bo_fortnew_2" , []),
    ("fortnew_27", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_27", "bo_fortnew_2" , []),
    ("fortnew_28", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_28", "bo_fortnew_2" , []),

    ("fortnew_3", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_3", "bo_fortnew_3" , []),
    ("fortnew_31", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_31", "bo_fortnew_3" , []),
    ("fortnew_32", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_32", "bo_fortnew_3" , []),
    ("fortnew_33", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_33", "bo_fortnew_3" , []),
    ("fortnew_34", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_34", "bo_fortnew_3" , []),
    ("fortnew_35", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_35", "bo_fortnew_3" , []),
    ("fortnew_36", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_36", "bo_fortnew_36" , []),
    ("fortnew_37", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_37", "bo_fortnew_36" , []),
    ("fortnew_38", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_38", "bo_fortnew_38" , []),

    ("fortnew_4", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_4", "bo_fortnew_4" , []),
    
    ("mm_new_wall_1_1" ,sokf_static_movement,"newall1" ,"bo_newall1" , []),
    ("mm_new_wall_1_1d" ,sokf_static_movement,"newall1d" ,"bo_newall1" , []),
    ("mm_new_wall_1_2" ,sokf_static_movement,"newall2" ,"bo_newall1" , []),
    ("mm_new_wall_1_2d" ,sokf_static_movement,"newall2d" ,"bo_newall1" , []),
    ("mm_new_wall_1_3" ,sokf_static_movement,"newall3" ,"bo_newall1" , []),
    ("mm_new_wall_1_3d" ,sokf_static_movement,"newall3d" ,"bo_newall1" , []),
    ("mm_new_wall_1_4" ,sokf_static_movement,"newall4" ,"bo_newall1" , []),
    ("mm_new_wall_1_4d" ,sokf_static_movement,"newall4d" ,"bo_newall1" , []),
    ("mm_new_wall_1_5" ,sokf_static_movement,"newall5" ,"bo_newall5" , []),
    ("mm_new_wall_1_5d" ,sokf_static_movement,"newall5d" ,"bo_newall5" , []),
    ("mm_new_wall_1_6" ,sokf_static_movement,"newall6" ,"bo_newall6" , []),
    ("mm_new_wall_1_6d" ,sokf_static_movement,"newall6d" ,"bo_newall6" , []),
    ("mm_new_wall_1_7" ,sokf_static_movement,"newall7" ,"bo_newall7" , []),
    ("mm_new_wall_1_7d" ,sokf_static_movement,"newall7d" ,"bo_newall7" , []),
    ("mm_new_wall_1_8" ,sokf_static_movement,"newall8" ,"bo_newall8" , []),
    ("mm_new_wall_1_8d" ,sokf_static_movement,"newall8d" ,"bo_newall8" , []),
    ("mm_new_wall_1_9" ,sokf_static_movement,"newall9" ,"bo_newall7" , []),
    ("mm_new_wall_1_9d" ,sokf_static_movement,"newall9d" ,"bo_newall7" , []),
    ("mm_new_wall_1_10" ,sokf_static_movement,"newall10" ,"bo_newall10" , []),
    ("mm_new_wall_1_10d" ,sokf_static_movement,"newall10d" ,"bo_newall10" , []),
    ("mm_new_wall_1_11" ,sokf_static_movement,"newall11" ,"bo_newall7" , []),
    ("mm_new_wall_1_11d" ,sokf_static_movement,"newall11d" ,"bo_newall7" , []),
    
    ("mm_new_wall_2_1" ,sokf_static_movement,"ne1wall1" ,"bo_newall1" , []),
    ("mm_new_wall_2_1d" ,sokf_static_movement,"ne1wall1d" ,"bo_newall1" , []),
    ("mm_new_wall_2_2" ,sokf_static_movement,"ne1wall2" ,"bo_newall1" , []),
    ("mm_new_wall_2_2d" ,sokf_static_movement,"ne1wall2d" ,"bo_newall1" , []),
    ("mm_new_wall_2_3" ,sokf_static_movement,"ne1wall3" ,"bo_newall1" , []),
    ("mm_new_wall_2_3d" ,sokf_static_movement,"ne1wall3d" ,"bo_newall1" , []),
    ("mm_new_wall_2_4" ,sokf_static_movement,"ne1wall4" ,"bo_newall1" , []),
    ("mm_new_wall_2_4d" ,sokf_static_movement,"ne1wall4d" ,"bo_newall1" , []),
    ("mm_new_wall_2_5" ,sokf_static_movement,"ne1wall5" ,"bo_newall5" , []),
    ("mm_new_wall_2_5d" ,sokf_static_movement,"ne1wall5d" ,"bo_newall5" , []),
    ("mm_new_wall_2_6" ,sokf_static_movement,"ne1wall6" ,"bo_newall6" , []),
    ("mm_new_wall_2_6d" ,sokf_static_movement,"ne1wall6d" ,"bo_newall6" , []),
    ("mm_new_wall_2_7" ,sokf_static_movement,"ne1wall7" ,"bo_newall7" , []),
    ("mm_new_wall_2_7d" ,sokf_static_movement,"ne1wall7d" ,"bo_newall7" , []),
    ("mm_new_wall_2_8" ,sokf_static_movement,"ne1wall8" ,"bo_newall8" , []),
    ("mm_new_wall_2_8d" ,sokf_static_movement,"ne1wall8d" ,"bo_newall8" , []),
    ("mm_new_wall_2_9" ,sokf_static_movement,"ne1wall9" ,"bo_newall7" , []),
    ("mm_new_wall_2_9d" ,sokf_static_movement,"ne1wall9d" ,"bo_newall7" , []),
    ("mm_new_wall_2_10" ,sokf_static_movement,"ne1wall10" ,"bo_newall10" , []),
    ("mm_new_wall_2_10d" ,sokf_static_movement,"ne1wall10d" ,"bo_newall10" , []),
    ("mm_new_wall_2_11" ,sokf_static_movement,"ne1wall11" ,"bo_newall7" , []),
    ("mm_new_wall_2_11d" ,sokf_static_movement,"ne1wall11d" ,"bo_newall7" , []),
    
    ("mm_new_wall_3_1" ,sokf_static_movement,"ne2wall1" ,"bo_newall1" , []),
    ("mm_new_wall_3_1d" ,sokf_static_movement,"ne2wall1d" ,"bo_newall1" , []),
    ("mm_new_wall_3_2" ,sokf_static_movement,"ne2wall2" ,"bo_newall1" , []),
    ("mm_new_wall_3_2d" ,sokf_static_movement,"ne2wall2d" ,"bo_newall1" , []),
    ("mm_new_wall_3_3" ,sokf_static_movement,"ne2wall3" ,"bo_newall1" , []),
    ("mm_new_wall_3_3d" ,sokf_static_movement,"ne2wall3d" ,"bo_newall1" , []),
    ("mm_new_wall_3_4" ,sokf_static_movement,"ne2wall4" ,"bo_newall1" , []),
    ("mm_new_wall_3_4d" ,sokf_static_movement,"ne2wall4d" ,"bo_newall1" , []),
    ("mm_new_wall_3_5" ,sokf_static_movement,"ne2wall5" ,"bo_newall5" , []),
    ("mm_new_wall_3_5d" ,sokf_static_movement,"ne2wall5d" ,"bo_newall5" , []),
    ("mm_new_wall_3_6" ,sokf_static_movement,"ne2wall6" ,"bo_newall6" , []),
    ("mm_new_wall_3_6d" ,sokf_static_movement,"ne2wall6d" ,"bo_newall6" , []),
    ("mm_new_wall_3_7" ,sokf_static_movement,"ne2wall7" ,"bo_newall7" , []),
    ("mm_new_wall_3_7d" ,sokf_static_movement,"ne2wall7d" ,"bo_newall7" , []),
    ("mm_new_wall_3_8" ,sokf_static_movement,"ne2wall8" ,"bo_newall8" , []),
    ("mm_new_wall_3_8d" ,sokf_static_movement,"ne2wall8d" ,"bo_newall8" , []),
    ("mm_new_wall_3_9" ,sokf_static_movement,"ne2wall9" ,"bo_newall7" , []),
    ("mm_new_wall_3_9d" ,sokf_static_movement,"ne2wall9d" ,"bo_newall7" , []),
    ("mm_new_wall_3_10" ,sokf_static_movement,"ne2wall10" ,"bo_newall10" , []),
    ("mm_new_wall_3_10d" ,sokf_static_movement,"ne2wall10d" ,"bo_newall10" , []),
    ("mm_new_wall_3_11" ,sokf_static_movement,"ne2wall11" ,"bo_newall7" , []),
    ("mm_new_wall_3_11d" ,sokf_static_movement,"ne2wall11d" ,"bo_newall7" , []),
    
    # wood walls
    ("mm_woodenwall1" ,sokf_static_movement,"woodenwall1" ,"bo_woodenwall1" , []),
    ("mm_woodenwall1d" ,sokf_static_movement,"woodenwall1d" ,"bo_woodenwall1d" , []),
    ("mm_woodenwall2" ,sokf_static_movement,"woodenwall2" ,"bo_woodenwall2" , []),
    ("mm_woodenwall2d" ,sokf_static_movement,"woodenwall2d" ,"bo_woodenwall2d" , []),
    ("mm_woodenwall3" ,sokf_static_movement,"woodenwall3" ,"bo_woodenwall3" , []),
    ("mm_woodenwall3d" ,sokf_static_movement,"woodenwall3d" ,"bo_woodenwall3d" , []),
    
    ("mm_woodenwallsnowy1" ,sokf_static_movement,"woodenwallsnowy1" ,"bo_woodenwallsnowy1" , []),
    ("mm_woodenwallsnowy1d" ,sokf_static_movement,"woodenwallsnowy1d" ,"bo_woodenwall1d" , []),
    ("mm_woodenwallsnowy2" ,sokf_static_movement,"woodenwallsnowy2" ,"bo_woodenwallsnowy2" , []),
    ("mm_woodenwallsnowy2d" ,sokf_static_movement,"woodenwallsnowy2d" ,"bo_woodenwallsnowy2d" , []),
    ("mm_woodenwallsnowy3" ,sokf_static_movement,"woodenwallsnowy3" ,"bo_woodenwallsnowy3" , []),
    ("mm_woodenwallsnowy3d" ,sokf_static_movement,"woodenwallsnowy3d" ,"bo_woodenwallsnowy3d" , []),
    
    ("mm_sp_rich_bridge4" ,sokf_static_movement|sokf_dont_move_agent_over,"sp_rich_village_bridge13" ,"bo_sp_rich_village_bridge13" , []),
    ("mm_sp_rich_bridge1", sokf_static_movement|sokf_dont_move_agent_over, "sp_rich_village_bridge1", "bo_sp_rich_village_bridge1" , []),
    ("mm_sp_rich_bridge2", sokf_static_movement|sokf_dont_move_agent_over, "sp_rich_village_bridge11", "bo_sp_rich_village_bridge11" , []),
    ("mm_sp_rich_bridge3", sokf_static_movement|sokf_dont_move_agent_over, "sp_rich_village_bridge12", "bo_sp_rich_village_bridge12" , []),
    
    
    ("mm_stakes" ,sokf_static_movement|sokf_dont_move_agent_over,"stackes" ,"stackes_collision" , []),
    ("mm_stakes_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "stackes" , "stackes_collision" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    ("mm_stakes2_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "mmstackes" , "bo_mmstackes" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    ("sandbags_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "sandbags" , "bo_sandbags" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    ("chevaux_de_frise_tri_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "chevaux_de_frise_tri" , "bo_chevaux_de_frise_tri" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    
    ("gabiondeploy_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "gabiondeploy" , "bo_gabiondeploy" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    
    ("mm_fence1", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "mmfence1", "bo_mmfence1" ,
    [    
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    
    ("plank_destructible2" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mm_plank1" ,"bo_mm_plank1" , #patch1115 55/2
    [
       check_common_constructable_prop_on_hit_trigger,
       #check_common_destructible_props_destroy_trigger,
			 check_common_constructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    
    ("earthwork1_destructible", sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible, "earthwork1" ,"bo_earthwork1" , 
     [
       check_common_constructable_prop_on_hit_trigger,
       check_common_destructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    ("mm_destructible_pioneer_builds_end", 0,"0" ,"0" , []),
    
    ("plank_destructible" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mm_plank1" ,"bo_mm_plank1" , #patch1115 55/9
    [
       check_common_constructable_prop_on_hit_trigger,
       #check_common_destructible_props_destroy_trigger,
			 check_common_constructible_props_destroy_trigger,
       (ti_on_scene_prop_use,[]),
    ]),
    
    #Pontoon bridges (contructed props (these are destructible by cannons))
    ("mm_pontoon_bridge_short" ,sokf_static_movement|sokf_dont_move_agent_over,"pontoon_deploy_short" ,"bo_pontoon_deploy_short" , []),
    ("mm_pontoon_bridge_med" ,sokf_static_movement|sokf_dont_move_agent_over,"pontoon_deploy_med" ,"bo_pontoon_deploy_med" , []),
    ("mm_pontoon_bridge_long" ,sokf_static_movement|sokf_dont_move_agent_over,"pontoon_deploy_long" ,"bo_pontoon_deploy_long" , []),

    #Watchtower complete
    ("mm_watchtower" ,sokf_static_movement|sokf_dont_move_agent_over,"deploy_watchtower" ,"bo_deploy_watchtower" , []),
    #Construct props destructs end
    
    
    
    ("mm_dummy",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible,"mm_dummy","bo_arena_archery_target_b",   [
      check_common_dummy_destroy_trigger,
      check_common_dummy_on_hit_trigger,
    ]),   
    
    ("crate_explosive_fra" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(2),"barreltriangulated_fra" ,"barreltriangulated_collision" , [check_common_explosive_crate_use_trigger,]),
    ("crate_explosive_ger" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(2),"barreltriangulated_prus" ,"barreltriangulated_collision" , [check_common_explosive_crate_use_trigger,]),
    ("crate_explosive_rus" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(2),"barreltriangulated_rus" ,"barreltriangulated_collision" , [check_common_explosive_crate_use_trigger,]),
    ("crate_explosive_brit" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(2),"barreltriangulated_brit" ,"barreltriangulated_collision" , [check_common_explosive_crate_use_trigger,]),
    #("crate_explosive_end", 0,"0" ,"0" , []),
    
    # this bird is used as ending for explosive crates!
     ("mm_bird",sokf_static_movement|sokf_destructible,"birdmodel" ,"bo_birdmodel",
     [
       (ti_on_scene_prop_destroy,
        [
          (try_begin),
            (this_or_next|multiplayer_is_server),
            (neg|game_in_multiplayer_mode),

            (store_trigger_param_1, ":instance_no"),
            (prop_instance_get_position, pos1, ":instance_no"),            
            
            (particle_system_burst, "psys_dummy_straw", pos1, 70),
            (particle_system_burst, "psys_bird_blood", pos1, 70),
            
            (call_script,"script_clean_up_prop_instance",":instance_no"),
          (try_end),
        ]),
      ]),
    
    ("mm_ship",sokf_static_movement,"mmboat1","bo_mmboat1", []),
    ("mm_ship_longboat",sokf_static_movement,"longboat","bo_longboat", []),
    ("mm_ship_longboat_1_mast",sokf_static_movement,"longboat_1_mast","bo_longboat", []),
    ("mm_ship_longboat_2_mast",sokf_static_movement,"longboat_2_masts","bo_longboat", []),
    ("mm_ship_gunboat",sokf_static_movement,"gunboat","bo_longboat", []),
    ("mm_ship_rocket_boat",sokf_static_movement,"rocket_boat","bo_longboat", []),
    ("mm_ship_schooner",sokf_static_movement,"schooner","bo_schooner", []),
   # ("ships_end", 0,"0" ,"0" , []),
    
      # doors
  # center all but lenth  (-2.07157,-0.021905),(-0.239644,0.210002),(-1.54562,1.92346)
  
  #This one is used as ending for SHIPS!!
  ("door_destructible",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(2),"tutorial_door_a","bo_tutorial_door_a", [
    check_castle_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,2000),
    ]),
  ]),
  # not center high,len  (-1.37214,0.019246),(-0.026511,0.191006),(0,3.28525)
  ("castle_f_door_a",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_f_door_a","bo_castle_f_door_a", [
    check_castle_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,1000),
    ]),
  ]),
  
  # not center high,len (-1.56653,0.0015),(0,0.202951),(-0.003239,2.55992)
  ("castle_f_sally_door_a",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_f_sally_door_a","bo_castle_f_sally_door_a", [
    check_sally_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,1000),
    ]),
  ]),
  
  # not center high,len  (-1.49895,0.000219),(0.008935,0.157788),(0.00018,2.47752)
  ("castle_e_sally_door_a",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_e_sally_door_a","bo_castle_e_sally_door_a", [
    check_sally_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,3000),
    ]),
  ]),
  
  # not center high,len  (-0.00935,3.03804),(-0.298414,0.410144),(-0.0213,6.0018)
  ("earth_sally_gate_left",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"earth_sally_gate_left","bo_earth_sally_gate_left", [
    check_sally_door_use_trigger_double,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,2000),
    ]),
  ]),
  # not center high,len (-3.05882,-0.011432),(-0.298415,0.410144),(-0.0213,6.0018)
  ("earth_sally_gate_right",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"earth_sally_gate_right","bo_earth_sally_gate_right", [
    check_sally_door_use_trigger_double,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,2000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,2000),
    ]),
  ]),
  
  # not center high,len (-1.62127,0.013701),(-0.11062,0.118904),(0.002755,4.52336)
  ("viking_keep_destroy_sally_door_right",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"viking_keep_destroy_sally_door_right","bo_viking_keep_destroy_sally_door_right", [
    check_sally_door_use_trigger_double,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,3000),
    ]),
  ]),

  # not center high,len   (-0.019187,1.61579),(-0.110621,0.118904),(0.002755,4.52336)
  ("viking_keep_destroy_sally_door_left",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"viking_keep_destroy_sally_door_left","bo_viking_keep_destroy_sally_door_left", [
    check_sally_door_use_trigger_double,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,3000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,3000),
    ]),    
  ]),

  # not center high,len   (-1.49895,0.000219),(0.008935,0.157788),(0.00018,2.47752)
  ("castle_f_door_b",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(0),"castle_e_sally_door_a","bo_castle_e_sally_door_a", [
    check_castle_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,1000),
    ]),
  ]),
  
  # not center high,len   (-0.025536,0.012768),(0,1.11021),(-1.58424e-16,2.18051)
  ("mm_restroom_door",sokf_static_movement|sokf_show_hit_point_bar|sokf_destructible|spr_use_time(2),"mm_restroom_door","bo_mm_restroom_door", [
    check_castle_door_use_trigger,
    check_common_object_hit_trigger,
    check_common_door_destroy_trigger,

   (ti_on_init_scene_prop,
    [
      (store_trigger_param_1, ":instance_no"),
      (scene_prop_set_hit_points, ":instance_no", 1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_health,1000),
      (scene_prop_set_slot,":instance_no",scene_prop_slot_max_health,1000),
    ]),
  ]),
  
 # ("doors_end", 0,"0" ,"0" , []),
    
    # add new stuff here!
    
    
    
    # add new stuff here!
    # USED AS ENDING FOR DOORS!
    ("mm_barrier_20m",sokf_invisible|sokf_type_barrier,"barrier_20m","bo_barrier_20m", []),
    ("mm_barrier_16m",sokf_invisible|sokf_type_barrier,"barrier_16m","bo_barrier_16m", []),
    ("mm_barrier_8m" ,sokf_invisible|sokf_type_barrier,"barrier_8m" ,"bo_barrier_8m" , []),
    ("mm_barrier_4m" ,sokf_invisible|sokf_type_barrier,"barrier_4m" ,"bo_barrier_4m" , []),
    ("mm_barrier_2m" ,sokf_invisible|sokf_type_barrier,"barrier_2m" ,"bo_barrier_2m" , []),
    ("mm_barrier_no_col_20m",sokf_invisible|sokf_type_barrier,"barrier_20m","0", []),
    ("mm_barrier_no_col_16m",sokf_invisible|sokf_type_barrier,"barrier_16m","0", []),
    ("mm_barrier_no_col_8m" ,sokf_invisible|sokf_type_barrier,"barrier_8m" ,"0" , []),
    ("mm_barrier_no_col_4m" ,sokf_invisible|sokf_type_barrier,"barrier_4m" ,"0" , []),
    ("mm_barrier_no_col_2m" ,sokf_invisible|sokf_type_barrier,"barrier_2m" ,"0" , []),

    #("mm_destructible_props_end", 0,"0" ,"0" , []),
    
    # Destroyed props.
    # used as destructible_props_end!
    ("mm_house_wall_2dd" ,sokf_static_movement,"2ddwall" ,"bo_2ddwall" , []),
    ("mm_house_wall_2ddd" ,sokf_static_movement,"2dddwall" ,"bo_2dddwall" , []),
    ("mm_house_wall_3dd" ,sokf_static_movement,"3ddwall" ,"bo_3ddwall" , []),
    ("mm_house_wall_3ddd" ,sokf_static_movement,"3dddwall" ,"bo_3dddwall" , []),
    ("mm_house_wall_4dd" ,sokf_static_movement,"4ddwall" ,"bo_4ddwall" , []),
    ("mm_house_wall_4ddd" ,sokf_static_movement,"4dddwall" ,"bo_4dddwall" , []),
    ("mm_house_wall_5dd" ,sokf_static_movement,"5ddwall" ,"bo_5ddwall" , []),
    ("mm_house_wall_5ddd" ,sokf_static_movement,"5dddwall" ,"bo_5dddwall" , []),
    ("mm_house_wall_6dd" ,sokf_static_movement,"6ddwall" ,"bo_6ddwall" , []),
    ("mm_house_wall_6ddd" ,sokf_static_movement,"6dddwall" ,"bo_6dddwall" , []),
    ("mm_house_wall_7dd" ,sokf_static_movement,"7ddwall" ,"bo_7ddwall" , []),
    ("mm_house_wall_7ddd" ,sokf_static_movement,"7dddwall" ,"bo_7dddwall" , []),
    ("mm_house_wall_11dd" ,sokf_static_movement,"11ddwall" ,"bo_11ddwall" , []),
    ("mm_house_wall_11ddd" ,sokf_static_movement,"11dddwall" ,"bo_11dddwall" , []),
    ("mm_house_wall_21dd" ,sokf_static_movement,"21ddwall" ,"bo_21ddwall" , []),
    ("mm_house_wall_21ddd" ,sokf_static_movement,"21dddwall" ,"bo_21dddwall" , []),
    ("mm_house_wall_31dd" ,sokf_static_movement,"31ddwall" ,"bo_31ddwall" , []),
    ("mm_house_wall_31ddd" ,sokf_static_movement,"31dddwall" ,"bo_31dddwall" , []),
    ("mm_house_wall_41dd" ,sokf_static_movement,"41ddwall" ,"bo_41ddwall" , []),
    ("mm_house_wall_41ddd" ,sokf_static_movement,"41dddwall" ,"bo_41dddwall" , []),
    ("mm_house_wall_51dd" ,sokf_static_movement,"51ddwall" ,"bo_51ddwall" , []),
    ("mm_house_wall_51ddd" ,sokf_static_movement,"51dddwall" ,"bo_51dddwall" , []),
    ("mm_house_wall_61dd" ,sokf_static_movement,"61ddwall" ,"bo_61ddwall" , []),
    ("mm_house_wall_61ddd" ,sokf_static_movement,"61dddwall" ,"bo_61dddwall" , []),
    ("mm_house_wall_71dd" ,sokf_static_movement,"71ddwall" ,"bo_71ddwall" , []),
    ("mm_house_wall_71ddd" ,sokf_static_movement,"71dddwall" ,"bo_71dddwall" , []),
    
    ("mm_wall2" ,sokf_static_movement,"wall2" ,"wall2_collision" , []),
    ("mm_walldesert2" ,sokf_static_movement,"desertWall1ddd" ,"bo_desertWall1ddd" , []),
    ("mm_wallwood2" ,sokf_static_movement,"woodWall1ddd" ,"bo_woodWall1ddd" , []),
    ("mm_wall_destoyed" ,sokf_static_movement,"wall_destoyed" ,"wall_destoyed_collision" , []),
    
    ("fortnew9", sokf_static_movement|sokf_dont_move_agent_over, "fortnew9", "bo_fortnew9" , []),
    ("fortnew_111", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_111", "bo_fortnew_111" , []),
    ("fortnew_29", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_29", "bo_fortnew_29" , []),
    ("fortnew_39", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_39", "bo_fortnew_39" , []),
    ("fortnew_41", sokf_static_movement|sokf_dont_move_agent_over, "fortnew_41", "bo_fortnew_41" , []),
    
    ("mm_new_wall_1_1dd" ,sokf_static_movement,"newall1dd" ,"bo_newall1dd" , []),
    ("mm_new_wall_1_1ddd" ,sokf_static_movement,"newall1ddd" ,"bo_newall1ddd" , []),
    ("mm_new_wall_1_2dd" ,sokf_static_movement,"newall2dd" ,"bo_newall2dd" , []),
    ("mm_new_wall_1_2ddd" ,sokf_static_movement,"newall2ddd" ,"bo_newall2ddd" , []),
    ("mm_new_wall_1_3dd" ,sokf_static_movement,"newall3dd" ,"bo_newall3dd" , []),
    ("mm_new_wall_1_3ddd" ,sokf_static_movement,"newall3ddd" ,"bo_newall3ddd" , []),
    ("mm_new_wall_1_4dd" ,sokf_static_movement,"newall4dd" ,"bo_newall4dd" , []),
    ("mm_new_wall_1_4ddd" ,sokf_static_movement,"newall4ddd" ,"bo_newall4ddd" , []),
    ("mm_new_wall_1_5dd" ,sokf_static_movement,"newall5dd" ,"bo_newall5dd" , []),
    ("mm_new_wall_1_5ddd" ,sokf_static_movement,"newall5ddd" ,"bo_newall5ddd" , []),
    ("mm_new_wall_1_6dd" ,sokf_static_movement,"newall6dd" ,"bo_newall6dd" , []),
    ("mm_new_wall_1_6ddd" ,sokf_static_movement,"newall6ddd" ,"bo_newall6ddd" , []),
    ("mm_new_wall_1_7dd" ,sokf_static_movement,"newall7dd" ,"bo_newall7dd" , []),
    ("mm_new_wall_1_7ddd" ,sokf_static_movement,"newall7ddd" ,"bo_newall7ddd" , []),
    ("mm_new_wall_1_8dd" ,sokf_static_movement,"newall8dd" ,"bo_newall8dd" , []),
    ("mm_new_wall_1_8ddd" ,sokf_static_movement,"newall8ddd" ,"bo_newall8ddd" , []),
    ("mm_new_wall_1_9dd" ,sokf_static_movement,"newall9dd" ,"bo_newall9dd" , []),
    ("mm_new_wall_1_9ddd" ,sokf_static_movement,"newall9ddd" ,"bo_newall9ddd" , []),
    ("mm_new_wall_1_10dd" ,sokf_static_movement,"newall10dd" ,"bo_newall10dd" , []),
    ("mm_new_wall_1_10ddd" ,sokf_static_movement,"newall10ddd" ,"bo_newall10ddd" , []),
    ("mm_new_wall_1_11dd" ,sokf_static_movement,"newall11dd" ,"bo_newall11dd" , []),
    ("mm_new_wall_1_11ddd" ,sokf_static_movement,"newall11ddd" ,"bo_newall11ddd" , []),
    
    ("mm_new_wall_2_1dd" ,sokf_static_movement,"ne1wall1dd" ,"bo_newall1dd" , []),
    ("mm_new_wall_2_1ddd" ,sokf_static_movement,"ne1wall1ddd" ,"bo_newall1ddd" , []),
    ("mm_new_wall_2_2dd" ,sokf_static_movement,"ne1wall2dd" ,"bo_newall2dd" , []),
    ("mm_new_wall_2_2ddd" ,sokf_static_movement,"ne1wall2ddd" ,"bo_newall2ddd" , []),
    ("mm_new_wall_2_3dd" ,sokf_static_movement,"ne1wall3dd" ,"bo_newall3dd" , []),
    ("mm_new_wall_2_3ddd" ,sokf_static_movement,"ne1wall3ddd" ,"bo_newall3ddd" , []),
    ("mm_new_wall_2_4dd" ,sokf_static_movement,"ne1wall4dd" ,"bo_newall4dd" , []),
    ("mm_new_wall_2_4ddd" ,sokf_static_movement,"ne1wall4ddd" ,"bo_newall4ddd" , []),
    ("mm_new_wall_2_5dd" ,sokf_static_movement,"ne1wall5dd" ,"bo_newall5dd" , []),
    ("mm_new_wall_2_5ddd" ,sokf_static_movement,"ne1wall5ddd" ,"bo_newall5ddd" , []),
    ("mm_new_wall_2_6dd" ,sokf_static_movement,"ne1wall6dd" ,"bo_newall6dd" , []),
    ("mm_new_wall_2_6ddd" ,sokf_static_movement,"ne1wall6ddd" ,"bo_newall6ddd" , []),
    ("mm_new_wall_2_7dd" ,sokf_static_movement,"ne1wall7dd" ,"bo_newall7dd" , []),
    ("mm_new_wall_2_7ddd" ,sokf_static_movement,"ne1wall7ddd" ,"bo_newall7ddd" , []),
    ("mm_new_wall_2_8dd" ,sokf_static_movement,"ne1wall8dd" ,"bo_newall8dd" , []),
    ("mm_new_wall_2_8ddd" ,sokf_static_movement,"ne1wall8ddd" ,"bo_newall8ddd" , []),
    ("mm_new_wall_2_9dd" ,sokf_static_movement,"ne1wall9dd" ,"bo_newall9dd" , []),
    ("mm_new_wall_2_9ddd" ,sokf_static_movement,"ne1wall9ddd" ,"bo_newall9ddd" , []),
    ("mm_new_wall_2_10dd" ,sokf_static_movement,"ne1wall10dd" ,"bo_newall10dd" , []),
    ("mm_new_wall_2_10ddd" ,sokf_static_movement,"ne1wall10ddd" ,"bo_newall10ddd" , []),
    ("mm_new_wall_2_11dd" ,sokf_static_movement,"ne1wall11dd" ,"bo_newall11dd" , []),
    ("mm_new_wall_2_11ddd" ,sokf_static_movement,"ne1wall11ddd" ,"bo_newall11ddd" , []),
    
    ("mm_new_wall_3_1dd" ,sokf_static_movement,"ne2wall1dd" ,"bo_newall1dd" , []),
    ("mm_new_wall_3_1ddd" ,sokf_static_movement,"ne2wall1ddd" ,"bo_newall1ddd" , []),
    ("mm_new_wall_3_2dd" ,sokf_static_movement,"ne2wall2dd" ,"bo_newall2dd" , []),
    ("mm_new_wall_3_2ddd" ,sokf_static_movement,"ne2wall2ddd" ,"bo_newall2ddd" , []),
    ("mm_new_wall_3_3dd" ,sokf_static_movement,"ne2wall3dd" ,"bo_newall3dd" , []),
    ("mm_new_wall_3_3ddd" ,sokf_static_movement,"ne2wall3ddd" ,"bo_newall3ddd" , []),
    ("mm_new_wall_3_4dd" ,sokf_static_movement,"ne2wall4dd" ,"bo_newall4dd" , []),
    ("mm_new_wall_3_4ddd" ,sokf_static_movement,"ne2wall4ddd" ,"bo_newall4ddd" , []),
    ("mm_new_wall_3_5dd" ,sokf_static_movement,"ne2wall5dd" ,"bo_newall5dd" , []),
    ("mm_new_wall_3_5ddd" ,sokf_static_movement,"ne2wall5ddd" ,"bo_newall5ddd" , []),
    ("mm_new_wall_3_6dd" ,sokf_static_movement,"ne2wall6dd" ,"bo_newall6dd" , []),
    ("mm_new_wall_3_6ddd" ,sokf_static_movement,"ne2wall6ddd" ,"bo_newall6ddd" , []),
    ("mm_new_wall_3_7dd" ,sokf_static_movement,"ne2wall7dd" ,"bo_newall7dd" , []),
    ("mm_new_wall_3_7ddd" ,sokf_static_movement,"ne2wall7ddd" ,"bo_newall7ddd" , []),
    ("mm_new_wall_3_8dd" ,sokf_static_movement,"ne2wall8dd" ,"bo_newall8dd" , []),
    ("mm_new_wall_3_8ddd" ,sokf_static_movement,"ne2wall8ddd" ,"bo_newall8ddd" , []),
    ("mm_new_wall_3_9dd" ,sokf_static_movement,"ne2wall9dd" ,"bo_newall9dd" , []),
    ("mm_new_wall_3_9ddd" ,sokf_static_movement,"ne2wall9ddd" ,"bo_newall9ddd" , []),
    ("mm_new_wall_3_10dd" ,sokf_static_movement,"ne2wall10dd" ,"bo_newall10dd" , []),
    ("mm_new_wall_3_10ddd" ,sokf_static_movement,"ne2wall10ddd" ,"bo_newall10ddd" , []),
    ("mm_new_wall_3_11dd" ,sokf_static_movement,"ne2wall11dd" ,"bo_newall11dd" , []),
    ("mm_new_wall_3_11ddd" ,sokf_static_movement,"ne2wall11ddd" ,"bo_newall11ddd" , []),
	
    ("mm_woodenwall1dd" ,sokf_static_movement,"woodenwall1dd" ,"bo_woodenwall1dd" , []),
    ("mm_woodenwallsnowy1dd" ,sokf_static_movement,"woodenwallsnowy1dd" ,"bo_woodenwallsnowy1dd" , []),
  
    ("mm_sp_poor_bridge1d" ,sokf_static_movement,"sp_poor_village_bridge1d" ,"bo_sp_poor_village_bridge1d" , []),
    ("mm_sp_rich_bridge2d" ,sokf_static_movement,"sp_rich_village_bridge11d" ,"bo_sp_rich_village_bridge11d" , []),
    ("mm_sp_rich_bridge3d", sokf_static_movement, "sp_rich_village_bridge12d", "bo_sp_rich_village_bridge12d" , []),

        
    ("mm_sp_rich_bridge4d" ,sokf_static_movement,"sp_rich_village_bridge13d" ,"bo_sp_rich_village_bridge13d" , []),
    
    ("mm_stockade_cannon_destroyed" ,sokf_static_movement,"stockade_cannon_destroyed" ,"stockade_cannon_destroyed_collision" , []),
    ("mm_stockade_destroyed" ,sokf_static_movement,"stockade_destroyed" ,"stockade_destroyed_collision" , []),
    ("mm_stakes_destroyed" ,sokf_static_movement,"stackes_destroyed" ,"0" , []),
    ("mm_stakes2_destroyed" ,sokf_static_movement,"mmstackesd" ,"bo_mmstackesd" , []),
    ("mm_dummy_destroyed",sokf_static_movement,"mm_dummy_destroyed","0", []),
    
    # construction props are in fact destroyed props.
    
    #Buildable/repairable palisade
    ("mm_palisadedd" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mmpalisadedd" ,"bo_mmpalisadedd" , [
   #   check_common_construction_props_start_use_trigger,
    #  check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    #Pontoon bridges (build props)
    #Short
    ("mm_constr_pontoon_short" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"pontoon_construct" ,"bo_pontoon_construct" , [
    #  check_common_construction_props_start_use_trigger,
    #  check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    #Med
    ("mm_constr_pontoon_med" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"pontoon_construct" ,"bo_pontoon_construct" , [
    #  check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    #Long
    ("mm_constr_pontoon_long" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"pontoon_construct" ,"bo_pontoon_construct" , [
   #   check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    #Watchtower contruct
    ("mm_constr_watchtower" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"watchtower_construct" ,"bo_watchtower_construct" , [
   #   check_common_construction_props_start_use_trigger,
    #  check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
    ]),
    
    
    # Hammer Contruction Props Begin
    ("mm_stakes_construct",sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"stackes_destroyed" ,"bo_stackes_destroyed" , [
   #   check_common_construction_props_start_use_trigger,
    #  check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("mm_stakes2_construct" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mmstackesd" ,"bo_mmstackesd" , [  
  #    check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("sandbags_construct" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"sandbags_destroy" ,"bo_sandbags_destroy" , [  
   #   check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("chevaux_de_frise_tri_construct" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"chevaux_de_frise_tri_destroy" ,"bo_chevaux_de_frise_tri_destroy" , [  
   #   check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("gabiondeploy_construct" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"hanskopf" ,"bo_hanskopf" , [
  #    check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("mm_fence1d" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mmfence1d" ,"bo_mmfence1d" , [
   #   check_common_construction_props_start_use_trigger,
    #  check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
    ]),
    ("plank_construct_dummy" ,sokf_static_movement|sokf_dont_move_agent_over|sokf_show_hit_point_bar|sokf_destructible,"mm_plank1" ,"bo_mm_plank1" , [#patch1115 55/3
     # check_common_object_hit_trigger,
  #    check_common_construction_props_start_use_trigger,
   #   check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("earthwork1_construct_dummy" ,sokf_static_movement,"earthwork1" ,"bo_earthwork1" , [  
  #    check_common_construction_props_start_use_trigger,
  #    check_common_construction_props_use_trigger,
      check_common_constructable_prop_on_hit_trigger,
      check_common_constructible_props_destroy_trigger,
      (ti_on_scene_prop_use,[]),
      ]),
    ("crate_explosive" ,sokf_static_movement,"barreltriangulated" ,"barreltriangulated_collision" , [  
     # check_common_explosive_crate_use_trigger,
    ]),
    
    #("mm_construct_props_end", 0,"0" ,"0" , []),
       
    # prop used as construct_prop_end!       
    ("mm_crator_small",sokf_static_movement,"crator_small","0", []),
    ("mm_crator_crator_medium_very_small",sokf_static_movement,"crator_medium_very_small","0", []),
    ("mm_crator_medium_small",sokf_static_movement,"crator_medium_small","0", []),
    ("mm_crator_medium",sokf_static_movement,"crator_medium","0", []),
    ("mm_crator_big_medium",sokf_static_movement,"crator_big_medium","0", []),
    ("mm_crator_big",sokf_static_movement,"crator_big","0", []),
    ("mm_crator_explosion",sokf_static_movement,"crator_explosion","0", []),
    
    #("mm_crators_end", 0,"0" ,"0" , []),

    # prop used as crators end!
    ("mm_wall_wood_planks1",sokf_static_movement,"splinters","0", []),
    ("mm_wall_wood_planks2",sokf_static_movement,"splinters2","0", []),
    ("mm_wall_wood_planks3",sokf_static_movement,"splinters3","0", []),


    ("mm_wall_stones1",sokf_static_movement,"wall_stones1","0", []),
    ("mm_wall_stones2",sokf_static_movement,"wall_stones2","0", []),
    ("mm_wall_stones3",sokf_static_movement,"wall_stones3","0", []),
    ("mm_wall_stones4",sokf_static_movement,"wall_stones4","0", []),
    
    ("mm_wall_stonesdesert1",sokf_static_movement,"desertBricks1","0", []),
    ("mm_wall_stonesdesert2",sokf_static_movement,"desertBricks2","0", []),
    
    #("mm_destroyed_props_end", 0,"0" ,"0" , []),
    
    # used as Destroyed_props_end!!!
    ("mm_wallgate" ,0,"wallgate" ,"wallgate_collision" , []),
	  ("mm_walldesertgatedesert" ,0,"desertWallGatehouse" ,"bo_desertWallGatehouse" , []),
	  ("mm_wallwoodgatewood" ,0,"woodWallGatehouse" ,"bo_woodWallGatehouse" , []),
    ("mm_gunrack" ,0,"gunrack" ,"gunrack_collision" , []),
    ("mm_lantern" ,0,"lantern" ,"0" , []),
    ("mm_table1" ,0,"table1" ,"table1_collision" , []),
    ("mm_cupboard1" ,0,"cupboard1" ,"cupboard1_collision" , []),
    ("mm_cupboard2" ,0,"cupboard2" ,"bo_cupboard2" , []),
    ("mm_cupboard3" ,0,"cupboard3" ,"bo_cupboard3" , []),
    ("mm_french_barrel" ,0,"barreltriangulated" ,"barreltriangulated_collision" , []),
    ("mm_brit_barrel" ,0,"barreltriangulated_brit" ,"barreltriangulated_collision" , []),
    ("mm_coffin" ,0,"coffin" ,"coffin_collision" , []),
    ("mm_grave1" ,0,"grave1" ,"0" , []),
    ("mm_grave2" ,0,"grave2" ,"0" , []),
    ("mm_restroom" ,0,"restroom" ,"restroom_collision" , []),
    ("mm_sign" ,0,"sign" ,"sign_collision" , []),
    ("mm_bed" ,0,"bed" ,"bed_collision" , []),
    ("mm_chair1" ,0,"chair1" ,"chair_collision" , []),
    ("mm_little_table" ,0,"little_table" ,"little_table_collision" , []),
    ("mm_little_table2" ,0,"little_table2" ,"little_table2_collision" , []),
    ("mm_bank1" ,0,"bank" ,"bank_collision" , []),
    ("mm_crate1" ,0,"crate1" ,"bo_crate" , []),
    ("mm_crate2" ,0,"crate2" ,"bo_crate" , []),
    ("mm_wall82" ,0,"wall82" ,"wall82_collision" , []),
	("mm_walldesert82" ,0,"desertWall82" ,"bo_desertWall82" , []),
	("mm_wallwood82" ,0,"woodWall82" ,"bo_woodWall82" , []),
    ("mm_wall84" ,0,"wall84" ,"wall84_collision" , []),
    ("mm_fountain1" ,0,"brunnen" ,"brunnen_collision" , []),
    ("mm_fireplace1" ,0,"camin" ,"camin_collision" , []),
    ("mm_fireplace2" ,0,"camin2" ,"camin2_collision" , []),
    ("mm_bookcase" ,0,"bookcase" ,"bookcase_collision" , []),
    ("mm_piano",spr_use_time(0),"piano","bo_piano",
    [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),
        
        (agent_is_active,":agent_id"),
        (agent_is_alive,":agent_id"),
        (agent_get_player_id,":player_id",":agent_id"),
        (player_is_active,":player_id"),
        
        (prop_instance_is_valid,":instance_id"),
        
        (assign,":in_use",0),
        (try_for_agents, ":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_slot,":cur_inst",":cur_agent",slot_agent_used_prop_instance),
          (eq,":cur_inst",":instance_id"), # same prop
          (neq,":cur_agent",":agent_id"), # and not meself
          (assign,":in_use",1),
        (try_end),
        
        # not in use by a other player.
        (try_begin),
          (eq,":in_use",0),
          
          # Always stop first.
          (call_script,"script_multiplayer_server_agent_stop_music",":agent_id"),
          
          # not on horseback
          (try_begin),
            (agent_get_horse, ":player_horse", ":agent_id"),
            (le, ":player_horse", 0),
            
            (try_begin),
              
              (set_fixed_point_multiplier, 100),
              
              (agent_get_position,pos33,":agent_id"),
              (prop_instance_get_position, pos40, ":instance_id"),
              
              (position_move_y,pos40,-200),
              (get_distance_between_positions,":dist",pos33,pos40),
              
              (lt, ":dist", 280),
              
              #(get_angle_between_positions, ":rotation", pos33, pos40),
              
            
              (prop_instance_get_scene_prop_kind,":prop_kind",":instance_id"),
              (agent_set_slot, ":agent_id", slot_agent_used_prop_instance, ":instance_id"),
              
              (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_return_server_action, server_action_force_music_selection, ":prop_kind"),
            (else_try),
              (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_cannot_use_piano_angle"),
            (try_end),
          (else_try),
            (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_cannot_use_piano"),
          (try_end),
        (else_try),
          (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_piano_in_use"),
        (try_end),
      ]),
    ]),
    ("mm_organ",spr_use_time(0),"organ","bo_organ",
    [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),
        
        (agent_is_active,":agent_id"),
        (agent_is_alive,":agent_id"),
        (agent_get_player_id,":player_id",":agent_id"),
        (player_is_active,":player_id"),
        
        (prop_instance_is_valid,":instance_id"),
        
        (assign,":in_use",0),
        (try_for_agents, ":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_slot,":cur_inst",":cur_agent",slot_agent_used_prop_instance),
          (eq,":cur_inst",":instance_id"), # same prop
          (neq,":cur_agent",":agent_id"), # and not meself
          (assign,":in_use",1),
        (try_end),
        
        # not in use by a other player.
        (try_begin),
          (eq,":in_use",0),
          
          # Always stop first.
          (call_script,"script_multiplayer_server_agent_stop_music",":agent_id"),
          
          # not on horseback
          (try_begin),
            (agent_get_horse, ":player_horse", ":agent_id"),
            (le, ":player_horse", 0),
            
            (try_begin),
              (set_fixed_point_multiplier, 100),
              
              (agent_get_position,pos33,":agent_id"),
              (prop_instance_get_position, pos40, ":instance_id"),
              
              (position_move_y,pos40,-250),
              (get_distance_between_positions,":dist",pos33,pos40),
              
              (lt, ":dist", 280),
              
              #(get_angle_between_positions, ":rotation", pos33, pos40),
              
            
              (prop_instance_get_scene_prop_kind,":prop_kind",":instance_id"),
              (agent_set_slot, ":agent_id", slot_agent_used_prop_instance, ":instance_id"),
              
              (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_return_server_action, server_action_force_music_selection, ":prop_kind"),
            (else_try),
              (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_cannot_use_piano_angle"),
            (try_end),
          (else_try),
            (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_cannot_use_organ"),
          (try_end),
        (else_try),
          (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_organ_in_use"),
        (try_end),
      ]),
    ]),
    
    ("mm_shithouse_button",spr_use_time(1),"0","cannon_button_collision",
    [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),
        
        (agent_is_active,":agent_id"),
        (agent_is_alive,":agent_id"),
        (agent_get_player_id,":player_id",":agent_id"),
        (player_is_active,":player_id"),
        
        (prop_instance_is_valid,":instance_id"),
        
        (assign,":in_use",0),
        (try_for_agents, ":cur_agent"),
          (agent_is_active,":cur_agent"),
          (agent_is_alive,":cur_agent"),
          (agent_get_slot,":cur_inst",":cur_agent",slot_agent_used_prop_instance),
          (eq,":cur_inst",":instance_id"), # same prop
          (neq,":cur_agent",":agent_id"), # and not meself
          (assign,":in_use",1),
        (try_end),
        
        # not in use by a other player.
        (try_begin),
          (eq,":in_use",0),
          
          # not on horseback
          (try_begin),
            (agent_get_horse, ":player_horse", ":agent_id"),
            (le, ":player_horse", 0),
            
            (try_begin),
              (call_script,"script_cf_agent_is_taking_a_shit",":agent_id"),
              # we stopped shitting.
              (call_script,"script_multiplayer_server_agent_stop_music",":agent_id"),
            (else_try),
              (agent_set_slot, ":agent_id", slot_agent_used_prop_instance, ":instance_id"),
              
              (agent_set_animation,":agent_id","anim_shitting",0),
              
              (agent_set_wielded_item,":agent_id",-1),  
        
              # put player on stool.
              (prop_instance_get_position,pos5,":instance_id"),
              (position_move_x,pos5,30),
              (agent_set_position,":agent_id",pos5),
            (try_end),
          (else_try),
            (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_cannot_use_toilet"),
          (try_end),
        (else_try),
          (multiplayer_send_2_int_to_player, ":player_id", multiplayer_event_show_multiplayer_message, multiplayer_message_type_error, "str_toilet_in_use"),
        (try_end),
      ]),
    ]),
    
    ("mm_ammobox_cannon", sokf_static_movement|sokf_dont_move_agent_over, "ammobox_cannon" , "bo_ammobox", []),
    ("mm_ammobox_howitzer", sokf_static_movement|sokf_dont_move_agent_over, "ammobox_howitzer" , "bo_ammobox", []),
    
    ("mm_tent1",0,"mm_tent1","bo_mmtent1", []),
    ("mm_wood_heap1",0,"mm_wood_heap1","bo_mm_wood_heap1", []),
    ("mm_wood_heap2",0,"mm_wood_heap2","bo_mm_wood_heap2", []),
    ("mm_wood_heap3",0,"mm_wood_heap3","bo_mm_wood_heap3", []),
    ("mm_shrine",0,"mmshrine","bo_shrine", []),
    ("mm_shrine1",0,"mmshrine1","bo_shrine", []),
    ("mm_shrine2",0,"mmshrine2","bo_shrine", []),
    ("mm_shrine3",0,"mmshrine3","bo_shrine", []),
    ("mm_shrine4",0,"mmshrine4","bo_shrine", []),
    ("mm_arc",0,"arc","bo_arc", []),
    
    ("mm_redoubt1",0,"mmredoubts1","bo_mmredoubts1", []),
    ("mm_redoubt2",0,"mmredoubts2","bo_mmredoubts1", []),
    ("mm_redoubt3",0,"mmredoubts3","bo_mmredoubts1", []),
    ("mm_redoubt4",0,"mmredoubts4","bo_mmredoubts1", []),
    ("mm_redoubt5",0,"mmredoubts5","bo_mmredoubts1", []),
    ("mm_redoubt6",0,"mmredoubts6","bo_mmredoubts6", []),
    ("mm_redoubt7",0,"mmredoubts7","bo_mmredoubts6", []),
    ("mm_redoubt8",0,"mmredoubts8","bo_mmredoubts6", []),
    ("mm_redoubt9",0,"mmredoubts9","bo_mmredoubts6", []),
    
    ("mm_great_redoubt1",0,"greatredoubts","bo_greatredoubts", []),
    ("mm_great_redoubt2",0,"greatredoubts1","bo_greatredoubts", []),
    ("mm_smallredoubt1",0,"smallredoubts","bo_smallredoubts", []),
    ("mm_smallredoubt2",0,"smallredoubts1","bo_smallredoubts1", []),
    ("mm_smallredoubt3",0,"smallredoubts2","bo_smallredoubts1", []),
    ("mm_smallredoubt4",0,"smallredoubts3","bo_smallredoubts", []),

    ("mm_trenches1",0,"mmtrenches1","bo_mmtrenches1", []),
    ("mm_trenches2",0,"mmtrenches2","bo_mmtrenches2", []),
    
    ("mm_sp_small_fort",0,"testforts","bo_testforts", []),
    ("mm_sp_small_fort1",0,"testforts1","bo_testforts1", []),
    ("mm_sp_small_fort2",0,"testforts2","bo_testforts2", []),

    ("mm_sp_czech1",0,"czech","bo_czech", []),
    ("mm_sp_czech2",0,"czech1","bo_czech1", []),
    ("mm_sp_czech3",0,"czech2","bo_czech2", []),
    ("mm_sp_czech4",0,"czech3","bo_czech3", []),

    
  
    ("mm_oim_fortwall1",0,"euro_fort_wall_blasted","bo_euro_fort_wall_blasted", []),
    ("mm_oim_fortwall2",0,"euro_fort_wall","bo_euro_fort_wall", []),
    ("mm_oim_fortwall3",0,"euro_fort_stairs","bo_euro_fort_stairs", []),
    ("mm_oim_fortwall4",0,"euro_fort_gate_house","bo_euro_fort_gate_house", []),
    ("mm_oim_fortwall5",0,"euro_fort_tower","bo_euro_fort_tower", []),
    ("mm_oim_fortwall6",0,"euro_fort_tower_ugol","bo_euro_fort_tower_ugol", []),
    ("mm_oim_fortwall7",0,"euro_fort_wall_corner","bo_euro_fort_wall_corner", []),
    
    ("mm_oim_fortwall9",0,"euro_fort_wall_in","bo_euro_fort_wall_in", []),
    ("mm_oim_fortwall10",0,"euro_fort_wall_in_half","bo_euro_fort_wall_in_half", []),
    
    ("mm_oim_debris1",0,"zaval","bo_zaval", []),
    ("oim_church1",0,"oim_rus_wood_church_a","bo_oim_rus_wood_church_a", []),
    ("oim_church2",0,"polsc_chapel_1a","bo_pol_wood_church", []),
    ("oim_rus_house1",0,"rus_izba_c","bo_rus_izba_c", []),
    ("oim_rus_house2",0,"rus_izba_d","bo_rus_izba_d", []),
    ("oim_rus_house3",0,"rus_izba_e","bo_rus_izba_e", []),
    ("oim_rus_house4",0,"rus_izba_a","bo_rus_izba_a", []),
    ("oim_rus_house5",0,"rus_izba_b","bo_rus_izba_b", []),

    ("mm_sp_rich_house1",0,"sp_rich_village_houses1","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house2",0,"sp_rich_village_houses2","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house3",0,"sp_rich_village_houses3","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house4",0,"sp_rich_village_houses4","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house5",0,"sp_rich_village_houses5","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house6",0,"sp_rich_village_houses6","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house7",0,"sp_rich_village_houses8","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house8",0,"sp_rich_village_houses9","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house9",0,"sp_rich_village_houses10","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house10",0,"sp_rich_village_houses11","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_house11",0,"sp_rich_village_houses12","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_house12",0,"sp_rich_village_houses13","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_church1",0,"sp_rich_village_houses7","bo_sp_rich_village_houses3", []),
    ("mm_sp_rich_street1",0,"sp_rich_village_street1","bo_sp_rich_village_street1", []),
    ("mm_sp_rich_street2",0,"sp_rich_village_street2","bo_sp_rich_village_street2", []),
    ("mm_sp_rich_street3",0,"sp_rich_village_street3","bo_sp_rich_village_street3", []),
    ("mm_sp_rich_street4",0,"sp_rich_village_street4","bo_sp_rich_village_street4", []),
    ("mm_sp_rich_street5",0,"sp_rich_village_street5","bo_sp_rich_village_street5", []),
   # ("mm_sp_rich_street6",0,"sp_rich_village_street6","bo_sp_rich_village_street6", []),
    ("mm_sp_poor_house6",0,"sp_poor_village_houses6","bo_sp_poor_village_houses6", []),
    ("mm_sp_poor_house7",0,"sp_poor_village_houses7","bo_sp_poor_village_houses7", []),
    ("mm_sp_poor_house9",0,"sp_poor_village_houses9","bo_sp_poor_village_houses9", []),
    ("mm_sp_poor_house10",0,"sp_poor_village_houses10","bo_sp_poor_village_houses10", []),
    ("mm_sp_poor_house11",0,"sp_poor_village_houses11","bo_sp_poor_village_houses11", []),

    
    ("mm_sp_rich_house14",0,"sp_rich_village_houses15","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house15",0,"sp_rich_village_houses15","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house16",0,"sp_rich_village_houses17","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house17",0,"sp_rich_village_houses17","bo_sp_rich_village_houses1", []),
    ("mm_sp_rich_house18",0,"sp_rich_village_houses18","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house19",0,"sp_rich_village_houses19","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house20",0,"sp_rich_village_houses22","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_house21",0,"sp_rich_village_houses21","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_house22",0,"sp_rich_village_houses22","bo_sp_rich_village_houses4", []),
    ("mm_sp_rich_house23",0,"sp_rich_village_houses24","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house24",0,"sp_rich_village_houses24","bo_sp_rich_village_houses2", []),
    ("mm_sp_rich_house25",0,"sp_rich_village_houses25","bo_sp_rich_village_houses2", []),

    
    #Trenches
    ("mm_trench_straight",0,"mm_trench_straight","bo_mm_trench_straight", []),
    ("mm_trench_corner",0,"mm_trench_corner","bo_mm_trench_corner", []),
    ("mm_trench_curve",0,"mm_trench_curve","bo_mm_trench_curve", []),
    ("mm_trench_big_curve",0,"mm_trench_big_curve","bo_mm_trench_big_curve", []),
    ("mm_trench_cross",0,"mm_trench_cross","bo_mm_trench_cross", []),
    ("mm_trench_cross2",0,"mm_trench_cross2","bo_mm_trench_cross2", []),
    ("mm_trench_bastion",0,"mm_trench_bastion","bo_mm_trench_bastion", []),
    ("mm_trench_entrance1",0,"mm_trench_entrance1","bo_mm_trench_entrance1", []),
    ("mm_trench_entrance2",0,"mm_trench_entrance2","bo_mm_trench_entrance2", []),
    
    ("mm_brit_barrel_explosive" ,sokf_static_movement,"barreltriangulated_brit" ,"barreltriangulated_collision" , []),
    ("mm_french_barrel_explosive" ,sokf_static_movement|spr_use_time(2),"barreltriangulated" ,"barreltriangulated_collision" , [  
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),
        
        (scene_prop_get_slot,":cur_time",":instance_id",scene_prop_slot_time),
        (le,":cur_time",0),
        (scene_prop_set_slot,":instance_id", scene_prop_slot_time, 5), #Seconds until exploding
        (scene_prop_set_slot,":instance_id", scene_prop_slot_user_agent, ":agent_id"), #User agent
      ]),]),
    ("mm_prus_barrel_explosive" ,sokf_static_movement,"barreltriangulated_brit" ,"barreltriangulated_collision" , []),
    
    ("windmill_fan_turning",sokf_static_movement,"windmill_fan_turning","0", []),
    
    #("fans_end", 0,"0" ,"0" , []),
    #used as end fan!
    ("mm_cannon_aim_platform" ,sokf_static_movement|sokf_dont_move_agent_over,"0" ,"bo_gunplane_combined" , []), # test mesh: gunplane_combined
    
    # Cannon types for mappers to place on map, will be replaced with seperate bits.
    ("mm_cannon_12pdr" ,sokf_static_movement,"cannon_12pdr" ,"0" , []),
    ("mm_cannon_howitzer" ,sokf_static_movement,"cannon_howitzer" ,"0" , []),
    ("mm_cannon_mortar" ,sokf_static_movement,"cannon_mortar" ,"0" , []),
    ("mm_cannon_fort" ,sokf_static_movement,"cannon_fort" ,"0" , []),
    ("mm_cannon_naval" ,sokf_static_movement,"cannon_naval" ,"0" , []),
    ("mm_cannon_carronade" ,sokf_static_movement,"cannon_carronade" ,"0" , []),
    ("mm_cannon_swievel" ,sokf_static_movement,"cannon_swievel" ,"0" , []),
    ("mm_cannon_rocket" ,sokf_static_movement,"rocket_launcher" ,"0" , []),
    #("mm_cannons_end", 0,"0" ,"0" , []),
    
    # Used as cannons end!
    # Normal cannonballs for mappers
    ("mm_cannonball_6pd", 0, "cannonball_6pd" , "cannonball_collision" , []),
    ("mm_cannonball_12pd", 0, "cannonball_12pd" , "cannonball_collision" , []),
    ("mm_cannonball_24pd", 0, "cannonball_24pd" , "cannonball_collision" , []),
    ("mm_cannonball_36pd", 0, "cannonball_36pd" , "cannonball_collision" , []),
    ("mm_rocket", 0, "rocket_projectile" , "cannonball_collision" , []),
    
    # Static cannon bits.
    ("mm_cannon_mortar_static",sokf_static_movement,"cannon_mortar_wood_static","0",[]),
    ("mm_cannon_fort_static",sokf_static_movement,"cannon_fort_static","0",[]),
    ("mm_cannon_rocket_static",sokf_static_movement,"rocket_launcher_static","0",[]),
    
    # loaded ammo cannon bits.
    ("mm_cannon_mortar_loaded_ammo",sokf_static_movement,"mortar_cartdridge","0",[]),
    ("mm_cannon_rocket_loaded_ammo",sokf_static_movement,"rocket_projectile","0",[]),
    #("mm_loaded_ammos_end", 0, "0" , "0" , []),
    
    # used as loaded_ammo_end!
    # Code cannonballs for trajectory
    ("mm_cannonball_code_only_6pd",sokf_static_movement,"cannonball_6pd","0",[]),
    ("mm_cannonball_code_only_12pd",sokf_static_movement,"cannonball_12pd","0",[]),
    ("mm_cannonball_code_only_24pd",sokf_static_movement,"cannonball_24pd","0",[]),
    ("mm_cannonball_code_only_36pd",sokf_static_movement,"cannonball_36pd","0",[]),
    ("mm_rocket_code_only",sokf_static_movement, "rocket_projectile" , "0" , []),
    
    # Cannon bits :)
    ("mm_cannon_12pdr_wood",sokf_static_movement|sokf_dont_move_agent_over,"cannon_12pdr_wood","12wood_barrel",[check_cannon_animation_finished_trigger]),
    ("mm_cannon_howitzer_wood",sokf_static_movement|sokf_dont_move_agent_over,"cannon_howitzer_wood","howitzerwood_barrel",[check_cannon_animation_finished_trigger]),
    ("mm_cannon_mortar_wood" ,sokf_static_movement,"cannon_mortar_wood" ,"mortarwood" , []),
    ("mm_cannon_fort_wood" ,sokf_static_movement,"cannon_fort_movable" ,"0" , []),
    ("mm_cannon_naval_wood" ,sokf_static_movement,"cannon_naval_wood" ,"navalbarrel" , [check_cannon_animation_finished_trigger]),
    ("mm_cannon_carronade_wood" ,sokf_static_movement,"cannon_carronade_wood" ,"navalwheels" , []),
    ("mm_cannon_swievel_wood" ,sokf_static_movement,"cannon_swievel_wood" ,"0" , []),
    ("mm_cannon_rocket_wood" ,sokf_static_movement,"rocket_launcher_wood" ,"0" , []),
    
    ("mm_cannon_12pdr_wheels",sokf_static_movement,"cannon_12pdr_wheels","0",[]),
    ("mm_cannon_howitzer_wheels",sokf_static_movement,"cannon_12pdr_wheels","0",[]),
    ("mm_cannon_fort_wheels",sokf_static_movement,"cannon_fort_movable2","bo_cannon_fort",[check_cannon_wheels_animation_finished_trigger]),
    ("mm_cannon_naval_wheels",sokf_static_movement,"0","0",[]),
    
    ("mm_cannon_12pdr_barrel" ,sokf_static_movement,"cannon_12pdr_barrel" ,"0" , []),
    ("mm_cannon_howitzer_barrel" ,sokf_static_movement,"cannon_howitzer_barrel" ,"0" , []),
    ("mm_cannon_mortar_barrel" ,sokf_static_movement,"cannon_mortar_barrel" ,"0" , []),
    ("mm_cannon_fort_barrel" ,sokf_static_movement,"cannon_fort_barrel" ,"0" , []),
    ("mm_cannon_naval_barrel" ,sokf_static_movement,"cannon_naval_barrel" ,"0" , []),
    ("mm_cannon_carronade_barrel" ,sokf_static_movement,"cannon_carronade_barrel" ,"0" , []),
    ("mm_cannon_swievel_barrel" ,sokf_static_movement,"cannon_swievel_barrel" ,"0" , []),
    ("mm_cannon_rocket_barrel" ,sokf_static_movement,"rocket_launcher_barrel" ,"0" , []),
    
    ("mm_cannon_12pdr_limber_wheels",sokf_static_movement,"cannon_12pdr_limber_wheels","0",[]),
    ("mm_cannon_howitzer_limber_wheels",sokf_static_movement,"cannon_12pdr_limber_wheels","0",[]),
    
    # Limber part
    ("mm_limber_wood",sokf_static_movement|sokf_dont_move_agent_over,"limber_wood","bo_limber_wood",[]),
    ("mm_limber_wheels",sokf_static_movement,"limber_wheels","0",[]),
    
    # Buttons
    # ("mm_cannon1_limber" ,sokf_static_movement|spr_use_time(10),"cannon1_limber" ,"0" , [ # Only use for unlimber
      # check_mm_use_cannon_prop_start_trigger,
      # check_mm_use_cannon_prop_end_trigger,
      # check_mm_use_cannon_prop_cancel_trigger,
    # ]),
    
    ("mm_cannon_12pdr_limber" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(10),"cannon_12pdr_limber" ,"bo_cannon4_limber" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_cannon_howitzer_limber" ,sokf_static_movement|sokf_dont_move_agent_over|spr_use_time(10),"cannon_howitzer_limber" ,"bo_cannon4_limber" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_limber_button", sokf_static_movement|spr_use_time(5), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_pickup_rocket_button", sokf_static_movement|spr_use_time(5), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_aim_button", sokf_static_movement|spr_use_time(0), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_load_cartridge_button", sokf_static_movement|spr_use_time(2), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_load_bomb_button", sokf_static_movement|spr_use_time(2), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_load_rocket_button", sokf_static_movement|spr_use_time(5), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_reload_button", sokf_static_movement|spr_use_time(9), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_12pdr_push_button",sokf_static_movement|spr_use_time(1),"0","12wheels",[
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    ("mm_howitzer_push_button",sokf_static_movement|spr_use_time(1),"0","12wheels",[
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    ("mm_fort_push_button",sokf_static_movement|spr_use_time(1),"0","fortwheels",[
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    ("mm_naval_push_button",sokf_static_movement|spr_use_time(1),"0","navalwheels",[
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    # Taking of difirent ammo
    ("mm_round_button", sokf_static_movement|spr_use_time(2), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_shell_button", sokf_static_movement|spr_use_time(2), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_canister_button", sokf_static_movement|spr_use_time(2), "0" , "cannon_button_collision" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    ("mm_bomb_button", sokf_static_movement|spr_use_time(2), "mortar_bomb_stack" , "bo_ammobox" , [
      check_mm_use_cannon_prop_start_trigger,
      check_mm_use_cannon_prop_end_trigger,
      check_mm_use_cannon_prop_cancel_trigger,
    ]),
    
    #("mm_buttons_end", 0,"0" ,"0" , []),
    
    # Rudders
    # button end!
    ("mm_ship_rudder",sokf_static_movement,"mmrudder","0", []),
    ("mm_ship_rudder_control",sokf_static_movement|spr_use_time(1),"mmrudder","bo_mmrudder", [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),

        (call_script, "script_use_item", ":instance_id", ":agent_id"),
      ]),
    ]),
    ("mm_ship_longboat_rudder",sokf_static_movement,"longboat_rudder","0", []),
    ("mm_ship_longboat_rudder_control",sokf_static_movement|spr_use_time(1),"longboat_rudder","bo_mmrudder", [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),

        (call_script, "script_use_item", ":instance_id", ":agent_id"),
      ]),
    ]),
    ("mm_ship_schooner_rudder",sokf_static_movement,"schooner_rudder","0", []),
    ("mm_ship_schooner_rudder_control",sokf_static_movement|spr_use_time(1),"schooner_rudder","bo_schooner_rudder", [
      (ti_on_scene_prop_use,
      [
        (store_trigger_param_1, ":agent_id"),
        (store_trigger_param_2, ":instance_id"),

        (call_script, "script_use_item", ":instance_id", ":agent_id"),
      ]),
    ]),
    
    ("mm_ship_hit_detect",sokf_static_movement,"0","bo_boat_hit_detect", []),
    ("mm_ship_hit_detect_back",sokf_static_movement,"0","bo_boat_hit_detect_back", []),
    ("mm_ship_schooner_hit_detect",sokf_static_movement,"0","bo_schooner_hit_detect", []),
    ("mm_ship_schooner_hit_detect_back",sokf_static_movement,"0","bo_schooner_hit_detect_back", []),
    
    # Digging stuff
    ("mm_tunnel_wall" ,sokf_static_movement|sokf_destructible,"mm_shovel_earth3" ,"bo_mm_shovel_earth3" , [check_common_earth_on_hit_trigger,]),
    ("mm_earth_dig1" ,sokf_static_movement|sokf_destructible,"mm_shovel_earth" ,"bo_mm_shovel_earth" , [check_common_earth_on_hit_trigger,]),
    ("mm_earth_dig2" ,sokf_static_movement|sokf_destructible,"mm_shovel_earth1" ,"bo_mm_shovel_earth1" , [check_common_earth_on_hit_trigger,]),
    ("mm_earth_dig3" ,sokf_static_movement|sokf_destructible,"mm_shovel_earth2" ,"bo_mm_shovel_earth2" , [check_common_earth_on_hit_trigger,]),
    ("mm_earth_dig4" ,sokf_static_movement|sokf_destructible,"mm_shovel_earth4" ,"bo_mm_shovel_earth4" , [check_common_earth_on_hit_trigger,]),
    #("mm_earths_end", 0,"0" ,"0" , []),
  #Ambient sound props  
# earths end!!
  #Global (plays wherever you are without position)
 ("ambience_sound_global_wind_snow",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_snow"),
    ]),]),  

 ("ambience_sound_global_night",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_night"),
    ]),]),  

 ("ambience_sound_global_beach",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_beach"),
    ]),]),  

 ("ambience_sound_global_farmland",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_farmland"),
    ]),]),  

 ("ambience_sound_global_farmland_evening",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_farmland_evening"),
    ]),]),  

 ("ambience_sound_global_farmland_empty",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_farmland_empty"),
    ]),]),  
 
("ambience_sound_global_city_empty",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      (play_sound,"snd_global_ambient_city_empty"),
    ]),]),  


 #Local (plays at the position of the prop)
 ("ambience_sound_local_birds",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_birds"),
    ]), ]),  
 ("ambience_sound_local_birds_many",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_birds_many"),
    ]), ]),  
 ("ambience_sound_local_ocean",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_ocean"),
    ]), ]),  
  ("ambience_sound_local_crickets",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_crickets_few"),
    ]), ]),  
  ("ambience_sound_local_crickets_many",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_crickets_many"),
    ]), ]),     
  ("ambience_sound_local_river",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_river"),
    ]), ]),   
  ("ambience_sound_local_night",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_night"),
    ]), ]),  
  ("ambience_sound_local_seagulls",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_seagulls"),
    ]), ]),  
  ("ambience_sound_local_flys",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_fly"),
    ]), ]),    

 ("ambience_sound_local_roof_rain",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_roof"),
    ]), ]), 
 ("ambience_sound_local_stone_rain",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_stone"),
    ]), ]), 
 ("ambience_sound_local_windmill",0,"0" ,"0" , [
  (ti_on_init_scene_prop,
    [
      (neg|multiplayer_is_dedicated_server),
      #(store_trigger_param_1,":instance_no"),
      #(prop_instance_get_position,pos1,":instance_no"),
      (play_sound,"snd_ambient_windmill"),
    ]), ]), 
    
  #Non-constant local sounds
  ("ambience_sound_local_crow",0,"0","0",
   [
   (ti_on_scene_prop_init,
    [
      (store_trigger_param_1,":instance_id"),
    
      (store_random_in_range,":cur_time",1,31), #0-30 sec until first burst
      (scene_prop_set_slot, ":instance_id", scene_prop_slot_time,":cur_time"), #Initial time until first particle burst in sec
                                                                               #delete the random and change cur_time to a value
                                                                               #to set this to the same for all props
    ]),
   ]),
            
   
  #Extra for siege    
 ("headquarters_flag_attacker_no_capture",sokf_static_movement|sokf_face_player,"mp_flag_blue","0", []),
 ("mm_siege_spawn_code_only", 0,"0" ,"0" , []),

 #For bots
 ("formation_locator",sokf_static_movement|sokf_face_player,"ctf_flag_britain","0", []),
 ("formation_locator_2",sokf_static_movement|sokf_face_player,"ctf_flag_france","0", []),
 ("formation_locator_3",sokf_static_movement|sokf_face_player,"ctf_flag_prussia","0", []),
 ("formation_locator_4",sokf_static_movement|sokf_face_player,"ctf_flag_russia","0", []),
 ("formation_locator_5",sokf_static_movement|sokf_face_player,"ctf_flag_austria","0", []),
 
 #For SP
 ("objectives_locator",sokf_static_movement|sokf_face_player,"ctf_flag_france","0", []),
 
 #Static Player Limiters
 ("mm_player_limiter_2m" ,sokf_invisible|sokf_type_player_limiter,"barrier_2m" ,"bo_barrier_2m" , []),
 ("mm_player_limiter_4m" ,sokf_invisible|sokf_type_player_limiter,"barrier_4m" ,"bo_barrier_4m" , []),
 ("mm_player_limiter_8m" ,sokf_invisible|sokf_type_player_limiter,"barrier_8m" ,"bo_barrier_8m" , []),
 ("mm_player_limiter_16m",sokf_invisible|sokf_type_player_limiter,"barrier_16m","bo_barrier_16m", []),
 
 #Movable Limiters to enable areas at a certain point
 ("mm_player_limiter_move_1" ,sokf_invisible|sokf_type_player_limiter|sokf_static_movement,"barrier_4m" ,"bo_barrier_4m" , []),
 ("mm_player_limiter_move_2" ,sokf_invisible|sokf_type_player_limiter|sokf_static_movement,"barrier_4m" ,"bo_barrier_4m" , []),
 ("mm_player_limiter_move_3" ,sokf_invisible|sokf_type_player_limiter|sokf_static_movement,"barrier_4m" ,"bo_barrier_4m" , []),
 ("mm_player_limiter_move_4" ,sokf_invisible|sokf_type_player_limiter|sokf_static_movement,"barrier_4m" ,"bo_barrier_4m" , []),
  
 #SP props
 ("mm_sp_ladder_sokolnitz_only",spr_use_time(0),"ladder","boladder", [
 (ti_on_scene_prop_use,
  [
    (assign,"$g_ladder_used",1),
  ]),
 ]),
 
 ("mm_sp_crate_explosive",sokf_static_movement|sokf_destructible,"barreltriangulated" ,"barreltriangulated_collision" , [ # sokf_moveable|sokf_dynamic_physics|
  (ti_on_init_scene_prop,
    [
      (this_or_next|multiplayer_is_server), #In case someone wants them in a multi scene...
      (neg|game_in_multiplayer_mode),
      (store_trigger_param_1,":prop_id"),
      (scene_prop_set_hit_points,":prop_id",70),
      
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos5, 1500), #mass=15.0
      (position_set_y, pos5, 80), #friction coefficient = 0.8
      (position_set_z, pos5, 0), #reserved variable
      (prop_instance_dynamics_set_properties, ":prop_id", pos5),
      (position_set_x, pos5, 300),
      (position_set_y, pos5, 300),
      (position_set_z, pos5, 300),
      (prop_instance_dynamics_set_omega, ":prop_id", pos5),
    ]), 
  (ti_on_scene_prop_hit,
    [
  #    (this_or_next|multiplayer_is_server), #In case someone wants them in a multi scene...
  #    (neg|game_in_multiplayer_mode),
  #    
  #    (store_trigger_param_1,":prop_id"),
  #    (set_fixed_point_multiplier, 1),
  #    (position_get_x,":attacker_agent",pos2),
  #    (scene_prop_set_slot,":prop_id",scene_prop_slot_last_hit_by,":attacker_agent"),
  #    (set_fixed_point_multiplier, 100),
      
      (try_begin),
        (neg|game_in_multiplayer_mode),
        (store_current_scene,":cur_scene"), 
        (eq,":cur_scene","scn_sp_vienna"), #ONLY for Vienna Battle
        (display_message,"@Careful...",0xF00000),
      (try_end),
    ]),
  (ti_on_scene_prop_destroy,
    [
      (this_or_next|multiplayer_is_server), #In case someone wants them in a multi scene...
      (neg|game_in_multiplayer_mode),
      
      (store_trigger_param_1,":prop_id"),
    #  (scene_prop_get_slot,":attacker_agent_no",":prop_id",scene_prop_slot_last_hit_by),
      (assign,":attacker_agent_no",-1),
      
      (set_fixed_point_multiplier, 100),
      (prop_instance_get_position,pos3,":prop_id"),
      (copy_position,pos47,pos3),
      (position_set_z,pos3,-3000),#patch1115 fix 29/1
      (prop_instance_set_position,":prop_id",pos3),
      (prop_instance_animate_to_position,":prop_id",pos3),
      (call_script,"script_explosion_at_position",":attacker_agent_no",300,500),#If you hit it too much, it will blow up in your face!
      (try_begin),
        (neg|game_in_multiplayer_mode),
        (store_current_scene,":cur_scene"), 
        (eq,":cur_scene","scn_sp_vienna"), #ONLY for Vienna Battle
        (get_player_agent_no,":player_agent"),
        (agent_is_active,":player_agent"),
        (agent_set_hit_points,":player_agent",0),
        (agent_deliver_damage_to_agent,":player_agent",":player_agent"), #Ensuring that you fail even if you for some reason don't die from the explosion
      (try_end),
    ]),
 ]),
 
 ("mm_campaign_table",spr_use_time(0),"table_tavern","botable_tavern", 
 [
  (ti_on_scene_prop_use,
    [
     (neg|game_in_multiplayer_mode),
      
     (start_presentation,"prsnt_singleplayer_campain_map"),
     
     #(store_trigger_param_1, ":agent_id"),
     #(store_trigger_param_2, ":instance_no"),
     
     
     ]),
 ]),

  ("ze_treasure",spr_use_time(4),"chest_b","bo_ze_treasure", [
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      #(store_trigger_param_2, ":instance_id"),

      #(neg|scene_prop_slot_eq, ":instance_id", scene_prop_slot_just_fired, 1), # abuse just_fired for already used.
      
      (agent_is_active,":agent_id"),
      (agent_is_alive,":agent_id"),
      
      # remove his shit.
      #(try_for_range_backwards,":equipment_slot",0,4), # ,ek_item_0,ek_head),
      #  (agent_get_item_slot, ":item_id", ":agent_id", ":equipment_slot"),
        
      #  (gt,":item_id",-1), # even have a item there?
        
      #  (agent_unequip_item, ":agent_id", ":item_id", ":equipment_slot"),
      #(try_end),
      (try_begin),
        (agent_get_item_slot, ":item_id", ":agent_id", 4), #ek_head
        (gt,":item_id",-1), # even have a item there?
        (agent_unequip_item, ":agent_id", ":item_id", 4), #ek_head
      (try_end),
      
      # add ze goodies.
      (agent_equip_item,":agent_id","itm_pirate_hat"),
      #(agent_equip_item,":agent_id","itm_french_officer_pistol"),
      #(agent_equip_item,":agent_id","itm_pistol_ammo"),
      #(agent_equip_item,":agent_id","itm_spyglass"),
      #(agent_equip_item,":agent_id","itm_french_light_cav_off_sabre"),
      
      #(agent_set_wielded_item,":agent_id","itm_french_officer_pistol"),
      
      #(scene_prop_set_slot,":instance_id",scene_prop_slot_just_fired,1),
      
      (try_for_players, ":player_no", 1),
        (player_is_active, ":player_no"),
        (multiplayer_send_3_int_to_player, ":player_no", multiplayer_event_return_agent_set_item, ":agent_id", "itm_pirate_hat", 4),
      (try_end),
    ]),
  ]),
 
  ("royale_weapon_spawn",sokf_static_movement,"pikecrate","0", []),
  # Var 1; weapon type: 0:random 1:Musket 2:Pistol 3:Carabine/rifle 4:smallsword/knife 5:bigsword 6:bottle 7:axe 8:Lance/pike/spear 9:clubs 10:tools(shovel/hammer/bandage/spyglass) 11:ramrod 12:lighter
  # Var 2: Spawn chance: 0:Always 1-100% of chance
 
  ("royale_weapon_spawn_musket",sokf_static_movement|spr_use_time(0),"musketcrate","bo_musketcrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_musket),
    ]),
  ]),

  ("royale_weapon_spawn_pistol",sokf_static_movement,"pistolcrate","bo_pistolcrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_pistol),
    ]),
  ]),

  ("royale_weapon_spawn_carabine",sokf_static_movement,"riflecrate","bo_riflecrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_carabine),
    ]),
  ]),

  ("royale_weapon_spawn_smallsword",sokf_static_movement,"sabrebriquetcrate","bo_sabrebriquetcrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_smallsword),
    ]),
  ]),

  ("royale_weapon_spawn_bigsword",sokf_static_movement,"longsabrecrate","bo_longsabrecrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_bigsword),
    ]),
  ]),

  ("royale_weapon_spawn_bottle",sokf_static_movement,"vodkacrate","bo_vodkacrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_bottle),
    ]),
  ]),

  ("royale_weapon_spawn_axe",sokf_static_movement,"axescrate","bo_axescrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_axe),
    ]),
  ]),

  ("royale_weapon_spawn_spear",sokf_static_movement,"pikecrate","bo_pikecrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_spear),
    ]),
  ]),

  ("royale_weapon_spawn_club",sokf_static_movement,"clubscrate","bo_clubscrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_club),
    ]),
  ]),

  ("royale_weapon_spawn_tool",sokf_static_movement,"toolscrate","bo_toolscrate", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_tool),
    ]),
  ]),

  ("royale_weapon_spawn_ramrod",sokf_static_movement,"ramrod","cannon_button_collision", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_ramrod),
    ]),
  ]),

  ("royale_weapon_spawn_lighter",sokf_static_movement,"lighter","cannon_button_collision", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_lighter),
    ]),
  ]),
  
  ("royale_ammo_spawn",sokf_static_movement,"cartridge_box_mesh","0", []),
  # Var 1; Ammo type: 0:random 1:Musket 2:Pistol
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_ammo_spawn_musket",sokf_static_movement,"cartridge_box_mesh","cannon_button_collision", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_ammo_musket),
    ]),
  ]),
  
  ("royale_ammo_spawn_pistol",sokf_static_movement,"cartridge_box_mesh","cannon_button_collision", [
    # Var 1; weapon type: nothing
    # Var 2: Spawn chance: 0:Always 1-100% of chance
    (ti_on_scene_prop_use,
    [
      (store_trigger_param_1, ":agent_id"),
      (store_trigger_param_2, ":instance_id"),
      (call_script,"script_multiplayer_server_royale_use_weaponbox",":agent_id",":instance_id",royale_item_class_ammo_pistol),
    ]),
  ]),
  
  ("royale_horse_spawn",sokf_static_movement,"austrian_hussard_horse","0", []),
  # Var 1; Horse type: 0:random 1:Light 2:Middle 3:Heavy 4:Artycarry
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_horse_spawn_light",sokf_static_movement,"austrian_lightcav_horse","0", []),
  # Var 1; Horse type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance
  
  ("royale_horse_spawn_middle",sokf_static_movement,"austrian_dragoon_horse","0", []),
  # Var 1; Horse type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance
  
  ("royale_horse_spawn_heavy",sokf_static_movement,"austrian_cuirassier_horse","0", []),
  # Var 1; Horse type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance
  
  ("royale_horse_spawn_arty",sokf_static_movement,"prussian_cuirassier_horse1","0", []),
  # Var 1; Horse type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance
  
  ("royale_cannon_spawn_field",sokf_static_movement,"cannon_12pdr","0", []),
  # Var 1; Cannon type: 0:random 1:12pdr 2:howitzer 3:mortar 4:rocket
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_cannon_spawn_fort",sokf_static_movement,"cannon_fort","0", []),
  # Var 1; Cannon type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_cannon_spawn_naval",sokf_static_movement,"cannon_naval","0", []),
  # Var 1; Cannon type: 0:random 1:naval 2:carronade
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_cannon_spawn_swievel",sokf_static_movement,"cannon_swievel","0", []),
  # Var 1; Cannon type: nothing
  # Var 2: Spawn chance: 0:Always 1-100% of chance

  ("royale_props_end", 0, "0", "0", []),
  
#modders_props:
    #   If custom button's var1 value is between 1 and 40,
    #   button's custom use label text is decided by its var1 value 
    #   and the name of corresponding trp_custom_string_[var1number] on server

  ("custom_button_instant",spr_use_time(0),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
        #   # Example: doing different things based on value of button's var2 as set in scene editor
        #   # (store_trigger_param_2, ":instance_id"),
        #   # (prop_instance_get_variation_id_2, ":button_type", ":instance_id"),
        #   # (try_begin),
        #   #   (eq, ":button_type", 1),
        #   #       (do_stuff),
        #   # (else_try),
        #   #   (eq, ":button_type", 2),
        #   #       (do_other_stuff),
        #   # (try_end),
    ]),
  ]),
  ("custom_button_1_second",spr_use_time(1),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
    ]),
  ]),
  ("custom_button_2_seconds",spr_use_time(2),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
    ]),
  ]),
  ("custom_button_4_seconds",spr_use_time(4),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
    ]),
  ]),
  ("custom_button_8_seconds",spr_use_time(8),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
    ]),
  ]),
  ("custom_button_16_seconds",spr_use_time(16),"0","cannon_button_collision", [
    (ti_on_scene_prop_use,
    [        #add custom server side code here.. 
    ]),
  ]),
  
#  ("custom_button_1_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_1_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_2_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_2_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_3_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_3_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_4_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_4_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_5_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_5_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_6_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_6_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_7_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_7_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_8_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_8_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_9_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_9_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
#  ("custom_button_10_4seconds",spr_use_time(4),"0","cannon_button_collision", [
#    (ti_on_init_scene_prop,
#      [
#        (troop_set_name, "trp_custom_button_10_4seconds", "@Use Me"), # Set custom use string here, displayed when looking at button
#      ]),
#    (ti_on_scene_prop_use,
#    [        #add custom server side code here.. 
#    ]),
#  ]),
  

  ("custom_buttons_end", 0,"0" ,"0" , []),
 
  ("mm_weather_fog_color_red", 0, "0", "0", []), # var1 0-127 number; var2: 0-127, values are added up to get a value of 0-254 in red color. (like html RGB)
  ("mm_weather_fog_color_green", 0, "0", "0", []), # var1 0-127 number; var2: 0-127, values are added up to get a value of 0-254 in green color. (like html RGB)
  ("mm_weather_fog_color_blue", 0, "0", "0", []), # var1 0-127 number; var2: 0-127, values are added up to get a value of 0-254 in blue color. (like html RGB)
 
  ("door_teleport_vertical",spr_use_time(2),"tavern_door_b","bo_tavern_door_a", [ # var1 0-127 number to link this teleporting door to other TP door. (can be of any type)
    check_common_teleport_door_trigger, 
  ]),
  ("door_teleport_horizontal",spr_use_time(2),"house_roof_door","bo_house_roof_door", [ # var1 0-127 number to link this teleporting door to other TP door. (can be of any type)
    check_common_teleport_door_trigger,
  ]),
  ("door_teleport_invisible",spr_use_time(2),"0","cannon_button_collision", [ # var1 0-127 number to link this teleporting door to other TP door. (can be of any type)
    check_common_teleport_door_trigger,
  ]),
  
  ("door_teleport_props_end", 0,"0" ,"0" , []),
  
  ("headquarters_base_flag_names",0,"0","0",[]), # custom name ids for the conquest flags that spawn on team base points (entries 64 and 65). var1 for team 1, var2 for team 2
 
 ("ground_prop_stone_a",0,"mm_ground_prop_stone_a","bo_zaval", []),
 ("ground_prop_patch_rock",0,"mm_ground_prop_patch_rock","bo_zaval", []),
 ("ground_prop_grassy_ground",0,"mm_ground_prop_grassy_ground","bo_zaval", []),
 #("ground_prop_ground_steppe",0,"mm_ground_prop_ground_steppe","bo_zaval", []),
 ("ground_prop_snow",0,"mm_ground_prop_snow","bo_zaval", []),
 #("ground_prop_pebbles",0,"mm_ground_prop_pebbles","bo_zaval", []),
 ("ground_prop_ground_earth",0,"mm_ground_prop_ground_earth","bo_zaval", []),
 ("ground_prop_ground_desert",0,"mm_ground_prop_ground_desert","bo_zaval", []),
 #("ground_prop_ground_forest",0,"mm_ground_prop_ground_forest","bo_zaval", []),
 #("ground_prop_ground_village",0,"mm_ground_prop_ground_village","bo_zaval", []),
 ("ground_prop_ground_path",0,"mm_ground_prop_ground_path","bo_zaval", []),
 ("ground_prop_stucco_5",0,"mm_ground_prop_stucco_5","bo_zaval", []),
 ("ground_prop_roof3",0,"mm_ground_prop_roof3","bo_zaval", []),
 ("ground_prop_bricks1",0,"mm_ground_prop_bricks1","bo_zaval", []),
 ("ground_prop_stone_wall_5",0,"mm_ground_prop_stone_wall_5","bo_zaval", []),
 ("ground_prop_wood1",0,"mm_ground_prop_wood1","bo_zaval", []),
 #("ground_prop_wood2",0,"mm_ground_prop_wood2","bo_zaval", []),
 ("ground_prop_wood4",0,"mm_ground_prop_wood4","bo_zaval", []),
 
 ("triangle_wood1",0,"mm_triangle_wood1","bo_mm_triangle_wood1", []),
 ("triangle_wood9",0,"mm_triangle_wood9","bo_mm_triangle_wood1", []),
 ("triangle_bricks1",0,"mm_triangle_bricks1","bo_mm_triangle_wood1", []),
 ("triangle_stucco_5",0,"mm_triangle_stucco_5","bo_mm_triangle_wood1", []),
 ("triangle_mmstuco",0,"mm_triangle_mmstuco","bo_mm_triangle_wood1", []),
 ("triangle_mmstuco4",0,"mm_triangle_mmstuco4","bo_mm_triangle_wood1", []),
 
 ("pyramid",0,"pyramid","bo_pyramid", []),
 ("mm_house_wall_1_sandstones2",0,"1wall_sandstones2","bo_1wall", []),
 
 
  ("scene_props_end", 0,"0" ,"0" , []),
]
