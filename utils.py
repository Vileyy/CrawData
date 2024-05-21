import json, os
from WebFilm import app
from WebFilm.models import Phim
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_phim(page = 1):
    listphim = Phim.query.all()
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return listphim[start:end]

def search_phim(keyword,page = 1):
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    search_result = Phim.query.filter(Phim.tenPhim.like('%{}%'.format(keyword))).all()
    return search_result[start:end]

def count_Phim():
    return Phim.query.count()
    
