from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################


factions = [
  ("no_faction","No Faction",0, 0.9, [], []),
  ("commoners","Commoners",0, 0.1,[("player_faction",0.1)], []),
  ("outlaws","Outlaws", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15)], [], 0x888888),
# Factions before this point are hardwired into the game end their order should not be changed.

  ("neutral","Neutral",0, 0.1,[("player_faction",0.0)], [],0xFFFFFF),

  ("player_faction","Player Faction",0, 0.9, [], []),
  ("player_supporters_faction","Player's Supporters",0, 0.9, [("player_faction",1.00),("outlaws",-0.05)], [], 0xFF4433), #changed name so that can tell difference if shows up on map
  ("britain",  "United Kingdom",    0, 0.9, [("outlaws",-0.05),], [], 0xCCBB99),
  ("france",  "Empire Francais", 0, 0.9, [("outlaws",-0.05)], [], 0xCC99FF),
  ("prussia",  "Konigreich Preussen", 0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),
  ("russia",  "Rossiyskaya Imperiya",    0, 0.9, [("outlaws",-0.05)], [], 0x33DDDD),
  ("austria",  "Kaisertum Osterreich",  0, 0.9, [("outlaws",-0.05)], [], 0x33DD33),
  ("rhine",  "Rheinbund",  0, 0.9, [("outlaws",-0.05)], [], 0xDDDD33),
  ("kingdoms_end","{!}kingdoms_end", 0, 0,[], []),
  ("kingdom_7",  "Invalid Faction",  0, 0.9, [("outlaws",-0.05)], [], 0xDDDD33),
  ("kingdom_8",  "Invalid Faction",  0, 0.9, [("outlaws",-0.05)], [], 0xDDDD33),
  ("kingdom_9",  "Invalid Faction",  0, 0.9, [("outlaws",-0.05)], [], 0xDDDD33),
  ("kingdom_10", "Invalid Faction",  0, 0.9, [("outlaws",-0.05)], [], 0xDDDD33),
  ("british_ranks", "British Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),
  ("french_ranks", "French Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCC99FF),
  ("prussian_ranks", "Prussian Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),
  ("russian_ranks", "Russian Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),
  ("austrian_ranks", "Austrian Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),
  ("rhine_ranks", "Rhenish Other Ranks",  0, 0.9, [("outlaws",-0.05)], [], 0xCCBB99),

]
