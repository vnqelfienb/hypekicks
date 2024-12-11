# hypekicks

## Project Information
This is my submission for the SoftUni Django Advanced Exam.
HypeKicks is a e-commerce website for luxury sneakers.
My intention for the exam was to create a website that mimics a 'real world' example rather than something unique and original.

## Project Stack
### Frontend
> [HTMX](https://htmx.org/)
> [AlpineJs](https://alpinejs.dev/)
> [Tailwind](https://tailwindcss.com)
> [Django Cotton](https://django-cotton.com/)

### Backend
> [Django](https://www.djangoproject.com/)


## Project Setup

### Clone the repo and create the virtual env
```bash
git clone https://github.com/vnqelfienb/hypekicks.git
```

```bash
cd hypekicks
python3 -m venv .venv
```

### Install project dependencies

```bash
# activate the virtual env

# for mac/linux
source .venv/bin/activate

# for windows
.\venv\Scripts\activate

pip3 install -r requirements.txt

# or if you use a python package manager like uv or poetry
uv pip install -r pyproject.toml 
```

### Install Tailwind

```bash
# cd into project/tailwind
npm install
```
There are two commands:
```bash
npm run watch:css
# this command is used for development purposes

npm run build:css
# this command compiles and minifies the main.css
```

### Environment variables
```bash
# create a .env file in project/project
touch .env
```

```env
# this is a template for the env vars
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=

RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=

EMAIL_HOST=smtp.gmail.com
EMAIL_FROM=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=587
EMAIL_USE_TLS=True

STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

PAYMENT_SUCCESS_URL=http://127.0.0.1:8000/products/payment-success/
PAYMENT_CANCEL_URL=http://127.0.0.1:8000/products/payment-cancel/
BACKEND_DOMAIN=http://127.0.0.1:8000


# they can be tweaked in settings.py accordingly
```

#### Generate a Django Secret Key
```python
# python3 manage.py shell

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Place the generated secret key in the .env
