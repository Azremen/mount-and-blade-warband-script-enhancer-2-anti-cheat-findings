from header_music import *
####################################################################################################################
#  Each track record contains the following fields:
#  1) Track id: used for referencing tracks.
#  2) Track file: filename of the track
#  3) Track flags. See header_music.py for a list of available flags
#  4) Continue Track flags: Shows in which situations or cultures the track can continue playing. See header_music.py for a list of available flags
####################################################################################################################

# WARNING: You MUST add mtf_module_track flag to the flags of the tracks located under module directory

tracks = [
##  ("losing_battle", "alosingbattle.mp3", sit_calm|sit_action),
##  ("reluctant_hero", "reluctanthero.mp3", sit_action),
##  ("the_great_hall", "thegreathall.mp3", sit_calm),
##  ("requiem", "requiem.mp3", sit_calm),
##  ("silent_intruder", "silentintruder.mp3", sit_calm|sit_action),
##  ("the_pilgrimage", "thepilgrimage.mp3", sit_calm),
##  ("ambushed", "ambushed.mp3", sit_action),
##  ("triumph", "triumph.mp3", sit_action),

##  ("losing_battle", "alosingbattle.mp3", mtf_sit_map_travel|mtf_sit_attack),
##  ("reluctant_hero", "reluctanthero.mp3", mtf_sit_attack),
##  ("the_great_hall", "thegreathall.mp3", mtf_sit_map_travel),
##  ("requiem", "requiem.mp3", mtf_sit_map_travel),
##  ("silent_intruder", "silentintruder.mp3", mtf_sit_map_travel|mtf_sit_attack),
##  ("the_pilgrimage", "thepilgrimage.mp3", mtf_sit_map_travel),
##  ("ambushed", "ambushed.mp3", mtf_sit_attack),
##  ("triumph", "triumph.mp3", mtf_sit_attack),
  ("bogus", "cant_find_this.ogg", 0, 0),
  ("mount_and_blade_title_screen", "mm_intro.ogg", mtf_module_track|mtf_sit_main_title|mtf_start_immediately, 0),

  ("strauss_radetzky_march", "strauss_radetzky_march.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("beethoven_symphony_no_9_movement_4", "beethoven_symphony_no_9_movement_4.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("franz_schubert_marche_militaire", "franz_schubert_marche_militaire.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("mozart_great_mass_gloria", "mozart_great_mass_gloria.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bizet_carmen_toreador", "bizet_carmen_toreador.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("wagner_ride_of_the_valkyries", "wagner_ride_of_the_valkyries.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("beethoven_symphony_5_1", "beethoven_symphony_5_1.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("dvorak_symphony_9_4", "dvorak_symphony_9_4.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("tchaikovsky_overture_1812", "tchaikovsky_overture_1812.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bach_cello_suite_1", "bach_cello_suite_1.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("elgar_pomp_and_circumstance_march_1", "elgar_pomp_and_circumstance_march_1.mp3", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("handel_queen_of_sheba", "handel_queen_of_sheba.mp3", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("handel_hallelujah_chorus_from_the_messiah", "handel_hallelujah_chorus_from_the_messiah.mp3", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_summer_presto", "vivaldi_summer_presto.mp3", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("william_boyce_sinfonia_1", "william_boyce_sinfonia_1.mp3", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("mazurek_dabrowskiego_polish_national_anthem", "mazurek_dabrowskiego_polish_national_anthem.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("grieg_peer_gynt_overture", "grieg_peer_gynt_overture.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bach_orchestral_suite_3_air", "bach_orchestral_suite_3_air.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("geminiani_concerto_grosso", "geminiani_concerto_grosso.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("grieg_peer_gynt_in_the_hall_of_the_mountain_king", "grieg_peer_gynt_in_the_hall_of_the_mountain_king.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("liszt_les_preludes", "liszt_les_preludes.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("chopin_polonaise_military", "chopin_polonaise_military.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bizet_carmen_aragonaise", "bizet_carmen_aragonaise.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("hummel_rondo", "hummel_rondo.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bach_concerto_for_two_violins_first_movement", "bach_concerto_for_two_violins_first_movement.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("boccherini_minuet", "boccherini_minuet.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("brahms_hungarian_dance_5", "brahms_hungarian_dance_5.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("mozart_eine_kleine_nachtmusik_allegro", "mozart_eine_kleine_nachtmusik_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("strauss_blue_danube_waltz", "strauss_blue_danube_waltz.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("rimsky_korsakov_the_flight_of_the_bumble_bee", "rimsky_korsakov_the_flight_of_the_bumble_bee.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bach_gavotte", "bach_gavotte.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_spring_allegro", "vivaldi_spring_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_spring_allegro_2", "vivaldi_spring_allegro_2.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_autumn_allegro", "vivaldi_autumn_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_summer_allegro_adagio", "vivaldi_summer_allegro_adagio.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_winter_presto", "vivaldi_winter_presto.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_winter_allegro", "vivaldi_winter_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_concerto_10_allegro_II", "vivaldi_concerto_10_allegro_II.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_concerto_flute_violin_continuo_allegro", "vivaldi_concerto_flute_violin_continuo_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("vivaldi_concerto_grosso_8_allegro", "vivaldi_concerto_grosso_8_allegro.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("mendelssohn_wedding_march_recessional", "mendelssohn_wedding_march_recessional.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("bach_brandenburg_concerto_movement_1", "bach_brandenburg_concerto_movement_1.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("pachelbel_canon", "pachelbel_canon.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("saint_saens_danse_macabre", "saint_saens_danse_macabre.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  ("rossini_william_tell_overture", "rossini_william_tell_overture.ogg", mtf_module_track|mtf_sit_fight|mtf_sit_multiplayer_fight|mtf_sit_ambushed|mtf_sit_siege, 0),
  
]
