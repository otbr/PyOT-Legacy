scarab = game.monster.genMonster("Scarab", (83, 6024), "a scarab")
scarab.setHealth(320, healthmax=320)
scarab.bloodType(color="slime")
scarab.setDefense(armor=15, fire=1.18, earth=0, energy=0.9, ice=0.8, holy=1, death=1, physical=0.95, drown=1)
scarab.setExperience(120)
scarab.setSpeed(170)
scarab.setBehavior(summonable=395, hostile=1, illusionable=1, convinceable=395, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=80)
scarab.walkAround(energy=1, fire=1, poison=0)
scarab.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
scarab.regMelee(75)
scarab.loot( ("scarab coin", 1.0), ("piece of scarab shell", 4.5), (2148, 100, 52), ("meat", 40.0, 2), ("small amethyst", 0.5), ("daramanian mace", 0.25), ("small emerald", 0.25) )