// GAEKS DIGITAL ECOSYSTEM - AUTH & USER MANAGEMENT CONTROLLER
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
const USERS_DB_KEY = 'gaeks_users_db_v2';

const GaeksAuth = {
  getUsersDb() {
    const raw = localStorage.getItem(USERS_DB_KEY);
    if (!raw) {
      const initial = [
        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
      ];
      localStorage.setItem(USERS_DB_KEY, JSON.stringify(initial));
      return initial;
    }
    try { return JSON.parse(raw); } catch(e) { return []; }
  },

  saveUsersDb(db) {
    localStorage.setItem(USERS_DB_KEY, JSON.stringify(db));
  },

  recordUserRegistration(userObj) {
    const db = this.getUsersDb();
    const existingIndex = db.findIndex(u => u.email.toLowerCase() === userObj.email.toLowerCase());
    if (existingIndex >= 0) {
      db[existingIndex].lastLoginAt = Date.now();
      if (userObj.name) db[existingIndex].name = userObj.name;
    } else {
      db.unshift({
        id: userObj.id || 'usr_' + Date.now(),
        email: userObj.email,
        name: userObj.name || userObj.email.split('@')[0],
        provider: userObj.provider || 'email',
        plan: userObj.plan || 'FREE',
        registeredAt: Date.now(),
        lastLoginAt: Date.now()
      });
      this.sendWelcomeEmailNotice(userObj.email, userObj.name);
    }
    this.saveUsersDb(db);
  },

  sendWelcomeEmailNotice(email, name) {
    try {
      fetch('/api/send_welcome_email.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, name: name })
      }).catch(() => {});
    } catch(e) {}
  },

  getCurrentUser() {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    try {
      const user = JSON.parse(raw);
      if (user && user.email) {
        const clean = user.email.toLowerCase().trim();
        user.isAdmin = (clean === SUPER_ADMIN_EMAIL);
        if (VIP_WHITELIST.includes(clean)) {
          user.isPro = true;
          user.plan = 'PRO_VIP';
          user.planLabel = (clean === SUPER_ADMIN_EMAIL) ? 'SUPER ADMIN (Akses Penuh)' : 'GAEKS PRO VIP (Akses Penuh)';
        }
      }
      return user;
    } catch(e) {
      return null;
    }
  },

  isProUser() {
    const user = this.getCurrentUser();
    return user ? !!user.isPro : false;
  },

  isAdmin() {
    const user = this.getCurrentUser();
    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
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
      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.recordUserRegistration(user);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  loginWithGoogle(emailInput = '') {
    const cleanEmail = (emailInput || prompt("Masukkan Akun Google Anda (contoh: gaeks.group@gmail.com):") || "").toLowerCase().trim();
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
      isAdmin: (cleanEmail === SUPER_ADMIN_EMAIL),
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (cleanEmail === SUPER_ADMIN_EMAIL ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.recordUserRegistration(user);
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    window.location.reload();
  },

  logout() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    window.location.reload();
  },

  toggleUserPlan(email) {
    const db = this.getUsersDb();
    const target = db.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (target) {
      target.plan = (target.plan === 'PRO' || target.plan === 'PRO_VIP') ? 'FREE' : 'PRO';
      this.saveUsersDb(db);
      return target.plan;
    }
    return null;
  }
};
