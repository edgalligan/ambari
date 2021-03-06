#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from resource_management.core.exceptions import Fail

class ConfigDictionary(dict):
  """
  Immutable config dictionary
  """
  
  def __init__(self, dictionary, allow_overwrite=False):
    """
    Recursively turn dict to ConfigDictionary
    """
    self.__allow_overwrite = allow_overwrite
    for k, v in dictionary.iteritems():
      if isinstance(v, dict):
        dictionary[k] = ConfigDictionary(v, allow_overwrite=allow_overwrite)
        
    super(ConfigDictionary, self).__init__(dictionary)

  def __setitem__(self, name, value):
    if self.__allow_overwrite:
      super(ConfigDictionary, self).__setitem__(name, value)
    else:
      raise Fail("Configuration dictionary is immutable!")

  def __getitem__(self, name):
    """
    - use Python types
    - enable lazy failure for unknown configs. 
    """
    try:
      value = super(ConfigDictionary, self).__getitem__(name)
    except KeyError:
      return UnknownConfiguration(name)
      
    
    if value == "true":
      value = True
    elif value == "false":
      value = False
    else: 
      try:
        value = int(value)
      except (ValueError, TypeError):
        try:
          value =  float(value)
        except (ValueError, TypeError):
          pass
    
    return value


class UnknownConfiguration():
  """
  Lazy failing for unknown configs.
  """
  def __init__(self, name):
    self.name = name
   
  def __getattr__(self, name):
    raise Fail("Configuration parameter '" + self.name + "' was not found in configurations dictionary!")
  
  def __getitem__(self, name):
    """
    Allow [] 
    """
    return self