cliff_strider = genMonster("Cliff Strider", (497, 17420), "a cliff strider")#mostly unkniown including
cliff_strider.setHealth(9400, healthmax=9400)
cliff_strider.bloodType("blood")
cliff_strider.setDefense(armor=55, fire=0.8, earth=0, energy=0, ice=0.2, holy=1, death=0.65, physical=0.9, drown=1)
cliff_strider.setExperience(5700)
cliff_strider.setSpeed(350)
cliff_strider.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
cliff_strider.walkAround(energy=0, fire=1, poison=0)
cliff_strider.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
cliff_strider.voices("Knorrrr")
cliff_strider.regMelee(500)