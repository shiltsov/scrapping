import requests
import os
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

base_dir = '/home/sda/AI-WORK/scrapping/data'
not_essantial_external = ['wa.me','facebook.com', 'www.facebook.com','instagram.com','vk.com']

int_url = set()
ext_url = set()

def prepare_content(text):
    # на входе - содержимое html файла, на выходе - готовую пхп-шку
    #
    #
    return text


def valid_url(url):
    parsed = urlparse(url)
    if parsed.scheme in ['skype','tel','whatsapp']:
        return False
    return bool(parsed.netloc) and bool(parsed.scheme)

def website_links(url):
    # если мы сюда попали с каким-то url - то это хороший валидный урл по которому надо делать файл index.php
    # других у нас нет - у нас что не адрес то папка

    print(f'---- current url {url} ----')
    urls = set()

    url_parsed  = urlparse(url)

    file_path = url_parsed.path
    domain_name = url_parsed.netloc

    if file_path.startswith('/'):
        file_path = file_path[1:]

    dir_name = os.path.join(base_dir, file_path)
    print('base:', base_dir, 'fp:', file_path,  'dirname:', dir_name)

    if not os.path.exists(dir_name):
        print('path:', dir_name)
        os.makedirs(dir_name)

    content = requests.get(url)

    with open(os.path.join(base_dir, file_path, 'index.php'), 'w+') as fp:
        fp.write(prepare_content(content.text))

    soup = BeautifulSoup(content.text, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        # если есть #new или ссылка пустая и тп - ее не добавляем в список просмотра
        if href in ["","#"] or href is None:
            continue 
        
        href = urljoin(url, href)   

        if href[-3:].lower() in ['jpg','png','gif','avi','mov','peg']:
            continue

        if not valid_url(href) or href in int_url:
            continue

        if domain_name not in href:
            # внешняя ссылка
            if href not in ext_url:
                link_domain = urlparse(href).netloc
                if link_domain in not_essantial_external:
                    continue
                print(f"[!] External link: {href}, url: {url}")
                ext_url.add((href,url))
            continue

        
        # не хотим добавлять если такая уже есть без учета фрагмента
        if urlparse(href).fragment != '':
            href = href.split('#')[0]
            if href in urls:
                continue

        if href not in urls:
            print('добавляем: ', href)
            urls.add(href)
            int_url.add(href)

    return urls

visited_urls = []
visited_urls_count = 0

def crawl(url, max_urls=50000):
    global visited_urls_count
    visited_urls_count += 1
    links = website_links(url)
    for link in links:
        if visited_urls_count > max_urls:
            break
        if link in visited_urls:
            continue
        visited_urls.append(link)
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    crawl("http://dublikatnomera.com")
    print("[+] Total External links:", len(ext_url))
    print("[+] Total Internal links:", len(int_url))
    print("[+] Total:", len(ext_url) + len(int_url))
    
    for acceptor, donor in ext_url:
        print(acceptor, ' : ', donor)

    print("----------------------------------------------")


