# Crop Price Tracker

   Crop Price Tracker is a Django-based web application that allows users to track real-time and historical commodity prices for crops like wheat, maize, rice, soybeans, sugar, coffee, cotton, barley, and oats. Users can sign up, log in, manage favorite crops in their profile, and view price data with historical charts. The app integrates with the API Ninjas Commodity Price API for live data and uses mock data for historical trends. It is deployed on Heroku at crop-price-tracker-410438b977b9.herokuapp.com.

# Features
  * User Authentication: Sign up, login, and logout with POST-based forms.
  * Crop Price Tracking: View real-time prices for crops via API Ninjas( e.g $10.855 for rice) with fallback to mock data if API files.
  * User Profiles: Authenticated users can add/remove favourite crops stored in the FavouriteCrop model.
  * Deployment: Hosted on Heroku with SQLite locally and Postgres in production.

# Languages, Dependencies & Frameworks utilized.
    * Python
    * Django Framework
    * Database: SQLite(local)
    * API: API Ninjas Commodity Price API
    * Dependencies: django-crispy-forms, crispy-bootstrap5, requests, dj-database-url, whitenoise
    * Deployment: Heroku


# Setup Instructions
## Prerequisites
* Python 3.13
* Git
* API Ninjas key (Sign up at api-ninjas.com)


# Licenses
 * MIT License
    * The presence of this license encourages open source contributions from independent parties.
    * Crop tracker  corrections
