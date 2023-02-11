
summon marker ~ ~ ~ {Tags:["hoppercounter.counter", "hoppercounter.new"]}

execute as @e[type=marker,tag=hoppercounter.new] run scoreboard players operation @s hoppercounter.id = target_id hoppercounter.id
execute as @e[type=marker,tag=hoppercounter.new] run tag @s remove hoppercounter.new

fill ~ ~ ~ ~ ~ ~ hopper keep
