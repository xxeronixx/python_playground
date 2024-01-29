import socket
import subprocess
import concurrent.futures

def check_port(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, 8006))
        if result == 0:
            print(f"IP {ip} is hosting a web page on port 8006")
        sock.close()
    except socket.error:
        pass

def get_local_ip():
    # Retrieve the local IP address on macOS
    try:
        output = subprocess.check_output(['ifconfig']).decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            if 'inet ' in line and '127.0.0.1' not in line:
                local_ip = line.strip().split(' ')[1]
                return local_ip
    except subprocess.CalledProcessError:
        return None


def main():
    local_ip = get_local_ip()
    if local_ip is None:
        print("Failed to retrieve local IP address.")
        return

    network_prefix = '.'.join(local_ip.split('.')[:-2]) + '.'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_port, f"192.168.100.{str(i)}")
                   for i in range(256)]

        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == '__main__':
    main()
