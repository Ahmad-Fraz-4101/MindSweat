from django.http import HttpResponse,HttpResponseRedirect # type: ignore
from django.shortcuts import render # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate, login as login_,logout as logout_ # type: ignore
from django.contrib import messages # type: ignore
from .models import *
from django.db import connection # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore

def home(request):
    return render(request, "index.html")
def bmi(request):
    return render(request, "bmi.html")
def calories(request):
    return render(request, "calories.html")
def login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login_(request, user)
            messages.success(request, 'YOU HAVE BEEN LOGGED IN !')
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "login.html",{
                "message":"Invalid Credentials"
            })
    return render(request, "login.html")
def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    logout_(request)
    messages.success(request, 'YOU HAVE BEEN LOGGED OUT !')
    return HttpResponseRedirect(reverse('home'))

def port(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        idd=1
        user = request.user
        with connection.cursor() as cursor:
            cursor.execute("SELECT Heightfeet FROM fitness_FitUser WHERE username = %s", [user.username])
            r = cursor.fetchone()
            cursor.execute("SELECT Heightinch FROM fitness_FitUser WHERE username = %s", [user.username])
            h = cursor.fetchone()
            cursor.execute("SELECT weight FROM fitness_FitUser WHERE username = %s", [user.username])
            w = cursor.fetchone()
            cursor.execute("SELECT fname FROM fitness_FitUser WHERE username = %s", [user.username])
            fn = cursor.fetchone()
            cursor.execute("SELECT lname FROM fitness_FitUser WHERE username = %s", [user.username])
            ln = cursor.fetchone()
            cursor.execute("SELECT age FROM fitness_FitUser WHERE username = %s", [user.username])
            age = cursor.fetchone()
            cursor.execute("SELECT goal FROM fitness_FitUser WHERE username = %s", [user.username])
            goal = cursor.fetchone()
            cursor.execute("Select contact from fitness_trainer where id =%s",[idd])
            tr=cursor.fetchone()

            k = int(r[0])
            i = int(h[0])
            weight = float(w[0])
            height = (k * 30.48) + (i * 2.54)

            diet_id = None
            workout_id = None

            # Determine diet and workout based on weight and height conditions
            if 50 <= weight <= 60 and 60 <= height <= 70:
                diet_id = 2
                workout_id = 2
            elif 60 < weight < 70 and 50 <= height <= 65:
                diet_id = 2
                workout_id = 2
            elif 70 < weight < 80 and 65 <= height <= 70:
                diet_id = 1
                workout_id = 1
            elif 80 <= weight <= 90 and 60 <= height <= 70:
                diet_id = 3
                workout_id = 2
            elif 90 <= weight <= 100 and 75 <= height <= 80:
                diet_id = 3
                workout_id = 2
            else:
                diet_id = 3
                workout_id = 3

            # Fetch the diet and workout based on the determined IDs
            diet = None
            workout = None
            try:
                cursor.execute("SELECT description FROM fitness_diet WHERE id = %s", [diet_id])
                row = cursor.fetchone()
                # Process the fetched diet data
                diet = {
                    'description': row[0],
                    # Add more fields as needed
                }
            except:
                pass

            try:
                cursor.execute("SELECT description FROM fitness_workout WHERE id = %s", [workout_id])
                row = cursor.fetchone()
                print(row[0])
                # Process the fetched workout data
                workout = {
                    'description': row[0],
                    # Add more fields as needed
                }
            except:
                pass

            height_m = height / 100

    # Calculate BMI
            bmi = round(weight / (height_m ** 2), 2)
 

            fituser = {
                "fname": fn[0],
                "lname": ln[0],
                "height": height,
                "weight": weight,
                "age": age[0],
                "goal": goal[0],
                "bmi":bmi
            }

            trainer={
                "tr_contact":tr[0]
            }
            print(11111)
            print(tr[0])
            return render(request, "port.html", {
                "fituser": fituser,
                "diet": diet,
                "workout": workout,
                "trainer":trainer
            })


def shop(request):
    if request.user.is_authenticated:
        cart_user = request.user
    else:
        try:
            temp_key = request.session['temporary_id']
            _username = "Anonymous" + temp_key
            cart_user = User.objects.get(username=_username)  
        except:
            if not request.session.session_key:
                request.session.create()
            request.session['temporary_id'] = request.session.session_key
            request.session['account'] = 0
            temp_key = request.session.session_key
            _username = "Anonymous" + temp_key
            password = "Anonymous" + temp_key
            user = User.objects.create(username=_username)
            user.set_password(password)
            user.save()
            request.session['account'] = 1
            cart_user = user

    list_cart = []
    if cart_user:
        print(9999)
        print(1)
        print(cart_user)
        
        with connection.cursor() as cursor:
            # Execute the raw SQL query to get cart items for the user with status 0
            cursor.execute(" SELECT * FROM fitness_Cart WHERE usern = %s  ", ['cart_user'])
            cart_items = cursor.fetchall()

        # Print fetched cart items for debugging
        print(cart_items)
        
        if cart_items:
            cart_product_id = [item[3] for item in cart_items]  # Assuming productname is the 4th column in the result
            with connection.cursor() as cursor:
                for product_id in cart_product_id:
                    cursor.execute("SELECT * FROM fitness_Shop_Item WHERE id = %s", [product_id])
                    rows = cursor.fetchall()
                    for row in rows:
                        id, name, quantity, price, description, imr_src = row
                        shop_item = Shop_Item(id=id, name=name, quantity=quantity, price=price, description=description, imr_src=imr_src)
                        # Append the Shop_Item instance to the list
                        list_cart.append(shop_item)
    else:
        list_cart = []

    return render(request, "shop.html", {
        "item": Shop_Item.objects.all(),
        "cart": list_cart
    })



@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')  # Getting the address from the request
        if request.user.is_authenticated:
            buyer = request.user
        else:
            temp_key = request.session['temporary_id']
            if request.session['account'] == 0:
                username = "Anonymous" + temp_key
                password = "Anonymous" + temp_key
                user = User.objects.create(username=username)
                user.set_password(password)
                user.save()
                request.session['account'] = 1
                buyer = user
            else:
                _username = "Anonymous" + temp_key
                buyer = User.objects.get(username=_username)
        
        # Updating cart items status
        print(76)
        print(buyer)
        #carts = Cart.objects.filter(user=buyer)
        with connection.cursor() as cursor:
            # Execute the raw SQL query to get cart items for the user with status 0
            cursor.execute(" SELECT * FROM fitness_Cart WHERE usern = %s  ", ['buyer'])
            carts = cursor.fetchall()

        for item in carts:
            item.status = 1
            item.save()
        
        # Creating or updating user address
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM fitness_address WHERE user_id = %s", [buyer.id])
            address_id = cursor.fetchone()
            print(address_id)
            if address_id:
                # Update existing address
                cursor.execute("UPDATE fitness_address SET address = %s WHERE id = %s", [address, address_id[0]])
            else:
                # Create new address
                cursor.execute("INSERT INTO fitness_address (user_id, address) VALUES (%s, %s)", [buyer.id, address])

        return HttpResponse("Success!")
    
    return HttpResponse("Failed!")

@csrf_exempt
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            buyer = request.user
        else:
            temp_key=request.session['temporary_id']
            _username = "Anonymous" + temp_key
            buyer = User.objects.get(username=_username)
        product_id = request.POST.get('product_id')  # Getting the product id from the request
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, quantity FROM fitness_Shop_Item WHERE id = %s", [product_id])
            result = cursor.fetchone()
            if result:
                name=result[0]
                p_quantity=result[1]
                #name, p_quantity = result
                print(name,p_quantity)
                print(product_id)
                p_quantity = int(p_quantity) - 1
                cursor.execute("UPDATE fitness_Shop_Item SET quantity = %s WHERE id = %s", [p_quantity, product_id])
                with connection.cursor() as cc:
                     print(87)
                     print(buyer.id)
                     cc.execute("Select username from fitness_FitUser where id_id=%s",[buyer.id])
                     f=cc.fetchall()
                     print(f[0][0])
                     cc.execute("INSERT INTO fitness_Cart (user_id,usern, productname, quantity, status) VALUES (%s,%s, %s, %s, %s)", [buyer.id,f[0][0], product_id, 1, 0])
                     

                return HttpResponse("Success!")  # Sending a success response
            else:
                return HttpResponse("Failed!")  # Sending a failure response
    return HttpResponse("Failed!")  # Sending a failure response
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        fname=request.POST["firstname"]
        lname=request.POST["lastname"]
        Age=request.POST["age"]
        heightinch=request.POST["heightinch"]
        heightfeet=request.POST["heightfeet"]
        Weight=request.POST["weight"]
        Goal=request.POST["goal"]

        if User.objects.filter(username = username).first():
            message="This username is already taken"
            return render(request, "signup.html",{
                message:message
                })
        user=User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        
        FitUser.objects.create(id=user,username=username,fname=fname,lname=lname,goal=Goal,age=Age,heightfeet=heightfeet,heightinch=heightinch,weight=Weight)
        return render(request, "login.html",{
            "message":"Account Created Successfully"
        })
    return render(request, "signup.html")

def training(request):
     if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
     else:
        return render(request, "training.html")
def video(request):
    return render(request, "video.html")

def feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback', '')
        if feedback_text:
            user_id = request.user.id
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO fitness_feedback (user_id, feedback) VALUES (%s, %s)", [user_id, feedback_text])
            print(feedback_text)
            return HttpResponseRedirect(reverse("feedback"))
    return render(request, "feedback.html",{
        "feedback": Feedback.objects.all()
    })

