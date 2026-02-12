# 🛡️ PhishGuard: AI-Powered Phishing Detection System

**PhishGuard** is a sophisticated web application designed to detect and classify phishing websites in real-time. It utilizes a **Hybrid Detection Engine** that combines machine learning (Gradient Boosting) with heuristic keyword analysis to identify malicious URLs with high accuracy.



## 🚀 Key Features

* **Hybrid Detection Engine:**
    * **AI Model:** Uses a **Gradient Boosting Classifier** to analyze structural URL features (length, special characters, IP usage).
    * **Heuristic Scanner:** Applies a penalty system for URLs containing high-risk social engineering keywords (e.g., "banking", "secure", "login").
* **Real-Time Analysis:** Instantly extracts and processes 8 key features from any input URL.
* **Visual Risk Scoring:** Provides a clear percentage-based safety score, categorizing sites as **Safe**, **Suspicious**, or **Phishing**.
* **Interactive Dashboard:** Built with **Streamlit**, offering a clean, professional dark-themed UI with detailed technical telemetry and risk breakdown.

## 🛠️ Technology Stack

* **Frontend:** Streamlit (Python web framework)
* **Machine Learning:** Scikit-Learn (Gradient Boosting Classifier)
* **Data Processing:** Pandas, NumPy
* **Model Serialization:** Joblib
* **Language:** Python 3.x

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `app.py` | The main application file containing the Streamlit UI and hybrid detection logic. |
| `train_model.py` | Script used to train the machine learning model and save it as a `.pkl` file. |
| `phishing_model.pkl` | The pre-trained Gradient Boosting model used for predictions. |
| `dataset_phishing.csv` | The dataset containing 11,430 legitimate and phishing URLs used for training. |
| `analysis.ipynb` | Jupyter Notebook used for data analysis, feature engineering, and model training. |

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/phishguard.git](https://github.com/yourusername/phishguard.git)
    cd phishguard
    ```

2.  **Install Dependencies**
    Create a `requirements.txt` file (or install manually) with the following libraries:
    ```bash
    pip install streamlit pandas scikit-learn joblib
    ```

3.  **Run the Application**
    Launch the web interface:
    ```bash
    streamlit run app.py
    ```

## 📊 How It Works

1.  **Feature Extraction:** The app parses the input URL to extract numerical features:
    * `length_url`: Total characters in the URL.
    * `nb_dots`: Count of full stops (often used in subdomains).
    * `nb_hyphens`: Count of dashes (common in look-alike domains).
    * `nb_at`: Presence of the `@` symbol (obfuscation technique).
    * `nb_slash`: URL depth / folder count.
    * `https_token`: Usage of HTTPS.
    * `ip`: Checks if the domain is a raw IP address.
2.  **AI Prediction:** The pre-trained **Gradient Boosting** model calculates a base probability score based on these features.
3.  **Heuristic Adjustment:** The system scans for suspicious keywords (e.g., "verify", "wallet"). If found, a risk penalty is added to the base score.
4.  **Final Verdict:**
    * 🟢 **Safe:** Low risk score.
    * 🟠 **Suspicious:** Medium risk score.
    * 🔴 **Phishing:** High risk score.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

---

**Disclaimer:** This tool is for educational and research purposes. Always verify suspicious URLs through multiple channels before interacting with them.