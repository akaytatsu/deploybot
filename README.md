# DeployBot

This project is for integration of slack + rundeck + chatbot integration. 
In resume, is for deploy projects using rundeck of slack bot integration.

### Using

* Python 3.6+
* Django 2.1
* Sqlite

### Instalation Guide

``` bash 
pip install -r requirements.txt 
python manage.py migrate
python manage.py createsuperuser
```

### Configuration 

Rename "settings.sample.ini" for "settings.ini"

edit this data:

``` settings
[settings]
SLACK_BOT_TOKEN={SLACK BOT TOKEN}
SLACK_CHANNEL_ID={CHANNEL CODE}
SLACK_DEPLOY_CHANNEL_ID={CHANNEL DEPLOY CODE}
RUNDECK_USER_NAME={RUNDECK USERNAME}
RUNDECK_USER_PASS={RUNDECK PASSWORD}
RUNDECK_URL={RUNDECK URL}
```

##### SlackBot Token

* Enter https://api.slack.com/apps
* Click "Create New App" and create your app
* Go to "Bot Users" and click "Add a Bot User"
* Go to "install App" and click "Install App to Workspace"
* Click Autorize
* Copy de content "Bot User OAuth Access Token" (this is SLACK BOT TOKEN)

##### SlackBot Channel Code

The code of channel is visible in URL:

https://yourspace.slack.com/messages/**CEU7RU5A7**/details/

##### SlackBot DEPLOY Channel Code

if you get log for all requests, do you set this param.

The code of channel is visible in URL:

https://yourspace.slack.com/messages/**CEU7RU5A7**/details/

#### Sincronize rundeck project

``` python
python manage.py sync_rundeck
```

#### Finally start slack listener

This process is continuos

```
python manage.py slack_listener
```