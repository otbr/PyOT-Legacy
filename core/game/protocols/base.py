# This is the "common protocol" in which all other sub protocols is based upon
from packet import TibiaPacket
from twisted.internet.defer import deferredGenerator, waitForDeferred
from twisted.internet import defer, reactor
import game.enum
enum = game.enum
import math
import config
import sys
from collections import deque

class BasePacket(TibiaPacket):
    # Position
    # Parameters is list(x,y,z)
    def position(self, position):
        self.uint16(position[0])
        self.uint16(position[1])
        self.uint8(position[2])

    # Magic Effect
    def magicEffect(self, pos, type):
        self.uint8(0x83)
        self.position(pos)
        self.uint8(type)
   
    # Shoot
    def shoot(self, fromPos, toPos, type):
        self.uint8(0x85)
        self.position(fromPos)
        self.position(toPos)
        self.uint8(type)

    # Item
    # Parameters is of class Item or ItemID
    def item(self, item, count=None):
        import game.item
        if isinstance(item, game.item.Item):
            self.uint16(item.cid)

            if item.stackable:
                self.uint8(item.count or 1)
            elif item.type == 11 or item.type == 12:
                self.uint8(item.fluidSource or 0)
            if item.animation:
                self.uint8(0xFE)
            
        else:
            print item
            self.uint16(item)
            if count:
                self.uint8(count)

    # Map Description (the entier visible map)
    # Isn't "Description" a bad word for it?
    def mapDescription(self, position, width, height, player=None):
        skip = -1
        start = 7
        end = 0
        step = -1

        # Lower then ground level
        if position[2] > 7:
            start = position[2] - 2
            end = min(15, position[2] + 2) # Choose the smallest of 15 and z + 2
            step = 1

        # Run the steps by appending the floor
        for z in xrange(start, (end+step), step):
            skip = self.floorDescription((position[0], position[1], z), width, height, position[2] - z, skip, player)

        if skip >= 0:
            self.uint8(skip)
            self.uint8(0xFF)
        
    # Floor Description (the entier floor)
    def floorDescription(self, position, width, height, offset, skip, player=None):
        for x in xrange(0, width):
            for y in xrange(0, height):
                tile = sys.modules["game.map"].getTile((position[0] + x + offset, position[1] + y + offset, position[2]))

                if tile and tile.things:
                    if skip >= 0:
                        self.uint8(skip)
                        self.uint8(0xFF)
                    skip = 0
                    self.tileDescription(tile, player)
                else:
                    skip += 1
                    if skip == 0xFF:
                        self.uint8(0xFF)
                        self.uint8(0xFF)
                        skip = -1
        return skip

    def tileDescription(self, tile, player=None):
        self.uint16(0x00)
        isSolid = False
        for item in tile.topItems():
            if item.solid:
                isSolid = True
                
            self.item(item)
        
        if not isSolid:
            for creature in tile.creatures():
                if creature == None:
                    del creature
                    continue
                
                known = False
                if player:
                    known = creature.cid in player.knownCreatures
                    
                    if not known:
                        player.knownCreatures.append(creature.cid)
    
                self.creature(creature, known)
                if creature.creatureType != 0 and creature.noBrain:
                    print "Begin think 1"
                    creature.base.brain.handleThink(creature, False)

            for item in tile.bottomItems():
                self.item(item)

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
            
        self.uint16(mount) # Mount
        
    def creature(self, creature, known):
        if known:
            self.uint16(0x62)
            self.uint32(creature.clientId())
        else:
            self.uint16(0x61)
            self.uint32(0) # Remove known
            self.uint32(creature.clientId())
            self.uint8(creature.creatureType)
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
        
    def worldlight(self, level, color):
        self.uint8(0x82)
        self.uint8(level)
        self.uint8(color)

    def creaturelight(self, cid, level, color):
        self.uint8(0x8D)
        self.uint32(cid)
        self.uint8(level)
        self.uint8(color)

    def removeInventoryItem(self, pos):
        self.uint8(0x79)
        self.uint8(pos)
        
    def addInventoryItem(self, pos, item):
        self.uint8(0x78)
        self.uint8(pos)
        self.item(item)

    def addContainerItem(self, openId, item):
        self.uint8(0x70)
        self.uint8(openId)
        self.item(item)
        
    def updateContainerItem(self, openId, slot, item):
        self.uint8(0x71)
        self.uint8(openId)
        self.uint8(slot)
        self.item(item)
       
    def removeContainerItem(self, openId, slot):
        self.uint8(0x72)
        self.uint8(openId)
        self.uint8(slot)
        
    def addTileItem(self, pos, stackpos, item):
        self.uint8(0x6A)
        self.position(pos)
        self.uint8(stackpos)
        self.item(item)

    def addTileCreature(self, pos, stackpos, creature, player=None):
        self.uint8(0x6A)
        self.position(pos)
        self.uint8(stackpos)
        known = False
        if player and creature != player:
            known = creature.cid in player.knownCreatures
                
            if not known:
                player.knownCreatures.append(creature.cid)
 
        self.creature(creature, known)

    def moveUpPlayer(self, player, oldPos):
        self.uint8(0xBE)
        
        # Underground to surface
        if oldPos[2]-1 == 7:
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 5), 18, 14, 3, -1, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 4), 18, 14, 4, skip, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 3), 18, 14, 5, skip, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 2), 18, 14, 6, skip, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 1), 18, 14, 7, skip, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, 0), 18, 14, 8, skip, player)

            if skip >= 0:
                self.uint8(skip)
                self.uint8(0xFF)
                
        elif oldPos[2]-1 > 7: # Still underground
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]-3), 18, 14, oldPos[2]+3, -1, player)
            
            if skip >= 0:
                self.uint8(skip)
                self.uint8(0xFF)
                
        self.uint8(0x68) # West
        self.mapDescription((oldPos[0] - 8, oldPos[1] + 1 - 6, oldPos[2]-1), 1, 14, player)
        
        self.uint8(0x65) # North
        self.mapDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]-1), 18, 1, player)
        
        
    def moveDownPlayer(self, player, oldPos):
        self.uint8(0xBF)
        if oldPos[2]+1 == 8:
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]+1), 18, 14, -1, -1, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]+2), 18, 14, -2, skip, player)
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]+3), 18, 14, -3, skip, player)

            if skip >= 0:
                self.uint8(skip)
                self.uint8(0xFF)
                
        elif oldPos[2]+1 > 8:
            skip = self.floorDescription((oldPos[0] - 8, oldPos[1] - 6, oldPos[2]+3), 18, 14, oldPos[2]-3, -1, player)
            
            if skip >= 0:
                self.uint8(skip)
                self.uint8(0xFF)            
        
        self.uint8(0x66) # East
        self.mapDescription((oldPos[0] + 9, oldPos[1] - 6, oldPos[2]+1), 1, 14, player)
        self.uint8(0x67) # South
        self.mapDescription((oldPos[0] - 8, oldPos[1] + 7, oldPos[2]+1), 18, 1, player)
        
    def updateTileItem(self, pos, stackpos, item):
        self.uint8(0x6B)
        self.position(pos)
        self.uint8(stackpos)
        self.item(item)
        
    def removeTileItem(self, pos, stackpos):
        self.uint8(0x6C)
        self.position(pos)
        self.uint8(stackpos)
        
    def status(self, player):
        self.uint8(0xA0)
        self.uint16(player.data["health"])
        self.uint16(player.data["healthmax"])
        self.uint32(player.data["capasity"] * 100) # TODO: Free Capasity
        self.uint32(player.data["capasity"] * 100) # TODO: Cap
        self.uint64(player.data["experience"]) # TODO: Virtual cap? Experience
        if player.data["level"] > 0xFFFF:
            self.uint16(0xFFFF)
        else:
            self.uint16(player.data["level"]) # TODO: Virtual cap? Level
        self.uint8(math.ceil(float(config.levelFormula(player.data["level"]+1)) / player.data["experience"])) # % to next level, TODO
        self.uint16(player.data["mana"]) # mana
        self.uint16(player.data["manamax"]) # mana max
        self.uint8(player.data["maglevel"]) # TODO: Virtual cap? Manalevel
        self.uint8(1) # TODO: Virtual cap? ManaBase
        self.uint8(0) # % to next level, TODO
        self.uint8(player.data["soul"]) # TODO: Virtual cap? Soul
        self.uint16(min(42 * 60, player.data["stamina"] / 60)) # Stamina minutes
        self.uint16(player.speed) # Speed
        
        self.uint16(0x00) # Condition

    def skills(self, player):
        self.uint8(0xA1) # Skill type
        for x in xrange(game.enum.SKILL_FIRST, game.enum.SKILL_LAST+1):
            self.uint8(player.skills[x]) # Value / Level
            self.uint8(1) # Base
            self.uint8(0) # %
            
class BaseProtocol(object):
    Packet = BasePacket
    def handle(self, player, packet):
        packetType = packet.uint8()

        if packetType == 0x14 or player.data["health"] < 1: # Logout
            player.client.transport.loseConnection()
            
        elif packetType == 0x1E: # Keep alive
            player.pong()
            
        elif packetType == 0xA0: # Set modes
            player.setModes(packet.uint8(), packet.uint8(), packet.uint8())
            
        elif packetType in (0x6F, 0x70, 0x71, 0x72): # Turn packages
            player.turn(packetType - 0x6F)
            
        elif packetType == 0x64: # movement with multiple steps
            self.handleAutoWalk(player,packet)
    
        elif packetType == 0x69: # Stop autowalking
            player.stopAutoWalk()
            
        elif packetType in (0x65, 0x66, 0x67, 0x68): # Movement
            self.handleWalk(player,packetType - 0x65)
        
        elif packetType == 0x6A: # Northeast
            self.handleWalk(player,7)
            
        elif packetType == 0x6B: # Southeast
            self.handleWalk(player,5)

        elif packetType == 0x6C: # Northwest
            self.handleWalk(player,4)
            
        elif packetType == 0x6D: # Southwest
            self.handleWalk(player,6)
            
        elif packetType == 0x96: # Say
            self.handleSay(player,packet)
            
        elif packetType == 0x78: # Throw/move item
            self.handleMoveItem(player,packet)
        
        elif packetType == 0x79: # Look at in trade window
            self.handleLookAtTrade(player,packet)
            
        elif packetType == 0x7A: # Player brought from store
            self.handlePlayerBuy(player,packet)
            
        elif packetType == 0x7B: # Player sold to store
            self.handlePlayerSale(player,packet)
        
        elif packetType == 0x80: # Player close trade
            player.closeTrade()
            
        elif packetType == 0x82:
            self.handleUse(player,packet)

        elif packetType == 0x83:
            self.handleUseWith(player,packet)
            
        elif packetType == 0x85: # Rotate item
            self.handleRotateItem(player,packet)
            
        elif packetType == 0x87: # Close container
            player.closeContainerId(packet.uint8())
            
        elif packetType == 0x88: # Arrow up container
            player.arrowUpContainer(packet.uint8())
        
        elif packetType == 0x89: # Text from textWindow
            self.handleWriteBack(player,packet)
            
        elif packetType == 0x97: # Request channels
            player.openChannels()

        elif packetType == 0x98: # Open channel
            player.openChannel(packet.uint16())
            
        elif packetType == 0x99: # Close channel
            player.closeChannel(packet.uint16())
            
        elif packetType == 0x8C: # Look at
            self.handleLookAt(player,packet)
        
        elif packetType == 0xA1: # Attack
            self.handleAttack(player,packet)

        elif packetType == 0xA2: # Attack
            self.handleFollow(player,packet)
            
        elif packetType == 0xCA:
            self.handleUpdateContainer(player,packet)
            
        elif packetType == 0xD2: # Request outfit
            player.outfitWindow()
            
        elif packetType == 0xD3: # Set outfit
            self.handleSetOutfit(player,packet)
        
        elif packetType == 0xD4: # Set mount status
            self.handleSetMounted(player,packet)
            
        elif packetType == 0xBE: # Stop action
            player.stopAction()
            
        else:
            log.msg("Unhandled packet (type = {0}, length: {1}, content = {2})".format(hex(packetType), len(packet.data), ' '.join( map(str, map(hex, map(ord, packet.getData())))) ))
            #self.transport.loseConnection()
            
    def handleSay(self, player, packet):
        channelType = packet.uint8()
        channelId = 0
        reciever = ""
        if channelType in (enum.MSG_CHANNEL_MANAGEMENT, enum.MSG_CHANNEL, enum.MSG_CHANNEL_HIGHLIGHT):
            channelId = packet.uint16()
        elif channelType in (enum.MSG_PRIVATE_TO, enum.MSG_GAMEMASTER_PRIVATE_TO):
            reciever = packet.string()

        text = packet.string()

        player.handleSay(channelType, channelId, reciever, text)
        
    def handleAutoWalk(self, player, packet):
        if player.target:
            player.target = None
        player.stopAction()    
        steps = packet.uint8()

        walkPattern = deque()
        for x in xrange(0, steps):
            direction = packet.uint8()
            if direction == 1:
                walkPattern.append(1) # East
            elif direction == 2:
                walkPattern.append(7) # Northeast
            elif direction == 3:
                walkPattern.append(0) # North
            elif direction == 4:
                walkPattern.append(6) # Northwest          
            elif direction == 5:
                walkPattern.append(3) # West
            elif direction == 6:
                walkPattern.append(4) # Southwest
            elif direction == 7:
                walkPattern.append(2) # South
            elif direction == 8:
                walkPattern.append(5) # Southeast           
            else:
                continue # We don't support them
                
        game.engine.autoWalkCreature(player, walkPattern)

    def handleWalk(self, player, direction):
        game.engine.autoWalkCreature(player, deque([direction]))
            
    @deferredGenerator
    def handleMoveItem(self, player, packet):
        from game.item import Item, sid, items
        fromPosition = packet.position()
        fromMap = False
        toMap = False
        if fromPosition[0] != 0xFFFF:
            # From map
            fromMap = True
        
        clientId = packet.uint16()
        fromStackPos = packet.uint8()
        toPosition = packet.position()
        if toPosition[0] != 0xFFFF:
            toMap = True
           
        count = packet.uint8()
        oldItem = None
        renew = False
        stack = True
        
        isCreature = False
        if clientId < 100:
            isCreature = True
        if not isCreature:
            # Remove item:
            currItem = player.findItemWithPlacement(toPosition)

            """if currItem and currItem[1] and not ((currItem[1].stackable and currItem[1].itemId == sid(clientId)) or currItem[1].containerSize):
                currItem[1] = None
            """
            if fromMap:
                
                walkPattern = game.engine.calculateWalkPattern(player.position, fromPosition, -1)
                if len(walkPattern):
                    def sleep(seconds):
                        d = Deferred()
                        reactor.callLater(seconds, d.callback, seconds)
                        return d
                    
                    walking = [True]
                    game.engine.autoWalkCreature(player, deque(walkPattern), lambda: walking.pop())
                    while walking:
                        yield waitForDeferred(sleep(0.05))
                            
                    
                stream = TibiaPacket()
                oldItem = player.findItemWithPlacement(fromPosition, fromStackPos)

                # Before we remove it, can it be placed there?
                if toPosition[0] == 0xFFFF and toPosition[1] < 64 and toPosition[1] not in (game.enum.SLOT_DEPOT, game.enum.SLOT_AMMO) and toPosition[1] != game.enum.SLOT_BACKPACK and toPosition[1] != oldItem[1].slotId():
                    player.notPossible()
                    return
                    
                if oldItem[1].stackable and count < 100:
                    renew = True
                    oldItem[1].reduceCount(count)
                    if oldItem[1].count:
                        stream.updateTileItem(fromPosition, fromStackPos, oldItem[1])
                    else:
                        stream.removeTileItem(fromPosition, fromStackPos)
                        game.map.getTile(fromPosition).removeItem(oldItem[1])
                else:
                    stream.removeTileItem(fromPosition, fromStackPos)
                    game.map.getTile(fromPosition).removeClientItem(clientId, fromStackPos)
                stream.sendto(game.engine.getSpectators(fromPosition))
                
            else:
                stream = TibiaPacket()
                        
                oldItem = player.findItemWithPlacement(fromPosition)
                
                # Before we remove it, can it be placed there?
                if toPosition[0] == 0xFFFF and toPosition[1] < 64 and toPosition[1] not in (game.enum.SLOT_DEPOT, game.enum.SLOT_AMMO) and toPosition[1] != game.enum.SLOT_BACKPACK and toPosition[1] != oldItem[1].slotId():
                    player.notPossible()
                    return
                    
                if oldItem[1].stackable and count < 100:
                    renew = True
                    oldItem[1].count -= count
                    if oldItem[1].count > 0:
                        if oldItem[0] == 1:
                            stream.addInventoryItem(fromPosition[1], oldItem[1])
                        elif oldItem[0] == 2:
                            stream.updateContainerItem(player.openContainers.index(oldItem[2]), fromPosition[2], oldItem[1])
                    else:
                        if oldItem[0] == 1:
                            player.inventory[fromPosition[1]-1] = None
                            stream.removeInventoryItem(fromPosition[1])
                        elif oldItem[0] == 2:
                            oldItem[2].container.removeItem(oldItem[1])
                            stream.removeContainerItem(player.openContainers.index(oldItem[2]), fromPosition[2])
                else:
                    if oldItem[0] == 1:
                        player.inventory[fromPosition[1]-1] = None
                        stream.removeInventoryItem(fromPosition[1])
                    elif oldItem[0] == 2:
                        oldItem[2].container.removeItem(oldItem[1])
                        stream.removeContainerItem(player.openContainers.index(oldItem[2]), fromPosition[2])
                
                if toPosition[1] == fromPosition[1]:
                    stack = False
                    
                stream.send(player.client)
            if toMap:
                stream = TibiaPacket()
                if renew:
                    newItem = Item(sid(clientId), count)
                else:
                    newItem = oldItem[1]
                findItem = game.map.getTile(toPosition).findClientItem(clientId, True) # Find item for stacking
                if findItem and newItem.stackable and count < 100 and findItem[1].count + count <= 100:
                    newItem.count += findItem[1].count
                    stream.removeTileItem(toPosition, findItem[0])
                    game.map.getTile(toPosition).removeItem(findItem[1])
                    
                toStackPos = game.map.getTile(toPosition).placeItem(newItem)
                stream.addTileItem(toPosition, toStackPos, newItem )
                
                if not renew and newItem.containerSize and newItem.opened:
                    player.closeContainer(newItem)
                stream.sendto(game.engine.getSpectators(toPosition))

            else:
                
                if currItem and currItem[1] and currItem[1].containerSize:
                    ret = player.itemToContainer(currItem[1], Item(sid(clientId), count) if renew else oldItem[1], count=count, stack=stack)

                elif currItem and (currItem[0] == 2) and not currItem[1] and currItem[2]:
                    ret = player.itemToContainer(currItem[2], Item(sid(clientId), count) if renew else oldItem[1], count=count, stack=stack)
                else:
                    stream = TibiaPacket()
                    if toPosition[1] < 64:
                        if oldItem[1].stackable and player.inventory[toPosition[1]-1] and player.inventory[toPosition[1]-1].itemId == sid(clientId) and (player.inventory[toPosition[1]-1].count + count <= 100):
                            player.inventory[toPosition[1]-1].count += count
                        else:       
                            player.inventory[toPosition[1]-1] = Item(sid(clientId), count) if renew else oldItem[1]
                        stream.addInventoryItem(toPosition[1], player.inventory[toPosition[1]-1])
                    else:
                        container = player.getContainer(toPosition[1]-64)
                        try:
                            container.container.items[toPosition[2]] = Item(sid(clientId), count) if renew else oldItem[1]
                            stream.updateContainerItem(toPosition[1]-64, toPosition[2], container.container.items[toPosition[2]])
                        except:
                            player.itemToContainer(container, Item(sid(clientId), count) if renew else oldItem[1], count=count, stack=stack, streamX=stream)                  
                    if renew and currItem and currItem[1]:
                        if fromPosition[1] < 64:
                            player.inventory[fromPosition[1]-1] = currItem[1]
                            stream.addInventoryItem(fromPosition[1], player.inventory[fromPosition[1]-1])
                        else:
                            player.itemToContainer(player.inventory[2], currItem[1])

                    stream.send(player.client)
        else:
            if game.map.getTile(toPosition).creatures():
                player.notEnoughRoom()
                return
                
            creature = game.map.getTile(fromPosition).getThing(fromStackPos) 
            toTile = game.map.getTile(toPosition)
            for i in toTile.getItems():
                if i.solid:
                    player.notPossible()
                    return
            if abs(creature.position[0]-player.position[0]) > 1 or abs(creature.position[1]-player.position[1]) > 1:
                walkPattern = game.engine.calculateWalkPattern(creature.position, toPosition)
                if len(walkPattern) > 1:
                    player.outOfRange()
                else:
                    game.engine.autoWalkCreatureTo(player, creature.position, -1, True, lambda: game.engine.autoWalkCreature(creature, deque(walkPattern)))
            else:
                game.engine.autoWalkCreatureTo(creature, toPosition)
            
    def handleLookAt(self, player, packet):
        from game.item import sid, cid, items
        position = packet.position()
        print "Look at"
        print position
            
        clientId = packet.uint16()
        stackpos = packet.uint8()

        thing = player.findItem(position, stackpos)     
        
        if thing:
            if isinstance(thing, game.item.Item):
                def afterScript():
                    extra = ""
                    # TODO propper description handling
                    if config.debugItems:
                        extra = "(ItemId: %d, Cid: %d)" % (thing.itemId, clientId)
                    player.message(thing.description() + extra, game.enum.MSG_INFO_DESCR)
            elif isinstance(thing, Creature):
                def afterScript():
                    if self == thing:
                        player.message(thing.description(True), game.enum.MSG_INFO_DESCR)
                    else:
                        player.message(thing.description(), game.enum.MSG_INFO_DESCR)
            game.scriptsystem.get('lookAt').run(thing, self, afterScript, position=position, stackpos=stackpos)
        else:
            player.notPossible()

    def handleLookAtTrade(self, player, packet):
        from game.item import sid
        clientId = packet.uint16()
        count = packet.uint8()
        
        item = game.item.Item(sid(clientId), count)
        player.message(item.description(), game.enum.MSG_INFO_DESCR)
        del item
        
    def handleRotateItem(self, player, packet):
        position = packet.position() # Yes, we don't support backpack rotations
        clientId = packet.uint16()
        stackpos = packet.uint8()
        
        # TODO: WalkTo
        item = game.map.getTile(position).getThing(stackpos)
        game.engine.transformItem(item, item.rotateTo, position, stackpos)
        
    def handleSetOutfit(self, player, packet):
        player.outfit = [packet.uint16(), packet.uint8(), packet.uint8(), packet.uint8(), packet.uint8()]
        player.addon = packet.uint8()
        player.mount = packet.uint16() # Not really supported
        player.refreshOutfit()
    
    def handleSetMounted(self, player, packet):
        if player.mount:
            mount = packet.uint8() != 0
            player.changeMountStatus(mount)
        else:
            player.outfitWindow()
            
    def handleUse(self, player, packet):
        position = packet.position()

        clientId = packet.uint16() # Junk I tell you :p
        stackpos = packet.uint8()
        index = packet.uint8()
        thing = player.findItem(position, stackpos)

        if thing:
            game.scriptsystem.get('use').run(thing, self, None, position=position, stackpos=stackpos, index=index)

    def handleUseWith(self, player, packet):
        game.engine.explainPacket(packet)
        position = packet.position()
        clientId = packet.uint16() # Junk I tell you :p
        stackpos = packet.uint8()
        
        onPosition = packet.position()
        onId = packet.uint16()
        onStack = packet.uint8()
        
        thing = player.findItem(position, stackpos)
        
        if thing:
            game.scriptsystem.get('useWith').run(thing, self, None, position=position, stackpos=stackpos, onPosition=onPosition, onId=onId, onStackpos=onStack)

    def attackTarget(self):
        if player.target and player.inRange(player.target.position, 1, 1):
            if not player.inventory[5]:
                player.message("Fist is not supported, targetcheck failed!")
            else:
                
                if not player.target.data["health"]:
                    player.target = None
                else:
                    dmg = -1 * random.randint(0, round(config.meleeDamage(player.inventory[5].attack, 1, player.data["level"], 1)))
                    player.target.onHit(player, dmg, game.enum.PHYSICAL)
                
                
        if player.target:        
            player.targetChecker = reactor.callLater(config.meleeAttackSpeed, player.attackTarget)
                
    def handleAttack(self, player, packet):
        cid = packet.uint32()
        print "CreatureID %d" %  cid
        if player.targetMode == 1:
            player.targetMode = 0
            player.target = None
            try:
                player.targetChecker.cancel()
            except:
                pass
            return
            
        if cid in allCreatures:
            player.target = allCreatures[cid]
            player.targetMode = 1
        else:
            player.notPossible()
            
        if player.modes[1] == game.enum.CHASE:
            game.engine.autoWalkCreatureTo(player, player.target.position, -1, True)
            player.target.scripts["onNextStep"].append(player.__followCallback)

        try:
            player.targetChecker.cancel()
        except:
            pass        
        player.attackTarget()
        
    def __followCallback(self, player, who):
        if player.target == who:
            game.engine.autoWalkCreatureTo(player, player.target.position, -1, True)
            player.target.scripts["onNextStep"].append(player.__followCallback)
            
    def handleFollow(self, player, packet):
        cid = packet.uint32()
        
        if player.targetMode == 2:
            player.targetMode = 0
            player.target = None
            return
            
        if cid in allCreatures:
            player.target = allCreatures[cid]
            player.targetMode = 2
            game.engine.autoWalkCreatureTo(player, player.target.position, -1, True)
            player.target.scripts["onNextStep"].append(player.__followCallback)
        else:
            player.notPossible()

    def handleUpdateContainer(self, player, packet):
        openId = packet.uint8()
        
        parent = False
        try:
            parent = bool(container.parent)
        except:
            pass
        player.openContainer(player.openContainers[openId], parent=parent, update=True)
        
    def handlePlayerBuy(self, player, packet):
        from game.item import sid
        if not player.openTrade:
            return
            
        clientId = packet.uint16()
        count = packet.uint8()
        amount = packet.uint8()
        ignoreCapasity = packet.uint8()
        withBackpack = packet.uint8()
        
        player.openTrade.buy(player, sid(clientId), count, amount, ignoreCapasity, withBackpack)
        
    def handlePlayerSale(self, player, packet):
        from game.item import sid
        if not player.openTrade:
            return
            
        clientId = packet.uint16()
        count = packet.uint8()
        amount = packet.uint8()
        ignoreEquipped = packet.uint8() 
        
        player.openTrade.sell(player, sid(clientId), count, amount, ignoreEquipped)

    def handleWriteBack(self, player, packet):
        windowId = packet.uint32()
        text = packet.string()
        
        if windowId in player.windowHandlers:
            player.windowHandlers[windowId](text)
            