bane_of_light = genMonster("Bane of Light", (68, 6006), "a bane of light")
bane_of_light.health(1100, healthmax=1100)
bane_of_light.type("blood")
bane_of_light.defense(armor=32, fire=0, earth=0.8, energy=1.2, ice=0, holy=1, death=1, physical=1, drown=1)
bane_of_light.experience(750)
bane_of_light.speed(300)
bane_of_light.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
bane_of_light.walkAround(energy=0, fire=0, poison=0)
bane_of_light.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
bane_of_light.regMelee(370)
bane_of_light.loot( ("midnight shard", 7.25) )