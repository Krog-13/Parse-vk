import requests
from bs4 import BeautifulSoup as BS
import _csv


count = 0

#scraping of articles
response = requests.get('https://vk.com/@yvkurse')
html = BS(response.content, 'html')
print(html)
#links to articles
articles = [str(i['href'])[9:str(i['href']).index('?')] for i in html.find_all('a', class_=('author-page-article__href'),href=True)]
page_of_articles = []
for article in articles:
    page_of_articles.append(requests.get('https://vk.com/@yvkurse' + article))

data_articles = [[] for _ in range(len(page_of_articles))]


def head_article(article, count:int):

    data_articles[count].append(article.select('.article > h1')[0].text)


def text_article(article, count:int):

    text = ''
    all_text = article.find_all('p', class_='article_decoration_first article_decoration_last article_decoration_before')
    for line in all_text:
        text += line.text
    data_articles[count].append(text)


def img_article(article, count:int):

    images = ','.join([str(i['src']) for i in article.find_all('img', class_=('article_object_sizer_inner'), src=True)])
    data_articles[count].append(images)


for regular_article in page_of_articles:

    one_article = BS(regular_article.content, 'html.parser')
    #add head
    head_article(one_article, count)

    #add text of article
    text_article(one_article, count)

    #add link of images
    img_article(one_article, count)
    count += 1

with open('DATA_articles.csv', 'w', newline='') as file:
    add_article = _csv.writer(file, delimiter=';')
    for line in data_articles:
        add_article.writerow(line)




