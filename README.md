DoS-Suic Attack Tool
Overview DoS-Suic is a powerful tool designed to simulate Denial of Service (DoS) attacks for educational and testing purposes. It provides a user-friendly graphical user interface (GUI) for launching various types of network attacks, including HTTP, UDP, TCP, and SYN flood attacks. The tool is implemented using Python and Tkinter.

Features
HTTP Attack: Floods a target URL with HTTP GET requests.
UDP Attack: Sends UDP packets to a specified IP address and port.
TCP Attack: Establishes TCP connections to a target IP address and port.
SYN Flood Attack: Sends SYN packets to a target IP address and port.
How it Works DoS-Suic utilizes the following Python libraries:

requests: For sending HTTP GET requests.
socket: For sending UDP packets, establishing TCP connections, and creating raw sockets for SYN flood attacks.
threading: Manages concurrent execution of multiple attack threads.
tkinter: Provides the GUI for configuring and controlling attacks.

Installation
Clone the repository:
```
git clone https://github.com/Shikan-c/DoS-Suic.git
```
```
cd DoS-Suic
```

Install dependencies:
```
pip install requests
```

Run the tool:
```
python dos_suic.py
```

Usage
Open the GUI
Run the script to open the GUI window.

Configure Attack
Target Domain (optional): For HTTP attacks, enter the target domain.
Target IP Address (optional): For UDP, TCP, and SYN attacks, enter the target IP address.
Number of Threads: Specify the number of threads to be used. Enter "unlimited" for unlimited threads.
Packet Limit: Enter the number of packets to send.
Attack Type: Choose from HTTP, UDP, TCP, or SYN.
Start Attack
Click the "Start Attack" button to initiate the attack with the specified parameters.

Run Unlimited Threads
Click "Run Unlimited Threads" to start the attack with unlimited threads.

Stop Attack
Click "Stop Attack" to halt the ongoing attack.

Disclaimer
DoS-Suic is intended solely for educational purposes. It is designed to be used in controlled environments, such as test networks or with explicit permission from network administrators. Using this tool for any form of unauthorized access, malicious activity, or unethical hacking is strictly prohibited.

The author, Shikan-c, and any associated parties are not liable for any damages, legal consequences, or claims arising from the misuse of this tool. You are solely responsible for complying with all applicable laws and regulations.

License
DoS-Suic is licensed under the MIT License. See LICENSE for details.

Author
Shikan-c

Version
1.0

