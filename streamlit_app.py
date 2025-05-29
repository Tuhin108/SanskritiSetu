import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Page configuration
st.set_page_config(
    page_title="India Cultural Heritage & Tourism",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #004643;
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-card {
        background-color: #F8F4E6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = None

# Sidebar navigation
st.sidebar.title("🎭 Cultural Tourism Navigator")
page = st.sidebar.radio(
    "Explore",
    ["Home", "Traditional Art Forms", "Cultural Experiences", 
     "Tourism Analytics", "Responsible Tourism", "Data Insights"]
)

# Sample data - In production, this would come from Snowflake
@st.cache_data
def load_sample_data():
    # Enhanced sample data that mimics real government data structure
    art_forms = pd.DataFrame({
        'name': ['Kathakali', 'Bharatanatyam', 'Madhubani', 'Warli', 'Pattachitra', 
                 'Kuchipudi', 'Odissi', 'Dhokra', 'Chau Dance', 'Puppetry',
                 'Kalaripayattu', 'Theyyam', 'Yakshagana', 'Lavani', 'Giddha'],
        'state': ['Kerala', 'Tamil Nadu', 'Bihar', 'Maharashtra', 'Odisha', 
                  'Andhra Pradesh', 'Odisha', 'West Bengal', 'Jharkhand', 'Rajasthan',
                  'Kerala', 'Kerala', 'Karnataka', 'Maharashtra', 'Punjab'],
        'category': ['Dance', 'Dance', 'Painting', 'Painting', 'Painting', 
                     'Dance', 'Dance', 'Craft', 'Dance', 'Performance',
                     'Martial Art', 'Ritual', 'Theatre', 'Dance', 'Dance'],
        'tourism_score': [85, 90, 70, 65, 75, 80, 78, 60, 55, 88, 72, 68, 82, 77, 71],
        'preservation_status': ['Good', 'Excellent', 'Fair', 'Fair', 'Good', 
                               'Good', 'Good', 'At Risk', 'At Risk', 'Good',
                               'Good', 'At Risk', 'Good', 'Fair', 'Good'],
        'practitioners': [5000, 15000, 8000, 3000, 4500, 7000, 6000, 1200, 800, 12000,
                         2000, 500, 3500, 9000, 6500],
        'govt_support': ['High', 'High', 'Medium', 'Low', 'Medium', 'High', 'High', 
                        'Low', 'Low', 'High', 'Medium', 'Low', 'Medium', 'Medium', 'Medium']
    })
    
    # Tourism data with more realistic patterns
    dates = pd.date_range('2023-01', periods=12, freq='M')
    tourism_data = pd.DataFrame({
        'month': dates,
        'domestic_tourists': [4500000, 4800000, 5200000, 4200000, 3800000, 2800000, 
                             2500000, 2700000, 3800000, 5500000, 6200000, 6800000],
        'international_tourists': [120000, 140000, 160000, 110000, 80000, 45000, 
                                  35000, 40000, 85000, 180000, 220000, 250000],
        'revenue_crores': [2800, 3200, 3600, 2900, 2400, 1800, 1600, 1700, 2500, 3800, 4200, 4600]
    })
    
    # Expanded cultural sites data
    cultural_sites = pd.DataFrame({
        'site': ['Ajanta Caves', 'Hampi', 'Khajuraho', 'Konark Temple', 'Mysore Palace', 
                 'Red Fort', 'Qutub Minar', 'Taj Mahal', 'Sanchi Stupa', 'Ellora Caves',
                 'Mahabalipuram', 'Fatehpur Sikri', 'Agra Fort', 'Humayun Tomb'],
        'state': ['Maharashtra', 'Karnataka', 'Madhya Pradesh', 'Odisha', 'Karnataka', 
                  'Delhi', 'Delhi', 'Uttar Pradesh', 'Madhya Pradesh', 'Maharashtra',
                  'Tamil Nadu', 'Uttar Pradesh', 'Uttar Pradesh', 'Delhi'],
        'visitors_2023': [580000, 420000, 380000, 320000, 750000, 820000, 680000, 
                         1200000, 180000, 650000, 450000, 380000, 890000, 420000],
        'lat': [20.5519, 15.3350, 24.8318, 19.8876, 12.3051, 28.6562, 28.5244, 
                27.1751, 23.4793, 20.0269, 12.6208, 27.0945, 27.1767, 28.5933],
        'lon': [75.7033, 76.4601, 79.9199, 86.0945, 76.6551, 77.2410, 77.1855, 
                78.0421, 77.7398, 75.1789, 80.1982, 77.5619, 78.0081, 77.2507],
        'unesco_status': ['Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 
                         'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'type': ['Cave', 'Ruins', 'Temple', 'Temple', 'Palace', 'Fort', 'Monument', 
                'Mausoleum', 'Stupa', 'Cave', 'Temple', 'City', 'Fort', 'Tomb']
    })
    
    # Government schemes data (based on actual schemes)
    govt_schemes = pd.DataFrame({
        'scheme': ['Swadesh Darshan 2.0', 'PRASHAD', 'Adopt a Heritage', 'Dekho Apna Desh'],
        'budget_crores': [5000, 1200, 0, 800],
        'sites_covered': [134, 56, 95, 0],
        'focus_area': ['Theme Circuits', 'Pilgrimage Sites', 'Monument Conservation', 'Domestic Tourism'],
        'launch_year': [2014, 2014, 2017, 2020],
        'ministry': ['Tourism', 'Tourism', 'Tourism & Culture', 'Tourism']
    })
    
    return art_forms, tourism_data, cultural_sites, govt_schemes

# Update the function call
art_forms, tourism_data, cultural_sites, govt_schemes = load_sample_data()

# Home Page
if page == "Home":
    st.markdown('<h1 class="main-header">🎭 Discover India\'s Cultural Heritage</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A Data-Driven Journey Through Traditional Arts, Culture & Responsible Tourism</p>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Traditional Art Forms", "500+", "Documented")
    with col2:
        st.metric("Cultural Sites", "3,691", "UNESCO & ASI Protected")
    with col3:
        st.metric("Annual Tourists", "1.9B", "↑ 15% from 2022")
    with col4:
        st.metric("Economic Impact", "₹15.2T", "Tourism Contribution")
    
    st.markdown("---")
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 Welcome to India's Cultural Tourism Platform
        
        India's cultural heritage spans over 5,000 years, encompassing diverse art forms, 
        architectural marvels, and living traditions. This platform leverages data to:
        
        - **Showcase** traditional art forms and their current status
        - **Analyze** tourism patterns and seasonality
        - **Identify** lesser-known cultural treasures
        - **Promote** sustainable and responsible tourism practices
        - **Connect** travelers with authentic cultural experiences
        
        Explore our interactive dashboards to discover the stories behind the data and 
        plan your cultural journey through India.
        """)
    
    with col2:
        # Quick stats visualization
        fig = go.Figure(data=[
            go.Bar(name='Art Forms', x=['Dance', 'Music', 'Craft', 'Painting'], 
                   y=[147, 89, 156, 112], marker_color='#FF6B35'),
            go.Bar(name='At Risk', x=['Dance', 'Music', 'Craft', 'Painting'], 
                   y=[23, 15, 34, 18], marker_color='#004643')
        ])
        fig.update_layout(
            barmode='stack',
            title='Traditional Art Forms Status',
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

# Traditional Art Forms Page
elif page == "Traditional Art Forms":
    st.title("🎨 Traditional Art Forms of India")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Select Category", 
                                     ["All"] + list(art_forms['category'].unique()))
    with col2:
        state_filter = st.selectbox("Select State", 
                                  ["All"] + list(art_forms['state'].unique()))
    with col3:
        status_filter = st.selectbox("Preservation Status", 
                                   ["All"] + list(art_forms['preservation_status'].unique()))
    
    # Filter data
    filtered_data = art_forms.copy()
    if category_filter != "All":
        filtered_data = filtered_data[filtered_data['category'] == category_filter]
    if state_filter != "All":
        filtered_data = filtered_data[filtered_data['state'] == state_filter]
    if status_filter != "All":
        filtered_data = filtered_data[filtered_data['preservation_status'] == status_filter]
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Tourism score chart
        fig = px.bar(filtered_data, x='name', y='tourism_score', 
                     color='preservation_status',
                     title='Tourism Potential Score by Art Form',
                     color_discrete_map={'Good': '#4CAF50', 'Excellent': '#2196F3', 
                                       'Fair': '#FFC107', 'At Risk': '#F44336'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category distribution
        category_counts = filtered_data['category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index,
                     title='Distribution by Category',
                     color_discrete_sequence=['#FF6B35', '#F7931E', '#F8B500', '#004643'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed information
    st.markdown("### 📋 Detailed Information")
    for idx, row in filtered_data.iterrows():
        with st.expander(f"{row['name']} - {row['state']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Category", row['category'])
            with col2:
                st.metric("Tourism Score", f"{row['tourism_score']}/100")
            with col3:
                status_color = {'Good': '🟢', 'Excellent': '🔵', 'Fair': '🟡', 'At Risk': '🔴'}
                st.metric("Status", f"{status_color.get(row['preservation_status'], '⚪')} {row['preservation_status']}")

# Cultural Experiences Page
elif page == "Cultural Experiences":
    st.title("🗺️ Cultural Experiences Map")
    
    # Interactive map
    fig = px.scatter_mapbox(cultural_sites, 
                           lat="lat", 
                           lon="lon", 
                           hover_name="site",
                           hover_data=["state", "visitors_2023"],
                           size="visitors_2023",
                           color="visitors_2023",
                           color_continuous_scale="Viridis",
                           size_max=30,
                           zoom=4,
                           height=600,
                           title="Major Cultural Sites and Visitor Traffic")
    
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
    
    # Site details
    st.markdown("### 🏛️ Cultural Site Analytics")
    
    # Top sites by visitors
    top_sites = cultural_sites.nlargest(5, 'visitors_2023')
    fig = px.bar(top_sites, x='visitors_2023', y='site', orientation='h',
                 title='Top 5 Most Visited Cultural Sites (2023)',
                 color='visitors_2023',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

# Tourism Analytics Page
elif page == "Tourism Analytics":
    st.title("📊 Tourism Analytics Dashboard")
    
    # Time series analysis
    st.markdown("### 📈 Tourism Trends (2023)")
    
    # Prepare data for visualization
    tourism_data['total_tourists'] = tourism_data['domestic_tourists'] + tourism_data['international_tourists']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tourism_data['month'], y=tourism_data['domestic_tourists'],
                            name='Domestic Tourists', line=dict(color='#FF6B35', width=3)))
    fig.add_trace(go.Scatter(x=tourism_data['month'], y=tourism_data['international_tourists'],
                            name='International Tourists', line=dict(color='#004643', width=3)))
    fig.add_trace(go.Scatter(x=tourism_data['month'], y=tourism_data['total_tourists'],
                            name='Total', line=dict(color='#F7931E', width=3, dash='dash')))
    
    fig.update_layout(title='Monthly Tourist Arrivals',
                     xaxis_title='Month',
                     yaxis_title='Number of Tourists',
                     height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonality insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌡️ Seasonality Insights")
        st.info("""
        **Peak Season (Oct-Mar):** 
        - 65% of annual tourist arrivals
        - Pleasant weather across most regions
        - Major festivals: Diwali, Durga Puja, Holi
        
        **Off-Season Opportunities:**
        - Monsoon tourism in Kerala, Western Ghats
        - Summer cultural festivals in hill stations
        - Lower accommodation costs
        """)
    
    with col2:
        st.markdown("### 🎯 Untapped Destinations")
        untapped = pd.DataFrame({
            'Destination': ['Majuli Island', 'Spiti Valley', 'Dholavira', 'Orchha', 'Bundi'],
            'State': ['Assam', 'Himachal Pradesh', 'Gujarat', 'Madhya Pradesh', 'Rajasthan'],
            'Potential': [85, 78, 82, 79, 76]
        })
        
        fig = px.bar(untapped, x='Destination', y='Potential',
                     title='Hidden Cultural Gems - Tourism Potential',
                     color='Potential',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

# Responsible Tourism Page
elif page == "Responsible Tourism":
    st.title("🌱 Responsible Tourism Guide")
    
    st.markdown("""
    ### 🤝 Our Commitment to Sustainable Cultural Tourism
    
    Responsible tourism ensures that India's cultural heritage is preserved for future generations 
    while benefiting local communities today.
    """)
    
    # Guidelines
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📜 For Travelers
        
        **Do's:**
        - ✅ Respect local customs and traditions
        - ✅ Support local artisans by buying authentic crafts
        - ✅ Use eco-friendly transportation when possible
        - ✅ Stay in locally-owned accommodations
        - ✅ Participate in cultural activities respectfully
        
        **Don'ts:**
        - ❌ Take photos without permission
        - ❌ Touch or damage historical monuments
        - ❌ Litter at cultural sites
        - ❌ Bargain unfairly with local artisans
        - ❌ Disrespect religious sentiments
        """)
    
    with col2:
        st.markdown("""
        #### 🏘️ Community Impact
        
        **Economic Benefits:**
        - 💰 Direct employment: 45 million jobs
        - 🏪 Local business growth: 23% annually
        - 🎨 Artisan income increase: 35% in tourist areas
        
        **Cultural Preservation:**
        - 📚 Documentation of 200+ art forms
        - 👥 Youth engagement programs
        - 🏛️ Monument restoration projects
        - 🎭 Festival revival initiatives
        """)
    
    # Impact calculator
    st.markdown("### 🧮 Your Tourism Impact Calculator")
    
    days = st.slider("Number of days traveling", 1, 30, 7)
    local_spending = st.slider("Daily spending on local products (₹)", 500, 5000, 2000)
    
    total_impact = days * local_spending
    jobs_supported = total_impact / 50000
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Economic Impact", f"₹{total_impact:,}")
    with col2:
        st.metric("Jobs Supported", f"₹{jobs_supported:.1f}")
    with col3:
        st.metric("Artisan Families Helped", f"{int(total_impact/15000)}")

# Data Insights Page
elif page == "Data Insights":
    st.title("📊 Government Data Insights")
    
    st.markdown("""
    ### 🏛️ Data Sources and Government Initiatives
    
    Our analysis is based on comprehensive data from various government sources:
    """)
    
    # Use the loaded government schemes data
    fig = px.bar(govt_schemes, x='scheme', y='budget_crores', 
                 title='Government Investment in Cultural Tourism Schemes',
                 color='budget_crores',
                 color_continuous_scale='Viridis',
                 text='budget_crores')
    fig.update_traces(texttemplate='₹%{text} Cr', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Add scheme details
    st.markdown("### 📋 Government Scheme Details")
    for idx, scheme in govt_schemes.iterrows():
        with st.expander(f"{scheme['scheme']} - {scheme['ministry']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Budget", f"₹{scheme['budget_crores']} Cr")
            with col2:
                st.metric("Sites Covered", scheme['sites_covered'] if scheme['sites_covered'] > 0 else "All States")
            with col3:
                st.metric("Launch Year", scheme['launch_year'])
            st.write(f"**Focus Area:** {scheme['focus_area']}")
    
    # Key findings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔍 Key Findings from Government Data
        
        1. **Tourism Growth**: 15.6% CAGR (2015-2023)
        2. **Digital Adoption**: 78% sites now have online presence
        3. **Infrastructure**: ₹12,000 Cr invested in last 5 years
        4. **Employment**: 1 in 10 jobs linked to tourism
        5. **Revenue**: ₹2.3 Lakh Cr contribution to GDP
        """)
    
    with col2:
        st.markdown("""
        #### 📈 Future Projections
        
        - **2025 Target**: 2.5 billion domestic tourists
        - **International**: 30 million foreign arrivals
        - **Revenue Goal**: ₹35 Lakh Cr by 2030
        - **Job Creation**: 140 million by 2030
        - **Sustainable Sites**: 100% by 2035
        """)
    
    # Data quality note
    st.info("""
    **Data Sources**: Ministry of Tourism, Archaeological Survey of India, UNESCO, 
    UNWTO, State Tourism Departments, and data.gov.in
    
    **Note**: This dashboard uses sample data for demonstration. In production, 
    it would connect to Snowflake for real-time government data integration.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ for preserving India's cultural heritage | Data updated: January 2024</p>
</div>
""", unsafe_allow_html=True)
