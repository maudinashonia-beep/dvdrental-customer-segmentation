from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.cluster import KMeans
from sqlalchemy import create_engine

class Command(BaseCommand):
    help = 'Customer Payment Segmentation using KMeans'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting clustering process..."))

        # koneksi ke PostgreSQL (ubah sesuai punyamu)
        engine = create_engine("postgresql://postgres:Shoniadu2@localhost:5432/dvdrental")

        # ambil data dari tabel OLAP
        query = "SELECT customer_id, total_payment, frequency FROM customer_payment_summary"
        df = pd.read_sql(query, engine)

        # fitur untuk clustering
        X = df[['total_payment', 'frequency']]

        # KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['cluster'] = kmeans.fit_predict(X)

        # mapping cluster ke label
        def label_cluster(row):
            if row['cluster'] == 0:
                return 'Low'
            elif row['cluster'] == 1:
                return 'Medium'
            else:
                return 'High'

        df['segment'] = df.apply(label_cluster, axis=1)

        # simpan ke database
        df.to_sql('customer_segment', engine, if_exists='replace', index=False)

        self.stdout.write(self.style.SUCCESS("Clustering finished! Table 'customer_segment' created."))