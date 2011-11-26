
conjure = spell.Spell("Light Magic Missile", "adori min vis", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=120, level=15, maglevel=0, soul=1, learned=0, vocations=(1, 2, 5, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2287, 10))

# Incomplete! Target rune.
rune = spell.Rune(2287, icon=7, count=10, target=TARGET_TARGET, group=None)
rune.cooldowns(0, 2)
rune.require(mana=0, level=15, maglevel=0)
rune.targetEffect() # TODO
rune.effects() # TODO