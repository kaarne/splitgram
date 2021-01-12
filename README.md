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

## Usage

When the bot is present in a Telegram chat, and any user sends a message consisting only of an integer or decimal number, the bot interprets this value as a payment that the user in question has made. The user is not considered as part of the cost splitting until he/she has messaged at least one value (if you want to join cost splitting without adding any value, just send 0). After every added value, the bot prints out the current state of the costs. It is recommended that a dedicated chat is created for the cost splitting purposes, so that no values are accidentally added during regular conversation. 

Example status message:

Lala owes Lulu 75.0 €<br/>
Nana owes Lulu 50.0 €<br/>
Nana owes Momo 75.0 €

In addition, the following commands are available:

**/reset** Reset the state<br/>
**/status** Print the current status

## Todo

- Optionally limit users participating in a single cost by enabling tagging users in a cost message.
- Don't force disabling privacy mode by letting users also add costs via a command (e.g. /add 19.90) if that is what they prefer. The original reason for not enabling this is ease of use: it is much faster to write a single value **50**, instead of **/add 50** or **@botName 50**.
- Localisation
- Improve performance by implementing concurrency.
