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
