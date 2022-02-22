import requests
from bs4 import BeautifulSoup
import os

SUCCESS = 200
NUM_OF_WORDS = 1
NUM_OF_EXAMPLES = 1
FIRST_INDEX = 1
PATH = ""
WEB_BASE = 'https://context.reverso.net/translation/'
ALL_LANGUAGES = ["All", "Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese",
                 "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]


class Translator:

    src_language = None
    trg_language = None
    url = None
    path = None
    word = None
    word_list = None
    examples_list = None

    def __init__(self):

        print("Hello, you're welcome to the translator. Translator supports:")
        for i, each_language in enumerate(ALL_LANGUAGES):
            if i != 0:
                print(f"{i}. {each_language}")

    def display(self, num_of_words, num_of_examples):

        print(f'You chose "{self.trg_language}" as a language to translate "{self.word}".')
        print(f"\n{self.trg_language} Translations:\n")

        # Print translated words
        for word in self.word_list[:num_of_words]:
            print(word)

        print(f"\n{self.trg_language} Examples:\n")
        # Multiply by two come from source language and target language examples
        for index in range(0, num_of_examples * 2, 2):
            print(f'{self.examples_list[index]}\n{self.examples_list[index + 1]}\n\n')

    def write_to_file(self, path, num_of_words, num_of_examples):

        with open(path, 'a', encoding='utf-8') as f:
            f.write(f'You chose "{self.trg_language}" as a language to translate "{self.word}".\n')
            f.write(f"\n{self.trg_language} Translations:\n\n")
            # Write translated words
            for word in self.word_list[:num_of_words]:
                f.write(word + "\n")

            f.write(f"\n{self.trg_language} Examples:\n\n")
            # Multiply by two come from source language and target language examples
            for index in range(0, num_of_examples * 2, 2):
                f.write(f'{self.examples_list[index]}\n{self.examples_list[index + 1]}\n\n\n')

    def menu(self):

        self.src_language = ALL_LANGUAGES[int(input('Type the number of your language:'))]
        self.trg_language = ALL_LANGUAGES[int(input("Type the number of a language you "
                                                    "want to translate to or '0' to translate"
                                                    " to all languages:"))]
        self.word = input('Type the word you want to translate:')

    def build_url(self):

        self.url = WEB_BASE + f'{self.src_language}-{self.trg_language}/' + self.word
        self.url = self.url.lower()

    def scrap_answer(self, r):
        soup = BeautifulSoup(r.content, "html.parser")
        # Find all translated words by css id translations and tag a
        translation_words = soup.select("#translations-content a")
        self.word_list = [each_word.text.strip() for each_word in translation_words]
        # Find all examples by css id examples-content and class text
        translation_sentences = soup.select("#examples-content .text")
        self.examples_list = [sentence.text.strip() for sentence in translation_sentences]

    def translate_word(self):
        self.build_url()
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.url, headers=headers)
        if r.status_code == SUCCESS:
            self.scrap_answer(r)

    def build_path(self):
        self.path = os.path.join(os.getcwd(), self.word + ".txt")

    def translate(self):
        self.build_path()
        if self.trg_language == "All":
            for language in ALL_LANGUAGES[FIRST_INDEX:]:
                self.trg_language = language
                if self.trg_language != self.src_language:
                    self.translate_word()
                    self.display(NUM_OF_WORDS, NUM_OF_EXAMPLES)
                    self.write_to_file(self.path, NUM_OF_WORDS, NUM_OF_EXAMPLES)
        else:
            self.translate_word()
            self.display(NUM_OF_WORDS, NUM_OF_EXAMPLES)
            self.write_to_file(self.path, NUM_OF_WORDS, NUM_OF_EXAMPLES)

    def start(self):
        self.menu()
        self.translate()


if __name__ == '__main__':

    translator = Translator()
    translator.start()
