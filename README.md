# Connect machine to VPS

First, [install the ZeroTier client](https://www.zerotier.com/download/). Follow the instructions on the ZeroTier download page for your platform.

After that, use the graphical ZeroTier client or the console client to join the ZeroTier network. For example on Linux, do it like this:

```sh
sudo zerotier-cli join <network ID>
sudo zerotier-cli set <network ID> allowDNS=1
```

Once this is done, go to the ZeroTier dashboard and allow the machine (use the "Auth" checkbox) and give it a name. That's it!

# Add new VPS

## Join ZeroTier network

Once the machine exists, you must manually SSH to it and add it to the ZeroTier network:

```sh
sudo apt update
sudo apt install gpg

sudo curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
    if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi

sudo zerotier-cli join <network ID>
```

Once this is done, go to the ZeroTier dashboard and allow the machine (use the "Auth" checkbox) and give it a name. That's it!

## Integrate with Ansible

Not yet!

## First playbook launch

```sh
ansible-playbook -i inventories/preprod mla.yml --vault-password-file ansible-mla.vault --tags=base -e ansible_user=debian -e ansible_ssh_private_key_file=~/.ssh/id_rsa
```

# Deploying with ansible

## Production

Not yet!

## Vagrant

Install the following packagers first:

```sh
sudo apt install vagrant vagrant-hostmanager
```

### Initialize VMs

Execute from the vagrant directory:

```sh
cd vagrant
vagrant up --no-provision
```

### Deploy

```sh
vagrant provision
```
