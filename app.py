from signature_module import match_signatures
from flask import Flask, request
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def test():
    return "Hello World!"


@app.route("/endpoint", methods=["POST"])
def handle_post_request():
    image_data_base64 = request.json["first_image"]
    second_imagedata_base64 = request.json["second_image"]

    # Decode the base64 encoded image data
    image_data = base64.b64decode(image_data_base64)
    second_image_data = base64.b64decode(second_imagedata_base64)

    # Specify the path to save the image
    first_image_path = "first_image.jpg"
    second_image_path = "second_image.jpg"

    # Save the image locally
    with open(first_image_path, "wb") as f:
        f.write(image_data)

    with open(second_image_path, "wb") as f:
        f.write(second_image_data)

    return match_signatures(first_image_path, second_image_path), 200


if __name__ == "__main__":
    app.run(debug=True)
