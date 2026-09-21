# Déploiement machine

## Configuration réseau

### Dédié

```plain
# /etc/network/interfaces

auto lo
iface lo inet loopback

auto enp5s0
iface enp5s0 inet static
    address 195.154.254.166/32
    gateway 195.154.254.1

    post-up echo 1 > /proc/sys/net/ipv4/ip_forward
    post-up iptables -A INPUT -i enp5s0 -p tcp -m tcp -m multiport --dports 80,443,22 -j ACCEPT
    post-up iptables -A INPUT -i enp5s0 -m conntrack -j ACCEPT  --ctstate RELATED,ESTABLISHED
    post-up iptables -A INPUT -i enp5s0 -j DROP

iface enp5s0 inet static
    address 212.83.186.68/32

auto vmbr0
iface vmbr0 inet static
    address 10.10.10.1/24
    bridge-ports none
    bridge-stp off
    bridge-fd 0

    post-up sysctl -w net.bridge.bridge-nf-call-iptables=1
    post-up iptables -t nat -A PREROUTING -d 212.83.186.68 -p tcp --dport 80 -j DNAT --to 10.10.10.2:80
    post-up iptables -t nat -A PREROUTING -d 212.83.186.68 -p tcp --dport 443 -j DNAT --to 10.10.10.2:443
    post-up iptables -t nat -A PREROUTING -d 212.83.186.68 -p tcp --dport 22 -j DNAT --to 10.10.10.3:2222
    post-up iptables -t nat -A POSTROUTING -s '10.10.10.0/24' -o enp5s0 -j MASQUERADE
```

### VM

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
          - 86.54.11.100
          - 86.54.11.200
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
