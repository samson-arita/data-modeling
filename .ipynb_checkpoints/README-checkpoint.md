# Songplays

Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 

Here, we create a Postgres database with tables designed to optimize queries on song play analysis

Songplays is a postgresql database ETL on songplays data created from files with songs data files and logs data files.

create_tables.py - Creates database and drops any existing tables prior to creating
etl.ipynb - shows the etl on the jupyter notebook
etl.py - processes the files
sql_querys.py - has all the queries used in the project
test.ipynb - shows a summary on the project's tables


## Installation of postgresql wrapper

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install psycopg2.

```bash
pip install psycopg2
```

## Usage

```bash
python create_tables.py
python etl.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT]