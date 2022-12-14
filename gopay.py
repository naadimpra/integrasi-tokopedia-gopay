#Library python-mysql
import mysql.connector

#Melakukan koneksi ke database Gopay
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="gopay"
)

#Mysql Cursor untuk eksekusi statement yang berkomunikasi dengan mysql database
mycursor = mydb.cursor()

#Fungsi untuk mendaftarkan akun baru pada Gopay
def register_gopay(nohp, nama):
    try:
        sql = "INSERT INTO user (telepon, nama, saldo) VALUES (%s, %s, 0)"
        val = (nohp, nama)
        mycursor.execute(sql, val)

        mydb.commit()
        print("\n=== PENDAFTARAN BERHASIL ===\nBerhasil mendaftarkan user Gopay", nama)
    except:
        print("\nGagal mendaftarkan user Gopay baru\n")

#Fungsi untuk mengecek apakah user sudah terdaftar dalam database
def check_user(nohp):
    try:
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (nohp, )
        mycursor.execute(sql, val)

        result = mycursor.fetchall()

        if len(result) == 1:
            print("\n=== CEK AKUN ===\nAkun dengan No HP", nohp,"tersedia")
            return(1)
        else:
            print("\n=== CEK AKUN ===\nAkun dengan No HP", nohp,"tidak tersedia")
            return(0)
    except:
        print("Gagal mendapatkan informasi akun", nohp)

#Fungsi untuk menampilkan saldo Gopay
def cek_saldo_gopay(nohp):
    try:
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (nohp, )
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        print("\n=== CEK SALDO ===\nSaldo", result[1],"saat ini = Rp.", result[2])

        return(result[2])
    except:
        print("\nGagal mendapatkan informasi akun", nohp)

#Fungsi untuk melakukan topup saldo Gopay
def tambah_saldo_gopay(nohp, nominal):
    try:
        print("\n=== MENAMBAH SALDO ===")
        sql = "UPDATE user SET saldo = saldo + %s WHERE telepon = %s"
        val = (nominal, nohp)
        mycursor.execute(sql, val)

        sql = "INSERT INTO history (telepon, nominal, keterangan) VALUES (%s, %s,'Top Up Saldo')"
        val = (nohp, nominal)
        mycursor.execute(sql, val)

        mydb.commit()
        print("\n=== TAMBAH SALDO ===\nBerhasil menambah saldo sebesar Rp. ", nominal, "pada user", nohp)
    except:
        print("\nGagal menambah saldo pada user", nohp)

#Fungsi pembayaran dengan memotong saldo Gopay
def kurangi_saldo_gopay(nohp, nominal):
    try:
        saldo = cek_saldo_gopay(nohp)
        if saldo >= nominal:
            print("=== MEMULAI PENGURANGAN SALDO ===")
            sql = "UPDATE user SET saldo = saldo - %s WHERE telepon = %s"
            val = (nominal, nohp)
            mycursor.execute(sql, val)
            print("=== BERHASIL MENGURANGI SALDO ===")

            sql = "INSERT INTO history (telepon, nominal, keterangan) VALUES (%s, %s,'Pembayaran')"
            val = (nohp, nominal)
            mycursor.execute(sql, val)
            print("=== BERHASIL MENAMBAHKAN HISTORY TRANSAKSI ===")

            mydb.commit()
            print("\n====Pembayaran Berhasil ===\nBerhasil melakukan Pembayaran sebesar", nominal, "pada user", nohp)

            saldo = cek_saldo_gopay(nohp)
        else:
            print("\n=== Pembayaran Gagal ===\nSaldo yang anda miliki tidak mencukupi untuk melakukan transaksi.")
    except:
        print("\nGagal melakukan pembayaran pada user", nohp)

#Fungsi main yang digunakan untuk menampilkan menu yang digunakan untuk mengeksekusi program Gopay
if __name__ == '__main__':
    while True:
        command = input("=== HALAMAN UTAMA GOPAY ===\n1. Daftar akun Gopay\n2. Top Up Saldo\n3. Pembayaran\n4. Logout\n\nMenu => ")
        if command == "1":
            try:
                print("=== DAFTAR USER GOPAY BARU ===\n")
                new_name = input("Nama => ")
                new_nohp = input("No HP => ")

                register_gopay(new_nohp, new_name)
            except:
                print("Format Salah!\n")
        elif command == "2":
            try:
                nohp = input("No HP => ")
                print("Masukkan Nominal Saldo\n")
                add_saldo = int(input("Saldo => "))

                tambah_saldo_gopay(nohp, add_saldo)
            except:
                print("Format Salah!\n")
        elif command == "3":
            try:
                nohp = input("No HP => ")
                add_saldo = int(input("Masukkan Nominal Pembayaran => "))

                kurangi_saldo_gopay(nohp, add_saldo)
            except:
                print("Format Salah!\n")
        elif command == "4":
            break
        else:
            print("Command tidak ditemukan!\n")
