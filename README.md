# Real‑Time‑Weapon‑Detection

**Detect Threats Instantly, Secure with Confidence**

Built with Flask, Python, NumPy, and Twilio, this application uses YOLOv8 to detect weapons live from camera feeds, logging each detection event and sending instant email/SMS alerts. :contentReference[oaicite:1]{index=1}

---

## Overview

Real‑Time‑Weapon‑Detection is a powerful security tool intended to identify weapons instantly through live camera input. Key features include:

- **🛡 Real‑Time Detection**: Uses **YOLOv8** to analyze live video streams with high accuracy.  
- **📊 Detection Logging**: Records events with metadata (timestamps, image snapshots, etc.) for review.  
- **📢 Alerting System**: Sends notifications via email and SMS, powered by Twilio integration.  
- **🌐 Web Dashboard**: Provides a responsive interface for viewing live feeds, detection history, and system configuration.  
- **⚙ Seamless Setup**: Uses a well-defined `requirements.txt` to ensure environment consistency.  
- **🔍 Historical Data Review**: Enables users to browse past detection events using the web dashboard UI.

---

## Getting Started

### Prerequisites

- Python (3.8+ recommended)  
- Pip package manager  
- A webcam or IP camera for streaming input  
- Twilio account with API credentials for alerts  

### Installation

```bash
git clone https://github.com/kushalpatel0265/Real-Time-Weapon-Detection.git
cd Real-Time-Weapon-Detection
pip install -r requirements.txt
````

---

### Configuration

1. **YOLOv8 Model**
   Place your pretrained YOLOv8 `.pt` model file in the designated folder (e.g. `weights/`).

2. **Environment Variables / Config File**
   Configure the following settings:

   * Twilio account SID, auth token, sender phone number
   * Email SMTP details (server, port, sender credentials, recipient list)
   * Camera stream URL or local webcam index

---

### Usage

To launch the application:

```bash
python app.py
```

Replace `app.py` with the actual entrypoint file name configured in your repository.

Once running, access the web dashboard (typically at `http://localhost:5000`) to view live camera stream, recent detections, and system settings.

---

### Features & Workflow

1. **Live video input** is fed into the YOLOv8 model for inference.
2. When a weapon is detected, a **log entry is created** in the database (e.g. SQLite or JSON).
3. A **notification** is immediately dispatched via Twilio (SMS) and/or email.
4. All past detections are accessible through a sleek **web interface** for analysis and verification.

---

### Dependencies & Technologies

* **Flask** — lightweight web server and dashboard framework
* **NumPy** — for numeric operations and image preprocessing
* **Python** — main programming language
* **Twilio SDK** — for SMS/email alerting
* **YOLOv8** — object detection base model for weapon detection

---

### Contribution & Feedback

Contributions are welcome! If you’d like to:

* Improve detection accuracy
* Add support for different camera systems
* Enhance notification logic
  ...please open a GitHub issue or submit a pull request.

---

### License

Distributed under the MIT License. See the `LICENSE` file for full details.

---

### Acknowledgments

* Inspired by weapon detection projects utilizing YOLOv8 architecture and real-time alerting pipelines
  ([researchgate.net][1], [github.com][2], [arxiv.org][3], [scribd.com][4])
* Many thanks to the open-source communities behind Flask, Twilio, NumPy, and YOLOv8!

---

### Contact

For questions or business inquiries, please email **\kushalpatel0265@gmail.com** or open an issue on GitHub.

---
