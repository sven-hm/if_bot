# Telegram Frotz Bot

## usage

### dependencies
Except some standard python modules:
* [telepot](https://github.com/nickoala/telepot)

* [frotz](https://github.com/DavidGriffith/frotz), the z-machine interpreter
    * clone repo
    * `make dumb` to get dfrotz

* a nice interactive-fiction-game, that frotz can handle (like zork)

* a running telegram bot
    * use [BotFather](https://core.telegram.org/bots)

### Configuration
0. Rename `tfbot.conf.template` in `tfbot.conf`.
1. Set path to dfrotz.
2. Set your bot's token you got from BotFather.
3. Set receiver id, or group id.
4. Set path to z-game-file.
5. Set path to backup file.

### Start

Run `python2.7 run_tfbot.py`.

