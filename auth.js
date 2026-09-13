// GAEKS DIGITAL ECOSYSTEM - AUTH, DUAL PERSISTENCE & HARD REDIRECT
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v2';
const USERS_DB_KEY = 'gaeks_users_db_v2';

const GaeksAuth = {
  getUsersDb() {
    let raw = null;
    try { raw = localStorage.getItem(USERS_DB_KEY); } catch(e) {}
    if (!raw) {
      const initial = [
        { id: 'usr_adm_1', email: 'gaeks.group@gmail.com', name: 'GAEKS Group (Admin)', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 5, lastLoginAt: Date.now() },
        { id: 'usr_vip_2', email: 'triawan25@gmail.com', name: 'Deny Triawan', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 4, lastLoginAt: Date.now() },
        { id: 'usr_vip_3', email: 'ranesath@gmail.com', name: 'Ranesath', provider: 'google', plan: 'PRO_VIP', registeredAt: Date.now() - 86400000 * 3, lastLoginAt: Date.now() }
      ];
      try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(initial)); } catch(e) {}
      return initial;
    }
    try { return JSON.parse(raw); } catch(e) { return []; }
  },

  saveUsersDb(db) {
    try { localStorage.setItem(USERS_DB_KEY, JSON.stringify(db)); } catch(e) {}
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
      this.sendEmailNotification('welcome', userObj.email, userObj.name);
    }
    this.saveUsersDb(db);
  },

  sendEmailNotification(actionType, email, name, extraData = {}) {
    try {
      fetch('/api/mailer.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: actionType,
          email: email,
          name: name,
          ...extraData
        })
      }).catch(() => {});
    } catch(e) {}
  },

  getCurrentUser() {
    let raw = null;
    try { raw = localStorage.getItem(AUTH_STORAGE_KEY); } catch(e) {}
    if (!raw) {
      try {
        const m = document.cookie.match(/gaeks_session=([^;]+)/);
        if (m) raw = decodeURIComponent(m[1]);
      } catch(e) {}
    }
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

  saveSessionDual(user) {
    try {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
    } catch(e) {}
    try {
      document.cookie = "gaeks_session=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
    } catch(e) {}
  },

  processVerifiedGoogleUser(email, name, avatar, targetUrl = '') {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
    const displayName = name || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_goog_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: avatar || ('https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName)),
      provider: 'google',
      isPro: isVip,
      isAdmin: isSuperAdmin,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.saveSessionDual(user);
    this.recordUserRegistration(user);

    let dest = targetUrl;
    if (!dest) {
      const p = new URLSearchParams(window.location.search);
      dest = p.get('redirect') || 'index.html';
    }
    dest = decodeURIComponent(dest).replace(/^\//, '');
    const finalUrl = window.location.origin + '/' + dest;
    window.location.replace(finalUrl);
  },

  loginWithEmail(email, password, customName = '', targetUrl = '') {
    const cleanEmail = email.toLowerCase().trim();
    const isVip = VIP_WHITELIST.includes(cleanEmail);
    const isSuperAdmin = (cleanEmail === SUPER_ADMIN_EMAIL);
    const displayName = customName || cleanEmail.split('@')[0];

    const user = {
      id: 'usr_' + Math.random().toString(36).substr(2, 9),
      email: cleanEmail,
      name: displayName,
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=' + encodeURIComponent(displayName),
      provider: 'email',
      isPro: isVip,
      isAdmin: isSuperAdmin,
      plan: isVip ? 'PRO_VIP' : 'FREE',
      planLabel: isVip ? (isSuperAdmin ? 'SUPER ADMIN' : 'GAEKS PRO VIP') : 'Free Tier',
      loginAt: Date.now()
    };

    this.saveSessionDual(user);
    this.recordUserRegistration(user);

    let dest = targetUrl;
    if (!dest) {
      const p = new URLSearchParams(window.location.search);
      dest = p.get('redirect') || 'index.html';
    }
    dest = decodeURIComponent(dest).replace(/^\//, '');
    const finalUrl = window.location.origin + '/' + dest;
    window.location.replace(finalUrl);
  },

  logout() {
    try { localStorage.removeItem(AUTH_STORAGE_KEY); } catch(e) {}
    try { document.cookie = "gaeks_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"; } catch(e) {}
    window.location.replace(window.location.origin + '/index.html');
  },

  toggleUserPlan(email) {
    const db = this.getUsersDb();
    const target = db.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (target) {
      const willBePro = (target.plan !== 'PRO' && target.plan !== 'PRO_VIP');
      target.plan = willBePro ? 'PRO' : 'FREE';
      this.saveUsersDb(db);
      if (willBePro) {
        this.sendEmailNotification('purchase', target.email, target.name, { plan_name: 'GAEKS PRO Member' });
      }
      return target.plan;
    }
    return null;
  }
};
