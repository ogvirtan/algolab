import unittest
from game.shakki import Shakki
from services.engine import Engine


class TestEngine (unittest.TestCase):
    def setUp(self):
        self.eng = Engine()

    def test_engine_exists(self):
        self.assertNotEqual(self.eng, None)

    def test_alphabeta_returns_best_move(self):
        self.eng.peli.set_board([[-5, 0, -4, -6, -7, -4, -3, -5],
                                [-1, -1, -1, -1, -1, -1, -1, -1],
                                [0, 3, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, -3, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [1, 1, 1, 1, 1, 1, 1, 1],
                                [5, 0, 4, 6, 7, 4, 3, 5]])
        self.eng.generate_supporting_lists()
        self.assertIn(self.eng.move_as_UCI(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), False, 0,
                      self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[1]), {"a7b6", "c7b8"})

    def test_heuristic_function_evaluates_position_correctly(self):
        lauta1 = ([[-5, 0, -4, -6, -7, -4, -3, -5],
                   [-1, -1, -1, -1, -1, -1, -1, -1],
                   [0, 3, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, -3, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                  [5, 0, 4, 6, 7, 4, 3, 5]])
        self.eng.generate_supporting_lists(lauta1)
        poslist1 = self.eng.piece_positions_all[:]
        lauta2 = ([[-5, 0, -4, -6, -7, -4, -3, -5],
                   [0, -1, -1, -1, -1, -1, -1, -1],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, -3, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1],
                  [5, 0, 4, 6, 7, 4, 3, 5]])
        self.eng.generate_supporting_lists(lauta2)
        poslist2 = self.eng.piece_positions_all[:]
        self.assertGreater(self.eng.heuristic_function(
            poslist1, 0), self.eng.heuristic_function(poslist2, 0))

    def test_alphabeta_returns_correct_values_at_imminent_mate(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 6, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertGreaterEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                                self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 100000)
        self.assertIn(self.eng.move_as_UCI(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                      self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[1]), {"g5e7", "g5g8"})

    def test_alphabeta_returns_zero_at_stalemate_black(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 5, 0, 5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), False, 0,
                         self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 0)

    def test_alphabeta_returns_zero_at_stalemate_white(self):
        self.eng.peli.set_board([[0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, -5, 0, -5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                         self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 0)

    def test_generate_move_king_returns_empty_list_with_no_moves(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 5, 0, 5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.generate_move_king(
            0, 4, 7, False, self.eng.peli.lauta), [])

    def test_generate_move_king_returns_empty_list_with_no_moves_and_in_check(self):
        self.eng.peli.set_board([[6, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.generate_move_king(
            0, 4, 7, False, self.eng.peli.lauta), [])

    def test_king_not_checked_after_move_returns_false_moving_into_check(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 5, 0, 5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.king_not_checked_after_move(
            0, 4, 1, 4, self.eng.peli.lauta, False), False)

    def test_square_threatened_returning_correct_values(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 5, 0, 5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.square_threatened(
            1, 4, False, self.eng.threatlist_white, self.eng.threatlist_black), True)
        self.assertEqual(self.eng.square_threatened(
            1, 5, False, self.eng.threatlist_white, self.eng.threatlist_black), True)
        self.assertEqual(self.eng.square_threatened(
            1, 3, False, self.eng.threatlist_white, self.eng.threatlist_black), True)
        self.assertEqual(self.eng.square_threatened(
            0, 5, False, self.eng.threatlist_white, self.eng.threatlist_black), True)
        self.assertEqual(self.eng.square_threatened(
            0, 3, False, self.eng.threatlist_white, self.eng.threatlist_black), True)
        self.assertEqual(self.eng.square_threatened(
            0, 2, False, self.eng.threatlist_white, self.eng.threatlist_black), False)

    def test_alphabeta_returns_inf_at_checkmate_with_white(self):
        self.eng.peli.set_board([[0, 0, 6, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), False, 0,
                         self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[1], None)
        self.assertGreaterEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), False, 0,
                                self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 100000)

    def test_make_move_changes_game_state_to_endstate_on_mate(self):
        self.eng.peli.set_board([[0, 0, 6, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.peli.change_mover()
        self.eng.make_move()
        self.assertEqual(self.eng.peli.gamestatus, "CHECKMATE")

    def test_alphabeta_returns_inf_at_checkmate_with_black(self):
        self.eng.peli.set_board([[0, 0, -6, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, -7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                         self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[1], None)
        self.assertLessEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                             self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], -100000)

    def test_alphabeta_returns_correct_move_with_mate_in_one_step(self):
        self.eng.peli.set_board([[0, 0, 0, 0, -7, 0, 0, 0],
                                [6, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertGreaterEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                                self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 100000)
        self.assertIn(self.eng.move_as_UCI(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), True, 0,
                      self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[1]), {"a7a8", "a7b8", "a7e7"})

    def test_alphabeta_returns_correct_move_with_mate_in_two_steps(self):
        self.eng.peli.set_board([[0, 0, 0, 0, 0, 0, -7, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 0],
                                [0, 0, 0, 0, 0, 0, 6, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertGreaterEqual(self.eng.alphabeta(self.eng.peli.lauta, self.eng.depth, float("-inf"), float("inf"), False, 0,
                                self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 100000)

    def test_alphabeta_returns_correct_move_with_mate_in_three_steps(self):
        self.eng.peli.set_board([[0, 0, 0, 0, 0, 0, -7, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 7, 0, 0, 0],
                                [0, 0, 0, 0, 0, 5, 0, 0],
                                [0, 0, 0, 0, 6, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists()
        self.assertEqual(self.eng.alphabeta(self.eng.peli.lauta, 3, float("-inf"), float("inf"), True, 0,
                         self.eng.movelist_white, self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)[0], 100000)

    def test_manage_board_changing_board_correctly_no_special_rules(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

        self.eng.generate_supporting_lists(lauta)
        self.eng.manage_board(2, 4, 2, 3, lauta)

        self.assertCountEqual(lauta, [[0, 0, 0, 0, 0, 0, -7, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 7, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 5, 0, 0],
                                      [0, 0, 0, 0, 6, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_manage_board_changing_board_correctly_queening(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.eng.manage_board(1, 0, 0, 0, lauta)
        self.assertCountEqual(lauta, [[6, 0, 0, 0, 0, 0, -7, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 7, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 5, 0, 0],
                                      [0, 0, 0, 0, 6, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_revert_board_changing_board_correctly_queening(self):
        lauta = ([[6, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.eng.revert_board(1, 0, 0, 0, 0, 1, lauta)
        self.assertCountEqual(lauta, [[0, 0, 0, 0, 0, 0, -7, 0],
                                      [1, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 7, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 5, 0, 0],
                                      [0, 0, 0, 0, 6, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_revert_board_changing_board_correctly_no_special_rules(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.eng.revert_board(2, 4, 2, 3, 0, 7, lauta)
        self.assertCountEqual(lauta, [[0, 0, 0, 0, 0, 0, -7, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 7, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 5, 0, 0],
                                      [0, 0, 0, 0, 6, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_manage_board_and_revert_board_changing_kingpos_correctly(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.eng.manage_board(2, 3, 2, 4, lauta)
        self.assertEqual(self.eng.white_king_pos, (2, 4))
        self.eng.revert_board(2, 3, 2, 4, 0, 7, lauta)
        self.assertEqual(self.eng.white_king_pos, (2, 3))

    def test_threat_king_returns_correct_values(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.assertEqual(
            len(self.eng.generate_threat_king(0, 6, 7, False, lauta)), 5)

    def test_move_king_returns_correct_values(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.assertEqual(
            len(self.eng.generate_move_king(0, 6, 7, False, lauta)), 3)

    def test_move_threat_king_returns_correct_values(self):
        lauta = ([[0, 0, 0, 0, 0, 0, -7, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 7, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 0, 0, 0, 6, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        tark = self.eng.generate_move_threat_all(0, 6, 7, False, lauta)
        self.assertEqual(len(tark[0]), 3)
        self.assertEqual(len(tark[1]), 5)

    def test_manage_list_states_returns_correct_values(self):
        lauta = ([[0, 0, 0, 0, 0, 0, 0, -7],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 5, 0, 0, 0],
                  [0, 0, 0, 0, -5, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [7, 0, 0, 0, 0, 0, 0, 0]])
        self.eng.generate_supporting_lists(lauta)
        self.eng.manage_board(4, 4, 3, 4, lauta)
        self.eng.manage_list_states(-5, 4, 4, 3, 4, False, lauta, self.eng.movelist_white,
                                    self.eng.movelist_black, self.eng.threatlist_white, self.eng.threatlist_black)
