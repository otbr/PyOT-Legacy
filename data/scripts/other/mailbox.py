mailboxes = (2593,)

def parseText(text):
    lines = text.split("\n")
    if lines >= 2:
        townId = townNameToId(lines[1])
        if townId:
            return (lines[0], townId)

# When we're working with IO blocking behavior such as SQL (which might be needed in case of placeInDepot) we are required to use callbacks to deal with result)
@inlineCallbacks        
def onSend(creature, position, thing, onId, onThing, **k):
    # Is it a letter perhaps?
    if onId == ITEM_LETTER:
        if not onThing.text:
            creature.message("To whom shall this letter be sent?", onPos=position)
            return
        parse = parseText(onThing.text)
        
        if not parse:
            creature.message("Did you spell it right?", onPos=position)
            
        onThing.itemId = ITEM_LETTER_STAMPED # We need to change the Id before the placeInDepot takes place in case the player is offline, the data is saved right away
        result = yield engine.placeInDepot(parse[0], parse[1], onThing)
        
        if not result:
            onThing.itemId = ITEM_LETTER # Convert the item back to it's original Id
            creature.message("Did you spell it right?", onPos=position)
            return
        else:
            returnValue(False) # (equal to return False in other, regular scripts)
    elif onId == ITEM_PARCEL:
        found = None
        for item in onThing.container.items:
            if item.itemId == ITEM_LABEL:
                found = item
                break
                
        if not found or not found.text:
            creature.message("To whom shall this parcel be sent?", onPos=position)
            return            

        parse = parseText(found.text)

        if not parse:
            creature.message("Did you spell it right?", onPos=position)
            
        onThing.itemId = ITEM_PARCEL_STAMPED
        result = yield engine.placeInDepot(parse[0], parse[1], onThing)

        if not result:
            onThing.itemId = ITEM_PARCEL # Convert the item back to it's original Id
            creature.message("Did you spell it right?", onPos=position)
            return
        else:
            returnValue(False) # (equal to return False in other, regular scripts)
            
reg('useWith', mailboxes, onSend)