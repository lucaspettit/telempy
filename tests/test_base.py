from unittest import TestCase
from unittest.mock import MagicMock, Mock
from granturismo.utils import Settings
from typing import Union


class TestBase(TestCase):
  _settings = Settings()

  @staticmethod
  def unpack_mocks(*mocks) -> dict:
      return {m._extract_mock_name(): m for m in mocks}

  @staticmethod
  def get_method_call_names(mock: Union[Mock, MagicMock]) -> [str]:
      return list(map(lambda x: x[0], mock.method_calls))