from django.shortcuts import render
from .models import Movie, FilmCategory, Customer, CustomerSegment
from .forms import CustomerPredictionForm, MovieSearchForm
import os
from django.conf import settings
import json
from django.db.models import Count
import joblib
import numpy as np
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd #baru
from sklearn.cluster import KMeans #baru
from sqlalchemy import create_engine #baru

# Create your views here.
def home(request):
    total_customers = Customer.objects.count()
    total_movies = Movie.objects.count()
    
    # Get segment counts
    segment_counts = list(CustomerSegment.objects.values('segment').annotate(count=Count('customer_id')))
    
    # Initialize counts
    low_count = 0
    medium_count = 0
    high_count = 0
    
    for item in segment_counts:
        segment_name = item['segment'].lower()
        if 'low' in segment_name:
            low_count += item['count']
        elif 'medium' in segment_name:
            medium_count += item['count']
        elif 'high' in segment_name:
            high_count += item['count']
            
    context = {
        'total_customers': total_customers,
        'total_movies': total_movies,
        'low_count': low_count,
        'medium_count': medium_count,
        'high_count': high_count,
    }
    return render(request, 'dvdrental_prediction/home.html', context)

def about(request):
    return render(request, 'dvdrental_prediction/about.html')

def movie_list(request):
     movie = Movie.objects.select_related('language').all() #mengambil semua data dari model Movie
     form = MovieSearchForm() #membuat instance form search
     return render(request, 'dvdrental_prediction/movie_list.html', {
         'movies': movie, 
         'form': form})
 
def movie_detail(request,film_id):
     movie = Movie.objects.get(film_id=film_id) #mengambil data movie berdasarkan film_id
     actors = movie.actors.all() #mengambil semua data aktor yang berelasi dengan movie
     return render(request, 'dvdrental_prediction/movie_detail.html', {'movie': movie, 'actors': actors})
 
def search_result(request):
     form= MovieSearchForm(request.GET) #mengambil data dari form search
     movies= Movie.objects.select_related('language').all() #mengambil semua data dari model Movie
     
     if form.is_valid(): #jika form valid
            actor = form.cleaned_data['actor'] #mengambil data actor dari form
            category = form.cleaned_data['category'] #mengambil data category dari form
            language = form.cleaned_data['language'] #mengambil data language dari form
            
            if actor: #jika actor tidak kosong
                movies = movies.filter(actors=actor) #filter movie berdasarkan actor
            if category: 
                movies = movies.filter(filmcategory__category=category) 
            if language: 
                movies = movies.filter(language=language) 
                
     return render(request, 'dvdrental_prediction/movie_search.html', {
         'movies': movies, 
         'form': form})
     
def customer_prediction_view(request):
    form = CustomerPredictionForm() #membuat instance form prediksi
    return render(request, 'dvdrental_prediction/dashboard.html', {'form': form})           

model_path = os.path.join(settings.BASE_DIR, 'final_customer_model.pkl')
model = joblib.load(model_path)

@csrf_exempt
def predict_customer(request):
    print(f"request method: {request.method}")
    if request.method == 'POST':
        # parse incoming json data
        data = json.loads(request.body)
        print(f"Data received: {data}")

        #prepare feature array (ensure correct features order)
        features = np.array([[
            data["store_id"],
            data["active"],
            data["total_payment"],
            data["payment_count"],
            data["average_payment"]
        ]]).reshape(1, -1)
        
        # make prediction and Calculate probability
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()

        #Return prediction and probability as JSON response
        return JsonResponse({
            'prediction': int(prediction),
            'probability': probability
        })



# CASE BARU
def predict_segment(request):
    result = None

    if request.method == 'POST':
        total_payment = float(request.POST.get('total_payment')or 0) # default ke 0 jika kosong
        frequency = int(request.POST.get('frequency') or 0) # default ke 0 jika kosong 
        
        if not total_payment or not frequency:
            return render(request, 'predict_segment.html', {
        'error': 'All fields are required!'
    })

        total_payment = float(total_payment)
        frequency = float(frequency) 

        # koneksi database
        engine = create_engine("postgresql://postgres:Shoniadu2@localhost:5432/dvdrental")

        # ambil data
        df = pd.read_sql("SELECT total_payment, frequency FROM customer_payment_summary", engine)

        # fitur
        X = df[['total_payment', 'frequency']]

        # training model
        MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'kmeans_model.pkl')
        kmeans = joblib.load(MODEL_PATH)

        # input user
        new_data = [[total_payment, frequency]]
        cluster = kmeans.predict(new_data)[0]

        # 🔥 FIX: mapping berdasarkan nilai centroid
        cluster_centers = kmeans.cluster_centers_

        # urutkan berdasarkan total_payment (kolom ke-0)
        sorted_clusters = sorted(
            [(i, center[0]) for i, center in enumerate(cluster_centers)],
            key=lambda x: x[1]
        )

        # mapping otomatis
        mapping = {
            sorted_clusters[0][0]: 'Low',
            sorted_clusters[1][0]: 'Medium',
            sorted_clusters[2][0]: 'High'
        }

        result = mapping[cluster]

    return render(request, 'dvdrental_prediction/predict_segment.html', {'result': result})