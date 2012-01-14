
warlock = game.monster.genMonster("Warlock", (130, 6080), "a warlock")
warlock.setOutfit(19, 71, 128, 128) #needs an addon
warlock.setHealth(3500)
warlock.bloodType(color="blood")
warlock.setDefense(armor=37, fire=0, earth=0.05, energy=0, ice=0, holy=1.08, death=1, physical=1.05, drown=1)
warlock.setExperience(4000)
warlock.setSpeed(220)
warlock.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=800)
warlock.walkAround(energy=0, fire=0, poison=0)
warlock.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
warlock.voices("Even a rat is a better mage than you!", "Learn the secret of our magic! YOUR death!", "We don't like intruders!")
warlock.summon("stone golem", 10)
warlock.maxSummons(1)
warlock.regMelee(130)
warlock.loot( ("lightning robe", 1.0), ("small sapphire", 1.25), ("inkwell", 1.0), ("talon", 1.0), ("blue robe", 1.75), ("energy ring", 1.75), ("dark mushroom", 3.0), ("candlestick", 1.25), ("ring of the sky", 0.5), ("crystal ring", 0.75), ("luminous orb", 0.5), ("great mana potion", 5.0), ("red tome", 0.25), ("poison dagger", 7.5), ("skull staff", 6.0), ("assassin star", 8.75, 4), ("mind stone", 2.25), ("great health potion", 5.0), ("cherry", 49.25, 4), ("bread", 9.25), (2148, 100, 80), ("golden armor", 0.25), ("stone skin amulet", 0.5), ("piggy bank", 0.0025) )