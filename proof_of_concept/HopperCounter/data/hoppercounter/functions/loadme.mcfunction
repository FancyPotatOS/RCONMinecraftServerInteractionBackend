
scoreboard objectives add hoppercounter.id dummy

execute unless score init hoppercounter.id matches 1 run function hoppercounter:init
