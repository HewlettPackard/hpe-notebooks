# Examples

This directory contains everything you need to start with SimpliVIty and Ansible.

## Running the sample playbooks

**Requirements:** To run these examples you need to execute the [Ansible SimpliVity Setup.](https://github.com/HewlettPackard/simplivity-ansible#setup)

**NOTE:** A sample configuration file is provided within the examples directory. To use it, execute the following steps:

1. `cd` into the `examples` directory.
2. Copy the `simplivity_config-rename.json` file into a new file named `simplivity_config.json`.
3. Modify the file inserting your credentials and OVC IP.

:lock: Tip: Check the `simplivity_config.json` file permissions, since the password is stored in clear-text.

To run an Ansible playbook, execute the following command:

`ansible-playbook -i <path_to_inventory_file> <example_file>.yml`
