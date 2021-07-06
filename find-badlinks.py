import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


int_url = set()
ext_url = set()

def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def website_links(url):
    urls = set()
    # извлекаем доменное имя из URL
    domain_name = urlparse(url).netloc
    # скачиваем HTML-контент вэб-страницы
    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href пустой тег
            continue 

        href = urljoin(url, href)   
        if not valid_url(href):
            # недействительный URL
            continue
        if href in int_url:
            # уже в наборе
            continue
        if domain_name not in href:
            # внешняя ссылка
            if href not in ext_url:
                print(f"[!] External link: {href}")
                ext_url.add(href)
            continue
        #print(f"[*] Internal link: {href}")
        urls.add(href)
        int_url.add(href)
    return urls


# Количество посещенных URL-адресов
visited_urls = 0
# Просматриваем веб-страницу и извлекаем все ссылки.
def crawl(url, max_urls=5000):
    # max_urls (int): количество макс. URL для сканирования
    global visited_urls
    visited_urls += 1
    links = website_links(url)
    for link in links:
        if visited_urls > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    crawl("https://medestetik.ru")
    print("[+] Total External links:", len(ext_url))
    print("[+] Total Internal links:", len(int_url))
    print("[+] Total:", len(ext_url) + len(int_url))
    print(ext_url)