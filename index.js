document.addEventListener('DOMContentLoaded', function () {

  /* Fill every "Relationship Manager" field from config.js so
     there is one place to change the assigned manager, instead
     of editing each form in index.html. Falls back to whatever
     is already in the HTML if config.js hasn't loaded. */
  var cfg = window.SITE_CONFIG || {};
  if (cfg.DEFAULT_DEVELOPER_NAME) {
    document.querySelectorAll('[name="developer"]').forEach(function (el) {
      el.value = cfg.DEFAULT_DEVELOPER_NAME;
    });
  }
  if (cfg.DEFAULT_MANAGER_NAME) {
    document.querySelectorAll('[name="manager_name"]').forEach(function (el) {
      el.value = cfg.DEFAULT_MANAGER_NAME;
    });
  }
  if (cfg.DEFAULT_MANAGER_EMAIL) {
    document.querySelectorAll('[name="manager_email"]').forEach(function (el) {
      el.value = cfg.DEFAULT_MANAGER_EMAIL;
    });
  }

  /* Mobile nav toggle */
  var navToggle = document.getElementById('navToggle');
  var mainNav = document.getElementById('mainNav');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    /* Close mobile nav after tapping a link */
    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mainNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* Smooth scroll for in-page anchor links (nav links only) */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var targetId = link.getAttribute('href');
      if (targetId.length > 1) {
        var target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* Back-to-top button */
  var backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 600) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    });
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =====================================================
     ENQUIRY POPUP MODAL
     Note: form validation, the Supabase insert, and the
     success message are all handled by form.js. This file
     opens/closes the popup, pre-fills the "Interested In"
     field, and — the important part — decides what happens
     AFTER a successful submit based on which button opened
     the popup ("intent"): a plain enquiry, a WhatsApp chat,
     or a call request. WhatsApp/Call never fire on their own;
     they only run once form.js confirms the enquiry was saved.
  ===================================================== */
  var CONTACT_NUMBER = '917264011256';        // +91 7264011256, no symbols, for wa.me / tel:
  var CONTACT_NUMBER_DISPLAY = '+91 7264011256';
  var pendingWaWindow = null;

  var modalOverlay = document.getElementById('modalOverlay');
  var modalClose = document.getElementById('modalClose');
  var modalForm = document.getElementById('modalForm');
  var modalInterest = document.getElementById('modal-interest');
  var modalTitle = document.getElementById('modalTitle');
  var modalSub = document.getElementById('modalSub');
  var modalSubmit = document.getElementById('modalSubmit');

  var INTENT_COPY = {
    enquire: {
      title: 'Get Best Price &amp; Floor Plans',
      sub: 'Share your details — our team will call you with pricing, floor plans and the brochure.',
      submit: 'Enquire Now'
    },
    whatsapp: {
      title: 'Chat with us on WhatsApp',
      sub: 'Share your details and WhatsApp will open with your message ready to send to our team.',
      submit: 'Continue to WhatsApp'
    },
    call: {
      title: 'Request a Call Back',
      sub: 'Share your details and we\u2019ll connect your call to ' + CONTACT_NUMBER_DISPLAY + ' right away.',
      submit: 'Continue to Call'
    }
  };

  function openModal(plan, intent) {
    if (!modalOverlay) return;

    var activeIntent = intent || 'enquire';
    modalOverlay.dataset.intent = activeIntent;

    var copy = INTENT_COPY[activeIntent] || INTENT_COPY.enquire;
    if (modalTitle) modalTitle.innerHTML = copy.title;
    if (modalSub) modalSub.textContent = copy.sub;
    if (modalSubmit) modalSubmit.textContent = copy.submit;

    if (plan && modalInterest) {
      modalInterest.value = plan;
    }

    modalOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    var firstField = document.getElementById('modal-name');
    if (firstField) {
      window.setTimeout(function () { firstField.focus(); }, 100);
    }
  }

  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (modalClose) {
    modalClose.addEventListener('click', closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) closeModal();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('open')) {
      closeModal();
    }
  });

  /* Any element marked data-open-modal opens the popup.
     Optional data-plan pre-selects that unit type (used by the
     pricing card CTAs). Optional data-intent decides what runs
     after a successful submit — defaults to a plain enquiry. */
  document.querySelectorAll('[data-open-modal]').forEach(function (el) {
    el.addEventListener('click', function () {
      openModal(el.getAttribute('data-plan'), el.getAttribute('data-intent'));
    });
  });

  /* form.js's own "submit" listener on this same form runs first
     (it was attached first, since form.js loads before this file)
     and does the async Supabase insert. This second listener runs
     synchronously right after it, in the same click — so we grab
     a blank tab HERE, while the browser still trusts this as a
     real user gesture, rather than after the async insert resolves
     (by which point some browsers block window.open as a popup). */
  if (modalForm) {
    modalForm.addEventListener('submit', function () {
      var intent = modalOverlay ? modalOverlay.dataset.intent : 'enquire';
      if (intent === 'whatsapp') {
        pendingWaWindow = window.open('', '_blank');
      }
    });
  }

  /* form.js dispatches "enquirySubmitted" on the form right after
     a successful Supabase insert. We listen for it here, and only
     act on it for the popup form — the footer form has no
     WhatsApp/Call intent tied to it. */
  if (modalForm) {
    modalForm.addEventListener('enquirySubmitted', function (e) {
      var intent = modalOverlay ? modalOverlay.dataset.intent : 'enquire';
      var detail = e.detail || {};

      if (intent === 'whatsapp') {
        var message =
          'Hi, I\'m ' + (detail.name || '') + '. ' +
          'I\'m interested in ' + (detail.interest || 'a home') +
          ' at ' + (detail.project || 'Tanish Urbania, Charholi, Pune') + '. ' +
          'My phone number is ' + (detail.phone || '') + '. ' +
          'Please share more details.';
        var waUrl = 'https://wa.me/' + CONTACT_NUMBER + '?text=' + encodeURIComponent(message);

        if (pendingWaWindow && !pendingWaWindow.closed) {
          pendingWaWindow.location.href = waUrl;
        } else {
          window.open(waUrl, '_blank');
        }
        pendingWaWindow = null;

      } else if (intent === 'call') {
        window.setTimeout(function () {
          window.location.href = 'tel:+' + CONTACT_NUMBER;
        }, 300);
      }
    });
  }

  /* Auto-open the popup ONCE, 15 seconds after the page loads (or is
     refreshed). It never re-opens by itself: if the visitor already
     opened or closed it, or is typing in a form, it stays away. */
  var AUTO_OPEN_DELAY_MS = 15000;
  window.setTimeout(function () {
    var a = document.activeElement;
    var typing = a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName);
    if (modalOverlay && !modalOverlay.classList.contains('open') && !typing) {
      openModal();
    }
  }, AUTO_OPEN_DELAY_MS);

});
