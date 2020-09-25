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

import mock
import logging
import pytest
import sys

from module_utils import simplivity

SIMPLIVITY_MODULE_UTILS_PATH = 'module_utils.simplivity'

sys.modules['ansible.module_utils.simplivity'] = simplivity

from copy import deepcopy
from module_utils.simplivity import (SimplivityModule,
                                     OVC,
                                     SimplivityModuleException,
                                     SimplivityModuleValueError,
                                     _str_sorted,
                                     transform_list_to_dict,
                                     compare,
                                     get_logger)

MSG_GENERIC_ERROR = 'Generic error message'
MSG_GENERIC = "Generic message"


class StubResource(SimplivityModule):
    """Stub class to test the resource object"""


class TestSimplivityModule():
    """
    SimplivityModuleSpec provides the mocks used in this test case.
    """
    mock_ovc_client_from_json_file = None
    mock_ovc_client_from_env_vars = None
    mock_ansible_module = None
    mock_ansible_module_init = None
    mock_ovc_client = None

    MODULE_EXECUTE_RETURN_VALUE = dict(
        changed=True,
        msg=MSG_GENERIC,
        ansible_facts={'ansible_facts': None}
    )

    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data={'name': 'testname'}
    )

    RESOURCE_COMMON = {'id': '123456',
                       'name': 'Resource Name'}

    EXPECTED_ARG_SPEC = {'config': {'type': 'path'},
                         'ovc_ip': {'type': 'str'},
                         'password': {'type': 'str', 'no_log': True},
                         'username': {'type': 'str'}}

    @pytest.fixture(autouse=True)
    def setUp(self):
        # Define Simplivity Client Mock (FILE)
        patcher_json_file = mock.patch.object(OVC, 'from_json_file')
        self.mock_ovc_client_from_json_file = patcher_json_file.start()

        # Define Simplivity Client Mock
        self.mock_ovc_client = self.mock_ovc_client_from_json_file.return_value

        # Define Simplivity Client Mock (ENV)
        patcher_env = mock.patch.object(OVC, 'from_environment_variables')
        self.mock_ovc_client_from_env_vars = patcher_env.start()

        # Define Simplivity Module Mock
        patcher_ansible = mock.patch(SimplivityModule.__module__ + '.AnsibleModule')
        self.mock_ansible_module_init = patcher_ansible.start()
        self.mock_ansible_module = mock.Mock()
        self.mock_ansible_module_init.return_value = self.mock_ansible_module

        yield
        patcher_json_file.stop
        patcher_env.stop
        patcher_ansible.stop

    def test_should_call_simplivity_exception_with_a_data(self):
        error = {'message': 'Failure with data'}
        SimplivityModuleException(error)

    def test_should_call_exit_json_properly(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT
        mock_run = mock.Mock()
        mock_run.return_value = self.MODULE_EXECUTE_RETURN_VALUE.copy()

        base_mod = SimplivityModule()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_call_exit_json_adding_changed_false_when_undefined(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.return_value = dict(
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

        base_mod = SimplivityModule()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=MSG_GENERIC,
            ansible_facts={'ansible_facts': None}
        )

    def test_should_load_config_from_file(self):
        self.mock_ansible_module.params = {'config': 'config.json'}

        SimplivityModule()

        self.mock_ovc_client_from_json_file.assert_called_once_with('config.json')
        self.mock_ovc_client_from_env_vars.not_been_called()

    def test_should_load_config_from_environment(self):
        self.mock_ansible_module.params = {'config': None}

        SimplivityModule()

        self.mock_ovc_client_from_env_vars.assert_called_once_with()
        self.mock_ovc_client_from_json_file.not_been_called()

    def test_should_load_config_from_parameters(self):

        params = {'ovc_ip': '10.40.4.245', 'username': 'admin', 'password': 'mypass'}
        params_for_expect = {'ip': '10.40.4.245',
                             'credentials': {'username': 'admin', 'password': 'mypass'}}
        self.mock_ansible_module.params = params

        with mock.patch('module_utils.simplivity.OVC', first='one', second='two') as mock_ovc_client_from_credentials:
            SimplivityModule()

        self.mock_ovc_client_from_env_vars.not_been_called()
        self.mock_ovc_client_from_json_file.not_been_called()
        mock_ovc_client_from_credentials.assert_called_once_with(params_for_expect)

    def test_should_call_fail_json_when_simplivity_sdk_not_installed(self):
        self.mock_ansible_module.params = {'config': 'config.json'}

        with mock.patch(SimplivityModule.__module__ + ".HAS_HPE_SIMPLIVITY", False):
            SimplivityModule()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg='HPE SimpliVity Python SDK is required for this module.')

    def test_additional_argument_spec_construction(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SimplivityModule(additional_arg_spec={'options': 'list'})

        expected_arg_spec = deepcopy(self.EXPECTED_ARG_SPEC)
        expected_arg_spec['options'] = 'list'

        self.mock_ansible_module_init.assert_called_once_with(argument_spec=expected_arg_spec,
                                                              supports_check_mode=False)

    def test_should_call_fail_json_when_simplivity_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = SimplivityModuleException(MSG_GENERIC_ERROR)

        base_mod = SimplivityModule()
        base_mod.execute_module = mock_run
        base_mod.run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=MSG_GENERIC_ERROR)

    def test_should_not_handle_value_error_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = ValueError(MSG_GENERIC_ERROR)

        try:
            base_mod = SimplivityModule()
            base_mod.execute_module = mock_run
            base_mod.run()
        except ValueError as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected ValueError was not raised')

    def test_should_not_handle_exception(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        mock_run = mock.Mock()
        mock_run.side_effect = Exception(MSG_GENERIC_ERROR)

        try:
            base_mod = SimplivityModule()
            base_mod.execute_module = mock_run
            base_mod.run()
        except Exception as e:
            assert(e.args[0] == MSG_GENERIC_ERROR)
        else:
            self.fail('Expected Exception was not raised')

    def test_resource_present_should_create(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ovc_base = SimplivityModule()
        ovc_base.resource_client = mock.Mock()

        resource_obj = StubResource()
        resource_obj.data = self.RESOURCE_COMMON.copy()
        ovc_base.resource_client.create.return_value = resource_obj
        ovc_base.data = {'name': 'Resource Name'}

        facts = ovc_base.resource_present(fact_name="resource")

        expected = self.RESOURCE_COMMON.copy()

        ovc_base.resource_client.create.assert_called_once_with({'name': 'Resource Name'})

        assert facts == dict(changed=True,
                             msg=SimplivityModule.MSG_CREATED,
                             ansible_facts=dict(resource=expected))

    def test_resource_present_should_not_update_when_data_is_equals(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ovc_base = SimplivityModule()
        ovc_base.resource_client = mock.Mock()
        ovc_base.data = self.RESOURCE_COMMON.copy()

        ovc_base.resource_client.get_by_name.return_value = mock.Mock()
        ovc_base.set_resource_object(ovc_base.resource_client)
        ovc_base.active_resource.data = self.RESOURCE_COMMON.copy()

        facts = ovc_base.resource_present(fact_name="resource")
        assert facts == dict(changed=False,
                             msg=SimplivityModule.MSG_ALREADY_PRESENT,
                             ansible_facts=dict(resource=self.RESOURCE_COMMON.copy()))

    def test_resource_present_should_update_when_data_has_modified_attributes(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ovc_base = SimplivityModule()
        ovc_base.resource_client = mock.Mock()
        resource_obj = StubResource()
        updated_value = self.RESOURCE_COMMON.copy()
        updated_value['name'] = 'Resource Name New'
        resource_obj.data = updated_value

        ovc_base.resource_client.get_by_name.return_value = mock.Mock()
        ovc_base.set_resource_object(ovc_base.resource_client)
        ovc_base.active_resource.data = self.RESOURCE_COMMON.copy()

        ovc_base.data = {'newName': 'Resource Name New'}
        facts = ovc_base.resource_present('resource')

        expected = self.RESOURCE_COMMON.copy()
        expected['name'] = 'Resource Name New'

        ovc_base.active_resource.update.assert_called_once_with(expected)

        assert dict(changed=facts['changed'], msg=facts['msg']) == dict(changed=True,
                                                                        msg=SimplivityModule.MSG_UPDATED)

    def test_resource_absent_should_remove(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ovc_base = SimplivityModule()
        ovc_base.resource_client = mock.Mock()
        ovc_base.resource_client.get_by_name.return_value = mock.Mock()
        ovc_base.set_resource_object(ovc_base.resource_client)

        facts = ovc_base.resource_absent()
        ovc_base.active_resource.delete.assert_called_once_with()

        assert facts == dict(changed=True,
                             msg=SimplivityModule.MSG_DELETED)

    def test_resource_absent_should_do_nothing_when_not_exist(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        ovc_base = SimplivityModule()
        ovc_base.resource_client = mock.Mock()
        ovc_base.resource_client.get_by_name.return_value = None
        ovc_base.set_resource_object(ovc_base.resource_client)

        facts = ovc_base.resource_absent()

        assert facts == dict(changed=False,
                             msg=SimplivityModule.MSG_ALREADY_ABSENT)


if __name__ == '__main__':
    pytest.main([__file__])
