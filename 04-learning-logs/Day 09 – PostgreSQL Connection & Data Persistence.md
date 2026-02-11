\# Day 09 – PostgreSQL Connection \& Data Persistence



\##  Objective

Integrate PostgreSQL into the scraping pipeline and persist product data into relational tables.



\##  What I Built

\- Created database/db\_manager.py

\- Implemented connection pooling using psycopg2

\- Added context manager for safe transactions

\- Designed schema:

&nbsp; - sellers

&nbsp; - products

&nbsp; - price\_history



\##  Issues Encountered

\- psycopg2 connection error due to incorrect environment variables

\- Duplicate product entries when running scraper multiple times

\- Price stored as text instead of numeric



\##  Root Cause Analysis

\- .env file was not loaded properly

\- No UNIQUE constraint on product\_url

\- Price parsing did not remove currency formatting



\##  Fix Implemented

\- Used python-dotenv to load environment variables

\- Added UNIQUE constraint on product\_url

\- Converted price to numeric after cleaning string



\##  Key Learnings

\- Importance of idempotent data pipelines

\- Why schema design matters before inserting data

\- Difference between raw data scraping and production-grade ingestion



\##  Next Step

\- Implement price change detection

\- Add logging instead of print debugging



