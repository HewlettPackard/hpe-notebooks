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

import abc
import collections
import json
import logging
import os
import traceback

try:
    from simplivity.ovc_client import OVC
    from simplivity.exceptions import HPESimpliVityResourceNotFound
    HAS_HPE_SIMPLIVITY = True
except ImportError:
    HAS_HPE_SIMPLIVITY = False

try:
    from ansible.module_utils import six
    from ansible.module_utils._text import to_native
except ImportError:
    import six
    to_native = str

from ansible.module_utils.basic import AnsibleModule


logger = logging.getLogger(__name__)  # Logger for development purposes


def get_logger(mod_name):
    """
    To activate logs, setup the environment var LOGFILE
    e.g.: export LOGFILE=/tmp/ansible-simplivity.log
    Args:
        mod_name: module name
    Returns: Logger instance`
    """

    logger = logging.getLogger(os.path.basename(mod_name))
    global LOGFILE
    LOGFILE = os.environ.get('LOGFILE')

    if not LOGFILE:
        logger.addHandler(logging.NullHandler())
    else:
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            filename=LOGFILE, filemode='a')
    return logger


def transform_list_to_dict(list_):
    """
    Transforms a list into a dictionary, putting values as keys.

    :arg list list_: List of values
    :return: dict: dictionary built
    """

    ret = {}

    if not list_:
        return ret

    for value in list_:
        if isinstance(value, collections.Mapping):
            ret.update(value)
        else:
            ret[to_native(value)] = True

    return ret


def _str_sorted(obj):
    if isinstance(obj, collections.Mapping):
        return json.dumps(obj, sort_keys=True)
    else:
        return str(obj)


def _standardize_value(value):
    """
    Convert value to string to enhance the comparison.

    :arg value: Any object type.

    :return: str: Converted value.
    """
    if isinstance(value, float) and value.is_integer():
        # Workaround to avoid erroneous comparison between int and float
        # Removes zero from integer floats
        value = int(value)

    return str(value)


def compare(first_resource, second_resource):
    """
    Recursively compares dictionary contents equivalence, ignoring types and elements order.
    Particularities of the comparison:
        - Inexistent key = None
        - These values are considered equal: None, empty, False
        - Lists are compared value by value after a sort, if they have same size.
        - Each element is converted to str before the comparison.
    :arg dict first_resource: first dictionary
    :arg dict second_resource: second dictionary
    :return: bool: True when equal, False when different.
    """
    resource1 = first_resource
    resource2 = second_resource

    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

    # The first resource is True / Not Null and the second resource is False / Null
    if resource1 and not resource2:
        logger.debug("resource1 and not resource2. " + debug_resources)
        return False

    # Checks all keys in first dict against the second dict
    for key in resource1:
        if key not in resource2:
            if resource1[key] is not None:
                # Inexistent key is equivalent to exist with value None
                logger.debug(SimplivityModule.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        # If both values are null, empty or False it will be considered equal.
        elif not resource1[key] and not resource2[key]:
            continue
        elif isinstance(resource1[key], collections.Mapping):
            # recursive call
            if not compare(resource1[key], resource2[key]):
                logger.debug(SimplivityModule.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif isinstance(resource1[key], list):
            # change comparison function to compare_list
            if not compare_list(resource1[key], resource2[key]):
                logger.debug(SimplivityModule.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif _standardize_value(resource1[key]) != _standardize_value(resource2[key]):
            logger.debug(SimplivityModule.MSG_DIFF_AT_KEY.format(key) + debug_resources)
            return False

    # Checks all keys in the second dict, looking for missing elements
    for key in resource2.keys():
        if key not in resource1:
            if resource2[key] is not None:
                # Inexistent key is equivalent to exist with value None
                logger.debug(SimplivityModule.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
    return True


def compare_list(first_resource, second_resource):
    """
    Recursively compares lists contents equivalence, ignoring types and element orders.
    Lists with same size are compared value by value after a sort,
    each element is converted to str before the comparison.
    :arg list first_resource: first list
    :arg list second_resource: second list
    :return: True when equal; False when different.
    """

    resource1 = first_resource
    resource2 = second_resource

    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

    # The second list is null / empty  / False
    if not resource2:
        logger.debug("resource 2 is null. " + debug_resources)
        return False

    if len(resource1) != len(resource2):
        logger.debug("resources have different length. " + debug_resources)
        return False

    resource1 = sorted(resource1, key=_str_sorted)
    resource2 = sorted(resource2, key=_str_sorted)

    for i, val in enumerate(resource1):
        if isinstance(val, collections.Mapping):
            # change comparison function to compare dictionaries
            if not compare(val, resource2[i]):
                logger.debug("resources are different. " + debug_resources)
                return False
        elif isinstance(val, list):
            # recursive call
            if not compare_list(val, resource2[i]):
                logger.debug("lists are different. " + debug_resources)
                return False
        elif _standardize_value(val) != _standardize_value(resource2[i]):
            logger.debug("values are different. " + debug_resources)
            return False

    # no differences found
    return True


class SimplivityModuleException(Exception):
    """
    Simplivity base Exception.

    Attributes:
       msg (str): Exception message.
       simplivity_response (dict): Simplivity rest response.
   """

    def __init__(self, data):
        self.msg = None
        self.simplivity_response = None

        if isinstance(data, six.string_types):
            self.msg = data
        else:
            self.simplivity_response = data

            if data and isinstance(data, dict):
                self.msg = data.get('message')

        if self.simplivity_response:
            Exception.__init__(self, self.msg, self.simplivity_response)
        else:
            Exception.__init__(self, self.msg)


class SimplivityModuleTaskError(SimplivityModuleException):
    """
    Simplivity Task Error Exception.

    Attributes:
       msg (str): Exception message.
       error_code (str): A code which uniquely identifies the specific error.
    """

    def __init__(self, msg, error_code=None):
        super(SimplivityModuleTaskError, self).__init__(msg)
        self.error_code = error_code


class SimplivityModuleValueError(SimplivityModuleException):
    """
    Simplivity Value Error.
    The exception is raised when the data contains an inappropriate value.

    Attributes:
       msg (str): Exception message.
    """
    pass


# @six.add_metaclass(abc.ABCMeta)
class SimplivityModule(object):
    MSG_CREATED = 'Resource created successfully.'
    MSG_UPDATED = 'Resource updated successfully.'
    MSG_DELETED = 'Resource deleted successfully.'
    MSG_ALREADY_PRESENT = 'Resource is already present.'
    MSG_ALREADY_ABSENT = 'Resource is already absent.'
    MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '
    MSG_MANDATORY_FIELD_MISSING = 'Missing mandatory field: name'
    HPE_SIMPLIVITY_SDK_REQUIRED = 'HPE SimpliVity Python SDK is required for this module.'

    SIMPLIVITY_ARGS = dict(
        config=dict(type='path'),
        ovc_ip=dict(type='str'),
        password=dict(type='str', no_log=True),
        username=dict(type='str')
    )

    def __init__(self, additional_arg_spec=None):
        """
        SimplivityModuleBase constructor.

        :arg dict additional_arg_spec: Additional argument spec definition.
        """
        argument_spec = self._build_argument_spec(additional_arg_spec)

        self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

        self.resource_client = None
        self.active_resource = None

        self.state = self.module.params.get('state')
        self.data = self.module.params.get('data')

        self._check_simplivity_sdk()
        self._create_simplivity_client()

        # Preload params for get_all - used by facts
        self.facts_params = self.module.params.get('params') or {}

        # Preload options as dict - used by facts
        self.options = transform_list_to_dict(self.module.params.get('options'))

    def _build_argument_spec(self, additional_arg_spec):
        """
        Creates argument list by merging default arguments with additional arguments.
        """
        merged_arg_spec = dict()
        merged_arg_spec.update(self.SIMPLIVITY_ARGS)

        if additional_arg_spec:
            merged_arg_spec.update(additional_arg_spec)

        return merged_arg_spec

    def _check_simplivity_sdk(self):
        """
        Checks for Simplivity Python SDK
        """
        if not HAS_HPE_SIMPLIVITY:
            self.module.fail_json(msg=self.HPE_SIMPLIVITY_SDK_REQUIRED)

    def _create_simplivity_client(self):
        """
        Creates Simplivity client object using module prams/env variables/config file
        """
        if self.module.params.get('ovc_ip'):
            config = dict(ip=self.module.params['ovc_ip'],
                          credentials=dict(username=self.module.params['username'],
                                           password=self.module.params['password']))
            self.ovc_client = OVC(config)

        elif not self.module.params['config']:
            self.ovc_client = OVC.from_environment_variables()
        else:
            self.ovc_client = OVC.from_json_file(self.module.params['config'])

    def set_resource_object(self, resource_client):
        """
        Sets the resource client and an object of the resource if name of the resource passed.
        """
        self.resource_client = resource_client
        name = None

        if self.data and self.data.get("name"):
            name = self.data["name"]

        elif self.module.params.get("name"):
            name = self.module.params["name"]

        if name:
            try:
                self.active_resource = self.resource_client.get_by_name(name)
            except HPESimpliVityResourceNotFound:
                logger.debug("Resource not found")
        return

    @abc.abstractmethod
    def execute_module(self):
        """
        Abstract method, must be implemented by the inheritor.

        This method is called from the run method. It should contain the module logic

        :return: dict: It must return a dictionary with the attributes for the module result,
            such as ansible_facts, msg and changed.
        """
        pass

    def run(self):
        """
        Common implementation of the Simplivity run modules.

        It calls the inheritor 'execute_module' function and sends the return to the Ansible.

        It handles any SimplivityModuleException in order to signal a failure to Ansible, with a descriptive error message.

        """
        try:
            result = self.execute_module()

            if not result:
                result = {}

            if "changed" not in result:
                result['changed'] = False

            self.module.exit_json(**result)

        except SimplivityModuleException as exception:
            error_msg = '; '.join(to_native(e) for e in exception.args)
            self.module.fail_json(msg=error_msg, exception=traceback.format_exc())

    def resource_absent(self, method='delete'):
        """
        Generic implementation of the absent state for the Simplivity resources.

        It checks if the resource needs to be removed.

        :arg str method: Function of the OVC client that will be called for resource deletion.
            Usually delete or remove.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        if self.active_resource:
            getattr(self.active_resource, method)()

            return {"changed": True, "msg": self.MSG_DELETED}
        else:
            return {"changed": False, "msg": self.MSG_ALREADY_ABSENT}

    def resource_present(self, fact_name, create_method='create'):
        """
        Generic implementation of the present state for the Simplivity resources.

        It checks if the resource needs to be created or updated.

        :arg str fact_name: Name of the fact returned to the Ansible.
        :arg str create_method: Function of the OVC client that will be called for resource creation.
            Usually create or add.
        :return: A dictionary with the expected arguments for the AnsibleModule.exit_json
        """
        changed = False

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        if not self.active_resource:
            self.active_resource = getattr(self.resource_client, create_method)(self.data)
            msg = self.MSG_CREATED
            changed = True
        else:
            changed, msg = self._update_resource()

        data = self.active_resource.data
        return dict(
            msg=msg,
            changed=changed,
            ansible_facts={fact_name: data}
        )

    def _update_resource(self):
        """
        Updates the resource configuration.

        It updates the resource if the requested configuration is
        different from the current configuration.

        :return: Tuple (change flag, message)
        """
        updated_data = self.active_resource.data.copy()
        updated_data.update(self.data)
        changed = False

        if compare(self.active_resource.data, updated_data):
            msg = self.MSG_ALREADY_PRESENT
        else:
            self.active_resource.update(updated_data)
            changed = True
            msg = self.MSG_UPDATED

        return (changed, msg)
