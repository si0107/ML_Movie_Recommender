from flask import Flask, request
from flask_cors import CORS
from ML_recommender import recListMovie

app = Flask(__name__)
CORS(app)

@app.route("/movie", methods=["POST"])
def movie_recs_list():
    try:
        out = {}
        ids = request.args.get("ids") # get the comma separated ids
        ids = ids.split(",") # split the ids with ,
        for i in range(len(ids)):
            ids[i] = int(ids[i].strip()) # removing unnecesary spaces
        movie100 = recListMovie(ids)
        movie100 = list(map(int, movie100))
        out["recommendation"] = movie100
        return out
    except IndexError as err:
        return {"error": f"Maybe movie_ID does not exist in database. {err}"} 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)