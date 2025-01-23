# IP-Rotation-Bruteforce
Script to bruteforce an HTTP POST form using hydra and rotating the IP using TOR and Proxychains.

## TOR Installation and Configuration
Install TOR in a Kali machine.
```bash
sudo apt install tor
```
Add in the configuration file **/etc/tor/torrc** the following lines.
```text
ControlPort 9051
CookieAuthentication 0
```

## Usage
```bash
usage: bruteforce_rotation.py [-h] -u USERS -w WORDLIST [-c COUNT] target uri

Programa que realitza força bruta i cada cert intents canvia de IP per evitar filtres de WAF

positional arguments:
  target                Domini on es vol atacar. Ex: example.com
  uri                   Camí del login on es vol realitzar el bruteforce.

options:
  -h, --help            show this help message and exit
  -u USERS, --users USERS
                        Ubicació del llistat d'usuaris a comprometre.
  -w WORDLIST, --wordlist WORDLIST
                        Ubicació del diccionari de contrasenyes a utilitzar.
  -c COUNT, --count COUNT
                        Nombre d'intents abans de fer el canvi d'IP. Per defecte 25
```
