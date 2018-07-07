import logging
from src import Utils
from . import Normal

######################
#
# This is a Normal solver :
# It tries using existing algorithms to solve sudoku, and if blocked, it make one hypothesis
#
######################

def solve(matrix):

  logger = logging.getLogger("sudoku_solver")

  size = len(matrix[0])
  score = size*size

  while not Utils.check_matrix_is_finished(matrix, size):
    Utils.calculate_matrix_score(matrix, size)
    matrix = Normal.run_1_time(matrix, size)
    Utils.print_matrix(matrix, size)
    current_score = Utils.calculate_matrix_score(matrix, size)
    if score == current_score:
      # TODO : We are blcoked but could we try to make some assumptions and parallelize treatment ?
      parallelize_run(matrix, size)
      logger.error("Sudoku is blocked with %i empty cases", score)
      break
    score = current_score

  Utils.print_matrix(matrix, size)

  return matrix

def parallelize_run(matrix, size):
  # TODO : We will try to make an hypothesis on a case and use parallelization to compute all different possibilities
  # TODO : Make more than one hypothesis
  logger = logging.getLogger("sudoku_solver")

  # Find a case where there is different possibilities (maybe try to get the one with the most different possibilities)
  x, y = -1
  for i in range(0, size):
    for j in range(0, size):
      logger.info("point %i %i is : %i ", i, j, matrix[i][j])

      actual_value = matrix[i][j]

      if actual_value == 0:
        x = i
        y = j
        break

    if x != -1:
      break

  # Get all different possibilities for this case
  possibilities = Normal.get_list_of_possibilities_for_one_point(matrix, x, y, size)

  # Create an array of different matrix


  # create an array of matrix and parallelize their treatment
  # Try to get the result of the one that is not blocked (if there is one ;) )
