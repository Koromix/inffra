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

## Configuration ZeroTier

```sh
sudo apt update
sudo apt install gpg

sudo curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
    if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi

sudo zerotier-cli join <safe ID> # Replace <safe ID> values with info from private document
```

# Déploiement Ansible

```sh
ansible-playbook play.yml -i inventory --vault-password-file ../keys/interactions.vault
```
