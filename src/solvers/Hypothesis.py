import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from src import Utils
from . import Normal

######################
#
# This is an Hypothesis solver :
# It tries using existing algorithms to solve sudoku, and if blocked, it makes one hypothesis
#
######################

def solve(matrix):

  logger = logging.getLogger("sudoku_solver")

  size = len(matrix[0])

  while not Utils.check_matrix_is_finished(matrix, size):
    score = Utils.calculate_matrix_score(matrix, size)
    matrix = Normal.run_1_time(matrix, size)
    # Utils.print_matrix(matrix, size)
    current_score = Utils.calculate_matrix_score(matrix, size)
    if score == current_score:
      solution = solve_with_hypothesis(matrix, size)
      if solution is None:
        logger.warning("Sudoku is blocked with %i empty cases", score)
      else:
        logger.info("A solution has been found with hypothesis")
        matrix = solution
      break

  Utils.print_matrix(matrix, size)

  return matrix


# TODO : Make more hypothesis, one after the other
def solve_with_hypothesis(matrix, size):
  logger = logging.getLogger("sudoku_solver")

  # Find a case where there is different possibilities (maybe try to get the one with the most different possibilities)
  y = -1
  x = -1

  # TODO : Try to get the point with the most possibilities
  # TODO : Create as many matrixes as possible, checking all the possibilities for each point unfilled ?

  for i in range(0, size):
    for j in range(0, size):
      logger.debug("point %i %i is : %i ", i, j, matrix[i][j])

      actual_value = matrix[i][j]

      if actual_value == 0:
        x = i
        y = j
        break

    if x != -1:
      break

  # Get all different possibilities for this case
  possibilities = Normal.get_list_of_possibilities_for_one_point(matrix, x, y, size)

  # Create a set of different matrix
  set_of_matrix = []

  for possibility in possibilities:
    matrix_with_hypothesis = matrix[:]
    matrix_with_hypothesis[x][y] = possibility
    set_of_matrix.append(matrix_with_hypothesis)

    logger.debug("Possiblity is : %i at ( %i ; %i )", possibility, x, y)

  # TODO : Secure Threads by closing them

  # Parallelize list of matrix treatment
  pool = ThreadPoolExecutor(max_workers=10)
  list_of_futures = []

  for matrix_with_hypothesis in set_of_matrix:
    list_of_futures.append(pool.submit(solve_one_matrix, (matrix[:])))

  # Check if there is a solution
  solution = None
  for future in as_completed(list_of_futures):
    result = future.result()
    if result[1] == 0:
      solution = result[0]
      break

  return solution


def solve_one_matrix(matrix):
  logger = logging.getLogger("sudoku_solver")
  size = len(matrix[0])
  score = size*size

  while not Utils.check_matrix_is_finished(matrix, size):
    matrix = Normal.run_1_time(matrix, size)

    current_score = Utils.calculate_matrix_score(matrix, size)
    if score == current_score:
      logger.warning("Using hypothesis, Sudoku is still blocked with %i empty cases", score)
      break

    score = current_score

  return matrix, score
