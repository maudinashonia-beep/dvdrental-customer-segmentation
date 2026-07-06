# DVD Rental Customer Analytics & Predictive Dashboard

A modern, responsive, and data-driven customer analytics portal built on top of the classic PostgreSQL `dvdrental` database. This application integrates Machine Learning algorithms to segment customers and predict customer retention status.

## 🚀 Key Features

* **Executive Analytics Dashboard (`/`):** An intuitive dashboard providing high-level operational statistics (total customers, catalog size, active ML models) with interactive data visualization using **Chart.js**.
* **Customer Spending Segmentation (`/predict-segment/`):** Unsupervised Machine Learning (**K-Means Clustering**) that automatically groups customers into spending tiers (*Low*, *Medium*, *VIP/High*) based on transaction totals and rental frequencies.
* **Customer Status Predictor (`/predict_view/`):** Supervised Machine Learning (**Random Forest Classifier**) that classifies customers into *High-Value (Class 1)* vs *Standard (Class 0)* status based on multi-dimensional transaction history.
* **Dynamic Movie Catalog (`/movies/`):** A robust catalog interface allowing search and filtering by category, language, and actor, connected directly to a live PostgreSQL relational database.
* **Modern UI & Navigation:** Implemented a unified, sticky sidebar navigation layout styled with **Lucide Icons** and dynamic active link indicators.

## 🛠️ Technology Stack

* **Backend Framework:** Django (Python)
* **Database:** PostgreSQL (Relational Database)
* **Machine Learning:** Scikit-Learn (K-Means & Random Forest), Pandas, NumPy, Joblib
* **Data Visualization:** Chart.js (Interactive JS Charts)
* **Iconography:** Lucide Icons
* **Styling:** Premium Vanilla CSS (Responsive & Modern Layout)

## 📋 Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/maudinashonia-beep/dvdrental-customer-segmentation.git
   cd dvdrental-customer-segmentation
   ```
2. **Install Dependencies:**
   Make sure you have your virtual environment active, then install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Database Settings:**
   Ensure your PostgreSQL instance is running and has the `dvdrental` database loaded. Update the database connection credentials in `dvdrental_project/settings.py` and `dvdrental_prediction/views.py`.
4. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.
