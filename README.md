# Splitgram

A simple cost splitting bot for Telegram.

## Setup

Create your own Telegram bot and acquire the Telegram TOKEN according to [Telegram BotFather documentation](https://core.telegram.org/bots#6-botfather).

Since Splitgram is designed to receive all messages in a Telegram chat, you need to set the bot privacy mode to false (send **/setprivacy** command to [BotFather](https://t.me/botfather))

You can run the bot using pipenv virtual environment. Execute the following commands in the project directory to install dependencies and to run the bot (make sure that you have pipenv installed in your system).

```
$ pipenv install
$ pipenv run python splitgram.py YOUR_TELEGRAM_TOKEN
```

Run unit tests:
```
$ pipenv run pytest
```

## Usage

Create a dedicated chat and add the bot and all the users you wish to take part to the cost splitting. When a user sends a message consisting only of an integer or a decimal number, the bot interprets this value as a payment and adds it to the user's total costs. The user is not considered as part of the cost splitting until he/she has messaged at least one value (if you want to join cost splitting without adding any value, just send 0). After every added value, the bot prints out the current state of the costs.

Example status message:

```
Lala owes Lulu 75.0 €
Nana owes Lulu 50.0 €
Nana owes Momo 75.0 €
```

In addition, the following commands are available:

**/reset** Reset the state<br/>
**/status** Print the current status<br/>
**/language** Set user language, pass the language string as a parameter (supported: en, de, fi)

## To Do
- Allow limiting users participating in a single cost (maybe by enabling tagging users in a cost message).
- Mode, where specific command needs to be used to add a cost. The reason for the current implementation is ease of use: it is much faster to write a single value '50', instead of '/add 50' or '@botName 50'.
- Status message: distinguish between users who have same name.
- Webhooks support.
- Improve performance by implementing concurrency.
