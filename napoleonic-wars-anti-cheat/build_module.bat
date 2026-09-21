@echo off
py -V:2.7 process_init.py
py -V:2.7 process_global_variables.py
py -V:2.7 process_strings.py
py -V:2.7 process_skills.py
py -V:2.7 process_music.py
py -V:2.7 process_animations.py
py -V:2.7 process_meshes.py
py -V:2.7 process_sounds.py
py -V:2.7 process_skins.py
py -V:2.7 process_map_icons.py
py -V:2.7 process_factions.py
py -V:2.7 process_items.py
py -V:2.7 process_scenes.py
py -V:2.7 process_troops.py
py -V:2.7 process_particle_sys.py
py -V:2.7 process_scene_props.py
py -V:2.7 process_tableau_materials.py
py -V:2.7 process_presentations.py
py -V:2.7 process_party_tmps.py
py -V:2.7 process_parties.py
py -V:2.7 process_quests.py
py -V:2.7 process_info_pages.py
py -V:2.7 process_scripts.py
py -V:2.7 process_mission_tmps.py
py -V:2.7 process_game_menus.py
py -V:2.7 process_simple_triggers.py
py -V:2.7 process_dialogs.py
py -V:2.7 process_global_variables_unused.py
py -V:2.7 process_postfx.py
@del *.pyc
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to exit. . .
pause>nul