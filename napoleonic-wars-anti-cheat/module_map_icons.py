from header_map_icons import *

####################################################################################################################
#  Each map icon record contains the following fields:
#  1) Map icon id: used for referencing map icons in other files.
#     The prefix icon_ is automatically added before each map icon id.
#  2) Map icon flags. See header_map icons.py for a list of available flags
#  3) Mesh name.
#  4) Scale. 
#  5) Sound.
#  6) Offset x position for the flag icon.
#  7) Offset y position for the flag icon.
#  8) Offset z position for the flag icon.
####################################################################################################################

map_icons = [
    ("player", 0, "empty_mesh", 0.15, 0, 0.15, 0.173, 0),
    ("player_horseman", 0, "empty_mesh", 0.15, 0, 0.15, 0.173, 0),
]
