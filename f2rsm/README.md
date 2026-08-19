# Déploiement machine

## Configuration réseau

```plain
# /etc/network/interfaces.d/ens18
# sudo systemctl restart networking

auto ens18
iface ens18 inet static
    address 10.10.11.X/24
    gateway 10.10.11.1
```

```plain
# /etc/resolv.conf
#
nameserver 8.8.8.8
nameserver 8.8.4.4
```

## Configuration Netbird

```sh
curl -fsSL https://pkgs.netbird.io/install.sh | sh
netbird up --setup-key <SETUP KEY>
```

# Déploiement Ansible

```sh
ansible-playbook play.yml -i inventory --vault-password-file ../keys/f2rsmpsy.vault
```
