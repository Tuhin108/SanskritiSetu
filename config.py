"""
Configuration file for the Cultural Tourism Dashboard
This file contains settings and can be extended to include API keys when available
"""

# App Configuration
APP_TITLE = "India Cultural Heritage & Tourism"
APP_ICON = "🎭"

# Data Sources (for future integration)
DATA_SOURCES = {
    "government": "https://data.gov.in",
    "tourism_ministry": "https://tourism.gov.in",
    "asi": "https://asi.nic.in",
    "unesco": "https://whc.unesco.org"
}

# Sample data configuration
SAMPLE_DATA_CONFIG = {
    "use_sample_data": True,  # Set to False when real data sources are available
    "data_refresh_interval": 3600,  # 1 hour in seconds
}

# Color scheme for visualizations
COLOR_SCHEME = {
    "primary": "#FF6B35",
    "secondary": "#004643", 
    "accent": "#F7931E",
    "success": "#4CAF50",
    "warning": "#FFC107",
    "danger": "#F44336",
    "info": "#2196F3"
}

# Tourism metrics (based on government data)
TOURISM_METRICS = {
    "total_heritage_sites": 3691,
    "unesco_sites": 40,
    "annual_domestic_tourists": 1900000000,  # 1.9 billion
    "annual_international_tourists": 10930000,  # 10.93 million
    "tourism_gdp_contribution": 15200000000000,  # ₹15.2 trillion
    "employment_millions": 45
}

# States and their cultural significance
STATES_DATA = {
    "Rajasthan": {"forts": 15, "palaces": 25, "art_forms": 12},
    "Kerala": {"backwaters": 5, "art_forms": 8, "ayurveda_centers": 200},
    "Tamil Nadu": {"temples": 300, "dance_forms": 5, "crafts": 15},
    "Karnataka": {"heritage_sites": 25, "classical_music": True, "crafts": 20},
    "Maharashtra": {"caves": 8, "forts": 20, "folk_arts": 10}
}
