from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def basit_bot_test():
    print("🤖 Basit bot testi başlıyor...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--single-process')
    
    # Chrome binary path belirt
    options.binary_location = '/usr/bin/google-chrome'
    
    try:
        # Chrome driver'ı başlat
        driver = webdriver.Chrome(options=options)
        
        # Basit bir siteye git
        driver.get("https://httpbin.org/html")
        time.sleep(2)
        
        # Sayfa başlığını al
        baslik = driver.title
        icerik = driver.find_element(By.TAG_NAME, "h1").text
        
        driver.quit()
        
        return {
            "status": "success",
            "baslik": baslik,
            "icerik": icerik,
            "mesaj": "🎉 SELENIUM RENDER'DA ÇALIŞIYOR!"
        }
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return """
    <h1>🤖 Selenium Bot - CHROME KURULUMU</h1>
    <p><strong>Test Sayfaları:</strong></p>
    <ul>
        <li><a href="/test">Bot Testi</a></li>
        <li><a href="/status">Durum Kontrol</a></li>
    </ul>
    <p>Hocam Chrome kuruluyor, biraz bekleyeceğiz... ⏳</p>
    """

@app.route('/test')
def test():
    sonuc = basit_bot_test()
    return jsonify(sonuc)

@app.route('/status')
def status():
    return jsonify({"status": "active", "chrome": "installing"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
