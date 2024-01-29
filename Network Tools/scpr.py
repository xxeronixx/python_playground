#!/usr/bin/python3
import nmap
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import urllib3
import os
import csv
import socket
from pythonping import ping


# Specify your subnet here (e.g., "10.0.0.0/24" for a /24 subnet)
try:
    # Options to Initialize: IP scan, Open SSH/SFTP/FTP
    os.system('clear')

    # Disable InsecureRequestWarning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # noqa
    console = Console()
    subnet = console.input("[blue]Enter CIDR IP/subnet (ex: [cyan]192.168.0.0/24[blue])[/]\n[green]IP:")
    option = console.input("[blue]Scan Options:\n"
                           "1:Active IP Scan\n"
                           "2:Web Host Scan\n"
                           "3:Open SSH Scan\n"
                           "4:Open FTP Scan\n"
                           "0:Scan All\n"
                           "[green]Option:")
    subnet_object = ipaddress.IPv4Network(subnet)
    num_ips = subnet_object.num_addresses
    output_file = f"{subnet_object.network_address}_{subnet_object.prefixlen}"

    # Initialize Nmap PortScanner
    nm = nmap.PortScanner()
except KeyboardInterrupt:
    os.system('clear')
    exit()


# Function to check if a web page is hosted on a specific port of an IP
def check_web_page(ip, port):
    http_url = f"http://{ip}:{port}"
    https_url = f"https://{ip}:{port}"
    try:
        # Check if the IP is hosting a web page on the current port using HTTP
        http_response = requests.get(http_url, timeout=1)
        if http_response.status_code == 200:
            return f"""
            <h3><a href='{http_url}' target='_blank'>http://{ip}:{port}</a></h3>
            <iframe src='{http_url}' frameborder='0' style='width:100%; height:800px;'></iframe>
            """
    except requests.exceptions.RequestException:
        pass
    try:
        # Check if the IP is hosting a web page on the current port using HTTPS
        https_response = requests.get(https_url, timeout=5, verify=False)
        if https_response.status_code == 200:
            return f"""
            <h3><a href='{https_url}' target='_blank'>https://{ip}:{port}</a></h3>
            <iframe src='{https_url}' frameborder='0' style='width:100%; height:800px;'></iframe>
            """
    except requests.exceptions.RequestException:
        pass
    return ""


# Function to scan a subnet for open ports and web pages
def scan_subnet(subnet):
    # Start blank html file
    with open(f"{output_file}_scan.html", "w") as file:
        file.write("")
    # Perform port scanning on each IP in the subnet and check for open ports
    with open(f"{output_file}_scan.html", "a") as file:
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
                        font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", "Helvetica", "Lucida Grande", sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 50px auto;
                        padding: 20px;
                        background-color: #333;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{
                        text-align: center;
                    }}
                    .animation {{
                        animation: fadeIn 1s ease-in-out;
                    }}
                    @keyframes fadeIn {{
                        0% {{
                            opacity: 0;
                        }}
                        100% {{
                            opacity: 1;
                        }}
                    }}
                    a {{
                        color: #fff;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
            <div class="container">
                <h1>Device Scan Report</h1>
                <div class="animation">
                """
        )
        with Progress(TextColumn("{task.description}"), SpinnerColumn(), BarColumn(), TimeElapsedColumn(),TaskProgressColumn()) as progress:
            task1 = progress.add_task(f"[cyan]Scanning subnet...", total=None)

            def scan_ip(ip):
                # Use Nmap to find open ports
                nm.scan(ip, arguments="--top-ports 1000 -T4")

                if ip in nm.all_hosts():
                    open_ports = nm[ip].all_tcp()
                    task = progress.add_task(f"[cyan]Scanning [/cyan][red]{ip}...", total=len(open_ports))

                    for port in open_ports:
                        # Check if the port is hosting a web page
                        web_page_info = check_web_page(ip, port)
                        progress.update(task, description=f"[cyan]Scanning[/cyan] [green]{ip}:{port}", advance=1)
                        progress.update(task1, advance=1)
                        if web_page_info:
                            file.write(web_page_info)

            with ThreadPoolExecutor() as executor:
                network = ipaddress.ip_network(subnet)
                ip_range = [str(ip) for ip in network.hosts()]
                executor.map(scan_ip, ip_range)
            progress.update(task1, description=f"[cyan]Scanning", completed=1)
        file.write(
            """
                </div>
            </div>
            </body>
            </html>
            """
        )
    console.print(f"[blue]Scanning completed. The report has been exported to [green]{output_file}.html")


def perform_active_ip_scan(subnet):
    with Progress(TextColumn("{task.description}"), SpinnerColumn(), BarColumn(), TimeElapsedColumn()) as progress:
        task = progress.add_task("[blue]Scanning Active IPs...", total=None)
    # Initialize Nmap PortScanner with the desired number of threads
        try:
            nm.scan(hosts=subnet, arguments="-sn -T4")
        except Exception as err:
            console.print(f"[red]{err}")
        progress.update(task)
        active_ips = []
        for host in nm.all_hosts():
            if nm[host].state() == "up":
                active_ips.append([host])

    # Save active IP addresses, device names, and MAC addresses to CSV file
    with open(f"{output_file}_active.csv", "w") as file:
        write = csv.writer(file)
        write.writerow(["IP Address"])
        write.writerows(active_ips)

    console.print(f"\n[green]Active IP scan completed. Active IPs found: {len(active_ips)}")


# Option handler
def handle_option(option, subnet):
    if option == "1":
        perform_active_ip_scan(subnet)
    elif option == "2":
        scan_subnet(subnet)
    elif option is None:
        perform_active_ip_scan(subnet)
    else:
        console.print("[red]Invalid option. Please try again.")


if __name__ == '__main__':
    handle_option(option, subnet)
    exit(0)

