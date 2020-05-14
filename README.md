# DISGO - DIcks Sporting Goods Online detector
Get notified when a product is available at Dick's Sporting Goods

## Purpose
* Monitor if a product sold by Dick's Sporting Goods is available online
* If the product is available, send an email notification from a Gmail account you own

## Why? Dick's notifies me when a product is in stock
This script notifies you earlier. Using the API or the API and GUI methods together will produce a notification quicker than one originating from Dick's.

## Setup
### Clone the repository & install dependencies
```
git clone https://github.com/venominfosec/disgo.git
cd disgo && pip3 install -r requirements.txt
python3 disgo.py -h
```
### Create & configure the source Gmail account
* DISGO uses Gmail to send email notifications that a product is available
* Configure the Gmail account to use smtplib (plaintext smtp) as [outlined in this Google help article](https://support.google.com/accounts/answer/6010255)
* It is recommended to use a new Gmail account just for running this script

### Run the script
API: `python3 disgo.py -m api -te example@example.com -se gmail@gmail.com -o api_log.txt 17444005,55404`

GUI: `python3 disgo.py -m gui -te example@example.com -se gmail@gmail.com -o gui_log.txt "https://www.dickssportinggoods.com/p/bowflex-selecttech-552-dumbbells-16bfxuslcttchdmbbslc/16bfxuslcttchdmbbslc"`

## Usage
```
# python disgo.py -h
usage: disgo.py [-h] [-t TIME_DELAY] -m DETECT_METHOD -te TARGET_EMAIL -se
                SOURCE_EMAIL [-o OUTPUT] [--insecure INSECURE]
                target

Detect if a product is available at Dick's Sporting Goods

positional arguments:
  target                Full GUI URL or if API, comma separated SKU and zip
                        code (eg: 11465449,10001

optional arguments:
  -h, --help            show this help message and exit
  -t TIME_DELAY, --time-delay TIME_DELAY
                        Minutes to wait before rechecking if product is
                        available, default = 5
  -m DETECT_METHOD, --detect-method DETECT_METHOD
                        Detection method to use if product is available,
                        options: api, gui
  -te TARGET_EMAIL, --target-email TARGET_EMAIL
                        Email to send notifications to if product is online
  -se SOURCE_EMAIL, --source-email SOURCE_EMAIL
                        Gmail account to send notification from
  -o OUTPUT, --output OUTPUT
                        File to log results to, default = dsgo_log.txt
  --insecure INSECURE   Insecurely provide the Gmail account password as an
                        argument

```

## Finding the Required Data
### GUI
If the product currently isn't available and you are seeing the message on the website: `PRODUCT NOT AVAILABLE The product you're looking for is not available at this time.`, then you can use this URL as the target.

### API
* If the website is working, you can use the "Change Store" functionality under "Delivery & Pickup Options". Then click on "Product Details" to get the SKU.
* If the product currently isn't available and you are seeing the message on the website: `PRODUCT NOT AVAILABLE The product you're looking for is not available at this time.`, then you can use the [Wayback Machine](https://archive.org/web/) to use the website at a time when the product is available.

## Questions? 
Post an issue and I do my best to help.

