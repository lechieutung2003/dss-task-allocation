# Pandosima intern starter project
We publish this repository to help students, who wisht to join Pandosima's intership/open training program, have chance to adtap with technologies and build something for yourself.
* Checkout this project as a starter point.
* Follow the guideline in Readme files to setup enviroment, build and run the backend, frontend. 
* Then take a look on the project's structure, coding convention,...
* Read the requirements in Todo.md files to implement/develop features and functions as your own.

## Requirements

* MySQL Client 8.0
* Python 3.12.2. Note: One Mac OSX, after install python, make sure to go to the `Applications/<your python folder>` and rund the command `Install Certificates.command`.
* Node 22.14.0 (LTS) or later
* [Gettex](https://mlocati.github.io/articles/gettext-iconv-windows.html)
* You have to follow [this guide](./devtools/Readme.md) to setup local development environment before starting config or build source code.
## Preparing accounts
(Only creates these accounts for your local debuging puporse. On the server side, we already created these accounts for all environments.)
1. Create account for mailing service
    * Register an new [Google Account](https://accounts.google.com/) for mailing service 
    * Turn on [2-Steps Verification](https://support.google.com/accounts/answer/185839) for your account
    * Create an [App Passwords](https://support.google.com/mail/answer/185833) for your mailing service
    * Remember [SMTP setup options](https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-restricted-gmail-smtp-server%2Cuse-the-gmail-smtp-server) to fill in `backend/config.env` later.

## Install dependencies

### Create virtual environemnt

* For Linux:

```
    python3 -m venv .venv
    source .venv/bin/activate
```

* For Mac OS:

```
    python3 -m venv .venv
    source .venv/bin/activate
```

* For Windows:

```
    py -3 -m venv .venv
    .venv\scripts\activate
```

### Install dependencies

```
    pip3 install -r requirements/base.txt
```
Note: For Mac OSX, before installing python libraries, you might have to install addition tools and export environment variables
#### Install addition tools:
```
brew install mysql-client pkg-config
```
#### Export environment variables:
```
export CFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -I/usr/local/include/ ${CFLAGS}"
export LDFLAGS="-isysroot $(xcrun --show-sdk-path) -L/usr/local/lib -L/usr/lib"
export CPPFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -L/usr/lib"
export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

## Config and build

### Create RSA private key

Go to the [backend](./backend/) folder and runt the command below on your terminal. If you are using Windows, the command below should be run in git bash shell instead.

```
    openssl genrsa -out oidc.key 4096
```

### Config environment variables
Copy the [backend/config.env.sample](backend/config.env.sample) to `backend/config.env`, then open the file and change values for environment variables.

### Migrate data
From the [backend](backend) folder, runt this command:
```
python manage.py migrate
```
### Build business site frontend
From the [business](business) folder, runt these commands:
```
npm install
npm run build
```

### Collect static files
(For production only)
From the [backend](backend) folder, runt this command:
```
python manage.py collectstatic --settings=core.settings.base
```

### Run
From the [backend](backend) folder, runt this command:
```
python manage.py runserve
```
You can also open the project with Visual Studio Code, Open the `Run and Debug tab` and run the config `Run Dev`

## Access the webstites
* Access the host pointed by the `BUSINESS_HOST` environemnt variable, you will see the business site. Example: http://127.0.0.1:8008

## Debuging
In case you want to debug frontend in paralell with backend, make sure to follow these step:
1. Turn on these evironement variable (in `backend/config.env`):
```
BUSINESS_FRONTEND_DEV_MODE=True
DOCS_FRONTEND_DEV_MODE=True
```
2. Run the business site (frontend)
From visual studio terminal, at the folder [business](business):
```
npm install
npm run dev
```
3. Run the document site (frontend)
From visual studio terminal, at the folder [docs](docs):
```
npm install
npm run dev
```
4. On Visual studio, in the `Run and Debug` tag, chose `Run Dev` and click the run button next to it.

Note: Copy [launch config tempalte](./.vscode/launch-template.json) to [launch config file](./.vscode/launch.json). Depend on your Operation System, you might have to modify the [launch config](./.vscode/launch.json), change path separator from '/' to '\\\\' and versa.

## Using docker
If you want to use docker, copy these file to the root folder and rename it:
- [ci/docker-compose.yml.local](ci/docker-compose.yml.local) -> `docker-compose.yml`
- [ci/Dockerfile.template](ci/Dockerfile.template) -> `Dockerfile`
- [ci/docker.env.template](docker.env.template) -> `docker.env`. Then open it and change the environment variable's values acord to your environment.

Build and run the container:
```
docker-compose up -d --build
```

## Localization
To translate your response content to other langueages:
1. Create [language files](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#localization-how-to-create-language-files) inside each app folder.

    For example: [backend/businesses/locale/vi/LC_MESSAGES/django.po](./backend/businesses/locale/vi/LC_MESSAGES/django.po)
Note that you can use [django-admin makemessages](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#localization-how-to-create-language-files) command to create this file. It will collect the text from python/html/js files and generate the languague file for you. But sometime, we traslate dynamic text from database or external services too. They are not available in your source code, so make sure to put these text to the file manually.

2. From your app folder, call this command to compile the texts
```
django-admin compilemessages
```

3. Use translate APIs

    Use [translate APIs](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/) to translate your response or your templates.

4. Consum translated contents

    On client side (frontend or mobile app), put `Accept-Language` to your request, you will see the translated contents.
