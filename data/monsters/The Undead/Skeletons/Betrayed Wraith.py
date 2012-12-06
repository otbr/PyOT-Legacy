betrayed_wraith = genMonster("Betrayed Wraith", (233, 6316), "a betrayed wraith")
betrayed_wraith.setHealth(4200)
betrayed_wraith.bloodType("blood")
betrayed_wraith.setDefense(armor=46, fire=0, earth=0, energy=0, ice=0.5, holy=1.2, death=0, physical=1, drown=1)
betrayed_wraith.setExperience(3500)
betrayed_wraith.setSpeed(310)
betrayed_wraith.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=250)
betrayed_wraith.walkAround(energy=0, fire=0, poison=0)
betrayed_wraith.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
betrayed_wraith.voices("Rrrah!", "Gnarr!", "Tcharrr!")
betrayed_wraith.regMelee(455)
betrayed_wraith.loot( ("battle hammer", 4.75), ("concentrated demonic blood", 39.5), ("double axe", 31.5), (2148, 100, 318), ("unholy bone", 19.5), ("platinum coin", 24.0, 4), ("spike sword", 4.75), ("soul orb", 8.5), ("sniper arrow", 26.25, 5), ("demonic essence", 5.75, 3), ("orichalcum pearl", 9.25, 2), ("small diamond", 9.5), ("great mana potion", 1.0), ("skull helmet", 0.75), ("onyx arrow", 0.25), ("bloody edge", 0.25), ("death ring", 0.0025), ("golden figurine", 0.25) )