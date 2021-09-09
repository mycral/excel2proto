import compileall
import sys

PYTHON_IN_PATH = sys.argv[1]
compileall.compile_dir(PYTHON_IN_PATH)
