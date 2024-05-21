from flask import Flask, render_template,request
from WebFilm import app
import utils
import math

@app.route("/")
def home():
    return render_template('index.html')

# @app.route("/products")
# def products_list():
#     phim = utils.load_phim()
#     return render_template('products.html', countproducts=phim)

@app.route("/ListFilm")
def list_phim():
    page = request.args.get('page', 1)
    page = int(page)
    phim = utils.load_phim(page=page)
    count = utils.count_Phim()
    return render_template('ListFilm.html', list_noidung = phim,pages=math.ceil(count/app.config['PAGE_SIZE']),page=page,count=count)

@app.route("/search", methods=['GET'])
def search():
    page = request.args.get('page', 1)
    page = int(page)
    count = utils.count_Phim()
    keyword = request.args.get('keyword')
    if keyword:
        search_result = utils.search_phim(keyword,page)
        count = len(search_result)
        return render_template('search_film.html',keyword = keyword, search_result = search_result,pages=math.ceil(count/app.config['PAGE_SIZE']),page=page,count=count)
    else:
        return render_template('search_film.html',keyword = keyword, search_result = [])
if __name__ == '__main__':
    app.run(debug=True)