# Yodel forum

![screenshot](https://github.com/user-attachments/assets/6eef2634-2a65-4e62-878b-fc7b0bc12ad5)

## Getting Started:

Prepopulated SQLite database included for demonstration only.


#### 1. Create virtual environment:
A virtual environment is used to isolate the project's dependencies. 

`$ python3 -m venv <your_virtual_environment_name>`

#### 2. Install dependancies:
`$ pip install -r requirements.txt`

#### 3. Obtain reCAPTCHA keys:
- Visit the Google reCAPTCHA admin console (https://www.google.com/recaptcha/admin) and create a new site key and secret key.
- Follow the instructions provided by Google to integrate reCAPTCHA into the project.

#### 4. Set reCAPTCHA keys as environment variables:
- Create a `.env` file and add the following lines, replacing <YOUR_SITE_KEY> and <YOUR_SECRET_KEY> with your actual reCAPTCHA keys:
`RECAPTCHA_PUBLIC_KEY='<YOUR_SITE_KEY>'`

`RECAPTCHA_PRIVATE_KEY='<YOUR_SECRET_KEY>'`

#### 5. Create superuser to access admin dashboard:
This user will have full access to the forum's admin panel. 

- For Windows run
`$ python manage.py createsuperuser`
- For Mac/Linux run
`$ python3 manage.py createsuperuser`

#### 6. Start development server
This will start the forum locally so you can access it in your web browser.

`$ python3 manage.py runserver`

By default, the server will be running on http://127.0.0.1:8000/. Open this address in a web browser to see the forum.


### Or (For Own Testing)


#### 1. Remove prepopulated data
- Delete the `db.sqlite3` file from the root directory
- Remove migrations 0001 and 0002 from both the `content` and `users` apps (located in the `migrations` folder).
- Delete all user folders within the `media` directory except for `default.png.`

#### 2. Configure database settings (skip this step if not using Postgres):
- In the project's `yodel/settings.py` file, comment out the SQLite database configuration section.
- Uncomment the Postgres database configuration section.
- Create a `.env` file in the project's root directory and store your Postgres database connection details as environment variables.

#### 3. Migrate models, integrate reCAPTCHA and create admin user:
- Create migration files for model changes:
`$ python3 manage.py makemigrations`

- Apply the migrations to database:
`$ python3 manage.py migrate`

- Obtain reCAPTCHA keys using steps 3 and 4 of the "Getting Started" section.

- Create an admin user using the same command as before (step 5 of the "Getting Started" section).


#### 4. Run the server and populate data:
- Start the development server using the same command (step 6 of "Getting Started").
- Visit the admin dashboard at http://127.0.0.1:8000/admin/ to create dummy content for different topics (at least 7 for pagination to work properly).

#### 6. Visit the forum
- After populating some topics, navigate to http://127.0.0.1:8000/ to see the Yodel forum