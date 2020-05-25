from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.db import IntegrityError
from .models import Breed, Dog_Type, Age_Cat, Gender, Picture, Location, Ad_Item, State
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings as conf_settings
import os
import sqlite3
from datetime import datetime
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator


# Create your views here.

#login page
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username:
            return render(request, "users/login.html", {"message": "Must provide username."})
        if not password:
            return render(request, "users/login.html", {"message": "Must provide password."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        request.session.clear()
        return render(request, "users/login.html", {"message": None})
    
#register a new user   
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        if not username:
            return render(request, "users/register.html", {"message": "Must provide username."})
        if not password:
            return render(request, "users/register.html", {"message": "Must provide password."})
        if password != confirm_password:
            return render(request, "users/register.html", {"message": "Passwords didn't match."})
        if not first_name:
            return render(request, "users/register.html", {"message": "Must provide first name."})
        if not last_name:
            return render(request, "users/register.html", {"message": "Must provide last name."})
        if not email:
            return render(request, "users/register.html", {"message": "Must provide email."})

        try:
            User.objects.create_user(username=username, password=password,  first_name=first_name, last_name=last_name, email=email)
        except IntegrityError:
            return render(request, "users/register.html", {"message": "User already exists."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/register.html", {"message":None})
    

# logout view
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": None})


# forgot password, recover through an email
def forgot_password(request):
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'users/forgot_password.html')

#index page
@login_required(login_url='login')
def index(request):
    try:
        ad_items = None
        context = {}
        # if user filter results
        if request.method == "POST":
            state = request.POST["state"]
            # filter by state
            if state and state != "ALL":
                ad_items = Ad_Item.objects.filter(active = True, item_location__state = state)
                context.update(state_val = state )
            else:
                ad_items = Ad_Item.objects.filter(active = True)
            
            # filter by location and within given kms of distance
            # for this functionality had to use sql math functions extention
            location_str = request.POST["location"]
            if location_str:
                location_data  = location_str.split(", ")
                if len(location_data) == 3:
                    location= Location.objects.get(Q(postcode=location_data[2]) & Q(suburb=location_data[0]) & Q(state=location_data[1]))
                    if location:
                        context.update(location = location )
                        
                        distance = request.POST["distance"]
                        context.update(distance = int(distance) )
                        
                        conn = sqlite3.connect(os.path.join(conf_settings.BASE_DIR, 'db.sqlite3'))
                        conn.enable_load_extension(True)
                        conn.load_extension("./math")
                        c = conn.cursor()
                        c.execute('Select id From pooch_finder_location Where acos(sin(radians(?))*sin(radians(lat)) + cos(radians(?))*cos(radians(lat))*cos(radians(lon)- radians(?))) * 6371 < ? and lat != 0.0 and lon !=0.0', (location.lat, location.lat, location.lon, int(distance)))
                        
                        rows = c.fetchall()
                        surrounding_subs = [i[0] for i in rows]
                        conn.enable_load_extension(False)
                        conn.close()
                        ad_items = ad_items.filter(item_location__id__in = surrounding_subs)
                        
            # filter by price range
            price_range = request.POST["price_range"]
            if price_range:
                ad_items = ad_items.filter(price__lte = float(price_range))
                context.update(price_range = price_range )
            # filter by age    
            age = request.POST["age"]
            if age and age != "ALL":
                ad_items = ad_items.filter(age__id = age)
                context.update(age_val = age )
            # filter by breed    
            breed = request.POST["breed"]
            if breed and breed != "ALL":
                ad_items = ad_items.filter(breed__id = breed)
                context.update(breed_val = breed )
            # filter by gender
            gender = request.POST["gender"]
            if gender and gender != "ALL":
                ad_items = ad_items.filter(gender__id = gender)
                context.update(gender_val = gender)
            
            # sort by most recent(MR) or Alphabetical order(AO) or Most Expensive(ME) or Cheapest(C)
            sort = request.POST["sort"]
            if sort:
                context.update(sort_val = sort )
                if sort == "MR":
                    ad_items = ad_items.order_by('-date_time')
                if sort == "AO":
                    ad_items = ad_items.order_by('title')
                if sort == "ME":
                    ad_items = ad_items.order_by('-price')
                if sort == "C":
                    ad_items = ad_items.order_by('price')
                
                
        else:
            # get all active ads
            ad_items = Ad_Item.objects.filter(active = True)
        
        # pagination
        paginator = Paginator(ad_items, conf_settings.NO_OF_ADS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        dict_photo_items ={}
        
        for ad_item in page_obj:
            # laod photos for each ad item
            photo_items = Picture.objects.filter(ad_item =ad_item)
            if photo_items:
                dict_photo_items[ad_item.id] = photo_items
    except Ad_Item.DoesNotExist:
        return render(request, "error.html", {"message": "Ad items does not exist."})
    except Picture.DoesNotExist:
        return render(request, "error.html", {"message": "photo items does not exist."})
    
    # load all below details to populate filter section
    states = State.objects.all().order_by('name')
    breeds = Breed.objects.all().order_by('name')
    genders = Gender.objects.all()
    ages = Age_Cat.objects.all()
    
    context.update({'page_obj': page_obj, "photo_items":dict_photo_items, "states":states,"breeds":breeds,"genders":genders,"ages":ages,})
    
    return render(request, "index.html", context)


# more details of a selected Ad
@login_required(login_url='login')
def ad_more_details(request, ad_id):
    
    try:
        item = Ad_Item.objects.get(pk=ad_id)
        photo_items = Picture.objects.filter(ad_item =item)
    except Ad_Item.DoesNotExist:
        return render(request, "error.html", {"message": "item does not exist."})
    except Picture.DoesNotExist:
        return render(request, "error.html", {"message": "photo items does not exist."})
    context = {
      "item": item,"photo_items":photo_items, 
    }
    return render(request, "item.html", context)

# ajax call for location autocomplete
def autocomplete_location(request):
    if request.is_ajax():
        location = request.GET.get('search', None)
        queryset = Location.objects.filter(Q(postcode__contains=location) | Q(suburb__contains=location) | Q(state__contains=location))
        list = []        
        for i in queryset:
            list.append(i.suburb+", " + i.state + ", " + i.postcode)
        data = {
            'list': list,
        }
        return JsonResponse(data)

    
# post a new Ad    
@login_required(login_url='login')
def post_ad(request):
    if request.method == "POST":
        try:
            ad_item = Ad_Item()
            ad_item.user = request.user
            price = request.POST["price"]
            ad_item.price = float(price)
            negotiable = request.POST.get("negotiable",None)
            if negotiable:
                ad_item.negotiable = True
            title = request.POST["title"]
            ad_item.title = title
            summary_desc = request.POST["summary"]
            ad_item.summary_desc = summary_desc
            desc = request.POST["description"]
            ad_item.desc = desc
            
            gender = request.POST["gender"]
            ad_item.gender = Gender.objects.get(pk=gender)
            
            age = request.POST["age"]
            ad_item.age = Age_Cat.objects.get(pk=age)
            
            breed = request.POST["breed"]
            ad_item.breed = Breed.objects.get(pk=breed)
            
            dog_type  = request.POST["dog_type"]
            ad_item.dog_type = Dog_Type.objects.get(pk=dog_type)
            
            microchip_number = request.POST["microchip_number"]
            ad_item.microchip_number = microchip_number
            
            breeder_id = request.POST["breeder_id"]
            ad_item.breeder_id = breeder_id
            
            contact_name = request.POST["contact_name"]
            ad_item.contact_name = contact_name
            
            contact_email = request.POST["contact_email"]
            ad_item.email = contact_email
            
            mobile = request.POST["mobile"]
            ad_item.mobile = mobile
            
            location_str = request.POST["location"]
            if location_str:
                location_data  = location_str.split(", ")
                if len(location_data) == 3:
                    location = Location.objects.get(Q(postcode=location_data[2]) & Q(suburb=location_data[0]) & Q(state=location_data[1]))
                    if location:
                        ad_item.item_location = location
                    else:
                        return render(request, "error.html", {"message": "Invalid item location."})
                else:
                    return render(request, "error.html", {"message": "Invalid item location."})
            else:
                return render(request, "error.html", {"message": "Invalid item location."})
            
            ad_item.date_time = datetime.now()
            ad_item.active = True
            ad_item.save()
            
            for i in range(1,6):
                img = request.FILES.get('img_' + str(i))
                if img:
                    picture = Picture()
                    picture.ad_item = ad_item
                    picture.image = img
                    picture.save()
            return HttpResponseRedirect(reverse("index"))
            
        except Gender.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid gender type."})
        except Age_Cat.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid age category."})
        except Breed.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid breed category."})
        except Dog_Type.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid dog category."})
        except Location.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid item location."})
        
    else:
        
        breeds = Breed.objects.all().order_by('name')
        genders = Gender.objects.all()
        ages = Age_Cat.objects.all()
        types = Dog_Type.objects.all()
        context ={"breeds":breeds, "genders":genders, "ages":ages, "types":types, }
        return render(request, "post_ad.html", context)
    
    
# view Ads posted by login user
@login_required(login_url='login')
def view_my_ads(request):
    status = request.GET.get('status','')
    ad_items = None
    
    if status and status == 'active':
        ad_items = Ad_Item.objects.filter(user = request.user, active = True)
    elif status and status == 'inactive':
        ad_items = Ad_Item.objects.filter(user = request.user, active = False)
    else:
        status = 'active'
        ad_items = Ad_Item.objects.filter(user = request.user, active = True)
    dict_photo_items ={}

    for ad_item in ad_items:
    
        photo_items = Picture.objects.filter(ad_item =ad_item)
        if photo_items:
            dict_photo_items[ad_item.id] = photo_items
    context ={"ad_items":ad_items, "photo_items":dict_photo_items,"status":status,}
    return render(request, "my_ads.html", context)



# edit details of already posted Ad
@login_required(login_url='login')
def edit_ad(request, ad_id):
    ad_item = None
    try:
        ad_item = Ad_Item.objects.get(user = request.user, pk = ad_id )
        if not ad_item:
            return render(request, "error.html", {"message": "You are not authorised to update this item"})
    except Ad_Item.DoesNotExist:
            return render(request, "error.html", {"message": "You are not authorised to update this item"})

    if request.method == "POST":
        try:
            ad_item.user = request.user
            price = request.POST["price"]
            ad_item.price = float(price)
            negotiable = request.POST.get("negotiable",None)
            if negotiable:
                ad_item.negotiable = True
            title = request.POST["title"]
            ad_item.title = title
            summary_desc = request.POST["summary"]
            ad_item.summary_desc = summary_desc
            desc = request.POST["description"]
            ad_item.desc = desc

            gender = request.POST["gender"]
            ad_item.gender = Gender.objects.get(pk=gender)

            age = request.POST["age"]
            ad_item.age = Age_Cat.objects.get(pk=age)

            breed = request.POST["breed"]
            ad_item.breed = Breed.objects.get(pk=breed)

            dog_type  = request.POST["dog_type"]
            ad_item.dog_type = Dog_Type.objects.get(pk=dog_type)

            microchip_number = request.POST["microchip_number"]
            ad_item.microchip_number = microchip_number

            breeder_id = request.POST["breeder_id"]
            ad_item.breeder_id = breeder_id

            contact_name = request.POST["contact_name"]
            ad_item.contact_name = contact_name

            contact_email = request.POST["contact_email"]
            ad_item.email = contact_email

            mobile = request.POST["mobile"]
            ad_item.mobile = mobile

            location_str = request.POST["location"]
            if location_str:
                location_data  = location_str.split(", ")
                if len(location_data) == 3:
                    location = Location.objects.get(Q(postcode=location_data[2]) & Q(suburb=location_data[0]) & Q(state=location_data[1]))
                    if location:
                        ad_item.item_location = location
                    else:
                        return render(request, "error.html", {"message": "Invalid item location."})
                else:
                    return render(request, "error.html", {"message": "Invalid item location."})
            else:
                return render(request, "error.html", {"message": "Invalid item location."})

            ad_item.date_time = datetime.now()
            
            active = request.POST.get("active",None)
            if active:
                ad_item.active = True
            else:
                ad_item.active = False
            ad_item.save()

            for i in range(1,7):
                img = request.FILES.get('img_' + str(i))
                if img:
                    picture = Picture()
                    picture.ad_item = ad_item
                    picture.image = img
                    picture.save()
            return HttpResponseRedirect(reverse("index"))

        except Gender.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid gender type."})
        except Age_Cat.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid age category."})
        except Breed.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid breed category."})
        except Dog_Type.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid dog category."})
        except Location.DoesNotExist:
            return render(request, "error.html", {"message": "Invalid item location."})

    else:
        pictures = Picture.objects.filter(ad_item = ad_item).order_by('id')
        breeds = Breed.objects.all().order_by('name')
        genders = Gender.objects.all()
        ages = Age_Cat.objects.all()
        types = Dog_Type.objects.all()
        if pictures:
            loop_times = range(len(pictures)+1,7)
        else:
            loop_times = range(1,7)
        context ={"breeds":breeds, "genders":genders, "ages":ages, "types":types, "ad_item":ad_item,"pictures":pictures,"loop_times":loop_times}
        return render(request, "edit_ad.html", context)
  