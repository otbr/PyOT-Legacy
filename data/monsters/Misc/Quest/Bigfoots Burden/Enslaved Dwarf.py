enslaved_dwarf = genMonster("Enslaved Dwarf", (494, 17407), "an enslaved dwarf")#mostly unkniown
enslaved_dwarf.health(3800, healthmax=3800)
enslaved_dwarf.type("blood")
enslaved_dwarf.defense(armor=35, fire=0, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
enslaved_dwarf.experience(2700)
enslaved_dwarf.speed(400)
enslaved_dwarf.behavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
enslaved_dwarf.walkAround(energy=1, fire=0, poison=0)
enslaved_dwarf.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
enslaved_dwarf.voices("Bark!")
enslaved_dwarf.regMelee(400)