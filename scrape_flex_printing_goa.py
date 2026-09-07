#!/usr/bin/env python3
"""
Scrape flex print shops in Goa, India
Location: 15.2993°N, 74.1240°E
"""

import json
import time
import requests
from datetime import datetime

# Goa coordinates
LAT = 15.2993
LON = 74.1240
SEARCH_QUERY = "flex print shop"
RADIUS = 5000  # 5km radius

def scrape_flex_print_shops():
    """Scrape flex print shops in Goa using Google Maps API"""
    
    print(f"Starting flex print shop search in Goa")
    print(f"Coordinates: {LAT}°N, {LON}°E")
    print(f"Search query: '{SEARCH_QUERY}'")
    print(f"Search radius: {RADIUS}m")
    print("-" * 60)
    
    payload = {
        "keywords": ["flex print shop", "flex printing", "digital printing"],
        "lat": str(LAT),
        "lon": str(LON),
        "max_time": 600,
        "depth": 1
    }
    
    try:
        # Create scraping job
        print("\n[1/3] Creating scraping job...")
        response = requests.post(
            "http://localhost:8080/api/v1/jobs",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        job_data = response.json()
        job_id = job_data.get('id')
        print(f"✓ Job created: {job_id}")
        
        # Poll for results
        print("\n[2/3] Polling for results...")
        max_attempts = 120  # 10 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            status_response = requests.get(
                f"http://localhost:8080/api/v1/jobs/{job_id}",
                timeout=10
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data.get('Status', 'unknown')
            
            if status == 'ok':
                print(f"✓ Scrape completed (attempt {attempt})")
                break
            else:
                print(f"  Status: {status} (attempt {attempt}/{max_attempts})")
                time.sleep(5)
        else:
            print("✗ Timeout waiting for results")
            return False
        
        # Fetch results
        print("\n[3/3] Fetching results...")
        results_response = requests.get(
            f"http://localhost:8080/api/v1/jobs/{job_id}/results",
            timeout=10
        )
        results_response.raise_for_status()
        results = results_response.json()
        
        # Save results
        output_file = "flex_printing_goa_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "search_params": {
                    "location": "Goa, India",
                    "latitude": LAT,
                    "longitude": LON,
                    "query": SEARCH_QUERY,
                    "radius_meters": RADIUS,
                    "timestamp": datetime.now().isoformat()
                },
                "job_id": job_id,
                "results": results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Results saved to {output_file}")
        
        # Display summary
        if isinstance(results, list):
            print(f"\n📍 Found {len(results)} flex print shops in Goa")
            print("\nTop results:")
            for idx, shop in enumerate(results[:5], 1):
                name = shop.get('name', 'N/A')
                address = shop.get('address', 'N/A')
                rating = shop.get('rating', 'N/A')
                print(f"\n{idx}. {name}")
                print(f"   Address: {address}")
                print(f"   Rating: {rating}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to scraper API at localhost:8080")
        print("  Make sure the scraper is running: python main.py")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = scrape_flex_print_shops()
    exit(0 if success else 1)
