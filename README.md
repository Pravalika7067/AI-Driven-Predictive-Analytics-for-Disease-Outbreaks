# 🏪 Disease Outbreak Prediction using Machine Learning

This repository contains code and documentation for predicting disease outbreaks using machine learning techniques. By leveraging historical data, environmental factors, and socio-economic indicators, the project aims to develop predictive models to identify the likelihood and intensity of disease outbreaks in specific regions.

---

## 🎥 Demo: Disease Prediction Web App

Watch the demo of the application in action:

[![Disease Prediction Demo](https://youtu.be/Q9zsqP_l_GM)](https://youtu.be/Q9zsqP_l_GM)

---

## ✨ Features

* **Data Preprocessing:** Handle missing values, normalize data, and engineer features relevant to disease outbreaks.
* **Exploratory Data Analysis (EDA):** Visualize trends, correlations, and spatial distributions.
* **Machine Learning Models:** Implement various models including Random Forest, Gradient Boosting, Neural Networks, and more.
* **Evaluation Metrics:** Assess model performance using accuracy, precision, recall, F1-score, and AUC-ROC.
* **Prediction Visualization:** Display predictions on maps and charts for intuitive understanding.
* ✅ **Multilingual Support:** Switch between **English and Tamil** within the web app.
* 🧾 **PDF Report Generation:** Download medical prediction reports in **PDF format**.
* 🔤 **Tamil Font Integration:** Ensures proper rendering of Tamil characters in generated PDFs.
  👉 [Download Tamil Font - Latha.ttf](https://www.cdnfonts.com/latha.font)

---

## 📚 Table of Contents

* [Getting Started](#getting-started)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Dataset](#dataset)
* [Models](#models)
* [Results](#results)
* [Contributing](#contributing)
* [Contact Information](#contact-information)

---

## 🚀 Getting Started

Follow the instructions below to set up the project and run the models on your system.

---

## 📦 Prerequisites

* Python 3.8+
* pip package manager

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/Janviswa/Disease-outbreak-prediction-using-Machine-Learning.git
cd Disease-outbreak-prediction-using-Machine-Learning
```

Create a virtual environment:

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

1. Prepare your dataset by placing it in the `data/` directory. Ensure it matches the expected format.

2. Run the preprocessing script:

   ```bash
   python preprocess.py
   ```

3. Train the machine learning models:

   ```bash
   python train.py
   ```

4. Evaluate the models and visualize results:

   ```bash
   python evaluate.py
   ```

5. Generate predictions for new data:

   ```bash
   python predict.py --input new_data.csv
   ```

6. Run the Streamlit web application:

   ```bash
   streamlit run app.py
   ```

---

## 🗃 Dataset

Supported datasets:

* **Heart Disease**: [Heart Disease Dataset on Kaggle](https://www.kaggle.com/ronitf/heart-disease-uci)
* **Diabetes**: [Diabetes Dataset on Kaggle](https://www.kaggle.com/datasets/mathchi/diabetes-data-set)
* **Parkinson's Disease**: [Parkinson's Dataset on Kaggle](https://www.kaggle.com/datasets/nidaguler/parkinsons-data)

---

## 🧠 Models

This project supports various machine learning models, including but not limited to:

* Decision Trees
* Random Forest
* Gradient Boosting (e.g., XGBoost, LightGBM)
* Neural Networks
* Support Vector Machines (SVM)

Includes hyperparameter tuning and model optimization.

---

## 📊 Results

Evaluation metrics used to assess model performance:

* Accuracy
* Precision
* Recall
* F1-score
* AUC-ROC

Visualizations display predictions and insights in spatial and temporal formats.

---

## 🌐 Multilingual Support

| Feature         | Language       |
| --------------- | -------------- |
| Interface Texts | English, Tamil |
| PDF Reports     | English, Tamil |

Tamil fonts are embedded into the PDF reports. If you’re facing any font rendering issues, [download the Latha Tamil font here](https://www.cdnfonts.com/latha.font) and install it locally.

---

## ✍️ Contributing

Contributions are welcome! To contribute:

1. Fork the repository.

2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit:

   ```bash
   git commit -m "Description of changes"
   ```

4. Push to the branch:

   ```bash
   git push origin feature-name
   ```

5. Create a pull request.

---

## 📬 Contact Information

For questions, feedback, or collaborations, feel free to reach out:

📧 Email: [jananiviswa05@gmail.com](mailto:jananiviswa05@gmail.com)
🔗 LinkedIn: [linkedin.com/in/janani-v](https://www.linkedin.com/in/jananiv05)

---
