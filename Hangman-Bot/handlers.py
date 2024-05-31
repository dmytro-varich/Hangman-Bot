# Library
from aiogram import types, Bot
from aiogram.utils import exceptions 
from aiogram.types import ReplyKeyboardRemove, User
from main import dp, bot
from hangman import get_word, is_word_guessed, get_guessed_word, get_available_letters
from translate import Translator
from datetime import datetime
from math import ceil
from background import keep_alive
from kb import kb, Topics_UA, Topics_EN, Game_Buttons_UA, Game_Buttons_EN, Start_Daily_Word_UA, Start_Daily_Word_EN
from db import create_profile, add_topic, total_points, update_points, update_start_time, create_profile_to_play, get_data, get_time, change_count,\
    change_letters_guessed, delete_row, change_language, create_statistics, show_statistics, update_daily, rating_show, get_users_with_daily_option, add_total_points, add_mode

# user_id->0, secret->1, count->2, letters_guessed->3, language->4, time_start->5
# 🧐✍️✨😭🥰👺😎🙄🛐🤩😂🤧😞❤️🤮😍🌞😩🤪☺️😳🥳😶‍🌫️😡🤝😦😢😉😘😥👸🤨😔🥺😜🤕😄🤔👋☹️😊🔍🌿🐠🏀🔬🌍🎲🌄🌟🇬🇧🇺🇦


translator = Translator(to_lang="uk")

def user_check_profile(user_id):
    tag_name = ""
    user = User.get_current(user_id)
    if user.username:
        tag_name = f"@{user.username}"
    elif not isinstance(user, User):
        if user.last_name is not None:
            tag_name = f"{user.first_name} {user.last_name}"
        else:
            tag_name = f"<code>{user.first_name}</code>"
    return tag_name


async def get_user_info(bot: Bot, user_id):
    tag_name = ""
    try:
      user = await bot.get_chat(user_id)
      
      if user.username:
          tag_name = f"@{user.username}"
      elif not isinstance(user, User):
          if user.last_name is not None:
              tag_name = f"<code>{user.first_name} {user.last_name}</code>"
          else:
              tag_name = f"<code>{user.first_name}</code>"
    except exceptions.ChatNotFound: 
      pass
    finally:
      return tag_name


# Command: /START
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    #keep_alive()
    id = message.from_user.id
    await message.answer(text="""
Ласкаво просимо до нашого Телеграм Боту.
Welcome to our Telegram bot.
      """)
    await message.answer_animation(animation="CgACAgIAAxkBAAIOX2PEflqP2xcSYF-X1SI0DaXxUSmZAAKPCQACTs5xSImPadHwfWmsLQQ")
    await delete_row(id)
    await create_profile(user_id=message.from_user.id)
    await message.answer(text="Обери мову / Choose language:", reply_markup=kb)


# Command: /HELP
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0 and get_data(id, 4) != '':
        if get_data(id, 4) == 'ua':
          await message.answer(text="""
<b>О «Hangman»</b>
Шибениця — це гра, в якій потрібно відгадувати слово по літерах. Вгадані літери відкриваються в загаданому слові, при невдалій спробі малюється наступна частина шибениці. Гра закінчується у випадку, якщо гравець вгадає слово або інший гравець малює цілу шибеницю.

<b>Правила Гри</b>
1. Щоб запустити гру Вам потрібно вести команду /play. 
2. У Вас є 8 спроб, щоб вгадати слово. Віднімається спроба, якщо Ви вводите неправильну літеру, тобто цієї літери нема в наявності задуманого словa, а якщо правильна літера є, то спроби лишаються незмінними. Якщо спроб залишилося - 0, то це значить, що Ви програли.
3. Якщо ввести повністю слово, то гра автоматично видає Вам результат. Ввели одразу правильне слово — перемогли! Ввели неправильне слово — одразу програли! Спроб більше не буде.
4. Якщо Ви повторно вводите літеру, яка вже використовувалась - спроба не знімається.

<b>Команди</b>
/play — почати грати в гру 
/edit_language — змінити мову 
/statistics — статистика користувача
/rating — рейтинг користувачів
/daily_word — щоденне слово

<b>Розробники</b>
Варіч Д. О. — @Dima_Varich
Варіч В. О. — @w0leriy
Рагулін А. О. — @anton_rahulin
Поляков Р. В. — @Catharsy
          """)
        else:
          await message.answer(text="""
<b>About «Hangman»</b>
Hangman is a game in which you have to guess the word by letters. The guessed letters are revealed in the riddled word, with an unsuccessful attempt, the next part of the gallows is drawn. The game ends if a player guesses the word or another player draws the entire gallows.

<b>Game rules</b>
1. To start the game, you need to run the /play command.
2. You have 8 attempts to guess the word. An attempt is subtracted if you enter the wrong letter, that is, this letter is not present in the intended word, and if the correct letter is present, the attempts remain unchanged. If there are 0 attempts left, it means that you have lost.
3. If you enter the word in its entirety, the game will automatically give you the result. They immediately entered the correct word - they won! They entered the wrong word - they immediately lost! There will be no more attempts.
4. If you re-enter a letter that has already been used - the attempt is not removed.

<b>Commands</b>
/play — start playing the game
/edit_language — change language
/statistics — user statistics
/rating — user rating
/daily_word — daily word

<b>Creators</b>
Varich D. O. — @Dima_Varich
Varich V. O. — @w0leriy
Ragulin A. O. — @anton_rahulin
Polyakov R. V. — @Catharsy
          """)
    else:
        await message.delete()


# Command: /EDIT LANGUAGE
@dp.message_handler(commands=['edit_language'])
async def edit_language(message: types.Message):
    #keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0:
        await message.answer(text="Обери мову / Choose language:", reply_markup=kb)
        await change_language(id, '')
    else:
        await message.delete()


# Command: /STATISTICS
@dp.message_handler(commands=['statistics'])
async def statistics_command(message: types.Message):
    id = message.from_user.id
    user_statistics = await show_statistics(id)
    message = ""
    for idx, record in enumerate(user_statistics):
        secret = record[0]
        count = record[1]
        time = record[2]
        topic = record[3]
        points = record[4]
        if get_data(id, 4) == 'ua':
            message += f"""🎮 Запис <b>#{idx+1}</b>
📚 <b>Тема:</b> {topic}
🤫 <b>Секретне слово:</b> {secret}
📈 <b>Кількість спроб:</b> {count}
⏳ <b>Час гри:</b> {time}
🏅 <b>Очки:</b> {points}

"""
        elif get_data(id, 4) == 'gb':
            message += f"""🎮 Record <b>#{idx+1}</b>
📚 <b>Topic:</b> {topic}
🤫 <b>Secret word:</b> {secret}
📈 <b>Number of attempts:</b> {count}
⏳ <b>Game time:</b> {time}
🏅 <b>Points:</b> {points}

"""
    if get_data(id, 4) == 'ua':
        await bot.send_message(chat_id=id, text=f"""🏆 <b>Статистика найкращих твоїх ігор</b>  🏆

<b>Користувач:</b> {user_check_profile(id)}

{message}""")
    elif get_data(id, 4) == 'gb':
        await bot.send_message(chat_id=id, text=f"""🏆 <b>Statistics of your best games 🏆</b>

<b>User:</b> {user_check_profile(id)}  🏆

{message}""")


# Command: /RATING
@dp.message_handler(commands=['rating'])
async def rating_command(message: types.Message):
    message_text = ""
    user = message.from_user
    top_users = await rating_show()
    # print(top_users)
    if get_data(user.id, 4) == 'ua':
        message_text = "🏆 <b>Рейтинг найкращих гравців</b> 🏆\n\n"
        for rank, (user_id, points) in enumerate(top_users, start=1):
            tag_name = await get_user_info(bot, user_id)
            if tag_name == '': tag_name = '<code>User</code>'
            message_text += f"{rank}. {tag_name}  <i>{points} очок</i>\n"
    elif get_data(user.id, 4) == 'gb':
        message_text = "🏆 <b>The Best Players Rating</b> 🏆\n\n"
        for rank, (user_id, points) in enumerate(top_users, start=1):
            tag_name = await get_user_info(bot, user_id)
            if tag_name == '': tag_name = '<code>User</code>'
            message_text += f"{rank}. {tag_name}  <i>{points} points</i>\n"
    await bot.send_message(chat_id=user.id, text=message_text)


# Command: /DAILY_WORD
@dp.message_handler(commands=['daily_word'])
async def daily_word_command(message: types.Message):
    id = message.from_user.id
    if get_data(id, 4) == 'ua':
        await message.answer("🔮 Чи бажаєте отримувати щоденне слово?", reply_markup=Start_Daily_Word_UA)
    elif get_data(id, 4) == 'gb':
        await message.answer("🔮 Would you like to receive a daily word?", reply_markup=Start_Daily_Word_EN)


@dp.callback_query_handler(lambda callback: callback.data in ['Yes', 'No'])
async def callback_daily_word(callback: types.CallbackQuery):
    id = callback.from_user.id
    if get_data(id, 4) == 'ua':
        if callback.data == 'Yes':
            print(id, callback.data)
            await update_daily(id, callback.data)
            await callback.message.delete()
            await bot.send_message(chat_id=id, text="😎 Відмінно! Ви будете отримувати щоденні слова. Перше загадане слово надійде завтра. 📚🔮")
        elif callback.data == 'No':
            await update_daily(id, callback.data)
            await callback.message.delete()
            await bot.send_message(chat_id=id, text="🥺 Добре, Я не буду надсилати вам щоденні слова. Ви завжди можете активувати цю опцію командою /daily_word 🙌")
    elif get_data(id, 4) == 'gb':
        if callback.data == 'Yes':
            await update_daily(id, callback.data)
            await callback.message.delete()
            await bot.send_message(chat_id=id, text="😎 Great! You will receive daily words. The first guessed word will arrive tomorrow. 📚🔮")
        elif callback.data == 'No':
            await update_daily(id, callback.data)
            await callback.message.delete()
            await bot.send_message(chat_id=id, text="🥺 Ok, I won't send you daily words. You can always activate this option with the command /daily_word 🙌")


# Play Message
async def play_message(id):
    if get_data(id, 4) == 'gb':
        await bot.send_message(chat_id=id, text=f"🧐 I guessed the word: ||{len(get_data(id, 1)) * '? '}||",
                               parse_mode='MarkdownV2')
        await bot.send_message(chat_id=id, text=f"""
Welcome to the game <b>Hangman</b>!
I am thinking of a word that is <b>{len(get_data(id, 1))}</b> letters long
                        """)

        print("game was start")

        await bot.send_message(chat_id=id, text=f"""
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------
                        """)
    elif get_data(id, 4) == 'ua':
        await bot.send_message(chat_id=id, text=f"🧐 Я загадав слово: ||{len(get_data(id, 1)) * '? '}||",
                               parse_mode='MarkdownV2')
        await bot.send_message(chat_id=id, text=f"""
Ласкаво просимо до гри <b>Шибениця</b>
Я думаю про слово, яке складається з <b>{len(get_data(id, 1))}</b> літер
                         """)

        print("гра почалась")

        await bot.send_message(chat_id=id, text=f"""
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------
                    """)
      

# FUNCTION FOR POINTS TWO PARAMETERS
async def get_points(id):
    sum_points = 0
    topic = get_data(id, 5)
    secret = get_data(id, 1)

    # Points for difficult topic
    if topic in ['Flora', 'Fauna']:
        sum_points += 100
    elif topic in ['Sports', 'Countries']:
        sum_points += 150
    elif topic in ['RandomWord', 'Science']:
        sum_points += 200

    # Points for Length word Secret
    sum_points += len(secret) * 10

    total_seconds = get_time(id)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
  
    count = (8 - get_data(id, 2)) * 5
    if total_seconds > 300: total_seconds = 600
    final_points = sum_points - (total_seconds / 2) + count
    await total_points(id, final_points)

    time_parts = []
    if get_data(id, 4) == 'gb':
      if hours > 0:
          time_parts.append(f"{hours} h")
      if minutes > 0:
          time_parts.append(f"{minutes} m")
      if seconds > 0 or not time_parts:
          time_parts.append(f"{seconds} s")
    elif get_data(id, 4) == 'ua':
      if hours > 0:
          time_parts.append(f"{hours} г")
      if minutes > 0:
          time_parts.append(f"{minutes} хв")
      if seconds > 0 or not time_parts:
          time_parts.append(f"{seconds} с")
        
    return " ".join(time_parts)
 

async def statistics_message(id, text, mode):
    
    time = await get_points(id)

    if get_data(id, 4) == 'gb' and mode=="Daily Word":
        await bot.send_message(chat_id=id, text=f"""{text}

📊 <b>Game Statistics:</b>

📝 <b>Word:</b> {get_data(id, 1)}
📚 <b>Topic:</b> {get_data(id, 6)}
⏱ <b>Game time:</b> {time}
🏆 <b>Points per game:</b> {ceil(get_data(id, 8))}

Game over! Thank you for your participation and have a great time! 🌟""", parse_mode='HTML')
    elif get_data(id, 4) == 'gb' and mode=="Normal":
        await bot.send_message(chat_id=id, text=f"""{text}
        
📊 <b>Game Statistics:</b>

📝 <b>Word:</b> {get_data(id, 1)}
📚 <b>Topic:</b> {get_data(id, 6)}
⏱ <b>Game time:</b> {time}
🏆 <b>Points per game:</b>  {ceil(get_data(id, 8))}

Game over! Thank you for your participation and have a great time! 🌟""", reply_markup=Game_Buttons_EN)
    elif get_data(id, 4) == 'ua' and mode=="Daily Word":
        
        await bot.send_message(chat_id=id, text=f"""{text}
        
📊 <b>Статистика Гри:</b>

📝 <b>Слово:</b> {get_data(id, 1)}
📚 <b>Тема:</b> {translator.translate(get_data(id, 6))}
⏱ <b>Час гри:</b> {time}
🏆 <b>Очки за гру:</b> {ceil(get_data(id, 8))}

Гра завершена! Дякуємо за участь і гарно проведений час! 🌟""")
    elif get_data(id, 4) == 'ua' and mode=="Normal":
      await bot.send_message(chat_id=id, text=f"""{text}
        
📊 <b>Статистика Гри:</b>

📝 <b>Слово:</b> {get_data(id, 1)}
📚 <b>Тема:</b> {translator.translate(get_data(id, 6))}
⏱ <b>Час гри:</b> {time}
🏆 <b>Очки за гру:</b> {ceil(get_data(id, 8))}

Гра завершена! Дякуємо за участь і гарно проведений час! 🌟""", reply_markup=Game_Buttons_UA)
      
    await add_total_points(id, ceil(get_data(id, 8)))
    await create_statistics(id, user_check_profile(id), get_data(id, 1), 8-get_data(id, 2), time, get_data(id, 6), ceil(get_data(id, 8)))


# Daily game ...
@dp.callback_query_handler(lambda callback: callback.data in ['GuessNow', 'GuessLater'])
async def callback_profile(callback: types.CallbackQuery):
    id = callback.from_user.id
    await callback.message.delete()
    if callback.data == 'GuessNow':
        await update_points(id, 0)
        await total_points(id, 200)
        await update_start_time(id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        word = get_data(id, 10)
        await add_mode(id, "Daily Word")
        if get_data(id, 4) == 'ua':
            await add_topic(id, "Щоденне слово", "Daily word")
            await create_profile_to_play(user_id=id, secret=translator.translate(word).lower())
            await bot.send_message(chat_id=id, text=f"👌 <b>Чудово!</b> Тоді розпочнемо гру в щоденне слово 😎")
        elif get_data(id, 4) == 'gb':
            await add_topic(id, "Daily word", "Daily word")
            await create_profile_to_play(user_id=id, secret=word)
            await bot.send_message(chat_id=id, text=f"👌 <b>Awesome!</b> Let's find out the word 😎")
        await play_message(id)
    elif callback.data == 'GuessLater':
        if get_data(id, 4) == 'ua':
            await bot.send_message(chat_id=id, text=f"😔 Добре, тоді до завтра! 🌄 Але не забувай, що за гру в щоденне слово дають більше очок. Нехай тобі пощастить! 🎉")
        elif get_data(id, 4) == 'gb':
            await bot.send_message(chat_id=id, text=f"😔 Good, see you tomorrow! 🌄 Ale, don't forget what game in the chosen word to give more points. Let me spare you! 🎉")


# Command: /PLAY
@dp.message_handler(commands=['play'])
async def play_command(message: types.Message):
    # keep_alive()
    id = message.from_user.id
    if get_data(id, 2) == 0 and get_data(id, 4) != '':
        if get_data(id, 4) == 'gb':
            await message.answer("Choose a topic and I will guess the word for you 🔍", reply_markup=Topics_EN)    
        elif get_data(id, 4) == 'ua':
            await message.answer("Вибери тему, і я загадаю тобі слово 🔍", reply_markup=Topics_UA)       
    else:
        await message.delete()

      
@dp.callback_query_handler(lambda callback: callback.data in ['Flora', 'Fauna', 'Sports', 'Science', 'Countries', 'RandomWord'])
async def callback_profile(callback: types.CallbackQuery):
    id = callback.from_user.id
    # print("WOrkingg...")
    await update_points(id, 0)
    await update_start_time(id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    await add_mode(id, "Normal")
    await create_profile_to_play(user_id=id, secret=get_word(callback.data, get_data(id, 4)))
    await callback.answer(callback.data, show_alert=False)
    if get_data(id, 4) == 'gb':
        await add_topic(id, callback.data, callback.data)
        await callback.message.edit_text(text=f"Wonderful! You chose a topic — <b>{callback.data}</b>")
    elif get_data(id, 4) == 'ua':
        await add_topic(id, translator.translate(callback.data), callback.data)
        await callback.message.edit_text(text=f"Відмінно! Ти обрав тему — <b>{translator.translate(callback.data)}</b>")
    await play_message(id)


# NEW GAME (CONTINUE)
@dp.callback_query_handler(lambda callback: callback.data == 'New_Game')
async def callback_profile(callback: types.CallbackQuery):
    id = callback.from_user.id
    print(get_data(id, 7))
    await update_points(id, 0)
    await update_start_time(id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    await add_mode(id, "Normal")
    await create_profile_to_play(user_id=id, secret=get_word(get_data(id, 7), get_data(id, 4)))
    if get_data(id, 4) == 'gb':
        await callback.answer(callback.data, show_alert=False)
        await add_topic(id, get_data(id, 6), get_data(id, 7))
        await callback.message.edit_text(text=f"👾 Let's keep the game going with the same topic — <b>{get_data(id, 7)}</b>")
        
    elif get_data(id, 4) == 'ua':
        await callback.answer(translator.translate(callback.data), show_alert=False)
        await add_topic(id, translator.translate(get_data(id, 6)), get_data(id, 7))
        await callback.message.edit_text(text=f"👾 Продовжуймо гру з тією ж темою — <b>{translator.translate(get_data(id, 7))}</b>")
    await play_message(id)


# NEW_TOPIC (RESTART)
@dp.callback_query_handler(lambda callback: callback.data == 'New_Topic')
async def callback_profile(callback: types.CallbackQuery):
    id = callback.from_user.id
    await callback.message.delete()
    await bot.send_message(chat_id=id, text="Відмінно! Ти бажаєш змінити тему 🌟")
    if get_data(id, 2) == 0 and get_data(id, 4) != '':
        if get_data(id, 4) == 'gb':
            await bot.send_message(chat_id=id, text="Choose a topic and I will guess the word for you 🔍", reply_markup=Topics_EN)
        elif get_data(id, 4) == 'ua':
            await bot.send_message(chat_id=id, text="Виберіть нову тему для гри і я загадаю тобі слово 🔍", reply_markup=Topics_UA)
    else:
        await callback.message.delete()


# Game
@dp.message_handler(content_types='text')
async def game(message: types.Message):
    # keep_alive()
    id = message.from_user.id
    if get_data(id, 2) != 0:
        if get_data(id, 4) == 'gb':
            alphabet = "qwertyuiopasdfghjklzxcvbnm"
            if len(message.text) == 1 and message.text.lower() in alphabet:
                word = message.text.lower()
                if word in get_data(id, 3):
                    await message.answer(
                        f"Letter ' <b>{word}</b> ' has been used already: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 5)  # POINTS_ATTEMPT
                elif word in get_data(id, 1):
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(f"Good guess: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 10)  # POINTS_GUESSING
                    if is_word_guessed(get_data(id, 1), get_data(id, 3)) == 1:
                        await message.answer("🥳 <b>Congratulations, you won!</b>")
                        await total_points(id, 125 * (get_data(id, 2) / 10))  # POINTS_ALL_GUESSING
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                        if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🎉 Congratulations! You guessed the daily word - that's great! 💫", "Daily Word")
                        elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                        print('id: ', get_data(id, 0), 'won')
                        await change_count(id, 0)
                        return
                else:
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(
                        f"Oops! ' <b>{word}</b> ' is not a valid letter: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 5)  # POINTS_ATTEMPT
                    await change_count(id, get_data(id, 2) - 1)
                    if get_data(id, 2) == 0:
                        await message.answer(f"😭 Sorry, <b>you lose</b>. The word was <code>{get_data(id, 1)}</code>.")
                        await total_points(id, -150)  # POINTS_LOSS
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                        if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🌈 You didn't guess this time, but don't be upset. Next time you will definitely succeed! 🌻", "Daily Word")
                        elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                        print('id: ', get_data(id, 0), 'lost')
                        await change_count(id, 0)

                        return

                await message.answer(text=f"""
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Topic — <b>{get_data(id, 6)}</b>.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------""")
            elif len(message.text) == 1 and message.text not in alphabet:
                await message.answer("Please use only english letters!")
                await message.answer(text=f"""
------------------------------
You have <b>{get_data(id, 2)}</b> guesses left.
Topic — <b>{get_data(id, 6)}</b>.
Available letters: {get_available_letters(get_data(id, 3), get_data(id, 4))}
word: {get_guessed_word(get_data(id, 1), get_data(id, 3))}
------------------------------""")
            elif len(message.text) > 1:
                if message.text.lower() == get_data(id, 1):
                    await message.answer("🥳 <b>Congratulations, you won!</b>")
                    await total_points(id, 125 * (get_data(id, 2) / 10))  # POINTS_ALL_GUESSING
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                    if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🎉 Congratulations! You guessed the daily word - that's great! 💫", "Daily Word")
                    elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                    print('id: ', get_data(id, 0), 'won')
                else:
                    await message.answer(f"😭 Sorry, <b>bad guess</b>. The word was <code>{get_data(id, 1)}</code>.")
                    await total_points(id, -150)  # POINTS_LOSS
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                    if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🌈 You didn't guess this time, but don't be upset. Next time you will definitely succeed! 🌻", "Daily Word")
                    elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                    print('id: ', get_data(id, 0), 'lost')
                await change_count(id, 0)
                return
        elif get_data(id, 4) == 'ua':
            alphabet = "''йцукенгґшщзхїфівапролджєячсмитьбю"
            if len(message.text) == 1 and message.text.lower() in alphabet:
                word = message.text.lower()
                if word in get_data(id, 3):
                    await message.answer(
                        f"Літера ' <b>{word}</b> ' вже використовувалась: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 5)  # POINTS_ATTEMPT
                elif word in get_data(id, 1):
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(f"Гарна спроба: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 10)  # POINTS_GUESSING
                    if is_word_guessed(get_data(id, 1), get_data(id, 3)) == 1:
                        await message.answer("🥳 <b>Вітання, ти переміг!</b>")
                        await total_points(id, 125 * (get_data(id, 2) / 10))  # POINTS_ALL_GUESSING
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                        if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🎉 Вітаємо! Ви вгадали щоденне слово - це чудово! 💫", "Daily Word")
                        elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                        print('id: ', get_data(id, 0), 'won')
                        await change_count(id, 0)
                        return
                else:
                    letters_guessed_new = get_data(id, 3) + word
                    await change_letters_guessed(id, letters_guessed_new)
                    await message.answer(
                        f"Уупс! ' <b>{word}</b> ' літера не підходить: {get_guessed_word(get_data(id, 1), get_data(id, 3))}")
                    await total_points(id, 5)  # POINTS_ATTEMPT
                    await change_count(id, get_data(id, 2) - 1)
                    if get_data(id, 2) == 0:
                        await message.answer(
                            f"😭 Вибачте, <b>ви програли</b>. Я загадав <code>{get_data(id, 1)}</code>.")
                        await total_points(id, -150)
                        await message.answer_animation(
                            animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                        if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🌈 Ви не вгадали цього разу, але не засмучуйтесь. Наступного разу точно вдасться! 🌻", "Daily Word")
                        elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                        print('id: ', get_data(id, 0), 'lost')
                        await change_count(id, 0)

                        return

                await message.answer(text=f"""
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Тема — <b>{get_data(id, 6)}</b>.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
------------------------------""")
            elif len(message.text) == 1 and message.text not in alphabet:
                await message.answer("Будь ласка, використовуй тільки українські літери!")
                await message.answer(text=f"""
------------------------------
Ти маєш <b>{get_data(id, 2)}</b> спроб.
Тема — <b>{get_data(id, 6)}</b>.
Ти можеш використовувати літери: {get_available_letters(get_data(id, 3), get_data(id, 4))}
слово: {get_guessed_word(get_data(id, 1), get_data(id, 3))}
------------------------------"""
                                     )
            elif len(message.text) > 1:
                if message.text.lower() == get_data(id, 1):
                    await message.answer("🥳 <b>Вітання, ти переміг!</b>")
                    await total_points(id, 125 * (get_data(id, 2) / 10))  # POINTS_ALL_GUESSING
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGVWPBlgeuAfUyhDksznKNtkDAtnWZAAK2AgACaYgNU4wtzH86zUCuLQQ')
                    if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🎉 Вітаємо! Ви вгадали щоденне слово - це чудово! 💫", "Daily Word")
                    elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                    print('id: ', get_data(id, 0), 'won')
                else:
                    await message.answer(f"😭 Вибачте, <b>ви програли</b>. Я загадав <code>{get_data(id, 1)}</code>.")
                    await total_points(id, -150)
                    await message.answer_animation(
                        animation='CgACAgQAAxkBAAIGWWPBlk1ToX-nSFX3v65h8fzQgZgAA-QCAAKmWERTuaKDCXVqayItBA')
                    if get_data(id, 11) == "Daily Word":
                            await statistics_message(id, "🌈 Ви не вгадали цього разу, але не засмучуйтесь. Наступного разу точно вдасться! 🌻", "Daily Word")
                    elif get_data(id, 11) == "Normal":
                            await statistics_message(id, '', "Normal")
                    print('id: ', get_data(id, 0), 'lost')
                await change_count(id, 0)
                return
    else:
        if get_data(id, 4) == '':
            if message.text == '🇬🇧':
                await change_language(id, 'gb')
                await message.answer("Language has been chosen: 🇬🇧", reply_markup=ReplyKeyboardRemove())
                await message.answer_animation(
                    animation="CgACAgQAAxkBAAIMX2PEaxuSXHx370MYiZThZGUs9sRcAALdAgACSHMNU-y3XeWcD72ILQQ")
                await message.answer("Use /play to start the game")

            elif message.text == '🇺🇦':
                await change_language(id, 'ua')
                await message.answer("Мова обрана: 🇺🇦", reply_markup=ReplyKeyboardRemove())
                await message.answer_animation(
                    animation="CgACAgQAAxkBAAIMXGPEaqThQRkHtXYnB7MDS8tEq5JwAAInAwACt3cFU7KZqW-eAAH4Jy0E")
                await message.answer("Щоб почати гру введіть команду /play")
        await message.delete()

    print('id: ', get_data(id, 0), 'count: ', get_data(id, 2))