# [Hangman-Bot](https://t.me/hangman_guessing_game_bot)

Hangman is a Telegram bot where you have to guess words letter by letter on various topics. Guessed letters are revealed in the hidden word, and with each incorrect attempt, a part of the hangman is drawn. The game ends when the player guesses the word or when the entire hangman is drawn.

![image](https://github.com/dmytro-varich/Hangman-Bot/assets/136006220/a8bbfeef-4822-4c42-80ce-561f20428765)

## Promo Video
[https://github.com/dmytro-varich/Hangman-Bot/blob/main/Hangman_Bot_Promo_Video.mp4](https://github.com/dmytro-varich/Hangman-Bot/assets/136006220/ed41bd6a-8458-4dbf-b466-a74872a49e4b)

## Features
- **Various Themes**: Players can choose from a variety of themes for word guessing. Themes: `Flora`, `Fauna`, `Sports`, `Science`, `Countries`, `Random Word`.
- **"Daily Word"**: Upon activating this command, the player receives a random word every morning and earns more points.

## Game Rules
1. To start the game, type the command `/play`. After that, choose the theme you want to guess.
2. You have **8** attempts to guess the word. An attempt is deducted if you enter a wrong letter, i.e., a letter not present in the hidden word. If the correct letter is present, the attempts remain *unchanged*. If there are no attempts left - **0**, it means you *lose*.
3. If you enter the entire word correctly, the game automatically gives you the result. Enter the right word at once — *you win!* Enter the wrong word — *you lose* immediately. There will be no more attempts.
4. If you enter a letter that has already been used, the *attempt is not deducted*.

## Commands
- `/start` - start the bot.
- `/play` - start playing.
- `/edit_language` - change the language.
- `/statistics` - show game statistics.
- `/rating` - player rating.
- `/daily_word` - daily word.
- `/help` - instructions.

## Supported Languages
- Ukrainian 🇺🇦
- English 🇬🇧

## About the Project
Developing the Telegram bot was a task for the "Software Development" course at [HRTK](https://www.hrtt.kh.ua/). Its goal was to gather a team, develop a project aimed at the audience, and present it for product evaluation. The team consisted of 4 people: Dmytro Varich, Valeriy Varich, Anton Ragulin, Roman Polyakov. The active development phase was in the winter of 2022 when the product was eventually presented. Subsequent optimizations and additions took place, such as displaying the player's game history, rating the best players, adding various themes, etc. Additionally, a promo video was created to attract Telegram users to the game.

## Future Updates
Thanks to this project, the path was paved for working with the [aiogram](https://docs.aiogram.dev/) framework, creating a database using [SQLite](https://sqlite.org/), interaction between the server and [Telegram](https://web.telegram.org/), and other aspects. Unfortunately, the project is currently not supported by developers and does not have a server for operation. However, it can be anticipated that future steps in the project's development would include creating the Hangman game in the form of a [mini-app](https://core.telegram.org/bots/webapps) in Telegram, code optimization, and improving the bot's interface.
