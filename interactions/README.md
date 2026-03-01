# Déploiement machine

## Configuration réseau

```yaml
# /etc/netplan/99-ens18.yaml
# sudo netplan apply

network:
  version: 2
  ethernets:
    ens18:
      dhcp4: false
      dhcp6: false
      accept-ra: false
      link-local: []
      addresses:
        - 10.10.10.X/24
      routes:
        - to: default
          via: 10.10.10.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

## Configuration Netbird

```sh
curl -fsSL https://pkgs.netbird.io/install.sh | sh
netbird up --setup-key <SETUP KEY>
```

# Déploiement Ansible

```sh
ansible-playbook play.yml -i inventory --vault-password-file ../keys/interactions.vault
```
