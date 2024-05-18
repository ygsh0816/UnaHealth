# UnaHealth
# Glucose Levels API

This Django project is designed to store and manage glucose level data for users. It provides API endpoints to retrieve glucose levels for a specific user, with options to filter by timestamps, sort, paginate, and limit the results.

## Features

- **Models:** Defines the data structure for storing glucose levels.
- **Serializers:** Handles the conversion between Django models and JSON.
- **Views:** Manages the logic for handling API requests and responses.
- **URLs:** Routes the API requests to the appropriate views.
- **Data Loading:** Includes a management command to load sample data from CSV files.

### Prerequisites

Ensure you have the following installed on your local machine:
- Python 3.8+
- Git

### Step 1: Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/ygsh0816/UnaHealth.git
cd unahealth
```

### Step 2: Create a virtual env

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
### Step 4: Set Up the Database

```bash
python manage.py makemigrations
python manage.py migrate
```
### Step 5: Load Sample Data

```bash
python manage.py load_sample_data
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```
### Step 7: Test the API
You can now test the API using a tool like Postman or cURL. The available endpoints are:

1. Retrieve a list of glucose levels for a specific user, with optional filtering by timestamps, sorting, and pagination:
    ```bash
   GET /api/v1/levels/?user_id=<user_id>&start=<start_timestamp>&stop=<stop_timestamp>&ordering=<field>&page_size=<number>&page=<number>&limit=<number>&ordering=<order_by_field>
   ```
2. Retrieve a specific glucose level by its ID:
```bash
GET /api/v1/levels/<id>/
```
3. Create a Glucose Level entry for a user
```bash
POST /api/v1/levels/create/

request data:

{
    "user_id": "yogesh",
    "timestamp": "2021-02-18T12:12:00Z",
    "device_name" : "Apple Watch",
    "device_serial_number": "S34TRE67",
    "glucose_value": 55

}
```
4. Export the User data to a json file or CSV file
```bash
GET /api/v1/levels/export/?user_id=<user_id>&format_type=<format_type>
```

## Future Improvements that can be done
1. Authentication and Authorization:
   * Implement user authentication (e.g., using JWT or OAuth2) to secure the API.
   * Add permissions to control access to data based on user roles.

2. Enhanced Filtering:
   * We can add more advanced filtering options, such as filtering by glucose value ranges.

3. Error Handling:
   * Improve error handling and return more descriptive error messages.
4. Asynchronous Processing:
   * Implement asynchronous processing for long-running tasks, such as exporting large datasets.
5. Throttling and Rate Limiting:
   * Implement throttling to prevent abuse of the API.
6. Data Validation:
   * Add more comprehensive validation for input data to ensure data integrity.
7. Documentation:
   * Use tools like Swagger or Redoc to generate interactive API documentation.
8. Create Env Variables for constants, secrets, etc.

By implementing these improvements, we can enhance the functionality, security, and performance of this small project, making it more robust and scalable.