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
port = 3306

status_user = 2
id_user = None
nama_user = None

#Fungsi untuk mendaftarkan akun baru pada Tokopedia
def register_tokopedia(nohp, nama):
    try:
        sql = "INSERT INTO user (telepon, nama) VALUES (%s, %s)"
        val = (nohp, nama)
        mycursor.execute(sql, val)

        mydb.commit()
        print("=== PENDAFTARAN BERHASIL ===\nBerhasil mendaftarkan user", nama, "\n")
    except:
        print("Gagal mendaftarkan user baru\n")

#Fungsi untuk login ke akun Tokopedia
def login_tokopedia():
    try:
        global id_user, nama_user, status_user
        print("=== LOGIN PENGGUNA TOKOPEDIA ===")
        log_id = input("No HP => ")
        
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (log_id, )
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        id_user = result[0]
        nama_user = result[1]
        status_user = result[2]
        print("\nBerhasil Login\n")
    except:
        print("\nGagal untuk login, Nomor anda belum terdaftar dan/atau belum teraktivasi.\n")

#Fungsi untuk mengaktifkan akun Gopay pada akun Tokopedia
def aktivasi_gopay():
    try:
        message = f"cek_user;{id_user};;"
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()

        if response == "empty":
            print("Gagal untuk mengaktivasi Gopay\nTidak ada akun dengan nomor tersebut!")
        elif response == "exist":
            sql = "UPDATE user SET gopay_status = 1 WHERE telepon = %s"
            val = (id_user, )
            mycursor.execute(sql, val)

            mydb.commit()
            global status_user
            status_user = 1
            print("Berhasil mengaktivasi Gopay pada akun", nama_user)
        else:
            print("Gagal mengaktivasi Gopay pada akun", nama_user)
    except:
        print("Gagal mengaktivasi Gopay pada akun", nama_user)

#Menu program Tokopedia
def program_tokopedia():

    while True:
        command = input("=== HALAMAN UTAMA TOKOPEDIA ===\n1. Cek Saldo\n2. Membeli Barang\n3. Top Up\n4. Cashback\n5. Log out\n\nMenu => ")
        
        if command == "1":
            message = f"cek_saldo_gopay;{id_user}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("Gopay sedang mengalami gangguan!")
            else:
                print("\n=== CEK SALDO ===")
                print("Saldo", nama_user, "saat ini adalah Rp. ", response, "\n")
                print("\nBerhasil melakukan cek saldo.")
        elif command == "2":
            sql = "SELECT item.nama_item, item.harga_item, penjual.nama_penjual, item.rating_item FROM item LEFT JOIN penjual ON item.id_item=penjual.id_penjual"
            mycursor.execute(sql)
            print("=== DATA BARANG === \nNo.\tNama Barang\tHarga Barang\tPenjual\tRating")
            result = mycursor.fetchall()

            for num, i in enumerate(result):
                print(f"{num+1}. {i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")

            pilihItem = int(input("Pilih Item dengan memasukkan Nomor Item => "))
            nominal = int(input("Jumlah Barang => "))
            bayar = result[pilihItem-1][3]*nominal
            message = f"transaction;{id_user};{bayar}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("Gopay sedang mengalami gangguan!")
            elif response == "minus":
                print("Saldo Gopay anda tidak cukup!\n")
            else:
                print("\nPembayaran Sukses!")
                print("Saldo", nama_user, "saat ini adalah Rp. ", response, "\n")
        elif command == "3":
            nominal = input("Nominal Top-Up => ")

            message = f"topup;{id_user};{nominal}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("Gopay sedang mengalami gangguan!")
            else:
                print("\n=== TOP UP SUKSES ===\nBerhasil Top-Up!")
                print("Saldo", nama_user, "saat ini adalah Rp. ", response, "\n")
        elif command == "4":
            nominal = input("Nominal cashback => ")

            message = f"cashback;{id_user};;{nominal}"
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()

            if response == "failed":
                print("Gopay sedang mengalami gangguan!")
            else:
                print("\n=== CASHBACK ===\nBerhasil memproses cashback")
                print("Saldo", nama_user, "saat ini adalah Rp. ", response, "\n")
                
        elif command == "5":
            logout()
            break
            
#Fungsi logout akun Tokopedia
def logout():
    global id_user, nama_user, status_user

    id_user = None
    nama_user = None
    status_user = 2

    client_socket.close()

#Fungsi main yang dieksekusi pertama kali saat program Tokopedia berjalan
if __name__ == '__main__':
    while True:
        reg_status = input("Apakah Anda ingin menambahkan user baru? y/n => ")
        if reg_status == "n":
            break
        else:
            if reg_status == "y":
                print("=== DAFTAR USER TOKOPEDIA BARU ===\n")
                nama_daftar = input("Nama => ")
                hp_daftar = input("No HP => ")

                register_tokopedia(hp_daftar, nama_daftar)
            else:
                print("Format Salah!\n")

    client_socket.connect((host, port))
    login_tokopedia()

    if status_user == 0:
        try:
            aktivasi_gopay()
            if status_user == 1:
                program_tokopedia()
            else:
                logout()
        except:
            logout()
    elif status_user == 1:
        program_tokopedia()
    else:
        logout()