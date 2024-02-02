from socket import *
import argparse
import dns.resolver

def nameservers(domain):
    names = dns.resolver.resolve(domain, 'NS')
    nameservers = [(str(name), dnslookup(str(name))) for name in names]
    
    for ns in nameservers: print(ns[0], ns[1])

def dnslookup(hostname):
    return gethostbyname(hostname)

def reversednslookup(ip):
    return gethostbyaddr(ip)[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dnslookup')
    parser.add_argument('-d', type=str, dest='domain', help='takes domain name www.google.com')
    parser.add_argument('-ip', type=str, dest='IP', help='takes IP address 8.8.8.8')
    parser.add_argument('-ns', type=str, dest='NS', help='takes domain www.google.com')
    options = parser.parse_args()
    
    try:
        if options.domain: print(dnslookup(options.domain))
        if options.IP: print(reversednslookup(options.IP))
        if options.NS: nameservers(options.NS)
    except:
        raise ValueError('please enter correct value')