#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2019) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

class ModuleDocFragment(object):
    # Simplivity doc fragment
    DOCUMENTATION = '''
options:
    config:
      description:
        - Path to a .json configuration file containing the Simplivity client configuration.
          The configuration file is optional. If the file path is not provided, the configuration will be loaded from
          environment variables.
      required: false

notes:
    - "A sample configuration file for the config parameter can be found at:
       U(https://github.com/HewlettPackard/simplivity-ansible/blob/master/examples/simplivity_config-rename.json)"
    - "Check how to use environment variables for configuration at:
       U(https://github.com/HewlettPackard/simplivity-ansible#environment-variables)"
    - "Additional Playbooks for the HPE Simplivity Ansible modules can be found at:
       U(https://github.com/HewlettPackard/simplivity-ansible/tree/master/examples)"
    '''
