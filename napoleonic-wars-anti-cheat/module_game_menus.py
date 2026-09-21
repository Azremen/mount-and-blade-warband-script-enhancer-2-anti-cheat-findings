# -*- coding: cp1254 -*-
from header_game_menus import *
from module_constants import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################

game_menus = [
  ("start_game_0",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Welcome, Soldier, to Mount and Blade Stories: Age of Napoleon.^Before beginning the game you must create your character and choose your preferred difficulty.",
    "none",
    [ 
      (change_screen_quit),
      
      (eq,1,0),
      
      (assign,"$g_pres_started_from_mission",0),
      (try_begin),
        (neq,"$g_has_been_first_started",1),
      # (try_begin),
        # (gt,"$g_next_presentation",-1),
        # (start_presentation, "$g_next_presentation"),
      # (else_try),
       (assign,"$g_has_been_first_started",1),
       (assign,"$g_sp_money_gained",0),
       (assign,"$g_sp_allies_lost",0),
       (assign,"$g_sp_companions_lost",0),
       (assign,"$g_sp_enemies_killed",0),
       (assign,"$g_sp_personal_kills",0),
      
      
       # Beaver - added below for custom battles - NEEDS TWEAKING
      # BRITAIN
      (troop_set_slot,"trp_british_infantry_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_british_infantry2_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_british_highlander_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_british_foot_guard_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_british_rifle_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_british_dragoon_ai", slot_troop_initial_morale, 5000),
      #(troop_set_slot,"trp_british_dragoon2_ai", slot_troop_initial_morale, 5000),
      
      # FRANCE
      (troop_set_slot,"trp_french_infantry_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_french_infantry2_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_french_infantry_vistula_ai", slot_troop_initial_morale, 3000),
      #(troop_set_slot,"trp_french_infantry_bavarian_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_french_voltigeur_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_french_old_guard_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_french_hussar_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_french_lancer_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_french_dragoon_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_french_cuirassier_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_french_carabineer_ai", slot_troop_initial_morale, 5000),
      
      # PRUSSIA
      (troop_set_slot,"trp_prussian_infantry_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_prussian_infantry_kurmark_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_prussian_infantry_15_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_prussian_infantry_rifle_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_prussian_dragoon_ai", slot_troop_initial_morale, 5000),
      #(troop_set_slot,"trp_prussian_ulany_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_prussian_landwehr_cav_ai", slot_troop_initial_morale, 4000),
      
      # RUSSIA
      (troop_set_slot,"trp_russian_opol_ai", slot_troop_initial_morale, 2000),
      (troop_set_slot,"trp_russian_infantry_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_russian_grenadier_ai", slot_troop_initial_morale, 4000),
      (troop_set_slot,"trp_russian_foot_guard_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_russian_infantry_rifle_ai", slot_troop_initial_morale, 3000),
      (troop_set_slot,"trp_russian_hussar_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_russian_cossack_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_russian_dragoon_ai", slot_troop_initial_morale, 5000),
      (troop_set_slot,"trp_russian_horse_guard_ai", slot_troop_initial_morale, 5000),
      
      (try_for_range,":value",0,20),
         (troop_set_slot,"trp_custom_battle_dummy",":value",0),
      (try_end),
      (try_for_range,":value",20,40),
         (troop_set_slot,"trp_custom_battle_dummy",":value",20),
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
      
         #faction banners
      (faction_set_slot, "fac_britain", slot_faction_banner, "mesh_banner_kingdom_f"),
      (faction_set_slot, "fac_france", slot_faction_banner, "mesh_banner_kingdom_b"),
      (faction_set_slot, "fac_prussia", slot_faction_banner, "mesh_banner_kingdom_c"),
      (faction_set_slot, "fac_russia", slot_faction_banner, "mesh_banner_kingdom_a"),
      (faction_set_slot, "fac_austria", slot_faction_banner, "mesh_banner_kingdom_d"),
      #(faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_kingdom_e"),
        
        (troop_set_type,"trp_player",0),
        (assign,"$character_gender",tf_male), # Assign to male at all times to fit the stories.. Im sorry ladies =( xxx vince.
        (set_show_messages, 0),
        
        # Uniform
        (troop_add_item, "trp_player","itm_french_inf_shako_84_officer"),
        (troop_add_item, "trp_player","itm_french_84e_body_officer"),
        (troop_add_item, "trp_player","itm_french_voltigeur_officer_pants"),
        
        # Weapons
        
        (try_begin), 	   
          (eq, debug_mode, 1), 		   
          (troop_add_item, "trp_player","itm_grenade",0),
          (troop_add_item, "trp_player","itm_grenade",0),
          #(troop_add_item, "trp_player","itm_french_officer_pistol"),
          ###
          (troop_add_item, "trp_player","itm_sniper_rifle"),
          (troop_add_item, "trp_player","itm_explosive_bullets"),
          ###
          (troop_add_item, "trp_player","itm_french_inf_off_sabre"),
          #(troop_add_item, "trp_player","itm_pistol_ammo"),
          #(troop_add_item, "trp_player","itm_heavy_horse_dragon"),
        (else_try),
          (troop_add_item, "trp_player","itm_french_charleville"),
          (troop_add_item, "trp_player","itm_bullets"),
          (troop_add_item, "trp_player","itm_french_briquet"),
        (end_try), 
        
        (assign, "$g_player_troop", "trp_player"),
        (troop_raise_skill, "$g_player_troop", skl_athletics, 2),
        (troop_raise_skill, "$g_player_troop", skl_riding, 3),
        (troop_raise_skill, "$g_player_troop", skl_power_strike, 1),
        (troop_raise_skill, "$g_player_troop", skl_weapon_master, 4),
        (troop_raise_skill, "$g_player_troop", skl_ironflesh, 7),
        
        (assign,"$g_finished_missions",0),
        (assign,"$g_finished_sub_missions",0),
        
         # Give the player some random companions.
         (assign,":found_companions",0),
         (assign,":loop_end",1000),
         (try_for_range, ":companion_number", 0, ":loop_end"),
           (store_random_in_range,":random_companion",companions_begin, companions_end),
           (neg|troop_slot_eq,":random_companion", slot_troop_occupation, slto_player_companion),
           (troop_set_slot,":random_companion", slot_troop_occupation, slto_player_companion),
           (val_add,":found_companions",1),
           (eq,":found_companions",10),
           (assign,":loop_end",0),
           (eq,":companion_number",":companion_number"), # remove warning
         (try_end),
        
        (troop_add_gold, "trp_player", 5000),
        
        (troop_equip_items, "trp_player"),
      (try_end),
    ],
    [

       ("start_easy",[],"Easy",
       [
        (options_set_damage_to_player, 0),  #    = 261 # (options_set_damage_to_player, <value>), #0 = 1/4, 1 = 1/2, 2 = 1/1
        (options_set_damage_to_friends, 0), #    = 263 # (options_set_damage_to_friends, <value>), #0 = 1/2, 1 = 3/4, 2 = 1/1
        (options_set_combat_ai, 2),         #    = 265 # (options_set_combat_ai, <value>), #0 = good, 1 = average, 2 = poor
        (options_set_campaign_ai, 2),       #    = 267 # (options_set_campaign_ai, <value>), #0 = good, 1 = average, 2 = poor
        (options_set_combat_speed, 0),      #    = 269 # (options_set_combat_speed, <value>), #0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
        (assign,"$g_global_morale_modifier",12), #Player troops' morale x1.2
        (start_presentation, "prsnt_singleplayer_campain_map"),
		    #(jump_to_menu, "mnu_start_game_1"),
        #(assign,"$g_finished_missions",2),
        ]
       ),
	   
      ("start_normal",[],"Normal",
       [
		   (options_set_damage_to_player, 1),  #    = 261 # (options_set_damage_to_player, <value>), #0 = 1/4, 1 = 1/2, 2 = 1/1
		   (options_set_damage_to_friends, 1), #    = 263 # (options_set_damage_to_friends, <value>), #0 = 1/2, 1 = 3/4, 2 = 1/1
		   (options_set_combat_ai, 0),         #    = 265 # (options_set_combat_ai, <value>), #0 = good, 1 = average, 2 = poor
		   (options_set_campaign_ai, 1),       #    = 267 # (options_set_campaign_ai, <value>), #0 = good, 1 = average, 2 = poor
		   (options_set_combat_speed, 2),      #    = 269 # (options_set_combat_speed, <value>), #0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
       (assign,"$g_global_morale_modifier",10), #Player troops' morale x1.0
       (start_presentation, "prsnt_singleplayer_campain_map"),
		   #(jump_to_menu, "mnu_start_game_1"),
        ]
       ),

      ("start_hard",[],"Hard",
       [
		    (options_set_damage_to_player, 2),  #    = 261 # (options_set_damage_to_player, <value>), #0 = 1/4, 1 = 1/2, 2 = 1/1
		    (options_set_damage_to_friends, 2), #    = 263 # (options_set_damage_to_friends, <value>), #0 = 1/2, 1 = 3/4, 2 = 1/1
		    (options_set_combat_ai, 0),         #    = 265 # (options_set_combat_ai, <value>), #0 = good, 1 = average, 2 = poor
		    (options_set_campaign_ai, 0),       #    = 267 # (options_set_campaign_ai, <value>), #0 = good, 1 = average, 2 = poor
		    (options_set_combat_speed, 4),      #    = 269 # (options_set_combat_speed, <value>), #0 = slowest, 1 = slower, 2 = normal, 3 = faster, 4 = fastest
        (assign,"$g_global_morale_modifier",8), #Player troops' morale x0.8
        (start_presentation, "prsnt_singleplayer_campain_map"),
			  #(jump_to_menu, "mnu_start_game_1"),
        ]
       ),
      ("go_back",[],"Go back",
       [
         (change_screen_quit),
       ]),
      ("debug",[],"Debug",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),

 ("start_phase_2", mnf_disable_all_keys,
	"Start Phase 2",
	"none",
	[],
	[
	    ("map", [], "Map",
		[
		    (change_screen_map),
		]),
	]),
	
	("start_game_3", mnf_disable_all_keys,
	"Start Game 3",
	"none",
	[
  (change_screen_quit),
      
      (eq,1,0),
      ],
	[
	]),

  (
    "tutorial",mnf_disable_all_keys,
    "Good Afternoon, Sir. Beautiful weather today, sir. Would you care for a cup of tea?",
    "none",
    [
      (try_begin),
        (eq, "$g_tutorial_entered", 1),
        (change_screen_quit),
      (else_try),
        (set_passage_menu, "mnu_tutorial"),
        (assign, "$g_tutorial_entered", 1),
        (play_sound,"snd_tutorial_voice_start_1"),
      (try_end),
    ],
    [

      ("continue",[],"Yes, please.",
      [
        (stop_all_sounds,1),
        (modify_visitors_at_site,"scn_tutorial"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
        (assign, "$g_player_troop", "trp_player"),
        (troop_raise_attribute, "$g_player_troop", ca_strength, 14),
        (troop_raise_attribute, "$g_player_troop", ca_agility, 14),
        (troop_raise_skill, "$g_player_troop", skl_athletics, 3),
        (troop_raise_skill, "$g_player_troop", skl_riding, 6),
        (troop_raise_skill, "$g_player_troop", skl_power_strike, 3),
        (troop_raise_skill, "$g_player_troop", skl_weapon_master, 4),
        (troop_raise_skill, "$g_player_troop", skl_ironflesh, 3),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_one_handed_weapon, 80),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_polearm, 130),
        (troop_raise_proficiency_linear, "$g_player_troop", wpt_crossbow, 150),
     
        (troop_clear_inventory, "$g_player_troop"),
        (troop_add_item, "$g_player_troop","itm_british_infantry_ranker",0),
        (troop_add_item, "$g_player_troop","itm_french_voltigeur_officer_pants",0),
        (troop_add_item, "$g_player_troop","itm_33_stovepipe",0),
        #(troop_add_item, "$g_player_troop","itm_ramrod",0),
        #(troop_add_item, "$g_player_troop","itm_rockets",0),
        (troop_equip_items, "$g_player_troop"),
        (set_visitor,0,"trp_player"),
        (set_jump_mission,"mt_tutorial"),
        (jump_to_scene,"scn_tutorial"),
        (change_screen_mission),
        ]),

      ("go_back_dot",
      [],
      "No, thanks.",
       [
         (stop_all_sounds,1),
         (change_screen_quit),
       ]),
    ]
  ),

    ("reports", 0,
    "Reports",
    "none",
    [],
    [
      ("resume_travelling",[],"Resume travelling.",
      [
      (change_screen_return),
      ]),
    ]),

    ("camp", mnf_scale_picture,
    "Camp",
    "none",
    [
    ],
    [
      ("camp_wait_here", [], "Rest.",
      [
        (rest_for_hours_interactive, 24 * 365, 5, 1),
        (change_screen_return),
      ]),
  
      ("resume_travelling",[], "Dismantle camp.",
      [
        (change_screen_return),
      ]),
    ]),
  
  

  (
    "custom_battle_scene",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "(NO_TRANS)",
	
    "none",
    [],
    [

      ("quick_battle_scene_1",[],"{!}quick_battle_scene_1",
       [
       #    (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_1"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_2",[],"{!}quick_battle_scene_2",
       [
         #  (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_2"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_3",[],"{!}quick_battle_scene_3",
       [
        #   (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_3"),(change_screen_mission)        
		]
       ),
      ("quick_battle_scene_4",[],"{!}quick_battle_scene_4",
       [
         #  (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_4"),(change_screen_mission)        
		]
       ),
      # ("quick_battle_scene_5",[],"{!}quick_battle_scene_5",
       # [
          ##(set_jump_mission,"mt_ai_training"),
           # (jump_to_scene,"scn_quick_battle_scene_5"),(change_screen_mission)        
		# ]
       # ),
	   
      ("go_back",[],"{!}Go back",
       [(change_screen_quit),
        ]
       ),
      ]
  ),
  
  #depreciated



  (
    "custom_battle_end",mnf_disable_all_keys,
    "The battle is over. {s1} Your side killed {reg5} enemies and lost {reg6} troops over the battle. You personally slew {reg7} men in the fighting.",
    "none",
    [(music_set_situation, 0),
     (assign, reg5, "$g_custom_battle_team2_death_count"),
     (assign, reg6, "$g_custom_battle_team1_death_count"),
     (get_player_agent_kill_count, ":kill_count"),
     (get_player_agent_kill_count, ":wound_count", 1),
     (store_add, reg7, ":kill_count", ":wound_count"),
     (try_begin),
       (eq, "$g_battle_result", 1),
       (str_store_string, s1, "str_battle_won"),
     (else_try),
       (str_store_string, s1, "str_battle_lost"),
     (try_end),
     ],
    [
      ("continue",[],"Continue.",
       [(change_screen_quit),
        ]
       ),
    ]
  ),

  (
    "town_trade",0,
    "You head towards the camp's trading place.",
    "none",
    [],
    [
      ("trade_with_arms_merchant",[],
       "Trade with the arms merchant.",
       [
           (change_screen_trade, "trp_camp_weaponsmith"),
        ]),
      ("trade_with_armor_merchant",[],
       "Trade with the tailor.",
       [
           (change_screen_trade, "trp_camp_armorer"),
        ]),
      ("trade_with_horse_merchant",[],
       "Trade with the horse merchant.",
       [
           (change_screen_trade, "trp_camp_horse_merchant"),
        ]),
      ("back_to_town_menu",[],"Head back.",
       [
         (start_presentation,"prsnt_singleplayer_camp_screen"),
        ]),
    ]
  ),

  
  ("debug",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Choose a scene",
    "none",
    [],
    [
     ("scene1",[],"Vienna Bridge (sp_vienna)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_vienna"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_vienna"),
        (jump_to_scene,"scn_sp_vienna"),
        (change_screen_mission),
        ]
       ),
     ("scene2",[],"Austerlitz part 1 (sp_sokolniz)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_sokolniz"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_austerlitz_1"),
        (jump_to_scene,"scn_sp_sokolniz"),
        (change_screen_mission),
        ]
       ),
       ("scene3",[],"Austerlitz part 2 (sp_auster)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_auster"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_austerlitz_2"),
        (jump_to_scene,"scn_sp_auster"),
        (change_screen_mission),
        ]
       ),
      ("scene4",[],"Austerlitz part 3 (sp_sokolniz2)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_sokolniz2"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_austerlitz_3"),
        (jump_to_scene,"scn_sp_sokolniz2"),
        (change_screen_mission),
        ]
       ),
      ("scene5",[],"Dresden part 1 (sp_dresden1)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_dresden1"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_dresden_1"),
        (jump_to_scene,"scn_sp_dresden1"),
        (change_screen_mission),
        ]
       ),
      ("scene6",[],"Dresden part 2 (sp_dresden2)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_dresden2"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_dresden_2"),
        (jump_to_scene,"scn_sp_dresden2"),
        (change_screen_mission),
        ]
       ),
      ("scene7",[],"New Scene 1 (NON-PLAYABLE)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_scene_1"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_dresden_2"),
        (jump_to_scene,"scn_sp_scene_1"),
        (change_screen_mission),
        ]
       ),
      ("scene8",[],"New Scene 2 (NON-PLAYABLE)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_scene_2"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_dresden_2"),
        (jump_to_scene,"scn_sp_scene_2"),
        (change_screen_mission),
        ]
       ),
      ("scene9",[],"New Scene 3 (NON-PLAYABLE)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_scene_3"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_dresden_2"),
        (jump_to_scene,"scn_sp_scene_3"),
        (change_screen_mission),
        ]
       ),
      ("scene10",[],"New Scene 4 (NON-PLAYABLE)",
       [
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_scene_4"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        #(set_jump_mission,"mt_sp_campaign_dresden_2"),
        (jump_to_scene,"scn_sp_scene_4"),
        (change_screen_mission),
        ]
       ),
      ("go_back",[],"Go back",
       [
         (jump_to_menu, "mnu_start_game_0"),
       ]),
    ]
  ),

  
  (
    "run_mission_dummy",mnf_disable_all_keys,
    "debug screen",
    "none",
    [
    (try_begin),
      (eq,"$g_started_mission",1),
      (assign,"$g_started_mission",0),
      (assign,"$g_global_morale_modifier",10),
      (try_begin),
        (eq,"$g_finished_missions",0), # Vienna
        
        (assign,"$g_global_morale_modifier",10),
        (modify_visitors_at_site,"scn_sp_vienna"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_vienna"),
        (jump_to_scene,"scn_sp_vienna"),
        (change_screen_mission),
        
      (else_try),
        (eq,"$g_finished_missions",1), # Austerlitz

        (modify_visitors_at_site,"scn_sp_sokolniz"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
     
        (set_visitor,0,"trp_player"),
       
        (set_jump_mission,"mt_sp_campaign_austerlitz_1"),
         #(jump_to_menu, "mnu_custom_battle_end"),
        (jump_to_scene,"scn_sp_sokolniz"),
        (change_screen_mission),
       
         # (presentation_set_duration,0),
      (else_try),
        (eq,"$g_finished_missions",2), # Drezden
        (try_begin),
          (eq,"$g_finished_sub_missions",0), # part 1
          
          (modify_visitors_at_site,"scn_sp_dresden1"),
          (reset_visitors, 0),
          (set_player_troop, "trp_player"),
       
          (set_visitor,0,"trp_player"),
         
          (set_jump_mission,"mt_sp_campaign_dresden_1"),
          (jump_to_scene,"scn_sp_dresden1"),
          (change_screen_mission),
          #(presentation_set_duration,0),
        (else_try),
          (eq,"$g_finished_sub_missions",1), # part 2
          
          (modify_visitors_at_site,"scn_sp_dresden2"),
          (reset_visitors, 0),
          (set_player_troop, "trp_player"),
       
          (set_visitor,0,"trp_player"),
         
          (set_jump_mission,"mt_sp_campaign_dresden_2"),
          (jump_to_scene,"scn_sp_dresden2"),
          (change_screen_mission),
        (try_end),
      (else_try),
        #(val_add,"$g_finished_missions",1),
        #(val_add,"$g_finished_sub_missions",1),
        #(jump_to_menu, "mnu_custom_battle_end"),
        (start_presentation, "prsnt_singleplayer_mission_results"),
      (try_end),
    (try_end),
    
            
     ],
    [
      ("continue",[],"Continue",
       [
         (start_presentation, "prsnt_singleplayer_mission_results"),
       ]),
       ("debug",[],"Debug menu",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),
  
  (
    "run_companion_dummy",mnf_disable_all_keys,
    "debug screen",
    "none",
    [
    (try_begin),
      (neq,"$g_started_companion",0),
      (assign,":this_comp","$g_started_companion"),
      (assign,"$g_started_companion",0),
      (change_screen_equip_other, ":this_comp"),
    (else_try),
      #(val_add,"$g_finished_missions",1),
      #(val_add,"$g_finished_sub_missions",1),
      #(jump_to_menu, "mnu_custom_battle_end"),
      #(start_presentation, "prsnt_singleplayer_mission_results"),
    (try_end),

     ],
    [
      ("continue",[],"Continue",
       [
         (start_presentation, "prsnt_singleplayer_companion_equipment_select"),
       ]),
       ("debug",[],"Debug menu",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),
  
  (
    "visit_camp_dummy",mnf_disable_all_keys,
    "debug screen",
    "none",
    [
    (try_begin),
      (neq,"$g_started_camp",0),
      (assign,":this_scn","$g_started_camp"),
      (assign,"$g_started_camp",0),
      
      (modify_visitors_at_site,":this_scn"),
      (reset_visitors, 0),
      (set_player_troop, "trp_player"),
   
      (set_visitor,0,"trp_player"),
     
      (set_jump_mission,"mt_camp_1"),
      (jump_to_scene,":this_scn"),
      (change_screen_mission),
      
    (else_try),
      #(val_add,"$g_finished_missions",1),
      #(val_add,"$g_finished_sub_missions",1),
      #(jump_to_menu, "mnu_custom_battle_end"),
      #(start_presentation, "prsnt_singleplayer_mission_results"),
    (try_end),

     ],
    [
      ("continue",[],"Continue",
       [
         (start_presentation, "prsnt_singleplayer_camp_screen"),
       ]),
       ("debug",[],"Debug menu",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),
  
  (
    "go_briefing_dummy",mnf_disable_all_keys,
    "debug screen",
    "none",
    [

     ],
    [
      ("continue",[],"Continue",
       [
         (start_presentation, "prsnt_singleplayer_memoir_screen"),
       ]),
       ("debug",[],"Debug menu",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),
  
  (
    "quit_dummy",mnf_disable_all_keys,
    "debug screen",
    "none",
    [
    (change_screen_quit),

     ],
    [
      ("continue",[],"Continue",
       [
         (start_presentation, "prsnt_singleplayer_camp_screen"),
       ]),
       ("debug",[],"Debug menu",
       [
         (assign,"$character_gender",tf_male),
         (jump_to_menu, "mnu_debug"),
       ]),
    ]
  ),
 # (change_screen_quit),
  
 ]
