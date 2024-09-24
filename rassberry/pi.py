import cv2
import time
import requests

harcascade = "haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0
last_save_time = time.time()
save_interval = 5  # seconds
server_url = 'http://127.0.0.1:8000/process-image/'

while True:
    success, img = cap.read()
    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)

            # Save and send the image if the interval has passed
            current_time = time.time()
            if current_time - last_save_time > save_interval:
                img_path = "plates/scaned_img_" + str(count) + ".jpg"
                cv2.imwrite(img_path, img_roi)  
                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
                
                # Send the image to the Django server
                with open(img_path, 'rb') as img_file:
                    response = requests.post(server_url, files={'file': img_file})
                    print(response.json())
                
                last_save_time = current_time
                count += 1

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()