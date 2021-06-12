import unittest
import orion


class MyTestCase(unittest.TestCase):

    def test_default_game(self):
        manager = orion.OrionManager()
        game = manager.root
        game.boot()

    def test_game_subclass(self):

        class MyGame(orion.Game):
            pass

        manager = orion.OrionManager(MyGame)
        my_game = manager.root
        my_game.boot()
        assert isinstance(my_game, orion.Game)


if __name__ == '__main__':
    unittest.main()
