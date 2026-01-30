# Data Analytics Portfolio

**Hieu Tran** | Data Analyst in Training | Vietnam National University, Hanoi

16-week intensive program to become internship-ready | Building in public

---

## Key Highlights

**112-Day Commitment:** Daily practice and project work (Current streak: 4 days)

**5 Real-World Projects:** From SQL analytics to ML forecasting and web scraping - not just tutorials

**70% SQL Proficiency in 4 Days:** 35/50 LeetCode problems solved with focus on business analytics

**Building in Public:** Full transparency - every query, every mistake, every learning documented

**Business-First Approach:** Projects answer real business questions, not just showcase technical skills

---

## About

Year 2 student on a focused journey to master data analytics through practical projects and daily practice. This portfolio documents real-world projects solving actual business problems, with complete code and documentation.

**Timeline:** January - April 2026 (16 weeks)  
**Goal:** Land Data Analyst internship with demonstrable skills

**What sets this apart:**
- Projects use real datasets (100K+ rows), not toy examples
- Every project has clear business value and actionable insights
- Complete transparency: successes and failures both documented
- Focus on end-to-end analysis: from raw data to business recommendations

---

## Technical Skills

**SQL** - Advanced (70%)
- Complex JOINs, Window Functions, CTEs
- Analytical queries (Cohort, RFM, Funnel)
- Query optimization

**Python** - Learning (Week 3 start)
- pandas, NumPy, matplotlib, seaborn
- Data cleaning and manipulation
- Basic machine learning (scikit-learn)

**Excel** - Intermediate (50%)
- PivotTables, Power Query, INDEX-MATCH
- Array formulas, data validation
- Advanced functions and dashboards

**Business Intelligence** - Planned (Week 7)
- Tableau Public / Power BI
- Dashboard design and visualization

---

## Portfolio Projects

> **Project Philosophy:** Quality over quantity. Three comprehensive projects demonstrating end-to-end data analytics skills - from data collection to business recommendations.

---

### 📊 Project 1: E-Commerce Analytics Platform
**Week 2-4 | SQL + Python + Tableau | In Progress**

**Business Challenge:** E-commerce company needs actionable insights to increase revenue and improve customer retention in a competitive market.

**Dataset:** 100,000 real orders from Brazilian E-Commerce (Olist) | 8 relational tables

**Comprehensive Analysis (3-Week Deep Dive):**

**Week 2 - SQL Mastery:**
- Revenue intelligence: Daily/weekly/monthly trends with growth rates
- Customer segmentation using RFM methodology in pure SQL
- Product performance: ABC analysis (80/20 rule)
- Geographic insights: Sales patterns by state/city
- Operational metrics: Delivery performance and review correlation

**SQL Techniques Demonstrated:**
- Complex multi-table JOINs (4-5 tables)
- Advanced Window Functions (RANK, LAG, LEAD, running totals)
- CTEs and subqueries for complex logic
- Date functions and aggregations
- CASE WHEN for business rules

**Week 3 - Python Analytics:**
- Statistical analysis (correlation, distributions, outliers)
- 8-10 professional visualizations (trends, heatmaps, scatter plots)
- Cohort retention matrix
- Basic predictive insights (linear regression for forecasting)

**Week 4 - Business Deliverables:**
- Interactive Tableau dashboard (published publicly)
- Executive report (PDF, 3-5 pages) with strategic recommendations
- Complete GitHub documentation with reproducible code

**Expected Business Impact:**
- Identify top 20% customers driving 80% revenue
- Optimize delivery operations to reduce late deliveries by 15%
- Product bundling recommendations to increase AOV
- Geographic expansion opportunities based on untapped markets

**Skills Showcased:** Advanced SQL, Python (pandas, matplotlib, seaborn, scipy), Tableau, Business Analysis, Technical Documentation

**Dataset:** [Brazilian E-Commerce - Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

📁 [View Project Details →](./03-projects/01-ecommerce-analytics-platform)

---

### 🌟 Project 2: Vietnam Tech News Intelligence
**Week 6-8 | Web Scraping + NLP + Analysis | Planned**

**Research Question:** What are the hottest trends in Vietnam's tech ecosystem? Which technologies and topics dominate the news cycle?

**Why This Project Stands Out:**
- ✅ **Original data collection** - Web scraping, not pre-made datasets
- ✅ **Shows initiative** - Self-directed research project
- ✅ **Vietnam-specific** - Unique insights unavailable elsewhere
- ✅ **Current & relevant** - Real-time tech landscape analysis

**Data Collection Strategy:**
- **Primary sources:** VnExpress Tech, Genk.vn (RSS feeds - 200-300 articles)
- **Secondary:** TechInAsia Vietnam (web scraping if feasible)
- **Time period:** Recent 6-12 months of tech coverage

**Analysis Framework:**

**Week 6 - Data Collection:**
- Build RSS feed scraper (Python: feedparser, requests)
- Implement web scraper for dynamic content (BeautifulSoup/Selenium)
- Data cleaning: text normalization, duplicate removal
- Dataset: 300-400 tech news articles

**Week 7 - Text Analytics:**
- **Topic modeling:** Most discussed topics (AI, blockchain, startups, funding)
- **Trend analysis:** Topic popularity over time
- **Keyword extraction:** Top companies, technologies, people mentioned
- **Sentiment analysis:** Positive/negative/neutral distribution using TextBlob
- **Temporal patterns:** Publishing frequency and hot news periods

**Week 8 - Insights & Deliverables:**
- Interactive Tableau dashboard: Topic trends, word clouds, sentiment gauges
- Research report: "Vietnam Tech Landscape 2026: Data-Driven Insights"
- Blog post: "I Analyzed 300+ Vietnam Tech Articles: Here's What's Hot"
- **Public dataset release** on Kaggle - first Vietnamese tech news dataset

**Research Findings (Expected):**
- Top 10 most covered tech topics in Vietnam
- Which companies/startups get most media attention
- Sentiment trends (positive vs critical coverage)
- Emerging technologies gaining traction
- Content gaps and underreported topics

**Skills Showcased:** Web Scraping, NLP (Natural Language Processing), Text Analytics, Data Cleaning (messy real-world data), Python (Beautiful Soup, pandas, TextBlob), Data Visualization

**Unique Value:** Demonstrates ability to gather original data and conduct independent research - a key differentiator from candidates who only use pre-cleaned datasets.

📁 [View Project Details →](./03-projects/02-vietnam-tech-news-intelligence)

---

### 🤖 Project 3: Sales Forecasting System
**Week 10-13 | Machine Learning + Deployment | Planned**

**Business Problem:** Retail chain needs accurate sales forecasts to optimize inventory investment and reduce waste while meeting demand.

**Dataset:** Real grocery store sales data from Corporación Favorita (Ecuador) | 3+ years of daily sales

**Advanced ML Implementation (4-Week Build):**

**Week 10 - Exploratory Analysis:**
- Deep time series analysis: trend, seasonality, residuals decomposition
- External factor analysis: holidays, promotions, oil prices impact
- Store-level and product category variations
- **Deliverable:** Comprehensive EDA notebook (15-20 pages), 15+ visualizations

**Week 11-12 - Model Development:**
- **Baseline models:** Moving average, naive forecast, linear regression
- **Advanced models:** Random Forest, XGBoost, ARIMA (time series specific)
- Feature engineering: lag features, rolling statistics, holiday indicators
- Cross-validation strategy for time series
- **Metrics:** RMSE, MAE, MAPE with business context
- Error analysis and feature importance interpretation

**Week 13 - Production Simulation:**
- Modularized Python package (preprocessing, training, prediction modules)
- **Streamlit web app:** Upload data → Generate forecasts → Visualize results
- **App features:** Interactive predictions, downloadable reports, model explanations
- **Deployment:** Live app on Streamlit Cloud (shareable link)
- Complete technical documentation and user guide

**Business Impact (Expected):**
- Reduce inventory waste by 10-15% through accurate forecasting
- Optimize staffing schedules based on predicted demand patterns
- Identify high-ROI promotional periods
- Provide forecast confidence intervals for risk management

**Deliverables:**
- Multiple Jupyter notebooks (EDA, baseline models, advanced models)
- Clean Python package with modular code structure
- **Deployed web application** (accessible via link - portfolio highlight!)
- Technical report: Model methodology, performance, limitations
- 5-minute video demo showcasing the system

**Skills Showcased:** Time Series Analysis, Machine Learning (multiple algorithms), Model Evaluation, Python Packaging, Web Development (Streamlit), Software Engineering Best Practices, Communication (video demo)

**Production-Ready Mindset:** This project goes beyond Jupyter notebooks to demonstrate how data science solutions are deployed in real companies.

**Dataset:** [Store Sales Forecasting - Kaggle](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

📁 [View Project Details →](./03-projects/03-sales-forecasting-system)

---

## What Makes This Portfolio Different

**Real Business Focus**
- Every project answers specific business questions
- Emphasis on ROI and actionable insights
- Projects mirror actual work scenarios

**Full Transparency**
- Complete code with comments explaining reasoning
- Documentation includes what didn't work and why
- Learning process visible, not just final results

**Scalable & Production-Ready**
- Queries optimized for large datasets (100K+ rows)
- Reusable code with clear structure
- Professional documentation standards

**Self-Directed Learning**
- Project 5 entirely self-initiated
- Daily problem-solving practice
- Continuous improvement mindset

---

## Learning Roadmap

**Phase 1: SQL & Excel** (Week 1-2) - Current
- Advanced SQL and analytics
- Excel intermediate to advanced
- Project 1 completion

**Phase 2: Python Foundation** (Week 3-6)
- Python basics and pandas
- Data manipulation and visualization
- Project 2 completion

**Phase 3: BI Tools** (Week 7-8)
- Tableau/Power BI mastery
- Dashboard design
- Project 3 completion

**Phase 4: Machine Learning** (Week 9-12)
- ML fundamentals and forecasting
- Web scraping and automation
- Projects 4-5 completion

**Phase 5: Portfolio & Job Search** (Week 13-16)
- Virtual externships (Accenture, KPMG, BCG)
- Portfolio refinement
- Job applications and interviews

---

## Current Progress

**Week 1/16** - SQL Mastery & Excel

| Metric | Progress | Notes |
|--------|----------|-------|
| LeetCode SQL 50 | 35/50 (70%) | Focus on CTEs, Window Functions |
| Excel Skills | 50% | PivotTables, INDEX-MATCH, Power Query |
| Projects | 1/5 in progress | E-commerce analysis underway |
| Daily Streak | 4/112 days | Committed to daily practice |
| Study Hours | 16/336 total | Average 4 hours/day |

**This Week's Achievements:**
- Completed 35 SQL problems in 4 days (above target)
- Built first Excel dashboard with real data
- Set up professional GitHub portfolio
- Documented all learning in markdown

---

## Problem-Solving Track Record

**SQL Practice (LeetCode, StrataScratch)**
- 35 problems solved (70% of target)
- Focus areas: CTEs (10), Window Functions (12), JOINs (8), Analytics (5)
- Average time: 18 minutes per problem (improving)

**All solutions documented:** [View SQL Practice →](./02-sql-practice/)

---

## Certifications

**Completed:**
- Kaggle: Introduction to SQL (Nov 2025)
- Kaggle: Advanced SQL (Jan 2026)

**In Progress:**
- LeetCode SQL 50 Badge (70% complete)

**Planned (Week-by-week):**
- Week 4: Kaggle Python + Pandas
- Week 6: Kaggle Data Cleaning + Visualization
- Week 8: Microsoft Excel + Power BI
- Week 13: Virtual Externships (Accenture, KPMG, BCG)

---


---

## Why Hire Me for an Internship?

**Proven Learning Ability**
- 70% SQL proficiency achieved in 4 days
- Self-directed learning with clear results

**Business Mindset**
- Projects focus on ROI and actionable insights
- Understand that data serves business goals

**Professional Work Ethic**
- 112-day commitment to daily practice
- Detailed documentation and clean code
- Building in public demonstrates accountability

**Real-World Ready**
- Projects use production-scale datasets
- Analysis follows industry best practices
- Can explain technical concepts to non-technical stakeholders

---

## Connect

Open to feedback, mentorship, and internship opportunities.

**LinkedIn:** [https://www.linkedin.com/in/hieutran-analytics/]  
**Email:** tranhieu71tdh@gmail.com 
**Kaggle:** [https://www.kaggle.com/kydiotsann71  
**GitHub:** You're already here - star this repo to follow my journey


---

**Last Updated:** January 30, 2026 | Day 5 of 112

*"Consistency beats intensity. Building something meaningful, one day at a time."*
