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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: simplivity_virtual_machine
short_description: Manage SimpliVIty Virtual Machine resource
description:
    - Provides an interface to do operations supported by SimpliVity VM resource
version_added: 1.0.0
requirements:
    -  python >= 3.3
    -  simplivity >= 1.0.0
author: Sijeesh Kattumunda (@kattumun)
options:
    state:
        description:
            - Indicates the desired state of the SimpliVity VM
              C(set_policy_for_multiple_vms) Helps to set a policy for multiple VMs
              C(clone) Performs clone operation
              C(move) Performs move operation
              C(create_backup) Creates a backup of the VM
              C(set_backup_parameters) Sets backup parameters for a VM
              C(set_policy) Set policy for a single VM
        choices: ['set_policy_for_multiple_vms',
                  'clone',
                  'move',
                  'create_backup',
                  'set_backup_parameters',
                  'set_policy']
    data:
        description:
            - Dict with Virtual Machine properties
        required: true
notes:
    - 'This resource does not support create and update operations'
'''

EXAMPLES = '''
- name: 'Set policy for multiple VMs'
  simplivity_virtual_machine:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    state: set_policy_for_multiple_vms
    data:
      vm_names:
        - 'vm1'
        - 'vm2'
      policy_name: 'policy name'
  delegate_to: localhost

- name: 'Simplivity clone'
  simplivity_virtual_machine:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    state: clone
    data:
      name: 'vm1'
      new_name: 'vm2'
  delegate_to: localhost

- name: 'Simplivity clone and move to another datastore'
  simplivity_virtual_machine:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    state: clone
    data:
      name: 'vm1'
      new_name: 'vm2'
      datastore: 'Datastore name'
  delegate_to: localhost

- name: 'Simplivity move VM to another datastore'
  simplivity_virtual_machine:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    state: move
    data:
      name: 'vm1'
      new_name: 'vm2'
      datastore_name: 'Datastore name'
  delegate_to: localhost

- name: 'Simplivity create VM backup'
  simplivity_virtual_machine:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    state: backup
    data:
      name: 'vm'
      backup_name: 'backup'
      cluster_name: null
      app_consistent: false
      consistency_type: null
'''

RETURN = '''
virtual_machine:
    description: Has the SimpliVity facts about a VM.
    returned: On states 'set_backup_parameters' and 'set_policy'.
    type: dict

policy_updated_vms:
    description: Has the SimpliVity facts about the policy updated VMs
    returned: On states 'set_policy_for_multiple_vms'.
    type: list

cloned_vm:
    description: Has the SimpliVity facts about the cloned VM.
    returned: On states 'clone'.
    type: dict

moved_vm:
    description: Has the SimpliVity facts about the moved VM.
    returned: On states 'move'.
    type: dict

backup:
    description: Has the SimpliVity facts about the backup of a VM.
    returned: On states 'backup'.
    type: dict
'''

from ansible.module_utils.simplivity import SimplivityModule
from simplivity import exceptions


class VirtualMachineModule(SimplivityModule):

    MSG_UPDATED_POLICY_OF_MULTIPLE_VMS = "Updated policy of the VMs successfully."
    MSG_POLICY_ALREADY_APPLIED = "Policy has allready been applied to all of the requested VMs."
    MSG_CLONED_SUCCESSFULLY = "Cloned successfully."
    MSG_VM_WITH_SAME_NAME_EXISTS = "VM with the same name already exists."
    MSG_MOVED_SUCCESSFULLY = "Moved VM to datastore successfully"
    MSG_BACKUP_CREATED = "Created backup successfully"
    MSG_BACKUP_EXISTS = "Backup exists with the same name"
    MSG_CREATED_BACKUP_PARAMETERS = "Successfully set the backup parameters"
    MSG_SET_VM_POLICY = "Successfully set the VM policy"
    MSG_VM_POLICY_ALREADY_APPLIED = "Policy has allready been applied to this VM"

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['set_policy_for_multiple_vms',
                     'clone',
                     'move',
                     'backup',
                     'set_backup_parameters',
                     'set_policy']
        ),
        data=dict(required=True, type='dict'),
    )

    def __init__(self):
        super(VirtualMachineModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.set_resource_object(self.ovc_client.virtual_machines)

    def execute_module(self):
        params = self.module.params.get("params")
        self.params = params if params else {}

        if self.active_resource:
            if self.state == 'clone':
                changed, msg, fact = self.__clone()
            elif self.state == 'move':
                changed, msg, fact = self.__move()
            elif self.state == 'backup':
                changed, msg, fact = self.__create_backup()
            elif self.state == 'set_backup_parameters':
                changed, msg, fact = self.__set_backup_parameters()
            elif self.state == 'set_policy':
                changed, msg, fact = self.__set_policy()
        else:
            if self.state == 'set_policy_for_multiple_vms':
                changed, msg, fact = self.__set_policy_for_multiple_vms()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=fact)

    def __set_policy_for_multiple_vms(self):
        changed = True
        message = self.MSG_UPDATED_POLICY_OF_MULTIPLE_VMS

        policy_name = self.data["policy_name"]
        vm_name_list = self.data["vm_names"]

        policy = self.ovc_client.policies.get_by_name(policy_name)
        vms = [self.resource_client.get_by_name(vm_name) for vm_name in vm_name_list]

        vms_using_policy = policy.get_vms()
        vms_to_exclude = [vm.data["id"] for vm in vms_using_policy]
        final_vm_list = [vm for vm in vms if vm.data["id"] not in vms_to_exclude]

        if final_vm_list:
            self.resource_client.set_policy_for_multiple_vms(policy, final_vm_list)
        else:
            changed = False
            message = self.MSG_POLICY_ALREADY_APPLIED

        updated_vm_names = [vm.data["name"] for vm in final_vm_list]
        return changed, message, {'policy_updated_vms': updated_vm_names}

    def __clone(self):
        changed = True
        message = self.MSG_CLONED_SUCCESSFULLY

        new_vm_name = self.data["new_name"]
        app_consistent = self.data.get("app_consistent", False)
        datastore = self.data.get("datastore", None)

        try:
            self.resource_client.get_by_name(new_vm_name)
            changed = False
            message = self.MSG_VM_WITH_SAME_NAME_EXISTS
            data = {}
        except exceptions.HPESimpliVityResourceNotFound:
            cloned_vm = self.active_resource.clone(new_vm_name, app_consistent, datastore)
            data = cloned_vm.data

        return changed, message, {'cloned_vm': data}

    def __move(self):
        changed = True
        message = self.MSG_MOVED_SUCCESSFULLY

        vm_name = self.data["name"]
        new_vm_name = self.data["new_name"]
        datastore_name = self.data.get("datastore_name", None)

        filters = {'name': vm_name}
        if datastore_name:
            filters['datastore_name'] = datastore_name

        result = self.resource_client.get_all(filters=filters)
        if not result:
            moved_vm = self.active_resource.move(new_vm_name, datastore_name)
            data = moved_vm.data
        else:
            data = {}
            changed = False
            message = self.MSG_VM_WITH_SAME_NAME_EXISTS

        return changed, message, {'moved_vm': data}

    def __create_backup(self):
        changed = True
        message = self.MSG_BACKUP_CREATED

        backup_name = self.data["backup_name"]
        cluster_name = self.data.get("cluster_name", None)
        app_consistent = self.data.get("app_consistent", False)
        consistency_type = self.data.get("consistency_type", None)
        retention = self.data.get("retention", 0)

        try:
            backup = self.ovc_client.backups.get_by_name(backup_name)
            changed = False
            message = self.MSG_BACKUP_EXISTS
            data = {}
        except exceptions.HPESimpliVityResourceNotFound:
            backup = self.active_resource.create_backup(backup_name,
                                                        cluster_name,
                                                        app_consistent,
                                                        consistency_type,
                                                        retention)
            data = backup.data

        return changed, message, {'backup': data}

    def __set_backup_parameters(self):
        changed = True
        message = self.MSG_CREATED_BACKUP_PARAMETERS

        guest_username = self.data["guest_username"]
        guest_password = self.data["guest_password"]
        override_guest_validation = self.data.get("override_guest_validation", False)
        app_aware_type = self.data.get("app_aware_type", None)

        self.active_resource.set_backup_parameters(guest_username,
                                                   guest_password,
                                                   override_guest_validation,
                                                   app_aware_type)

        return changed, message, {'virtual_machine': self.active_resource.data}

    def __set_policy(self):
        changed = True
        message = self.MSG_SET_VM_POLICY

        policy_name = self.data["policy_name"]
        policy = self.ovc_client.policies.get_by_name(policy_name)

        vms_using_this_policy = policy.get_vms()
        vm_ids = [vm.data["id"] for vm in vms_using_this_policy]

        if self.active_resource.data["id"] in vm_ids:
            changed = False
            message = self.MSG_VM_POLICY_ALREADY_APPLIED
            data = {}
        else:
            self.active_resource.set_policy(policy)
            data = self.active_resource.data

        return changed, message, {'virtual_machine': data}


def main():
    VirtualMachineModule().run()


if __name__ == '__main__':
    main()
