#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_aam_authentication_server_ldap_instance
description:
    - None
short_description: Configures A10 aam.authentication.server.ldap.instance
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
    health_check_disable:
        description:
        - "None"
        required: False
    protocol:
        description:
        - "None"
        required: False
    encrypted:
        description:
        - "None"
        required: False
    port:
        description:
        - "None"
        required: False
    ldaps_conn_reuse_idle_timeout:
        description:
        - "None"
        required: False
    port_hm:
        description:
        - "None"
        required: False
    uuid:
        description:
        - "None"
        required: False
    admin_dn:
        description:
        - "None"
        required: False
    default_domain:
        description:
        - "None"
        required: False
    auth_type:
        description:
        - "None"
        required: False
    admin_secret:
        description:
        - "None"
        required: False
    pwdmaxage:
        description:
        - "None"
        required: False
    health_check_string:
        description:
        - "None"
        required: False
    derive_bind_dn:
        description:
        - "Field derive_bind_dn"
        required: False
        suboptions:
            username_attr:
                description:
                - "None"
    prompt_pw_change_before_exp:
        description:
        - "None"
        required: False
    base:
        description:
        - "None"
        required: False
    secret_string:
        description:
        - "None"
        required: False
    name:
        description:
        - "None"
        required: True
    port_hm_disable:
        description:
        - "None"
        required: False
    host:
        description:
        - "Field host"
        required: False
        suboptions:
            hostipv6:
                description:
                - "None"
            hostip:
                description:
                - "None"
    ca_cert:
        description:
        - "None"
        required: False
    bind_with_dn:
        description:
        - "None"
        required: False
    sampling_enable:
        description:
        - "Field sampling_enable"
        required: False
        suboptions:
            counters1:
                description:
                - "None"
    dn_attribute:
        description:
        - "None"
        required: False
    timeout:
        description:
        - "None"
        required: False
    health_check:
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
AVAILABLE_PROPERTIES = ["admin_dn","admin_secret","auth_type","base","bind_with_dn","ca_cert","default_domain","derive_bind_dn","dn_attribute","encrypted","health_check","health_check_disable","health_check_string","host","ldaps_conn_reuse_idle_timeout","name","port","port_hm","port_hm_disable","prompt_pw_change_before_exp","protocol","pwdmaxage","sampling_enable","secret_string","timeout","uuid",]

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
        health_check_disable=dict(type='bool',),
        protocol=dict(type='str',choices=['ldap','ldaps','starttls']),
        encrypted=dict(type='str',),
        port=dict(type='int',),
        ldaps_conn_reuse_idle_timeout=dict(type='int',),
        port_hm=dict(type='str',),
        uuid=dict(type='str',),
        admin_dn=dict(type='str',),
        default_domain=dict(type='str',),
        auth_type=dict(type='str',choices=['ad','open-ldap']),
        admin_secret=dict(type='bool',),
        pwdmaxage=dict(type='int',),
        health_check_string=dict(type='str',),
        derive_bind_dn=dict(type='dict',username_attr=dict(type='str',)),
        prompt_pw_change_before_exp=dict(type='int',),
        base=dict(type='str',),
        secret_string=dict(type='str',),
        name=dict(type='str',required=True,),
        port_hm_disable=dict(type='bool',),
        host=dict(type='dict',hostipv6=dict(type='str',),hostip=dict(type='str',)),
        ca_cert=dict(type='str',),
        bind_with_dn=dict(type='bool',),
        sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','admin-bind-success','admin-bind-failure','bind-success','bind-failure','search-success','search-failure','authorize-success','authorize-failure','timeout-error','other-error','request','ssl-session-created','ssl-session-failure','pw_expiry','pw_change_success','pw_change_failure'])),
        dn_attribute=dict(type='str',),
        timeout=dict(type='int',),
        health_check=dict(type='bool',)
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/aam/authentication/server/ldap/instance/{name}"
    f_dict = {}
    f_dict["name"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/aam/authentication/server/ldap/instance/{name}"
    f_dict = {}
    f_dict["name"] = module.params["name"]

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
    payload = build_json("instance", module)
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
    payload = build_json("instance", module)
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