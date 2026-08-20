MetricMind-1
AI-powered data analytics platform for governed Semantic BI, natural-language insights, and interactive data visualization.

MetricMind
AI-Powered Data Analytics Platform
MetricMind is an advanced data analytics and conversational BI project designed to transform natural-language business questions into meaningful analytical insights.

The project follows the concept of Semantic BI, where business metrics such as Revenue, Cost, Profit, and Margin are defined consistently before analytics are performed.

Features
Natural-language business queries
Semantic metric definitions
Revenue, Cost, Profit and Margin analysis
Automatic data filtering
Interactive charts
Business insights generation
CSV-based analytics
Simple and easy-to-use dashboard
No external API key required for the demo
Technology Stack
Python
Streamlit
Pandas
Plotly
CSV
Semantic Analytics
Project Structure
MetricMind/
│
├── app.py
├── data.csv
├── requirements.txt
└── README.md
How to Run
1. Clone the repository
git clone https://github.com/akhilames/MetricMind-1.git
cd MetricMind-1
2. Install dependencies
pip install -r requirements.txt
3. Run the application
streamlit run app.py
4. Open in browser

The application will open at:
http://localhost:8501
Example Queries

Try queries such as:
Show revenue by region
Show cost by region
Show profit by region
Show margin by region
Show quarterly revenue
Why did revenue decrease?
| Metric  | Definition             |
| ------- | ---------------------- |
| Revenue | Total sales revenue    |
| Cost    | Total business cost    |
| Profit  | Revenue - Cost         |
| Margin  | Profit / Revenue × 100 |

Goal

The goal of MetricMind is to demonstrate how conversational analytics and governed semantic metrics can provide reliable and understandable business insights instead of relying on uncontrolled raw SQL generation.
Future Enhancements
LLM integration
LangChain agent
dbt/Cube semantic layer
PostgreSQL/Snowflake integration
Authentication
Advanced dashboards
Automatic root-cause analysis
AI-generated business recommendations
Author

Akhila Mesupamu
