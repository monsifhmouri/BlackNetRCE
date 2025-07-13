BlackNetRCE
BlackNetRCE is a Python-based Remote Code Execution (RCE) tool that lets you create a secure communication channel between a server and a client using SSL certificates.

Features
Encrypted communication using SSL certificates (cert.pem and key.pem).

Simple server script to accept incoming client connections.

Client script that connects automatically and waits for commands.

Ability to convert the client script into a standalone executable (EXE) for easy deployment.

Requirements
Python 3.7 or higher

PyInstaller library (optional, for building EXE files)

OpenSSL (for generating SSL certificates)

Setup and Usage
Generate SSL Certificates (one-time):
Open the C2_Server directory, then open a terminal and run the following command:
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
Fill in the requested info or press Enter to skip.

Run the Server:
Make sure server.py, cert.pem, and key.pem are in the same folder, then run:
python server.py

Configure the Client:
Open RCE.py and find the line:
C2_SERVER = "your-c2-domain.com"
Change "your-c2-domain.com" to your local IP address.
To find your IP address, run ipconfig in a terminal and copy your IPv4 address (e.g., 192.168.1.5).

Run the Client (for testing):
Run the client with:
python RCE.py
If successful, the server terminal will show an active shell ready to receive commands.

Building the Client Executable (EXE)
Install PyInstaller if not installed:
pip install pyinstaller

Convert the client script to an EXE file with:
pyinstaller --noconsole --onefile RCE.py

The executable will be available inside the dist folder as RCE.exe.

Notes
Make sure your firewall allows connections on the server port (default is 443).

If you use a public domain or tunneling service like ngrok, ensure SSL is properly configured.

Always start the server before running the client.

Disclaimer
This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use is illegal and unethical.
