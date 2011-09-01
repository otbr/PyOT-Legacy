# This is a shadow of the main branch, 9.1. TODO: Update for 8.6 changes
import base
from twisted.python import log
import config
import math
import game.enum

provide = []
compatible_protocols = [910]

def vertify():
    if config.allowMounts:
        log.msg("Protocol 860 doesn't allow mounts")
        return False
    return True
    
class Packet(base.BasePacket):
    def creature(self, creature, known):
        if known:
            self.uint16(0x62)
            self.uint32(creature.clientId())
        else:
            self.uint16(0x61)
            self.uint32(0) # Remove known
            self.uint32(creature.clientId())
            #self.uint8(creature.creatureType)
            self.string(creature.name())
        self.uint8(100) # Health %
        self.uint8(creature.direction) # Direction
        self.outfit(creature.outfit, creature.addon, creature.mount if creature.mounted else 0x00)
        self.uint8(0) # Light
        self.uint8(0) # Light
        self.uint16(creature.speed) # Speed
        self.uint8(0) # Skull
        self.uint8(0) # Party/Shield
        if not known:
            self.uint8(0) # Emblem
        self.uint8(creature.solid) # Can't walkthrough

    def status(self, player):
        self.uint8(0xA0)
        self.uint16(player.data["health"])
        self.uint16(player.data["healthmax"])
        self.uint32(player.data["capasity"] * 100) # TODO: Free Capasity
        #self.uint32(player.data["capasity"] * 100) # TODO: Cap
        if player.data["experience"] <= 0x7FFFFFFF:
            self.uint32(player.data["experience"]) # TODO: Virtual cap? Experience
        else:
            self.uint32(0)
            
        if player.data["level"] > 0xFFFF:
            self.uint16(0xFFFF)
        else:
            self.uint16(player.data["level"]) # TODO: Virtual cap? Level
            
        self.uint8(math.ceil(float(config.levelFormula(player.data["level"]+1)) / player.data["experience"])) # % to next level, TODO
        self.uint16(player.data["mana"]) # mana
        self.uint16(player.data["manamax"]) # mana max
        self.uint8(player.data["maglevel"]) # TODO: Virtual cap? Manalevel
        #self.uint8(1) # TODO: Virtual cap? ManaBase
        self.uint8(0) # % to next level, TODO
        self.uint8(player.data["soul"]) # TODO: Virtual cap? Soul
        self.uint16(min(42 * 60, player.data["stamina"] / 60)) # Stamina minutes
        #self.uint16(player.speed) # Speed
        
        #self.uint16(0x00) # Condition

    def skills(self, player):
        self.uint8(0xA1) # Skill type
        for x in xrange(game.enum.SKILL_FIRST, game.enum.SKILL_LAST+1):
            self.uint8(player.skills[x]) # Value / Level
            #self.uint8(1) # Base
            self.uint8(0) # %

    def outfit(self, look, addon=0, mount=0x00):
        
        self.uint16(look[0])
        if look[0] != 0:
            self.uint8(look[1])
            self.uint8(look[2])
            self.uint8(look[3])
            self.uint8(look[4])
            self.uint8(addon)
        else:
            self.uint16(look[1])
            
        #self.uint16(mount) # Mount
        
class Protocol(base.BaseProtocol):
    Packet = Packet