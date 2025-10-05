from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from flask import Flask

app = Flask(__name__)

def bot_islemi_yap():
    print("🟡 Selenium başlıyor...")
    
    chrome_options = Options()
    
    # MEMORY TASARRUF AYARLARI
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")  # ✅ Resimleri kapat
    chrome_options.add_argument("--disable-javascript")  # ✅ JS kapat (test için)
    chrome_options.add_argument("--single-process")  # ✅ Memory için
    chrome_options.add_argument("--window-size=640,480")  # ✅ Küçük pencere
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("🟢 Chrome başlatıldı!")
        
        # Daha basit bir siteye git
        driver.get("https://httpbin.org/ip")
        time.sleep(1)
        
        baslik = driver.title
        print(f"📄 Sayfa başlığı: {baslik}")
        
        # Hızlıca kapat
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
        <body style="font-family: Arial; padding: 20px;">
            <h1>🎉 Render'da Selenium ÇALIŞTI!</h1>
            <p><strong>Sonuç:</strong> {sonuc}</p>
            <p>Hocam memory hatasını yendik! 💪</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False
