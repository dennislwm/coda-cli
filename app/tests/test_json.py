import pytest

def test_jsonplan(clsJsonPlan):
  output = clsJsonPlan.get_plan()
  assert '{"coda": {"docs": [' in output