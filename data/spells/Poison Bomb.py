
conjure = spell.Spell("Poison Bomb", "adevo mas pox", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=520, level=25, maglevel=0, soul=2, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2286, 2))

# Incomplete! Field rune.
rune = spell.Rune(2286, icon=91, count=2, target=TARGET_AREA, group=None)
rune.cooldowns(0, 2)
rune.require(mana=0, level=25, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO