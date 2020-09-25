[![Build Status](https://travis-ci.com/HewlettPackard/simplivity-ansible.svg?branch=master)](https://travis-ci.com/HewlettPackard/simplivity-ansible)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/simplivity-ansible/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/simplivity-ansible?branch=master)

# Ansible Modules for HPE SimpliVity

Modules to manage HPE SimpliVity using Ansible playbooks.

## Requirements

 - Ansible >= 2.5
 - Python >= 3.3
 - HPE SimpliVity Python SDK
 
## Modules

Each SimpliVity resource operation is exposed through an Ansible module. We also provide a specific module to gather facts about the resource.

The detailed documentation for each module is available at: [HPE SimpliVity Ansible Modules Documentation](simplivity-ansible.md)

### Example playbook

```yml
- hosts: all
  vars:
    config: "{{ playbook_dir }}/simplivity_config.json"
    vm_1_name: <vm_name>
    vm_2_name: <vm_name>
    datastore_name: <datastore_name>
    policy_name: <policy_name>
  tasks:
    - name: 'Set policy for multiple VMs'
      simplivity_virtual_machine:
        config: "{{ config }}"
        state: set_policy_for_multiple_vms
        data:
          vm_names:
            - '{{ vm_1_name }}'
            - '{{ vm_2_name }}'
          policy_name: '{{ policy_name }}'
      delegate_to: localhost

    - name: 'Simplivity clone'
      simplivity_virtual_machine:
        config: "{{ config }}"
        state: clone
        data:
          name: '{{ vm_1_name }}'
          new_name: '{{ vm_1_name}}_clone_test'
      delegate_to: localhost

    - name: 'Simplivity clone and move to another datastore'
      simplivity_virtual_machine:
        config: "{{ config }}"
        state: clone
        data:
          name: '{{ vm_1_name }}_clone_test'
          new_name: '{{ vm_1_name }}_clone_and_move_test'
          datastore: '{{ datastore_name }}'
      delegate_to: localhost

    - name: 'Simplivity create VM backup'
      simplivity_virtual_machine:
        config: "{{ config }}"
        state: backup
        data:
          name: '{{ vm_1_name }}'
          backup_name: '{{ vm_1_name }}_backup'
          cluster_name: null
          app_consistent: false
          consistency_type: null
          retention: 0
      delegate_to: localhost
```

## Setup

To perform a full installation, you should execute the following steps:

### 1. Clone the repository

Run:

```bash
$ git clone https://github.com/HewlettPackard/simplivity-ansible.git
```

### 2. Install dependency packages

Run pip command from the cloned directory:
    
  ```bash
  pip install -r requirements.txt
  ```
  
### 3. Configure the ANSIBLE_LIBRARY environmental variable

Set the environment variables `ANSIBLE_LIBRARY` and `ANSIBLE_MODULE_UTILS`, specifying the `library` full path from the cloned project:

```bash
$ export ANSIBLE_LIBRARY=/path/to/simplivity-ansible/library
$ export ANSIBLE_MODULE_UTILS=/path/to/simplivity-ansible/library/module_utils/
```

### 4. SimpliVity client Configuration

#### Using a JSON Configuration File

To use the Ansible SimpliVity modules, you can store the configuration on a JSON file. 
```json
{
  "ip": "10.30.4.56",
  "credentials": {
    "username": "username",
    "password": "password"
  }
}
```

:lock: Tip: Check the file permissions since the password is stored in clear-text.

The configuration file path must be provided for all of the playbooks `config` arguments. For example:

```yml
- name: Gather facts about SimpliVity virtual machine'
  simplivity_virtual_machine_facts:
    config: "/path/to/config.json"
    name: "VM name"
```

#### Environment Variables

If you prefer, the configuration can also be stored in environment variables.

```bash
# Required
export SIMPLIVITYSDK_OVC_IP='10.30.4.56'
export SIMPLIVITYSDK_USERNAME='username'
export SIMPLIVITYSDK_PASSWORD='password'

# Optional
export SIMPLIVITYSDK_SSL_CERTIFICATE='<path_to_cert.crt_file>'
export SIMPLIVITYSDK_CONNECTION_TIMEOUT='<connection time-out in seconds>'
```

:lock: Tip: Make sure no unauthorised person has access to the environment variables, since the password is stored in clear-text.

In this case, you shouldn't provide the `config` argument. For example:

```yml
- name: Gather facts about SimpliVity virtual machine'
  simplivity_virtual_machine_facts:
    name: "VM name"
```

Once you have defined the environment variables, you can run the plays.

#### Parameters in the playbook

The third way to pass in your OVC credentials to your tasks is through explicit specification on the task.

This option allows the parameters `ovc_ip`, `username`, `password` to be passed directly inside your task.

```yaml
- name: Gather facts about SimpliVity virtual machine'
  simplivity_virtual_machine_facts:
    ovc_ip: 10.30.4.56
    username: username
    password: password
    name: "VM name"
  no_log: true
  delegate_to: localhost
```

Setting `no_log: true` is highly recommended in this case, as the credentials are otherwise returned in the log after task completion.

## License

This project is licensed under the Apache 2.0 license. Please see the [LICENSE](LICENSE) for more information.

## Contributing and feature requests

**Contributing:** We welcome your contributions to the Ansible Modules for HPE SimpliVity. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

**Feature Requests:** If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

## Testing

The basic test execution can be achieved by executing the `build.sh` file.

Please refer to [TESTING.md](TESTING.md) for further testing information.
