import game.monster

mutated_bat = game.monster.genMonster("Mutated Bat", (307, 9829), "a mutated bat")
mutated_bat.setHealth(900)
mutated_bat.bloodType(color="blood")
mutated_bat.setDefense(armor=30, fire=1, earth=0, energy=1, ice=1, holy=1, death=0, physical=1, drown=0)
mutated_bat.setExperience(615)
mutated_bat.setSpeed(245)
mutated_bat.setBehavior(summonable=0, attackable=1, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=300)
mutated_bat.walkAround(energy=0, fire=0, poison=0)
mutated_bat.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
mutated_bat.voices("Shriiiiiek")