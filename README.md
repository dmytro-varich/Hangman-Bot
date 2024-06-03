# [Hangman-Bot](https://t.me/hangman_guessing_game_bot)
Шибениця — це телеграм-бот, у якому потрібно відгадувати слова по літерах на різні теми. Вгадані літери відкриваються в загаданому слові, при невдалій спробі малюється наступна частина шибениці. Гра закінчується, якщо гравець вгадає слово або якщо буде намальована вся шибениця.

![image](https://github.com/dmytro-varich/Hangman-Bot/assets/136006220/a8bbfeef-4822-4c42-80ce-561f20428765)


## Промо-відео (Українською)
[https://github.com/dmytro-varich/Hangman-Bot/blob/main/Hangman_Bot_Promo_Video.mp4
](https://github.com/dmytro-varich/Hangman-Bot/assets/136006220/ed41bd6a-8458-4dbf-b466-a74872a49e4b
)

## Можливості
- **Різні теми**: Гравець може обирати різноманітні теми для відгадування слів. Теми: `Флора`, `Фауна`, `Спорт`, `Наука`, `Країни`, `Випадкове слово`.
- **«Щоденне слово»**: При активації цієї команди гравець буде отримувати випадкове слово кожного ранку та здобуватиме більше очок.

## Правила Гри
1. Щоб запустити гру Вам потрібно вести команду `/play`. Після цього оберіть тему, яку бажаєте відгадувати.
2. У Вас є **8** спроб, щоб вгадати слово. Віднімається спроба, якщо Ви вводите неправильну літеру, тобто цієї літери нема в наявності задуманого словa, а якщо правильна літера є, то спроби лишаються *незмінними*. Якщо спроб залишилося - **0**, то це значить, що Ви *програли*.
3. Якщо ввести повністю слово, то гра автоматично видає Вам результат. Ввели одразу правильне слово — *перемогли!* Ввели неправильне слово — одразу *програли!* Спроб більше не буде.
4. Якщо Ви повторно вводите літеру, яка вже використовувалась - *спроба не знімається*.
   
## Команди 
- `/start` - запустити бота.
- `/play` - почати грати.
- `/edit_language` - змінити мову.
- `/statistics` - показати статистику ігор.
- `/rating` - рейтинг гравців.
- `/daily_word` - щоденне слово.
- `/help` - інструкція.

## Підтримувані мови
- Українська 🇺🇦
- English 🇬🇧

## Про проект
Розробка телеграм-бота була завданням для предмету "Розробка ПЗ" у навчальному закладі [ХРТК](https://www.hrtt.kh.ua/). Метою його було зібрати команду, розробити проект, спрямований на аудиторію, та його презентація для оцінки продукту. У складі команди було 4 людини: Дмитро Варіч, Валерій Варіч, Антон Рагулін, Роман Поляков. Активна фаза розробки припадала на зиму 2022 року, коли в кінцевому підсумку був представлений продукт. Після цього відбулися подальші оптимізації та додавання нових функцій, таких як: відображення історії ігор гравця, рейтинг найкращих гравців, додавання різних тем і т. д. Також було створено промо-ролик для залучення користувачів Телеграм до гри.

## Подальші оновлення
Завдяки цьому проекту було відкрито шлях до роботи з фреймворком [aiogram](https://docs.aiogram.dev/), створення бази даних за допомогою [SQLite](https://sqlite.org/), взаємодія між сервером та [Telegram](https://web.telegram.org/), та інші аспекти. На жаль, зараз проект не підтримується розробниками і не має сервера для роботи. Проте, все ж можна передбачити, що подальші кроки у розвитку проекту включатимуть створення гри "Шибениця" у формі [міні-додатка](https://core.telegram.org/bots/webapps) в Telegram, оптимізацію коду та поліпшення інтерфейсу бота.

