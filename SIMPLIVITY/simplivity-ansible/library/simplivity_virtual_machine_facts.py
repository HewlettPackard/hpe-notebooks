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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: simplivity_virtual_machine_facts
short_description: Retrieves the facts about one or more Virtual Machines
description:
    - Retrieves the facts about one or more Virtual Machines from SimpliVity.
version_added: 1.0.0
requirements:
    - python >= 3.3
    - simplivity >= 1.0.0
author:
    - Sijeesh Kattumunda (@sijeesh)
options:
    name:
      description:
        - Virtual Machine name
    options:
      description:
        - 'List with options to gather additional facts about a Virtual Machine
          Options allowed: C(bakups)'
'''

EXAMPLES = '''
- name: Gather facts about all Virtual Machines
  simplivity_virtual_machine_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- debug: var=virtual_machines

- name: Get all VMs with filters
  simplivity_virtual_machine_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a VM by name
  simplivity_virtual_machine_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost

- name: Gather facts about a VM by name with options
  simplivity_virtual_machine_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
    options:
      - backups
  delegate_to: localhost
'''

RETURN = '''
virtual_machines:
    description: Facts about the SimpliVity Virtual Machines
    returned: Always, but can be empty list.
    type: list

backups:
    description: Facts about all the backups of a SimpliVity Virtual Machine.
    returned: Always, but can be empty list
    type: list
'''

from ansible.module_utils.simplivity import SimplivityModule


class VirtualMachineFactsModule(SimplivityModule):

    def __init__(self):
        argument_spec = dict(name=dict(type='str'),
                             options=dict(type='list'),
                             params=dict(type='dict'))

        super(VirtualMachineFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.ovc_client.virtual_machines)

    def execute_module(self):
        facts = {'virtual_machines': []}

        if self.module.params['name'] and self.active_resource:
            facts["virtual_machines"].append(self.active_resource.data)

            if self.options.get("backups"):
                backup_data_list = []
                backups = self.active_resource.get_backups()
                for backup in backups:
                    backup_data_list.append(backup.data)
                facts["backups"] = backup_data_list

        elif not self.module.params['name']:
            vms = self.resource_client.get_all(**self.facts_params)
            for vm in vms:
                facts["virtual_machines"].append(vm.data)

        return dict(changed=False, ansible_facts=facts)


def main():
    VirtualMachineFactsModule().run()


if __name__ == '__main__':
    main()
