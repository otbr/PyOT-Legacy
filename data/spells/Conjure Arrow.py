
conjure = spell.Spell("Conjure Arrow", "exevo con", icon=51, group=SUPPORT_GROUP)
conjure.require(mana=100, level=13, maglevel=0, soul=1, learned=0, vocations=(3, 7))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2544, 10))