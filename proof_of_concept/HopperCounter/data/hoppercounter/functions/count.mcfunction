
data modify storage hoppercounter:main hoppers prepend value {id:-1,Items:[]}
execute store result storage hoppercounter:main hoppers[0].id int 1 run scoreboard players get @s hoppercounter.id
data modify storage hoppercounter:main hoppers[0].Items set from block ~ ~ ~ Items

data modify block ~ ~ ~ Items set value []
