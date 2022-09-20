# skelbiu-botas

## Use case

The bot retrieves the most recently uploaded advertisements on skelbiu.lt and sends a notification through Telegram. It can be hosted for free on Heroku.

## How it works

When initialized, the bot first fetches all existing and visible advertisements with the given configuration and stores their ids in a set. After finishing, every 30 seconds it fetches all unseen ads and sends their title, price, and link to Telegram as a message. Mostly new ads show up as well as the ones that were previously hidden.

### Set-up

1. Clone the repository
2. Follow this [post](https://stackoverflow.com/a/67152755) to set up the Telegram bot.
3. Modify the code (main.py) with your ClientId, bot API key, keywords, and advertisement filtering configuration.
4. Follow this [tutorial](https://www.youtube.com/watch?v=Ven-pqwk3ec) to set up the bot on Heroku.
