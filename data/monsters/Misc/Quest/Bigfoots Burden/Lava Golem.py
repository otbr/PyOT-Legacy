Lava_Golem = genMonster("Lava Golem", (491, 15987), "a lava golem") #mostly unknown
Lava_Golem.health(9000)
Lava_Golem.type("blood")
Lava_Golem.defense(armor=80, fire=0, earth=0, energy=0.7, ice=1.05, holy=1, death=0.55, physical=0.7, drown=1)
Lava_Golem.experience(6200)
Lava_Golem.speed(500)
Lava_Golem.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
Lava_Golem.walkAround(energy=0, fire=0, poison=0)
Lava_Golem.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Lava_Golem.voices("Grrrrunt")
Lava_Golem.regMelee(200)