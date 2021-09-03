import compileall
import sys

PYTHON_INPUTPATH = sys.argv[1]
compileall.compile_dir(PYTHON_INPUTPATH)
