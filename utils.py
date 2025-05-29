import pandas as pd
import json
from datetime import datetime, timedelta

def calculate_seasonality_index(df, date_column, value_column):
    """Calculate seasonality index for tourism data"""
    df['month'] = pd.to_datetime(df[date_column]).dt.month
    monthly_avg = df.groupby('month')[value_column].mean()
    overall_avg = df[value_column].mean()
    seasonality_index = (monthly_avg / overall_avg * 100).round(2)
    return seasonality_index

def identify_untapped_destinations(sites_df, threshold_percentile=25):
    """Identify cultural sites with high potential but low current tourism"""
    # Calculate potential score based on various factors
    sites_df['potential_score'] = (
        sites_df['cultural_significance'] * 0.3 +
        sites_df['infrastructure_rating'] * 0.2 +
        sites_df['accessibility_score'] * 0.2 +
        (100 - sites_df['tourism_saturation']) * 0.3
    )
    
    # Filter sites below tourism threshold but high potential
    low_tourism = sites_df['annual_visitors'] < sites_df['annual_visitors'].quantile(threshold_percentile/100)
    high_potential = sites_df['potential_score'] > sites_df['potential_score'].quantile(0.75)
    
    untapped = sites_df[low_tourism & high_potential].sort_values('potential_score', ascending=False)
    return untapped

def calculate_economic_impact(visitors, avg_spending_per_day=2500, avg_stay_days=3):
    """Calculate economic impact of tourism"""
    direct_revenue = visitors * avg_spending_per_day * avg_stay_days
    
    # Multiplier effect (conservative estimate)
    multiplier = 1.5
    total_impact = direct_revenue * multiplier
    
    # Job creation (1 job per ₹15 lakh annual revenue)
    jobs_created = total_impact / 1500000
    
    return {
        'direct_revenue': direct_revenue,
        'total_economic_impact': total_impact,
        'jobs_supported': int(jobs_created),
        'tax_revenue': total_impact * 0.18  # Assuming 18% tax rate
    }

def generate_recommendations(user_preferences, cultural_sites, art_forms):
    """Generate personalized cultural tourism recommendations"""
    recommendations = []
    
    # Filter based on preferences
    if user_preferences.get('preferred_states'):
        cultural_sites = cultural_sites[
            cultural_sites['state'].isin(user_preferences['preferred_states'])
        ]
        art_forms = art_forms[
            art_forms['origin_state'].isin(user_preferences['preferred_states'])
        ]
    
    if user_preferences.get('art_categories'):
        art_forms = art_forms[
            art_forms['category'].isin(user_preferences['art_categories'])
        ]
    
    # Score and rank recommendations
    for _, site in cultural_sites.iterrows():
        score = calculate_recommendation_score(site, user_preferences)
        recommendations.append({
            'type': 'cultural_site',
            'name': site['site_name'],
            'state': site['state'],
            'score': score,
            'description': f"Visit {site['site_name']} in {site['state']}"
        })
    
    for _, art in art_forms.iterrows():
        score = calculate_recommendation_score(art, user_preferences)
        recommendations.append({
            'type': 'art_form',
            'name': art['art_form_name'],
            'state': art['origin_state'],
            'score': score,
            'description': f"Experience {art['art_form_name']} from {art['origin_state']}"
        })
    
    # Sort by score and return top recommendations
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations[:10]

def calculate_recommendation_score(item, preferences):
    """Calculate recommendation score based on user preferences"""
    score = 50  # Base score
    
    # Adjust based on preferences
    if preferences.get('prefer_offbeat') and item.get('tourism_saturation', 50) < 30:
        score += 20
    
    if preferences.get('prefer_unesco') and item.get('unesco_status'):
        score += 15
    
    if preferences.get('budget_conscious') and item.get('avg_cost_rating', 3) <= 2:
        score += 10
    
    return min(score, 100)
