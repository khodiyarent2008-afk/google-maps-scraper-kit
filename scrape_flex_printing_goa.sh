#!/bin/bash

# Scrape flex printing businesses in Goa, India
# Coordinates: 15.2993°N, 74.1240°E

echo "Starting flex printing search in Goa..."

curl -X POST http://localhost:8080/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["flex printing", "flex print shop", "digital flex printing"],
    "lat": "15.2993",
    "lon": "74.1240",
    "max_time": 300,
    "depth": 1
  }' > job_response.json

# Extract job ID
JOB_ID=$(jq -r '.id' job_response.json)
echo "Job ID: $JOB_ID"

# Poll for completion
echo "Polling for results..."
for i in {1..60}; do
  STATUS=$(curl -s http://localhost:8080/api/v1/jobs/$JOB_ID | jq -r '.Status')
  echo "Attempt $i - Status: $STATUS"
  
  if [ "$STATUS" = "ok" ]; then
    echo "Scrape complete! Fetching results..."
    curl -s http://localhost:8080/api/v1/jobs/$JOB_ID/results > flex_printing_goa_results.json
    echo "Results saved to flex_printing_goa_results.json"
    exit 0
  fi
  
  sleep 5
done

echo "Timeout waiting for results"
exit 1
