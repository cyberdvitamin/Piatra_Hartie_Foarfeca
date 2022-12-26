import socket

# Creaza "socket"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host primeste localhost
host = socket.gethostname()

# Port primeste numarul port
port = 9999

# Conectare la server cu host si port
client_socket.connect((host, port))

# Optiunile pentru alegeri. P pentru Piatra, H pentru Hartie, F pentru Foarfeca
options = ['P', 'H', 'F']

# Functia alegere testeaza daca "choice" este una dintre optiuni sau nu
def alegere(choice):
    while True:
        if choice not in options:
            print("Input gresit, incearca inca o data!")
            choice = input("Scrie alegerea ta P/H/F: ").upper()
        else:
            break

# Functia start_game testeaza daca ai introdus corect "START"
def start_game(start):
    while True:
        if start != "START":
            # Daca nu ai introdus corect "START", intreaba din nou de input
            print("Nu ai scris START, incearca sa scrii din nou! ")
            start = input("Scrie START daca vrei sa incepi jocul: ").upper()
        else:
            # Daca ai introdus corect "START", jocul va incepe
            main()
            break

# Functia rematch intreaba jucatorul daca vrea sa inceapa un alt joc
def rematch(match):
    while True:
        if match == "START":
            # Daca jucatorul a scris "START" jocul va incepe din nou
            client_socket.send("START".encode())
            main()
            break
        elif match == "STOP":
            # Daca jucatorul a scris "STOP" jocul se va oprii
            break
        else:
            # Daca jucatorul a scris orice altceva, va primi un mesaj de eroare si va fi intrebat din nou de input
            print("Nu ai scris corect comanda, incearca START pentru rematch sau STOP pentru a inchide jocul! ")
            match = input("Scrie START daca vrei sa incepi un joc nou sau scrie STOP pentru a inchide jocul: ").upper()

# Functia main contine jocul
def main():
    score = {'player': 0, 'server': 0}
    for i in range(3):
        # Intreaba jucatorul pentru a face o alegere
        choice = input("Scrie alegerea ta P/H/F: ").upper()
        alegere(choice)

        # Trimite alegerea catre server
        client_socket.send(choice.encode())

        # Primeste rezultatul din acea runda
        result = client_socket.recv(1024).decode()

        # Tine minte scorul
        if result == 'player':
            score['player'] += 1
        elif result == 'server':
            score['server'] += 1

    # Primeste castigatorul final
    winner = client_socket.recv(1024).decode()

    # Afiseaza scorul final si castigatorul final
    print(f'Scor final: Jucator {score["player"]}, Server {score["server"]}')
    if winner == 'Egal':
        print("Meciul s-a terminat in egal!\n")
    else:
        print(f'Castigator final: {winner}\n')

    match = input("Scrie START daca vrei sa incepi un joc nou sau scrie STOP pentru a inchide jocul: ").upper()
    rematch(match)


start = input("Scrie START daca vrei sa incepi jocul: ").upper()
start_game(start)
# Inchide conexiunea "socket"
client_socket.close()
