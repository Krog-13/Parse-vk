import requests
from bs4 import BeautifulSoup as BS
import _csv
'''
script for https://vk.com/@yvkurse, paring it
and save file in .csv format with data (itle;article text;images url) 
'''

#count = 0
#scraping of articles
response = requests.get('https://vk.com/@yvkurse')
html = BS(response.content, 'html.parser')

#links to articles
articles = [str(i['href'])[9:str(i['href']).index('?')] for i in html.find_all('a', class_=('author-page-article__href'),href=True)]
page_of_articles = []

#create a list all of urls
for article in articles:
    page_of_articles.append(requests.get('https://vk.com/@yvkurse' + article))

data_articles = [[] for _ in range(len(page_of_articles))] # create empty list


def head_article(article, count:int):
    """
    :param article: html page of article
    :param count: article number
    data_article adding 'article title'
    """
    data_articles[count].append(article.select('.article > h1')[0].text)


def text_article(article, count:int):
    '''
    :param article: html page of article
    :param count: article number
    data_article adding 'article text'
    '''
    text = ''
    all_text = article.find_all('p', class_='article_decoration_first article_decoration_last article_decoration_before')
    for line in all_text:
        text += line.text
    data_articles[count].append(text)


def img_article(article, count:int):
    """
    :param article: html page of article
    :param count: article number
    data_article adding 'links to pictures in the article'
    """
    images = ','.join([str(i['src']) for i in article.find_all('img', class_=('article_object_sizer_inner'), src=True)])
    data_articles[count].append(images)


def main():
    """
        start script
    """
    count = 0 #
    # Проверка на наличие страниц
    try:
        if not page_of_articles:
            print('Стати не найдены!!!')
    except:
        print('Something wrong')

    for regular_article in page_of_articles:
        one_article = BS(regular_article.content, 'html.parser')
        #add head
        head_article(one_article, count)

        #add text of article
        text_article(one_article, count)

        #add link of images
        img_article(one_article, count)
        count += 1

if __name__ == '__main__':
    with open('DATA_articles.csv', 'w', newline='') as file:
        """
        create .csv file 
        with data of https://vk.com/@yvkurse 
        """
        main()#start parse
        add_article = _csv.writer(file, delimiter=';')
        for line in data_articles:
            add_article.writerow(line)
