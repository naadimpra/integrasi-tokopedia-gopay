#Library yang digunakan untuk melakukan komunikasi antar program python dengan menggunakan socket

import socket

#Library yang digunakan agar program python dapat menggunakan database mysql

import mysql.connector

#Melakukan koneksi ke database tokopedia
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="tokopedia"
)

#mysql cursor untuk melakukan eksekusi statement yang berkomunikasi dengan mysql database
mycursor = mydb.cursor()

#Inisialisasi socket untuk client Tokopedia
client_socket = socket.socket()

#Konfigurasi host dan port yang akan digunakan
host = socket.gethostname()
port = 5000

#Deklarasi variabel global
user_id = None
user_name = None
user_status = 2

#Fungsi untuk mendaftarkan akun baru pada Tokopedia
def daftar_tokopedia(nohp, nama):
    try:
        sql = "INSERT INTO user (telepon, nama) VALUES (%s, %s)"
        val = (nohp, nama)
        mycursor.execute(sql, val)

        mydb.commit()
        print("[PENDAFTARAN BERHASIL]\nBerhasil mendaftarkan user", nama, "\n")
    except:
        print("Gagal mendaftarkan user baru\n")

#Fungsi untuk login ke akun Tokopedia
def tokopedia_login():
    try:
        global user_id, user_name, user_status
        print("[LOGIN USER TOKOPEDIA]")
        log_id = input("No HP -> ")
        
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (log_id, )
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        user_id = result[0]
        user_name = result[1]
        user_status = result[2]
        print("\n[LOGIN BERHASIL]\n")
    except:
        print("\n[LOGIN GAGAL]\n")

#Fungsi untuk mengaktifkan akun Gopay pada akun Tokopedia
def activate_gopay():
    try:
        message = f"check_user;{user_id};;"
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()

        if response == "empty":
            print("Gagal aktivasi gopay\nTidak ada akun dengan nomor tersebut!")
        elif response == "exist":
            sql = "UPDATE user SET gopay_status = 1 WHERE telepon = %s"
            val = (user_id, )
            mycursor.execute(sql, val)

            mydb.commit()
            global user_status
            user_status = 1
            print("Berhasil mengaktifkan gopay pada akun\n", user_name)
        else:
            print("Gagal mengaktifkan gopay pada akun\n", user_name)
    except:
        print("Gagal mengaktifkan gopay pada akun\n", user_name)

#Fungsi untuk menampilkan list item Tokopedia
def list_item():
    try:
        print("[LIST ITEM TOKOPEDIA]")
        
        sql = "SELECT * FROM item"
        mycursor.execute(sql)

        result = mycursor.fetchone()
        print(result)
    except:
        print("\n[LIST ITEM GAGAL]\n")

#Fungsi logout akun Tokopedia
def logout():
    global user_id, user_name, user_status

    user_id = None
    user_name = None
    user_status = 2

    client_socket.close()

#Menu program Tokopedia
def tokopedia_program():

    while True:
        command = input("[PILIH MENU]\n1. Cek Saldo\n2. Pesan Item\n3. Top Up\n4. Cashback\n5. History\n\nMenu -> ")
        
        if command == "1":
            message = f"check_balance;{user_id}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("gopay sedang error!")
            else:
                print("\n[CEK SALDO]\nBerhasil cek saldo")
                print("Saldo", user_name, "saat ini adalah", response, "\n")
        elif command == "2":
            sql = "SELECT item.nama_item, item.rating_item, penjual.nama_penjual, item.harga_item FROM item LEFT JOIN penjual ON item.id_item=penjual.id_penjual"
            mycursor.execute(sql)
            print("Data Item: \nNo.\tHarga\tRating\tPenjual\tNama Item")
            result = mycursor.fetchall()

            for num, i in enumerate(result):
                print(f"{num+1}. {i[3]}\t{i[1]}\t{i[2]}\t{i[0]}")

            pilihItem = int(input("Pilih Item dengan memasukkan Nomor Item -> "))
            nominal = int(input("Jumlah Barang -> "))
            bayar = result[pilihItem-1][3]*nominal
            message = f"transaction;{user_id};{bayar}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("gopay sedang error!")
            elif response == "minus":
                print("Saldo gopay tidak cukup!\n")
            else:
                print("\n[TRANSAKSI SUKSES]\nBerhasil Berhasil memproses transaksi")
                print("Saldo", user_name, "saat ini adalah Rp. ", response, "\n")
        elif command == "3":
            nominal = input("Nominal Top-Up -> ")

            message = f"topup;{user_id};{nominal}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("gopay sedang error!")
            else:
                print("\n[TOP UP SUKSES]\nBerhasil Top-Up!")
                print("Saldo", user_name, "saat ini adalah Rp. ", response, "\n")
        elif command == "4":
            nominal = input("Nominal cashback -> ")

            message = f"cashback;{user_id};;{nominal}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("gopay sedang error!")
            else:
                print("\n[CASHBACK]\nBerhasil memproses cashback")
                print("Saldo", user_name, "saat ini adalah Rp. ", response, "\n")
        elif command == "5":
            tanggal = input("Masukkan tanggal (sampai)-> ")

            message = f"history;{user_id};{tanggal}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            print(type(response))
            response = eval(response)
            
            if response == "failed":
                print("gopay sedang error!")
            else:
                print("\n[HISTORY TRANSAKSI]\nBerhasil mereturn history transaksi")
                print(response)
        elif command == "6":
            logout()
            break
        else:
            print("Maaf, perintah tidak dikenali\n")

#Fungsi main yang dieksekusi pertama kali saat program Tokopedia berjalan
if __name__ == '__main__':
    while True:
        reg_status = input("Apakah Anda ingin menambahkan user baru? [y/n] ")
        if reg_status == "n":
            break
        else:
            try:
                print("[DAFTAR USER BARU]\n")
                nama_daftar = input("Nama -> ")
                hp_daftar = input("No HP -> ")

                daftar_tokopedia(hp_daftar, nama_daftar)
            except:
                print("Format Salah!\n")

    client_socket.connect((host, port))
    tokopedia_login()

    if user_status == 1:
        tokopedia_program()
    elif user_status == 0:
        try:
            activate_gopay()
            if user_status == 1:
                tokopedia_program()
            else:
                logout()
        except:
            logout()
    else:
        logout()