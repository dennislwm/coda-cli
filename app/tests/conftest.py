import pytest
import os

from common.json_cli import JsonFile, JsonPlan
from common.pycoda import Pycoda

@pytest.fixture
def clsJsonFile():
  objRet = JsonFile()
  return objRet

@pytest.fixture
def clsPycoda():
  objRet = Pycoda(os.environ['CODA_API_KEY'])
  return objRet

@pytest.fixture
def clsJsonPlan(clsPycoda, clsJsonFile):
  objRet = JsonPlan(clsPycoda, clsJsonFile.config)
  return objRet