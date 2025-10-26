#!/bin/bash
apt-get update
apt-get install -y wget gnupg

# Chrome'u kur
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Chrome driver'ı kur
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f3)
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f1)
wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
unzip -q chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "✅ Chrome ve Driver kuruldu: $CHROME_VERSION"
