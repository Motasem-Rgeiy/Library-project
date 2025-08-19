import shutil
from pathlib import Path

shutil.copytree(Path.home() / Path('Desktop', 'Library') , Path.home() / Path('Documents' ,'Library-project'))


