import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import GermanStemmer

from lib.Tokenizer import Tokenizer

#nltk.data.path.append('./nltk')
#nltk.download('punkt', download_dir="./nltk")
#nltk.download('wordnet', download_dir="./nltk")

#stemmer = LancasterStemmer()
stemmer = GermanStemmer()

sentences = ["Dies ist ein Test Satz in deusch!", "ein einer eine einiges", "der die das", "wer wie was wieso wesshalb"]

sentences.append("Hallo ich bin ein Text.")
sentences.append("Hi, wie geht es?")
sentences.append("Programme")
sentences.append("Program")
sentences.append("Programierer")
sentences.append("Programiererin")
sentences.append("Text text texte texten")
#\nThis is an english sentences with some interesting things and stuff.\nsentence sentences "


print(sentences)

# tokenizer = Tokenizer()
#
# for sentence in sentences:
#     tokens = tokenizer.classify(sentences)
#     print (tokens)
#
# re_sentence = tokenizer.get_value(tokens)
# print(re_sentence)
#
# print(tokenizer.get_full_lenght_array())
# print(tokenizer.get_data_size())
#
# print(tokenizer.sentence_to_1hot("ein Test"))
# print(tokenizer.sentence_to_1hot("Test"))
# print(tokenizer.sentence_to_1hot("zweiter Test"))


for sentence in sentences:
    print('normal:', sentence)
    stemmed = stemmer.stem(sentence)
    print('stemmed:', stemmed)
    print()
