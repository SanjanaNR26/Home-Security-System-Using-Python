import cv2
import smtplib
import os
import time
import threading
from datetime import datetime

EMAIL_USER = os.environ.get("ALERT_EMAIL_USER", "your_email@gmail.com")
EMAIL_PASS = os.environ.get("ALERT_EMAIL_PASS", "your_app_password")
EMAIL_TO = os.environ.get("ALERT_EMAIL_TO", "receiver_email@gmail.com")

CAPTURE_INDEX = int(os.environ.get("CAM_INDEX", "0"))
MIN_AREA = int(os.environ.get("MIN_MOTION_AREA", "1000"))
ALERT_COOLDOWN = int(os.environ.get("ALERT_COOLDOWN_SECONDS", "60"))  # seconds

cap = cv2.VideoCapture(CAPTURE_INDEX)
if not cap.isOpened():
    raise SystemExit(f"Camera index {CAPTURE_INDEX} cannot be opened. Check camera or index.")

def send_alert():
    try:
        print(f"[{datetime.now()}] Sending alert email to {EMAIL_TO}...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        subject = "Intruder Alert!"
        body = f"Motion detected at {datetime.now().isoformat()}"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_USER, EMAIL_TO, message)
        server.quit()
        print("Alert sent.")
    except Exception as e:
        print("Failed to send alert:", e)


first_frame = None
for _ in range(10):  
    ret, frame = cap.read()
    if ret:
        first_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)
        first_frame = first_gray
        break
    time.sleep(0.1)

if first_frame is None:
    cap.release()
    raise SystemExit("Unable to read initial frame from camera.")

last_alert_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame read failed, trying again...")
            time.sleep(0.1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        for contour in contours:
            if cv2.contourArea(contour) < MIN_AREA:
                continue
            motion = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Security Feed", frame)

        if motion and (time.time() - last_alert_time) > ALERT_COOLDOWN:
            last_alert_time = time.time()
            threading.Thread(target=send_alert, daemon=True).start()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()