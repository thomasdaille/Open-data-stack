# Hospital OLTP Synthetic Dataset  
  
This repository contains a fully synthetic hospital OLTP dataset, designed to simulate the operational data of a healthcare institution.

The dataset is generated using the Python script data-generation.py and produces a set of CSV files stored in /data directory.

Command line : `python data-generation.py`

The script uses:

- Faker for realistic names, cities, addresses
- controlled randomness for distributions
- systematic anomaly injection
- referential integrity across all tables