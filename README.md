# Amazon Transaction Scraper PoC #

## Requirements ##
* Docker should be installed
* Python 3 should be installed and included in path
* Bash should be available to run `run.sh`

## Quick Start ##
Clone the repository from github and move into it:
```
git clone git@github.com:Ghorbanian/Amazon-Transaction-Scraper
cd amazon_txn_scraper/
```

Add your Amazon username and password to a `.env` file in the root of the project directory:
```
echo "AMAZON_USERNAME='<username>'\nAMAZON_PASSWORD='<password>'" > .env
```

Run the `run.sh` script
```
bash run.sh
```

Find all of your transactions from your amazon account in the `transactions` directory.
