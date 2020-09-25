#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2017) Hewlett Packard Enterprise Development LP
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

"""
This module was created because the code in this repository is shared with Ansible Core.
So, to avoid merging issues, and maintaining the tests code equal, we create a unique file to
configure the imports that change from one repository to another.
"""

import sys
from module_utils import simplivity

SIMPLIVITY_MODULE_UTILS_PATH = 'module_utils.simplivity'

sys.modules['ansible.module_utils.simplivity'] = simplivity

from module_utils.simplivity import (SimplivityModule,
                                     OVC,
                                     SimplivityModuleException,
                                     SimplivityModuleTaskError,
                                     SimplivityModuleValueError,
                                     _str_sorted,
                                     transform_list_to_dict,
                                     compare,
                                     get_logger)

from simplivity_virtual_machine import VirtualMachineModule
from simplivity_virtual_machine_facts import VirtualMachineFactsModule
from simplivity_backup_facts import BackupFactsModule
from simplivity_datastore_facts import DatastoreFactsModule
from simplivity_host_facts import HostFactsModule
from simplivity_cluster_facts import ClusterFactsModule
from simplivity_policy_facts import PolicyFactsModule
