
conjure = spell.Spell("Ultimate Healing Rune", "adura vita", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=400, level=24, maglevel=0, soul=3, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2273, 1))

# Incomplete! Target rune.
rune = spell.Rune(2273, icon=5, count=1, target=TARGET_TARGET, group=None)
rune.cooldowns(0, 1)
rune.require(mana=0, level=24, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO