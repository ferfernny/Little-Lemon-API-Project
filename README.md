# Little-Lemon-API-Project
This repository is mini project from APIs Django rest framework Coursera. start this project on October 2023

**Note**: The idea and the scope of the project is from APIs coursera.

# scope
You will create a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 
The next section will walk you through the required endpoints with an authorization level and other helpful notes. Your task is to create these endpoints by following the instructions.

# structure
You will create one single Django app called LittleLemonAPI and implement all API endpoints in it. Use pipenv to manage the dependencies in the virtual environment.

# The process to install and run server
1. Clone a repository
   
![image](https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/ca239fbc-012c-47b4-8825-fa7ab44b83c6)


2. run server on the local
  - run in python terminal

![image](https://github.com/ferfernny/Playtorium-take-home/assets/86872329/5b18c2a0-e14f-4eb5-ad14-e953b5e19852)

# Explore Web broswer in conclusion
   - http://127.0.0.1:8000/api/

![image](https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/9f668137-ec02-4c20-a095-0050ea18b52e)

# User groups
Create the following two user groups and then create some random users and assign them to these groups from the Django admin panel. 
- Manager
- Delivery crew
- Users not assigned to a group will be considered customers.

# API Endpoints
Here are all the required API routes for this project grouped into several categories.
User registration and token generation endpoints 
You can use Djoser in your project to automatically create the following endpoints and functionalities for you.

<img width="607" alt="Screenshot 2023-11-06 120425" src="https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/e42fd5c2-563c-4bc3-be3d-3145221eca5d">


you can see all of the created endpoint accoridng to the links below.
   - http://127.0.0.1:8000/api/users/
   - http://127.0.0.1:8000/api/users/me/
   - http://127.0.0.1:8000/token/login/

#  Menu-items endpoints
<img width="410" alt="image" src="https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/45a601f7-adff-4764-9276-55d3f51ffd4d">

   you can see all of the created endpoint accoridng to the links below.
   - http://127.0.0.1:8000/api/menu-items
   - http://127.0.0.1:8000/api/menu-items/1 (The id of the menu-items can be changed to 1,2,3,4... according to the menu id you want to look in single view)
# User group management endpoints
<img width="461" alt="image" src="https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/1e19c760-f414-4106-ba2b-1caa38d13d91">

   you can see all of the created endpoint accoridng to the links below.
   - http://127.0.0.1:8000/api/groups/delivery-crew/users
   - http://127.0.0.1:8000/api/groups/delivery-crew/users/2 ( the user id can be changed to 1,2,3,4,... according to the user-id you want to look in single view)
# Cart management endpoints 
<img width="603" alt="image" src="https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/96453334-df8a-4912-93e0-e55cdbb826dd">

   you can see all of the created endpoint accoridng to the links below.
   - http://127.0.0.1:8000/api/cart/menu-items

# Order management endpoints
<img width="407" alt="image" src="https://github.com/ferfernny/Little-Lemon-API-Project/assets/86872329/7c892052-af1e-4fa7-ac23-03d05bf57582">

   you can see all of the created endpoint accoridng to the links below.
   - http://127.0.0.1:8000/api/orders
   - http://127.0.0.1:8000/api/orders/1 ( the order id can be changed to 1,2,3,4,... according to the order-id you want to look in single view)

# Additional step
Implement proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints.

# Throttling
Finally, apply some throttling for the authenticated users and anonymous or unauthenticated users.

# How to login and logout by not using token
   - this link can login by username and password.
   - http://127.0.0.1:8000/accounts/login/
   - after login It will appear Page not found (404), but it already login.
   - you can log out from your username by this link http://127.0.0.1:8000/accounts/logout/
