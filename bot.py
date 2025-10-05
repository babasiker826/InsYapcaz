from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

def google_arama_bot(aranacak_kelime):
    print(f"🔍 Google'da aranıyor: {aranacak_kelime}")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--single-process')
    
    try:
        # ChromeDriver Manager ile otomatik driver kurulumu
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Google'a git
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Cookie uyarısını kabul et (varsa)
        try:
            cookie_button = driver.find_element(By.XPATH, "//button[contains(., 'Kabul')]")
            cookie_button.click()
            time.sleep(1)
        except:
            pass
        
        # Arama kutusunu bul
        arama_kutusu = driver.find_element(By.NAME, "q")
        arama_kutusu.send_keys(aranacak_kelime)
        arama_kutusu.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Sonuçları al
        sonuclar = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
        sonuc_listesi = [sonuc.text for sonuc in sonuclar if sonuc.text]
        
        driver.quit()
        
        return {
            "status": "success",
            "aranan": aranacak_kelime,
            "sonuc_sayisi": len(sonuc_listesi),
            "sonuclar": sonuc_listesi
        }
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return """
    <h1>🤖 Selenium Bot AKTİF!</h1>
    <p><strong>Hocam site canlı! Test edelim:</strong></p>
    <ul>
        <li><a href="/google?q=python">Google'da Python Ara</a></li>
        <li><a href="/google?q=render selenium">Render Selenium Ara</a></li>
        <li><a href="/test">Basit Test</a></li>
    </ul>
    <p>🎉 Bot çalışıyor!</p>
    """

@app.route('/google')
def google_arama():
    kelime = request.args.get('q', 'Selenium Render')
    sonuc = google_arama_bot(kelime)
    return jsonify(sonuc)

@app.route('/test')
def test():
    return jsonify({"status": "active", "message": "Bot hazır!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
