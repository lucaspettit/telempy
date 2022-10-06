from unittest import TestCase
from unittest.mock import MagicMock
from gt.utils import Settings
from typing import Dict


class TestBase(TestCase):
  _settings = Settings()

  def unpack_mocks(self, *mocks) -> Dict[str, MagicMock]:
    raise NotImplemented()