instant = spell.Spell("Fire Wave", "exevo flam hur", icon=19, group=ATTACK_GROUP)
instant.require(mana=25, level=18, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(4, 2)
instant.area(AREA_WAVE4)
instant.targetEffect(callback=spell.damage(1.2, 2.2, 7, 8, FIRE))
instant.effects() # TODO