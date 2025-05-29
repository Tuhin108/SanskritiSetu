"""
Data loading utilities for the Cultural Tourism Dashboard
Handles sample data and future integration with real data sources
"""

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import random
from config import SAMPLE_DATA_CONFIG, TOURISM_METRICS

@st.cache_data(ttl=SAMPLE_DATA_CONFIG["data_refresh_interval"])
def load_government_tourism_stats():
    """
    Load tourism statistics - currently using sample data
    In production, this would connect to data.gov.in APIs
    """
    
    # Generate realistic monthly data for 2023
    months = pd.date_range('2023-01', periods=12, freq='M')
    
    # Seasonal patterns based on actual tourism trends
    seasonal_multipliers = [1.2, 1.3, 1.4, 1.1, 0.8, 0.6, 0.5, 0.6, 0.9, 1.5, 1.7, 1.8]
    base_domestic = 150000000  # Monthly base
    base_international = 800000  # Monthly base
    
    tourism_stats = pd.DataFrame({
        'month': months,
        'domestic_tourists': [int(base_domestic * mult) for mult in seasonal_multipliers],
        'international_tourists': [int(base_international * mult) for mult in seasonal_multipliers],
        'revenue_crores': [int(base_domestic * mult * 0.002) for mult in seasonal_multipliers],
        'hotel_occupancy': [min(95, max(35, 60 + mult * 15)) for mult in seasonal_multipliers]
    })
    
    return tourism_stats

@st.cache_data
def load_cultural_heritage_sites():
    """
    Load cultural heritage sites data
    Based on ASI and UNESCO data
    """
    
    sites_data = {
        'site_name': [
            'Taj Mahal', 'Red Fort', 'Qutub Minar', 'Humayun Tomb', 'Agra Fort',
            'Ajanta Caves', 'Ellora Caves', 'Elephanta Caves', 'Chhatrapati Shivaji Terminus',
            'Western Ghats', 'Hampi', 'Pattadakal', 'Mysore Palace', 'Gol Gumbaz',
            'Khajuraho Temples', 'Sanchi Stupa', 'Bhimbetka Rock Shelters',
            'Konark Sun Temple', 'Jagannath Temple', 'Lingaraj Temple',
            'Mahabalipuram', 'Brihadeeswara Temple', 'Airavatesvara Temple',
            'Meenakshi Temple', 'Rameshwaram Temple', 'Kanchipuram Temples',
            'Amber Fort', 'Hawa Mahal', 'City Palace Jaipur', 'Jantar Mantar',
            'Mehrangarh Fort', 'Umaid Bhawan Palace', 'Jaisalmer Fort',
            'Chittorgarh Fort', 'Kumbhalgarh Fort', 'Ranthambore Fort'
        ],
        'state': [
            'Uttar Pradesh', 'Delhi', 'Delhi', 'Delhi', 'Uttar Pradesh',
            'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra',
            'Karnataka', 'Karnataka', 'Karnataka', 'Karnataka',
            'Madhya Pradesh', 'Madhya Pradesh', 'Madhya Pradesh',
            'Odisha', 'Odisha', 'Odisha',
            'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu',
            'Rajasthan', 'Rajasthan', 'Rajasthan', 'Rajasthan',
            'Rajasthan', 'Rajasthan', 'Rajasthan', 'Rajasthan', 'Rajasthan', 'Rajasthan'
        ],
        'type': [
            'Mausoleum', 'Fort', 'Monument', 'Tomb', 'Fort',
            'Cave', 'Cave', 'Cave', 'Railway Station', 'Natural',
            'Ruins', 'Temple Complex', 'Palace', 'Mausoleum',
            'Temple Complex', 'Stupa', 'Rock Art', 'Temple', 'Temple', 'Temple',
            'Temple Complex', 'Temple', 'Temple', 'Temple', 'Temple', 'Temple Complex',
            'Fort', 'Palace', 'Palace', 'Observatory',
            'Fort', 'Palace', 'Fort', 'Fort', 'Fort', 'Fort'
        ],
        'unesco_status': [
            True, True, True, True, True,
            True, True, True, True, True,
            True, True, False, False,
            True, True, True,
            True, False, False,
            True, True, True,
            False, False, False,
            False, False, False, True,
            False, False, False, False, False, False
        ]
    }
    
    df = pd.DataFrame(sites_data)
    
    # Add synthetic visitor data and coordinates
    df['annual_visitors_2023'] = [random.randint(100000, 8000000) for _ in range(len(df))]
    df['latitude'] = [
        27.1751, 28.6562, 28.5244, 28.5933, 27.1767,
        20.5519, 20.0269, 18.9633, 18.9398, 16.0000,
        15.3350, 15.3647, 12.3051, 16.8302,
        24.8318, 23.4793, 22.9734,
        19.8876, 19.8135, 20.2961,
        12.6208, 10.7905, 11.0168,
        9.9252, 9.2881, 12.8266,
        26.9855, 26.9239, 26.9260, 26.9124,
        26.2389, 26.2124, 26.9157, 24.8829, 25.1462, 26.0173
    ]
    df['longitude'] = [
        78.0421, 77.2410, 77.1855, 77.2507, 78.0081,
        75.7033, 75.1789, 72.9347, 72.8347, 77.0000,
        76.4601, 75.8269, 76.6551, 75.7100,
        79.9199, 77.7398, 77.5946,
        86.0945, 85.8312, 85.8245,
        80.1982, 79.1378, 79.0747,
        78.1198, 79.3129, 79.7036,
        75.8513, 75.8267, 75.8235, 75.8235,
        73.0169, 73.0390, 70.9083, 74.6399, 73.5851, 76.1300
    ]
    
    return df

@st.cache_data
def load_traditional_arts():
    """
    Load traditional arts and crafts data
    """
    
    arts_data = {
        'art_form': [
            'Bharatanatyam', 'Kathak', 'Kathakali', 'Kuchipudi', 'Odissi', 'Manipuri', 'Mohiniyattam', 'Sattriya',
            'Madhubani', 'Warli', 'Pattachitra', 'Kalamkari', 'Tanjore Painting', 'Mysore Painting',
            'Dhokra', 'Blue Pottery', 'Channapatna Toys', 'Kondapalli Toys', 'Etikoppaka Toys',
            'Pashmina', 'Banarasi Silk', 'Kanjeevaram Silk', 'Pochampally Ikat', 'Bandhani',
            'Carnatic Music', 'Hindustani Music', 'Rabindra Sangeet', 'Qawwali',
            'Kalaripayattu', 'Gatka', 'Thang-Ta', 'Silambam'
        ],
        'category': [
            'Dance', 'Dance', 'Dance', 'Dance', 'Dance', 'Dance', 'Dance', 'Dance',
            'Painting', 'Painting', 'Painting', 'Painting', 'Painting', 'Painting',
            'Craft', 'Craft', 'Craft', 'Craft', 'Craft',
            'Textile', 'Textile', 'Textile', 'Textile', 'Textile',
            'Music', 'Music', 'Music', 'Music',
            'Martial Art', 'Martial Art', 'Martial Art', 'Martial Art'
        ],
        'origin_state': [
            'Tamil Nadu', 'Uttar Pradesh', 'Kerala', 'Andhra Pradesh', 'Odisha', 'Manipur', 'Kerala', 'Assam',
            'Bihar', 'Maharashtra', 'Odisha', 'Andhra Pradesh', 'Tamil Nadu', 'Karnataka',
            'West Bengal', 'Rajasthan', 'Karnataka', 'Andhra Pradesh', 'Andhra Pradesh',
            'Kashmir', 'Uttar Pradesh', 'Tamil Nadu', 'Telangana', 'Gujarat',
            'Tamil Nadu', 'North India', 'West Bengal', 'North India',
            'Kerala', 'Punjab', 'Manipur', 'Tamil Nadu'
        ],
        'practitioners_estimated': [
            50000, 30000, 8000, 15000, 12000, 3000, 2000, 1500,
            25000, 5000, 8000, 12000, 3000, 2000,
            2000, 1500, 5000, 800, 600,
            10000, 50000, 30000, 15000, 20000,
            100000, 150000, 25000, 5000,
            5000, 8000, 500, 3000
        ],
        'tourism_integration': [
            95, 85, 90, 80, 85, 70, 75, 60,
            70, 65, 75, 70, 80, 75,
            60, 85, 70, 55, 50,
            90, 95, 90, 70, 80,
            85, 80, 70, 65,
            75, 70, 40, 65
        ]
    }
    
    df = pd.DataFrame(arts_data)
    
    # Add preservation status based on practitioners and tourism integration
    def get_preservation_status(practitioners, tourism):
        if practitioners > 20000 and tourism > 80:
            return 'Excellent'
        elif practitioners > 10000 and tourism > 70:
            return 'Good'
        elif practitioners > 2000 and tourism > 50:
            return 'Fair'
        else:
            return 'At Risk'
    
    df['preservation_status'] = df.apply(
        lambda row: get_preservation_status(row['practitioners_estimated'], row['tourism_integration']), 
        axis=1
    )
    
    return df

def get_data_sources_info():
    """
    Return information about data sources
    """
    return {
        "current_status": "Sample Data",
        "sources": [
            "Ministry of Tourism, Government of India",
            "Archaeological Survey of India (ASI)",
            "UNESCO World Heritage Centre",
            "State Tourism Development Corporations",
            "National Sample Survey Office (NSSO)",
            "India Tourism Statistics (ITS)"
        ],
        "apis_available": [
            "data.gov.in - Open Government Data Platform",
            "incredibleindia.org - Official Tourism Portal",
            "asi.nic.in - Archaeological Survey Data"
        ],
        "update_frequency": "Sample data refreshes every hour",
        "note": "This dashboard uses representative sample data. In production, it would integrate with real-time government databases."
    }
