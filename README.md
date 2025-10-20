**Motion Detection + Email Alert**

Lightweight motion detector using OpenCV that sends an email alert (SMTP) when motion is detected.

**Features**

Detects motion by frame-differencing and contour area thresholding

Draws bounding boxes on detected motion in a live window

Sends email alerts (SMTP) in background threads to avoid blocking the UI

Configurable via environment variables

**Requirements**

Python 3.8+,

pip packages:

opencv-python

Standard library modules used: smtplib, threading, os, time, datetime

**Installation**

Run in PowerShell or CMD from the project folder:

python -m pip install --upgrade pip

python -m pip install opencv-python

Configuration

The script reads configuration from environment variables. Defaults are provided but you should set your production values.

ALERT_EMAIL_USER — SMTP username (your email)

ALERT_EMAIL_PASS — SMTP password (use an app password for providers like Gmail)

ALERT_EMAIL_TO — recipient email address

CAM_INDEX — camera index (default 0). Try 0, 1, 2 if your camera is not at 0.

MIN_MOTION_AREA — minimum contour area in pixels to count as motion (default 1000)

ALERT_COOLDOWN_SECONDS — minimum seconds between alert emails (default 60)

Set environment variables in PowerShell:

$env:ALERT_EMAIL_USER = "you@example.com"

$env:ALERT_EMAIL_PASS = "your_app_password"

$env:ALERT_EMAIL_TO = "recipient@example.com"

$env:CAM_INDEX = "0"

Important: for Gmail, create an App Password (recommended) instead of using your account password.

Troubleshooting

"Camera index X cannot be opened": try a different CAM_INDEX (1, 2) or ensure your camera is not used by another app.

"ModuleNotFoundError: No module named 'cv2'": install opencv-python into the interpreter you run (see Installation).

No console output: make sure you launched the correct file and Python executable (run python --version and where python).

SMTP login fails: verify EMAIL_USER and EMAIL_PASS, allow SMTP or use an app password, check network/firewall.

If running in a headless server (no display), remove cv2.imshow and window handling or use a virtual framebuffer.

Security notes

Do not hard-code credentials in the script. Prefer environment variables or a secure secret store.

Use app-specific passwords where possible.

If you want any of the README sections expanded or want an example systemd/task scheduler entry (Windows Task Scheduler) to auto-run the script, say which and I will add it.

GPT-5 mini • 1x
