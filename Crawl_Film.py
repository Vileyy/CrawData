import requests
from bs4 import BeautifulSoup
import mysql.connector

# Kết nối đến cơ sở dữ liệu MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="dbwebfilm",
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)
cursor = db.cursor()

# Hàm tạo bảng nếu chưa tồn tại
def create_table():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `Phim` (
                `MaPhim` INT AUTO_INCREMENT PRIMARY KEY,
                `TenPhim` NVARCHAR(500) DEFAULT NULL,
                `NgayChieu` NVARCHAR(200) DEFAULT NULL,
                `ChatLuong` NVARCHAR(200) DEFAULT NULL,
                `NoiSanXuat` NVARCHAR(300) DEFAULT NULL,
                `ThoiLuong` NVARCHAR(200) DEFAULT NULL,
                `NamPhatHanh` NVARCHAR(200) DEFAULT NULL,
                `TheLoai` NVARCHAR(600) DEFAULT NULL,
                `TenDaoDien` NVARCHAR(200) DEFAULT NULL,
                `TenDienVien` NVARCHAR(200) DEFAULT NULL,
                `MoTa` TEXT DEFAULT NULL,
                `Anh` NVARCHAR(1000) DEFAULT NULL,
                `Link`NVARCHAR(1000) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        db.commit()
    except mysql.connector.Error as err:
        print(err.msg)

# # Hàm chèn dữ liệu vào bảng
def insert_data(name_film, date, quality, country, duration,Nam,TheLoai,DirectorName,ActionName, description,img,link_film):
    try:
        sql = "INSERT INTO Phim (`TenPhim`, `NgayChieu`, `ChatLuong`, `NoiSanXuat`, `ThoiLuong`, `NamPhatHanh`, `TheLoai`,`TenDaoDien`, `TenDienVien`, `MoTa`,`Anh`,`Link`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name_film, date, quality, country, duration,Nam,TheLoai,DirectorName,ActionName, description,img,link_film)
        cursor.execute(sql, val)
        db.commit()
        print("Thêm thành công")
    except mysql.connector.Error as err:
        print(err.msg)

# # Hàm thu thập dữ liệu từ trang web và chèn vào cơ sở dữ liệu
def crawl_and_insert():
    for page in range(1, 3):
        url = f"https://phimmoi.tech/genre/phim-le/page/{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        phimmoi = soup.find_all("article",{"class": "item movies"})
        for movies in phimmoi:
            poster = movies.find("div",{"class": "poster"})
            img = poster.find("img")['src']
            quality = poster.find("div",{"class": "btnRV"}).get_text()
            data = movies.find("div",{"class": "data"})
            link_film = data.find("a")['href']
            name_film = data.find("h3").get_text()
            date = data.find("span").get_text()
            
            url1 = link_film
            thongtinphim = requests.get(url1)
            soup = BeautifulSoup(thongtinphim.content, 'html.parser')
            phimmoi_details = soup.find_all("div",{"class": "sheader"})
            mota_phim = soup.find_all("div",{"class": "sbox"})
            tendienvien = soup.find_all("div",{"class":"sbox fixidtab"})
            for chitietphim in phimmoi_details:
                # Tạo mốt biến là chuỗi để gán dữ liệu
                NameDicr = []
                NamAction = []
                Nam = []
                TheLoai = []
                description = []
                country = chitietphim.find("span",{"class": "country"}).get_text()
                duration = chitietphim.find("span",{"class": "runtime"}).get_text()
                genres = chitietphim.find("div",{"class": "sgeneros"})
                genres = genres.find_all("a")
                # gán genres thành 1 chuỗi
                genres = ', '.join(tag.get_text() for tag in genres)
                # tách chuỗi thành 1 split để dễ dàng lấy chuỗi ra ngoài theo dạng 0,1,2,3,4,...
                genres_list = genres.split(', ')
                # lấy năm bắt đầu từ chuỗi 0
                Nam = genres_list[0]
                TheLoai = genres_list[1::]
                TheLoai = ', '.join(TheLoai)
                for motafilms in mota_phim:
                    findmota = motafilms.find("p")
                    if findmota:
                        description = findmota.get_text()
                # lồng vòng lặp để lấy ra tên Direction từ itemprop director
                for _tendienvien in tendienvien:
                    nameDi = _tendienvien.find_all("div", {"itemprop": "director"})
                    for _nameDi in nameDi:
                        nameDia = _nameDi.find_all("a", {"itemprop": "url"})
                        
                        for _nameDi in nameDia:
                            NameDicr.append(_nameDi.get_text())
                        
                # lồng vòng lặp để lấy ra tên Diễn Viên từ itemprop actor        
                    nameAc = _tendienvien.find_all("div", {"itemprop": "actor"})
                    for _nameAC in nameAc:
                    
                        nameAct =_nameAC.find_all("a", {"itemprop": "url"})
                        for _nameAc in nameAct:
                            NamAction.append(_nameAc.get_text())
                    
                ActionName = ', '.join(NamAction)
                DirectorName = ', '.join(NameDicr)
                print([name_film, date, quality, country, duration,Nam,TheLoai,DirectorName,ActionName,description,img,link_film])
                # Chèn dữ liệu vào bảng
                insert_data(name_film, date, quality, country, duration,Nam,TheLoai,DirectorName,ActionName, description,img,link_film)

# Tạo bảng nếu chưa tồn tại
create_table()

# Thu thập dữ liệu từ trang web và chèn vào cơ sở dữ liệu
crawl_and_insert()