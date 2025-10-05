from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from flask import Flask

app = Flask(__name__)

def bot_islemi_yap():
    print("🟡 Selenium başlıyor...")
    
    # Chrome ayarları
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        # Driver'ı başlat
        driver = webdriver.Chrome(options=chrome_options)
        print("🟢 Chrome başlatıldı!")
        
        # Örnek siteye git
        driver.get("https://httpbin.org/html")
        time.sleep(2)
        
        # Sayfa başlığını al
        baslik = driver.title
        print(f"📄 Sayfa başlığı: {baslik}")
        
        # Örnek element bulma
        body = driver.find_element(By.TAG_NAME, "body")
        print("🔍 Body elementi bulundu!")
        
        driver.quit()
        print("🔴 Driver kapatıldı")
        
        return f"✅ BAŞARILI! Sayfa: {baslik}"
        
    except Exception as e:
        return f"❌ HATA: {str(e)}"

@app.route('/')
def ana_sayfa():
    sonuc = bot_islemi_yap()
    return f"""
    <html>
        <body>
            <h1>Render'da Selenium Çalışıyor! 🎉</h1>
            <p><strong>Sonuç:</strong> {sonuc}</p>
            <p>Hocam başardık! 🤖</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
