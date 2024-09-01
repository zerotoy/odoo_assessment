# odoo_assessment
Odoo Assessment

Cara install dan menjalankan:
1. Install aplikasi odoo
    Untuk cara menginstallnya dapat mengikuti langkah langkah yang diberikan di :
    
    # Ubuntu
    https://www.cybrosys.com/blog/how-to-install-odoo-16-on-ubuntu-2004-lts

    # Windows
    https://www.cybrosys.com/blog/how-to-install-odoo-16-in-windows-11

    # Mac
    https://ajsebastian.medium.com/tanpa-docker-tutorial-instalasi-odoo-16-secara-local-sol-di-mac-m1-dengan-macos-monterey-915ded5ba86e

2. Set odoo.conf
    Setelah mengingstall, langkah selanjutnya adalah mengedit odoo.conf untuk menambahkan addons tambahan yang telah saya custom. Penambahan addons ini dilakuan dengan dengan cara menambahkan path ke addons_path seperti dibawah ini :
    addons_path = C:\program files\odoo 16.0.20231128\server\odoo\addons,[path ke folder git ini]/addons

3. Jalankan odoo
    Setelah menambahkan addons yang telah dikostumisasi, maka jalankan aplikasi odoo. Untuk caranya bisa diikuti dari langkah yang diberikan pada proses instalasi.

4. Setup database
    Setelah menjalankan odoo, maka dilakukan setup database. Jika anda ingin menggunakan database yang telah disediakan oleh saya, maka lakukanlah restore database dengan file database yang tersedia pada folder database. Jika anda ingin menggunakan database yang sudah adapun tidak apa-apa. Dan yang terpenting adalah pastikan odoo berjalan dengan 1 database atau terdefinisi pada odoo.conf atau pada saat menjalankan/run odoo

5. Install Modul
    Jika anda menggunakan database yang telah saya sediakan, maka anda tidak perlu menginstall modul. Jika tidak, maka anda dapat menginstall modul di menu Apps dan install modul yang bernama room_module

## Notes:
    Adapun beberapa perubahan dari requirement yang diberikan pada soal. Hal ini saya lakukan karena hal tambahan yang saya berikan, saya anggap merupakan hal yang bersifat improvement
    perubahan yang diberikan :
        1. Status pemesanan dirubah menjadi Draft, On Going, Done, dan Cancel dengan value di odoo ['draft','progress','done','cancel']
        2. Tanggal pemesanan saya ubah menjadi waktu pemesanan yang memiliki range atau memiliki start dan end datenya, sehingga pemesanan atau booking dapat dilakukan dengan range waktu tertentu
        3. Waktu pemesanan tidak akan terjadi overlapping antara satu pesanan dengan yang lainnya, kecuali untuk pesanan yang telah di cancel
        4. Status pesanan hanya dapat di cancel ketika pesanan sedang berada di status draft
# API
    API yang saya buat hanya 1 API yang dapat melakukan get data untuk reservasi saja contoh API yang dapat dijalankan dengan data dari database yang saya sediakan, yaitu :
    
    http:localhost:8069/get_reservations?room=Aula&state=progress&time=2024-09-02 16:00:00&pemesan=Jane Smith&reservation_no=ROOM-RES/09/2024/0002&reservation_id=2
    
    Disana ada beberapa parameter yang dapat anda isi, yaitu:
    room => (string) diisi dengan nama ruangan yang akan anda cari
    state => (string) diisi dengan status pemesanan yang akan dicari dan hanya dapat disi oleh salah satu dari ['draft','progress','done','cancel']. Namun secara default tidak akan mencari reservasi dengan status done atau cancel
    pemesan => (string) diisi dengan nama pemesan yang akan dicari
    time => (string) diisi dengan waktu. Sistem akan mencari apakah pada waktu tersebut terdapat reservasi atau tidak
    reservation_no => (string) diisi dengan nama atau nomor reservasi tersebut
    reservation_id => (integer) diisi dengan id dari reservasi tersebut
    
    Setiap parameter dapat dicantumkan atau tidak sama sekali