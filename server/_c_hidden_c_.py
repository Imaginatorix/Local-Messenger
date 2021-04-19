entry_pass = "Thank you for telling me\n"
pm_code = "Private_Message?Whisper?\n"
show_people_code = "Peeps\n"
pm_error_code = "Oops! No Person With That Name Was Found!\n"
owner_tag = "[SERVER]"

def encryptor(word):
    # Modified Caesar's Wheel Encryption
    turn = 13
    
    alpha_num = {
        0: "Z",
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
        8: "H",
        9: "I",
        10: "J", 
        11: "K",
        12: "L",
        13: "M",
        14: "N",
        15: "O",
        16: "P",
        17: "Q",
        18: "R",
        19: "S",
        20: "T",
        21: "U",
        22: "V",
        23: "W",
        24: "X",
        25: "Y"
    }

    origplace = []
    newplace = []
    qeuedforword = []
    symbols = []
    newword = ""

    oppodic = lambda dic, val : (values for values, key in dic.items() if key == val)

    for letter in word:
        if letter.isalpha():
            letter = letter.upper()
            for key in oppodic(alpha_num, letter):
                origplace.append(key)
        else:
            symbols.append(letter)

    for places in origplace:
        newplaces = places + turn
        newplaces = newplaces % 26
        newplace.append(newplaces)

    for newplaces in newplace:
        newletters = alpha_num[newplaces]
        qeuedforword.append(newletters)

    letter_place = 0
    symbol_place = 0
    for letter in word:
        if letter.isalpha():
            if letter.islower():
                newword += qeuedforword[letter_place].lower()
            else:
                newword += qeuedforword[letter_place]
            letter_place += 1
        else:
            newword += symbols[symbol_place]
            symbol_place += 1

    return (newword)

def decryptor(word):
    turn = 13
    
    alpha_num = {
        0: "Z",
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
        8: "H",
        9: "I",
        10: "J", 
        11: "K",
        12: "L",
        13: "M",
        14: "N",
        15: "O",
        16: "P",
        17: "Q",
        18: "R",
        19: "S",
        20: "T",
        21: "U",
        22: "V",
        23: "W",
        24: "X",
        25: "Y"
    }

    origplace = []
    newplace = []
    qeuedforword = []
    symbols = []
    newword = ""

    oppodic = lambda dic, val : (values for values, key in dic.items() if key == val)

    for letter in word:
        if letter.isalpha():
            letter = letter.upper()
            for key in oppodic(alpha_num, letter):
                origplace.append(key)
        else:
            symbols.append(letter)

    for places in origplace:
        newplaces = places - turn
        newplaces = newplaces % 26
        newplace.append(newplaces)

    for newplaces in newplace:
        newletters = alpha_num[newplaces]
        qeuedforword.append(newletters)

    letter_place = 0
    symbol_place = 0
    for letter in word:
        if letter.isalpha():
            if letter.islower():
                newword += qeuedforword[letter_place].lower()
            else:
                newword += qeuedforword[letter_place]
            letter_place += 1
        else:
            newword += symbols[symbol_place]
            symbol_place += 1

    return (newword)

def encrypt(word):
    return encryptor(word)

def decrypt(word):
    return encryptor(word)

searcher_name = encrypt("The Probe Searcher Name")













