#Library python-socket

import socket

#Import program Gopay.py

import gopay as gopay_app

#Fungsi utama untuk server
def server_program():
    print("Server Starting")
    host = socket.gethostname()
    port = 3306 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    print("Menunggu Koneksi")
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Koneksi dari: " + str(address))

    while True:
        data_receive = conn.recv(1024).decode()

        data = data_receive.split(";")
        print(data)

        if not data_receive:
            print("Client Tokopedia", str(address), "telah keluar.")
            break
        else:
            if data[0] == "cek_saldo_gopay":
                try:
                    response = str(gopay_app.cek_saldo_gopay(data[1]))
                    conn.send(response.encode())
                except:
                    response = "failed"
                    conn.send(response.encode())
            elif data[0] == "cek_user":
                try:
                    result = gopay_app.cek_user(data[1])
                    if result == 1:
                        response = "exist"
                    else:
                        response = "empty"
                    
                    conn.send(response.encode())
                except:
                    response = "failed"
                    conn.send(response.encode())
            elif (data[0] == "cashback") or (data[0] == "return"):
                try:
                    gopay_app.tambah_saldo_gopay(data[1], int(data[3]))
                    gopay_app.kurangi_saldo_gopay(data[2], int(data[3]))
                    response = str(gopay_app.cek_saldo_gopay(data[1]))
                    conn.send(response.encode())
                except:
                    response = "failed"
                    conn.send(response.encode())
            elif data[0] == "transaction":
                try:
                    saldo = gopay_app.cek_saldo_gopay(data[1])

                    if saldo >= int(data[2]):
                        gopay_app.kurangi_saldo_gopay(data[1], int(data[2]))
                        response = str(gopay_app.cek_saldo_gopay(data[1]))
                    else:
                        response = "minus"
                    conn.send(response.encode())
                except:
                    print("TRANSACTION FAILED\n")
                    response = "failed"
                    conn.send(response.encode())
            elif data[0] == "topup":
                try:
                    nominal = int(data[2])

                    if nominal > 0:
                        gopay_app.tambah_saldo_gopay(data[1], int(data[2]))
                        response = str(gopay_app.cek_saldo_gopay(data[1]))
                    else:
                        response = "minus"
                    conn.send(response.encode())
                except:
                    print("TOP UP FAILED\n")
                    response = "failed"
                    conn.send(response.encode())
            else:
                print("Command tidak ditemukan")

    conn.close()

#Fungsi main yang digunakan untuk menampilkan menu yang digunakan untuk mengeksekusi program server
if __name__ == '__main__':
	while True:
		command = input("\n=== MENU SERVER ===\n1. Aktifkan Server\n2. Keluar\n\nMenu => ")
		if command == "1" :
			server_program()
		elif command == "2":
			break
		else:
			print("Command tidak ditemukan")