import logging
from src import Utils
from . import ResolutionAlgorithms
import copy
import random

######################
#
# This is a Brute Force solver :
# It tries using existing algorithms to solve sudoku, and if blocked, make a brute force
#
######################

def solve(matrix):

  logger = logging.getLogger("sudoku_solver")

  size = len(matrix[0])

  while not Utils.check_matrix_is_finished(matrix, size):
    score = Utils.calculate_matrix_score(matrix, size)
    matrix = filling_simply(matrix, size)
    current_score = Utils.calculate_matrix_score(matrix, size)
    if score == current_score:
      solution = solve_forcing(matrix, size)
      if solution is None:
        logger.warning("Sudoku is blocked with %i empty cases", score)
      else:
        logger.info("A solution has been found with brute force")
        matrix = solution
      break

  Utils.print_matrix(matrix, size)

  return matrix


def solve_forcing(matrix, size):
  logger = logging.getLogger("sudoku_solver")

  logger.info("There is %i cases to fill in", Utils.calculate_matrix_score(matrix, size))

  solution = None

  # TODO : Add a logic to the brute force, do not make it random

  while solution is None:

    matrix_forced = copy.deepcopy(matrix)
    for i in range(0, size):
      for j in range(0, size):

        if matrix[i][j] == 0:
          matrix_forced[i][j] = random.choice(get_simple_list_of_possibilities(matrix, size, i, j))

    if Utils.check_a_matrix_is_good(matrix):
      solution = matrix_forced
      break

  return solution



def filling_simply(matrix, size):
  logger = logging.getLogger("sudoku_solver")

  for i in range(0, size):
    for j in range(0, size):
      logger.debug("point %i %i is : %i ", i, j, matrix[i][j])

      actual_value = matrix[i][j]

      if actual_value == 0:

        # We will try to solve this point with only simple algos
        list_of_possibilities = get_simple_list_of_possibilities(matrix, size, i, j)

        # Print Possibilities
        for v in list_of_possibilities:
          logger.debug("v = %i ", v)

        if Utils.check_list(list_of_possibilities):
          matrix[i][j] = list_of_possibilities[0]

  return matrix


def get_simple_list_of_possibilities(matrix, size, i, j):
  list_of_possibilities = range(1, size + 1)

  list_of_possibilities = ResolutionAlgorithms.remove_possibilities_same_row(list_of_possibilities, matrix, i)

  list_of_possibilities = ResolutionAlgorithms.remove_possibilities_same_column(list_of_possibilities, matrix, j)

  ResolutionAlgorithms.remove_possibilities_same_square(list_of_possibilities, matrix, size, i, j)

  if len(list_of_possibilities) != 1:

    list_of_possibilities = ResolutionAlgorithms.give_solution_if_forced_by_other_lines_of_other_squares(matrix, i, j, size, list_of_possibilities)

    if len(list_of_possibilities) != 1:

      list_of_possibilities = ResolutionAlgorithms.give_solution_if_forced_by_other_columns_of_other_squares(matrix, i, j, size, list_of_possibilities)

  return list_of_possibilities
