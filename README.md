### What is it

This script parses odd tags from Genesis transactions of Bitcoin ordinal inscriptions using Bitcoin core RPC, populates them into MariaDB tables, and analyzes their content.
It uses `ord index export` – an option that became available as of v.8 of `ord`.

### Setup

```bash
git clone https://github.com/cypherpork/ordtagparser.git
cd ordparser
python3 -m venv env
source env/bin/activate
nano .env

# adjust .env contents to fit your environment. 
# uncomment the lines below after adjusting and put them inside .env:
# DB_USER = "parseruser"
# DB_PASSWORD = "..."
# DB_HOST = "..."
# DB_SCHEMA = "..."
# DB_PORT = "..."
# BTC_RPC_USER = "..."
# BTC_RPC_PASSWORD = "..."
# BTC_RPC_HOST = "..."
# BTC_CHAIN = "..." # (mainnet, testnet, signet)
# BTC_RPC_PORT = "..."
# BTC_RPC_PROTOCOL = "http" #(or https)

pip install --upgrade pip python-dotenv mariadb bitcoinrpc chainside-btcpy
mariadb
MariaDB [(none)]> grant all privileges on *.* TO 'ordparser'@'localhost' identified by '...';
MariaDB [(none)]> SET GLOBAL innodb_buffer_pool_size=8000000000;
MariaDB [(none)]> exit
# Test your BTC node connection:
curl -u "<BTC_RPC_USER>":"<BTC_RPC_PASSWORD>" --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockchaininfo", "params": [] }' -X POST http://<ip>:<port>/
```

### Usage

*    Update the default value for the `chain` column in the `inscr` table depending on what net you are going to work with (`signet`, `testnet`, `mainnet`)

*    Use the file that you can get from `ord index export` - `inscription_number_to_id.tsv`; load its data into the `inscr` table - populate `ord_id` and `inscr_id`.

*    Main Python script to run parsing:

     ```bash
     python parse-tags.py
     ```

     Pay attention to messages in `*.log` files that will be written into your working directory.

*    You can speed up parsing by running multiple instances of this code. I got the best performance on Mac Studio M1 by running the number of code instances `N = C-2`  where `C` is the number of available CPU cores. In this software version, to avoid DB locks, you need to partition the areas of the Inscr table by ID, allocating equal numbers of records for each instance. For that, modify the `StartQuery` method on queries.py, using comment lines as a template. Todo: automate this by using async and custom auto–partitioning.

*    If parsing chokes on some transaction, assign its id to `in_trxid` in `test-noda.py` and run:

     ```bash
     python test-noda.py
     ```

     Screen output will give you info that will help to debug.

*    To reset the database:

     ```sql
     mariadb ordparser < reset-db.sql
     ```

