from twisted.trial import unittest
import time
import sys
sys.path.insert(0, '.')
sys.path.insert(1, 'core')

import config

import game.engine
import game.map
import game.errors
from twisted.internet import reactor, threads, defer

startTime = time.time()

# Turn off looper call.
game.engine.looper = lambda x,y: x()

game.engine.loader(startTime)

# Clear reactor
for i in reactor.getDelayedCalls():
    i.cancel()

#### The tests ####

### Packet ###
class Packet(unittest.TestCase):
    def test_uint8(self):
        import packet
        p = packet.TibiaPacket()
        p.uint8(255)
        p.uint8(0)

        self.assertEqual(ord(p.bytes[0]), 255)
        self.assertEqual(ord(p.bytes[1]), 0)

### Engine ###
class GameEngine(unittest.TestCase):
    def test_getSpectators(self):
        # Without players
        self.assertEqual(game.engine.getSpectators([100,100,7]), set())

        # TODO: With players

    def test_getPlayers(self):
        # Without players
        self.assertEqual(game.engine.getPlayers([100,100,7]), set())

        # TODO: With players

    def test_getCreatures(self):
        # Without players
        self.assertEqual(game.engine.getCreatures([100,100,7]), set())

        # TODO: With map sectors / creatures loaded
        
    def test_getSpectators_tuple(self):
        # Without players
        self.assertEqual(game.engine.getSpectators((100,100,7)), set())

        # TODO: With players

    def test_getPlayers_tuple(self):
        # Without players
        self.assertEqual(game.engine.getPlayers((100,100,7)), set())

        # TODO: With players

    def test_getCreatures_tuple(self):
        # Without players
        self.assertEqual(game.engine.getCreatures((100,100,7)), set())

        # TODO: With map sectors / creatures loaded

class PositionClass(unittest.TestCase):
    def setUp(self):
        self.pos = game.map.Position(1,2,3)
        self.pos2 = game.map.Position(1,2,3)
        self.pos3 = game.map.Position(2,3,4)
        
    def test_values(self):
        self.assertEqual(self.pos.x, 1)
        self.assertEqual(self.pos.y, 2)
        self.assertEqual(self.pos.z, 3)
        
        
    def test_equality(self):    
        self.assertEqual(pos, pos2)
        self.assertNotEqual(pos, pos3)
        
    def test_outofrange(self):
        self.assertRaises(game.errors.PositionOutOfRange, game.map.position, 0xFFFF+1, 0xFFFF, 15)
        self.assertRaises(game.errors.PositionOutOfRange, game.map.position, 0xFFFF, 0xFFFF+1, 15)
        self.assertRaises(game.errors.PositionOutOfRange, game.map.position, 0xFFFF, 0xFFFF, 16)
        
    def test_changeOutOfRange(self):
        with self.assertRaises(game.errors.PositionOutOfRange):
            game.map.Position(1,2,3).x += 0xFFFF
            
    def test_negative(self):
        self.assertRaises(game.errors.PositionNegative, game.map.position, -1, 0xFFFF, 15)
        self.assertRaises(game.errors.PositionNegative, game.map.position, 0xFFFF, -1, 15)
        self.assertRaises(game.errors.PositionNegative, game.map.position, 0xFFFF, 0xFFFF, -1)
        
    def test_changeNegative(self):
        with self.assertRaises(game.errors.PositionNegative):
            game.map.Position(1,2,3).x -= 0xFFFF        