import logging
import configparser
from src.solvers import Normal
import Matrix


def main():
  logger.info("Starting script")

  matrix = Matrix.create_matrix_9x9_normal()

  Normal.solve(matrix)

  # TODO : Add a checker on the solution

  logger.info("Finishing script")


if __name__ == '__main__':

  # Configuration file load
  config = configparser.ConfigParser()
  config.read("config.cfg")

  # Loggers
  logger = logging.getLogger("sudoku_solver")
  logger.setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  file_handler = logging.FileHandler("sudoku_solver.log")
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(formatter)

  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  main()
