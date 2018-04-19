# Item Catalog Web Application
A Python web application for managing a catolog of items.<br/>

 
## Features
- Third party authentication and authorization with Google or Facebook, using OAuth.
- Anonymous users are allowed to view the web site.
- Authenticated users can create categories and items.
- Authenticated users can edit and delete their own content.
- Item images can be uploaded and displayed in the site.
- JSON endpoint for retrieving all items in the catalog.


## What you need
The application is written in Python 2.7 and uses a SQLite database.<br/>
The web application is built with the Flask framework
You can download dependencies from the requirements.txt file using sudo pip install -r requirements.

## Installation
To get the files copy the content of the zip file into the catalog folder


###Database Setup
- python database_setup.py
- python create_sample_data.py


###Browsing the web site
- python run.py
- Then, you can browse to the web site at **http://localhost:8000**.

###Adding Content
You will need to login with your Facebook or Google credentials
 in order to add categories or items to the catalog.
 You can only edit or delete content that you have added.

###API
The application provides a JSON endpoint at http://localhost:8000/catalog/json
to retrieve all the items in the catalog.

