from urllib.error import HTTPError
import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = None
ctx.verify_mode = ssl.CERT_NONE


def responseHeader(url):
    content = main(url)
    for (header, value) in content.info().items(): 
        print(f'{header}: {value}')

def main(url):
    try:
        content = urllib.request.urlopen(url, context=ctx)
        return content
    except HTTPError:
        print(f'{url} does\'nt let us curl')
        exit(0)

def htmlBody(url):
    content = main(url)
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

def headerBody(url):
    responseHeader(url)
    print('')
    htmlBody(url)

if __name__ == "__main__":
    args = len(sys.argv)
    
    if args == 1:
        print('''usage: curl.py <url> --head\nex.\n curl.py example.com --head\n curl.py example.com --nobody\n\n --head  - includes both header and body\n --nobody  - only includes header''')
        
    if args > 1 and args < 4:
        if args == 2:
            htmlBody(sys.argv[1])
        elif args == 3 and sys.argv[2] == '--head':
            headerBody(sys.argv[1])
        elif args == 3 and sys.argv[2] == '--nobody':
            responseHeader(sys.argv[1])
