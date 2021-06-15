from urllib.parse import urljoin, urlparse, urlsplit
import os

# print(urljoin('https://medestetik.ru/1/', 'index.php'))
url = "https://www.medestetik.ru:8000/faq/topic.php;12?page=10&a=23"

print(urlparse(url).fragment == '')
print(urlsplit(url))
print(urlparse(url, allow_fragments=False).geturl())

#u1 = 'http://www.mgido.ru/abc/'
#u2 = '/ino/smi/1.php'

#print(urljoin(u1, u2))

print(os.path.join('data','index.php'))