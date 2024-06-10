#### Server Code
#python
import socket
import threading

# Predefined bank accounts
accounts = {
    '12345': {'password': 'pass1', 'balance': 1000},
    '67890': {'password': 'pass2', 'balance': 1500},
    '11223': {'password': 'pass3', 'balance': 1200},
}

# Function to handle client connection
def handle_client(client_socket):
    try:
        # Authenticate client
        account_number = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        
        if account_number in accounts and accounts[account_number]['password'] == password:
            client_socket.send("Authenticated".encode())
        else:
            client_socket.send("Authentication Failed".encode())
            client_socket.close()
            return
        
        # Handle client requests
        while True:
            request = client_socket.recv(1024).decode()
            
            if request == 'BALANCE':
                balance = accounts[account_number]['balance']
                client_socket.send(f"Balance: {balance}".encode())
                
            elif request.startswith('DEPOSIT'):
                amount = int(request.split()[1])
                accounts[account_number]['balance'] += amount
                client_socket.send(f"Deposited: {amount}".encode())
                
            elif request.startswith('WITHDRAW'):
                amount = int(request.split()[1])
                if accounts[account_number]['balance'] >= amount:
                    accounts[account_number]['balance'] -= amount
                    client_socket.send(f"Withdrawn: {amount}".encode())
                else:
                    client_socket.send("Insufficient funds".encode())
                    
            elif request == 'EXIT':
                balance = accounts[account_number]['balance']
                client_socket.send(f"Final Balance: {balance}".encode())
                client_socket.close()
                break
    except Exception as e:
        print(f"Exception: {e}")
        client_socket.close()

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


#### Client Code
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    # Authenticate
    account_number = input("Enter account number: ")
    password = input("Enter password: ")
    
    client.send(account_number.encode())
    client.send(password.encode())
    
    response = client.recv(1024).decode()
    print(response)
    
    if response == "Authenticated":
        while True:
            operation = input("Enter operation (BALANCE, DEPOSIT <amount>, WITHDRAW <amount>, EXIT): ")
            client.send(operation.encode())
            response = client.recv(1024).decode()
            print(response)
            if operation == "EXIT":
                break
    
    client.close()

main()
### Design Choices and Challenges