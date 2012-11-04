water_elemental = genMonster("Water Elemental", (286, 10499), "a water elemental")
water_elemental.setHealth(550, healthmax=550)
water_elemental.bloodType(color="undead")
water_elemental.setDefense(armor=50, fire=0, earth=0, energy=1.25, ice=0, holy=0.5, death=0.5, physical=0.3, drown=1)
water_elemental.setExperience(650)
water_elemental.setSpeed(260)
water_elemental.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
water_elemental.walkAround(energy=1, fire=0, poison=0)
water_elemental.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
water_elemental.voices("Splish splash")
water_elemental.regMelee(165)
water_elemental.loot( ("energy ring", 1.25), (2148, 100, 100), ("rainbow trout", 1.25), ("fish", 20.0), ("strong health potion", 9.75), ("platinum coin", 10.25), ("life ring", 1.25), ("strong mana potion", 10.0), ("small emerald", 1.5, 2), ("small diamond", 1.0), ("green perch", 0.75) )