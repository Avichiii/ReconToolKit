from urllib.error import HTTPError
import urllib.request, urllib.parse
import argparse
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = None
ctx.verify_mode = ssl.CERT_NONE

class Scanner(object):
    def __init__(self, options) -> None:
        self.url = options.url
        self.wordlistpath = options.wordlist
        self.depth = options.depth
        self.valids = []
        self.redirected = []

    def start(self):
        self.wordlist = self.fileio()
        for route in self.wordlist:
            currenturl = f'{self.url}/{route}'
            self.scan(currenturl)
        
        if self.depth > 1 and self.valids != []:
            self.dirdepth()
        
    def scan(self, url):
        try:
            response = urllib.request.urlopen(url, context=ctx)
            if response.getcode() == 200: 
                self.valids.append(url)
                print(f'{url} 200')
            elif response.getcode() == 301:
                self.redirected.append(url)
        
        except HTTPError:
            pass
    
    def fileio(self) -> list:
        with open(self.wordlistpath) as endpoints:
            endpoints = [endpoint.strip('\n') for endpoint in endpoints.readlines()]
            return endpoints
    
    def dirdepth(self):
        for url in self.valids:
            for route in self.wordlist:
                url = f'{url}/{route}'
                self.scan(url)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dirb - a wed directory finder')
    parser.add_argument('-u', type=str, dest='url', help='takes domain name www.google.com')
    parser.add_argument('-w', type=str, dest='wordlist', help='wordlist path')
    parser.add_argument('-depth', type=int, default=1, dest='depth', help='takes int number ex. 2')
    options = parser.parse_args()
    
    try:
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            dirb = Scanner(options)
            dirb.start()
    except ValueError:
        print("please enter the correct values!")

    except KeyboardInterrupt:
        exit(0)
        
    