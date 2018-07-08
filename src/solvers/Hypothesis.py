import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import copy
from src import Utils
from . import Normal
from ..object import PointPossibility

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
# TODO: Optimizing number of treatment (not create too much matrix, get one point and not all etc..) ?
def solve_with_hypothesis(matrix, size):
  logger = logging.getLogger("sudoku_solver")

  # Get a list of each point unfilled with its possibilities
  points_with_possibilities = []


  for i in range(0, size):
    for j in range(0, size):
      logger.debug("point %i %i is : %i ", i, j, matrix[i][j])

      if matrix[i][j] == 0:
        points_with_possibilities.append(
          PointPossibility.PointPossibility(i, j,
                                            Normal.get_list_of_possibilities_for_one_point(matrix, i, j, size))
        )

  # Create all different possible matrix
  list_of_matrix = []

  for point in points_with_possibilities:
    for possibility in point.list_of_possibilities:
      matrix_with_hypothesis = copy.deepcopy(matrix)
      matrix_with_hypothesis[point.x][point.y] = possibility
      list_of_matrix.append(matrix_with_hypothesis)

      logger.debug("Possiblity is : %i at ( %i ; %i )", possibility, point.x, point.y)

  # Parallelize list of matrix treatment
  with ProcessPoolExecutor() as executor:

    list_of_futures = {executor.submit(solve_one_matrix, matrix_with_hypothesis): matrix_with_hypothesis for matrix_with_hypothesis in list_of_matrix}

    # Check if there is a solution from one of all the try
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
