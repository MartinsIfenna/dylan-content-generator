#!/usr/bin/env python3
"""
Enhanced Market Data Provider for Dylan Steman Content Generator
Integrates FRED, Census Bureau, BLS, and Zillow Research Data
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import time

load_dotenv()

class EnhancedMarketDataProvider:
    """Enhanced market data provider integrating multiple free APIs"""
    
    def __init__(self):
        self.fred_api_key = os.getenv('FRED_API_KEY')
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
        
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        return (datetime.now() - self.cache[key]['timestamp']).seconds < self.cache_duration
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def get_fred_economic_indicators(self) -> Dict:
        """Get key economic indicators from FRED"""
        cache_key = 'fred_indicators'
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        indicators = {}
        
        # Core economic indicators for CRE analysis
        series_list = [
            ('FEDFUNDS', 'Federal Funds Rate'),
            ('GS10', '10-Year Treasury Rate'),
            ('GS5', '5-Year Treasury Rate'),
            ('MORTGAGE30US', '30-Year Fixed Mortgage Rate'),
            ('UNRATE', 'National Unemployment Rate'),
            ('CPIAUCSL', 'Consumer Price Index'),
            ('HOUST', 'Housing Starts'),
            ('PERMIT', 'Building Permits'),
            ('CSUSHPISA', 'Case-Shiller Home Price Index'),
            ('RHORUSQ156N', 'Homeownership Rate'),
            ('GDPC1', 'Real GDP'),
            ('PAYEMS', 'Total Nonfarm Payrolls')
        ]
        
        for series_id, name in series_list:
            try:
                url = "https://api.stlouisfed.org/fred/series/observations"
                params = {
                    'series_id': series_id,
                    'api_key': self.fred_api_key,
                    'file_type': 'json',
                    'limit': 1,
                    'sort_order': 'desc'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'observations' in data and len(data['observations']) > 0:
                        latest = data['observations'][0]
                        if latest['value'] != '.':  # FRED uses '.' for missing data
                            indicators[series_id] = {
                                'name': name,
                                'value': float(latest['value']),
                                'date': latest['date'],
                                'source': 'Federal Reserve Economic Data (FRED)'
                            }
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                continue
        
        self._cache_data(cache_key, indicators)
        return indicators
    
    def get_metro_demographics(self) -> Dict:
        """Get demographic data for key metros from Census Bureau"""
        cache_key = 'census_demographics'
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        demographics = {}
        
        # Key metros for Dylan's content
        metros = {
            '16980': 'Chicago-Naperville-Elgin, IL-IN-WI',
            '33460': 'Minneapolis-St. Paul-Bloomington, MN-WI',
            '14460': 'Boston-Cambridge-Newton, MA-NH',
            '33100': 'Miami-Fort Lauderdale-West Palm Beach, FL',
            '19100': 'Dallas-Fort Worth-Arlington, TX',
            '26420': 'Houston-The Woodlands-Sugar Land, TX',
            '40140': 'Riverside-San Bernardino-Ontario, CA'
        }
        
        # Key variables for CRE analysis
        variables = {
            'B25001_001E': 'Total Housing Units',
            'B25003_002E': 'Owner Occupied Units',
            'B25003_003E': 'Renter Occupied Units',
            'B25064_001E': 'Median Gross Rent',
            'B19013_001E': 'Median Household Income',
            'B25077_001E': 'Median Home Value',
            'B25024_006E': 'Buildings 5-9 Units',
            'B25024_007E': 'Buildings 10-19 Units',
            'B25024_008E': 'Buildings 20-49 Units',
            'B25024_009E': 'Buildings 50+ Units'
        }
        
        var_string = ','.join(variables.keys())
        
        for metro_code, metro_name in metros.items():
            try:
                url = "https://api.census.gov/data/2022/acs/acs5"
                params = {
                    'get': var_string,
                    'for': f'metropolitan statistical area/micropolitan statistical area:{metro_code}'
                }
                
                response = requests.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1:
                        metro_data = {}
                        values = data[1]
                        
                        for i, var_code in enumerate(variables.keys()):
                            if i < len(values) and values[i] not in [None, '-', '']:
                                try:
                                    metro_data[var_code] = {
                                        'name': variables[var_code],
                                        'value': int(values[i]),
                                        'source': 'U.S. Census Bureau, ACS 2022 5-Year Estimates'
                                    }
                                except (ValueError, TypeError):
                                    continue
                        
                        if metro_data:
                            demographics[metro_code] = {
                                'metro_name': metro_name,
                                'data': metro_data
                            }
                
                time.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                print(f"Error fetching census data for {metro_name}: {e}")
                continue
        
        self._cache_data(cache_key, demographics)
        return demographics
    
    def get_employment_data(self) -> Dict:
        """Get employment data from Bureau of Labor Statistics"""
        cache_key = 'bls_employment'
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
        
        employment_data = {}
        
        # Metro unemployment rates
        metro_series = {
            'LAUMT171698000000003': 'Chicago-Naperville-Elgin Unemployment Rate',
            'LAUMT273346000000003': 'Minneapolis-St. Paul Unemployment Rate',
            'LAUMT251446000000003': 'Boston-Cambridge-Newton Unemployment Rate',
            'LAUMT123310000000003': 'Miami-Fort Lauderdale Unemployment Rate'
        }
        
        # National employment series
        national_series = {
            'CES0000000001': 'Total Nonfarm Employment',
            'CES2000000001': 'Construction Employment',
            'CES5553000001': 'Real Estate Employment'
        }
        
        all_series = {**metro_series, **national_series}
        
        for series_id, name in all_series.items():
            try:
                url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
                current_year = datetime.now().year
                
                payload = {
                    "seriesid": [series_id],
                    "startyear": str(current_year - 1),
                    "endyear": str(current_year),
                    "catalog": False
                }
                
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'REQUEST_SUCCEEDED' and data['Results']['series']:
                        series_data = data['Results']['series'][0]['data']
                        if series_data:
                            latest = series_data[0]
                            employment_data[series_id] = {
                                'name': name,
                                'value': float(latest['value']),
                                'date': f"{latest['year']}-{latest['period'][1:].zfill(2)}",
                                'source': 'U.S. Bureau of Labor Statistics'
                            }
                
                time.sleep(0.5)  # BLS rate limiting
                
            except Exception as e:
                print(f"Error fetching BLS data for {name}: {e}")
                continue
        
        self._cache_data(cache_key, employment_data)
        return employment_data
    
    def get_market_insights_for_content(self, topic: str = None) -> Dict:
        """Get comprehensive market insights formatted for content generation"""
        
        # Fetch all data sources
        fred_data = self.get_fred_economic_indicators()
        demographics = self.get_metro_demographics()
        employment = self.get_employment_data()
        
        # Format insights for content generation
        insights = {
            'economic_context': {},
            'regional_markets': {},
            'key_metrics': {},
            'data_sources': set()
        }
        
        # Economic context from FRED
        if 'FEDFUNDS' in fred_data:
            insights['economic_context']['fed_funds_rate'] = {
                'value': fred_data['FEDFUNDS']['value'],
                'date': fred_data['FEDFUNDS']['date'],
                'formatted': f"{fred_data['FEDFUNDS']['value']}% (as of {fred_data['FEDFUNDS']['date']})"
            }
            insights['data_sources'].add('Federal Reserve Economic Data (FRED)')
        
        if 'GS10' in fred_data:
            insights['economic_context']['treasury_10y'] = {
                'value': fred_data['GS10']['value'],
                'date': fred_data['GS10']['date'],
                'formatted': f"{fred_data['GS10']['value']}% (as of {fred_data['GS10']['date']})"
            }
        
        if 'MORTGAGE30US' in fred_data:
            insights['economic_context']['mortgage_rate'] = {
                'value': fred_data['MORTGAGE30US']['value'],
                'date': fred_data['MORTGAGE30US']['date'],
                'formatted': f"{fred_data['MORTGAGE30US']['value']}% (as of {fred_data['MORTGAGE30US']['date']})"
            }
        
        if 'HOUST' in fred_data:
            insights['economic_context']['housing_starts'] = {
                'value': fred_data['HOUST']['value'],
                'date': fred_data['HOUST']['date'],
                'formatted': f"{fred_data['HOUST']['value']:,.0f}K units (as of {fred_data['HOUST']['date']})"
            }
        
        # Regional market data from Census
        for metro_code, metro_info in demographics.items():
            metro_name = metro_info['metro_name'].split(',')[0]  # Simplified name
            metro_data = metro_info['data']
            
            regional_info = {
                'full_name': metro_info['metro_name'],
                'short_name': metro_name
            }
            
            if 'B25064_001E' in metro_data:
                regional_info['median_rent'] = {
                    'value': metro_data['B25064_001E']['value'],
                    'formatted': f"${metro_data['B25064_001E']['value']:,}/month"
                }
            
            if 'B19013_001E' in metro_data:
                regional_info['median_income'] = {
                    'value': metro_data['B19013_001E']['value'],
                    'formatted': f"${metro_data['B19013_001E']['value']:,}"
                }
            
            # Calculate multifamily units percentage
            total_units = metro_data.get('B25001_001E', {}).get('value', 0)
            mf_units = (
                metro_data.get('B25024_006E', {}).get('value', 0) +  # 5-9 units
                metro_data.get('B25024_007E', {}).get('value', 0) +  # 10-19 units
                metro_data.get('B25024_008E', {}).get('value', 0) +  # 20-49 units
                metro_data.get('B25024_009E', {}).get('value', 0)    # 50+ units
            )
            
            if total_units > 0:
                mf_percentage = (mf_units / total_units) * 100
                regional_info['multifamily_share'] = {
                    'value': mf_percentage,
                    'formatted': f"{mf_percentage:.1f}% multifamily"
                }
            
            insights['regional_markets'][metro_code] = regional_info
            insights['data_sources'].add('U.S. Census Bureau')
        
        # Employment context from BLS
        for series_id, emp_data in employment.items():
            if 'Unemployment Rate' in emp_data['name']:
                metro_key = emp_data['name'].replace(' Unemployment Rate', '').lower()
                insights['key_metrics'][f'{metro_key}_unemployment'] = {
                    'value': emp_data['value'],
                    'date': emp_data['date'],
                    'formatted': f"{emp_data['value']}% unemployment (as of {emp_data['date']})"
                }
                insights['data_sources'].add('U.S. Bureau of Labor Statistics')
        
        # Convert data sources set to list for JSON serialization
        insights['data_sources'] = list(insights['data_sources'])
        
        return insights
    
    def get_content_ready_data_summary(self) -> str:
        """Get a formatted summary of current market data for content generation"""
        insights = self.get_market_insights_for_content()
        
        summary_parts = []
        
        # Economic context
        if insights['economic_context']:
            summary_parts.append("**Current Economic Environment:**")
            
            if 'fed_funds_rate' in insights['economic_context']:
                summary_parts.append(f"• Federal Funds Rate: {insights['economic_context']['fed_funds_rate']['formatted']}")
            
            if 'treasury_10y' in insights['economic_context']:
                summary_parts.append(f"• 10-Year Treasury: {insights['economic_context']['treasury_10y']['formatted']}")
            
            if 'mortgage_rate' in insights['economic_context']:
                summary_parts.append(f"• 30-Year Mortgage Rate: {insights['economic_context']['mortgage_rate']['formatted']}")
            
            if 'housing_starts' in insights['economic_context']:
                summary_parts.append(f"• Housing Starts: {insights['economic_context']['housing_starts']['formatted']}")
        
        # Regional highlights
        if insights['regional_markets']:
            summary_parts.append("\n**Regional Market Highlights:**")
            
            for metro_code, metro_info in list(insights['regional_markets'].items())[:3]:  # Top 3 metros
                metro_line = f"• {metro_info['short_name']}: "
                details = []
                
                if 'median_rent' in metro_info:
                    details.append(f"Median rent {metro_info['median_rent']['formatted']}")
                
                if 'multifamily_share' in metro_info:
                    details.append(metro_info['multifamily_share']['formatted'])
                
                if details:
                    metro_line += ", ".join(details)
                    summary_parts.append(metro_line)
        
        # Data sources
        if insights['data_sources']:
            summary_parts.append(f"\n**Sources:** {', '.join(insights['data_sources'])}")
        
        return "\n".join(summary_parts)

def main():
    """Test the enhanced market data provider"""
    print("🚀 Testing Enhanced Market Data Provider")
    print("=" * 50)
    
    provider = EnhancedMarketDataProvider()
    
    # Test data fetching
    print("📊 Fetching FRED economic indicators...")
    fred_data = provider.get_fred_economic_indicators()
    print(f"✅ Retrieved {len(fred_data)} FRED indicators")
    
    print("\n🏘️  Fetching Census demographic data...")
    demographics = provider.get_metro_demographics()
    print(f"✅ Retrieved data for {len(demographics)} metros")
    
    print("\n💼 Fetching BLS employment data...")
    employment = provider.get_employment_data()
    print(f"✅ Retrieved {len(employment)} employment series")
    
    print("\n📋 Generating content-ready summary...")
    summary = provider.get_content_ready_data_summary()
    print("\n" + "="*50)
    print("CONTENT-READY DATA SUMMARY:")
    print("="*50)
    print(summary)
    
    # Save comprehensive data
    insights = provider.get_market_insights_for_content()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_market_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(insights, f, indent=2, default=str)
    
    print(f"\n💾 Comprehensive data saved to: {filename}")
    print("🎉 Enhanced market data provider test complete!")

if __name__ == "__main__":
    main()
