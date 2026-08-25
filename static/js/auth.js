// 문구 번역은 books.js의 t() / I18N_DICT 하나만 사용한다.
// (auth.js가 먼저 로드되지만 books.js가 같은 이름의 전역 함수를 다시 선언하므로,
//  여기에 래퍼를 두면 실행되지 않는 죽은 코드가 된다. t()가 실제로 불리는 시점은
//  사용자가 버튼을 누른 뒤라 books.js는 이미 준비돼 있다.)
// === AUTH & ACCOUNT MODULE ===
    /* ── AUTH LOGIC ── */
    var isLoggedIn = false;
    var currentUser = null;
    var CURRENT_USER_ID = 'ME';
    var assignedNick = '';
    // ── 전역 토스트 알림 ──
    function showToast(msg) {
      var t = document.getElementById('toast');
      if (!t) return;
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(function() { t.classList.remove('show'); }, 2200);
    }
    // ── 독서 닉네임 풀 ──
    var NICK_POOL = [
      '달빛독자','밤의활자','봄의문장','녹색독자','책상물림',
      '오후의책장','새벽서재','첫문장','여백의독자','침묵의장',
      '책등의향기','마지막페이지','낡은책방','서재의먼지','여름책장',
      '밑줄긋기','활자의숲','접힌페이지','독서의계절','북마크',
      '손때묻은책','조용한독자','문장수집가','책귀접기','여백의미',
      '늦은독서','오래된책방','단어사냥꾼','감상가','첫독자',
    ];
    function pickRandomNick() {
      return NICK_POOL[Math.floor(Math.random() * NICK_POOL.length)];
    }
    function clearLoginForm() {
      ['login-email', 'login-pw'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.value = '';
      });
      ['login-email-err', 'login-pw-err'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
    }
    async function clearSignupForm() {
      ['signup-email', 'signup-pw'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.value = '';
      });
      ['signup-email-err', 'signup-pw-err'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
      // 회원가입 전용 유니크 독서 닉네임 백엔드 실시간 배정
      assignedNick = '';
      var display = document.getElementById('signup-nick-display');
      if (display) display.textContent = t('auth_nick_loading');
      try {
        var res = await fetch('/api/auth/generate-nickname');
        if (res.ok) {
          var data = await res.json();
          assignedNick = data.nickname;
          if (display) display.textContent = assignedNick;
        } else {
          assignedNick = '가공의독서가' + Math.floor(Math.random() * 1000);
          if (display) display.textContent = assignedNick;
        }
      } catch (err) {
        assignedNick = '가공의독서가' + Math.floor(Math.random() * 1000);
        if (display) display.textContent = assignedNick;
      }
    }
    async function submitLogin() {
      var email = document.getElementById('login-email').value.trim();
      var pw = document.getElementById('login-pw').value;
      var ok = true;
      if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        var err = document.getElementById('login-email-err');
        if (err) err.style.display = 'block';
        ok = false;
      } else {
        var err = document.getElementById('login-email-err');
        if (err) err.style.display = 'none';
      }
      if (!pw || pw.length < 8) {
        var err = document.getElementById('login-pw-err');
        if (err) err.style.display = 'block';
        ok = false;
      } else {
        var err = document.getElementById('login-pw-err');
        if (err) err.style.display = 'none';
      }
      if (!ok) return;
      try {
        var res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, password: pw })
        });
        if (res.ok) {
          var data = await res.json();
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('user_nickname', data.nickname);
          localStorage.setItem('user_email', data.email);
          localStorage.setItem('user_is_admin', data.is_admin);
          isLoggedIn = true;
          currentUser = { name: data.nickname, nickname: data.nickname, email: data.email, isAdmin: data.is_admin };
          try {
            var profileRes = await fetch('/api/auth/me', {
              method: 'GET',
              headers: { 'Authorization': 'Bearer ' + data.access_token }
            });
            if (profileRes.ok) {
              var profileData = await profileRes.json();
              CURRENT_USER_ID = profileData.id;
              localStorage.setItem('user_id', profileData.id);
            }
          } catch (e) {
            console.error('로그인 시 회원 고유 ID 조회 중 에러:', e);
          }
          // 전역 navbar 정보 갱신
          updateNavbar();
          if (typeof updateAuthUI === 'function') updateAuthUI();
          // 내 서재 로드
          await loadMyLibrary();
          // 메인 홈 이동
          goPage('home');
          renderHome();
        } else {
          var errData = await res.json();
          alert(errData.detail || t('alert_login_failed'));
        }
      } catch (err) {
        console.error('로그인 에러:', err);
        alert('서버와 통신할 수 없습니다.');
      }
    }
    async function submitSignup() {
      var email = document.getElementById('signup-email').value.trim();
      var pw = document.getElementById('signup-pw').value;
      var ok = true;
      if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        var err = document.getElementById('signup-email-err');
        if (err) err.style.display = 'block';
        ok = false;
      } else {
        var err = document.getElementById('signup-email-err');
        if (err) err.style.display = 'none';
      }
      if (!pw || pw.length < 8) {
        var err = document.getElementById('signup-pw-err');
        if (err) err.style.display = 'block';
        ok = false;
      } else {
        var err = document.getElementById('signup-pw-err');
        if (err) err.style.display = 'none';
      }
      if (!ok) return;
      if (!assignedNick) {
        alert(t('alert_nick_missing'));
        return;
      }
      try {
        var res = await fetch('/api/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, password: pw, nickname: assignedNick })
        });
        if (res.status === 201) {
          alert(t('alert_signup_done'));
          goPage('login');
          clearLoginForm();
        } else {
          var errData = await res.json();
          alert(errData.detail || t('alert_signup_failed'));
        }
      } catch (err) {
        console.error('회원가입 에러:', err);
        alert('서버와 통신할 수 없습니다.');
      }
    }
    function logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user_nickname');
      localStorage.removeItem('user_email');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_is_admin');
      isLoggedIn = false;
      currentUser = null;
      CURRENT_USER_ID = 'ME';
      // 내 서재 및 도서 데이터 캐시 클리어
      if (typeof libBooks !== 'undefined') libBooks = [];
      if (typeof myLibraryData !== 'undefined') myLibraryData = [];
      updateNavbar();
      if (typeof updateAuthUI === 'function') updateAuthUI();
      goPage('home');
      renderHome();
    }
    function updateNavbar() {
      if (typeof updateAuthUI === 'function') {
        updateAuthUI();
      }
    }

    // 프로필 편집 모달 제어 함수
    function openProfileEditModal() {
      document.getElementById('edit-curr-pw').value = '';
      document.getElementById('edit-new-pw').value = '';
      document.getElementById('edit-confirm-pw').value = '';
      document.getElementById('withdraw-pw').value = '';
      document.getElementById('profile-edit-modal').style.display = 'flex';
    }

    function closeProfileEditModal() {
      document.getElementById('profile-edit-modal').style.display = 'none';
    }

    // 비밀번호 변경 적용
    async function submitChangePassword() {
      var currPw = document.getElementById('edit-curr-pw').value.trim();
      var newPw = document.getElementById('edit-new-pw').value.trim();
      var confirmPw = document.getElementById('edit-confirm-pw').value.trim();

      if (!currPw || !newPw || !confirmPw) {
        alert(t('alert_fill_all'));
        return;
      }
      if (newPw.length < 8) {
        alert(t('alert_pw_short'));
        return;
      }
      if (newPw !== confirmPw) {
        alert(t('alert_pw_mismatch'));
        return;
      }

      var token = localStorage.getItem('token');
      try {
        var res = await fetch('/api/auth/change-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({
            current_password: currPw,
            new_password: newPw
          })
        });

        var data = await res.json();
        if (res.ok) {
          alert(data.message || t('alert_pw_changed'));
        // 서버가 기존 토큰을 무효화했으므로(비밀번호 변경 시 password_changed_at 갱신),
        // 화면만 로그인 상태로 남겨두면 이후 모든 요청이 401이 되는 '좀비 세션'이 된다.
        localStorage.removeItem('token');
        localStorage.removeItem('user_nickname');
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_is_admin');
        isLoggedIn = false;
        if (typeof updateAuthUI === 'function') updateAuthUI();
        goPage('login');
          closeProfileEditModal();
        } else {
          alert(data.detail || t('alert_pw_change_failed'));
        }
      } catch (err) {
        console.error(err);
        alert('서버와 통신하는 도중 오류가 발생했습니다.');
      }
    }

    // 회원탈퇴 및 계정 삭제
    async function submitWithdraw() {
      var pw = document.getElementById('withdraw-pw').value.trim();
      if (!pw) {
        alert(t('alert_pw_required_withdraw'));
        return;
      }
      if (!confirm('정말로 가공독서회를 탈퇴하시겠습니까?\n탈퇴 시 모든 데이터는 영구 파기되며 절대 복구할 수 없습니다.')) {
        return;
      }

      var token = localStorage.getItem('token');
      try {
        var res = await fetch('/api/auth/withdraw', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({ password: pw })
        });

        var data = await res.json();
        if (res.ok) {
          alert(data.message || t('alert_withdraw_done'));
          closeProfileEditModal();

          // 로그아웃 및 홈화면 강제 이동
          localStorage.removeItem('token');
          localStorage.removeItem('user_nickname');
          localStorage.removeItem('user_email');
          localStorage.removeItem('user_id');
          localStorage.removeItem('user_is_admin');
          isLoggedIn = false;
          currentUser = null;
          CURRENT_USER_ID = null;

          // UI 리렌더링 및 홈 이동

          goPage('home');
          updateNavbar();
          if (typeof updateAuthUI === 'function') updateAuthUI();
        } else {
          alert(data.detail || t('alert_withdraw_failed'));
        }
      } catch (err) {
        console.error(err);
        alert('서버와 통신하는 도중 오류가 발생했습니다.');
      }
    }

    function updateAuthUI() {
      var navAuth = document.getElementById('nav-auth-area');
      var lang = (typeof CURRENT_LANG !== 'undefined') ? CURRENT_LANG : 'ko';
      if (navAuth) {
        if (isLoggedIn) {
          navAuth.innerHTML = '<button class="nav-btn-logout-red" id="nav-logout-btn" onclick="handleLogout()">' + t('auth_logout_btn') + '</button>';
        } else {
          navAuth.innerHTML = '<button class="nav-btn" id="nav-login-btn" onclick="goPage(\'auth-gate\')">' + t('auth_login_btn') + '</button>';
        }
      }

      // 내 서재 프로필 카드 업데이트 (회원 가입 당시 부여받은 실제 닉네임 연동)
      var profName = document.getElementById('lib-profile-name');
      var profEmail = document.getElementById('lib-profile-email');
      var profAvatar = document.getElementById('lib-profile-avatar');

      var userNick = localStorage.getItem('user_nickname')
        || (typeof currentUser !== 'undefined' && currentUser && currentUser.name)
        || (lang === 'ja' ? '読者' : '독자');
      var userEmail = localStorage.getItem('user_email')
        || (typeof currentUser !== 'undefined' && currentUser && currentUser.email)
        || '';

      if (isLoggedIn) {
        if (profName) profName.textContent = userNick;
        if (profAvatar) profAvatar.textContent = userNick.charAt(0);
        if (profEmail) profEmail.textContent = userEmail;
      }
    }

    // 글로벌 로그아웃 공통 처리
    function handleLogout() {
      if (!confirm(t('confirm_logout'))) return;
      logout();
      showToast(t('toast_logout_done'));
    }

    // 비밀번호 찾기 모달 제어 및 API 호출
    function openFindPasswordModal() {
      document.getElementById('find-pw-email').value = '';
      document.getElementById('find-password-modal').style.display = 'flex';
    }

    function closeFindPasswordModal() {
      document.getElementById('find-password-modal').style.display = 'none';
    }

    async function submitFindPassword() {
      var emailInput = document.getElementById('find-pw-email');
      var email = emailInput.value.trim();
      var submitBtn = document.getElementById('find-pw-submit-btn');

      if (!email) {
        alert(t('alert_email_required'));
        return;
      }

      // 간단한 이메일 정규식 검증
      var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert(t('alert_email_invalid'));
        return;
      }

      // 더블 클릭 및 중복 전송 방지 로딩 피드백
      submitBtn.disabled = true;
      submitBtn.textContent = t('reset_sending');

      try {
        var res = await fetch('/api/auth/find-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: email })
        });

        var data = await res.json();
        if (res.ok) {
          alert(data.message || t('reset_sent'));
          closeFindPasswordModal();
        } else {
          alert(data.detail || '이메일 확인에 실패했습니다. 등록 정보를 재확인해 주세요.');
        }
      } catch (err) {
        console.error(err);
        alert('서버 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = t('reset_send_btn');
      }
    }

    // ── Global Window Exports ──
    window.handleLogout = handleLogout;
    window.logout = logout;
    window.updateAuthUI = updateAuthUI;
    window.updateNavbar = updateNavbar;
    window.showToast = showToast;
    window.submitLogin = submitLogin;
    window.submitSignup = submitSignup;
    window.clearLoginForm = clearLoginForm;
    window.clearSignupForm = clearSignupForm;
    window.openProfileEditModal = openProfileEditModal;
    window.closeProfileEditModal = closeProfileEditModal;
    window.openFindPasswordModal = openFindPasswordModal;
    window.closeFindPasswordModal = closeFindPasswordModal;
    window.submitFindPassword = submitFindPassword;

