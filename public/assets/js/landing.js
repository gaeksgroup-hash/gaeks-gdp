(function () {
  "use strict";
  var sessionChecked = false;

  function currentUser() {
    try {
      return window.GaeksAuth && typeof window.GaeksAuth.getCurrentUser === "function"
        ? window.GaeksAuth.getCurrentUser()
        : null;
    } catch (error) {
      return null;
    }
  }

  function safeInternalTarget(value) {
    var allowed = ["cv-dashboard.html", "presentation.html", "profile.html", "pricing.html"];
    return allowed.indexOf(value) >= 0 ? value : "index.html";
  }

  async function openProduct(target) {
    var destination = safeInternalTarget(target);
    var user = window.GaeksAuth && window.GaeksAuth.ready ? await window.GaeksAuth.ready : currentUser();
    if (user) {
      window.location.assign(destination);
      return;
    }
    window.location.assign("login.html?redirect=" + encodeURIComponent(destination));
  }

  function updateAccountUI() {
    var user = currentUser();
    var loginLinks = document.querySelectorAll("[data-login-link]");
    var profileLinks = document.querySelectorAll("[data-profile-link]");
    var pill = document.querySelector("[data-user-pill]");
    loginLinks.forEach(function (link) {
      var showLogin = sessionChecked && !user;
      link.hidden = !showLogin;
      link.style.display = showLogin ? "" : "none";
      link.setAttribute("aria-hidden", showLogin ? "false" : "true");
    });
    profileLinks.forEach(function (link) {
      link.hidden = !user;
      link.style.display = user ? "" : "none";
      link.setAttribute("aria-hidden", user ? "false" : "true");
    });
    if (!pill) return;
    pill.classList.toggle("is-visible", Boolean(user));
    pill.hidden = !user;
    pill.setAttribute("aria-hidden", user ? "false" : "true");
    if (!user) return;
    var avatar = pill.querySelector("[data-user-avatar]");
    var name = pill.querySelector("[data-user-name]");
    if (avatar) {
      avatar.src = user.avatar || "https://api.dicebear.com/7.x/initials/svg?seed=" + encodeURIComponent(user.name || "User");
    }
    if (name) name.textContent = user.name || "Akun saya";
  }

  function setupNavigation() {
    var button = document.querySelector("[data-menu-button]");
    var links = document.querySelector("[data-nav-links]");
    if (!button || !links) return;
    button.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(open));
    });
    links.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        links.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function setupProductActions() {
    document.querySelectorAll("[data-product-target]").forEach(function (element) {
      element.addEventListener("click", function (event) {
        event.preventDefault();
        openProduct(element.getAttribute("data-product-target"));
      });
    });
  }

  function setupReveal() {
    var elements = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      elements.forEach(function (element) { element.classList.add("is-visible"); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });
    elements.forEach(function (element) { observer.observe(element); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupNavigation();
    setupProductActions();
    setupReveal();
    updateAccountUI();
    if (window.GaeksAuth && window.GaeksAuth.ready) {
      window.GaeksAuth.ready.then(function () { sessionChecked = true; updateAccountUI(); }, function () { sessionChecked = true; updateAccountUI(); });
    } else {
      sessionChecked = true;
      updateAccountUI();
    }
  });
  window.addEventListener("pageshow", function (event) {
    updateAccountUI();
    if (event.persisted && window.GaeksAuth && typeof window.GaeksAuth.refreshSession === "function") {
      window.GaeksAuth.refreshSession().then(updateAccountUI, updateAccountUI);
    }
  });
  window.addEventListener("gaeks-auth-change", updateAccountUI);
}());
