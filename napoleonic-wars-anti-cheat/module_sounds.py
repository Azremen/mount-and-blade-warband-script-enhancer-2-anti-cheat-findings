from header_sounds import *
from ID_factions import *

# default values:
# sf_priority_5
# sf_vol_10

sounds = [
 ("click", sf_2d|sf_vol_1,["drum_3.wav"]),
 ("gong", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_taken", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_completed", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_succeeded", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_concluded", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_failed", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_cancelled", sf_2d|sf_priority_9|sf_vol_7, []),
 ("rain",sf_2d|sf_priority_15|sf_vol_4|sf_looping, ["rain_1.wav"]),
 ("snow",sf_2d|sf_priority_15|sf_vol_4|sf_looping, ["snow.wav"]),
 ("money_received",sf_2d|sf_priority_10|sf_vol_6, []),
 ("money_paid",sf_2d|sf_priority_10|sf_vol_10, []),
 ("sword_clash_1", sf_priority_3|sf_vol_9,["sword_clank_metal_09.wav","sword_clank_metal_09b.wav","sword_clank_metal_10.wav","sword_clank_metal_10b.wav","sword_clank_metal_12.wav","sword_clank_metal_12b.wav","sword_clank_metal_13.wav","sword_clank_metal_13b.wav","weapon_sabre01.wav","weapon_sabre02.wav","weapon_sabre03.wav"]),
 ("sword_clash_2", 0,[]),#"s_swordClash2.wav"]),
 ("sword_clash_3", 0,[]),#"s_swordClash3.wav"]),
 ("sword_swing", sf_priority_2|sf_vol_8,["s_swordSwing.wav"]),
 ("footstep_grass", sf_priority_1|sf_vol_4,["footstep_1.wav","footstep_2.wav","footstep_3.wav","footstep_4.wav"]),
 ("footstep_wood", sf_priority_1|sf_vol_6,["footstep_wood_1.wav","footstep_wood_2.wav","footstep_wood_4.wav"]),

 ("footstep_water", sf_priority_1|sf_vol_3,["water_walk_1.wav","water_walk_2.wav","water_walk_3.wav","water_walk_4.wav"]),
 ("footstep_horse",sf_priority_8|sf_vol_8, []),#"footstep_horse_5.ogg","footstep_horse_2.ogg","footstep_horse_3.ogg","footstep_horse_4.ogg"]),
# ("footstep_horse",0, ["s_footstep_horse_4b.wav","s_footstep_horse_4f.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
 ("footstep_horse_1b",sf_priority_8|sf_vol_8, ["s_footstep_horse_4b.wav","s_footstep_horse_4f.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
 ("footstep_horse_1f",sf_priority_8|sf_vol_8, ["s_footstep_horse_2b.wav","s_footstep_horse_2f.wav","s_footstep_horse_3b.wav","s_footstep_horse_3f.wav"]),
# ("footstep_horse_1f",sf_priority_3|sf_vol_15, ["footstep_horse_5.ogg","footstep_horse_2.ogg","footstep_horse_3.ogg","footstep_horse_4.ogg"]),
 ("footstep_horse_2b",sf_priority_8|sf_vol_8, ["s_footstep_horse_2b.wav"]),
 ("footstep_horse_2f",sf_priority_8|sf_vol_8, ["s_footstep_horse_2f.wav"]),
 ("footstep_horse_3b",sf_priority_8|sf_vol_8, ["s_footstep_horse_3b.wav"]),
 ("footstep_horse_3f",sf_priority_8|sf_vol_8, ["s_footstep_horse_3f.wav"]),
 ("footstep_horse_4b",sf_priority_8|sf_vol_8, ["s_footstep_horse_4b.wav"]),
 ("footstep_horse_4f",sf_priority_8|sf_vol_8, ["s_footstep_horse_4f.wav"]),
 ("footstep_horse_5b",sf_priority_8|sf_vol_8, ["s_footstep_horse_5b.wav"]),
 ("footstep_horse_5f",sf_priority_8|sf_vol_8, ["s_footstep_horse_5f.wav"]),
 ("jump_begin", sf_vol_7|sf_priority_9,["jump_begin.wav"]),
 ("jump_end", sf_vol_5|sf_priority_9,["jump_end.wav"]),
 ("jump_begin_water", sf_vol_4|sf_priority_9,["jump_begin_water.wav"]),
 ("jump_end_water", sf_vol_4|sf_priority_9,["jump_end_water.wav"]),
 ("horse_jump_begin", sf_vol_8|sf_priority_9,["horse_jump_begin.wav"]),
 ("horse_jump_end", sf_vol_8|sf_priority_9,["horse_jump_end.wav"]),
 ("horse_jump_begin_water", sf_vol_6|sf_priority_9,["jump_begin_water.wav"]),
 ("horse_jump_end_water", sf_vol_6|sf_priority_9,["jump_end_water.wav"]),

 ("release_bow",sf_vol_5, []),
 ("release_crossbow",sf_vol_1, []),
 ("throw_javelin",sf_vol_5, []),
 ("throw_axe",sf_vol_7, []),
 ("throw_knife",sf_vol_5, []),
 ("throw_stone",sf_vol_7, ["throw_stone_1.wav"]),

 ("reload_crossbow",sf_priority_1|sf_vol_2, ["reload_musket.wav"]),
 ("reload_crossbow_continue",sf_priority_3|sf_vol_2, []),
 ("pull_bow",sf_vol_4, []),
 ("pull_arrow",sf_vol_5, []),

 ("arrow_pass_by",0, []),
 ("bolt_pass_by",0, ["bulletpass1.wav","bulletpass2.wav","bulletpass3.wav","bulletpass4.wav"]), #MM
 ("javelin_pass_by",0, []),
 ("stone_pass_by",sf_vol_9, []),
 ("axe_pass_by",0, []),
 ("knife_pass_by",0, []),
 ("bullet_pass_by",0, ["bulletpass1.wav","bulletpass2.wav","bulletpass3.wav","bulletpass4.wav"]),
 
 ("incoming_arrow_hit_ground",sf_priority_7|sf_vol_7, []),
 ("incoming_bolt_hit_ground",sf_priority_7|sf_vol_10, ["musket_groundhit.wav","musket_groundhit1.wav"]), #MM
 ("incoming_javelin_hit_ground",sf_priority_7|sf_vol_7, []),
 ("incoming_stone_hit_ground",sf_priority_7|sf_vol_7, []),
 ("incoming_axe_hit_ground",sf_priority_7|sf_vol_7, []),
 ("incoming_knife_hit_ground",sf_priority_7|sf_vol_7, []),
 ("incoming_bullet_hit_ground",sf_priority_7|sf_vol_10, ["musket_groundhit.wav","musket_groundhit1.wav"]),

 ("outgoing_arrow_hit_ground",sf_priority_7|sf_vol_7, []),
 ("outgoing_bolt_hit_ground",sf_priority_7|sf_vol_10,  ["musket_groundhit.wav","musket_groundhit1.wav"]), #MM
 ("outgoing_javelin_hit_ground",sf_priority_7|sf_vol_10, []),
 ("outgoing_stone_hit_ground",sf_priority_7|sf_vol_7, []),
 ("outgoing_axe_hit_ground",sf_priority_7|sf_vol_7, []),
 ("outgoing_knife_hit_ground",sf_priority_7|sf_vol_7, []),
 ("outgoing_bullet_hit_ground",sf_priority_7|sf_vol_10, ["musket_groundhit.wav","musket_groundhit1.wav"]),

 ("draw_sword",sf_priority_1|sf_vol_3, ["draw_sword.wav","draw_sword2.wav"]),
 ("put_back_sword",sf_priority_1|sf_vol_3, ["put_back_sword.wav"]),
 ("draw_greatsword",sf_priority_1|sf_vol_3, ["draw_greatsword.wav"]),
 ("put_back_greatsword",sf_priority_1|sf_vol_3, ["put_back_sword.wav"]),
 ("draw_axe",sf_priority_1|sf_vol_3, ["draw_mace.wav"]),
 ("put_back_axe",sf_priority_1|sf_vol_3, ["put_back_to_holster.wav"]),
 ("draw_greataxe",sf_priority_1|sf_vol_3, ["draw_greataxe.wav"]),
 ("put_back_greataxe",sf_priority_1|sf_vol_3, ["put_back_to_leather.wav"]),
 ("draw_spear",sf_priority_1|sf_vol_3, ["draw_spear.wav"]),
 ("put_back_spear",sf_priority_1|sf_vol_3, ["put_back_to_leather.wav"]),
 ("draw_crossbow",sf_priority_1|sf_vol_3, ["draw_crossbow.wav","draw_other3.wav"]),
 ("put_back_crossbow",sf_priority_1|sf_vol_3, ["put_back_to_leather.wav"]),
 ("draw_revolver",sf_priority_1|sf_vol_3, ["draw_from_holster.wav"]),
 ("put_back_revolver",sf_priority_1|sf_vol_3, ["put_back_to_holster.wav"]),
 ("draw_dagger",sf_priority_1|sf_vol_3, ["draw_dagger.wav"]),
 ("put_back_dagger",sf_priority_1|sf_vol_3, ["put_back_dagger.wav"]),
 ("draw_bow",sf_priority_1|sf_vol_3, []),
 ("put_back_bow",sf_priority_1|sf_vol_3, []),
 ("draw_shield",sf_priority_1|sf_vol_3, []),
 ("put_back_shield",sf_priority_1|sf_vol_3, []),
 ("draw_other",sf_priority_1|sf_vol_3, ["draw_other.wav"]),
 ("put_back_other",sf_priority_1|sf_vol_3, ["draw_other2.wav"]),

 ("body_fall_small",sf_priority_6|sf_vol_10, ["body_fall_small_1.wav","body_fall_small_2.wav"]),
 ("body_fall_big",sf_priority_6|sf_vol_10, ["body_fall_1.wav","body_fall_2.wav","body_fall_3.wav"]),
 ("horse_body_fall_begin",sf_priority_6|sf_vol_10, ["horse_body_fall_begin_1.wav"]),
 ("horse_body_fall_end",sf_priority_6|sf_vol_10, ["horse_body_fall_end_1.wav","body_fall_2.wav"]),
 
 ("hit_wood_wood",sf_priority_6|sf_vol_7, ["hit_wood_wood_1.wav","hit_wood_wood_2.wav","hit_wood_wood_3.wav","hit_wood_wood_4.wav","hit_wood_metal_4.wav","hit_wood_metal_5.wav","hit_wood_metal_6.wav"]),#dummy
 ("hit_metal_metal",sf_priority_6|sf_vol_7, ["hit_metal_metal_3.wav","hit_metal_metal_4.wav",
                                              "hit_metal_metal_5.wav","hit_metal_metal_6.wav","hit_metal_metal_7.wav","hit_metal_metal_8.wav",
                                              "hit_metal_metal_9.wav","hit_metal_metal_10.wav",
                                              "clang_metal_1.wav","clang_metal_2.wav","weapon_sabre01.wav","weapon_sabre02.wav","weapon_sabre03.wav"]),
 ("hit_wood_metal",sf_priority_6|sf_vol_7, ["hit_metal_metal_1.wav","hit_metal_metal_2.wav","hit_wood_metal_7.wav"]),

 ("shield_hit_wood_wood",sf_priority_7|sf_vol_10, []),
 ("shield_hit_metal_metal",sf_priority_7|sf_vol_10, []),
 ("shield_hit_wood_metal",sf_priority_7|sf_vol_10, []),
 ("shield_hit_metal_wood",sf_priority_7|sf_vol_10, []),
 ("shield_broken",sf_priority_9, []),
 ("man_hit",sf_priority_5|sf_vol_7, [
  "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav","man_pain_25.wav"
 ,"man_pain_26.wav","man_pain_27.wav","man_pain_28.wav","man_pain_29.wav"
 ]),
 # ("man_hit",sf_priority_5|sf_vol_7, ["man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav",
                                      # "man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_47.wav","man_hit_57.wav","man_hit_59.wav"]),
 
 ("man_die",sf_priority_6|sf_vol_8, [
  "man_death_1.wav","man_death_2.wav","man_death_3.wav","man_death_4.wav","man_death_5.wav"
 ,"man_death_6.wav","man_death_7.wav","man_death_8.wav","man_death_9.wav","man_death_10.wav"
 ,"man_death_11.wav","man_death_12.wav","man_death_13.wav","man_death_14.wav","man_death_15.wav"
 ,"man_death_16.wav","man_death_17.wav","man_death_18.wav","man_death_19.wav","man_death_20.wav"
 ,"man_death_21.wav","man_death_22.wav","man_death_23.wav","man_death_24.wav","man_death_25.wav"
 ,"man_death_26.wav","man_death_27.wav","man_death_28.wav","man_death_29.wav","man_death_30.wav"
 ,"man_death_31.wav","man_death_32.wav"
 ]),
 # ("man_die",sf_priority_6|sf_vol_8,  ["man_death_1.wav","man_death_8.wav","man_death_8b.wav","man_death_11.wav","man_death_14.wav","man_death_16.wav","man_death_18.wav","man_death_21.wav","man_death_29.wav","man_death_40.wav","man_death_44.wav","man_death_46.wav","man_death_48.wav","man_death_64.wav"
                            # MM
                             # ,"death1.wav","death2.wav","death3.wav","death4.wav"
                             # ]),# ["man_fall_1.ogg","man_fall_2.ogg","man_fall_3.ogg","man_fall_4.ogg"]),
 ("woman_hit",sf_priority_5|sf_vol_7, ["woman_hit_2.wav","woman_hit_3.wav",
                              "woman_hit_b_2.wav","woman_hit_b_4.wav","woman_hit_b_6.wav","woman_hit_b_7.wav","woman_hit_b_8.wav",
                              "woman_hit_b_11.wav","woman_hit_b_14.wav","woman_hit_b_16.wav",
                              "woman_pain_1.wav",
                              "woman_pain_2.wav",
                              "woman_pain_3.wav",
                              "woman_pain_4.wav",
                              "woman_pain_5.wav",
                              "woman_pain_6.wav",
                              "woman_pain_7.wav",
                              "woman_pain_8.wav",
                              "woman_pain_9.wav",
                              "woman_pain_10.wav",
                              "woman_pain_11.wav",
                              "woman_pain_12.wav",
                              ]),
 ("woman_die",sf_priority_6|sf_vol_8, [
   "woman_fall_1.wav","woman_hit_b_5.wav"
  ,"woman_death_1.wav"
  ,"woman_death_2.wav"
  ,"woman_death_3.wav"
  ,"woman_death_4.wav"
  ,"woman_death_5.wav"
  ,"woman_death_6.wav"
  ,"woman_death_7.wav"
  ,"woman_death_8.wav"
  ,"woman_death_9.wav"
  ,"woman_death_10.wav"
  ,"woman_death_11.wav"
  ,"woman_death_12.wav"
  ,"woman_death_13.wav"
  ,"woman_death_14.wav"
  ,"woman_death_15.wav"
  ,"woman_death_16.wav"
  ,"woman_death_17.wav"
  ,"woman_death_18.wav"
  ,"woman_death_19.wav"
  ,"woman_death_20.wav"
  ,"woman_death_21.wav"
  ,"woman_death_22.wav"
  ,"woman_death_23.wav"
 ]),
 ("woman_yell",sf_priority_10|sf_vol_10, []),#"woman_yell_1.wav","woman_yell_2.wav"]),
 ("hide",0, []),
 ("unhide",0, []),
 ("neigh",sf_priority_5|sf_vol_6, ["horse_exterior_whinny_01.wav","horse_exterior_whinny_02.wav","horse_exterior_whinny_03.wav","horse_exterior_whinny_04.wav","horse_exterior_whinny_05.wav","horse_whinny.wav"]),
 ("gallop",sf_priority_8|sf_vol_3, ["horse_gallop_3.wav","horse_gallop_4.wav","horse_gallop_5.wav"]),
 ("battle",sf_vol_4, []),
 ("arrow_hit_body",sf_priority_5|sf_vol_7, ["body_hit_1.wav","body_hit_2.wav","body_hit_3.wav","impact_body2.wav","impact_body6.wav"]),
 ("metal_hit_low_armor_low_damage",sf_priority_5|sf_vol_7, ["sword_hit_lo_armor_lo_dmg_1.wav","sword_hit_lo_armor_lo_dmg_2.wav","sword_hit_lo_armor_lo_dmg_3.wav"]),
 ("metal_hit_low_armor_high_damage",sf_priority_5|sf_vol_7, ["sword_hit_lo_armor_hi_dmg_1.wav","sword_hit_lo_armor_hi_dmg_2.wav","impact_body1.wav","impact_body3.wav","impact_body4.wav","impact_body5.wav","sword_hit_lo_armor_hi_dmg_3.wav","sword_impact.wav"]),
 ("metal_hit_high_armor_low_damage",sf_priority_5|sf_vol_7, ["metal_hit_high_armor_low_damage.wav","metal_hit_high_armor_low_damage_2.wav","metal_hit_high_armor_low_damage_3.wav"]),
 ("metal_hit_high_armor_high_damage",sf_priority_5|sf_vol_7, ["sword_hit_hi_armor_hi_dmg_1.wav","sword_hit_hi_armor_hi_dmg_2.wav","impact_body1.wav","impact_body3.wav","impact_body4.wav","impact_body5.wav","sword_hit_hi_armor_hi_dmg_3.wav","sword_impact.wav"]),
 ("wooden_hit_low_armor_low_damage",sf_priority_5|sf_vol_7, ["blunt_hit_low_1.wav","blunt_hit_low_2.wav","blunt_hit_low_3.wav"]),
 ("wooden_hit_low_armor_high_damage",sf_priority_5|sf_vol_7, ["blunt_hit_high_1.wav","blunt_hit_high_2.wav","blunt_hit_high_3.wav"]),
 ("wooden_hit_high_armor_low_damage",sf_priority_5|sf_vol_7, ["wooden_hit_high_armor_low_damage_1.wav","wooden_hit_high_armor_low_damage_2.wav"]),
 ("wooden_hit_high_armor_high_damage",sf_priority_5|sf_vol_7, ["blunt_hit_high_1.wav","blunt_hit_high_2.wav","blunt_hit_high_3.wav"]),
 ("mp_arrow_hit_target",sf_2d|sf_priority_10|sf_vol_9, ["mp_arrow_hit_target.wav"]),
 ("blunt_hit",sf_priority_5|sf_vol_7, ["punch_1.wav","punch_3.wav","punch_4.wav","punch_5.wav"]),
 ("player_hit_by_arrow",sf_priority_5|sf_vol_7, ["body_hit_1.wav","body_hit_2.wav","body_hit_3.wav","impact_body2.wav","impact_body6.wav"]),
 ("pistol_shot",sf_priority_15|sf_vol_15, []),#"fl_pistol.wav"]),
 
 # hardcoded shit.
 ("release_crossbow_medium",sf_vol_15|sf_priority_13, []),
 ("release_crossbow_far",sf_vol_15|sf_priority_12, []),
 ("bullet_hit_body",sf_priority_5|sf_vol_7, ["body_hit_1.wav","body_hit_2.wav","body_hit_3.wav","impact_body2.wav","impact_body6.wav"]),
 ("player_hit_by_bullet",sf_priority_5|sf_vol_7, ["body_hit_1.wav","body_hit_2.wav","body_hit_3.wav","impact_body2.wav","impact_body6.wav"]),
 
 ("man_grunt",sf_priority_4|sf_vol_4, ["man_excercise_1.wav","man_excercise_2.wav","man_excercise_4.wav"]),
 ("man_breath_hard",sf_priority_3|sf_vol_7, ["man_ugh_1.wav","man_ugh_2.wav","man_ugh_4.wav","man_ugh_7.wav","man_ugh_12.wav","man_ugh_13.wav","man_ugh_17.wav"]),
 ("man_stun",sf_priority_3|sf_vol_8, ["man_stun_1.wav"]),
 #("man_grunt_long",sf_priority_5|sf_vol_7, ["man_grunt_1.wav","man_grunt_2.wav","man_grunt_3.wav","man_grunt_5.wav","man_grunt_13.wav","man_grunt_14.wav"]),
 
 ("man_grunt_long",sf_priority_5|sf_vol_7, [
   "man_grunt_1.wav","man_grunt_2.wav","man_grunt_3.wav","man_grunt_4.wav","man_grunt_5.wav"
  ,"man_grunt_6.wav","man_grunt_7.wav","man_grunt_8.wav","man_grunt_9.wav","man_grunt_10.wav"
  ,"man_grunt_11.wav","man_grunt_12.wav","man_grunt_13.wav","man_grunt_14.wav","man_grunt_15.wav"
  ,"man_grunt_16.wav","man_grunt_17.wav","man_grunt_18.wav","man_grunt_19.wav","man_grunt_20.wav"]),

 ("man_yell",sf_priority_7|sf_vol_8, []),
# "man_yell_4.wav","man_yell_4_2.wav","man_yell_7.wav","man_yell_9.wav","man_yell_11.wav","man_yell_13.wav","man_yell_15.wav","man_yell_16.wav","man_yell_17.wav","man_yell_20.wav",
# "man_shortyell_4.wav","man_shortyell_5.wav","man_shortyell_6.wav","man_shortyell_9.wav","man_shortyell_11.wav","man_shortyell_11b.wav",
#                        "man_yell_b_18.wav","man_yell_22.wav", "man_yell_c_20.wav"]),
## not adequate, removed: "man_yell_b_21.ogg","man_yell_b_22.ogg","man_yell_b_23.ogg"]),
#TODONOW:
 ("man_warcry",sf_priority_6, []),#"man_insult_2.ogg","man_insult_3.ogg","man_insult_7.ogg","man_insult_9.ogg","man_insult_13.ogg","man_insult_15.ogg","man_insult_16.ogg"]),

 ("horse_walk",sf_priority_6|sf_vol_5, ["horse_walk_1.wav","horse_walk_2.wav","horse_walk_3.wav","horse_walk_4.wav"]),
 ("horse_trot",sf_priority_7|sf_vol_6, ["horse_trot_1.wav","horse_trot_2.wav","horse_trot_3.wav","horse_trot_4.wav"]),
 ("horse_canter",sf_priority_8|sf_vol_7, ["horse_canter_1.wav","horse_canter_2.wav","horse_canter_3.wav","horse_canter_4.wav"]),
 ("horse_gallop",sf_priority_8|sf_vol_8, ["horse_gallop_6.wav","horse_gallop_7.wav","horse_gallop_8.wav","horse_gallop_9.wav"]),
 ("horse_breath",sf_priority_1|sf_vol_4, ["horse_breath_4.wav","horse_breath_5.wav","horse_breath_6.wav","horse_breath_7.wav"]),
 ("horse_snort",sf_priority_1|sf_vol_2, ["horse_snort_1.wav","horse_snort_2.wav","horse_snort_3.wav","horse_snort_4.wav","horse_snort_5.wav"]),
 ("horse_low_whinny",sf_vol_12, ["horse_whinny-1.wav","horse_whinny-2.wav"]),
 ("block_fist",sf_priority_3|sf_vol_5, ["block_fist_3.wav","block_fist_4.wav"]),
 ("man_hit_blunt_weak",sf_priority_5|sf_vol_7,[#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_hit_blunt_strong",sf_priority_5|sf_vol_7,[#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_hit_pierce_weak",sf_priority_5|sf_vol_7,[#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_hit_pierce_strong",sf_priority_5|sf_vol_7, [#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_hit_cut_weak",sf_priority_5|sf_vol_7, [#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_hit_cut_strong",sf_priority_5|sf_vol_7, [#"man_hit_5.wav","man_hit_6.wav","man_hit_7.wav","man_hit_8.wav","man_hit_9.wav","man_hit_10.wav","man_hit_11.wav","man_hit_12.wav","man_hit_13.wav","man_hit_14.wav","man_hit_15.wav","man_hit_17.wav","man_hit_18.wav","man_hit_19.wav","man_hit_22.wav","man_hit_29.wav","man_hit_32.wav","man_hit_57.wav","man_hit_47.wav"]),
 "man_pain_1.wav","man_pain_2.wav","man_pain_3.wav","man_pain_4.wav","man_pain_5.wav"
 ,"man_pain_6.wav","man_pain_7.wav","man_pain_8.wav","man_pain_9.wav","man_pain_10.wav"
 ,"man_pain_11.wav","man_pain_12.wav","man_pain_13.wav","man_pain_14.wav","man_pain_15.wav"
 ,"man_pain_16.wav","man_pain_17.wav","man_pain_18.wav","man_pain_19.wav","man_pain_20.wav"
 ,"man_pain_21.wav","man_pain_22.wav","man_pain_23.wav","man_pain_24.wav"
 ]),
 
 ("man_victory",sf_priority_8|sf_vol_13, [
   ["brit_huzzah1.wav", fac_britain],["brit_godsave2.wav", fac_britain],["brit_king2.wav", fac_britain],["brit_rule1.wav", fac_britain],["brit_nosey1.wav", fac_britain], 
   ["fren_empereur1.wav", fac_france],["fren_empereur3.wav", fac_france],["fren_vivala1.wav", fac_france],["fren_vibatrie1.wav", fac_france],["fren_alabataille1.wav", fac_france],
   ["prus_fuerkoenig1.wav", fac_prussia], ["prus_gottschuetze3.wav", fac_prussia], ["prus_fuervater2.wav", fac_prussia], ["prus_hurra1.wav", fac_prussia],["prus_schlagt2.wav", fac_prussia],
   ["rus_battlecry3.wav", fac_russia],["rus_battlecry9.wav", fac_russia],["rus_battlecry5.wav", fac_russia],["rus_battlecry8.wav", fac_russia],["rus_battlecry11.wav", fac_russia],
   ["aus_kaiser1.wav", fac_austria],  ["aus_gottschuetzekaiser1.wav", fac_austria], ["prus_fuervater2.wav", fac_austria], ["prus_hurra1.wav", fac_austria],["prus_schlagt2.wav", fac_austria],
   ["prus_fuerkoenig1.wav", fac_rhine], ["prus_gottschuetze3.wav", fac_rhine], ["prus_fuervater2.wav", fac_rhine], ["prus_hurra1.wav", fac_rhine],["prus_schlagt2.wav", fac_rhine],
   "man_victory_4.ogg","man_victory_5.ogg"]),
 ("fire_loop",sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.wav"]),
 ("torch_loop",sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.wav"]),
 ("dummy_hit",sf_priority_9, ["shield_hit_cut_3.wav","shield_hit_cut_5.wav"]),
 ("dummy_destroyed",sf_priority_9, ["shield_broken.ogg"]),
 ("gourd_destroyed",sf_priority_9, ["shield_broken.ogg"]),#TODO
 ("tutorial_fail", sf_2d|sf_vol_7,["cue_failure.ogg"]),
 ("your_flag_taken", sf_2d|sf_priority_15|sf_vol_8, ["your_flag_taken.ogg"]),
 ("enemy_flag_taken", sf_2d|sf_priority_15|sf_vol_8, ["enemy_flag_taken.ogg"]),
 ("flag_returned", sf_2d|sf_priority_15|sf_vol_8, ["your_flag_returned.ogg"]),
 ("team_scored_a_point", sf_2d|sf_priority_15|sf_vol_8, ["you_scored_a_point.ogg"]),
 ("enemy_scored_a_point", sf_2d|sf_priority_15|sf_vol_8, ["enemy_scored_a_point.ogg"]),

 ("woman_grunt",sf_priority_4|sf_vol_4, ["woman_exercise_1.wav","woman_exercise_2.wav","woman_exercise_3.wav","woman_exercise_4.wav","woman_exercise_5.wav","woman_exercise_6.wav","woman_exercise_7.wav","woman_exercise_8.wav"]),
 
 ("woman_victory",sf_priority_8|sf_vol_13, [
   ["brit_f_battlecry_1.wav", fac_britain],["brit_f_battlecry_2.wav", fac_britain],["brit_f_battlecry_3.wav", fac_britain],["brit_f_battlecry_4.wav", fac_britain],["brit_f_battlecry_5.wav", fac_britain], 
   ["french_f_battlecry_1.wav", fac_france],["french_f_battlecry_2.wav", fac_france],["french_f_battlecry_3.wav", fac_france],["french_f_battlecry_4.wav", fac_france],["french_f_battlecry_5.wav", fac_france],
   ["prus_f_battlecry_1.wav", fac_prussia], ["prus_f_battlecry_2.wav", fac_prussia], ["prus_f_battlecry_3.wav", fac_prussia], ["prus_f_battlecry_4.wav", fac_prussia],["prus_f_battlecry_5.wav", fac_prussia],
   ["rus_f_battlecry1.wav", fac_russia],["rus_f_battlecry2.wav", fac_russia],["rus_f_battlecry3.wav", fac_russia],["rus_f_battlecry4.wav", fac_russia],["rus_f_battlecry5.wav", fac_russia],
   ["aus_f_battlecry_1.wav", fac_austria], ["aus_f_battlecry_2.wav", fac_austria], ["aus_f_battlecry_3.wav", fac_austria], ["aus_f_battlecry_4.wav", fac_austria],
   ["prus_f_battlecry_1.wav", fac_rhine], ["prus_f_battlecry_2.wav", fac_rhine], ["prus_f_battlecry_3.wav", fac_rhine], ["prus_f_battlecry_4.wav", fac_rhine],["prus_f_battlecry_5.wav", fac_rhine]
   ]),
 

 ## MM Sounds 
 
 # Sound effects.
 ("musket", sf_priority_15|sf_vol_15,["musket2.wav","musket3.wav","musket4.wav","musket5.wav","musket_shot01.wav","musket_shot02.wav","musket_shot03.wav","musket_shot04.wav","musket_shot05.wav"]),
 ("rifle", sf_priority_15|sf_vol_15, ["rifle.wav"]),
 ("pistol", sf_priority_15|sf_vol_15,["musket1.wav"]),
 #("reload_pistol",sf_priority_1|sf_vol_2, ["reload_pistol.ogg"]),
 ("cannon", sf_priority_15|sf_vol_15, ["canon01.ogg","canon02.ogg","canon03.ogg","canon04.ogg","canon05.ogg","canon06.ogg"]),
 ("rocket_launch", sf_priority_15|sf_vol_15, ["rocket_launch.wav","rocket_launch2.wav","rocket_launch1.wav"]),
 ("cannon_hit", sf_priority_7|sf_vol_10, ["cannon_hit.ogg","cannon_hit2.ogg"]), 
 ("cannon_hit_ground",sf_priority_7|sf_vol_9, ["cannonhitground.ogg"]),
 ("cannon_hit_wall",sf_priority_10|sf_vol_15, ["walls_destroy1.ogg","walls_destroy2.ogg"]),
 ("cannon_hit_wood_wall",sf_priority_10|sf_vol_15, ["wallhit_wood.wav"]),
 ("cannon_fuse",sf_vol_3, ["fuse.ogg"]),
 ("cannon_ball",sf_vol_3, ["cannonball.ogg"]),
 ("explosion",sf_priority_15|sf_vol_15, ["shell1.ogg","shell2.ogg","shell3.ogg"]),
 ("holy_call",sf_priority_10|sf_vol_15, ["holy_grenade.ogg"]),
 ("admin_banhammer",sf_priority_15|sf_vol_15|sf_2d, ["admin_banhammer.ogg"]),
 ("admin_shotgun",sf_priority_15|sf_vol_15|sf_2d, ["admin_shotgun.ogg"]),
 ("admin_rocketlauncher",sf_priority_15|sf_vol_15|sf_2d, ["admin_rocketlauncher.ogg"]),
 ("glass_break",sf_priority_7|sf_vol_10, ["glass.ogg"]),
 ("flag_loop",sf_priority_7|sf_vol_8|sf_looping, ["flagloop.wav"]),
 ("thunder",sf_2d|sf_priority_15|sf_vol_15, ["thunder1.wav","thunder2.wav","thunder3.wav","thunder4.wav"]),
 ("crate_fuse",sf_priority_7|sf_vol_10, ["crate_fuse.wav"]),
 ("bandaging",sf_priority_7|sf_vol_10, ["bandaging1.ogg","bandaging1_1.ogg"]),
 ("church_bell",sf_priority_15|sf_vol_15, ["churchbells.wav"]),
 ("boat_sinking",sf_priority_7|sf_vol_13|sf_stream_from_hd, ["boat_sinking.ogg"]),

 # ball/rocket flight loop sounds.
 ("cannonball_loop",sf_priority_15|sf_vol_5|sf_looping, ["ball_loop.wav"]),
 ("rocket_loop",sf_priority_15|sf_vol_6|sf_looping, ["fuse.wav"]),

 ("hammer",sf_vol_7, ["hammer1.wav","hammer3.wav","hammer2.wav"]),
 ("shovel",sf_vol_7, ["shovel1.wav","shovel2.wav","shovel4.wav","shovel3.wav"]),
 ("ramrod",sf_vol_15, ["ramrod.ogg"]),

 ("door_open",sf_vol_5, ["door_open.ogg"]),
 ("door_close",sf_vol_5, ["door_close.ogg"]),
 ("door_lock",sf_vol_5, ["door_locked.ogg"]),

 ("underwater_noise",sf_2d|sf_priority_7|sf_vol_7|sf_looping, ["underwater.wav"]),
 ("drown",sf_priority_7|sf_vol_7, ["gurgle1.wav","gurgle2.wav","gurgle3.wav","gurgle4.wav","gurgle5.wav","gurgle6.wav","gurgle7.wav","gurgle8.wav","gurgle9.wav","gurgle10.wav"]),
 ("come_up",sf_priority_7|sf_vol_7, ["breathe1.wav","breathe2.wav","breathe3.wav"]),
 
 #Ambience #
 ("ambient_birds",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["bird1_notmany.wav"]),
 ("ambient_birds_many",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["birds1_many.wav"]),
 ("ambient_ocean",sf_vol_10|sf_priority_15|sf_looping|sf_start_at_random_pos, ["oceanwaves.wav"]),
 ("ambient_crickets_many",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["crickets_many.wav"]),
 ("ambient_crickets_few",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["crickets.wav"]),  
 ("ambient_river",sf_vol_11|sf_priority_15|sf_looping|sf_start_at_random_pos, ["river.wav"]),
 ("ambient_seagulls",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["seagulls.wav"]), 
 ("ambient_fly",sf_vol_6|sf_priority_8|sf_looping|sf_start_at_random_pos, ["fly.wav"]), 
 ("ambient_night",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["night_forest.wav"]), 
 ("ambient_roof",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["Rain_heavy_roof.wav"]),
 ("ambient_stone",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["Rain_heavy_stone.wav"]),
 ("ambient_windmill",sf_vol_6|sf_priority_15|sf_looping|sf_start_at_random_pos, ["windmill_fan.wav"]),

 #global ambients, new sound system.
 ("global_ambient_night",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["night.ogg"]), 
 ("global_ambient_beach",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["beach.ogg"]), 
 ("global_ambient_farmland",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["farmland_sound_new.ogg"]), 
 ("global_ambient_farmland_evening",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["farmland_sound_new_evening.ogg"]), 
 ("global_ambient_farmland_empty",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["empty_farmland.ogg"]), 
 ("global_ambient_city_empty",sf_2d|sf_vol_10|sf_priority_15|sf_looping|sf_stream_from_hd, ["empty_city.ogg"]), 

 ("ambient_buzzard",sf_vol_15|sf_priority_15, ["buzzard.wav"]),
 ("ambient_crow",sf_vol_15|sf_priority_15, ["crow.wav"]),
 
 # Win/loose sounds.
 ("win_tune_brit", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win.ogg"]),
 ("win_tune_fren", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win1.ogg"]),
 ("win_tune_prus", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win2.ogg"]),
 ("win_tune_russ", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win4.ogg"]),
 ("win_tune_aust", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win2.ogg"]),
 ("win_tune_rhen", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["win2.ogg"]),
 
 ("loose_tune_brit", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose.ogg"]),
 ("loose_tune_fren", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose1.ogg"]),
 ("loose_tune_prus", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose.ogg"]),
 ("loose_tune_russ", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose1.ogg"]),
 ("loose_tune_aust", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose.ogg"]),
 ("loose_tune_rhen", sf_2d|sf_priority_15|sf_vol_8|sf_stream_from_hd, ["loose.ogg"]),
 
  # battle cries.
 ("voice_cry_brit", sf_priority_8|sf_vol_13, [
    "brit_huzzah1.wav" # Huzzah!
   ,"brit_huzzah2.wav"
   ,"brit_godsave1.wav" # God save the king!
   ,"brit_godsave2.wav"
   ,"brit_rule1.wav" # Rule Britannia
   ,"brit_rule2.wav"
   ,"brit_nosey1.wav" # Hurrah for old nosey
   ,"brit_nosey2.wav"
   ,"brit_king1.wav" # For king and country
   ,"brit_king2.wav" 
 ]), 
 ("voice_cry_fren", sf_priority_8|sf_vol_13, [
    "fren_empereur1.wav" # Vive lEmpereur!
   ,"fren_empereur2.wav"
   ,"fren_empereur3.wav" 
   ,"fren_enavant1.wav" # En avant!
   ,"fren_enavant2.wav"
   ,"fren_vivala1.wav" # Vive la France!
   ,"fren_vivala2.wav"
   ,"fren_alatacke1.wav" # a lattaque
   ,"fren_alatacke2.wav" 
   ,"fren_alabataille1.wav" # a la bataille
   ,"fren_alabataille2.wav"
   ,"fren_vibatrie1.wav" # Vive la patrie
   ,"fren_vibatrie2.wav"
   ,"fren_ecrazes1.wav" # Ecrasez les
   ,"fren_onvaleur1.wav" # Ecrasez les
 ]),
 ("voice_cry_prus", sf_priority_8|sf_vol_13, [
    "prus_fuerkoenig1.wav" # Fur Konig und Vaterland !
   ,"prus_fuerkoenig2.wav"
   ,"prus_gottschuetze1.wav" # Gott schutze den Konig !
   ,"prus_gottschuetze2.wav"
   ,"prus_gottschuetze3.wav"
   ,"prus_fuervater1.wav" # Fur das Vaterland !
   ,"prus_fuervater2.wav"
   ,"prus_fuervater3.wav"
   ,"prus_fuervater4.wav" 
   ,"prus_schlagt1.wav" # Schlagt sie !
   ,"prus_schlagt2.wav"
   ,"prus_hurra1.wav"	# Hurra !
   ,"prus_hurra2.wav"
   ,"prus_hurra3.wav"
   ,"prus_hurra4.wav"
   ,"prus_aufgehts1.wav" # Auf gehts Kameraden !
   ,"prus_aufgehts2.wav"
 ]),
 ("voice_cry_russ", sf_priority_8|sf_vol_13, [
    "rus_battlecry1.wav"
   ,"rus_battlecry2.wav"
   ,"rus_battlecry3.wav"
   ,"rus_battlecry4.wav"
   ,"rus_battlecry5.wav"
   ,"rus_battlecry6.wav"
   ,"rus_battlecry7.wav"
   ,"rus_battlecry8.wav"
   ,"rus_battlecry9.wav"
   ,"rus_battlecry10.wav"
   ,"rus_battlecry11.wav"
   ,"rus_battlecry12.wav"
   ,"rus_battlecry13.wav"
 ]),
 ("voice_cry_aust", sf_priority_8|sf_vol_13, [
    "aus_kaiser1.wav"	# Fur den Kaiser !
   ,"aus_kaiser2.wav"
   ,"aus_kaiser3.wav"
   ,"aus_gottschuetzekaiser1.wav" # Gott schutze den Kaiser !
   ,"aus_gottschuetzekaiser2.wav"
   ,"aus_gottschuetzekaiser3.wav"
   ,"aus_gottschuetzekaiser4.wav" 
   ,"prus_schlagt1.wav" # Schlagt sie !
   ,"prus_schlagt2.wav"
   ,"prus_hurra1.wav"	# Hurra !
   ,"prus_hurra2.wav"
   ,"prus_hurra3.wav"
   ,"prus_hurra4.wav"
   ,"prus_aufgehts1.wav" # Auf gehts Kameraden !
   ,"prus_aufgehts2.wav"
 ]),
 ("voice_cry_brit_scot", sf_priority_8|sf_vol_13, [
    "brit_bastard1.wav" # Come on yer bastards
   ,"brit_bastard2.wav"
   ,"brit_scotland1.wav" # Scotland Ferever
   ,"brit_scotland2.wav" 
   ,"brit_sonsof1.wav" # Sons of the hounds, come here and get flesh
   ,"brit_sonsof2.wav"
   ,"brit_bydand1.wav" # Bydand
   ,"brit_bydand2.wav"
 ]),
 ("voice_cry_russ_ukr", sf_priority_8|sf_vol_13, [
    "ukr_battlecry1.wav" 
   ,"ukr_battlecry2.wav"
   ,"ukr_battlecry3.wav"
   ,"rus_battlecry3.wav"
   ,"rus_battlecry10.wav"
   ,"rus_battlecry11.wav"
   ,"rus_battlecry12.wav"
 ]),
 ("voice_cry_rhen", sf_priority_8|sf_vol_13, [
    "prus_fuervater1.wav" # Fur das Vaterland !
   ,"prus_fuervater2.wav"
   ,"prus_fuervater3.wav"
   ,"prus_fuervater4.wav" 
   ,"prus_schlagt1.wav" # Schlagt sie !
   ,"prus_schlagt2.wav"
   ,"prus_hurra1.wav"	# Hurra !
   ,"prus_hurra2.wav"
   ,"prus_hurra3.wav"
   ,"prus_hurra4.wav"
   ,"prus_aufgehts1.wav" # Auf gehts Kameraden !
   ,"prus_aufgehts2.wav"
 ]),
 
 ("voice_cry_pirate", sf_priority_8|sf_vol_13, [
    "pirate_1.wav"
   ,"pirate_2.wav"
   ,"pirate_3.wav"
   ,"pirate_4.wav"
   ,"pirate_5.wav"
   ,"pirate_6.wav"
   ,"pirate_7.wav"
   ,"pirate_8.wav"
   ,"pirate_9.wav"
   ,"pirate_10.wav"
   ,"pirate_11.wav"
   ,"pirate_12.wav"
   ,"pirate_13.wav"
   ,"pirate_14.wav"
 ]), 
 
 
 # Surrendering
 ("voice_surrender_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, [
    "brit_surr1.wav" # I surrender!
   ,"brit_surr2.wav"
   ,"brit_surr3.wav"
   ,"brit_dont1.wav" # Dont shoot me!
   ,"brit_dont2.wav"
   ,"brit_dont3.wav"
   ,"brit_spare1.wav" # Spare me!
   ,"brit_spare2.wav"
 ]),
 ("voice_surrender_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, [
    "fren_jemerend1.wav" # Je me rend !
   ,"fren_onserend1.wav" # On se rend
   ,"fren_legarde1.wav" # La Garde meurt mais ne se rent pas!
   # Rendez vous
   ,"fren_netirez1.wav" # Ne tirez pas !
   ,"fren_savquie1.wav" # Sauve qui peut
 ]),
 ("voice_surrender_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, [
    "prus_ichergebe1.wav" # Ich ergebe mich !
   ,"prus_ichergebe2.wav"
   ,"prus_ichergebe3.wav"
   ,"prus_ichgebe1.wav" # Ich gebe auf !
   ,"prus_nichtschiessen1.wav" # Nicht schiessen !
   ,"prus_nichtschiessen2.wav"
 ]),
 ("voice_surrender_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, [
    "rus_surrender1.wav"
   ,"rus_surrender2.wav"
   ,"rus_surrender3.wav"
   ,"rus_surrender4.wav"
   ,"rus_surrender5.wav"
   ,"rus_surrender6.wav"
   ,"rus_surrender7.wav"
   ,"rus_surrender8.wav"
 ]),
  ("voice_surrender_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, [
    "ukr_surrender1.wav"
   ,"ukr_surrender2.wav"
   ,"ukr_surrender3.wav"
   ,"ukr_surrender4.wav"
 ]),
 
 # # Officer commands # #
 
 # Make Ready
 ("voice_comm_ready_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_ready1.wav","brit_ready2.wav","brit_ready3.wav"]),
 ("voice_comm_ready_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_armes1.wav","fren_armes2.wav","fren_armes3.wav"]),
 ("voice_comm_ready_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_bereit1.wav","prus_bereit2.wav","prus_bereit3.wav","prus_bereit4.wav","prus_bereit5.wav"]),
 ("voice_comm_ready_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_ready1.wav","rus_ready2.wav","rus_ready3.wav"]),
 ("voice_comm_ready_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_ready1.wav","ukr_ready2.wav"]),
 
 # Present
 ("voice_comm_present_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_pres1.wav","brit_pres2.wav","brit_pres3.wav","brit_pres4.wav","brit_pres5.wav"]),
 ("voice_comm_present_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_enjou1.wav","fren_enjou2.wav","fren_enjou3.wav"]),
 ("voice_comm_present_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_anlegen1.wav","prus_anlegen2.wav","prus_anlegen3.wav","prus_anlegen4.wav"]),
 ("voice_comm_present_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_present1.wav","rus_present2.wav"]),
 ("voice_comm_present_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_present1.wav","ukr_present2.wav"]),
 
 # Fire
 ("voice_comm_fire_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_fire1.wav","brit_fire2.wav","brit_fire3.wav","brit_fire4.wav"]),
 ("voice_comm_fire_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_feau1.wav","fren_feau2.wav","fren_feau3.wav"]),
 ("voice_comm_fire_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_feuer1.wav","prus_feuer2.wav","prus_feuer3.wav"]),
 ("voice_comm_fire_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_fire1.wav","rus_fire2.wav","rus_fire3.wav"]),
 ("voice_comm_fire_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_fire1.wav","ukr_fire2.wav"]),
 
 # Charge
 ("voice_comm_charge_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_charge1.wav","brit_charge2.wav","brit_charge3.wav"]),
 ("voice_comm_charge_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_charge1.wav","fren_bayonet1.wav","fren_bayonet2.wav","fren_bayonet3.wav","fren_bayonet4.wav"]),
 ("voice_comm_charge_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_nahkampfangriff1.wav","prus_angriff1.wav","prus_angriff2.wav","prus_attacke1.wav","prus_attacke2.wav","prus_attacke3.wav","prus_inden1.wav","prus_inden2.wav","prus_inden3.wav"]),
 ("voice_comm_charge_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_charge1.wav","rus_charge2.wav","rus_charge3.wav","rus_charge4.wav"]),
 ("voice_comm_charge_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_charge1.wav","rus_charge2.wav","rus_charge3.wav","rus_charge4.wav"]),
 
 # Company, advance!
 ("voice_comm_advance_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_advance1.wav","brit_advance2.wav","brit_advance3.wav","brit_advance4.wav","brit_advance5.wav","brit_advance6.wav"]),
 ("voice_comm_advance_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_avance1.wav","fren_march1.wav","fren_enaveant1.wav","fren_compagnie1.wav"]),
 ("voice_comm_advance_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_kompanie1.wav","prus_kompanie2.wav","prus_kompanie3.wav","prus_vorruecken1.wav","prus_vorruecken2.wav"]),
 ("voice_comm_advance_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_advance1.wav","rus_advance2.wav","rus_advance3.wav","rus_advance4.wav","rus_advance5.wav"]),
 ("voice_comm_advance_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_onme1.wav","ukr_onme2.wav"]),
 
 # Hold this position!
 ("voice_comm_hold_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_hold1.wav","brit_hold2.wav","brit_hold3.wav","brit_hold4.wav","brit_hold5.wav"]),
 ("voice_comm_hold_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_tenezcette1.wav","fren_tenezlapos1.wav","fren_defendez1.wav"]),
 ("voice_comm_hold_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_dieposition1.wav","prus_dieposition2.wav","prus_haltet1.wav","prus_haltet2.wav","prus_haltet3.wav","prus_verteidigt1.wav","prus_verteidigt2.wav","prus_verteidigt3.wav","prus_verteidigt4.wav"]),
 ("voice_comm_hold_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_holdpos1.wav","rus_holdpos2.wav","rus_holdpos3.wav"]),
 ("voice_comm_hold_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_holdpos1.wav","ukr_holdpos2.wav","ukr_holdpos3.wav"]),
 
 # Fire at will!
 ("voice_comm_fire_at_will_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_fireatwill1.wav","brit_fireatwill2.wav","brit_fireatwill3.wav"]),
 ("voice_comm_fire_at_will_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_volon1.wav","fren_volon2.wav"]),
 ("voice_comm_fire_at_will_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_feuernach1.wav","prus_feuernach2.wav","prus_feuernach3.wav","prus_feuerfrei1.wav","prus_feuerfrei2.wav","prus_feuerfrei3.wav"]),
 ("voice_comm_fire_at_will_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_fireatwill1.wav","rus_fireatwill2.wav"]),
 ("voice_comm_fire_at_will_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_fireatwill1.wav"]),
 
 # Company, on me! 
 ("voice_comm_on_me_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_onme1.wav","brit_onme2.wav","brit_onme3.wav","brit_onme4.wav"]),
 ("voice_comm_on_me_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_avec1.wav","fren_avec2.wav","fren_avec3.wav","fren_avec4.wav","fren_avec5.wav"]),
 ("voice_comm_on_me_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_zumir1.wav","prus_zumir2.wav","prus_zumir3.wav"]),
 ("voice_comm_on_me_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_onme1.wav","rus_onme2.wav","rus_onme3.wav"]),
 ("voice_comm_on_me_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_onme1.wav","ukr_onme2.wav","ukr_onme3.wav","ukr_onme4.wav"]),
 
 # Fall back!
 ("voice_comm_fall_back_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_fallback1.wav","brit_fallback2.wav","brit_fallback3.wav"]),
 ("voice_comm_fall_back_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["fren_ret1.wav","fren_ret2.wav","fren_ret3.wav"]),
 ("voice_comm_fall_back_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_zurueck1.wav","prus_zurueck2.wav"]),
 ("voice_comm_fall_back_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_all_retreat1.wav","rus_retreat1.wav","rus_fallback1.wav"]),
 ("voice_comm_fall_back_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_all_retreat1.wav","ukr_retreat1.wav","ukr_fallback1.wav"]),
 
 
 
 # Female voices.
 
  # battle cries.
 ("voice_cry_fem_brit", sf_priority_8|sf_vol_13, [
   "brit_f_battlecry_1.wav"
  ,"brit_f_battlecry_2.wav"
  ,"brit_f_battlecry_3.wav"
  ,"brit_f_battlecry_4.wav"
  ,"brit_f_battlecry_5.wav"
  ,"brit_f_battlecry_6.wav"
  ,"brit_f_battlecry_7.wav"
  ,"brit_f_battlecry_8.wav"
  ,"brit_f_battlecry_9.wav"
  ,"brit_f_battlecry_10.wav"
  ,"brit_f_battlecry_11.wav"
  ,"brit_f_battlecry_12.wav"
  ,"brit_f_battlecry_13.wav"
  ,"brit_f_battlecry_14.wav"
 ]), 
 ("voice_cry_fem_fren", sf_priority_8|sf_vol_13, [
   "french_f_battlecry_1.wav"
  ,"french_f_battlecry_2.wav"
  ,"french_f_battlecry_3.wav"
  ,"french_f_battlecry_4.wav"
  ,"french_f_battlecry_5.wav"
  ,"french_f_battlecry_6.wav"
  ,"french_f_battlecry_7.wav"
  ,"french_f_battlecry_8.wav"
  ,"french_f_battlecry_9.wav"
  ,"french_f_battlecry_10.wav"
  ,"french_f_battlecry_11.wav"
  ,"french_f_battlecry_12.wav"
  ,"french_f_battlecry_13.wav"
  ,"french_f_battlecry_14.wav"
  ,"french_f_battlecry_15.wav"
  ,"french_f_battlecry_16.wav"
  ,"french_f_battlecry_17.wav"
  ,"french_f_battlecry_18.wav"
  ,"french_f_battlecry_19.wav"
  ,"french_f_battlecry_20.wav"
 ]),
 ("voice_cry_fem_prus", sf_priority_8|sf_vol_13, [
   "prus_f_battlecry_1.wav"
  ,"prus_f_battlecry_2.wav"
  ,"prus_f_battlecry_3.wav"
  ,"prus_f_battlecry_4.wav"
  ,"prus_f_battlecry_5.wav"
  ,"prus_f_battlecry_6.wav"
  ,"prus_f_battlecry_7.wav"
  ,"prus_f_battlecry_8.wav"
  ,"prus_f_battlecry_9.wav"
  ,"prus_f_battlecry_10.wav"
 ]),
 ("voice_cry_fem_russ", sf_priority_8|sf_vol_13, [
   "rus_f_battlecry1.wav"
  ,"rus_f_battlecry2.wav"
  ,"rus_f_battlecry3.wav"
  ,"rus_f_battlecry4.wav"
  ,"rus_f_battlecry5.wav"
  ,"rus_f_battlecry6.wav"
  ,"rus_f_battlecry7.wav"
  ,"rus_f_battlecry8.wav"
  ,"rus_f_battlecry9.wav"
 ]),
 ("voice_cry_fem_aust", sf_priority_8|sf_vol_13, [
   "aus_f_battlecry_1.wav"
  ,"aus_f_battlecry_2.wav"
  ,"aus_f_battlecry_3.wav"
  ,"aus_f_battlecry_4.wav"
  ,"prus_f_battlecry_4.wav"
  ,"prus_f_battlecry_5.wav"
  ,"prus_f_battlecry_6.wav"
  ,"prus_f_battlecry_8.wav"
  ,"prus_f_battlecry_9.wav"
  ,"prus_f_battlecry_10.wav"
 ]),
 ("voice_cry_fem_russ_ukr", sf_priority_8|sf_vol_13, [
   "ukr_f_battlecry_1.wav"
  ,"ukr_f_battlecry_2.wav"
  ,"rus_f_battlecry1.wav"
  ,"rus_f_battlecry2.wav"
 ]),
 ("voice_cry_fem_rhen", sf_priority_8|sf_vol_13, [
  "prus_f_battlecry_4.wav"
  ,"prus_f_battlecry_5.wav"
  ,"prus_f_battlecry_6.wav"
  ,"prus_f_battlecry_8.wav"
  ,"prus_f_battlecry_9.wav"
  ,"prus_f_battlecry_10.wav"
 ]),
 
 # Surrendering
 ("voice_surrender_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_surrender_1.wav","brit_f_surrender_2.wav","brit_f_surrender_3.wav","brit_f_surrender_4.wav","brit_f_surrender_5.wav"]),
 ("voice_surrender_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_surrender_1.wav","french_f_surrender_2.wav","french_f_surrender_3.wav","french_f_surrender_4.wav"]),
 ("voice_surrender_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_surrender_1.wav","prus_f_surrender_2.wav","prus_f_surrender_3.wav"]),
 ("voice_surrender_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_surrender1.wav","rus_f_surrender2.wav","rus_f_surrender3.wav","rus_f_surrender4.wav","rus_f_surrender5.wav","rus_f_surrender6.wav","rus_f_surrender7.wav","rus_f_surrender8.wav"]),
 ("voice_surrender_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_surrender_1.wav","ukr_f_surrender_2.wav","ukr_f_surrender_3.wav","ukr_f_surrender_4.wav","ukr_f_surrender_5.wav","ukr_f_surrender_6.wav"]),
 
 # # Officer commands # #
 
 # Make Ready
 ("voice_comm_ready_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_ready_1.wav","brit_f_ready_2.wav","brit_f_ready_3.wav"]),
 ("voice_comm_ready_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_ready_1.wav","french_f_ready_2.wav","french_f_ready_3.wav","french_f_ready_5.wav"]),
 ("voice_comm_ready_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_ready_1.wav","prus_f_ready_2.wav"]),
 ("voice_comm_ready_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_ready1.wav","rus_f_ready2.wav","rus_f_ready3.wav"]),
 ("voice_comm_ready_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_ready_1.wav","ukr_f_ready_2.wav","ukr_f_ready_3.wav"]),
 
 # Present
 ("voice_comm_present_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_present_1.wav","brit_f_present_2.wav"]),
 ("voice_comm_present_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_present_1.wav","french_f_present_2.wav","french_f_present_3.wav"]),
 ("voice_comm_present_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_present_1.wav","prus_f_present_2.wav"]),
 ("voice_comm_present_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_present1.wav","rus_f_present2.wav"]),
 ("voice_comm_present_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_present_1.wav","ukr_f_present_2.wav"]),
 
 # Fire
 ("voice_comm_fire_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_fire_1.wav","brit_f_fire_2.wav","brit_f_fire_3.wav","brit_f_fire_4.wav"]),
 ("voice_comm_fire_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_fire_1.wav","french_f_fire_2.wav","french_f_fire_3.wav","french_f_fire_4.wav"]),
 ("voice_comm_fire_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_fire_1.wav","prus_f_fire_2.wav"]),
 ("voice_comm_fire_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_fire1.wav","rus_f_fire2.wav"]),
 ("voice_comm_fire_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_fire_1.wav","ukr_f_fire_2.wav"]),
 
 # Charge
 ("voice_comm_charge_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_charge_1.wav","brit_f_charge_2.wav","brit_f_charge_3.wav","brit_f_charge_4.wav"]),
 ("voice_comm_charge_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_charge_1.wav","french_f_charge_2.wav","french_f_charge_3.wav","french_f_charge_4.wav","french_f_charge_5.wav","french_f_charge_6.wav"]),
 ("voice_comm_charge_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_charge_1.wav","prus_f_charge_2.wav","prus_f_charge_3.wav","prus_f_charge_4.wav","prus_f_charge_5.wav"]),
 ("voice_comm_charge_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_charge1.wav","rus_f_charge2.wav","rus_f_charge3.wav","rus_f_charge4.wav","rus_f_charge5.wav","rus_f_charge6.wav","rus_f_charge7.wav"]),
 ("voice_comm_charge_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_charge5.wav"]),
 
 # Company, advance!
 ("voice_comm_advance_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_advance_1.wav","brit_f_advance_2.wav","brit_f_advance_3.wav","brit_f_advance_4.wav","brit_f_advance_5.wav","brit_f_advance_6.wav","brit_f_advance_7.wav","brit_f_advance_8.wav","brit_f_advance_9.wav"]),
 ("voice_comm_advance_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_advance_1.wav","french_f_advance_2.wav","french_f_advance_3.wav","french_f_advance_4.wav","french_f_advance_5.wav","french_f_advance_6.wav"]),
 ("voice_comm_advance_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_advance_1.wav","prus_f_advance_2.wav","prus_f_advance_3.wav"]),
 ("voice_comm_advance_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_advance1.wav","rus_f_advance2.wav","rus_f_advance3.wav","rus_f_advance4.wav"]),
 ("voice_comm_advance_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_advance_1.wav","ukr_f_advance_2.wav","ukr_f_advance_3.wav","ukr_f_advance_4.wav","rus_f_advance1.wav","rus_f_advance2.wav"]),
 
 # Hold this position!
 ("voice_comm_hold_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_holdpos_1.wav","brit_f_holdpos_2.wav","brit_f_holdpos_3.wav","brit_f_holdpos_4.wav","brit_f_holdpos_5.wav","brit_f_holdpos_6.wav"]),
 ("voice_comm_hold_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_holdpos_1.wav","french_f_holdpos_2.wav","french_f_holdpos_3.wav","french_f_holdpos_4.wav"]),
 ("voice_comm_hold_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_holdpos_1.wav","prus_f_holdpos_2.wav","prus_f_holdpos_3.wav"]),
 ("voice_comm_hold_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_holdpos1.wav","rus_f_holdpos2.wav"]),
 ("voice_comm_hold_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_holdpos_1.wav","ukr_f_holdpos_2.wav"]),
 
 # Fire at will!
 ("voice_comm_fire_at_will_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_fireatwill_1.wav","brit_f_fireatwill_2.wav","brit_f_fireatwill_3.wav","brit_f_fireatwill_4.wav","brit_f_fireatwill_5.wav","brit_f_fireatwill_6.wav"]),
 ("voice_comm_fire_at_will_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_fireatwill_1.wav","french_f_fireatwill_2.wav","french_f_fireatwill_3.wav"]),
 ("voice_comm_fire_at_will_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_fireatwill_1.wav","prus_f_fireatwill_2.wav","prus_f_fireatwill_3.wav"]),
 ("voice_comm_fire_at_will_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_fireatwill1.wav","rus_f_fireatwill2.wav"]),
 ("voice_comm_fire_at_will_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_fireatwill_1.wav","ukr_f_fireatwill_2.wav"]),
 
 # Company, on me! 
 ("voice_comm_on_me_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_onme_1.wav","brit_f_onme_2.wav","brit_f_onme_3.wav"]),
 ("voice_comm_on_me_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_onme_1.wav","french_f_onme_2.wav","french_f_onme_3.wav","french_f_onme_4.wav","french_f_onme_5.wav","french_f_onme_6.wav","french_f_onme_7.wav","french_f_onme_8.wav"]),
 ("voice_comm_on_me_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_onme_1.wav","prus_f_onme_2.wav"]),
 ("voice_comm_on_me_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_onme1.wav","rus_f_onme2.wav"]),
 ("voice_comm_on_me_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_onme_1.wav","ukr_f_onme_2.wav"]),
 
 # Fall back!
 ("voice_comm_fall_back_fem_brit", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["brit_f_fallback_1.wav","brit_f_fallback_2.wav","brit_f_fallback_3.wav"]),
 ("voice_comm_fall_back_fem_fren", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["french_f_fallback_1.wav","french_f_fallback_2.wav","french_f_fallback_3.wav","french_f_fallback_4.wav","french_f_fallback_5.wav","french_f_fallback_6.wav"]),
 ("voice_comm_fall_back_fem_prus", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["prus_f_retreat_1.wav","prus_f_retreat_2.wav"]),
 ("voice_comm_fall_back_fem_russ", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["rus_f_retreat1.wav","rus_f_retreat2.wav","rus_f_retreat3.wav","rus_f_retreat4.wav"]),
 ("voice_comm_fall_back_fem_ukra", sf_priority_8|sf_vol_13|sf_stream_from_hd, ["ukr_f_retreat_1.wav","ukr_f_retreat_2.wav","ukr_f_retreat_3.wav","ukr_f_retreat_4.wav","ukr_f_retreat_5.wav","ukr_f_retreat_6.wav"]),
 
 
 # Muscician sounds
 #DRUM
 #British
 ("drum_britain_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["brit_britishgrenadiers.ogg"]),
 ("drum_britain_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["brit_girlileftbehindme.ogg"]),
 ("drum_britain_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["brit_lili.ogg"]),
 ("drum_britain_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["brit_menofharlech.ogg"]),
 ("drum_britain_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["brit_rulebritannia.ogg"]),
 #French
 ("drum_france_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_drum_aux_champs.ogg"]),
 ("drum_france_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["fren_lacharge.ogg"]),
 ("drum_france_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["fren_diane.ogg"]),
 ("drum_france_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["fren_grenadiere.ogg"]),
 ("drum_france_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["fren_lapascadence.ogg"]),
 #Prussian
 ("drum_prussia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prus_yorkscher.ogg"]),
# ("drum_prussia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prus_dessauer.ogg"]),
 ("drum_prussia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_drum_hohenfriedberger.ogg"]),
 ("drum_prussia_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_drum_lockmarsch.ogg"]),
 ("drum_prussia_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_drum_parademarsch.ogg"]),
 ("drum_prussia_6",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_drum_praesentiermarsch.ogg"]),
 #Russian
("drum_russia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_drum_grenadiers.ogg"]),
("drum_russia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_drum_izmailovsky.ogg"]),
("drum_russia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_drum_march_of_attacking.ogg"]),
("drum_russia_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_drum_preabrazhensky.ogg"]),
("drum_russia_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_drum_semenovsky.ogg"]),
 #Austrian
("drum_austria_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_drum_grenadiersmarsch.ogg"]),
("drum_austria_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_drum_koburg.ogg"]),
("drum_austria_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_drum_pappenheimer.ogg"]),
("drum_austria_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_drum_pariser_einzugsmarsch.ogg"]),
("drum_austria_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_drum_prinz_von_eugen.ogg"]),
 #Highland
("drum_highland_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_drum_blue_bonnets.ogg"]),
("drum_highland_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_drum_bonnie_dundee.ogg"]),
 #Signals
("drum_signal_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["drum_signal_camp_taps.ogg"]),
("drum_signal_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["drum_signal_cease_fire.ogg"]),
("drum_signal_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["drum_signal_drummers_call.ogg"]),
 
 #FIFE
 #British
 ("fife_britain_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_fife_british_grenadiers.ogg"]),
 ("fife_britain_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_fife_girl_i_left_behind.ogg"]),
 ("fife_britain_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_fife_lilliburlero.ogg"]),
 ("fife_britain_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_fife_men_of_harlech.ogg"]),
 ("fife_britain_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_fife_rule_brit.ogg"]),
 #French
 ("fife_france_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_fife_aux_champs.ogg"]),
 ("fife_france_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_fife_la_charge.ogg"]),
 ("fife_france_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_fife_la_diane.ogg"]),
 ("fife_france_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_fife_la_grenadiere.ogg"]),
 ("fife_france_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["french_fife_la_pa_cadence.ogg"]),
 #Prussian
 ("fife_prussia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_fife_yorckscher.ogg"]), 
 ("fife_prussia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_fife_hohenfriedeberger.ogg"]),
 ("fife_prussia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_fife_lockmarsch.ogg"]),
 ("fife_prussia_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_fife_parademarsch_der_spielleute.ogg"]),
 ("fife_prussia_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["prussian_fife_praesentiermarsch.ogg"]),
 #Russian
 ("fife_russia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_fife_grenadiers_march.ogg"]),
 ("fife_russia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_fife_izmailovsky.ogg"]),
 ("fife_russia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_fife_of_attacking.ogg"]),
 ("fife_russia_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_fife_preobrazhensky.ogg"]),
 ("fife_russia_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["russian_fife_semenovsky.ogg"]),
 #Austrian
 ("fife_austria_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_fife_grenadiermarsch.ogg"]),
 ("fife_austria_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_fife_derkoburger.ogg"]),
 ("fife_austria_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_fife_pappenheimer.ogg"]),
 ("fife_austria_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_fife_pariser.ogg"]),
 ("fife_austria_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["austrian_fife_prinzeugen.ogg"]),

 #BUGLE
 #British
 ("bugle_britain_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_british_boots.ogg"]),
 ("bugle_britain_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["british_light_inf.ogg"]),
 #French
 ("bugle_france_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_french_danslehussards.ogg"]),
 ("bugle_france_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_french_lamarche.ogg"]),
 #Prussian
 ("bugle_prussia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_prussian_althessischer.ogg"]),
 ("bugle_prussia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_prussian_fehrbell.ogg"]),
 ("bugle_prussia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_prussian_freiwilligen.ogg"]),
 #Russian
 ("bugle_russia_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_russian_marchartillery.ogg"]),
 ("bugle_russia_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_russian_jaegers.ogg"]),
 ("bugle_russia_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_russian_musketeers.ogg"]),
 #Austrian
 ("bugle_austria_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_austrian_leban.ogg"]),
 ("bugle_austria_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_austrian_strauch.ogg"]),
 #Signals
 ("bugle_signal_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_call_assamble.ogg"]),
 ("bugle_signal_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_call_extend.ogg"]),
 ("bugle_signal_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_call_closeranks.ogg"]),
 ("bugle_signal_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_call_ondiscenemy.ogg"]),
 ("bugle_signal_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bugle_call_fire.ogg"]),

 #BAGPIPES
 #Highland
 ("bagpipes_britain_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bluebonnets.ogg"]),
 ("bagpipes_britain_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bonniedundee.ogg"]),
 #Additional...
 ("bagpipes_extra_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["blackbear.ogg"]),
 ("bagpipes_extra_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["amazing.ogg"]),
 ("bagpipes_extra_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["balmoral.ogg"]),
 ("bagpipes_extra_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["bonniedundee.ogg"]),
 ("bagpipes_extra_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["cockothenorth.ogg"]),
 ("bagpipes_extra_6",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["highlandcathedral.ogg"]),
 ("bagpipes_extra_7",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["myhome.ogg"]),
 ("bagpipes_extra_8",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["scotlandthebrave.ogg"]),
 ("bagpipes_extra_9",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["skyeboatsong.ogg"]),

 #PIANO
 ("piano_loop_1",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_beethoven_fur_elise.ogg"]),
 ("piano_loop_2",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_beethoven_ecossaise.ogg"]),
 ("piano_loop_3",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_erik_satie_gymnopedie_3.ogg"]),
 ("piano_loop_4",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_beethoven_laendler.ogg"]),
 ("piano_loop_5",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_lift_motif.ogg"]),
 ("piano_loop_6",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_bach_prelude.ogg"]),
 ("piano_loop_7",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_wagner_bridal_chorus.ogg"]),
 ("piano_loop_8",sf_priority_15|sf_vol_12|sf_stream_from_hd|sf_always_send_via_network, ["piano_schubert_ave_maria.ogg"]),
 
 #ORGAN
 ("organ_loop_1",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_bach_toccata_and_fugue.ogg"]),
 ("organ_loop_2",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_bach_toccata_and_fugue_2.ogg"]),
 ("organ_loop_3",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_bach_prelude_and_fugue.ogg"]),
 ("organ_loop_4",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_buxtehude_prelude.ogg"]),
 ("organ_loop_5",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_tiny_fugue.ogg"]),
 ("organ_loop_6",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_wagner_bridal_chorus.ogg"]),
 ("organ_loop_7",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_bach_chromatic_fuge.ogg"]),
 ("organ_loop_8",sf_priority_15|sf_vol_15|sf_stream_from_hd|sf_always_send_via_network, ["organ_bach_chromatic_fantasia.ogg"]),
 
 ("instruments_end",0, []),
 
 # tutorial
 ("tutorial_voice_start_1",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_1.ogg"]),
 #("tutorial_voice_start_2",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_2.ogg"]),
 #("tutorial_voice_start_3",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_3.ogg"]),
 ("tutorial_voice_1",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_4.ogg"]),
 ("tutorial_voice_2",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_5.ogg"]),
 ("tutorial_voice_3",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_6.ogg"]),
 #("tutorial_voice_4",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_7.ogg"]),
 ("tutorial_voice_4",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_8.ogg"]),
 ("tutorial_voice_5",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_9.ogg"]),
 ("tutorial_voice_6",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_10.ogg"]),
 ("tutorial_voice_7",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_11.ogg"]),
 ("tutorial_voice_8",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_12.ogg"]),
 ("tutorial_voice_9",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_13.ogg"]),
 ("tutorial_voice_10",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_14.ogg"]),
 ("tutorial_voice_11",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_15.ogg"]),
 ("tutorial_voice_12",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_16.ogg"]),
 ("tutorial_voice_13",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_17.ogg"]),
 ("tutorial_voice_14",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_18.ogg"]),
 ("tutorial_voice_15",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_19.ogg"]),
 ("tutorial_voice_16",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_20.ogg"]),
 ("tutorial_voice_17",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_21.ogg"]),
 ("tutorial_voice_18",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_22.ogg"]),
 ("tutorial_voice_19",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_23.ogg"]),
 ("tutorial_voice_20",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_24.ogg"]),
 ("tutorial_voice_21",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_25.ogg"]),
 ("tutorial_voice_22",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_26.ogg"]),
 ("tutorial_voice_23",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_27.ogg"]),
 ("tutorial_voice_24",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_28.ogg"]),
 ("tutorial_voice_25",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_29.ogg"]),
 ("tutorial_voice_26",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["tutorial_voice_30.ogg"]),
 
 
 # SP narrators 
 ("mission_narrator_1",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["mission_narrator_1.wav"]),
 ("mission_narrator_2",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["mission_narrator_1.wav"]),
 ("mission_narrator_3",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["mission_narrator_1.wav"]),
 ("mission_narrator_4",sf_2d|sf_priority_10|sf_vol_15|sf_stream_from_hd, ["mission_narrator_1.wav"]),
 
 ("sounds_end",0, []),
]
