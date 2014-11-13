zombie = genMonster("Zombie", (311, 9875), "a zombie")
zombie.health(500)
zombie.type("undead")
zombie.defense(armor=22, fire=0.5, earth=0, energy=0, ice=0, holy=1, death=0, physical=1, drown=0)
zombie.experience(280)
zombie.speed(180)#incorrect speed?
zombie.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
zombie.walkAround(energy=0, fire=1, poison=0)
zombie.immunity(paralyze=1, invisible=0, lifedrain=1, drunk=1)
zombie.voices("Mst.... klll....", "Whrrrr... ssss.... mmm.... grrrrl", "Dnnnt... cmmm... clsrrr....", "Httt.... hmnnsss...")
zombie.regMelee(130)
zombie.loot( (2148, 100, 65), ("brass helmet", 10.5), ("steel helmet", 5.0), ("mace", 8.75), ("half-eaten brain", 10.75), ("battle hammer", 7.25), ("rusty armor", 6.75), ("mana potion", 0.75), ("halberd", 4.25), ("life ring", 1.0), ("simple dress", 0.5) )