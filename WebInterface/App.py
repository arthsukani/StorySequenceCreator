from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
from DeepAIModel.DeepAISearch import SearchData
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/GetData",methods=['POST'])
@cross_origin()
def getStory():
    jData = {}
    jData = request.get_json()
    searchText = jData["query"]
    response = SearchData(searchText)
    response["target_id"] = jData["target_id"]
    return jsonify(response)