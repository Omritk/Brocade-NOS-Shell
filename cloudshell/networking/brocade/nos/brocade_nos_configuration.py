import re
from cloudshell.networking.brocade.autoload.brocade_generic_snmp_autoload import BrocadeGenericSNMPAutoload
from cloudshell.networking.brocade.brocade_configuration_operations import BrocadeConfigurationOperations
from cloudshell.networking.brocade.brocade_connectivity_operations import BrocadeConnectivityOperations
from cloudshell.networking.brocade.brocade_send_command_operations import BrocadeSendCommandOperations
from cloudshell.networking.brocade.nos.brocade_nos_configuration_operations import BrocadeNOSConfigurationOperations
from cloudshell.shell.core.context_utils import get_decrypted_password_by_attribute_name_wrapper


DEFAULT_PROMPT = '[#>]\s*$'
ENABLE_PROMPT = '#\s*$'
CONFIG_MODE_PROMPT = '\(conf.*\)#\s*$'


def send_default_actions(session):
    """Send default commands to configure/clear session outputs
    :return:
    """
    enter_enable_mode(session=session)
    session.hardware_expect('terminal length 0', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)
    session.hardware_expect(ENTER_CONFIG_MODE_PROMPT_COMMAND, CONFIG_MODE_PROMPT)
    #session.hardware_expect('no logging console', CONFIG_MODE_PROMPT)
    session.hardware_expect('exit', DEFAULT_PROMPT+'|'+ENABLE_PROMPT)


ENTER_CONFIG_MODE_PROMPT_COMMAND = 'configure'
EXIT_CONFIG_MODE_PROMPT_COMMAND = 'exit'
DEFAULT_ACTIONS = send_default_actions
SUPPORTED_OS = ['VDX', 'NOS']


def enter_enable_mode(session):
    result = session.hardware_expect('', re_string=DEFAULT_PROMPT)
    if not re.search(ENABLE_PROMPT, result):
        session.hardware_expect('enable', re_string=DEFAULT_PROMPT,
                                expect_map={'[Pp]assword': lambda session: session.send_line(
                                    get_decrypted_password_by_attribute_name_wrapper('Enable Password')())})
    result = session.hardware_expect('', re_string=DEFAULT_PROMPT)
    if not re.search(ENABLE_PROMPT, result):
        raise Exception('enter_enable_mode', 'Enable password is incorrect')


CONNECTIVITY_OPERATIONS_CLASS = BrocadeConnectivityOperations
CONFIGURATION_OPERATIONS_CLASS = BrocadeNOSConfigurationOperations
FIRMWARE_OPERATIONS_CLASS = BrocadeNOSConfigurationOperations
AUTOLOAD_OPERATIONS_CLASS = BrocadeGenericSNMPAutoload
SEND_COMMAND_OPERATIONS_CLASS = BrocadeSendCommandOperations
