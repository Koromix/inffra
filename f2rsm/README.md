# Déploiement machine

## Configuration réseau

### Dédié

```plain
# /etc/network/interfaces

auto lo
iface lo inet loopback

auto eno1
iface eno1 inet static
    address 149.202.71.92/32
    gateway 149.202.71.254

    post-up echo 1 > /proc/sys/net/ipv4/ip_forward
    post-up iptables -A INPUT -i eno1 -p tcp -m tcp -m multiport --dports 80,443,22 -j ACCEPT
    post-up iptables -A INPUT -i eno1 -m conntrack -j ACCEPT  --ctstate RELATED,ESTABLISHED
    post-up iptables -A INPUT -i eno1 -j DROP

    post-up

auto vmbr0
iface vmbr0 inet static
    address 10.10.11.1/24
    bridge-ports none
    bridge-stp off
    bridge-fd 0

    post-up sysctl -w net.bridge.bridge-nf-call-iptables=1
    post-up iptables -t nat -A PREROUTING -d 149.202.71.92 -p tcp --dport 80 -j DNAT --to 10.10.11.2:80
    post-up iptables -t nat -A PREROUTING -d 149.202.71.92 -p tcp --dport 443 -j DNAT --to 10.10.11.2:443
    post-up iptables -t nat -A PREROUTING -d 149.202.71.92 -p tcp --dport 22 -j DNAT --to 10.10.11.4:2222
    post-up iptables -t nat -A POSTROUTING -s '10.10.11.0/24' -o eno1 -j MASQUERADE
```

### VM

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
nameserver 86.54.11.100
nameserver 86.54.11.200
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
