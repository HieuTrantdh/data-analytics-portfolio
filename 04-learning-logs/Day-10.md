**What I Built**



* Implemented DataValidator class



* Added validation layer before DB insertion



* Built SQL trend analysis queries



* Created CLI-based analysis script



* Refactored project to remove sys.path hack



**Key Technical Lessons**



* Validation must happen before data persistence



* SQL aggregation logic requires careful grouping



* Time-based analytics must separate event time vs latest scrape time



* Proper Python packaging avoids fragile import hacks



**Challenges**



* Incorrect SQL logic for cheapest timestamp



* Import errors when running scripts incorrectly



* Handling optional fields safely in insert queries



**Architectural Insight**



* This project is evolving from a scraper into a structured data system:



* Scraper → Validator → Database → Analysis Layer



* This separation increases maintainability and scalability.



