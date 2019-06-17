
import bluetooth
import os
from time import sleep
import Class_Rpi_trial_3 as crt3


def connection():
    print("It Starts")
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    print("Socket Is Cool")
     
    port = 1
    print(server_socket)
    try:
        server_socket.bind(("", port))
        server_socket.listen(1)
        print("server is cool")         
        (client_socket,address) = server_socket.accept()
        print("Accepted connection from ",address)
        while 1:
            encoded_data = client_socket.recv(1024)
            decoded_data = encoded_data.decode("utf-8")
            print(decoded_data)
            if decoded_data == "s":
                string = ""
                string = crt3.start()
                print(string)
                client_socket.send(string)
        # test #
                break
            elif eData == "p":
                pass
            elif eData == "q":
                print("Quit")
                break
            else:
                break

        client_socket.close()
        server_socket.close()
        connection()
    except Exception as e:
            print(e)
            client_socket.close()
            server_socket.close()
            connection()


connection()
