
mySpell = spell.regSpell2("Phoenix", "pho", icon=30, target=TARGET_AREA)
mySpell.area(AREA_CIRCLE2)
# Effects. caster, target, area and shoot
mySpell.effects(caster=EFFECT_YALAHARIGHOST, area=EFFECT_FIREAREA)

# Require, can be any field inside player.data. Mana is special since it's used!
# We also have requireLess and requireCallback if you need some complex chceks :)
mySpell.require(level=10, mana=50, maglevel=15)

# You can register as many effects as you like.
mySpell.targetEffect(health=-100) # Static effect :p
mySpell.targetEffect(callback=spell.damage(3.184, 5.59, 20, 35)) # Formula generator :)

# You can also raise conditions.
mySpell.casterCondition(Condition(CONDITION_FIRE, '', 40, damage=5)) # Side effect.
mySpell.targetCondition(Condition(CONDITION_FIRE, '', 20, damage=15)) # Side effect on target

# TODO Rune syntax.