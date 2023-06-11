from pathlib import Path
import os



def curr_dir() -> str:
	return os.path.dirname(os.path.realpath(__file__))

def proj_root() -> str:
	temp = Path(curr_dir())
	return str(temp.parent)