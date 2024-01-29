import paramiko
import concurrent.futures
import socket
import getpass

# Replace these values with your actual network details
base_ip = input('Partial IP (e.g. 192.168.0.)  :')
start_ip = 1
end_ip = 254

# Replace 'your_command' with the actual command you want to run (e.g., ping)
command_template = "ping -D -i 0.01 -c 100000 {}"  # Adjust the command as needed

# Replace 'your_username' and 'your_password' with your SSH credentials
username = "root"
password = getpass("password")

def execute_command(ip):
    output_file = f"~/Downloads/ping_gw_{ip}.txt"

    try:
        # Establish SSH connection with password authentication
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Run the command remotely and redirect output to the specified file
        command = command_template.format("1.1.1.1")  # Target IP to ping
        stdin, stdout, stderr = ssh.exec_command(command)
        with open(output_file, 'w') as file:
            file.write(stdout.read().decode())

            # Close the SSH connection
            ssh.close()

        print(f"Command executed for {ip}. Output saved to {output_file}")

    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
        print(f"Error connecting to {ip}: {str(e)}")

if __name__ == "__main__":
    # Use concurrent.futures to run commands concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ip_list = [base_ip + str(i) for i in range(start_ip, end_ip + 1)]
        executor.map(execute_command, ip_list)
