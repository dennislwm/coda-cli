import json
import logging
import os

class JsonFile():
  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                   C O N S T R U C T O R                                  |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""

  def __init__(self, file='config.json'):
    assert not file is None
    assert os.path.exists(file) == True
    with open(file, mode='r') as f:
      config = json.load(f)
      f.close()
    self.config = config

class JsonPlan(object):
  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                                   C O N S T R U C T O R                                  |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""

  def __init__(self, client, config):
    assert(client)
    assert(isinstance(config, dict))

    self.client = client
    self.log = logging.getLogger()
    self.log.setLevel(logging.INFO)
    self.checkSum = True
    self.config = self.create_plan(config)
    if not self.checkSum:
      self.log.info(json.dumps(self.config))

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                        E X T E R N A L   C L A S S   M E T H O D S                       |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""

  def get_plan(self, output="json"):
    return json.dumps(self.config) if output == "json" else self.config

  """--------+---------+---------+---------+---------+---------+---------+---------+---------|
  |                        I N T E R N A L   C L A S S   M E T H O D S                       |
  |----------+---------+---------+---------+---------+---------+---------+---------+-------"""

  def create_plan(self, config):
    if config is None:
      assert config
    # Terminate condition int or str
    if isinstance(config, int):
      return config
    elif isinstance(config, str):
      return config
    elif isinstance(config, dict):
      data = {}
      for key, val in config.items():
        val = self.create_plan(val)
        data[key] = val
    elif isinstance(config, list):
      data = []
      for i, var in enumerate(config):
        var = self.create_plan(var)
        data.append(var)
    else:
      data = config
      self.log.info("[WARNING][create_plan] unknown data type " + str(type(config)))
    return data
