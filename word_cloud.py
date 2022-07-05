# import google
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request as url
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

language = input("\n\nEnter the language of the word cloud (default en): ")

language = language.lower() if language else "en"

query = input('\n\nEntrez votre recherche: ')

excludes = []

results = search(query=query, tld='com', lang=language,
                 num=10, start=0, stop=20, pause=2.0)

web_content_cleaned_all = []

for url_link in results:
    try:
        print(url_link, " ....Processing", end=' ')
        url_content = url.urlopen(url_link).read()
        text_content = BeautifulSoup(url_content, "lxml").text
        text_content = [val.lower() for val in text_content.split(
            ' ') if val.isalpha() or val.isnumeric()]
        web_content_cleaned_all.extend(text_content)
        print(" Read ✅")
    except:
        print(" Failed ❌")

lemmatizer = WordNetLemmatizer()
qry_words = query.lower().split(
    ' ') + [lemmatizer.lemmatize(w) for w in query.lower().split(' ')]
stop_words = list(set(stopwords.words('french' if language ==
                  'fr' else 'english'))) + qry_words + excludes

if language == "fr":
    web_content_cleaned_final = [
        word for word in web_content_cleaned_all if word not in stop_words]
else:
    web_content_cleaned_final = [lemmatizer.lemmatize(
        word) for word in web_content_cleaned_all if word not in stop_words]

print("Generating Word Cloud..")
text_final = ' '.join(web_content_cleaned_final)
wordcloud = WordCloud(max_font_size=100, max_words=100,
                      background_color="white", random_state=0).generate(text_final)
plt.figure(figsize=(12, 10))
wordcloud = plt.imshow(wordcloud, interpolation="bilinear")
plt.title(query+'\n', size=20)
plt.axis("off")

plt.show()
