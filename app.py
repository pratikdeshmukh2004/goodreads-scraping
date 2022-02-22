import concurrent.futures
import time
from scrap_data import *
from flask import Flask, request, g

app = Flask(__name__)

@app.before_request
def bef_req():
    g.start = time.time()

@app.after_request
def aft_req(res):
    print('\x1b[0;31;40m',"Exc Time:",time.time()-g.start, '\x1b[0m')
    return res

@app.route("/books")
def scrap_books():
    args  = request.args.to_dict(flat=True)
    if len(args)==0 or 'wishlist' not in args:
        return {'status':'error', "message":'Please provide wishlist.'}
    wish_list = args['wishlist']
    final = list_books_from_wishlist(wish_list)
    batch_list = []
    pagination = 10
    for i in range(0, len(final), pagination):
            batch_list.append(final[i:i + pagination])
    workers = int((len(final)/pagination)+1) if len(final)<100 else 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        result = executor.map(get_book_detail, batch_list)
    result  = list(result)
    results = []
    for r in result:
        results.extend(r)
    results = list(filter(lambda x: len(x)!=0, results))
    return {"status":'success', 'count': len(results), 'books': results}
    

@app.route("/gift_book")
def gift_book():
    args = request.args.to_dict(flat=True)
    return args

app.run(debug=True)