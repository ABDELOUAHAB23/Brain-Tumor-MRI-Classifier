# 🧠 Brain Tumor MRI Classifier (Flask + TensorFlow)

This project is a **web application for brain tumor detection from MRI images**.

It uses a trained **TensorFlow / Keras deep learning model** to classify MRI scans into four categories:

- **No Tumor**
- **Glioma**
- **Meningioma**
- **Pituitary Tumor**

A lightweight **Flask backend** provides both:

- A **web interface** for uploading MRI images  
- A **REST API** that returns predictions in JSON format

---
# Brain Tumor MRI Classifier

This project detects brain tumors from MRI images.

![Brain Tumor MRI Example](images/diagram.png)
# 🚀 Features

- Upload MRI images directly from a browser
- Automatic **image preprocessing**
- **Deep learning prediction** using TensorFlow
- Server-side **image validation**
- JSON API for integration with other systems
- Displays:
  - Predicted tumor class
  - Description of the tumor
  - Probability for each class
  - Confidence level (High / Medium / Low)
- **CORS enabled** for frontend integration

---

# 📁 Project Structure

```
Brain-Tumor-Classifier/
│
├── app.py
├── requirements.txt
├── Brain_Tumor_Model.h5
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

### Files

| File | Description |
|-----|-------------|
| `app.py` | Flask backend application |
| `Brain_Tumor_Model.h5` | Pretrained TensorFlow model |
| `requirements.txt` | Python dependencies |
| `templates/index.html` | Upload interface |
| `static/` | CSS, JS, images |

---

# ⚙️ Requirements

Recommended:

- **Python 3.9 – 3.11**
- **pip**
- **virtual environment (venv)**

Dependencies:

```
Flask==2.3.2
flask-cors==4.0.0
tensorflow==2.13.0
Pillow==10.2.0
numpy==1.24.3
```

⚠️ Important:

TensorFlow **2.13 is compatible with NumPy 1.x only**.

---

# 🔧 Setup & Installation

Open your terminal or PowerShell.

### 1️⃣ Navigate to the project

```
cd "path/to/Brain Tumor"
```

---

### 2️⃣ Create virtual environment

```
python -m venv .venv
```

Activate it.

Windows:

```
.\.venv\Scripts\activate
```

Mac / Linux:

```
source .venv/bin/activate
```

---

### 3️⃣ Upgrade pip

```
pip install --upgrade pip
```

---

### 4️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 5️⃣ Make sure the model exists

Place the model file in the root folder:

```
Brain_Tumor_Model.h5
```

Example structure:

```
Brain Tumor/
│
├── app.py
├── Brain_Tumor_Model.h5
└── requirements.txt
```

---

# ▶️ Running the Application

Activate the environment if needed:

Windows:

```
.\.venv\Scripts\activate
```

Run the application:

```
python app.py
```

The server will start at:

```
http://127.0.0.1:5000
```

Open your browser and upload an MRI image.

---

# 🌐 API Usage

## Endpoint

```
POST /predict
```

### Content-Type

```
multipart/form-data
```

### Field Name

```
file
```

### Supported Formats

- PNG
- JPG
- JPEG
- GIF
- BMP

---

# 📡 Example Request

```
curl -X POST http://127.0.0.1:5000/predict \
  -F "file=@/path/to/mri_image.jpg"
```

---

# 📊 Example JSON Response

```json
{
  "result": "Glioma",
  "description": "A type of tumor that starts in the glial cells of the brain or spine.",
  "probabilities": {
    "No Tumor": 0.23,
    "Glioma": 97.51,
    "Meningioma": 1.02,
    "Pituitary": 1.24
  },
  "confidence_level": "High"
}
```

### Response Fields

| Field | Description |
|------|-------------|
| result | Predicted tumor type |
| description | Explanation of tumor |
| probabilities | Model probability for each class |
| confidence_level | Prediction confidence |

---

# ⚠️ NumPy / TensorFlow Compatibility

Sometimes you may see this error:

```
A module compiled using NumPy 1.x cannot run in NumPy 2.x
AttributeError: _ARRAY_API not found
```

This happens because:

- TensorFlow **2.13 requires NumPy 1.x**
- NumPy **2.x was installed automatically**

### Fix

Create a clean environment and install the correct versions:

```
pip install tensorflow==2.13.0
pip install numpy==1.24.3
```

or simply:

```
pip install -r requirements.txt
```

Make sure your terminal shows:

```
(.venv)
```

before running the app.

---

# 🧠 Model Information

The application uses a **Keras CNN model** stored as:

```
Brain_Tumor_Model.h5
```

Input shape:

```
(224, 224, 3)
```

Output classes:

```
1. No Tumor
2. Glioma
3. Meningioma
4. Pituitary
```

If you retrain the model, make sure to update:

```
CLASS_NAMES
```

in `app.py`.

---

# ⚠️ Disclaimer

This project is for **educational and research purposes only**.

It **must not be used for real medical diagnosis**.

Always consult a **qualified medical professional**.

---

# 📜 License

You can use the **MIT License** or another open-source license.

Example:

```
MIT License
Copyright (c) 2026
```

Or create a `LICENSE` file in the repository.
