undead_gladiator = genMonster("Undead Gladiator", (306, 9823), "an undead gladiator")
undead_gladiator.health(1000)
undead_gladiator.type("undead")
undead_gladiator.defense(armor=37, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
undead_gladiator.experience(800)
undead_gladiator.speed(270)
undead_gladiator.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
undead_gladiator.walkAround(energy=1, fire=0, poison=1)
undead_gladiator.immunity(paralyze=0, invisible=1, lifedrain=1, drunk=0)
undead_gladiator.voices("Let's battle it out in a duel!", "Bring it!", "I'll fight here in eternity and beyond.", "I will not give up!", "Another foolish adventurer who tries to beat me.")
undead_gladiator.regMelee(250)
undead_gladiator.loot( ("plate armor", 2.5), (2148, 100, 148), ("brass legs", 6.75), ("brass armor", 6.0), ("scimitar", 11.25), ("protection amulet", 2.25), ("hunting spear", 4.5), ("belted cape", 4.5), ("throwing star", 100, 18), ("two handed sword", 2.5), ("meat", 4.75, 2), ("plate legs", 2.0), ("dark helmet", 1.25), ("health potion", 0.75), (5885, 0.25), ("knight axe", 0.5), ("broken gladiator shield", 3.5), ("stealth ring", 0.25), ("crusader helmet", 0.0025) )