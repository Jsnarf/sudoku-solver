import logging
from src import Utils
from . import ResolutionAlgorithms

######################
#
# This is a Normal solver :
# It tries using existing algorithms to solve sudoku, but no hypothesis are made
#
######################

# TODO : Add also a full variabilization on matrix' size

def solve(matrix):

  logger = logging.getLogger("sudoku_solver")

  size = len(matrix[0])
  score = size*size

  while not Utils.check_matrix_is_finished(matrix, size):
    Utils.calculate_matrix_score(matrix, size)
    matrix = run_1_time(matrix, size)
    Utils.print_matrix(matrix, size)
    current_score = Utils.calculate_matrix_score(matrix, size)
    if score == current_score:
      logger.error("Sudoku is blocked with %i empty cases", score)
      break
    score = current_score

  Utils.print_matrix(matrix, size)

  return matrix


def run_1_time(matrix, size):
  logger = logging.getLogger("sudoku_solver")

  for i in range(0, size):
    for j in range(0, size):
      logger.info("point %i %i is : %i ", i, j, matrix[i][j])

      actual_value = matrix[i][j]

      if actual_value == 0:

        # We will try to solve this point
        list_of_possibilities = get_list_of_possibilities_for_one_point(matrix, i, j, size)

        # Print Possibilities
        for v in list_of_possibilities:
          logger.info("v = %i ", v)

        if Utils.check_list(list_of_possibilities):
          matrix[i][j] = list_of_possibilities[0]

  return matrix



def get_list_of_possibilities_for_one_point(matrix, i, j, size):
  list_of_possibilities = range(1, size + 1)

  list_of_possibilities = ResolutionAlgorithms.remove_possibilities_same_row(list_of_possibilities, matrix, i)

  list_of_possibilities = ResolutionAlgorithms.remove_possibilities_same_column(list_of_possibilities, matrix, j)

  ResolutionAlgorithms.remove_possibilities_same_square(list_of_possibilities, matrix, size, i, j)

  if len(list_of_possibilities) != 1:

    list_of_possibilities = ResolutionAlgorithms.give_solution_if_forced_by_other_lines_of_other_squares(matrix, i, j, size, list_of_possibilities)

    if len(list_of_possibilities) != 1:

      list_of_possibilities = ResolutionAlgorithms.give_solution_if_forced_by_other_columns_of_other_squares(matrix, i, j, size, list_of_possibilities)

  return list_of_possibilities
