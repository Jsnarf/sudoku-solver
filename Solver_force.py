import logging
import Utils

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
        list_of_possibilities = range(1, size+1)

        # Remove all possibilities because they occur on the same line
        list_of_possibilities = [x for x in list_of_possibilities if x not in matrix[i]]

        # Remove all possibilities because they occur on the same column
        list_of_possibilities = [x for x in list_of_possibilities if x not in [row[j] for row in matrix]]

        # Remove all possibilities because they occur on the same square
        for l in Utils.coordinate_list_for_square(i, size):
          for c in Utils.coordinate_list_for_square(j, size):
            if matrix[l][c] != 0:
              try:
                list_of_possibilities.remove(matrix[l][c])
              except:
                pass


        # Here are more complex algorithms to check if a number could be chosen

        if len(list_of_possibilities) != 1:

          # If the line of the square is full
          # If the number is present on each other lines  (=> so twice for all lines or columns)
          # And is present in the list of possibilities (=> it is not a forbidden value due to columns, lines or square value)
          # Then it is the number to put on the empty case
          list_of_possibilities = give_solution_if_forced_by_other_lines_of_other_squares(matrix, i, j, size, list_of_possibilities)

          if len(list_of_possibilities) != 1:

            # If the column of the square is full
            # If the number is present on each other columns (=> so twice for all lines or columns)
            # And is present in the list of possibilities (it is not a forbidden value due to columns, lines or square value)
            # Then it is the number to put on the empty case
            list_of_possibilities = give_solution_if_forced_by_other_columns_of_other_squares(matrix, i, j, size, list_of_possibilities)


            # TODO : Add more algorithms resolution to solve more difficult sudoku


        # Print Possibilities
        for v in list_of_possibilities:
          logger.info("v = %i ", v)

        if Utils.check_list(list_of_possibilities):
          matrix[i][j] = list_of_possibilities[0]

  return matrix


def indices_of_others(indice):
  if (indice % 3) == 0:
    return [1, 2]
  elif (indice % 3) == 1:
    return [0, 2]
  else:
    return [0, 1]


def are_full_line(matrix,indice_line,indice_column,indices):
  are_full = True
  for x in indices:
    if matrix[indice_line][(indice_column // 3)*3 + x] == 0:
      are_full = False
  return  are_full


def are_full_column(matrix,indice_line,indice_column,indices):
  are_full = True
  for x in indices:
    if matrix[(indice_line // 3)*3 + x][indice_column] == 0:
      are_full = False
  return  are_full


def give_solution_if_forced_by_other_columns_of_other_squares(matrix, i, j, size, list_of_possibilities):
  logger = logging.getLogger("sudoku_solver")

  # Line indices to check if column is full
  indices = indices_of_others(i)
  if are_full_column(matrix, i, j, indices):
    logger.error("Column %i is full on lin %i from square %i", j, i, i // 3)
    list_of_other_numbers = []

    # Check other square' columns number that are on both columns
    for z in indices_of_others(j):
      column_to_check = (j // 3) * 3 + z
      logger.error("Column to check is %i", column_to_check)
      # We are in other columns of the square & we add for every line all the numbers listed if they are not equal to 0
      for x in range(0, size):
        if matrix[x][column_to_check] != 0:
          logger.error("value of %i : %i is %i", x, column_to_check, matrix[x][column_to_check])
          list_of_other_numbers.append(matrix[x][column_to_check])

    # We have to get every number present on both other columns
    list_of_number_present_on_both = Utils.get_duplicates_of_a_list(list_of_other_numbers)
    for n1 in list_of_number_present_on_both:
      logger.error("This number is present on both columns : %i ", n1)

    list_of_new_possibilities = [x for x in list_of_number_present_on_both if x in list_of_possibilities]
    for n1 in list_of_new_possibilities:
      logger.error("This number is maybe a new possibility : %i ", n1)

    if len(list_of_new_possibilities) == 1:
      list_of_possibilities = list_of_new_possibilities

  return list_of_possibilities


def give_solution_if_forced_by_other_lines_of_other_squares(matrix, i, j, size, list_of_possibilities):
  logger = logging.getLogger("sudoku_solver")

  # Column indices to check to know if line is full
  indices = indices_of_others(j)
  if are_full_line(matrix, i, j, indices):
    logger.error("Line %i is full on column %i from square %i", i, j, j // 3)
    list_of_other_numbers = []

    # Check other square' lines number that are on both lines
    for z in indices_of_others(i):
      line_to_check = (i // 3) * 3 + z
      logger.error("Line to check is %i", line_to_check)
      # We are in other lines of the square & we add for every line all the numbers listed if they are not equal to 0
      for x in range(0, size):
        if matrix[line_to_check][x] != 0:
          logger.error("value of %i : %i is %i", line_to_check, x, matrix[line_to_check][x])
          list_of_other_numbers.append(matrix[line_to_check][x])

    # We have to get every number present on both other lines
    list_of_number_present_on_both = Utils.get_duplicates_of_a_list(list_of_other_numbers)
    for n1 in list_of_number_present_on_both:
      logger.error("This number is present on both lines : %i ", n1)

    list_of_new_possibilities = [x for x in list_of_number_present_on_both if x in list_of_possibilities]
    for n1 in list_of_new_possibilities:
      logger.error("This number is maybe a new possibility : %i ", n1)

    if len(list_of_new_possibilities) == 1:
      list_of_possibilities = list_of_new_possibilities

  return list_of_possibilities
