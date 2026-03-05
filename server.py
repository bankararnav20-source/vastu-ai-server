from flask import Flask, request, send_file
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return "Vastu AI Server Running"

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    h, w = img.shape[:2]

    # center point
    cx = w // 2
    cy = h // 2

    cv2.circle(img, (cx, cy), 10, (0,0,255), -1)

    # draw 3x3 grid
    for i in range(1,3):
        cv2.line(img, (int(w*i/3),0), (int(w*i/3),h), (0,255,0), 2)
        cv2.line(img, (0,int(h*i/3)), (w,int(h*i/3)), (0,255,0), 2)

    output = "result.png"
    cv2.imwrite(output, img)

    return send_file(output, mimetype="image/png")


if __name__ == "__main__":
    app.run()
