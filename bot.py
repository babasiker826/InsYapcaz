from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import string
import json
import requests
from flask import Flask, request, jsonify
import os
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import base64

app = Flask(__name__)

class InstagramBot:
    def __init__(self):
        self.ua = UserAgent()
        self.accounts_file = "instagram_accounts.json"
        
    def setup_driver(self):
        """Render için optimize Chrome driver"""
        print("🚀 Chrome driver başlatılıyor...")
        
        options = Options()
        
        # Render optimizasyonları
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,720')
        options.add_argument('--single-process')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Gerçekçi user agent
        options.add_argument(f'--user-agent={self.ua.random}')
        
        try:
            # Chrome binary path
            options.binary_location = '/usr/bin/google-chrome'
            driver = webdriver.Chrome(options=options)
            
            # Anti-detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.ua.random
            })
            
            return driver
        except Exception as e:
            print(f"❌ Chrome hatası: {e}")
            return None

    def human_like_delay(self, min_sec=1, max_sec=3):
        """İnsan gibi rastgele bekleme"""
        time.sleep(random.uniform(min_sec, max_sec))

    def human_like_mouse_movement(self, driver, element):
        """İnsan gibi fare hareketi"""
        try:
            actions = ActionChains(driver)
            
            # Elemente doğru hareket et
            actions.move_to_element(element)
            actions.pause(random.uniform(0.5, 1.5))
            
            # Rastgele küçük hareketler
            for _ in range(random.randint(2, 4)):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                actions.move_by_offset(offset_x, offset_y)
                actions.pause(0.1)
            
            # Elemente geri dön ve tıkla
            actions.move_to_element(element)
            actions.click()
            actions.perform()
            
        except Exception as e:
            # Fallback: normal click
            element.click()

    def human_like_typing(self, element, text):
        """İnsan gibi yazma"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

    def get_temp_email(self):
        """Geçici email al"""
        try:
            # 1secmail API
            response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
            if response.status_code == 200:
                email = response.json()[0]
                return email
        except:
            pass
        
        # Fallback: rastgele email
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        name = ''.join(random.choices(string.ascii_lowercase, k=10))
        domain = random.choice(domains)
        return f"{name}@{domain}"

    def get_verification_code(self, email):
        """Doğrulama kodunu al"""
        try:
            # 1secmail'den kod al
            username, domain = email.split('@')
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
            
            for _ in range(30):  # 30 deneme
                response = requests.get(url)
                if response.status_code == 200:
                    messages = response.json()
                    if messages:
                        # Son mesajı al
                        message_id = messages[0]['id']
                        msg_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
                        msg_response = requests.get(msg_url)
                        
                        if msg_response.status_code == 200:
                            message_data = msg_response.json()
                            text = message_data.get('textBody', '')
                            
                            # Kodu bul (6 haneli)
                            import re
                            code_match = re.search(r'\b\d{6}\b', text)
                            if code_match:
                                return code_match.group()
                
                time.sleep(2)  # 2 saniye bekle
                
        except Exception as e:
            print(f"❌ Kod alma hatası: {e}")
        
        return None

    def generate_username(self):
        """Rastgele kullanıcı adı oluştur"""
        adjectives = ["cool", "happy", "smart", "fast", "clever", "brave", "calm", "proud", "wise", "bold"]
        nouns = ["wolf", "eagle", "tiger", "lion", "bear", "fox", "hawk", "shark", "dragon", "phoenix"]
        numbers = ''.join(random.choices(string.digits, k=4))
        
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        return f"{adjective}_{noun}_{numbers}"

    def generate_password(self):
        """Güçlü şifre oluştur"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(chars, k=12))

    def generate_name(self):
        """Rastgele isim oluştur"""
        first_names = ["Ali", "Mehmet", "Ahmet", "Mustafa", "Hasan", "Huseyin", "Ibrahim", "Yusuf", "Omer", "Muhammed"]
        last_names = ["Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Yildiz", "Arslan", "Dogan", "Kurt", "Koc"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def save_account(self, account_data):
        """Hesabı JSON'a kaydet"""
        try:
            accounts = []
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    accounts = json.load(f)
            
            accounts.append(account_data)
            
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(accounts, f, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"❌ Kayıt hatası: {e}")
            return False

    def create_instagram_account(self):
        """Instagram hesabı oluştur"""
        driver = self.setup_driver()
        if not driver:
            return {"status": "error", "message": "Chrome başlatılamadı"}
        
        try:
            print("📧 Geçici email alınıyor...")
            email = self.get_temp_email()
            print(f"✅ Email: {email}")
            
            # Instagram signup sayfası
            print("🌐 Instagram'a gidiliyor...")
            driver.get("https://www.instagram.com/accounts/emailsignup/")
            self.human_like_delay(3, 5)
            
            wait = WebDriverWait(driver, 15)
            
            # Email alanı
            print("📝 Form dolduruluyor...")
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))
            self.human_like_mouse_movement(driver, email_field)
            self.human_like_typing(email_field, email)
            self.human_like_delay()
            
            # Tam ad
            full_name = self.generate_name()
            fullname_field = driver.find_element(By.NAME, "fullName")
            self.human_like_mouse_movement(driver, fullname_field)
            self.human_like_typing(fullname_field, full_name)
            self.human_like_delay()
            
            # Kullanıcı adı
            username = self.generate_username()
            username_field = driver.find_element(By.NAME, "username")
            self.human_like_mouse_movement(driver, username_field)
            self.human_like_typing(username_field, username)
            self.human_like_delay()
            
            # Şifre
            password = self.generate_password()
            password_field = driver.find_element(By.NAME, "password")
            self.human_like_mouse_movement(driver, password_field)
            self.human_like_typing(password_field, password)
            self.human_like_delay()
            
            # Kayıt butonu
            print("🔄 Kayıt yapılıyor...")
            signup_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]")
            self.human_like_mouse_movement(driver, signup_button)
            self.human_like_delay(5, 8)
            
            # Yaş doğrulama
            try:
                year_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//select[@title='Year:']"))
                )
                year_select.click()
                self.human_like_delay()
                
                year_2000 = driver.find_element(By.XPATH, "//option[@value='2000']")
                year_2000.click()
                self.human_like_delay()
                
                next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                self.human_like_delay(3, 5)
                
            except TimeoutException:
                print("ℹ️ Yaş doğrulama gerekmedi")
            
            # Doğrulama kodu
            print("📨 Doğrulama kodu bekleniyor...")
            verification_code = self.get_verification_code(email)
            
            if verification_code:
                print(f"✅ Kod alındı: {verification_code}")
                
                # Kod alanını bul
                code_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "email_confirmation_code"))
                )
                self.human_like_mouse_movement(driver, code_field)
                self.human_like_typing(code_field, verification_code)
                self.human_like_delay()
                
                # Onayla butonu
                confirm_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
                confirm_button.click()
                self.human_like_delay(5, 8)
                
            else:
                print("❌ Kod alınamadı, manuel giriş gerekli")
            
            # Session'ı al
            print("🔐 Session alınıyor...")
            session_cookies = driver.get_cookies()
            session_id = None
            
            for cookie in session_cookies:
                if cookie['name'] == 'sessionid':
                    session_id = cookie['value']
                    break
            
            # Hesap bilgilerini hazırla
            account_data = {
                "email": email,
                "username": username,
                "password": password,
                "full_name": full_name,
                "session_id": session_id,
                "cookies": session_cookies,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "active"
            }
            
            # Hesabı kaydet
            if self.save_account(account_data):
                print("💾 Hesap kaydedildi!")
            
            driver.quit()
            
            return {
                "status": "success",
                "account": account_data,
                "message": "🎉 Instagram hesabı başarıyla oluşturuldu!"
            }
            
        except Exception as e:
            print(f"❌ Hesap oluşturma hatası: {e}")
            if driver:
                driver.quit()
            return {"status": "error", "message": str(e)}

# Flask Routes
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Instagram Bot - RENDER</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { background: #1877f2; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px; }
            .btn:hover { background: #166fe5; }
            .result { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Instagram Bot - RENDER</h1>
            <p><strong>Özellikler:</strong></p>
            <ul>
                <li>✅ Gerçek insan gibi davranış</li>
                <li>✅ Fare hareketleri simulasyonu</li>
                <li>✅ Geçici email ile doğrulama</li>
                <li>✅ Session ve cookie kaydetme</li>
                <li>✅ Render uyumlu</li>
            </ul>
            
            <button class="btn" onclick="createAccount()">🎯 Hesap Oluştur</button>
            <button class="btn" onclick="getAccounts()">📋 Hesapları Listele</button>
            
            <div id="result"></div>
        </div>
        
        <script>
            async function createAccount() {
                const result = document.getElementById('result');
                result.innerHTML = '🔄 Hesap oluşturuluyor... (2-3 dakika sürebilir)';
                
                const response = await fetch('/create-account');
                const data = await response.json();
                
                if (data.status === 'success') {
                    result.innerHTML = `
                        <div style="color: green;">
                            <h3>✅ BAŞARILI!</h3>
                            <p><strong>Email:</strong> ${data.account.email}</p>
                            <p><strong>Kullanıcı Adı:</strong> ${data.account.username}</p>
                            <p><strong>Şifre:</strong> ${data.account.password}</p>
                            <p><strong>Session ID:</strong> ${data.account.session_id || 'Alınamadı'}</p>
                        </div>
                    `;
                } else {
                    result.innerHTML = `<div style="color: red;">❌ HATA: ${data.message}</div>`;
                }
            }
            
            async function getAccounts() {
                const response = await fetch('/accounts');
                const data = await response.json();
                
                const result = document.getElementById('result');
                if (data.accounts && data.accounts.length > 0) {
                    let html = '<h3>📋 Oluşturulan Hesaplar:</h3>';
                    data.accounts.forEach(acc => {
                        html += `
                            <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px;">
                                <p><strong>Kullanıcı:</strong> ${acc.username}</p>
                                <p><strong>Email:</strong> ${acc.email}</p>
                                <p><strong>Oluşturulma:</strong> ${acc.created_at}</p>
                            </div>
                        `;
                    });
                    result.innerHTML = html;
                } else {
                    result.innerHTML = '<p>Henüz hesap oluşturulmadı.</p>';
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/create-account', methods=['POST', 'GET'])
def create_account():
    bot = InstagramBot()
    result = bot.create_instagram_account()
    return jsonify(result)

@app.route('/accounts')
def get_accounts():
    try:
        if os.path.exists("instagram_accounts.json"):
            with open("instagram_accounts.json", 'r', encoding='utf-8') as f:
                accounts = json.load(f)
            return jsonify({"accounts": accounts})
        return jsonify({"accounts": []})
    except:
        return jsonify({"accounts": []})

@app.route('/status')
def status():
    return jsonify({
        "status": "active", 
        "chrome": "ready",
        "message": "🤖 Bot hazır!",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    print("🚀 Instagram Bot RENDER'da başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, debug=False)
