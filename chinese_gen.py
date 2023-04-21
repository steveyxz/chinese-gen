from clipboard import copy
from pinyin import *
from translate import Translator

# Chinese class text generator

# Commands:
# section <pronouce-ways>
# cpy-word
# cpy-section

SECTION_COMMAND = "section"
COPY_WORD_COMMAND = "cpy-word"
COPY_SECTION_COMMAND = "cpy-section"
PRINT_WORD_CACHE_COMMAND = "wcache"

last_section = ""

word_cache = []
translator = Translator('en', 'zh')

command = input("Enter command: ")

while command:
    parts = command.split()
    if parts[0] == SECTION_COMMAND:
        last_section = ""
        # Start section wizard
        start_line = ""
        subsections = []
        chinese_word = input("Type the chinese word: ")
        start_line += chinese_word
        start_line += " - ("
        pinyins = []
        pronounciation_ways = int(input("How many ways are there to pronounce this word? "))
        for i in range(pronounciation_ways):
            print(f"Starting section {i}!")
            old_pinyin = None
            word_pinyin = get(chinese_word, delimiter=' ')
            if input(f"Is \'{word_pinyin}\' the right way to pronouce the word (y/n): ") == "n":
                old_pinyin = word_pinyin
                word_pinyin = input("Please give the right pronounciation: ")
            pinyins.append(word_pinyin)

            subsection = ""
            # Start inputting phrases
            print("Now we will begin inputting phrases!")
            phrase = input("Enter a phrase with the word: ")
            while phrase:
                subsection += phrase
                subsection += " - ("
                phrase_pinyin = get(phrase, delimiter=' ')
                if old_pinyin is not None:
                    phrase_pinyin = phrase_pinyin.replace(old_pinyin, word_pinyin)
                if input(f"Is \'{phrase_pinyin}\' the right way to pronouce the phrase (y/n): ") == "n":
                    phrase_pinyin = input("Please give the right pronounciation: ")
                subsection += phrase_pinyin
                subsection += ") - "
                phrase_translation = translator.translate(phrase)
                if input(f"Is \'{phrase_translation}\' the right translation of the word (y/n): ") == "n":
                    phrase_translation = input("Please give the right definition: ")
                subsection += phrase_translation.lower()
                subsection += "\n"
                print("Successfully added phrase!")
                phrase = input("Enter another phrase with the word: ")
            subsections.append(subsection)
        start_line += " / ".join(pinyins)
        start_line += ")\n\n"
        last_section += start_line
        last_section += "\n".join(subsections)
        word_cache.append(chinese_word)
        print("Successfully completed section! [Copied to clipboard]")
        copy(last_section)
    elif parts[0] == COPY_SECTION_COMMAND:
        # Copy the last section generated
        if last_section == "":
            print("There has been no sections generated so far!")
        copy(last_section)
        print("Copied last section generated to clipboard!")
        print(last_section)
    elif parts[0] == COPY_WORD_COMMAND:
        # Copy the last word used
        if len(word_cache) == 0:
            print("There has been no words!")
        copy(word_cache[-1])
        print(f"Copied last word used to clipboard ({word_cache[-1]})")
    elif parts[0] == PRINT_WORD_CACHE_COMMAND:
        # Print the entire word list in this session
        print("Here is a list of all the words you have used in this session!")
        for word in word_cache:
            print(word)
    else:
        print("Invalid command!")
        print(f"Possible commands are: {SECTION_COMMAND}, {COPY_SECTION_COMMAND}, {COPY_WORD_COMMAND}, {PRINT_WORD_CACHE_COMMAND}!")
    command = input("Enter command: ")