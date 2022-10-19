from flask import Flask, render_template, Response
import cv2
import HandTrackingModule as htm
import pyautogui as p

app = Flask(__name__)

camera = cv2.VideoCapture(0)  

def gen_frames(): 
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(detectionCon=0.75)
    tipIds = [4, 8, 12, 16, 20]
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
           
        if len(lmList) != 0:
            fingers = []
            
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            totalFingers = fingers.count(1)
            #print(totalFingers)
            if totalFingers == 1:
                 p.press("right") 
                 cv2.putText(img, "Forward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                
            elif totalFingers == 2:
                p.press("left")
                  
                cv2.putText(img, "Backward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)   
                 
                
            elif totalFingers == 3:
                p.press("up")
                 
                cv2.putText(img, "Volume UP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                
            elif totalFingers == 4:
                p.press("down")
                  
                cv2.putText(img, "Volume Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
               
            elif totalFingers == 5:
                p.press("space")
                cv2.putText(img, "Play/Pause", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                
            else:     
                pass   
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(25) &0xFF    
        if key == 27: 
            break
    
    cap.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/view_instructions',methods=['POST'])
def view_instructions():
    return render_template('move.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
