goblin_leader = game.monster.genMonster("Goblin Leader", (61, 6002), "a goblin leader")
goblin_leader.setHealth(50)
goblin_leader.bloodType(color="blood")
goblin_leader.setDefense(armor=5, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
goblin_leader.setExperience(75)
goblin_leader.setSpeed(200)
goblin_leader.setBehavior(summonable=290, hostile=1, illusionable=1, convinceable=0, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=10)
goblin_leader.walkAround(energy=1, fire=1, poison=1)
goblin_leader.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
goblin_leader.voices("Go go, Gobo attack!!", "Me the greenest and the meanest!", "Me have power to crush you!", "Goblinkiller! Catch him !!")
goblin_leader.regMelee(50)
goblin_leader.loot( (2148, 100, 9), ("bone", 10.75), ("dagger", 19.25), ("leather armor", 5.5), ("leather helmet", 12.0), ("small axe", 11.5), ("fish", 10.25), ("short sword", 9.75), ("bone club", 3.5), (2235, 3.0) )