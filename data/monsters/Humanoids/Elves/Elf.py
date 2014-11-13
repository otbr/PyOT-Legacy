elf = genMonster("Elf", (62, 6003), "an elf")
elf.health(100, healthmax=100)
elf.type("blood")
elf.defense(armor=7, fire=1, earth=1, energy=1, ice=1, holy=0.8, death=1.1, physical=1, drown=1)
elf.experience(42)
elf.speed(220)
elf.behavior(summonable=320, hostile=1, illusionable=1, convinceable=320, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=0)
elf.walkAround(energy=1, fire=1, poison=1)
elf.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
elf.voices("Death to the Defilers!", "You are not welcome here.", "Flee as long as you can.", "Bahaha aka!", "Ulathil beia Thratha!")
elf.regMelee(15)
elf.regDistance(25, ANIMATION_ARROW, chance(21))
elf.loot( ("arrow", 15.5, 3), ("plum", 33.5, 2), (2148, 100, 30), ("studded armor", 10.0), ("studded helmet", 16.0), ("plate shield", 8.75), ("leather boots", 11.5), ("longsword", 12.5), ("elvish talisman", 2.5), (5921, 1.0) )