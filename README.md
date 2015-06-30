# AWS Price Analysis
Use Flask to return pricing analysis information between Spot Instances and EC2 from Amazon’s public API endpoints in the format of your choosing (XML, JSON, etc).

## Endpoints
 * On-demand: http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js
 * Spot: http://spot-price.s3.amazonaws.com/spot.js

## Feature Requirements
 * Return the demand/spot price spread by instance type and region
 * Return the top 10 price per vCPU instances across all regions
 * Return the cheapest region overall

# URL
https://awspriceanalysis.herokuapp.com/
