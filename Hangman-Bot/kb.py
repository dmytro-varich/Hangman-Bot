from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# Keyboard for language
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('🇺🇦')).insert(KeyboardButton('🇬🇧'))


# Keyboard for topics UA
Topics_UA = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🌿 Флора', callback_data='Flora'))
Topics_UA.add(InlineKeyboardButton('🐠 Фауна', callback_data='Fauna'))
Topics_UA.add(InlineKeyboardButton('🏀 Спорт', callback_data='Sports'))
Topics_UA.add(InlineKeyboardButton('🔬 Наука', callback_data='Science'))
Topics_UA.add(InlineKeyboardButton('🌍 Країни', callback_data='Countries'))
Topics_UA.add(InlineKeyboardButton('🎲 Випадкове слово', callback_data='RandomWord'))
# Topics_UA.add(InlineKeyboardButton('🍽 Продукти та страви', callback_data='Products'))


# Keyboard for topics EN
Topics_EN = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🌿 Flora', callback_data='Flora'))
Topics_EN.add(InlineKeyboardButton('🐠 Fauna', callback_data='Fauna'))
Topics_EN.add(InlineKeyboardButton('🏀 Sports', callback_data='Sports'))
Topics_EN.add(InlineKeyboardButton('🔬 Science', callback_data='Science'))
Topics_EN.add(InlineKeyboardButton('🌍 Countries', callback_data='Countries'))
Topics_EN.add(InlineKeyboardButton('🎲 Random word', callback_data='RandomWord'))
# Topics_EN.add(InlineKeyboardButton('🍽 Products and dishes', callback_data='Products'))


# Keyboard for game buttons in the final
Game_Buttons_UA = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🎮 Нова гра', callback_data='New_Game'))
Game_Buttons_UA.add(InlineKeyboardButton('🔄 Змінити тему', callback_data='New_Topic'))


Game_Buttons_EN = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🎮 New game', callback_data='New_Game'))
Game_Buttons_EN.add(InlineKeyboardButton('🔄 Change topic', callback_data='New_Topic'))


# Keyboard for Daily_Word
Start_Daily_Word_UA = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('Звісно, хочу! ✅', callback_data='Yes'))
Start_Daily_Word_UA.add(InlineKeyboardButton('Ні, не сьогодні ❌', callback_data='No'))


Start_Daily_Word_EN = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('Sure, I want! ✅', callback_data='Yes'))
Start_Daily_Word_EN.add(InlineKeyboardButton('No, not today ❌', callback_data='No'))