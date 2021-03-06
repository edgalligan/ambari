#!/usr/bin/env python
"""
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

"""

from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import check_process_status, format

# Note: Phoenix Query Server is only applicable to HDP-2.3 and above.
def phoenix_service(action = 'start'): # 'start', 'stop', 'status'
    # Note: params/status_params should already be imported before calling phoenix_service()
    pid_file = format("{pid_dir}/phoenix-{hbase_user}-server.pid")
    no_op_test = format("ls {pid_file} >/dev/null 2>&1 && ps -p `cat {pid_file}` >/dev/null 2>&1")

    if action == "status":
      check_process_status(pid_file)
    else:
      env = {'JAVA_HOME': format("{java64_home}"), 'HBASE_CONF_DIR': format("{hbase_conf_dir}")}
      daemon_cmd = format("{phx_daemon_script} {action}")
      if action == 'start':
        Execute(daemon_cmd,
                user=format("{hbase_user}"),
                environment=env)
  
      elif action == 'stop':
        Execute(daemon_cmd,
                timeout = 30,
                on_timeout = format("! ( {no_op_test} ) || {sudo} -H -E kill -9 `cat {pid_file}`"),
                user=format("{hbase_user}"),
                environment=env
        )
        Execute(format("rm -f {pid_file}"))
