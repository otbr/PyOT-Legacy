from twisted.internet.defer import waitForDeferred, deferredGenerator
import sql, copy
from twisted.python import log
from collections import deque
import game.enum

items = {}
reverseItems = {}

### Container class ###
class Container(object):
    def __init__(self, size):
        self.items = deque()
        self.maxSize = size
        
    def placeItem(self, item):
        length = len(self.items)
        if length < self.maxSize:
            self.items.appendleft(item)
            return 0
        else:
            return None

    def placeItemRecursive(self, item):
        length = len(self.items)
        if length < self.maxSize:
            self.items.appendleft(item)
            return 0
        else:
            for itemX in self.items:
                if itemX.containerSize:
                    if itemX.container.placeItemRecursive(item) == 0:
                        return itemX

    def removeItem(self, item):
        return self.items.remove(item)
        
    def getThing(self, pos):
        try:
            return self.items[pos]
        except:
            return None
            
    def findSlot(self, item):
        return self.items.index(item)
        
### Item ###
class Item(object):
    def __init__(self, itemid, count=None):
        self.itemId = itemid
        self.count = count if self.stackable else None
        
        
        # Extend items such as containers, beds and doors
        if "containerSize" in self.attributes():
            self.container = Container(self.containerSize)
            
    def __getattr__(self, name):
        if name in items[self.itemId]:
            return items[self.itemId][name]
        elif not "__" in name:
            return None
        raise AttributeError, name
        
    def name(self):
        if self.count > 1 and "plural" in items[self.itemId]:
            return (items[self.itemId]["article"]+" " if items[self.itemId]["article"]+" " else "") + items[self.itemId]["plural"]
        else:
            return (items[self.itemId]["article"]+" " if items[self.itemId]["article"]+" " else "") + items[self.itemId]["name"]
            
    def attributes(self):
        return items[self.itemId]
        
    def reduceCount(self, count):
        self.count -= count
        if self.count <= 0:
            pass # TODO: remove
            
    def slotId(self):
        if not self.slotType:
            return None
        else:
            if self.slotType == "head":
                return game.enum.SLOT_HEAD
            elif self.slotType == "necklace":
                return game.enum.SLOT_NECKLACE
            elif self.slotType == "backpack":
                return game.enum.SLOT_BACKPACK
            elif self.slotType == "body":
                return game.enum.SLOT_ARMOR
            elif self.slotType == "two-handed":
                return game.enum.SLOT_LEFT
            elif self.slotType == "legs":
                return game.enum.SLOT_LEGS
            elif self.slotType == "feet":
                return game.enum.SLOT_FEET
            elif self.slotType == "ring":
                return game.enum.SLOT_RING
            elif self.slotType == "ammo":
                return game.enum.SLOT_AMMO
            else:
                if self.weaponType:
                    return game.enum.SLOT_LEFT if self.weaponType in ('sword', 'rod', 'ward') else game.enum.SLOT_RIGHT
                else:
                    return None
def cid(itemid):
    try:
        return items[itemid]["cid"]
    except:
        return None

def sid(itemid):
    try:
        return reverseItems[itemid]
    except:
        return None
        
            
@deferredGenerator
def loadItems():
    log.msg("Loading items...")
    
    global items
    global reverseItems

    # Async SQL (it's funny isn't it?)
    d = waitForDeferred(sql.conn.runQuery("SELECT sid,cid,name,`type`,plural,article,subs,speed,solid,blockprojectile,blockpath,usable,pickable,movable,stackable,ontop,hangable,rotatable,animation FROM items"))
    d2 = waitForDeferred(sql.conn.runQuery("SELECT sid, `key`, `value` FROM item_attributes"))
    yield d
    yield d2

    result = d.getResult()
    result2 = d2.getResult()
    
    # Make two new values while we are loading
    loadItems = {}
    reverseLoadItems = {}


    for item in result:
        item["cid"] = int(item["cid"]) # no long
        item["sid"] = int(item["sid"]) # no long
        item["speed"] = int(item["speed"]) # No long
        item["type"] = int(item["type"]) # No long
        item["subs"] = int(item["subs"]) # No long
        if not item["speed"]:
            del item["speed"]
        if not item["type"]:
            del item["type"]
        if not item["subs"]:
            del item["subs"]            
        for key in copy.copy(item):
            if key in ('solid','blockprojectile','blockpath','usable','pickable','movable','stackable','ontop','hangable','rotatable','animation'):
                if bool(item[key]):
                    item[key] = True
                else:
                    del item[key]
                    
        reverseLoadItems[item["cid"]] = copy.copy(item["sid"])
        
        loadItems[reverseLoadItems[item["cid"]]] = item
        if "subs" in item:
            for x in xrange(1, item["subs"]+1):
                newItem = copy.copy(item)
                newItem["cid"] = item["cid"]+x
                reverseLoadItems[newItem["cid"]] = item["sid"]+x
                del newItem["sid"]
                loadItems[reverseLoadItems[newItem["cid"]]] = newItem
            
        del item["sid"] # Unneeded

    for data in result2:
        if data["key"] == "fluidSource":
            val = getattr(game.enum, 'FLUID_'+data["value"].upper())
        elif data["key"] == "floorChange":
            val = game.enum.FLOORCHANGE_DOWN if data["value"]=="down" else game.enum.FLOORCHANGE_UP
        else:
            val = game.engine.autoCastValue(data["value"])
        if val:
            loadItems[data["sid"]][data["key"]] = val
            
    log.msg("%d Items loaded" % len(loadItems))
    
    # Replace the existing items
    items = loadItems
    reverseItems = reverseLoadItems
    
    
    
