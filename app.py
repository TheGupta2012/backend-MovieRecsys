from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import Recommender

app = Flask(__name__)
CORS(app)
REC = Recommender()
@app.route('/movie',methods = ['GET'])
def find_recommend():
    res = REC.get_recommendations(request.args.get('query'))
    return jsonify(res)

if __name__=='__main__':
    app.run(port= 5000, debug = True)
