
conjure = spell.Spell("Conjure Piercing Bolt", "exevo con grav", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=180, level=33, maglevel=0, soul=3, learned=0, vocations=(3, 7))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(7363, 5))