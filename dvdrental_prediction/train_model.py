import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import joblib

# koneksi database
engine = create_engine("postgresql://postgres:Shoniadu2@localhost:5432/dvdrental")

# ambil data
df = pd.read_sql("SELECT total_payment, frequency FROM customer_payment_summary", engine)

# fitur
X = df[['total_payment', 'frequency']]

# training model
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# simpan model
joblib.dump(kmeans, 'kmeans_model.pkl')

print("✅ Model berhasil disimpan!")