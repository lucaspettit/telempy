from unittest import TestCase
from unittest.mock import patch, MagicMock
from utils import Settings
from typing import Dict


class TestBase(TestCase):
  _settings = Settings()

  def unpack_mocks(self, *mocks) -> Dict[str, MagicMock]:
    raise NotImplemented()