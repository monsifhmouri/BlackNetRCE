# BlackNetRCE

BlackNetRCE is a Python-based Remote Code Execution (RCE) tool that allows you to create a secure server and client communication channel using SSL certificates.

---

## Features
- Encrypted communication with SSL certificates (`cert.pem` and `key.pem`).
- Simple server script to accept incoming client connections.
- Client script that connects automatically and waits for commands.
- Ability to convert the client script into a standalone executable (EXE) for easy deployment.

---

## Requirements
- Python 3.7 or higher
- `pyinstaller` library (optional, for building EXE files)
- OpenSSL (for generating SSL certificates)

---

## Setup and Usage

### 1. Generate SSL Certificates (one-time)
In the `C2_Server` directory, open a terminal and run:

```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
Fill in the required info or press Enter to skip.

2. Run the Server
Make sure server.py, cert.pem, and key.pem are in the same folder, then run:

bash
Copy
Edit
python server.py
3. Configure the Client
Open RCE.py and modify the line:

python
Copy
Edit
C2_SERVER = "your-c2-domain.com"
Change "your-c2-domain.com" to your local IP address.

To find your IP, run in terminal:

bash
Copy
Edit
ipconfig
Copy your IPv4 address (e.g., 192.168.1.5).

4. Run the Client (for testing)
Simply run:

bash
Copy
Edit
python RCE.py
If successful, the server terminal will show an active shell ready for commands.

Building the Client Executable (EXE)
Install PyInstaller if needed
bash
Copy
Edit
pip install pyinstaller
Convert client script to EXE
bash
Copy
Edit
pyinstaller --noconsole --onefile RCE.py
The executable will be located in the dist folder as RCE.exe.

Notes
Ensure your firewall allows connections on the server port (default is 443).

If using a public domain or tunneling service like ngrok, verify SSL is properly configured.

Always start the server before running the client.

Disclaimer
This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use is illegal and unethical.

Feel free to contribute or report issues!

csharp
Copy
Edit

If you want, I can help you add this directly to your GitHub repo.
