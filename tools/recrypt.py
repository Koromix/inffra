#!/bin/env -S uv run

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

# /// script
# dependencies = [
#   "pyyaml",
#   "ansible"
# ]
# ///

import argparse
import sys
import yaml
from dataclasses import dataclass
from ansible.parsing import vault

@dataclass
class VaultTag:
    encrypted: str

def vault_constructor(loader, node):
    value = loader.construct_scalar(node)
    return VaultTag(encrypted = value)

def vault_representer(dumper, obj):
    return dumper.represent_scalar('!vault', obj.encrypted, style = '|')

def make_secrets(secret):
    from ansible.constants import DEFAULT_VAULT_ID_MATCH
    return [(DEFAULT_VAULT_ID_MATCH, vault.VaultSecret(secret))]

def recrypt(obj, vault1, vault2):
    if isinstance(obj, dict):
        return { k: recrypt(v, vault1, vault2) for k, v in obj.items() }
    elif isinstance(obj, list):
        return [ recrypt(v, vault1, vault2) for v in obj ]
    elif isinstance(obj, VaultTag) and obj.encrypted:
        value = vault2.encrypt(vault1.decrypt(obj.encrypted)).decode('utf-8')
        return VaultTag(encrypted = value)
    else:
        return obj

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Update mimetypes include file')
    parser.add_argument('-S', '--source_key', dest = 'source_key', action = 'store', required = True, help = 'Source secret file')
    parser.add_argument('-D', '--dest_key', dest = 'dest_key', action = 'store', required = True, help = 'New secret file')
    parser.add_argument('yaml', help = 'YAML file with secrets')
    args = parser.parse_args()

    yaml.add_constructor('!vault', vault_constructor)
    yaml.add_representer(VaultTag, vault_representer)

    with open(args.source_key, 'rb') as f:
        secret1 = f.read()
    with open(args.dest_key, 'rb') as f:
        secret2 = f.read()
    with open(args.yaml, 'r') as f:
        src = yaml.full_load(f.read())

    vault1, vault2 = vault.VaultLib(make_secrets(secret1)), vault.VaultLib(make_secrets(secret2))
    dest = recrypt(src, vault1, vault2)

    with open(args.yaml, 'w') as f:
        yaml.dump(dest, f, sort_keys = False)
