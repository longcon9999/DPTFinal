import os
import cv2
import glob

from flask import Flask, render_template, request, jsonify, redirect
from skimage import io
from colordescriptor import ColorDescriptor
from seacher import Searcher
from werkzeug.utils import secure_filename

# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')
url = "http://127.0.0.1:5000/static/queries/"
app.config["IMAGE_UPLOADS"] = os.path.join(os.path.dirname(__file__), "static/queries/")

# main route
@app.route('/')
def index():
    content = []
    for file in glob.glob("static/queries/*.png"):
        content.append(file)
    print(content)
    return render_template('index.html', queries=content)


@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        RESULTS_ARRAY = []
        image_url = request.form.get('img')

        try:
            cd = ColorDescriptor((10, 12, 4))
            query = io.imread(image_url)
            # (h, w, d)
            if query.shape[2] == 4:
                (r, g, b, a) = cv2.split(query)
            else:
                (r, g, b) = cv2.split(query)
            query = cv2.merge([b, g, r])
            features = cd.describe2d(query)
            # print(features)
            searcher = Searcher(INDEX)
            results = searcher.search(features)
            for (score, resultID) in results:
                print("{} : {}".format(resultID, score))

            for (score, resultID) in results[:10]:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})
            return jsonify(results=RESULTS_ARRAY)
        except Exception as e:
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect("/")
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            return redirect("/")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
