#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_rekey_status
version_added: "3.3.0"
short_description: Hashicorp Vault rekey status module
description:
    - Module to get rekey status of Hashicorp Vault.
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
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_rekey_status:
      register: "vault_rekey_status"
'''

def main():
    argspec = hashivault_argspec()
    module = hashivault_init(argspec)
    result = hashivault_rekey_status(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *

@hashiwrapper
def hashivault_rekey_status(params):
    client = hashivault_client(params)
    return {'status': client.rekey_status}

if __name__ == '__main__':
    main()
