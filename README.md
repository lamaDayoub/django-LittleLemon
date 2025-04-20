"""

---

# **Restaurant API**

## **Description**
The Restaurant API is a Django-based backend application designed to manage a restaurant's operations. It supports three types of users: **Manager**, **Delivery Crew**, and **Customer**. Each user type has specific roles and permissions:

- **Manager**:
  - Add, edit, and delete menu items.
  - View all users, orders, and delivery crew members.
  - Assign orders to  a delivery .
  - Update the delivery of orders .
- **Customer**:
  - View the menu and categories.
  - Add items to their cart and place orders.
  - View their order history and search for menu items by name or category.
- **Delivery Crew**:
  - View and update the status of assigned orders.

This API uses session-based authentication, and users are activated immediately after signing up. The API is fully documented using Swagger for easy testing and integration.

The frontend for this project (built with Flutter) can be found here: [Master Chef Flutter-Django](https://github.com/HadiAlhamed/Master-chef-flutter-django).

---

## **Features**
- **User Authentication**:
  - Users can sign up, log in, and log out.
  - Session-based authentication ensures secure access.
- **Menu Management**:
  - Managers can add, edit, and delete menu items.
  - Customers can view the menu, filter items by category, and search by name.
- **Cart and Orders**:
  - Customers can add items to their cart and place orders.
  - After placing an order, the cart is cleared.
- **Order Management**:
  - Managers can assign orders to delivery crew members.
  - Delivery crew members can update the status of orders (e.g., mark as delivered).
- **Role-Based Access**:
  - Different user types have distinct permissions based on their roles.
- **Search and Filtering**:
  - Customers can search for menu items by name or filter them by category.
  - Menu items can be ordered by price.

---

## **Technologies Used**
- **Backend Framework**: Django
- **Database**: SQLite3
- **Authentication**: Session-based authentication
- **API Documentation**: Swagger
- **Frontend**: Flutter (available at [this link](https://github.com/HadiAlhamed/Master-chef-flutter-django))

---

## **Installation and Setup**

### **Prerequisites**
- Python 3.12
- Pipenv (Install it globally if not already installed: `pip install pipenv`)

### **Steps**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lamaDayoub/django-LittleLemon
   cd LittleLemon
   ```

2. **Install Dependencies with Pipenv**:
   Use Pipenv to create a virtual environment and install all dependencies:
   ```bash
   pipenv install django
   ```

3. **Activate the Virtual Environment**:
   Activate the virtual environment created by Pipenv:
   ```bash
   pipenv shell
   ```

4. **Run Migrations**:
   Apply database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**:
   To access the admin panel, create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   Run the Django development server:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

---

## **API Documentation**
All API endpoints are documented using Swagger. To explore the API:
1. Start the development server:
   ```bash
   python manage.py runserver
   ```
2. Navigate to the Swagger interface at:
   ```
   http://127.0.0.1:8000/swagger/
   ```
3. Use the interactive interface to test endpoints and view detailed documentation.

---

## **Key Functionalities**
### **Authentication**
- **Sign Up**: Register a new user. The user will be active immediately after signing up.
- **Log In**: Log in a user and start a session.
- **Log Out**: End the current user session.

### **Menu Items**
- **List Menu Items**: Customers can view all menu items, filter by category, and order by price.
- **Add/Edit/Delete Menu Items** (Manager Only): Managers can manage menu items.

### **Cart and Orders**
- **Add to Cart**: Customers can add items to their cart.
- **Place Order**: Placing an order clears the cart.
- **View Orders**: Customers can view their order history, and managers can view all orders.

### **Order Management**
- **Assign Orders** (Manager Only): Managers can assign orders to delivery crew members.
- **Update Order Status** (Delivery Crew): Delivery crew members can update the status of assigned orders.

---

## **Frontend Integration**
The frontend for this project is built using Flutter and can be found at the following repository:
[Master Chef Flutter-Django](https://github.com/HadiAlhamed/Master-chef-flutter-django)

To integrate the frontend with the backend:
1. Clone the Flutter repository:
   ```bash
   git clone https://github.com/HadiAlhamed/Master-chef-flutter-django.git
   ```
2. Update the API base URL in the Flutter app to point to your Django backend (e.g., `http://127.0.0.1:8000/`).
3. Run the Flutter app:
   ```bash
   flutter run
   ```

---

## **Future Improvements**
- **Token Authentication**: Replace session-based authentication with token-based authentication (e.g., JWT) for better scalability.

- **Notifications**: Implement real-time notifications for order updates (e.g., using WebSockets).
- **Deployment**: Deploy the application to a cloud platform (e.g., AWS, Heroku) for production use.

---

## **Contributing**
If you'd like to contribute to this project, feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss your ideas.

---

## **Contact**
For questions or support, feel free to reach out to me at:  
📧 **Email**: lama1e2dayoub@gmail.com

"""


