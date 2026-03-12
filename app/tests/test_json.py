import pytest

def test_jsonplan(clsJsonPlan):
  # plumb:req-f73a4adf
  output = clsJsonPlan.get_plan()
  assert '{"coda": {"docs": [' in output