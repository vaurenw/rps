# test_module.py

import unittest
from RPS_game import play, mrugesh, abbey, quincy, kris
from RPS import player

class UnitTests(unittest.TestCase):
    def test_player_vs_quincy(self):
        print("\nTesting against Quincy...")
        self.assertTrue(play(player, quincy, 1000) >= 60)

    def test_player_vs_abbey(self):
        print("\nTesting against Abbey...")
        self.assertTrue(play(player, abbey, 1000) >= 60)

    def test_player_vs_kris(self):
        print("\nTesting against Kris...")
        self.assertTrue(play(player, kris, 1000) >= 60)

    def test_player_vs_mrugesh(self):
        print("\nTesting against Mrugesh...")
        self.assertTrue(play(player, mrugesh, 1000) >= 60)

if __name__ == "__main__":
    unittest.main()
