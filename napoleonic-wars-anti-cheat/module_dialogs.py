# -*- coding: cp1254 -*-
from header_common import *
from header_dialogs import *
from header_operations import *
from module_constants import *


####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.  
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
# 7) Voice-over (string): sound filename for the voice over. Leave here empty for no voice over
####################################################################################################################

dialogs = [

    
  
  # Companion talks begin
  [anyone, "start", [(is_between, "$g_talk_troop", companions_begin, companions_end),
                    ],
   "Nice to meet you again {Sir/Madam}, How can I help you?.", "companion_talk", []],
  
  [anyone|plyr, "companion_talk", [
                    ],
   "Let me see your equipment.", "companion_talk_equipment", []],
   
   [anyone, "companion_talk_equipment", [
                    ],
   "Very well, Here it is.", "companion_talk_end", [(change_screen_equip_other)]],
   
   [anyone, "companion_talk_end", [
                    ],
   "Anything else?", "companion_talk", []],
   
   [anyone|plyr, "companion_talk", [
                    ],
   "What do you think of my commanding?", "companion_talk_opinion", []],
  
  [anyone, "companion_talk_opinion", [
                    ],
   "It is very good {Sir/Madam}!", "companion_talk", []],

  [anyone|plyr, "companion_talk", [
                    ],
   "Nothing, Carrry on.", "close_window", []],
  # Companion talks end

  
  # Merchants begin


  [anyone,"start", [(this_or_next|is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end),
                    (this_or_next|is_between,"$g_talk_troop",armor_merchants_begin, armor_merchants_end),
                    (             is_between,"$g_talk_troop",horse_merchants_begin, horse_merchants_end)
                    ], 
                    "Good day. What can I do for you?", "town_merchant_talk",[]],

  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",weapon_merchants_begin,weapon_merchants_end)],
   "I want to buy a new weapon. What do you have in stock?", "trade_requested_weapons",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",armor_merchants_begin,armor_merchants_end)],
   "I am looking for some new uniforms. Show me what you have.", "trade_requested_armor",[]],
  [anyone|plyr,"town_merchant_talk", [(is_between,"$g_talk_troop",horse_merchants_begin,horse_merchants_end)],
   "I am thinking of buying a horse.", "trade_requested_horse",[]],

  [anyone,"trade_requested_weapons", [], "Ah, yes {sir/madam}. These arms are the best you'll find anywhere.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_armor", [], "Of course, {sir/madam}. You won't find better quality uniforms anywhere in this army.", "merchant_trade",[[change_screen_trade]]],
  [anyone,"trade_requested_horse", [], "You have a fine eye for horses, {sir/madam}. You won't find better beasts than these anywhere else.", "merchant_trade",[[change_screen_trade]]],


  [anyone,"merchant_trade", [], "Anything else?", "town_merchant_talk",[]],
  [anyone|plyr,"town_merchant_talk", [], "Good-bye.", "close_window",[]],

 # Merchants end

# Camp walkers begin
                     
                     
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (is_between,"$g_talk_troop","trp_walker_french_infantry","trp_walker_french_officer"),
                    (str_store_troop_name,s14,"$g_talk_troop"),
                     ], "{s14} reporting for duty {Sir/Madam}!", "camp_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],
  
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (eq,"$g_talk_troop","trp_walker_french_officer"),
                     ], "Good day, {Sir/Madam}. Something to discuss?", "camp_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],
 
 [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (eq,"$g_talk_troop","trp_walker_messenger"),
                     ], "Sir, I bring orders for you to take on the next mission, are you prepared?", "camp_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],
 
  [anyone,"start", [(eq, "$talk_context", 0),
                    (is_between,"$g_talk_troop",walkers_begin, walkers_end),
                    (is_between,"$g_talk_troop","trp_walker_peasant_male","trp_walkers_end"),
                     ], "It is a honor to meet you, {Sir/Madam}. How can I be of service?", "camp_dweller_talk",[(assign, "$welfare_inquired", 0),(assign, "$rumors_inquired",0),(assign, "$info_inquired",0)]],

  [anyone|plyr,"camp_dweller_talk", [ (is_between,"$g_talk_troop","trp_walker_french_infantry","trp_walker_french_officer"),
                                    ], "Nothing, Carry on.", "close_window",[]],
  
  [anyone|plyr,"camp_dweller_talk", [ (eq,"$g_talk_troop","trp_walker_french_officer"),
                                    ], "Not at this time Sir, Have a nice evening.", "close_window",[]],
  [anyone|plyr,"camp_dweller_talk", [ (eq,"$g_talk_troop","trp_walker_messenger"),
                                    ], "Give me the orders! I shall leave at once.", "close_window",
                                    [ (jump_to_menu,"mnu_go_briefing_dummy"),
                                      (mission_enable_talk),
                                      (finish_mission,0)
                                      #(assign,"$g_pres_started_from_mission",1),
                                     # (start_presentation, "prsnt_singleplayer_campain_map"),
                                      #
                                      ]],
  [anyone|plyr,"camp_dweller_talk", [ (eq,"$g_talk_troop","trp_walker_messenger"),
                                    ], "I am not prepared yet.", "close_window",[]],
  [anyone|plyr,"camp_dweller_talk", [ (is_between,"$g_talk_troop","trp_walker_peasant_male","trp_walkers_end"),
                                    ], "Nevermind.", "close_window",[]],
                     
                     
# Camp walkers end
           
[anyone|plyr, "start", [], "Dialog Error. No dialog found.", "close_window", []],
]
