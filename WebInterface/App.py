from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
from DeepAIModel.DeepAISearch import SearchData
from GoogleSearchInterface.Interface import GoogleInterface
import asyncio
import threading

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/home")
def index():
    return render_template("home.html")


async def getAsyncStory(searchText,jData):
    print(searchText)
    GObj = GoogleInterface("")
    GObj.setKeywords(searchText)
    response = {}
    response["output_url"] = GObj.gettingUrls()
    response["target_id"] = jData["target_id"]
    return response

@app.route("/GetData",methods=['POST'])
@cross_origin()
def getStory():
    jData = request.get_json()
    searchText = jData["query"]

    print(f"Inside Flask Function: {threading.currentThread().name}")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(getAsyncStory(searchText,jData))
    return jsonify(result)