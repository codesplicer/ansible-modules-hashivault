#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_delete
version_added: "3.4.0"
short_description: Hashicorp Vault delete module
description:
    - Module to delete from Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    verify:
        description:
            - verify TLS certificate
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
    password:
        description:
            - password to login to vault.
    secret:
        description:
            - secret to delete.
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_delete:
        secret: giant
'''


def main():
    argspec = hashivault_argspec()
    argspec['secret'] = dict(required=True, type='str')
    module = hashivault_init(argspec)
    result = hashivault_delete(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_delete(params):
    result = { "changed": False, "rc" : 0}
    client = hashivault_auth_client(params)
    secret = params.get('secret')
    if secret.startswith('/'):
        secret = secret.lstrip('/')
    else:
        secret = ('secret/%s' % secret)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        returned_data = client.delete(secret)
        if returned_data:
            result['data'] = returned_data
        result['msg'] = "Secret %s deleted" % secret
    result['changed'] = True
    return result


if __name__ == '__main__':
    main()
