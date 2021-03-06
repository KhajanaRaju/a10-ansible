#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_slb_sip
description:
    - None
short_description: Configures A10 slb.sip
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    sampling_enable:
        description:
        - "Field sampling_enable"
        required: False
        suboptions:
            counters1:
                description:
                - "None"
    uuid:
        description:
        - "None"
        required: False


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["sampling_enable","uuid",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory, session_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','msg_proxy_current','msg_proxy_total','msg_proxy_mem_allocd','msg_proxy_mem_cached','msg_proxy_mem_freed','msg_proxy_client_recv','msg_proxy_client_send_success','msg_proxy_client_incomplete','msg_proxy_client_drop','msg_proxy_client_connection','msg_proxy_client_fail','msg_proxy_client_fail_parse','msg_proxy_client_fail_process','msg_proxy_client_fail_snat','msg_proxy_client_exceed_tmp_buff','msg_proxy_client_fail_send_pkt','msg_proxy_client_fail_start_server_Conn','msg_proxy_server_recv','msg_proxy_server_send_success','msg_proxy_server_incomplete','msg_proxy_server_drop','msg_proxy_server_fail','msg_proxy_server_fail_parse','msg_proxy_server_fail_process','msg_proxy_server_fail_selec_connt','msg_proxy_server_fail_snat','msg_proxy_server_exceed_tmp_buff','msg_proxy_server_fail_send_pkt','msg_proxy_create_server_conn','msg_proxy_start_server_conn','msg_proxy_fail_start_server_conn','msg_proxy_server_conn_fail_snat','msg_proxy_fail_construct_server_conn','msg_proxy_fail_reserve_pconn','msg_proxy_start_server_conn_failed','msg_proxy_server_conn_already_exists','msg_proxy_fail_insert_server_conn','msg_proxy_parse_msg_fail','msg_proxy_process_msg_fail','msg_proxy_no_vport','msg_proxy_fail_select_server','msg_proxy_fail_alloc_mem','msg_proxy_unexpected_err','msg_proxy_l7_cpu_failed','msg_proxy_l4_to_l7','msg_proxy_l4_from_l7','msg_proxy_to_l4_send_pkt','msg_proxy_l4_from_l4_send','msg_proxy_l7_to_L4','msg_proxy_mag_back','msg_proxy_fail_dcmsg','msg_proxy_deprecated_conn','msg_proxy_hold_msg','msg_proxy_split_pkt','msg_proxy_pipline_msg','msg_proxy_client_reset','msg_proxy_server_reset','session_created','session_freed','session_in_rml','session_invalid','conn_allocd','conn_freed','session_callid_allocd','session_callid_freed','line_mem_allocd','line_mem_freed','table_mem_allocd','table_mem_freed','cmsg_no_uri_header','cmsg_no_uri_session','sg_no_uri_header','smsg_no_uri_session','line_too_long','fail_read_start_line','fail_parse_start_line','invalid_start_line','request_unknown_version','response_unknown_version','request_unknown','fail_parse_headers','too_many_headers','invalid_header','header_name_too_long','body_too_big','fail_get_counter','msg_no_call_id','identify_dir_failed','no_sip_request','deprecated_msg','fail_insert_callid_session','fail_insert_uri_session','fail_insert_header','select_server_conn','select_server_conn_by_callid','select_server_conn_by_uri','select_server_conn_by_rev_tuple','select_server_conn_failed','select_client_conn','X_forward_for_select_client','call_id_select_client','uri_select_client','client_select_failed','acl_denied','assemble_frag_failed','wrong_ip_version','size_too_large','fail_split_fragment','client_keepalive_received','server_keepalive_received','client_keepalive_send','server_keepalive_send','ax_health_check_received','client_request','client_request_ok','concatenate_msg','save_uri','save_uri_ok','save_call_id','save_call_id_ok','msg_translation','msg_translation_fail','msg_trans_start_line','msg_trans_start_headers','msg_trans_body','request_register','request_invite','request_ack','request_cancel','request_bye','request_options','request_prack','request_subscribe','request_notify','request_publish','request_info','request_refer','request_message','request_update','response_unknown','response_1XX','response_2XX','response_3XX','response_4XX','response_5XX','response_6XX','ha_send_sip_session','ha_send_sip_session_ok','ha_fail_get_msg_header','ha_recv_sip_session','ha_insert_sip_session_ok','ha_update_sip_session_ok','ha_invalid_pkt','ha_fail_alloc_sip_session','ha_fail_alloc_call_id','ha_fail_clone_sip_session','save_smp_call_id_rtp','update_smp_call_id_rtp','smp_call_id_rtp_session_match','smp_call_id_rtp_session_not_match','process-error-when-message-switch'])),
        uuid=dict(type='str',)
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/slb/sip"
    f_dict = {}

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/slb/sip"
    f_dict = {}

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        if isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def get(module):
    return module.client.get(existing_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("sip", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result, existing_config):
    payload = build_json("sip", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result, existing_config):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result, existing_config)

def absent(module, result):
    return delete(module, result)

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()