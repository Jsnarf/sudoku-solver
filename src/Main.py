import logging
import configparser
import time
from src.solvers import Normal
from src.solvers import Hypothesis
import Utils
import Matrix

def main():
  logger.info("Starting script")
  start_time = Utils.current_milli_time()

  #matrix = Matrix.create_matrix_9x9_normal()
  #matrix = Matrix.create_matrix_9x9_diabolik()
  matrix = Matrix.create_matrix_9x9_difficil()

  #Normal.solve(matrix)
  matrix = Hypothesis.solve(matrix)

  # TODO : Add a checker on the solution

  end_time = Utils.current_milli_time()
  logger.info("Time spent to process : %i milliseconds", end_time-start_time)
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
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  main()
