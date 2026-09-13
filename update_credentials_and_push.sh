#!/bin/bash
set -e

echo "=== 1. Menyiapkan skrip pembaruan kredensial ==="
cat << 'PY_SCRIPT' > apply_credentials.py
import os, re

# 1. Update api/config.php
config_content = '''<?php
// GAEKS DIGITAL SMTP CONFIGURATION (HOSTINGER)
define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 465); // SSL
define('SMTP_USER', 'no-reply@gaeks.com');
define('SMTP_PASS', 'Adagagap499!');
define('SMTP_FROM_NAME', 'GAEKS Digital Products');
define('REPLY_TO_EMAIL', 'gaeks.group@gmail.com');
define('ADMIN_NOTIFICATION_EMAIL', 'gaeks.group@gmail.com');
'''

os.makedirs("api", exist_ok=True)
with open("api/config.php", "w") as f:
    f.write(config_content)
print("✓ api/config.php berhasil diperbarui dengan kata sandi Hostinger.")

# 2. Update auth.js
with open("auth.js", "r") as f:
    auth_text = f.read()

client_id = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com"
auth_text = re.sub(r'const GOOGLE_CLIENT_ID = .*?;', f'const GOOGLE_CLIENT_ID = "{client_id}";', auth_text)

gis_js = '''
  initGoogleAuth() {
    if (window.google && window.google.accounts && window.google.accounts.id) {
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: (response) => this.handleGoogleCredential(response),
        auto_select: false
      });

      const btnIndex = document.getElementById("google-btn-container-index");
      if (btnIndex) {
        window.google.accounts.id.renderButton(btnIndex, {
          theme: "outline",
          size: "large",
          width: "100%",
          text: "continue_with",
          shape: "pill"
        });
      }

      const btnCv = document.getElementById("google-btn-container-cv");
      if (btnCv) {
        window.google.accounts.id.renderButton(btnCv, {
          theme: "outline",
          size: "large",
          width: "100%",
          text: "continue_with",
          shape: "pill"
        });
      }
    }
  },

  handleGoogleCredential(response) {
    try {
      const base64Url = response.credential.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      const payload = JSON.parse(jsonPayload);
      const email = payload.email.toLowerCase().trim();
      const name = payload.name || payload.given_name || email.split('@')[0];
      const avatar = payload.picture || ('https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(name));

      const isVip = VIP_WHITELIST.includes(email);
      const isSuperAdmin = (email === SUPER_ADMIN_EMAIL);

      const user = {
        id: 'usr_goog_' + Math.random().toString(36).substr(2, 9),
        email: email,
        name: name,
        avatar: avatar,
        provider: 'google',
        isPro: isVip,
        isAdmin: isSuperAdmin,
        plan: isVip ? 'PRO_VIP' : 'FREE',
        planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
        loginAt: Date.now()
      };

      this.recordUserRegistration(user);
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
      window.location.reload();
    } catch (e) {
      console.error("Gagal memproses token Google:", e);
      alert("Terjadi kendala saat memproses akun Google Anda. Silakan coba lagi.");
    }
  },
'''

if "handleGoogleCredential" not in auth_text:
    auth_text = auth_text.replace("getCurrentUser() {", gis_js + "\n  getCurrentUser() {")

with open("auth.js", "w") as f:
    f.write(auth_text)
print("✓ auth.js berhasil diperbarui dengan Google Client ID resmi.")

# 3. Patch index.html & cv.html
def patch_file(fname, container_id, target_tag):
    if not os.path.exists(fname): return
    with open(fname, "r") as f: content = f.read()
    if "https://accounts.google.com/gsi/client" not in content:
        content = content.replace("</head>", "  <script src=\"https://accounts.google.com/gsi/client\" async defer></script>\n</head>")
    if container_id not in content and target_tag in content:
        content = content.replace(target_tag, target_tag + f"\n        <div id=\"{container_id}\" class=\"w-full flex justify-center min-h-[40px]\"></div>")
    if "GaeksAuth.initGoogleAuth()" not in content:
        content = content.replace("window.onload = function() {", "window.onload = function() {\n      setTimeout(() => { if (GaeksAuth.initGoogleAuth) GaeksAuth.initGoogleAuth(); }, 500);")
        content = content.replace("function openAuthModal() {", "function openAuthModal() {\n      setTimeout(() => { if (GaeksAuth.initGoogleAuth) GaeksAuth.initGoogleAuth(); }, 100);")
    with open(fname, "w") as f: f.write(content)
    print(f"✓ {fname} berhasil diintegrasikan dengan Google Sign-In.")

patch_file("index.html", "google-btn-container-index", "<!-- GOOGLE 1-CLICK SIGN IN -->\n      <div>")
patch_file("cv.html", "google-btn-container-cv", "<!-- GOOGLE SIGN IN BUTTON -->\n      <div>")
PY_SCRIPT

python3 apply_credentials.py
rm apply_credentials.py

echo "=== 2. Mem-push perubahan ke GitHub ==="
git add api/config.php auth.js index.html cv.html
git commit -m "chore: configure Google Client ID and Hostinger SMTP credentials for no-reply@gaeks.com" || true
git push origin main

echo "=== SELESAI! Seluruh kredensial telah aktif di https://gdp.gaeks.com ==="
