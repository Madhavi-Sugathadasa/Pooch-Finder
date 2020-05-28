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
