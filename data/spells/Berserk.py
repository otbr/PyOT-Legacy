instant = spell.Spell("Berserk", "exori", icon=80, group=ATTACK_GROUP)
instant.require(mana=115, level=35, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(4, 2)
instant.area(AREA_SQUARE)
instant.targetEffect(callback=spell.damage(3.184, 5.59, 7, 11, PHYSICAL)) # TODO unknown (x, x, 7 ,11)
#skill based?
instant.effects() # TODO