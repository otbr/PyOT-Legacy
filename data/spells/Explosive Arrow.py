
conjure = spell.Spell("Explosive Arrow", "exevo con flam", icon=49, group=SUPPORT_GROUP)
conjure.require(mana=290, level=25, maglevel=0, soul=3, learned=0, vocations=(3, 7))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2546, 8))