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
module: simplivity_host_facts
short_description: Retrieves the facts about one or more Hosts
description:
    - Retrieves the facts about one or more Hosts from SimpliVity.
version_added: 1.0.0
requirements:
    - python >= 3.3
    - simplivity >= 1.0.0
author:
    - Sijeesh Kattumunda (@sijeesh)
options:
    name:
      description:
        - Host name.
    options:
      description:
        - 'List with options to gather additional facts about a Host'
'''

EXAMPLES = '''
- name: Gather facts about all Hosts
  simplivity_host_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- name: Get all Hosts with filters
  simplivity_host_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a Host by name
  simplivity_host_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost
'''

RETURN = '''
hosts:
    description: Facts about the SimpliVity hosts
    returned: Always, but can be empty list.
    type: list
'''

from ansible.module_utils.simplivity import SimplivityModule


class HostFactsModule(SimplivityModule):

    def __init__(self):
        argument_spec = dict(name=dict(type='str'),
                             options=dict(type='list'),
                             params=dict(type='dict'))

        super(HostFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.ovc_client.hosts)

    def execute_module(self):
        facts = {'hosts': []}

        if self.module.params['name'] and self.active_resource:
            facts["hosts"].append(self.active_resource.data)
        elif not self.module.params['name']:
            hosts = self.resource_client.get_all(**self.facts_params)
            for host in hosts:
                facts["hosts"].append(host.data)

        return dict(changed=False, ansible_facts=facts)


def main():
    HostFactsModule().run()


if __name__ == '__main__':
    main()
