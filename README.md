# Carb Cycling Calculator

## Overview
The Carb Cycling Calculator is a webapp built with Flask that helps users manage their nutrition strategy based on their training schedule. The application allows users to input their dietary preferences and training days, and it calculates a personalized carb cycling plan.

## Features
- User authentication (sign up, login, logout)
- Input fields for protein intake, calorie intake, and carb cycling days
- Dynamic calculation of daily caloric needs based on user input
- Display of personalized nutrition strategy on the profile page
- Responsive design using Bootstrap for a better user experience

## Preview of the final result
<img width="1403" alt="Preview of WebApp" src="https://github.com/user-attachments/assets/c55a62a0-0f8f-4a5e-a9d0-23ac5eca47dd">


## Technologies Used
- **Flask**: A lightweight WSGI web application framework for Python.
- **SQLite**: A lightweight database for storing user data.
- **Bootstrap**: A front-end framework for developing responsive web applications.

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone <https://github.com/FlavioMili/Carb-Cyclying-Calculator.git
   >
   cd <CarbCycling>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - The application will automatically create a SQLite database file (`database.db`) in the `instance` directory when you run it for the first time.

4. Run the application:
   ```bash
   python main.py
   ```

5. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- **Sign Up**: Create a new account by providing your email and password.
- **Login**: Access your account using your registered email and password.
- **Home Page**: Input your protein intake, calorie intake, and carb cycling days.
- **Profile Page**: View your personalized carb cycling data and nutritional strategy.

## License
This project is licensed under the MIT License.


