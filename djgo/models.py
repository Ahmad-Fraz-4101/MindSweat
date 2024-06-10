from django.db import models # type: ignore
from django.core.validators import MinLengthValidator, MinValueValidator # type: ignore
from django.contrib.auth.models import User # type: ignore


# Model for the item table
class Shop_Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(default="")
    imr_src = models.CharField(max_length=1000,default="")
    def __str__(self):
        return f"{self.name} {str(self.quantity)}"

class trainer(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.CharField(max_length=11)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usern=models.CharField(max_length=30)
    productname = models.CharField(max_length=30)  # Change product to productname
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False)  # Use BooleanField instead of IntegerField for boolean values
    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Address = models.TextField(default="")
    def __str__(self):
        return f"{self.user.username} {self.Address}"
    
# Model for the fit_user table
class FitUser(models.Model):
    id = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,related_name='user_info')   
    username=models.CharField(max_length=30,default="abc")
    fname = models.CharField(max_length=20,default="John")
    lname = models.CharField(max_length=20,default="Doe")
    goal= models.TextField(max_length=15,null=False)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=False)
    heightfeet = models.IntegerField(validators=[MinValueValidator(2)], null=False)
    heightinch= models.IntegerField(validators=[MinValueValidator(0)], null=False)
    weight = models.FloatField(validators=[MinValueValidator(0.1)], null=False)
    #trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, null=True)

# # Model for the fit_user_login table
# class LoginInfo(models.Model):
#     email = models.EmailField(max_length=50, primary_key=True)
#     password = models.CharField(max_length=100, validators=[MinLengthValidator(8)], null=False)
#     profile = models.ForeignKey(FitUser, on_delete=models.CASCADE)


 # Model for the workout table
class Workout(models.Model):
     id = models.AutoField(primary_key=True)
     description = models.TextField()

# # Model for the diet table
class Diet(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
# # Model for the fit_plan table
# class FitPlan(models.Model):
#     id = models.AutoField(primary_key=True)
#     workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
#     diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
#     fit_user = models.ForeignKey(FitUser, on_delete=models.CASCADE)

# # Model for the Feedback table
class Feedback(models.Model):
    user = models.ForeignKey(FitUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    def __str__(self):
        return self.feedback


    
# # Model for the customer table
# class Customer(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30)
#     phone = models.CharField(max_length=12)

# # Model for the trainer table
# class Trainer(models.Model):
#     id = models.AutoField(primary_key=True)
#     phone = models.CharField(max_length=12)

#Model for the order_details table
# class OrderDetails(models.Model):
#     id = models.AutoField(primary_key=True)
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='OrderReference')
#     customer_address = models.TextField()
#     item = models.ForeignKey(Shop_Item, on_delete=models.CASCADE)

