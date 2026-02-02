# Data Analytics Portfolio

**Hieu Tran** | Data Analyst in Training | Vietnam National University, Hanoi

24-week sustainable program to become internship-ready | Building in public

---

## Key Highlights

**6-Month Commitment:** Sustainable learning with real-world impact (Current: Week 1, Day 7)

**3 Real-World Projects:** Solving actual problems for real users in Vietnam - not just portfolio pieces

**Production-Ready Focus:** Live applications with measurable user impact and business value

**Unique Vietnam Context:** Price tracking, air quality monitoring, VNU student tools - problems that matter locally

**Building in Public:** Full transparency - documenting the journey from idea to deployed solution

---

## About

Year 2 student at Vietnam National University, Hanoi on a mission to master data analytics through solving real problems. This portfolio showcases end-to-end capabilities: from identifying user needs to deploying production solutions.

**Timeline:** January - July 2026 (24 weeks / 6 months)  
**Goal:** Land Technical Data Analyst internship with portfolio of deployed, user-validated projects

**What makes this different:**
- **Real users, real impact:** Each project serves 10-200 actual users with measurable outcomes
- **Vietnam-specific problems:** Solving challenges unique to Vietnamese market
- **Production deployment:** Live applications accessible via public URLs
- **User validation:** Testimonials and usage metrics from real people
- **Sustainable approach:** 12-15 hours/week, flexible around academic schedule

---

## Technical Skills

**SQL** - Advanced (70% → 100% by Week 2)
- Complex JOINs, Window Functions, CTEs
- Analytical queries (Cohort, RFM, Funnel)
- Query optimization and database design

**Python** - Intermediate (Week 3+)
- Data engineering: pandas, SQLAlchemy, automation
- Web scraping: Scrapy, BeautifulSoup, Selenium
- Analysis: NumPy, matplotlib, seaborn, scipy
- ML: scikit-learn, ARIMA forecasting
- APIs: FastAPI, Telegram Bot

**Data Engineering** - Learning (Week 2+)
- ETL pipeline design and automation
- Workflow orchestration (Airflow basics)
- Data quality and validation
- PostgreSQL database design

**Deployment & Tools**
- Streamlit web applications
- Cloud deployment (Streamlit Cloud, Railway)
- Git version control
- Docker basics (Week 13+)

---

## Portfolio Projects

> **Project Philosophy:** Build solutions people actually use. Real users, real feedback, real impact.

---

### Project 1: Vietnam E-Commerce Price Intelligence
**Week 2-8 | Web Scraping + SQL + Python + Deployment | In Progress**

**Real Problem:** Shopee and Tiki prices fluctuate constantly. Vietnamese shoppers don't know when to buy, and fake discounts mislead consumers.

**My Solution:** Automated price tracking system that monitors products daily, detects genuine deals, and alerts users when prices drop.

**How It Works:**
- Track 10-15 popular products (laptops, phones) on Shopee/Tiki
- Scrape prices daily using Python (Scrapy)
- Store in PostgreSQL with full price history
- Analyze patterns: Real vs fake discounts, best time to buy
- Alert users via Telegram/Email when target price is reached

**Technical Implementation:**

**Week 2-4: Data Pipeline (Sprint during holiday break)**
- Build Scrapy spiders for Shopee + Tiki
- PostgreSQL database design (products, price_history, alerts)
- Automated daily scraping (cron job)
- Data validation and quality checks

**Week 5-6: Analysis & Insights**
- Python analysis: Price patterns, discount authenticity
- Statistical tests: Correlation between ratings and prices
- Identify optimal buying windows
- Jupyter notebook with findings

**Week 7-8: User Application**
- Streamlit web app: Search products, view price history, set alerts
- Alert system: Telegram bot or email notifications
- Deploy to Streamlit Cloud
- Onboard 5-10 real users (friends, family, classmates)

**Expected Impact:**
- **Users:** 5-10 people actively tracking prices
- **Savings:** Average 1-2M VND per user on purchases
- **Insights:** Identify X% fake discounts vs real deals
- **Testimonials:** User feedback validating usefulness

**Skills Demonstrated:**
- Web scraping at scale (respecting rate limits, error handling)
- Database design for time-series data
- Data pipeline automation
- Statistical analysis and pattern detection
- Building user-facing applications
- Product thinking (user needs → features)

**Dataset:** Original data scraped from Shopee/Tiki (proprietary)

[View Project →](./03-projects/01-ecommerce-price-tracker) *(In Development)*

---

### Project 2: Hanoi Air Quality Alert System
**Week 11-20 | API Integration + Time Series + ML + Telegram Bot | Planned**

**Real Problem:** Hanoi's air quality is frequently hazardous, but people don't know when it's safe to go outside, exercise, or commute.

**My Solution:** Real-time AQI monitoring system with ML-powered forecasting and smart alerts via Telegram bot.

**How It Works:**
- Collect hourly AQI data from IQAir API (5+ Hanoi locations)
- Store time-series data in PostgreSQL
- Analyze patterns: Worst times, weather correlations
- Forecast AQI 6 hours ahead using ARIMA
- Alert subscribers when AQI crosses thresholds

**Technical Implementation:**

**Week 11-12: Data Pipeline**
- API integration: IQAir, OpenWeather
- PostgreSQL time-series schema
- Automated hourly collection (Airflow)
- 2 weeks of historical data collection

**Week 14-15: Analysis & Forecasting**
- Pattern analysis: Time of day, weather impact
- Statistical correlations
- ARIMA model for 6-hour forecast
- Model evaluation (target: 75%+ accuracy)

**Week 17-18: Alert System & Dashboard**
- Telegram bot: Subscribe, set preferences, receive alerts
- Alert logic: Real-time threshold alerts, daily forecasts
- Streamlit dashboard: Live AQI map, historical trends
- Deploy both bot and dashboard

**Expected Impact:**
- **Users:** 10-20 Hanoi residents
- **Alerts sent:** 100+ over 1 month
- **Forecast accuracy:** 75%+ (MAE <20 AQI points)
- **Use cases:** Help users decide when to exercise outdoors

**Skills Demonstrated:**
- API integration and data collection
- Time-series analysis and forecasting
- Machine learning (ARIMA)
- Telegram Bot development
- Real-time systems
- Deployment and monitoring

**Dataset:** Real-time AQI data via IQAir API

[View Project →](./03-projects/02-hanoi-aqi-alerts) *(Week 11 Start)*

---

### Project 3: VNU Course Registration Optimizer
**Week 22-28+ | ML Classification + User Research + Deployment | Planned**

**Real Problem:** VNU course registration is chaotic - popular courses fill up in hours, students don't know which courses to prioritize.

**My Solution:** ML-powered tool that predicts which courses will fill quickly and recommends optimal registration strategy.

**How It Works:**
- Scrape VNU course portal (200+ courses, historical data)
- Survey 50-100 VNU students on pain points
- Build ML model: Predict probability of course filling in 24h
- Recommendation engine: Given wishlist → optimal registration order
- Web app for VNU students

**Technical Implementation:**

**Week 22-23: Research & Data**
- User research: Survey students, identify key problems
- Web scraping: VNU portal (handle authentication)
- Dataset: Courses, schedules, enrollment history

**Week 25-26: ML Model**
- Feature engineering: Course attributes, instructor, time slot
- Classification model: Logistic Regression, Random Forest
- Target: Predict "will fill in 24h" (binary)
- Evaluation: 80%+ accuracy target

**Week 28-29: User Application**
- Streamlit app: Search courses, build wishlist, get strategy
- Share in VNU student groups (Facebook, Zalo)
- Collect feedback, iterate
- Aim for 50-100 student users

**Expected Impact:**
- **Users:** 50-100 VNU students
- **Prediction accuracy:** 80%+
- **Success stories:** Students getting desired courses thanks to tool
- **Viral potential:** Word-of-mouth in VNU community

**Skills Demonstrated:**
- User research and problem validation
- Web scraping with authentication
- Machine learning classification
- Recommendation systems
- Product launch and user acquisition
- Community impact

**Dataset:** Original VNU course data (proprietary)

[View Project →](./03-projects/03-vnu-course-optimizer) *(Week 22 Start)*

---

## What Makes This Portfolio Different

**Real Users, Real Impact**
- Not hypothetical business cases - actual people using the tools
- Measurable outcomes: money saved, better decisions made
- User testimonials and feedback

**Vietnam-Specific Problems**
- Solutions tailored to local market (Shopee, Tiki, Hanoi AQI, VNU)
- Unique insights unavailable elsewhere
- Demonstrates cultural context understanding

**End-to-End Ownership**
- Problem identification → User research → Building → Deployment → User feedback
- Full product lifecycle experience
- Not just coding, but product thinking

**Production Deployment**
- All projects have live URLs recruiters can visit
- Real-world deployment challenges solved
- Ongoing maintenance and iteration

---

## Learning Roadmap (24 Weeks)

**Current Phase: Foundation (Week 1-3)**
- Week 1: SQL mastery (LeetCode 50/50) ← Current: Day 7
- Week 2: Python + Database design
- Week 3: Buffer / Python advanced

**Phase 1: Price Tracker Project (Week 2-8)**
- Week 2-4: Build scraper + automation (sprint during holiday)
- Week 5-6: Data analysis + insights
- Week 7-8: User app + deployment
- **Deliverable:** Live app with 5-10 users

**Phase 2: Preparation (Week 9-10)**
- Week 9: Python advanced, API basics
- Week 10: Buffer / Academic priority

**Phase 3: AQI Alert Project (Week 11-20)**
- Week 11-12: API integration + data collection
- Week 14-15: Analysis + ML forecasting
- Week 17-18: Telegram bot + dashboard
- Week 13, 16, 19: Buffer weeks
- **Deliverable:** Live bot + dashboard, 10-20 users

**Phase 4: VNU Tool Project (Week 21-28+)**
- Week 22-23: User research + data scraping
- Week 25-26: ML model development
- Week 28-29: App deployment + user acquisition
- **Deliverable:** Live app, 50-100 VNU student users

**Phase 5: Portfolio & Job Search (Week 30-32)**
- Week 30: Portfolio website + blog posts
- Week 31: Virtual externships
- Week 32: Job applications

---

## Why Hire Me for an Internship?

**Proven Ability to Ship**
- Don't just analyze - build production solutions
- Experience with full development lifecycle
- Portfolio of deployed applications with real users

**Real-World Problem Solving**
- Identify user needs and validate solutions
- Iterate based on feedback
- Measure and demonstrate impact

**Technical Versatility**
- SQL, Python, ML, deployment - full stack
- Self-taught through project-based learning
- Quick learner adapting to new tools

**User-Centric Mindset**
- Build for users, not just for portfolio
- Understand business value and ROI
- Can communicate technical work to non-technical stakeholders

**Vietnam Market Knowledge**
- Deep understanding of local market (e-commerce, tech landscape, education)
- Bilingual: Vietnamese + English
- Cultural context for business insights

                            
---

## Certifications

**Completed:**
- Kaggle: Introduction to SQL (Nov 2025)
- Kaggle: Advanced SQL (Nov 2025)

**In Progress:**
- LeetCode SQL 50 Badge (70% → target: 100% by Week 2)

**Planned:**
- Week 9: Kaggle Python + Pandas
- Week 10: Kaggle Data Cleaning
- Week 21: Introduction to Machine Learning (Coursera/Kaggle)
- Week 30: Virtual Externships (Forage: BCG, Accenture)

---

## Connect

Open to feedback, collaboration, and internship opportunities.

**LinkedIn:** [https://www.linkedin.com/in/hieutran-analytics/]  
**Email:** tranhieu71tdh@gmail.com  
**Kaggle:** [https://www.kaggle.com/kydiotsann71]  
**GitHub:** You're already here - star this repo to follow my journey

**Looking for:** 
- Mentorship from experienced data professionals
- Feedback on project ideas and implementations
- Internship opportunities (available from Week 32 - August 2026)

---

**Last Updated:** January 27, 2026 | Week 1, Day 7 of 168 days
