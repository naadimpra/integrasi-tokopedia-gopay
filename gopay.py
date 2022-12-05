# Library yang digunakan agar program python dapat menggunakan database mysql
import mysql.connector

# Melakukan koneksi ke database gopay
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="gopay"
)

# mysql cursor untuk melakukan eksekusi statement yang berkomunikasi dengan mysql database
mycursor = mydb.cursor()

# fungsi untuk mendaftarkan akun baru pada gopay
def new_gopay_user(nohp, nama):
    try:
        sql = "INSERT INTO user (telepon, nama, saldo) VALUES (%s, %s, 0)"
        val = (nohp, nama)
        mycursor.execute(sql, val)

        mydb.commit()
        print("\n[PENDAFTARAN BERHASIL]\nBerhasil mendaftarkan user", nama)
    except:
        print("\nGagal mendaftarkan user baru\n")

# fungsi untuk mengecek apakah user sudah terdaftar atau belum
def check_user(nohp):
    try:
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (nohp, )
        mycursor.execute(sql, val)

        result = mycursor.fetchall()

        if len(result) == 1:
            print("\n[CEK AKUN]\nAkun dengan No HP", nohp,"tersedia")
            return(1)
        else:
            print("\n[CEK AKUN]\nAkun dengan No HP", nohp,"tidak tersedia")
            return(0)
    except:
        print("Gagal mendapatkan informasi akun", nohp)

# fungsi untuk menampilkan saldo gopay
def check_gopay_balance(nohp):
    try:
        sql = "SELECT * FROM user WHERE telepon = %s"
        val = (nohp, )
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        print("\n[CEK SALDO]\nSaldo", result[1],"saat ini = Rp.", result[2])

        return(result[2])
    except:
        print("\nGagal mendapatkan informasi akun", nohp)

# fungsi untuk menampilkan history penggunaan akun gopay (pembayaran/topup) 
def check_history(nohp, date):
    try:
        sql = "SELECT * FROM history WHERE telepon = %s AND tanggal_history <= %s"
        val = (nohp, date)
        mycursor.execute(sql, val)

        results = mycursor.fetchall()
        print(f"HISTORY SAMPAI TANGGAL {date}:\n")
        return results
    except:
        print("\nGagal mendapatkan history akun", nohp)

# fungsi untuk melakukan topup saldo gopay
def increase_gopay_balance(nohp, nominal):
    try:
        print("\n[MENAMBAH SALDO]")
        sql = "UPDATE user SET saldo = saldo + %s WHERE telepon = %s"
        val = (nominal, nohp)
        mycursor.execute(sql, val)

        sql = "INSERT INTO history (telepon, nominal, keterangan) VALUES (%s, %s,'Top Up Saldo')"
        val = (nohp, nominal)
        mycursor.execute(sql, val)

        mydb.commit()
        print("\n[TAMBAH SALDO]\nBerhasil menambah saldo sebesar", nominal, "pada user", nohp)
    except:
        print("\nGagal menambah saldo pada user", nohp)

# fungsi pembayaran dengan potong saldo gopay
def decrease_gopay_balance(nohp, nominal):
    try:
        saldo = check_gopay_balance(nohp)
        if saldo >= nominal:
            print("MULAI DECREASE")
            sql = "UPDATE user SET saldo = saldo - %s WHERE telepon = %s"
            val = (nominal, nohp)
            mycursor.execute(sql, val)
            print("SELESAI UPDATE DECREASE")

            sql = "INSERT INTO history (telepon, nominal, keterangan) VALUES (%s, %s,'Pembayaran')"
            val = (nohp, nominal)
            mycursor.execute(sql, val)
            print("SELESAI HISTORY DECREASE")

            mydb.commit()
            print("\n[Pembayaran Berhasil]\nBerhasil melakukan Pembayaran sebesar", nominal, "pada user", nohp)

            saldo = check_gopay_balance(nohp)
        else:
            print("\n[Pembayaran Gagal]\nSaldo anda tidak mencukupi")
    except:
        print("\nGagal melakukan pembayaran pada user", nohp)

# fungsi main yang digunakan untuk menampilkan menu yang digunakan untuk mengeksekusi program gopay
if __name__ == '__main__':
    while True:
        command = input("[PILIH MENU]\n1. Daftar akun gopay\n2. Top Up Saldo\n3. Pembayaran\n4. Exit\n\nMenu -> ")
        if command == "1":
            try:
                print("[DAFTAR USER BARU]\n")
                new_name = input("Nama -> ")
                new_nohp = input("No HP -> ")

                new_gopay_user(new_nohp, new_name)
            except:
                print("Format Salah!\n")
        elif command == "2":
            try:
                nohp = input("No HP -> ")
                print("Masukkan Nominal Saldo\n")
                add_saldo = int(input("Saldo -> "))

                increase_gopay_balance(nohp, add_saldo)
            except:
                print("Format Salah!\n")
        elif command == "3":
            try:
                nohp = input("No HP -> ")
                print("Masukkan Nominal Pembayaran\n")
                add_saldo = int(input("Saldo -> "))

                decrease_gopay_balance(nohp, add_saldo)
            except:
                print("Format Salah!\n")
        elif command == "4":
            break
        else:
            print("Opsi tidak tersedia\n")
