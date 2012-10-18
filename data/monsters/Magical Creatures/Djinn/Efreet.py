efreet = genMonster("Efreet", (103, 6032), "a efreet")
efreet.setHealth(550, healthmax=550)
efreet.bloodType(color="blood")
efreet.setDefense(armor=27, fire=0.9, earth=0.9, energy=0.4, ice=1.05, holy=1.08, death=0.8, physical=1, drown=1)
efreet.setExperience(410)#325?
efreet.setSpeed(170)
efreet.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
efreet.walkAround(energy=1, fire=1, poison=1)
efreet.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
efreet.summon("green djinn", 10)
efreet.maxSummons(2)
efreet.voices("I grant you a deathwish!", "Good wishes are for fairytales")
efreet.regMelee(110)
efreet.loot( ("strong mana potion", 10.75), ("pear", 31.75, 5), (2148, 100, 130), ("small emerald", 7.25), ("royal spear", 32.5, 3), (12426, 7.5), ("magma monocle", 0.75), ("wand of inferno", 0.75), ("green piece of cloth", 3.5, 3), ("green tapestry", 2.5), ("heavy machete", 4.75), ("small oil lamp", 0.25), ("mystic turban", 0.25), (12442, 1.0), ("green gem", 0.0025) )