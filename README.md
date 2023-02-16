# Connecter une machine utilisateur au VPN

## Client graphique (ZeroTier one)

Commencez par faut [installer le client ZeroTier One](https://www.zerotier.com/download/). Il suffit ensuite de suivre les instructions indiquées sur cette page pour vous connecter.

Ensuite, il faut faut également activer l'option `Allow DNS configuration` (non active par défaut) dans l'interface graphique.

![Allow DNS in GUI client](https://www.zerotier.com/wp-content/uploads/2022/04/dns-1-1024x648.jpg)

Une fois cela fait, l'administrateur du réseau ZeroTier doit autoriser la machine dans son interface d'administration.

## ZeroTier en console

Une fois ZeroTier installé (https://www.zerotier.com/download/), 2 commandes suffisent :

```sh
sudo zerotier-cli join <network ID>
sudo zerotier-cli set <network ID> allowDNS=1
```

Une fois cela fait, l'administrateur du réseau ZeroTier doit autoriser la machine dans son interface d'administration.

# Architecture globale

L'environnement de production et celui de préproduction utilisent tous deux deux réseaux VPN basés sur ZeroTier :

- Les machines vulnérables (accès publique) sont sur le réseau `mla/unsafe`. L'accès SSH à ces machines nécessite de passer par ce réseau.
- Les machines sécurisées (accès privé) sont sur le réseau `mla/safe`. L'accès SSH à ces machines nécessite de passer par ce réseau. Ces machines n'ont pas d'IP publique et sont donc totalement inaccessibles en dehors de ce réseau.

La machine utilisée pour le déploiement Ansible doit être connectée aux deux réseaux privés au moment du déploiement !

# Déploiement Ansible

## Environnement de préproduction (PreMLA)

La machine utilisée pour le déploiement doit être connectée aux deux réseaux VPN décrits ci-dessous. Idéalement, l'accès de cette machine aux deux réseaux n'est activé que temporairement lors des déploiements, en passant par l'interface d'administration ZeroTier.

Par ailleurs, l'utilisation de ce playbook nécessite la possession de la clé Ansible Vault privée, qui ne doit **en aucun cas être enregistrée dans le dépôt** ! A cette fin, le fichier `.gitignore` est paramétré pour ignorer les fichiers ayant l'extension `.vault`.

Une fois les deux réseaux ZeroTier connectés et la clé en votre posession, vous pouvez lancer le déploiement complet avec la commande suivante :

```sh
ansible-playbook mla.yml -i inventories/preprod --vault-password-file ansible-mla.vault
```

## Environnement Vagrant

### Installation de Vagrant

```sh
sudo apt install vagrant vagrant-hostmanager
```

### Mise en route et déploiement

```sh
cd vagrant
vagrant up --no-provision # Démarrage des machines
vagrant provision # Exécution d'Ansible
```
