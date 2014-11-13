Lion = genMonster("Lion", (41, 5986), "a lion")
Lion.setTargetChance(10)
Lion.type("blood")
Lion.health(80)
Lion.experience(30)
Lion.speed(190) #correct
Lion.walkAround(1,1,1) # energy, fire, poison
Lion.behavior(summonable=320, hostile=1, illusionable=1, convinceable=320, pushable=0, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=10)
Lion.voices("Groarrr!")
Lion.immunity(0,0,0) # paralyze, invisible, lifedrain
Lion.defense(7, fire=1.0, earth=0.8, energy=1.0, ice=1.15, holy=0.8, death=1.08, physical=1.0, drown=1.0)
Lion.loot( ("meat", 48.0, 4), ("ham", 19.5, 2), (10608, 0.75) )
Lion.regMelee(40)