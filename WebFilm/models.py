from WebFilm import db

class Phim(db.Model):
    __tablename__ = 'phim'
    maPhim = db.Column(db.INT, primary_key=True)
    tenPhim = db.Column(db.String(100))
    ngayChieu = db.Column(db.String(2000))
    chatLuong = db.Column(db.String(20))
    noiSanXuat = db.Column(db.String(2000))
    thoiLuong = db.Column(db.String(2000))
    namPhatHanh = db.Column(db.String(2000))
    theLoai = db.Column(db.String(2000))
    tenDaoDien = db.Column(db.String(2000))
    tenDienVien = db.Column(db.String(2000))
    moTa = db.Column(db.String(2000))
    anh = db.Column(db.String(2000))
    link = db.Column(db.String(2000))
    def __repr__(self):
        return f"Phim(MaPhim='{self.maPhim}',TenPhim='{self.tenPhim},NgayChieu='{self.ngayChieu},ChatLuong='{self.chatLuong}',NoiSanXuat='{self.noiSanXuat},ThoiLuong='{self.thoiLuong},namPhatHanh='{self.namPhatHanh}',TheLoai='{self.theLoai},TenDaoDien='{self.tenDaoDien}',TenDienVien='{self.tenDienVien}',MoTa='{self.moTa}',Anh='{self.anh}',Link='{self.link}')"
