
execute as @e[type=marker] at @s run particle minecraft:dragon_breath ~ ~ ~ 0 1 0 0 1

execute as @e[type=marker,tag=hoppercounter.counter] at @s unless block ~ ~ ~ hopper run kill @s
