import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
# Create your views here.


def brefani(request, url):
    url = "https://aninews.in/"+url+"/"
    print(url)
    news = {}
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    details = soup.find('div', id="news-detail-block")
    if details is not None:
        
        if details.find('h1', class_="title") is not None:
            news["header"] = details.find(
                'h1', class_="title", itemprop="headline").text

        if details.find(class_="time-red", itemprop="dateModified") is not None:
            news["time"] = details.find(
                class_="time-red", itemprop="dateModified").text
        if details.find('div', itemprop="articleBody") is not None:
            news["content"] = details.find('div', itemprop="articleBody").text

    json_data = json.dumps(news)
    return HttpResponse(json_data)



def ani(request, sub, pageno):
    url = "https://aninews.in/category/" + sub
    if pageno == 0:
        url = url
    else:
        url = url+"page/"+(pageno)+"/"
        print(url)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    mainnews = soup.find_all('div', class_='col-xs-12')
    time = "notfound"
    heading = "notfound"
    content = "notfound"
    imgurl = "notfound"
    readmore = "notfound"
    data = {}
    list = []
    for i in mainnews:
        header = i.find('header')
        article = i.find('article')

        if article is not None:
            if article.find(class_='time-red') is not None:
                time = article.find(class_='time-red').text
            if article.find(class_='title') is not None:
                heading = article.find(class_='title').text

            if article.find_all('p') is not None:
                contentl = article.find_all(class_='content')
                for k in contentl:
                    if k.find('p', class_='time') is not None:
                        pass
                    else:
                        if k.find('p') is not None:
                            content = k.find('p').text
            if article.find(class_='read-more') is not None:
                readmore = article.find(class_='read-more').get('href')

            if header is not None:
                if header.find(class_='img-container') is not None:
                    if header.find(class_='img-container').find('img') is not None:
                        imgurl = header.find(
                            class_='img-container').find('img').get('data-src')

            data["time"] = time
            data["heading"] = heading
            data["short"] = content
            data["imgurl"] = imgurl
            data["url"] = readmore
            json_data = json.dumps(data)
            list.append(json_data)

            # print(time, "\n"+heading+"\n"+content+"\n"+imgurl+"\n"+readmore)

    extrarelated = soup.find_all('div', class_='extra-related-block')

    for m in extrarelated:
        figcaption = m.find("figcaption")
        figure = m.find('figure')

        if figcaption is not None:
            if figcaption.find(class_='time-red') is not None:
                time = figcaption.find(class_='time-red').text
            if figcaption.find(class_='title') is not None:
                heading = figcaption.find(class_='title').text
            if figcaption.find_all('p') is not None:
                for n in figcaption.find_all('p'):
                    if figcaption.find('p', class_='text-small') is not None:
                        pass
                    else:
                        if n.text != "":
                            content = n.text

            if figcaption.find(class_='read-more') is not None:
                readmore = figcaption.find(class_='read-more').get('href')

            if figure is not None:
                if figure.find(class_='img-container') is not None:
                    imgurl = figure.find(
                        class_='img-container').find('img').get('data-src')

            # if figure is not None:
                    data["time"] = time
            data["heading"] = heading
            data["short"] = content
            data["imgurl"] = imgurl
            data["url"] = readmore
            json_data = json.dumps(data)
            list.append(json_data)
    return HttpResponse(list)
