import cv2
import numpy as np
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['file']

    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray,50,150)

    contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    largest = max(contours,key=cv2.contourArea)

    x,y,w,h = cv2.boundingRect(largest)

    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

    cx = int(x+w/2)
    cy = int(y+h/2)

    cv2.circle(image,(cx,cy),6,(0,0,255),-1)

    cell_w = int(w/3)
    cell_h = int(h/3)

    for i in range(1,3):
        cv2.line(image,(x+i*cell_w,y),(x+i*cell_w,y+h),(255,0,0),2)
        cv2.line(image,(x,y+i*cell_h),(x+w,y+i*cell_h),(255,0,0),2)

    cv2.imwrite("result.png",image)

    return send_file("result.png")

app.run(host="0.0.0.0", port=10000)
