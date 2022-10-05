from pathlib import Path
from copy import deepcopy


class Settings:
  # this is a singleton class
  _PROJECT_NAME = 'telempy'
  _IS_INITIATED = False
  _ABSOLUTE_PROJECT_PATH: Path=None

  def __init__(self):
    if Settings._IS_INITIATED:
      return

    # find the absolute path to the project root
    p = Path(__file__)
    while p.name != Settings._PROJECT_NAME:
      p = p.parent
    Settings._ABSOLUTE_PROJECT_PATH = p

  def project_directory(self) -> Path:
    return deepcopy(self._ABSOLUTE_PROJECT_PATH)
