import unittest
from game.shakki import Shakki


class TestShakki(unittest.TestCase):

    def setUp(self):
        self.peli = Shakki()

    def test_shakki_exists(self):
        self.assertNotEqual(self.peli, None)

    def test_start_with_white_to_move(self):
        self.assertEqual(self.peli.whitetomove, True)

    def test_shakki_has_board(self):
        self.assertNotEqual(self.peli.lauta, None)

    def test_move_out_of_turn_black(self):
        self.assertEqual(self.peli.check_move_legality(1, 0, 1, 0), False)

    def test_move_with_specified_parameters_returns_correct_value_with_different_mover(self):
        self.assertEqual(self.peli.check_move_legality(
            1, 0, 1, 0, self.peli.lauta, False), True)
        self.assertEqual(self.peli.check_move_legality(
            0, 0, 1, 0, self.peli.lauta, False), False)
        self.assertEqual(self.peli.check_move_legality(
            0, 1, 2, 1, self.peli.lauta, False), True)
        self.assertEqual(self.peli.check_move_legality(
            0, 2, 1, 1, self.peli.lauta, False), False)
        self.assertEqual(self.peli.check_move_legality(
            0, 3, 1, 1, self.peli.lauta, False), False)
        self.assertEqual(self.peli.check_move_legality(
            0, 4, 1, 1, self.peli.lauta, False), False)

    def test_change_mover_passes_turn(self):
        self.peli.change_mover()
        self.assertEqual(self.peli.whitetomove, False)
        self.peli.change_mover()
        self.assertEqual(self.peli.whitetomove, True)

    def test_move_out_of_turn_white(self):
        self.peli.change_mover()
        self.assertEqual(self.peli.check_move_legality(6, 0, -1, 0), False)

    def test_trying_to_move_empty_square_returns_false(self):
        self.assertNotEqual(self.peli.check_move_legality(4, 4, 1, 1), True)

    def test_trying_to_move_empty_square_does_not_change_mover(self):
        self.peli.check_move_legality(4, 4, 1, 1)
        self.assertEqual(self.peli.whitetomove, True)

    # pawn moves white
    def test_two_pace_pawn_move_to_empty_square_white(self):
        self.assertEqual(self.peli.check_move_legality(6, 0, -2, 0), True)

    def test_one_pace_pawn_move_to_empty_square_white(self):
        self.assertEqual(self.peli.check_move_legality(6, 0, -1, 0), True)

    def test_pawn_capture_opposing_pieces_white(self):
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                                 [-1, -1, -1, -1, -1, -1, -1, -1],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, item, 0, 0, 0, 0, 0, 0],
                                 [1, 0, 0, 1, 1, 1, 1, 1],
                                 [0, 0, 0, 6, 7, 4, 3, 5]])
            self.assertEqual(self.peli.check_move_legality(6, 0, -1, 1), True)

    def test_pawn_move_to_occupied_square_white(self):
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 0, -3, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(6, 0, -2, 0), False)
        self.assertEqual(self.peli.check_move_legality(6, 2, -2, 0), False)

    def test_pawn_move_two_squares_having_already_moved_white(self):
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(5, 0, 2, 0), False)

    # pawn moves black
    def test_two_pace_pawn_move_to_empty_square_black(self):
        self.peli.change_mover()
        self.assertEqual(self.peli.check_move_legality(1, 0, 2, 0), True)

    def test_one_pace_pawn_move_to_empty_square_black(self):
        self.peli.change_mover()
        self.assertEqual(self.peli.check_move_legality(1, 0, 1, 0), True)

    def test_pawn_capture_opposing_pieces_black(self):
        self.peli.change_mover()
        for item in set(self.peli.lauta[6]+self.peli.lauta[7]):
            self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                                 [-1, 0, 0, -1, -1, -1, -1, -1],
                                 [0, item, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [1, 1, 1, 1, 1, 1, 1, 1],
                                 [5, 3, 4, 6, 7, 4, 3, 5]])
            self.assertEqual(self.peli.check_move_legality(1, 0, 1, 1), True)

    def test_pawn_capture_on_empty_square_black(self):
        self.peli.change_mover()
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                             [-1, 0, 0, -1, -1, -1, -1, -1],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [5, 3, 4, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(1, 0, 1, 1), False)
        self.assertEqual(self.peli.check_move_legality(1, 0, 1, -1), False)

    def test_pawn_move_two_squares_having_already_moved_black(self):
        self.peli.change_mover()
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                             [0, 0, 0, -1, -1, -1, -1, -1],
                             [-1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1, 1, 1, 1],
                             [5, 3, 4, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(2, 0, 2, 0), False)

    def test_pawn_move_to_occupied_square_black(self):
        self.peli.change_mover()
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [3, -3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(1, 0, -2, 0), False)
        self.assertEqual(self.peli.check_move_legality(1, 1, -2, 0), False)

    # knight moves white
    def test_knight_move_out_of_bounds_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [3, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(2, 0, 1, -2), False)

    def test_knight_move_emptyish_board_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, 1, -2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, -2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 1, 2), True)

    def test_knight_take_own_pieces_white(self):
        for item in set(self.peli.lauta[6]+self.peli.lauta[7]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, item, 0, 0],
                                 [0, 0, 0, 3, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 7, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 2), False)

    def test_knight_illegal_move_dimensions_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), False)

    # kinght moves black
    def test_knight_move_out_of_bounds_black(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [-3, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.peli.change_mover()
        self.assertEqual(self.peli.check_move_legality(2, 0, 1, -2), False)

    def test_knight_move_emptyish_board_black(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.peli.change_mover()
        self.assertEqual(self.peli.check_move_legality(3, 3, 1, -2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, -2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 1, 2), True)

    def test_knight_take_own_pieces_black(self):
        self.peli.change_mover()
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, item, 0, 0],
                                 [0, 0, 0, -3, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 7, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 2), False)

    # bishop white
    def test_bishop_move_emptyish_board_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, -1), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -3, 3), True)

    def test_bishop_move_over_or_on_top_own_piece_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, -1, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 2), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 2), False)

    def test_bishop_capture_opposing_pieces_white(self):
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, item, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, item, 0, 0, 0],
                                 [0, 0, 0, 4, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, item, 0, 0],
                                 [item, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 7, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, -2, -2), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, 3, -3), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, -2, -2), True)

    def test_bishop_illegal_move_dimensions_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 4, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 1), False)
    # bishop black

    def test_bishop_move_emptyish_board_black(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, -1), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, -3, 3), True)

    def test_bishop_move_over_or_on_top_own_piece_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, -1, 0, 0, 0],
                             [0, 0, 0, -4, 0, 0, 0, 0],
                             [0, 0, 0, 0, -1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 2), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 2), False)

    def test_bishop_illegal_move_dimensions_black(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -4, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 1), False)

    # rook white
    def test_rook_move_emptyish_board_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, -2), True)

    def test_rook_move_over_own_pieces_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 1, 5, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, -2), False)

    def test_rook_capture_opposing_pieces_white(self):
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, 0, 0, item, 0, 0, 0, 0],
                                 [0, 0, 0, 1, 0, 0, 0, 0],
                                 [0, 0, item, 5, item, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, item, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 7, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), False)
            self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), False)
            self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, 0, -1), True)

    # rook black
    def test_rook_move_emptyish_board_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -5, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), True)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, -2), True)

    def test_rook_move_over_own_pieces_black(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -1, 0, 0, 0, 0],
                             [0, 0, -1, -5, -1, 0, 0, 0],
                             [0, 0, 0, -1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 7, 0, 0, 0]], False)
        self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), False)
        self.assertEqual(self.peli.check_move_legality(3, 3, 0, -2), False)

    def test_rook_capture_opposing_pieces_black(self):
        for item in set(self.peli.lauta[6]+self.peli.lauta[7]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, item, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, item, -5, item, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, item, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0]], False)
            self.assertEqual(self.peli.check_move_legality(3, 3, -2, 0), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, 0, 2), False)
            self.assertEqual(self.peli.check_move_legality(3, 3, 2, 0), True)
            self.assertEqual(self.peli.check_move_legality(3, 3, 0, -3), False)

    # king white
    def test_king_move_emptyish_board_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    self.assertEqual(
                        self.peli.check_move_legality(3, 3, i, j), False)
                else:
                    self.assertEqual(
                        self.peli.check_move_legality(3, 3, i, j), True)

    def test_king_capture_opposing_pieces_white(self):
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, item, 0, 0, 0],
                                 [0, 0, 0, 7, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), True)

    def test_king_capture_own_pieces_white(self):
        for item in set(self.peli.lauta[6]+self.peli.lauta[7]):
            self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, item, 0, 0, 0],
                                 [0, 0, 0, 7, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), False)

    def test_king_move_into_check_by_pawn_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, -1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)

    def test_king_move_out_of_bounds_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, -1, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [7, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(7, 0, 1, 1), False)

    def test_king_move_into_check_by_bishop_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, -4, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)

    def test_king_move_into_check_by_rook_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, -5],
                             [0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)

    def test_king_move_into_check_by_queen_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, -6, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)
        self.assertEqual(self.peli.preview_move(3, 3, 1, 1), False)

    def test_square_threatened_queen_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -6, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            0, 3, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            0, 7, self.peli.lauta), False)

    def test_square_threatened_pawn_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            4, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 3, self.peli.lauta), False)

    def test_square_threatened_knight_white(self):
        self.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            1, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            1, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 1, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 1, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 5, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            5, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            5, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 5, self.peli.lauta), True)

    def test_square_threatened_king_white(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            4, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 3, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            3, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            3, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 3, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 2, self.peli.lauta), True)

    # king black
    def test_king_move_emptyish_board_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    self.assertEqual(
                        self.peli.check_move_legality(3, 3, i, j), False)
                else:
                    self.assertEqual(
                        self.peli.check_move_legality(3, 3, i, j), True)

    def test_king_capture_opposing_pieces_black(self):
        self.peli.change_mover()
        for item in set(self.peli.lauta[6]+self.peli.lauta[7]):
            self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, item, 0, 0, 0],
                                 [0, 0, 0, -7, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), True)

    def test_king_capture_own_pieces_black(self):
        self.peli.change_mover()
        for item in set(self.peli.lauta[0]+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, item, 0, 0, 0],
                                 [0, 0, 0, -7, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.check_move_legality(3, 3, -1, 1), False)

    def test_king_move_into_check_by_pawn_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, 1, 0), False)

    def test_king_move_into_check_by_bishop_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, -7, 0, 4, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)

    def test_king_move_into_check_by_rook_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 5],
                             [0, 0, 0, -7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)

    def test_king_move_into_check_by_queen_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6, 0],
                             [0, 0, 0, -7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(3, 3, -1, 1), False)
        self.assertEqual(self.peli.preview_move(3, 3, 1, 1), False)

    # king_threatened function testing
    def test_king_threatened_pawn_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, -7, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)

    def test_king_threatened_bishop_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, -7, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)

    def test_king_threatened_knight_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, -7, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)

    def test_king_threatened_rook_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, -7, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)

    def test_king_threatened_behind_piece_rook_threat_black(self):
        self.peli.change_mover()
        kinglessrow = self.peli.lauta[0]
        kinglessrow.remove(-7)
        for item in set(kinglessrow+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 5, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, item, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [5, 0, item, -7, 0, item, 5, 0],
                                 [0, 0, 0, item, 0, 0, 0, 0],
                                 [0, 0, 0, 5, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.king_threatened(self.peli.lauta), False)

    def test_king_threatened_behind_piece_queen_threat_black(self):
        self.peli.change_mover()
        kinglessrow = self.peli.lauta[0]
        kinglessrow.remove(-7)
        for item in set(kinglessrow+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                                 [4, 0, 0, 0, 4, 0, 0, 0],
                                 [0, item, 0, item, 0, 0, 0, 0],
                                 [0, 0, -7, 0, 0, 0, 0, 0],
                                 [0, item, 0, item, 0, 0, 0, 0],
                                 [4, 0, 0, 0, 4, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.king_threatened(self.peli.lauta), False)

    def test_king_threatened_behind_piece_queen_threat_black(self):
        self.peli.change_mover()
        kinglessrow = self.peli.lauta[0]
        kinglessrow.remove(-7)
        for item in set(kinglessrow+self.peli.lauta[1]):
            self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                                 [6, 6, 6, 6, 6, 6, 6, 6],
                                 [6, item, item, item, 6, 0, 0, 0],
                                 [6, item, -7, item, 6, 0, 0, 0],
                                 [6, item, item, item, 6, 0, 0, 0],
                                 [6, 6, 6, 6, 6, 6, 6, 6],
                                 [0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0]])
            self.assertEqual(self.peli.king_threatened(self.peli.lauta), False)

    def test_move_rook_laterally_to_make_king_threatened_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, -7, 0, 0, 0, 0, 0, 0],
                            [0, -5, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 5, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.preview_move(4, 1, 0, 2), False)
        self.assertEqual(self.peli.preview_move(4, 1, 0, -1), False)

    def test_square_threatened_queen_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 6, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, -7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            0, 3, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            0, 7, self.peli.lauta), False)

    def test_square_threatened_pawn_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, -7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            2, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 3, self.peli.lauta), False)

    def test_square_threatened_knight_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, -7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.square_threatened(
            1, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            1, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 1, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 1, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            4, 5, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            5, 4, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            5, 2, self.peli.lauta), True)
        self.assertEqual(self.peli.square_threatened(
            2, 5, self.peli.lauta), True)

    def test_black_queen_take_white_queen(self):
        self.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 6, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [-6, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, -7, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.check_move_legality(1, 2, 2, -2), True)

    def test_for_having_no_moves_but_actually_having_moves_white(self):
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_for_having_no_moves_but_actually_having_moves_black(self):
        self.peli.change_mover()
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_for_having_no_moves_actually_no_moves_white(self):
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, -5, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, -5],
                            [7, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.check_for_having_no_moves(), True)

    def test_for_having_no_moves_white(self):
        self.peli.set_board([[5, 3, 4, 6, 7, 4, 3, 5],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [-7, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_for_having_no_moves_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, -7],
                            [5, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 5, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]])
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_for_having_no_moves_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 5, 0, 5, 0, 0],
                            [0, 0, 0, 0, -7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.check_for_having_no_moves(), True)

    def test_check_king_threatened_white_to_move(self):
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, -6, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)

    def test_check_king_take_threat_white_to_move(self):
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, -6, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_check_king_not_threatened_after_check_taken_white_to_move(self):
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, -5, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -3, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)
        self.assertEqual(self.peli.check_for_having_no_moves(), False)
        self.assertEqual(self.peli.preview_move(6, 6, -1, -1), True)

    def test_check_king_not_threatened_after_check_taken_white_to_move_is_pawn_move_legal(self):
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, -5, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -3, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.check_move_legality(6, 6, -1, -1), True)
        self.assertEqual(self.peli.preview_move(6, 6, -1, -1), True)

    def test_move_like_pawn_on_capture(self):
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, -5, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -3, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.move_like_pawn(
            6, 6, -1, -1, self.peli.lauta), True)
        self.assertEqual(self.peli.move_like_pawn(
            6, 6, -1, 1, self.peli.lauta), False)

    def test_check_king_threatened_black_to_move(self):
        self.peli.change_mover()
        self.peli.set_board([[-5, -3, -1, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, 6, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 5, 3, 5]])
        self.assertEqual(self.peli.king_threatened(self.peli.lauta), True)
        self.assertEqual(self.peli.check_for_having_no_moves(), False)

    def test_square_threatened_edges_white(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        for i in range(len(self.peli.lauta)):
            for j in range(len(self.peli.lauta)):
                if j == 0 or j == 7:
                    self.assertEqual(self.peli.square_threatened(i, j), False)
                if i == 0 or i == 7:
                    self.assertEqual(self.peli.square_threatened(i, j), False)

    def test_square_threatened_edges_black(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        for i in range(len(self.peli.lauta)):
            for j in range(len(self.peli.lauta)):
                if j == 0 or j == 7:
                    self.assertEqual(self.peli.square_threatened(i, j), False)
                if i == 0 or i == 7:
                    self.assertEqual(self.peli.square_threatened(i, j), False)

    def test_square_threatened_edges_black_out_of_turn(self):
        self.peli.change_mover()
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        for i in range(len(self.peli.lauta)):
            for j in range(len(self.peli.lauta)):
                if j == 0 or j == 7:
                    self.assertEqual(self.peli.square_threatened(
                        i, j, self.peli.lauta, True), False)
                if i == 0 or i == 7:
                    self.assertEqual(self.peli.square_threatened(
                        i, j, self.peli.lauta, True), False)

    def test_can_pawn_movelist_returns_string(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, -1, 0, 7, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(self.peli.can_pawn_movelist(
            6, 1, 1, self.peli.lauta, self.peli.whitetomove), [])

    def test_promote_pawns_works_white(self):
        self.peli.set_board([[1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [7, 0, 0, 0, 0, 0, 0, 0]])
        self.peli.promote_pawns()
        self.assertCountEqual(self.peli.lauta, [[6, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, -7, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [7, 0, 0, 0, 0, 0, 0, 0]])

    def test_promote_pawns_works_black(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [7, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, -1]])
        self.peli.promote_pawns()
        self.assertCountEqual(self.peli.lauta, [[0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, -7, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [7, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, -6]])

    def test_execute_move_does_not_change_game_states_called_for_illegal_move(self):
        test_board = self.peli.lauta[:]
        test_mover = self.peli.whitetomove
        self.peli.execute_move(1, 0, 1, 0)
        self.assertEqual(self.peli.whitetomove, test_mover)
        self.assertCountEqual(self.peli.lauta, test_board)

    def test_execute_move_changes_game_states_called_for_legal_move(self):
        test_board = self.peli.lauta[:]
        test_mover = self.peli.whitetomove
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, -1, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0, 0],
                            [7, 0, 0, 0, 0, 0, 0, 0]])
        self.peli.execute_move(6, 1, -1, 1)
        self.assertNotEqual(self.peli.whitetomove, test_mover)
        self.assertCountEqual(self.peli.lauta, [[0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, -7, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 1, 0, 0, 0, 0, 0],
                                                [1, 0, 0, 0, 0, 0, 0, 0],
                                                [7, 0, 0, 0, 0, 0, 0, 0]])

    def test_execute_move_promotes_pawns(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, -7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [7, 0, 0, 0, 0, 0, 0, 0]])
        self.peli.execute_move(1, 4, -1, 0)
        self.assertCountEqual(self.peli.lauta, [[0, 0, 0, 0, 6, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, -7, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0, 0, 0],
                                                [7, 0, 0, 0, 0, 0, 0, 0]])

    def test_execute_move_changes_state_to_ending_on_repetition(self):
        self.peli.set_board([[-5, 0, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, -3, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]], False)
        self.peli.draw_by_repetition = {
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w": 2}
        self.peli.execute_move(2, 2, -2, -1)
        self.assertEqual(self.peli.gamestatus, "DRAW BY REPETITION")

    def test_execute_move_changes_state_to_ending_on_mate(self):
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 6, 0, 0],
                            [0, 0, 0, 0, 0, 5, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]], True)
        self.peli.execute_move(4, 5, -3, 0)
        self.assertEqual(self.peli.gamestatus, "CHECKMATE")

    def test_execute_move_changes_state_to_ending_on_stalemate(self):
        self.peli.set_board([[0, 0, 0, 0, 0, 0, 0, -7],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 5, 0],
                            [0, 0, 0, 0, 0, 5, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]], True)
        self.peli.execute_move(5, 5, -4, 0)
        self.assertEqual(self.peli.gamestatus, "STALEMATE")

    def test_execute_move_changes_state_to_check(self):
        self.peli.set_board([[-5, -3, -4, -6, -7, -4, -3, -5],
                            [-1, -1, -1, -1, -1, -1, -1, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 6, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [5, 3, 4, 6, 7, 4, 3, 5]], True)
        self.peli.execute_move(4, 5, -3, 0)
        self.assertEqual(self.peli.gamestatus, "CHECK! BLACK TO MOVE")

    def test_get_board_as_FEN_returns_correct_string(self):
        self.assertEqual(self.peli.get_board_as_FEN(),
                         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
