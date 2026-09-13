// GAEKS DIGITAL ECOSYSTEM - AUTH & SESSION CONTROLLER
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];

const AUTH_STORAGE_KEY = 'gaeks_user_session_v1';

const GaeksAuth = {
  getCurrentUser() {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    try {
      const user = JSON.parse(raw);
      if (user && user.email && VIP_WHITELIST.includes(user.email.toLowerCase().trim())) {
        user.isPro = true;
        user.plan = 'PRO_VIP';
        user.planLabel = 'GAEKS PRO VIP (Akses Penuh)';
      }
      return user;
    } catch(e) {
      return null;
    }
  },

  isProUser() {
    const user = this.getCurrentUser();
    if (!user) return false;
    return !!user.isPro;
  },

  loginWithEmail(email, password, name = '') {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const displayName = name || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'email',
      isPro: isVip,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
      loginAt: Date.now()
    };

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  loginWithGoogle(emailInput = '') {
    const cleanEmail = (emailInput || prompt("Masukkan Akun Google Anda (contoh: triawan25@gmail.com):") || "").toLowerCase().trim();
    if (!cleanEmail) return;

    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const displayName = cleanEmail.split('@')[0].toUpperCase();

    const user = {
      id: 'usr_goog_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'google',
      isPro: isVip,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? 'GAEKS PRO VIP (Akses Penuh)' : 'Free Tier',
      loginAt: Date.now()
    };

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  logout() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    window.location.reload();
  }
};
