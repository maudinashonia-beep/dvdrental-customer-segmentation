from django.db import models

# Create your models here.

class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'category'
        managed = False
        
    def __str__(self):
        return self.name
    
class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    first_name =models.CharField(max_length=45)    
    last_name =models.CharField(max_length=45)  
    
    class Meta:
        db_table = 'actor'
        managed = False
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'language'
        managed = False
        
    def __str__(self):
        return self.name

class Movie(models.Model):
    film_id = models.IntegerField (primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=5)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, db_column='language_id')
    actors = models.ManyToManyField(Actor, through='FilmActor')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'film' # film table in dvdrental db
        managed = False # Important or Django will auto create/alter existing table
        

class FilmActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, db_column='actor_id')
    film = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='film_id')
    
    class Meta:
        db_table = 'film_actor'
        unique_together = ('film', 'actor')
        managed = False
        
class FilmCategory(models.Model):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='film_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    
    class Meta:
        db_table = 'film_category'
        unique_together = ('film', 'category')
        managed = False      

class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField()
    address_id = models.IntegerField()
    active = models.BooleanField()
    create_date = models.DateTimeField()
    
    class Meta:
        db_table = 'customer'
        managed = False

class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, db_column= 'customer_id')
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField()
        
    class Meta:
        db_table = 'payment'
        managed = False
        
class ModelInfo(models.Model):
    model_name = models.CharField(max_length=100)
    model_file = models.CharField(max_length=255)
    training_data = models.CharField(max_length=255)
    training_date = models.DateTimeField()
    model_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.model_name} - {self.training_date.strftime('%Y-%m-%d')}"
    
    #customer segment model
   
    
    
# Case baru

class CustomerSegment(models.Model):
    customer_id = models.IntegerField(primary_key=True)  # 🔥 INI PENTING

    total_payment = models.FloatField()
    frequency = models.IntegerField()
    cluster = models.IntegerField()
    segment = models.CharField(max_length=50)

    class Meta:
        db_table = 'customer_segment'
    
    