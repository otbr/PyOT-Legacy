crimson_frog = genMonster("Crimson Frog", (226, 6079), "a crimson frog")
crimson_frog.setOutfit(94, 78, 94, 78)
crimson_frog.setTargetChance(10)
crimson_frog.type("blood")
crimson_frog.health(60)
crimson_frog.experience(20)
crimson_frog.speed(200)
crimson_frog.walkAround(1,1,1) # energy, fire, poison
crimson_frog.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=0)
crimson_frog.voices("Ribbit!", "Ribbit! Ribbit!")
crimson_frog.immunity(0,0,0) # paralyze, invisible, lifedrain
crimson_frog.defense(9, fire=1.1, earth=1.0, energy=1.0, ice=0.85, holy=1.0, death=1.0, physical=1.0, drown=1.0)
crimson_frog.loot( (2148, 100, 10), (3976, 9.0) )

crimson_frog.regMelee(24)