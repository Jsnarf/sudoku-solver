import logging
from src import Utils


# TODO : Add more algorithms resolution to solve more difficult sudoku

def remove_possibilities_same_row(list_of_possibilities, matrix, i):
  # Remove all possibilities because they occur on the same line
  return [x for x in list_of_possibilities if x not in matrix[i]]

def remove_possibilities_same_column(list_of_possibilities, matrix, j):
  # Remove all possibilities because they occur on the same column
  return [x for x in list_of_possibilities if x not in [row[j] for row in matrix]]

# Remove all possibilities because they occur on the same square
def remove_possibilities_same_square(list_of_possibilities, matrix, size, i, j):
  for l in Utils.coordinate_list_for_square(i, size):
    for c in Utils.coordinate_list_for_square(j, size):
      if matrix[l][c] != 0:
        try:
          list_of_possibilities.remove(matrix[l][c])
        except:
          pass

# If the column of the square is full
# If the number is present on each other columns (=> so twice for all lines or columns)
# And is present in the list of possibilities (it is not a forbidden value due to columns, lines or square value)
# Then it is the number to put on the empty case
def give_solution_if_forced_by_other_columns_of_other_squares(matrix, i, j, size, list_of_possibilities):
  logger = logging.getLogger("sudoku_solver")

  # Line indices to check if column is full
  indices = Utils.indices_of_others(i)
  if Utils.are_full_column(matrix, i, j, indices):
    logger.debug("Column %i is full on lin %i from square %i", j, i, i // 3)
    list_of_other_numbers = []

    # Check other square' columns number that are on both columns
    for z in Utils.indices_of_others(j):
      column_to_check = (j // 3) * 3 + z
      logger.debug("Column to check is %i", column_to_check)
      # We are in other columns of the square & we add for every line all the numbers listed if they are not equal to 0
      for x in range(0, size):
        if matrix[x][column_to_check] != 0:
          logger.debug("value of %i : %i is %i", x, column_to_check, matrix[x][column_to_check])
          list_of_other_numbers.append(matrix[x][column_to_check])

    # We have to get every number present on both other columns
    list_of_number_present_on_both = Utils.get_duplicates_of_a_list(list_of_other_numbers)
    for n1 in list_of_number_present_on_both:
      logger.debug("This number is present on both columns : %i ", n1)

    list_of_new_possibilities = [x for x in list_of_number_present_on_both if x in list_of_possibilities]
    for n1 in list_of_new_possibilities:
      logger.debug("This number is maybe a new possibility : %i ", n1)

    if len(list_of_new_possibilities) == 1:
      list_of_possibilities = list_of_new_possibilities

  return list_of_possibilities


# If the line of the square is full
# If the number is present on each other lines  (=> so twice for all lines or columns)
# And is present in the list of possibilities (=> it is not a forbidden value due to columns, lines or square value)
# Then it is the number to put on the empty case
def give_solution_if_forced_by_other_lines_of_other_squares(matrix, i, j, size, list_of_possibilities):
  logger = logging.getLogger("sudoku_solver")

  # Column indices to check to know if line is full
  indices = Utils.indices_of_others(j)
  if Utils.are_full_line(matrix, i, j, indices):
    logger.debug("Line %i is full on column %i from square %i", i, j, j // 3)
    list_of_other_numbers = []

    # Check other square' lines number that are on both lines
    for z in Utils.indices_of_others(i):
      line_to_check = (i // 3) * 3 + z
      logger.debug("Line to check is %i", line_to_check)
      # We are in other lines of the square & we add for every line all the numbers listed if they are not equal to 0
      for x in range(0, size):
        if matrix[line_to_check][x] != 0:
          logger.debug("value of %i : %i is %i", line_to_check, x, matrix[line_to_check][x])
          list_of_other_numbers.append(matrix[line_to_check][x])

    # We have to get every number present on both other lines
    list_of_number_present_on_both = Utils.get_duplicates_of_a_list(list_of_other_numbers)
    for n1 in list_of_number_present_on_both:
      logger.debug("This number is present on both lines : %i ", n1)

    list_of_new_possibilities = [x for x in list_of_number_present_on_both if x in list_of_possibilities]
    for n1 in list_of_new_possibilities:
      logger.debug("This number is maybe a new possibility : %i ", n1)

    if len(list_of_new_possibilities) == 1:
      list_of_possibilities = list_of_new_possibilities

  return list_of_possibilities

