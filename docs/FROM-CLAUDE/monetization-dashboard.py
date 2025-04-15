# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random

# Set page configuration
st.set_page_config(
    page_title="Content Extraction API Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Mock data generation functions
def generate_mock_usage_data(days=30):
    data = []
    today = datetime.now()
    
    # Define API endpoints
    endpoints = [
        "extract_web_content", 
        "extract_video_content", 
        "summarize_text", 
        "get_task_status"
    ]
    
    # Define subscription plans
    plans = ["Basic", "Professional", "Enterprise", "Pay-as-you-go"]
    
    # Generate 30 days of data with random fluctuations
    for i in range(days):
        date = today - timedelta(days=days-i)
        
        # Create different distribution patterns for different endpoints
        for endpoint in endpoints:
            # Base number of calls depending on endpoint popularity
            if endpoint == "extract_web_content":
                base_calls = random.randint(80, 120)
            elif endpoint == "extract_video_content":
                base_calls = random.randint(30, 50)
            elif endpoint == "summarize_text":
                base_calls = random.randint(60, 90)
            else:  # get_task_status
                base_calls = random.randint(150, 200)
            
            # Add weekly patterns (weekends have less activity)
            weekday_factor = 0.7 if date.weekday() >= 5 else 1.0
            
            # Add growth trend over time
            growth_factor = 1.0 + (i * 0.01)
            
            # Calculate actual calls
            calls = int(base_calls * weekday_factor * growth_factor)
            
            # Calculate revenue based on endpoint pricing
            if endpoint == "extract_web_content":
                cost_per_call = 0.05
            elif endpoint == "extract_video_content":
                cost_per_call = 0.12
            elif endpoint == "summarize_text":
                cost_per_call = 0.03
            else:  # get_task_status
                cost_per_call = 0.01
            
            revenue = calls * cost_per_call
            
            # Calculate processing time
            if endpoint == "extract_web_content":
                avg_processing_time = random.uniform(1.0, 3.0)
            elif endpoint == "extract_video_content":
                avg_processing_time = random.uniform(10.0, 30.0)
            elif endpoint == "summarize_text":
                avg_processing_time = random.uniform(0.5, 2.0)
            else:  # get_task_status
                avg_processing_time = random.uniform(0.1, 0.3)
            
            # Distribute across plans
            for plan in plans:
                # Distribute calls across plans based on plan popularity
                if plan == "Basic":
                    plan_percentage = 0.4
                elif plan == "Professional":
                    plan_percentage = 0.3
                elif plan == "Enterprise":
                    plan_percentage = 0.1
                else:  # Pay-as-you-go
                    plan_percentage = 0.2
                
                plan_calls = int(calls * plan_percentage)
                plan_revenue = plan_calls * cost_per_call
                
                data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "endpoint": endpoint,
                    "plan": plan,
                    "calls": plan_calls,
                    "revenue": plan_revenue,
                    "avg_processing_time": avg_processing_time
                })
    
    return pd.DataFrame(data)

def generate_mock_user_data(count=50):
    data = []
    today = datetime.now()
    
    # Define subscription plans with different costs
    plans = {
        "Basic": 19.99,
        "Professional": 49.99,
        "Enterprise": 199.99,
        "Pay-as-you-go": 0
    }
    
    # Status options
    statuses = ["Active", "Active", "Active", "Inactive", "Trial"]  # Weighted for more active users
    
    for i in range(count):
        # Randomly assign plan, with weighting
        plan_roll = random.random()
        if plan_roll < 0.5:
            plan = "Basic"
        elif plan_roll < 0.8:
            plan = "Professional"
        elif plan_roll < 0.9:
            plan = "Enterprise"
        else:
            plan = "Pay-as-you-go"
        
        # Generate join date
        days_ago = random.randint(1, 180)  # Users joined within the last 6 months
        join_date = today - timedelta(days=days_ago)
        
        # Determine if subscription is active
        status = random.choice(statuses)
        if status == "Trial":
            trial_expiry = join_date + timedelta(days=14)
            if trial_expiry < today:
                status = random.choice(["Active", "Inactive"])
        
        # Calculate total spent based on join date and plan
        if plan != "Pay-as-you-go":
            months = days_ago // 30
            base_spend = plans[plan] * months
            # Add some random usage charges
            usage_charges = random.uniform(0, plans[plan] * 0.5) * months
            total_spent = base_spend + usage_charges
        else:
            # Pay-as-you-go users have only usage charges
            total_spent = random.uniform(5, 100)
        
        # Calculate API usage
        if plan == "Basic":
            api_usage = random.randint(50, 200)
        elif plan == "Professional":
            api_usage = random.randint(200, 800)
        elif plan == "Enterprise":
            api_usage = random.randint(1000, 5000)
        else:  # Pay-as-you-go
            api_usage = random.randint(10, 500)
        
        # Generate some fake company names
        companies = [
            "TechCorp", "DataFlow Inc.", "ContentMasters", "WebScrape Solutions", 
            "VideoAI Labs", "TextSummaryCo", "Research Genius", "Data Extractors",
            "ContentAI", "WebHarvest", "InfoExtract", "SummaryPro", "ContentGenius",
            "AIContent", "ExtractMasters", "WebContent Solutions", "DataMine Pro"
        ]
        
        data.append({
            "user_id": f"user_{i+1}",
            "company": random.choice(companies) if random.random() > 0.3 else None,
            "plan": plan,
            "status": status,
            "join_date": join_date.strftime("%Y-%m-%d"),
            "total_spent": round(total_spent, 2),
            "api_usage": api_usage,
            "last_active": (today - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        })
    
    return pd.DataFrame(data)

# Generate mock data
@st.cache_data
def get_mock_data():
    usage_data = generate_mock_usage_data(days=90)
    user_data = generate_mock_user_data(count=100)
    return usage_data, user_data

usage_data, user_data = get_mock_data()

# Sidebar for filtering
st.sidebar.title("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=[datetime.now() - timedelta(days=30), datetime.now()],
    max_value=datetime.now()
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_usage_data = usage_data[
        (usage_data['date'] >= start_date.strftime("%Y-%m-%d")) & 
        (usage_data['date'] <= end_date.strftime("%Y-%m-%d"))
    ]
else:
    filtered_usage_data = usage_data

# Plan filter
all_plans = ["All"] + sorted(usage_data["plan"].unique().tolist())
selected_plan = st.sidebar.selectbox("Subscription Plan", all_plans)

if selected_plan != "All":
    filtered_usage_data = filtered_usage_data[filtered_usage_data["plan"] == selected_plan]

# Endpoint filter
all_endpoints = ["All"] + sorted(usage_data["endpoint"].unique().tolist())
selected_endpoint = st.sidebar.selectbox("API Endpoint", all_endpoints)

if selected_endpoint != "All":
    filtered_usage_data = filtered_usage_data[filtered_usage_data["endpoint"] == selected_endpoint]

# Main dashboard
st.title("Content Extraction API Analytics Dashboard")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

# Total API calls
total_calls = filtered_usage_data["calls"].sum()
col1.metric("Total API Calls", f"{total_calls:,}")

# Total Revenue
total_revenue = filtered_usage_data["revenue"].sum()
col2.metric("Total Revenue", f"${total_revenue:,.2f}")

# Active Users
active_users = len(user_data[user_data["status"] == "Active"])
col3.metric("Active Users", f"{active_users:,}")

# Average Processing Time
avg_time = filtered_usage_data["avg_processing_time"].mean()
col4.metric("Avg Processing Time", f"{avg_time:.2f}s")

# Create tabs for different analytics views
tab1, tab2, tab3 = st.tabs(["Usage Analytics", "Revenue Analytics", "User Analytics"])

with tab1:
    st.header("API Usage Over Time")
    
    # Group by date and endpoint to show usage trends
    daily_usage = filtered_usage_data.groupby(["date", "endpoint"])["calls"].sum().reset_index()
    
    # Create line chart for API calls over time
    fig_usage = px.line(
        daily_usage, 
        x="date", 
        y="calls", 
        color="endpoint",
        title="API Calls by Endpoint Over Time",
        labels={"calls": "Number of API Calls", "date": "Date", "endpoint": "Endpoint"}
    )
    st.plotly_chart(fig_usage, use_container_width=True)
    
    # Usage breakdown by endpoint
    st.subheader("Usage Breakdown by Endpoint")
    endpoint_usage = filtered_usage_data.groupby("endpoint")["calls"].sum().reset_index()
    
    fig_endpoint = px.pie(
        endpoint_usage, 
        values="calls", 
        names="endpoint",
        title="API Calls Distribution by Endpoint",
        hole=0.4
    )
    st.plotly_chart(fig_endpoint, use_container_width=True)
    
    # Usage statistics table
    st.subheader("Endpoint Usage Statistics")
    endpoint_stats = filtered_usage_data.groupby("endpoint").agg(
        total_calls=("calls", "sum"),
        avg_processing_time=("avg_processing_time", "mean")
    ).reset_index()
    
    # Format the statistics
    endpoint_stats["total_calls"] = endpoint_stats["total_calls"].apply(lambda x: f"{x:,}")
    endpoint_stats["avg_processing_time"] = endpoint_stats["avg_processing_time"].apply(lambda x: f"{x:.2f}s")
    
    # Rename columns for display
    endpoint_stats.columns = ["Endpoint", "Total Calls", "Avg Processing Time"]
    
    st.dataframe(endpoint_stats, use_container_width=True)

with tab2:
    st.header("Revenue Analytics")
    
    # Revenue over time
    daily_revenue = filtered_usage_data.groupby(["date", "plan"])["revenue"].sum().reset_index()
    
    fig_revenue = px.line(
        daily_revenue, 
        x="date", 
        y="revenue", 
        color="plan",
        title="Revenue Over Time by Plan",
        labels={"revenue": "Revenue ($)", "date": "Date", "plan": "Subscription Plan"}
    )
    st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Revenue by endpoint and plan
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_by_endpoint = filtered_usage_data.groupby("endpoint")["revenue"].sum().reset_index()
        fig_endpoint_revenue = px.bar(
            revenue_by_endpoint,
            x="endpoint",
            y="revenue",
            title="Revenue by Endpoint",
            labels={"revenue": "Revenue ($)", "endpoint": "Endpoint"}
        )
        st.plotly_chart(fig_endpoint_revenue, use_container_width=True)
    
    with col2:
        revenue_by_plan = filtered_usage_data.groupby("plan")["revenue"].sum().reset_index()
        fig_plan_revenue = px.bar(
            revenue_by_plan,
            x="plan",
            y="revenue",
            title="Revenue by Subscription Plan",
            labels={"revenue": "Revenue ($)", "plan": "Subscription Plan"}
        )
        st.plotly_chart(fig_plan_revenue, use_container_width=True)
    
    # Revenue forecast (simple linear projection)
    st.subheader("Revenue Forecast")
    
    # Group by date to get total daily revenue
    daily_total_revenue = filtered_usage_data.groupby("date")["revenue"].sum().reset_index()
    daily_total_revenue["date"] = pd.to_datetime(daily_total_revenue["date"])
    
    # Simple linear regression for forecast
    daily_total_revenue["day_number"] = range(len(daily_total_revenue))
    last_day = max(daily_total_revenue["day_number"])
    
    # Create future dates for projection
    future_days = 30
    future_dates = [max(pd.to_datetime(daily_total_revenue["date"])) + timedelta(days=i+1) for i in range(future_days)]
    future_day_numbers = range(last_day + 1, last_day + future_days + 1)
    
    # Create a linear model
    from sklearn.linear_model import LinearRegression
    X = daily_total_revenue[["day_number"]]
    y = daily_total_revenue["revenue"]
    model = LinearRegression().fit(X, y)
    
    # Predict future revenue
    future_revenues = model.predict([[day] for day in future_day_numbers])
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        "date": future_dates,
        "revenue": future_revenues,
        "type": ["Forecast"] * future_days
    })
    
    # Add type column to historical data
    daily_total_revenue["type"] = "Historical"
    daily_total_revenue = daily_total_revenue[["date", "revenue", "type"]]
    
    # Combine historical and forecast data
    combined_df = pd.concat([daily_total_revenue, forecast_df])
    
    # Create line chart with historical and forecast data
    fig_forecast = px.line(
        combined_df,
        x="date",
        y="revenue",
        color="type",
        title="Revenue Forecast (30-Day Projection)",
        labels={"revenue": "Revenue ($)", "date": "Date", "type": "Data Type"}
    )
    
    # Add confidence interval to forecast
    forecast_start = daily_total_revenue["date"].max()
    
    # Customizing the visualization
    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        legend_title="Data Type",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Projected monthly revenue
    current_month_revenue = daily_total_revenue[
        pd.to_datetime(daily_total_revenue["date"]).dt.month == pd.to_datetime(daily_total_revenue["date"]).max().month
    ]["revenue"].sum()
    
    forecast_month_revenue = future_revenues.sum()
    total_projected = current_month_revenue + forecast_month_revenue
    
    st.metric(
        "Projected Monthly Revenue", 
        f"${total_projected:.2f}",
        f"{forecast_month_revenue:.2f}"
    )

with tab3:
    st.header("User Analytics")
    
    # User metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Distribution of users by plan
        users_by_plan = user_data.groupby("plan").size().reset_index(name="count")
        fig_users_plan = px.pie(
            users_by_plan,
            values="count",
            names="plan",
            title="Users by Subscription Plan",
            hole=0.4
        )
        st.plotly_chart(fig_users_plan, use_container_width=True)
    
    with col2:
        # Users by status
        users_by_status = user_data.groupby("status").size().reset_index(name="count")
        fig_users_status = px.pie(
            users_by_status,
            values="count",
            names="status",
            title="Users by Status",
            hole=0.4
        )
        st.plotly_chart(fig_users_status, use_container_width=True)
    
    with col3:
        # User acquisition over time
        user_data["join_date"] = pd.to_datetime(user_data["join_date"])
        user_acquisition = user_data.groupby(pd.Grouper(key="join_date", freq="W")).size().reset_index(name="new_users")
        
        fig_acquisition = px.bar(
            user_acquisition,
            x="join_date",
            y="new_users",
            title="Weekly User Acquisition",
            labels={"new_users": "New Users", "join_date": "Week"}
        )
        st.plotly_chart(fig_acquisition, use_container_width=True)
    
    # Top users by API usage
    st.subheader("Top Users by API Usage")
    top_users = user_data.sort_values("api_usage", ascending=False).head(10)
    
    fig_top_users = px.bar(
        top_users,
        x="user_id",
        y="api_usage",
        color="plan",
        title="Top 10 Users by API Usage",
        labels={"api_usage": "API Calls", "user_id": "User", "plan": "Subscription Plan"}
    )
    st.plotly_chart(fig_top_users, use_container_width=True)
    
    # User retention analysis
    st.subheader("User Retention Analysis")
    
    # Convert join date to months ago
    today = datetime.now()
    user_data["months_ago"] = user_data["join_date"].apply(
        lambda x: (today - pd.to_datetime(x)).days // 30
    )
    
    # Group users by how many months ago they joined
    retention_data = user_data.groupby("months_ago").agg(
        total_users=("user_id", "count"),
        active_users=("status", lambda x: (x == "Active").sum())
    ).reset_index()
    
    # Calculate retention rate
    retention_data["retention_rate"] = retention_data["active_users"] / retention_data["total_users"] * 100
    
    # Sort by months ago (oldest first)
    retention_data = retention_data.sort_values("months_ago", ascending=False)
    
    # Create retention chart
    fig_retention = px.line(
        retention_data,
        x="months_ago",
        y="retention_rate",
        title="User Retention Rate by Cohort Age",
        labels={
            "months_ago": "Months Since Joining",
            "retention_rate": "Retention Rate (%)"
        }
    )
    
    # Customize the x-axis to reverse it (0 months ago on the right)
    fig_retention.update_xaxes(autorange="reversed")
    
    st.plotly_chart(fig_retention, use_container_width=True)
    
    # User table with search functionality
    st.subheader("User Database")
    
    # Add search functionality
    search_term = st.text_input("Search users by ID or company")
    
    if search_term:
        filtered_users = user_data[
            user_data["user_id"].str.contains(search_term, case=False) |
            (user_data["company"].astype(str).str.contains(search_term, case=False))
        ]
    else:
        filtered_users = user_data
    
    # Show table with pagination
    st.dataframe(filtered_users, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© 2025 Content Extraction API Analytics Dashboard | Data refreshed daily")
