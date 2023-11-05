# Little-Lemon-API-Project
This repository is mini project from APIs Django rest framework Coursera. start this project on October 2023
**Note**: The idea and the scope of the project is from APIs coursera.

# scope
You will create a fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 
The next section will walk you through the required endpoints with an authorization level and other helpful notes. Your task is to create these endpoints by following the instructions.

# structure
You will create one single Django app called LittleLemonAPI and implement all API endpoints in it. Use pipenv to manage the dependencies in the virtual environment.

# User groups
Create the following two user groups and then create some random users and assign them to these groups from the Django admin panel. 
- Manager
- Delivery crew
Users not assigned to a group will be considered customers.

# API Endpoints
Here are all the required API routes for this project grouped into several categories.
User registration and token generation endpoints 
You can use Djoser in your project to automatically create the following endpoints and functionalities for you.
attach the picture

#  Menu-items endpoints
attach the picture

# User group management endpoints
attach the picture

# Cart management endpoints 
attach the picture

# Order management endpoints
attach the picture

# Additional step
Implement proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints.

# Throttling
Finally, apply some throttling for the authenticated users and anonymous or unauthenticated users.







