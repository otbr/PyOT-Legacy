eternal_guardian = genMonster("Eternal Guardian", (345, 11278), "an eternal guardian")
eternal_guardian.health(2500)
eternal_guardian.type("blood")
eternal_guardian.defense(armor=2, fire=0.7, earth=0, energy=0.9, ice=0.9, holy=0.8, death=0.8, physical=1, drown=1)#
eternal_guardian.experience(1800)
eternal_guardian.speed(420)
eternal_guardian.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
eternal_guardian.walkAround(energy=1, fire=0, poison=0)
eternal_guardian.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
eternal_guardian.regMelee(300)
eternal_guardian.loot( (2148, 100, 53), ("small stone", 100, 10) )