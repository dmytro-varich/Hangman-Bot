import random, codecs


def get_word(topic, language):
    if language == 'gb':
        return random.choice(open(f"{topic}_EN.txt", "r").readline().split()).lower()
    elif language == 'ua':
        return random.choice(codecs.open(f"{topic}_UA.txt", "r", encoding='utf-8').readline().split()).lower()


def get_daily_word():
    topic = random.choice(['Fauna', 'Flora', 'Science', 'Sports', 'Countries'])
    return random.choice(codecs.open(f"{topic}_EN.txt", "r", encoding='utf-8').readline().split()).lower()


def is_word_guessed(secret, letters_guessed):
    count = 0
    n = len(secret)

    for i in secret:
        for j in letters_guessed:
            if i == j:
                count += 1

    if n == count:
        return 1

    return 0


def get_guessed_word(secret, letters_guessed):
    guessed_word = ""
    for i in range(len(secret)):
        if secret[i] in letters_guessed:
            guessed_word += secret[i]
            guessed_word += " "
        else:
            guessed_word += "_ "

    return guessed_word


def get_available_letters(letters_guessed, language):
    if language == 'gb':
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        available_letters = ""
        for i in alphabet:
            if i not in letters_guessed:
                available_letters += i
    else:
        alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'"
        available_letters = ""
        for i in alphabet:
            if i not in letters_guessed:
                available_letters += i

    return available_letters