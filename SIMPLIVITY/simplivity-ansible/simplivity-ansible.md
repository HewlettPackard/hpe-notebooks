# Ansible HPE Simplivity Modules

### Modules

  * [simplivity_backup_facts - Retrieves the facts about one or more Backups](#simplivity_backup_facts)
  * [simplivity_cluster_facts - Retrieves the facts about one or more OmniStack clusters](#simplivity_cluster_facts)
  * [simplivity_datastore_facts - Retrieves the facts about one or more Datastores](#simplivity_datastore_facts)
  * [simplivity_host_facts - Retrieves the facts about one or more Hosts](#simplivity_host_facts)
  * [simplivity_policy_facts - Retrieves the facts about one or more Policies](#simplivity_policy_facts)
  * [simplivity_virtual_machine - Manage SimpliVIty Virtual Machine resource](#simplivity_virtual_machine)
  * [simplivity_virtual_machine_facts - Retrieves the facts about one or more Virtual Machines](#simplivity_virtual_machine_facts)

---

## simplivity_backup_facts
Retrieves the facts about one or more Backups

#### Synopsis
 Retrieves the facts about one or more Backups from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  Backup name.  |
| options  |   |  | |  List with options to gather additional facts about a Backup  |


 
#### Examples

```yaml

- name: Gather facts about all Backups
  simplivity_backup_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- name: Get all VMs with filters
  simplivity_backup_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a Backup by name
  simplivity_backup_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| backups   | Facts about the SimpliVity backups |  Always, but can be empty list. |  list |



---


## simplivity_cluster_facts
Retrieves the facts about one or more OmniStack clusters

#### Synopsis
 Retrieves the facts about one or more OmniStack clusters from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  OmniStack cluster name.  |
| options  |   |  | |  List with options to gather additional facts about a OmniStack cluster  |


 
#### Examples

```yaml

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

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| clusters   | Facts about the SimpliVity OmniStack clusters |  Always, but can be empty list. |  list |



---


## simplivity_datastore_facts
Retrieves the facts about one or more Datastores

#### Synopsis
 Retrieves the facts about one or more Datastores from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  Backup name.  |
| options  |   |  | |  List with options to gather additional facts about a Datastores  |


 
#### Examples

```yaml

- name: Gather facts about all Datastores
  simplivity_datastore_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- name: Get all VMs with filters
  simplivity_datastore_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a Datastore by name
  simplivity_datastore_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| datastores   | Facts about the SimpliVity datastores |  Always, but can be empty list. |  list |



---


## simplivity_host_facts
Retrieves the facts about one or more Hosts

#### Synopsis
 Retrieves the facts about one or more Hosts from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  Host name.  |
| options  |   |  | |  List with options to gather additional facts about a Host  |


 
#### Examples

```yaml

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

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| hosts   | Facts about the SimpliVity hosts |  Always, but can be empty list. |  list |



---


## simplivity_policy_facts
Retrieves the facts about one or more Policies

#### Synopsis
 Retrieves the facts about one or more Policies from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  Policy name.  |
| options  |   |  | |  List with options to gather additional facts about a Policy  |


 
#### Examples

```yaml

- name: Gather facts about all Policies
  simplivity_policy_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
  delegate_to: localhost

- name: Get all Policies with filters
  simplivity_policy_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    params:
      filters:
        name: '{{ name }}'

- name: Gather facts about a Policy by name
  simplivity_policy_facts:
    ovc_ip: <ip>
    username: <username>
    password: <password>
    name: '{{ name }}'
  delegate_to: localhost

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| policies   | Facts about the SimpliVity policies |  Always, but can be empty list. |  list |



---


## simplivity_virtual_machine
Manage SimpliVIty Virtual Machine resource

#### Synopsis
 Provides an interface to do operations supported by SimpliVity VM resource

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| data  |   Yes  |  | |  Dict with Virtual Machine properties  |
| state  |   |  | <ul> <li>set_policy_for_multiple_vms</li>  <li>clone</li>  <li>move</li>  <li>create_backup</li>  <li>set_backup_parameters</li>  <li>set_policy</li> </ul> |  Indicates the desired state of the SimpliVity VM `set_policy_for_multiple_vms` Helps to set a policy for multiple VMs `clone` Performs clone operation `move` Performs move operation `create_backup` Creates a backup of the VM `set_backup_parameters` Sets backup parameters for a VM `set_policy` Set policy for a single VM  |


 
#### Examples

```yaml

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

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| backup   | Has the SimpliVity facts about the backup of a VM. |  On states 'backup'. |  dict |
| cloned_vm   | Has the SimpliVity facts about the cloned VM. |  On states 'clone'. |  dict |
| moved_vm   | Has the SimpliVity facts about the moved VM. |  On states 'move'. |  dict |
| policy_updated_vms   | Has the SimpliVity facts about the policy updated VMs |  On states 'set_policy_for_multiple_vms'. |  list |
| virtual_machine   | Has the SimpliVity facts about a VM. |  On states 'set_backup_parameters' and 'set_policy'. |  dict |


#### Notes

- This resource does not support create and update operations


---


## simplivity_virtual_machine_facts
Retrieves the facts about one or more Virtual Machines

#### Synopsis
 Retrieves the facts about one or more Virtual Machines from SimpliVity.

#### Requirements (on the host that executes the module)
  * python >= 3.3
  * simplivity >= 1.0.0

#### Options

| Parameter     | Required    | Default  | Choices    | Comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   |  | |  Virtual Machine name  |
| options  |   |  | |  List with options to gather additional facts about a Virtual Machine Options allowed: `bakups`  |


 
#### Examples

```yaml

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

```



#### Return Values

| Name          | Description  | Returned | Type       |
| ------------- |-------------| ---------|----------- |
| backups   | Facts about all the backups of a SimpliVity Virtual Machine. |  Always, but can be empty list |  list |
| virtual_machines   | Facts about the SimpliVity Virtual Machines |  Always, but can be empty list. |  list |



---

