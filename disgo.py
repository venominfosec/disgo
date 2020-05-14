#!/usr/bin/env python3

# DISGO - DIcks Sporting Goods Online detector

# Imports
import sys
import requests
import time
import cfscrape
import datetime
import json
import argparse
import re
import getpass
from gmail import GMail, Message


# Global variables
FILE = 'disgo_log.txt'


# Main function
def main(target, time_delay, method, target_email, source_email, password):

    # Run
    while True:
        log(str('Trying '+str(target)))
        if isAvailable(target, method):
            log(str('Site online! Sending email to '+target_email))
            if alert(target, target_email, source_email, password):
                log(str('Email sent to '+target_email))
            else:
                log(str('Exception while sending email, check logs'))
            time.sleep(time_delay*60)
        else:
            log(str('Site unchanged, sleeping for '+str(time_delay)+' minutes'))
            time.sleep(time_delay*60)


# Test if site has changed
def isAvailable(target, method):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Upgrade-Insecure-Requests': '1',
                'Connection': 'close' }
    try:
        # GUI method
        if method == 'gui':
            scraper = cfscrape.create_scraper()
            req = scraper.get(target)
            result = str(req.content)[2:-1]
            if 're looking for is not available at this time' in result:
                return False
            elif req.status_code == 503:
                return False
            else:
                return True

        # API method
        elif method == 'api':
            scraper = cfscrape.create_scraper()
            req = scraper.get(target, headers=headers)
            result = str(req.content)[2:-1]
            log(str('API Results: '+str(result)))
            product_results = []
            try:
                parsed = json.loads(result)
                for item in parsed['data']['results']:
                    product_results.append(str(item))
            except json.decoder.JSONDecodeError:
                string_result = result.split('"results":')[1]
                string_result = string_result.split('}}')[0]
                product_results = list(string_result[1:-1])
            if product_results:
                return True
            else:
                return False
    except Exception as e:
        log(str('WEB REQUEST ERROR:'+str(e)))
        log(str('Exception while requesting website, check logs'))
        return False


# Send email that site has changed
def alert(target, target_email, source_email, password):
    email_body = "Dicks Sporting Goods - Product Available\n"+str(target)
    try:
        gmail = GMail('Product Available <'+source_email+'>', password)
        msg = Message('[!] Dick\'s Sporting Goods Product Available!', to='<'+target_email+'>', text=email_body)
        gmail.send(msg)
        return True
    except Exception as e:
        log(str('EMAIL ERROR:'+str(e)))
        return False


# Print and log message
def log(string):
    now = str(datetime.datetime.now())
    string = now+' : '+str(string)
    print(string)
    try:
        with open(FILE,'a') as output:
            output.write('\n'+str(string))
    except:
        print('[!] Unable to write log to file '+str(FILE))


# Configure and launch program
if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Detect if a product is available at Dick\'s Sporting Goods')
    parser.add_argument('target', help='Full GUI URL or if API, comma separated SKU and zip code (eg: 11465449,10001')
    parser.add_argument('-t', '--time-delay', help='Minutes to wait before rechecking if product is available, default = 5')
    parser.add_argument('-m', '--detect-method', help='Detection method to use if product is available, options: api, gui', required=True)
    parser.add_argument('-te', '--target-email', help='Email to send notifications to if product is online', required=True)
    parser.add_argument('-se', '--source-email', help='Gmail account to send notification from', required=True)
    parser.add_argument('-o', '--output', help='File to log results to, default = dsgo_log.txt')
    parser.add_argument('--insecure', help='Insecurely provide the Gmail account password as an argument')
    args = parser.parse_args()
    arg_target= args.target
    arg_time = args.time_delay
    arg_method = args.detect_method
    arg_target_email = args.target_email
    arg_source_email = args.source_email
    arg_output = args.output
    arg_insecure = args.insecure
    arg_password = ''

    # Validate arguments
    ## Time dealy
    if not arg_time:
        arg_time = 5
    else:
        try:
            arg_time = int(arg_time)
        except ValueError:
            print('[!] ERROR: value for time delay parameter must be an integer')
            sys.exit()
    ## Method and target
    valid_methods = ['api', 'gui']
    arg_method = str(arg_method).lower()
    if arg_method not in valid_methods:
        print('[!] Detection method "'+arg_method+'" is not a valid method. Options: '+str(valid_methods))
        sys.exit()
    if arg_method == 'api':
        sku = ''
        zip_code = ''
        try:
            sku = str(arg_target.split(',')[0])
            zip_code = str(arg_target.split(',')[1])
        except IndexError:
            print('[!] ERROR: Invalid API target format provided: '+zip_code)
            print('[*] Valid comma seperated target format example (sku,zip_code): 11465449,10001')
            sys.exit()
        if len(zip_code) is not 5:
            print('[!] ERROR: Invalid zip code "'+zip_code+'" provided')
            sys.exit()
        arg_target = 'https://availability.dickssportinggoods.com/ws/v2/omni/stores?addr='+zip_code+'&radius=100&uom=imperial&lob=dsg&sku='+sku+'&res=locatorsearch&qty=1'
    elif arg_method == 'gui':
        if 'dickssportinggoods.com' not in arg_target:
            print('[!] ERROR: Invalid URL target provided: '+arg_target)
            print('[*] Valid target example: https://www.dickssportinggoods.com/p/bowflex-selecttech-552-dumbbells-16bfxuslcttchdmbbslc/16bfxuslcttchdmbbslc')
            sys.exit()
    ## Output
    if not arg_output:
        arg_output = FILE
    else:
        if not re.match(r'[a-zA-Z0-9_-]+\.\w+', arg_output):
            print('[!] ERROR: Illegal file name provided')
            sys.exit()
    ## Emails
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", arg_target_email):
        print('[!] WARNING: Target email does not match regex pattern. Check input for typos.')
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", arg_source_email):
        print('[!] WARNING: Source email does not match regex pattern. Check input for typos.')
    if 'gmail' not in arg_source_email.lower():
        print('[!] ERROR: "'+arg_source_email+'" is not a Gmail address. A Gmail account required to send email through this script.')
        sys.exit()
    ## Source email password
    if arg_insecure:
        print('[!] WARNING: Insecure password argument specified. Password may be locally logged.\n')
        arg_password = arg_insecure
    else:
        arg_password = getpass.getpass(prompt='[+] Enter password for Gmail account to send email from: ')

    # Run program
    FILE = arg_output
    main(arg_target, arg_time, arg_method, arg_target_email, arg_source_email, arg_password)
