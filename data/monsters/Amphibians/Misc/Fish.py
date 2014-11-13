fish = genMonster("Fish", (455, 2667), "a fish")
fish.health(25)
fish.type("blood")
fish.defense(armor=5, fire=0, earth=0, energy=1, ice=1, holy=1, death=1, physical=1, drown=0)
fish.experience(0)
fish.speed(250) #?
fish.behavior(summonable=0, hostile=0, illusionable=1, convinceable=0, pushable=0, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=25) #runs hostile?
fish.walkAround(energy=1, fire=0, poison=0)
fish.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
fish.voices("Blib!", "Blub!")