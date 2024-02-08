# REMASTER IN PROGRESS
## IGNORE THIS DOCUMENT haha

<br><br><br>
NOTE: levels are free to be changed on your own fork, but take note to avoid touching the lobby, as the level selectors are hard coded.
DO NOT remove OR add files to the 'levels' directory

Controls:
Move - wasd, arrow keys, mouse r-click
Interact - space, z, m, mouse l-click
Return to menu - esc, del
Quit (only from menu) - esc, del


Normal blocks:
#=normal block
*=fancy block
-=platform (top half of a normal block, is the only thing that can stop a lift, other than another lift)

Details: (non-collide-able)
g = random ground detail
c = random ceiling detail
: = light grey block
. = grey block

Interact-able blocks:
| = level select (should never be changed or added to a level)
! = win-pad (only one per level)
= = lift (must be placed beneath a platform or another lift)
^ = BLUE switch
~ = RED switch
" = BLUE timer switch (only one per level) (timer switches wait 10 seconds before switching)
' = RED timer switch (only one per level)

Teleporters:
Only 9 teleporters allowed in any one level (5 BLUE & 5 RED)
The 'base' of the teleporter is prefixed with a number (from 0 to 4 for BLUE, 5 to 9 for RED, numerically)
The first 'point' of a teleporter is prefixed with every second letter in the alphabet. BLUE starting with 'a', RED starting with 'k'
The second 'point' of a teleporter is prefixed with every second letter in the alphabet. BLUE starting with 'b', RED starting with 'l'
EXAMPLE: The first BLUE teleporter in a level has a base prefixed with '0', the first point of that teleporter is prefixed with 'a', and the second with 'b'
            Adding a second BLUE teleporter will be '1, c, d', a third would be '2, e, f' and so on.
            Adding the first RED teleporter into a level would be a base of '5', first point is 'k', and second point is 'l'. The next: '6, m, n'

Every block is 20px by 20px
