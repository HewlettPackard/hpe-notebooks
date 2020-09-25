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
module: simplivity_cluster_facts
short_description: Retrieves the facts about one or more OmniStack clusters
description:
    - Retrieves the facts about one or more OmniStack clusters from SimpliVity.
version_added: 1.0.0
requirements:
    - python >= 3.3
    - simplivity >= 1.0.0
author:
    - Sijeesh Kattumunda (@sijeesh)
options:
    name:
      description:
        - OmniStack cluster name.
    options:
      description:
        - 'List with options to gather additional facts about a OmniStack cluster'
'''

EXAMPLES = '''
- name: Gather facts about all OmniStack clusters
  simplivity_cluster_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- name: Get all OmniStack clusters with filters
  simplivity_cluster_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a OmniStack cluster by name
  simplivity_cluster_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost
'''

RETURN = '''
clusters:
    description: Facts about the SimpliVity OmniStack clusters
    returned: Always, but can be empty list.
    type: list
'''

from ansible.module_utils.simplivity import SimplivityModule


class ClusterFactsModule(SimplivityModule):

    def __init__(self):
        argument_spec = dict(name=dict(type='str'),
                             options=dict(type='list'),
                             params=dict(type='dict'))

        super(ClusterFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.set_resource_object(self.ovc_client.omnistack_clusters)

    def execute_module(self):
        facts = {'clusters': []}

        if self.module.params['name'] and self.active_resource:
            facts["clusters"].append(self.active_resource.data)
        elif not self.module.params['name']:
            clusters = self.resource_client.get_all(**self.facts_params)
            for cluster in clusters:
                facts["clusters"].append(cluster.data)

        return dict(changed=False, ansible_facts=facts)


def main():
    ClusterFactsModule().run()


if __name__ == '__main__':
    main()
