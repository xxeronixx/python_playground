import nmap
import requests
from bs4 import BeautifulSoup
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor

subnet = "10.0.1"  # Specify your subnet here
output_file = "web_hosts.html"

# Initialize Nmap PortScanner
nm = nmap.PortScanner()

# Create an empty HTML file
with open(output_file, "w") as file:
    file.write("")


# Function to check if a web page is hosted on a specific port of an IP
def check_web_page(ip, port):
    http_url = f"http://{ip}:{port}"
    https_url = f"https://{ip}:{port}"

    try:
        # Check if the IP is hosting a web page on the current port using HTTP
        http_response = requests.get(http_url, timeout=5)
        if http_response.status_code == 200:
            return f"<a href='{http_url}'>{ip}:{port} (HTTP)</a><br>"
    except requests.exceptions.RequestException:
        pass

    try:
        # Check if the IP is hosting a web page on the current port using HTTPS
        https_response = requests.get(https_url, timeout=5)
        if https_response.status_code == 200:
            return f"<a href='{https_url}'>{ip}:{port} (HTTPS)</a><br>"
    except requests.exceptions.RequestException:
        pass

    return ""


# Perform port scanning on each IP in the subnet and check for open ports
with open(output_file, "a") as file:
    file.write(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Device Scan Report</title>
            <style>
                body {{
                    background-color: #222;
                    color: #fff;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}

                .container {{
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #333;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                }}

                h1 {{
                    text-align: center;
                }}

                a {{
                    color: #fff;
                }}

                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>"""
    )

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=255)

        def scan_ip(ip):
            # Use Nmap to find open ports
            nm.scan(ip, arguments="-F")

            if ip in nm.all_hosts():
                open_ports = nm[ip].all_tcp()

                for port in open_ports:
                    progress.update(task, description=f"Scanning Port: {port} on {ip}")

                    # Check if the port is hosting a web page
                    web_page_info = check_web_page(ip, port)
                    if web_page_info:
                        file.write(web_page_info)

        with ThreadPoolExecutor() as executor:
            ip_range = [f"{subnet}.{i}" for i in range(1, 256)]
            executor.map(scan_ip, ip_range)

    file.write("</body></html>")

print("Scanning completed. The report has been exported to web_hosts.html.")
