# Site status bot for AWS Lambda

Bot:
```
✅✅
20:00:00 11.11.18

200    https://google.com
200    https://www.mozilla.org
```

## Environment variables
* `urls`: URLs that the bot will check.
* `token`: Bot token.
* `message_id`: Updateable message.
* `chat_id`: Chat id with message.

#### Example

* `urls`: `https://google.com,https://www.mozilla.org`
* `token`: `95123483458:AAAz65W9-bghuiacsYUnbghuiMNjkMhuio`
* `message_id`: `7`
* `chat_id`: `-1000000000000`

## To create a deployment package
1. Create a virtual environment.
    ```bash
    virtualenv ~/shrink_venv
    source ~/shrink_venv/bin/activate
    ```

1. Install libraries in the virtual environment
    ```bash
    pip install -r requirements.txt
    ```

1. Add the contents of lib and lib64 site-packages to your .zip file.
    ```bash
    cd $VIRTUAL_ENV/lib/python3.6/site-packages
    zip -r9 ~/service_status_bot_lambda.zip .
    ```
    
1. Add your python code to the .zip file
    ```bash
    cd ~
    
    zip -g service_status_bot_lambda.zip main.py
    zip -g service_status_bot_lambda.zip checker.py
    ```
