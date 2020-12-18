from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

def get_camelot(title, artist):
    #driver = webdriver.Firefox()
    title = title.replace('(', '')
    title = title.replace(')', '')
    title = title.replace(',', ', ')
    link = 'https://tunebat.com/Search?q=' + title.replace(' ', '+') + '+' + artist.replace(' ', '+')
    print(link)

    req = urllib.request.Request(link, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)

    #driver.get(link)
    camelots = ['>1A<', '>1B<', '>2A<', '>2B<', '>3A<', '>3B<', '>4A<', '>4B<', '>5A<', '>5B<', '>6A<', '>6B<', '>7A<',
                '>7B<', '>8A<', '>8B<', '>9A<', '>9B<', '>10A<', '>10B<', '>11A<', '>11B<', '>12A<', '>12B<']
    #content = driver.page_source
    soup = BeautifulSoup(con, features="html.parser")
    #print(soup)
    for a in soup.find_all('a'):
        for char in camelots:
            if(char in str(a)):
                print(char[1:3])
                return char[1:3]