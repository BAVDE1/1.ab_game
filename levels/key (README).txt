NOTE: levels are free to be changed, but avoid touching the lobby, or at least not the level selectors in the lobby.
DO NOT remove OR add files to the 'levels' directory

Normal blocks:
# = normal block
* = fancy block
: = grey block (non-collide-able)
. = light grey block (non-collide-able)
- = platform (top half of a normal block, is the only thing that can stop a lift, other than another lift)

Interact-able blocks:
| = level select (should never be changed or added to a level)
! = win-pad (only one per level)
= = lift (must be placed beneath a platform or another lift)
^ = BLUE switch
~ = RED switch
" = BLUE timer switch (only one per level)
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