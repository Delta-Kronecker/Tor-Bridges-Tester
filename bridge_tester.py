import socket
import re
import time
import concurrent.futures
from threading import Lock
import requests
import os
import random
import zipfile
from datetime import datetime

IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

BRIDGE_SOURCES = [
    {"type": "obfs4", "url": "https://raw.githubusercontent.com/scriptzteam/Tor-Bridges-Collector/main/bridges-obfs4", "output_file": "working_obfs4.txt"},
    {"type": "webtunnel", "url": "https://raw.githubusercontent.com/scriptzteam/Tor-Bridges-Collector/main/bridges-webtunnel", "output_file": "working_webtunnel.txt"},
    {"type": "vanilla", "url": "https://github.com/scriptzteam/Tor-Bridges-Collector/raw/refs/heads/main/bridges-vanilla", "output_file": "working_vanilla.txt"}
]

if not IS_GITHUB:
    for source in BRIDGE_SOURCES:
        source['output_file'] = os.path.join(r"C:\PyCharm\All\tor", source['output_file'])

MAX_WORKERS = 50
CONNECTION_TIMEOUT = 10
MAX_RETRIES = 3
file_lock = Lock()
final_stats = []

def test_bridge(bridge_line):
    try:
        if not bridge_line or len(bridge_line) < 8: return None
        
        if "obfs4" in bridge_line.lower():
            match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3}:\d+)', bridge_line)
            addr = match.group(1) if match else None
        elif "https" in bridge_line.lower():
            match = re.search(r'https://([^/:]+)(?::(\d+))?', bridge_line)
            addr = f"{match.group(1)}:{match.group(2) or 443}" if match else None
        else:
            first_part = bridge_line.split()[0]
            addr = first_part if ":" in first_part else None

        if addr:
            host, port = addr.split(':')
            sock = socket.create_connection((host, int(port)), timeout=CONNECTION_TIMEOUT)
            sock.close()
            return bridge_line
    except: pass
    return None

def send_to_telegram(file_path, caption):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, data={
                'chat_id': TELEGRAM_CHAT_ID, 
                'caption': caption,
                'parse_mode': 'Markdown'
            }, files={'document': f})
        print(f"Telegram Response: {response.status_code}")
    except Exception as e:
        print(f"Telegram Error: {e}")

def main():
    start_time = time.time()
    generated_files = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    summary_report = f"🔥 *Tor Bridges Teater Report*\n🔥 Date: `{now}`\n\n"
    summary_report += f"{'Type':<12} | {'Total':<6} | {'Work'}\n"
    summary_report += f"{'-'*30}\n"

    for source in BRIDGE_SOURCES:
        if not IS_GITHUB and source['type'] != 'vanilla': continue
        
        try:
            response = requests.get(source['url'], timeout=20)
            bridges = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        except: continue

        if not IS_GITHUB and source['type'] == 'vanilla' and len(bridges) > 1000:
            bridges = random.sample(bridges, 1000)

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(test_bridge, bridges))
            working_list = [r for r in results if r]

        with open(source['output_file'], 'w', encoding='utf-8') as f:
            for line in working_list: f.write(line + '\n')
        
        generated_files.append(source['output_file'])
        
        summary_report += f"{source['type'].upper():<12} | {len(bridges):<6} | {len(working_list)}\n"

    summary_report += f"{'-'*30}\n"
    summary_report += "*Note:* These bridges are tested from the scriptzteam/Tor-Bridges-Collector repository\n\n"
    summary_report += "The source updates slowly (may take months)\n\n"
    summary_report += "Use the tor-bridge-collector file for new bridges"

    zip_name = "Tor_Bridges_Configs.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in generated_files:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
    
    print(summary_report)

    if IS_GITHUB:
        send_to_telegram(zip_name, summary_report)

if __name__ == "__main__":
    main()
