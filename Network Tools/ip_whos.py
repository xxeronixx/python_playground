import csv
from tqdm import tqdm  # Import tqdm for the progress bar
from ipwhois import IPWhois
import concurrent.futures
import pycountry


# Function to get the country and region for an IP address using the ipwhois library
def get_country_and_region(ip):
    try:
        # Query the IP address using ipwhois
        ipwhois = IPWhois(ip)
        result = ipwhois.lookup_rdap()

        # Extract the country and region information
        country_abbr = result['asn_country_code']
        region = result['network']['country']

        # Convert country abbreviation to full name
        country = pycountry.countries.get(alpha_2=country_abbr)
        if country:
            country = country.name
        else:
            country = "Unknown"

        return country, region
    except Exception:
        return "Unknown", "Unknown"  # Return "Unknown" for IP addresses with no information


# Read IP addresses from the file
with open("ip_addresses.txt", "r") as file:
    ip_addresses = file.read().splitlines()

# Create a dictionary to store IPs by country and region
countries_and_regions = {}

# Create a dictionary to store counts of IPs per region
region_counts = {}

# Calculate the total number of provided IPs
total_ips = len(ip_addresses)


# Function to process an IP address and add it to the dictionary
def process_ip(ip):
    country, region = get_country_and_region(ip)

    # Handle cases where country or region is "Unknown"
    if country == "Unknown" or region == "Unknown":
        if "Unknown" not in countries_and_regions:
            countries_and_regions["Unknown"] = {}
        if "Unknown" not in region_counts:
            region_counts["Unknown"] = 0
        countries_and_regions["Unknown"]["Unknown"] = countries_and_regions["Unknown"].get("Unknown", []) + [ip]
        region_counts["Unknown"] += 1
    else:
        # Add the IP address to the corresponding country-region dictionary
        if country not in countries_and_regions:
            countries_and_regions[country] = {}
        if region not in countries_and_regions[country]:
            countries_and_regions[country][region] = []
        countries_and_regions[country][region].append(ip)

        # Update the count for the region, limiting it to the total number of provided IPs
        region_counts[region] = min(region_counts.get(region, 0) + 1, total_ips)


# Create a tqdm progress bar
with tqdm(total=len(ip_addresses)) as pbar:
    # Use concurrent.futures to perform IP lookups concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the IP processing tasks to the executor
        futures = [executor.submit(process_ip, ip) for ip in ip_addresses]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            pbar.update(1)  # Update the progress bar for each completed task

# Create a CSV file
with open("ip_addresses_by_country_and_region.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write headers
    csv_writer.writerow(["Country", "Region", "IP Addresses", "IP Count"])

    # Write data
    for country, regions in countries_and_regions.items():
        for region, ips in regions.items():
            csv_writer.writerow([country, region, ", ".join(ips), region_counts.get(region, 0)])

print("CSV file 'ip_addresses_by_country_and_region.csv' created.")