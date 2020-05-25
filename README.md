# Final Project

Web Programming with Python and JavaScript

This is a simple project that is a clone of twitter, that has the following features:

1. user register
2. user login
3. user logout
4. user can post a "piew" (a simple text with at maximum 200 characters about any subject)
5. user can see users' piews
6. user can like piews
7. user can see its own profile
8. user can see other users profile
9. user can like piews
10. user can delete its own piews
11. user can delete its own comments
13. user can see who liked the piew
14. user can see how many likes the piew's got
15. user can search for other users
16. user can follow a user to see their piews in the index page
17. user can unfollow a user
18. user can upload an image with their piew
19. user can change it's own avatar picture

## core\admin.py
    this  file adds the models to the admin ui that django provides

## core\foms.py
    this file contains the forms for user and avatar creation

## core\models.py
    this file contains the models that are going to be migrated to the database

## core\views.py
    this file contains all the backend data treatement for every single route and also renders the templates

## core\urls.py
    this file contains all app urls linked to a view form views.py for backend treatment

## core\templates\core
    contains al the html files to be rendered by the browser

## core\static\
    contains styling sheets and images to help styling the project

## media\avatar
    contains the uploaded avatar pictures

## media\photos
    contains the uploaded images from piews
