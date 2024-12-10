# Configuration ZeroTier

```sh
sudo apt update
sudo apt install gpg

sudo curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
    if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi

sudo zerotier-cli join <safe ID> # Replace <safe ID> values with info from private document
```

# Déploiement Ansible

```sh
ansible-playbook play.yml -i inventories/prod --vault-password-file ../keys/pknet.vault
```
