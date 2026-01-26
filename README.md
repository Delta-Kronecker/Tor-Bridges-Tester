# 🌐 Tor Bridges Tester

This project is an automated tool designed to test and publish working Tor Bridges. The script runs every day, identifying active bridges and publishing them here and to the Telegram channel.

---

## 📢 Telegram Channel

All final results are automatically compressed into a ZIP file and uploaded to our Telegram channel:

🔹 **Main Channel:** [DeltaKroneckerFreedom](https://t.me/GitKroneckerDelta)  

---



## 🚀 Direct Download Links

You can always find the latest tested and working bridges using the links below:

| Bridge Type | Status | Direct Download Link |
| :--- | :---: | :--- |
| **obfs4** | ✅ Active | [Download working_obfs4.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges/refs/heads/main/working_obfs4.txt) |
| **Vanilla** | ✅ Active | [Download working_vanilla.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges/refs/heads/main/working_vanilla.txt) |
| **WebTunnel** | ✅ Active | [Download working_webtunnel.txt](https://raw.githubusercontent.com/Delta-Kronecker/Tor-Bridges/refs/heads/main/working_webtunnel.txt) |



## 🛠 How It Works

1. **Fetch:** Retrieves the latest bridge lists from verified GitHub repositories.
2. **Socket Testing:** Performs a multi-threaded connection test (Socket Check) on every single bridge to verify port availability.
3. **Filtering:** Automatically removes dead, slow, or offline bridges.
4. **Deployment:** Updates the `.txt` files in this repository and pushes the consolidated ZIP file to Telegram.

## ⚙️ Technical Features

- **Multi-threading:** Tests up to 100 bridges simultaneously for maximum efficiency.
- **GitHub Actions:** Fully automated workflow—no personal server required.
- **Detailed Reporting:** Generates a real-time health rate report for each bridge type.
- **Vanilla Support:** Specifically optimized to handle raw IP:Port Vanilla bridges.

---

## ⚠️ Disclaimer
This project is for educational purposes and to facilitate free access to information. Users are responsible for their own actions and compliance with local regulations.

---
**Maintained by Delta Kronecker**
