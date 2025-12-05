# Contractions

Ceci est un projet pour le suivi des contractions avant un enfantement.

Serveur local permettant de cliquer sur un bouton à chaque contraction.
L'intervalle entre chaque contraction est affiché.

## Installation

```shell
python3.13 -m venv venv
. venv/bin/activate
```

```shell
python -m pip install -U pip
python -m pip install -r requirements.txt
```

## Démarrer le serveur

Pour lancer un serveur web accessible à [`http://localhost:2025`](http://localhost:2025) (le `port` est l'année en cours) :

```shell
python server.py
```
