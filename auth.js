// GLOBAL LANGUAGE FALLBACK GUARD
if (typeof window !== 'undefined') { window.currentLang = window.currentLang || 'id'; }

// GAEKS DIGITAL ECOSYSTEM - MULTI-KEY PERSISTENT AUTH ENGINE
const VIP_WHITELIST = [
  "gaeks.group@gmail.com",
  "triawan25@gmail.com",
  "ranesath@gmail.com"
];
const SUPER_ADMIN_EMAIL = "gaeks.group@gmail.com";
const GOOGLE_CLIENT_ID = "41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com";

const AUTH_STORAGE_KEY = 'gaeks_user_session_v3';
const USERS_DB_KEY = 'gaeks_users_db_v3';

const GaeksAuth = {
  getUsersDb() {
    let raw = null;
    try { raw = localStorage.getItem(USERS_DB_KEY); } catch(e) {}
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_users_db_v2'); } catch(e) {}
    }
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
    try { raw = localStorage.getItem('gaeks_user_session_v3'); } catch(e) {}
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_user_session_v2'); } catch(e) {}
    }
    if (!raw) {
      try { raw = localStorage.getItem('gaeks_user_session'); } catch(e) {}
    }
    if (!raw) {
      try {
        const m = document.cookie.match(/gaeks_session_v3=([^;]+)/);
        if (m) raw = decodeURIComponent(m[1]);
      } catch(e) {}
    }
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
        try {
          localStorage.setItem('gaeks_user_session_v3', JSON.stringify(user));
          document.cookie = "gaeks_session_v3=" + encodeURIComponent(JSON.stringify(user)) + "; path=/; max-age=2592000; SameSite=Lax";
        } catch(e) {}
        return user;
      }
    } catch(e) {
      return null;
    }
    return null;
  },

  isProUser() {
    const user = this.getCurrentUser();
    return user ? !!user.isPro : false;
  },

  isAdmin() {
    const user = this.getCurrentUser();
    return user ? (user.email.toLowerCase().trim() === SUPER_ADMIN_EMAIL) : false;
  },

    logout() {
    try {
      localStorage.removeItem('gaeks_user_session_v3');
      localStorage.removeItem('gaeks_user_session_v2');
      localStorage.removeItem('gaeks_user_session');
      sessionStorage.clear();
      document.cookie = "gaeks_session_v3=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      document.cookie = "gaeks_session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    } catch(e) {}
    window.location.replace(window.location.origin + '/login.html');
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
