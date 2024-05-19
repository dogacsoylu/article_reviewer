from bs4 import BeautifulSoup
import requests
import nltk
import PyPDF2
import io
from functools import reduce
from nltk.tokenize import sent_tokenize
import operator


def count_syllables(word):
    count = 0
    vowels = ["a","e","ı","i","o","ö","u","ü"]
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index -1] not in vowels:
            count += 1
    return count        

def count_total_syllables(text):
    text = text.split()
    cnt = 0
    for word in text:
        cnt += count_syllables(word)
    total_syllables = cnt
    return cnt

def extract_text_from_pdf(url):
    response = requests.get(url)
    pdf_file_obj = io.BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    return text

URL = input("Enter the URL of the article that you want us to review: ")

#Gereksiz sözcük yüzdesi
gereksiz_sozcuk = ["ve","Ve","veya","Veya", "fakat","Fakat", "ancak","Ancak", "veyahut","Veyahut", "gibi","Gibi", "ile", "ne","Ne",
                    "ya","Ya", "hem","Hem", "İse","ise", "oysa", "Oysa","yani", "Yani","eğer", "Eğer", "dahi", "Dahi", "çünkü", "Çünkü", "madem", "Madem",
                      "zira", "Zira", "şartıyla", "kadar", "Sanki", "sanki", "Daha", "daha", "Halbuki", "halbuki", "Lakin", "lakin", "Mesela", "mesela", "Hatta",
                        "hatta"]
gereksiz_sozcuk_sayisi = 0

text = extract_text_from_pdf(URL)
text_unsplit = text
text = text.split()

for word in gereksiz_sozcuk:
    if word in text:
        count = text.count(word)
        gereksiz_sozcuk_sayisi += count

print(gereksiz_sozcuk_sayisi)
print("Gereksiz Sözcük Yüzdesi: ", (gereksiz_sozcuk_sayisi / len(text)) * 100)



#Kendini Tekrarlama İndeksi (Aynı kelime indeksi) (formül = (Wx * Wx+1  * .... * Wx+n-1) / (Wtot * len(words)) )
endeks_arrayi = [0] * len(text)
words = [0] * len(text)
i = 0

for word in text:
    if word in words:
        continue

    words[i] = word
    count = text.count(word)
    endeks_arrayi[i] = count
    i += 1

words = [x for x in words if x!= 0]
endeks_arrayi = [x for x in endeks_arrayi if x!= 0]
product = 0
sum = 0

for a in endeks_arrayi:
    product += endeks_arrayi[a] ** 2
    sum += endeks_arrayi[a]

indeks = (product) / (sum * len(words)) #indeks ne kadar yüksekse tekrarlama o kadar fazladır
#print(endeks_arrayi)
#print(product)
#print(sum)
print("Tekrarlama İndeksi:",indeks*100)


#Length of the article and avg. reading time (avg. 238 wpm)
length = len(text)
mins = length / 238
print("Average Reading Time:", mins, "minutes")



#Öznellik Yüzdesi
cnt = 0
oznel_kelimeler = ["bence", "bizce", "sanırım", "düşünüyorum", "kanımca", "inanıyorum", "tahminen", "muhtemelen"]
for word in oznel_kelimeler:
    cnt += text.count(word)
yuzde = (cnt / len(text)) * 100
print("Öznellik yüzdesi:",yuzde)


#Flesch-Kincaid readability index = 206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)

total_syllables = count_total_syllables(text_unsplit)
total_words = len(text)
sentences = sent_tokenize(text_unsplit)
total_sentences = len(sentences)

#print(total_sentences,total_words,total_syllables)
print("Flesch-Kincaid Readability Index:", 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words))

