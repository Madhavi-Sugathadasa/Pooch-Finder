# Pooch Finder :dog: :paw_prints:
Created a web application named Pooch Finder for Connecting pet lovers with responsible dog breeders nationwide using Python (Django), SQLite3, jQuery, HTML, CSS and Bootstrap

---
### **Features:**

1. **_Registration, Login, Logout, forgot password_**

Site users are able to register for the web application with a username, password, first name, last name, and email address. Users are able to log in and log out of the website. If users forgot their passwords, they can reset the password via an email reset password link.

---

2. **_Viewing Ads_**

Once logged in, users are taken to the home page where they are able to see a list of all puppies and dogs for sale (which are Ads placed by other users (or breeders) including Ads placed by the login user itself)

Users are able to **filter the search** criteria by following fields:
```
    State - (select from a dropdown list)
    Location - (select suburb, state and postcode from autocomplete dropdown) and all suburbs within selected no of kms
    Breed -  (select from a dropdown list)
    Gender -  (select from a dropdown list)
    Age -  (select from a dropdown list)
    Price range - slider to select a price range
```
Users are able to **sort the results** by “Most Recent” OR  by “Alphabetical Order” (i.e. sort title by alphabetical order) OR by “Most Expensive” OR by “Cheapest”

Each list item display a summary of Ad details including price, title, summary description, part of full description and an image slider and item location. There is a link to see more details of a selected Ad

**Pagination** is available on this page. Currently displays five Ads per page & it is a configurable parameter.

---

3. **_More Details page_**

Once users click on “More Details” link from a selected Ad, they are able to see additional details about the Ad. Especially they are able to **send messages to the seller** from this page.

---

4. **_Post an Ad_**

Once login, users (dog breeders) are able to post an Ad about puppies or dogs that are for sale.

Following details needed to provide in order to publish an Ad:
```
    Selling price and whether price is negotiable or not
    title of Ad
    summary description
    full description
    gender (select from a dropdown list)
    age (select from a dropdown list)
    breed (select from a dropdown list)
    type (whether pure bred or x-breed, (select from a dropdown list)
    microchip numbers if available
    breeder id if registered
    contact name
    email
    mobile
    item location (select suburb, state and postcode from autocomplete dropdown)
    upload up to 6 images. At leases one image required
```
finally user need to accept terms and condition of posting an Ad.

---

5. **_View & Edit Ads posted by the logged in user_**

There is a link at the top of navigation bar named “My Ads”. Once they click on this link, users are able to see list all active and inactive Ads which are posted by them (active and inactive items are listed in two separate tabs)
Under each Ad there is a “Edit” link where users are able to edit the details of Ads


---


### **Technical Details:**

Developed using **JavaScript**, **Python**, and **SQL**. Used **Django, sqlite3 DB, jQuery and Bootstrap**

Used Django’s in built Authentication and Authorisation  system for user registration, login, logout and forgot password sections.

**8 tables** were used in the sqlite3 DB apart from the Django’s inbuilt user tables.
```
    **_States table_** - Keep a list of all states in Australia
    **_Locations table_** - Keep list of all suburbs in Australia including their postcode, state, longitude and latitude. I was able to find a free csv file online with above details. I wrote a python function to insert data in to the table by reading the csv file
    **_Breeds table_** - Keep a list of all dog breeds
    **_Gender table_** - Keep a list  of all genders
    **_Dog_types table_** - Keep a list  of all dog types (whether pure bred or x-breed)
    **_Age_cats table_** - Keep a list of predefined age categories
    **_Ad_items_** - Keep a list of all Ads posted by users
    **_Pictures_** - photos related to each Ad
```

Following variables were configured for email send functionality
```
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = (this was configured using environment variable )
    EMAIL_HOST_PASSWORD = (this was configured using environment variable )
    DEFAULT_FROM_EMAIL = (this was configured using environment variable )

```
Added following configureable parameters to configure image save path
```
    MEDIA_URL = "/Media/"
    MEDIA_PATH = "Media"
```
Added following configureable parameters to display currency & its symbol
```
    CURRENCY = 'AUD'
    CURRENCY_SYMBOL =‘$'
```
Added following configureable parameters to keep no of Ads per page
```
    NO_OF_ADS_PER_PAGE =5
```
---

**NOTE:**
In order to implement filter functionality for getting the ad items from within a specified distance in kilometres of given location, I had to use sqlite3 math extension to get acos, cos, sin, radians of given longitudes and latitudes. Sqlite3 was built with extension loading disabled. So I had to install sqlite3 via Homebrew and then build Python from scratch with the appropriate sqlite3 library linked.

Following commands were run in order to enable above functionality:
```
    brew install sqlite3
    brew install xz
    brew install openssl
    brew install gdbm
    brew install pyenv
```
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions --enable-optimizations --with-openssl=/usr/bin/openssl" LDFLAGS="-L/usr/local/Cellar/sqlite/3.32.1/lib -L/usr/local/opt/zlib/lib" CPPFLAGS="-I/usr/local/Cellar/sqlite/3.32.1/include -I/usr/local/opt/zlib/include" pyenv install 3.8.2

Reference : https://stackoverflow.com/questions/57977481/how-to-use-enable-load-extension-from-sqlite3

Also I had to download following extension-functions.c file for Sqlite web  (https://www.sqlite.org/contrib/download/extension-functions.c?get=25) and compile it using following command before using it in the python code

gcc -g -fPIC -dynamiclib extension-functions.c -o math


JQuery was used for writing javascript and Bootstrap used for CSS together with css classes written by me.

**All pages were responsive** in a smaller screen and a larger screen.


---
