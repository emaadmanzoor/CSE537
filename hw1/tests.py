import unittest
import readGame
import pegSolitaireUtils

class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        game = pegSolitaireUtils.game('./game.txt')
        print 'Testing with game:'
        print game

    def setUp(self):
        self.game = pegSolitaireUtils.game('./game.txt')

    def test_is_corner(self):
        self.assertTrue(self.game.is_corner((0,0)))
        self.assertFalse(self.game.is_corner((4,0)))

    def test_get_next_position(self):
        self.assertEqual((0,2), self.game.getNextPosition((0,0), 'E'))
        self.assertEqual((2,1), self.game.getNextPosition((0,1), 'S'))
        self.assertEqual((1,0), self.game.getNextPosition((1,2), 'W'))
        self.assertEqual((0,0), self.game.getNextPosition((2,0), 'N'))

    def test_is_valid_move(self):
        self.assertFalse(self.game.is_validMove((1,3), 'E'))
        self.assertFalse(self.game.is_validMove((1,3), 'S'))
        self.assertFalse(self.game.is_validMove((0,0), 'S'))
        self.assertFalse(self.game.is_validMove((2,0), 'W'))
        self.assertTrue(self.game.is_validMove((2,3), 'E'))

    def test_get_next_state(self):
        print '(2,3) E'
        newState = self.game.getNextState((2,3), 'E')
        print self.game

        print '(4,3) N'
        newState = self.game.getNextState((4,3), 'N')
        print self.game

        print '(2,2) E'
        newState = self.game.getNextState((2,2), 'E')
        print self.game

        print '(2,5) W'
        newState = self.game.getNextState((2,5), 'W')
        print self.game

        print '(1,3) S'
        newState = self.game.getNextState((1,3), 'S')
        print self.game

        self.assertEqual(self.game.gameState,
                         [[-1, -1, 0, 0, 0, -1, -1],
                          [-1, -1, 0, 0, 0, -1, -1],
                          [ 0,  0, 0, 0, 0,  0,  0],
                          [ 0,  0, 0, 1, 0,  0,  0],
                          [ 0,  0, 0, 0, 0,  0,  0],
                          [-1, -1, 0, 0, 0, -1, -1],
                          [-1, -1, 0, 0, 0, -1, -1]])

if __name__ == "__main__":
    unittest.main()
