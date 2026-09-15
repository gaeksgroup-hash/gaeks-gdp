(function () {
  'use strict';
  window.currentLang = window.currentLang || 'id';

  const SNAPSHOT_KEY = 'gaeks_authenticated_user';
  const GOOGLE_CLIENT_ID = '41832472270-6r8iudma1eho6kn3q6rs4rl7b9ank7n4.apps.googleusercontent.com';
  let currentUser = null;

  try {
    const cached = sessionStorage.getItem(SNAPSHOT_KEY);
    currentUser = cached ? JSON.parse(cached) : null;
  } catch (_) {}

  function cookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/[.$?*|{}()[\]\\/+^]/g, '\\$&') + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : '';
  }

  function saveSnapshot(user) {
    currentUser = user || null;
    try {
      if (currentUser) sessionStorage.setItem(SNAPSHOT_KEY, JSON.stringify(currentUser));
      else sessionStorage.removeItem(SNAPSHOT_KEY);
      ['gaeks_user_session_v3', 'gaeks_user_session_v2', 'gaeks_user_session'].forEach(k => localStorage.removeItem(k));
    } catch (_) {}
    window.dispatchEvent(new CustomEvent('gaeks-auth-change', { detail: currentUser }));
    return currentUser;
  }

  async function api(path, options) {
    const opts = Object.assign({ credentials: 'same-origin', headers: {} }, options || {});
    opts.headers = Object.assign({ Accept: 'application/json' }, opts.headers || {});
    if (opts.body && typeof opts.body !== 'string') {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(opts.body);
    }
    const csrf = cookie('gaeks_csrf');
    if (csrf && opts.method && opts.method.toUpperCase() !== 'GET') opts.headers['X-CSRF-Token'] = csrf;
    const response = await fetch(path, opts);
    let payload;
    try { payload = await response.json(); } catch (_) { payload = { ok: false, message: 'Respons server tidak valid.' }; }
    if (response.status === 401) saveSnapshot(null);
    if (!response.ok || payload.ok === false || payload.status === 'error') {
      const error = new Error(payload.error?.message || payload.message || 'Permintaan gagal.');
      error.code = payload.error?.code || 'request_failed';
      error.status = response.status;
      error.fields = payload.error?.fields || {};
      throw error;
    }
    return payload.data;
  }

  const GaeksAuth = {
    GOOGLE_CLIENT_ID,
    api,
    getCurrentUser() { return currentUser; },
    isProUser() { return !!currentUser?.isPro; },
    isAdmin() { return !!currentUser?.isAdmin; },
    getUsersDb() { return []; },
    saveUsersDb() {},
    recordUserRegistration() {},
    toggleUserPlan() { return null; },
    getDeterministicUserId(email) { return 'server_' + String(email || '').toLowerCase().replace(/[^a-z0-9]/g, '_'); },
    async refreshSession() {
      try {
        const data = await api('/api/auth.php?action=me', { method: 'GET' });
        return saveSnapshot(data.user);
      } catch (error) {
        if (error.status !== 401) console.error('Session check failed:', error);
        return saveSnapshot(null);
      }
    },
    async requireAuth(redirect) {
      const user = await this.ready;
      if (!user) {
        const target = redirect || (location.pathname.split('/').pop() + location.search);
        location.replace('/login.html?redirect=' + encodeURIComponent(target));
        return null;
      }
      return user;
    },
    async login(email, password, captchaToken) {
      const data = await api('/api/auth.php', { method: 'POST', body: { action: 'login', email, password, captchaToken } });
      saveSnapshot(data.user);
      return data.user;
    },
    async requestRegistrationOtp(name, email, captchaToken) {
      return api('/api/auth.php', { method: 'POST', body: { action: 'register_request', name, email, captchaToken } });
    },
    async verifyRegistration(name, email, code, password) {
      const data = await api('/api/auth.php', { method: 'POST', body: { action: 'register_verify', name, email, code, password } });
      saveSnapshot(data.user);
      return data.user;
    },
    async loginWithGoogle(credential, captchaToken) {
      const data = await api('/api/auth.php', { method: 'POST', body: { action: 'google', credential, captchaToken } });
      saveSnapshot(data.user);
      return data.user;
    },
    async logout() {
      try { await api('/api/auth.php', { method: 'POST', body: { action: 'logout' } }); } catch (_) {}
      saveSnapshot(null);
      location.replace('/login.html');
    },
    sendEmailNotification() { return Promise.resolve(); }
  };

  GaeksAuth.ready = GaeksAuth.refreshSession().then(user => {
    window.dispatchEvent(new CustomEvent('gaeks-auth-ready', { detail: user }));
    return user;
  });
  window.GaeksAuth = GaeksAuth;
  window.getDeterministicUserId = GaeksAuth.getDeterministicUserId;
}());
