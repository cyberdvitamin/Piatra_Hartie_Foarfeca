import random
import socket

# Creaza "socket"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host primeste localhost
host = socket.gethostname()

# Port primeste numarul port
port = 9999

# Creaza un server cu ajutorul lui host si port
server_socket.bind((host, port))

# Asteapta pentru o conexiune
server_socket.listen(1)

# Asteapta pentru client sa se conecteze
client_socket, client_address = server_socket.accept()

# Functia rematch intreaba jucatorul daca vrea sa inceapa un alt joc
def rematch():
    rematch_comanda = client_socket.recv(1024).decode()
    while True:
        if rematch_comanda == "START":
            # Daca serverul primeste comanda "START" jocul va reincepe
            main()
            rematch()
        else:
            # Daca nu primeste comanda "START" jocul se va oprii cu tot cu server
            client_socket.close()
            server_socket.close()
            break

# Functia main contine jocul
def main():
    score = {'player': 0, 'server': 0}
    for i in range(3):
        # Primeste alegerea clientului
        client_choice = client_socket.recv(1024).decode()

        # Serverul face o alegere random
        options = ['P', 'H', 'F']
        server_choice = random.choice(options)
        print(f"Serverul a ales: {server_choice}")

        # Determina castigatorul rundei
        if client_choice == server_choice:
            result = 'draw'
        elif (client_choice == 'P' and server_choice == 'F') or (
                client_choice == 'H' and server_choice == 'P') or (
                client_choice == 'F' and server_choice == 'H'):
            result = 'player'
            score['player'] += 1
        else:
            result = 'server'
            score['server'] += 1

        # Trimite rezultatul inapoi catre client
        client_socket.send(result.encode())

    # Determina castigatorul final
    if score['player'] > score['server']:
        winner = 'Jucator'
    elif score['player'] < score['server']:
        winner = 'Server'
    else:
        winner = 'Egal'

    # Trimite castigatorul final catre client
    client_socket.send(winner.encode())

main()
rematch()