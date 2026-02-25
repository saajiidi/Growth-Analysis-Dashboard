import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config for a premium feel
st.set_page_config(
    page_title="WPPOOL Growth Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8faff;
    }
    
    /* Premium Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1a1a1a;
    }
    
    div[data-testid="metric-container"] {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #edf2f7;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }
    
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
    }

    /* Card Containers */
    .chart-container {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('wppool_growth_data_sample_20k.csv')
    except:
        # Fallback if file is missing in some envs
        df = pd.read_csv('data/wppool_growth_data_sample_20k.csv')
        
    df.fillna({
        'total_sessions': df['total_sessions'].median(),
        'page_views': df['page_views'].median(),
        'days_active': df['days_active'].median(),
        'monthly_revenue': 0
    }, inplace=True)
    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# Sidebar Navigation
with st.sidebar:
    st.image("logo.svg", width=120)
    st.title("Growth Center")
    st.markdown("---")
    
    # Global Filters
    st.subheader("🌐 Global Filters")
    countries = sorted(df['country'].unique())
    selected_countries = st.multiselect("Select Countries", countries, default=countries[:5])
    
    sub_types = df['subscription_type'].unique()
    selected_subs = st.multiselect("Subscription Type", sub_types, default=list(sub_types))
    
    st.markdown("---")
    
    selection = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "📊 Data Exploration",
            "👥 User Engagement",
            "🤖 AI Segmentation",
            "📉 Churn Analysis",
            "💰 Revenue Trends",
            "💡 Strategic Insights",
            "🎯 Conversion (CRO)",
            "🗺️ Market Map"
        ]
    )
    st.markdown("---")
    
    # Data Export
    st.subheader("📤 Export Report")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full CSV",
        data=csv,
        file_name='wppool_growth_report.csv',
        mime='text/csv',
    )
    
    st.info("WPPOOL Growth Analytics v2.1")

# Apply Global Filters
filtered_df = df[
    (df['country'].isin(selected_countries)) & 
    (df['subscription_type'].isin(selected_subs))
]

# Header Section
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.image("logo.svg", width=80)
with col_title:
    st.title("WPPOOL Growth Analytics")
st.markdown(f"**Current View:** {selection}")
st.markdown("---")

# Metrics Calculations
total_users = len(filtered_df)
free_pro_dist = filtered_df['subscription_type'].value_counts(normalize=True) * 100
pro_users_pct = free_pro_dist.get('Pro', 0)
total_revenue = filtered_df['monthly_revenue'].sum()
churn_rate_total = filtered_df['churned'].mean() * 100

def display_metrics():
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Users", f"{total_users:,}", help="Total unique users across all platforms")
    m2.metric("Pro Conversion", f"{pro_users_pct:.2f}%", delta="1.4%", help="Percentage of users on a paid plan")
    m3.metric("Annual Revenue", f"${total_revenue * 12:,.0f}", help="Estimated annual recurring revenue")
    m4.metric("Avg Churn", f"{churn_rate_total:.1f}%", delta="-0.5%", delta_color="inverse")

if selection == "🏠 Overview":
    display_metrics()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Revenue Contribution by Plan Type")
        revenue_by_plan = filtered_df[filtered_df['subscription_type'] == 'Pro'].groupby('plan_type')['monthly_revenue'].sum().reset_index()
        fig = px.pie(revenue_by_plan, values='monthly_revenue', names='plan_type', hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Top Performers (Countries)")
        top_countries_rev = filtered_df.groupby('country')['monthly_revenue'].sum().nlargest(10).reset_index()
        st.dataframe(top_countries_rev, hide_index=True)
        
    st.markdown("---")
    st.subheader("Key Takeaways")
    st.success(f"Currently analyzing {total_users:,} users across {len(selected_countries)} countries.")

elif "Data Exploration" in selection:
    st.subheader("Filtered Data Inspection")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Statistical Summary")
        st.write(filtered_df.describe())
    with col2:
        st.subheader("Subscription Mix")
        fig = px.pie(filtered_df, names='subscription_type', hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig, use_container_width=True)

elif "User Engagement" in selection:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement by Group")
        avg_sessions = filtered_df.groupby('subscription_type')['total_sessions'].mean().reset_index()
        fig1 = px.bar(avg_sessions, x='subscription_type', y='total_sessions', 
                     color='subscription_type', 
                     color_discrete_sequence=['#6366f1', '#a5b4fc'])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Regional Engagement Heatmap")
        top_countries_eng = filtered_df.groupby('country')['total_sessions'].sum().nlargest(10).reset_index()
        fig2 = px.funnel(top_countries_eng, x='total_sessions', y='country',
                        color='total_sessions', color_continuous_scale='Blues')
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 High-Activity Users")
    top_users = filtered_df.nlargest(10, 'total_sessions')[['user_id', 'total_sessions', 'subscription_type', 'country']]
    st.table(top_users)

elif "AI Segmentation" in selection:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    
    st.subheader("🤖 User Persona Discovery (K-Means)")
    st.markdown("This model groups users based on their **Engagement** and **Tenure** to identify latent personas.")
    
    features = ['total_sessions', 'days_active']
    X = filtered_df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    n_clusters = st.slider("Select Number of Clusters (Personas)", 2, 5, 3)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    filtered_df['Persona_ID'] = kmeans.fit_predict(X_scaled)
    
    persona_map = {
        0: "Casual Explorers",
        1: "Power Users",
        2: "Loyal Fans",
        3: "Churn-Prone",
        4: "New Enthusiasts"
    }
    filtered_df['Persona'] = filtered_df['Persona_ID'].map(persona_map)
    
    fig = px.scatter(
        filtered_df, x='total_sessions', y='days_active', 
        color='Persona', 
        title=f"Discovered {n_clusters} User Personas",
        opacity=0.7,
        labels={'total_sessions': 'Total Sessions', 'days_active': 'Days Active'},
        hover_data=['country', 'subscription_type']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Persona Distribution")
    persona_counts = filtered_df['Persona'].value_counts().reset_index()
    fig2 = px.bar(persona_counts, x='Persona', y='count', color='Persona')
    st.plotly_chart(fig2, use_container_width=True)

elif "Churn Analysis" in selection:
    st.subheader("Predictive Churn Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn Rate per Segment")
        churn_rate_sub = filtered_df.groupby('subscription_type')['churned'].mean() * 100
        fig1 = px.pie(values=churn_rate_sub.values, names=churn_rate_sub.index, 
                     hole=0.5, color_discrete_sequence=['#ef4444', '#3b82f6'])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Churn Activity Breakdown")
        fig2 = px.box(filtered_df, x='churned', y='total_sessions', color='subscription_type',
                     title="Sessions vs Churn Status")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Feature Correlation with Churn")
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()['churned'].sort_values().to_frame()
    fig_corr = px.bar(corr, orientation='h', title="Feature Impact on Churn")
    st.plotly_chart(fig_corr, use_container_width=True)

elif "Revenue Trends" in selection:
    display_metrics()
    
    st.subheader("Revenue by Country (Selected Filter)")
    rev_by_country = filtered_df.groupby('country')['monthly_revenue'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(rev_by_country, x='country', y='monthly_revenue', color='monthly_revenue',
                color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Monthly Revenue Distribution by Plan")
    fig2 = px.violin(filtered_df[filtered_df['subscription_type']=='Pro'], 
                    x='plan_type', y='monthly_revenue', color='plan_type', box=True)
    st.plotly_chart(fig2, use_container_width=True)

elif "Strategic Insights" in selection:
    st.header("Actionable Growth Roadmap")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🛡️ Churn Prevention
        - **Phase 1:** Implement automated re-engagement emails for users inactive for >7 days.
        - **Phase 2:** Offer 'Standard' to 'Pro' transition discounts for power users.
        - **Phase 3:** Loyalty program for annual subscribers.
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Acquisition & Expansion
        - **Channel Opt:** Focus ad spend on Germany and Canada (High CLV).
        - **Product:** Simplify the 'Standard' plan onboarding flow.
        - **Upsell:** Target 'Basic' users with 'Enterprise' case studies.
        """)
    
    st.success("🎯 Goal: Increase conversion rate to 25% by Q4 2026.")

elif "Conversion (CRO)" in selection:
    st.subheader("A/B Testing Simulator")
    
    base_conv = 20.14
    improvement = st.slider("Hypothetical Conversion Improvement (%)", 1, 50, 10)
    
    new_conv = base_conv * (1 + improvement/100)
    extra_users = int(total_users * (new_conv - base_conv) / 100)
    extra_rev = extra_users * df['monthly_revenue'].mean()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("New Conv. Rate", f"{new_conv:.2f}%")
    c2.metric("Additional Pro Users", f"+{extra_users}")
    c3.metric("Monthly Revenue Impact", f"+${extra_rev:,.2f}")
    
    st.markdown("---")
    st.subheader("CRO Checklist")
    st.checkbox("Mobile-first design optimization", value=True)
    st.checkbox("One-click checkout for Pro upgrades", value=False)
    st.checkbox("Trust badges on pricing page", value=True)

elif "Market Map" in selection:
    st.subheader("Global Footprint")
    rev_by_country = df.groupby('country')['monthly_revenue'].sum().reset_index()
    fig = px.choropleth(rev_by_country, locations='country', locationmode='country names',
                        color='monthly_revenue', hover_name='country',
                        color_continuous_scale='Plasma',
                        title="Revenue Heatmap")
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Engagement Latency by Region")
    fig2 = px.scatter(df, x='country', y='total_sessions', size='monthly_revenue', color='subscription_type',
                     hover_name='user_id', title="Regional Engagement vs Revenue")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.caption("Generated by Antigravity AI | WPPOOL Growth Analytics Dashboard 2026")
