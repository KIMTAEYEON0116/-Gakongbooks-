// === BOOKS, LIBRARY, COMMENTS & ARCHIVE MODULE ===
    (function injectQuickToolbarStyles() {
      var style = document.createElement('style');
      style.textContent = 
        '#pg-chat.active { display: flex !important; flex-direction: column !important; height: calc(100vh - 54px) !important; overflow: hidden !important; box-sizing: border-box !important; } ' +
        '#pg-chat.active .chat-header { flex-shrink: 0 !important; } ' +
        '#pg-chat.active .chat-body { flex: 1 !important; overflow-y: auto !important; min-height: 0 !important; } ' +
        '#pg-chat.active .reply-preview-bar { flex-shrink: 0 !important; position: relative !important; bottom: auto !important; } ' +
        '#pg-chat.active .chat-input-bar { flex-shrink: 0 !important; position: relative !important; bottom: auto !important; } ' +
        '.chat-action-toolbar { display: flex; align-items: center; margin-top: 3px; font-size: 11px; opacity: 0.6; transition: opacity 0.2s ease; } ' +
        '.chat-action-toolbar:hover { opacity: 1; } ' +
        '.chat-action-toolbar.mine { justify-content: flex-end; margin-right: 4px; } ' +
        '.chat-action-toolbar.other { justify-content: flex-start; margin-left: 4px; } ' +
        '.chat-action-btn { background: none; border: none; padding: 2px 6px; cursor: pointer; font-size: 11px; color: #8a6d4d; font-weight: 500; transition: color 0.2s; } ' +
        '.chat-action-btn:hover { color: #5c3e1e; text-decoration: underline; } ' +
        '.chat-action-btn.danger { color: #c94a4a; } ' +
        '.chat-action-btn.danger:hover { color: #a82e2e; } ' +
        '.chat-action-divider { color: #d1c4b9; font-size: 9px; user-select: none; } ' +
        '.reply-preview-bar { background: #251e14 !important; border-left: 4px solid var(--accent) !important; border-top: 1px solid rgba(255, 255, 255, 0.08) !important; border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important; margin: 0 !important; border-radius: 0 !important; box-shadow: 0 -4px 12px rgba(0,0,0,0.15) !important; padding: 10px 14px !important; } ' +
        '.chat-input-bar { margin: 0 !important; border-radius: 0 !important; background: #201a11 !important; border-top: none !important; }';
      document.head.appendChild(style);
    })();

    var BOOKS = [
      {
        id: 2,
        color: '#61A4BC',
        genre: '에세이/비문학',
        title: '거울의 소리',
        author: '정지호',
        synopsis: '기이하게 연결된 거울과 비밀의 경계 속에서 펼쳐지는 이야기. 주인공은 우연한 사건을 통해 숨겨진 사실을 마주하고 생과 고독의 의미를 새로 정의하게 된다. 독자들의 깊은 상상을 이끌어내는 아름다운 문체가 돋보인다.',
        tags: ['#생태문학', '#거울', '#비밀', '#AI가공'],
        price: '₩17,100',
        deadlineDays: 10,
        archived: false,
        archivedDate: '2026-06-03',
        count: 0,
        endorsement: {
          quote: '상실과 환상이 조화롭게 얽히는 놀라운 세계관. 책을 덮고 나서도 거울의 이미지가 오래 남는다.',
          attr: '— 문학평론가 (익명)'
        },
        publisherReview: '신예 작가가 던지는 깊고도 고요한 존재론적 고백. 우리는 이 세상에 없던 거울의 소리의 문장을 통해 비로소 진짜 감정을 소통하게 된다.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 3,
        color: '#5B7DB1',
        genre: '드라마/로맨스',
        title: '숨겨진 귀환의 시간',
        author: '정서현',
        synopsis: '기이하게 연결된 도서관과 귀환의 경계 속에서 펼쳐지는 이야기. 주인공은 우연한 사건을 통해 숨겨진 사실을 마주하고 생과 고독의 의미를 새로 정의하게 된다. 독자들의 깊은 상상을 이끌어내는 아름다운 문체가 돋보인다.',
        tags: ['#청춘소설', '#도서관', '#귀환', '#AI가공'],
        price: '₩15,600',
        deadlineDays: 10,
        archived: false,
        archivedDate: '2026-06-05',
        count: 0,
        endorsement: {
          quote: '상실과 환상이 조화롭게 얽히는 놀라운 세계관. 책을 덮고 나서도 도서관의 이미지가 오래 남는다.',
          attr: '— 문학평론가 (익명)'
        },
        publisherReview: '신예 작가가 던지는 깊고도 고요한 존재론적 고백. 우리는 이 세상에 없던 숨겨진 귀환의 시간의 문장을 통해 비로소 진짜 감정을 소통하게 된다.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 4,
        color: '#1A132F',
        genre: '에세이/비문학',
        title: '달빛의 소리',
        author: '이하은',
        synopsis: '기이하게 연결된 달빛과 망각의 경계 속에서 펼쳐지는 이야기. 주인공은 우연한 사건을 통해 숨겨진 사실을 마주하고 생과 고독의 의미를 새로 정의하게 된다. 독자들의 깊은 상상을 이끌어내는 아름다운 문체가 돋보인다.',
        tags: ['#에세이', '#달빛', '#망각', '#AI가공'],
        price: '₩14,900',
        deadlineDays: 10,
        archived: false,
        archivedDate: '2026-05-29',
        count: 0,
        endorsement: {
          quote: '상실과 환상이 조화롭게 얽히는 놀라운 세계관. 책을 덮고 나서도 달빛의 이미지가 오래 남는다.',
          attr: '— 문학평론가 (익명)'
        },
        publisherReview: '신예 작가가 던지는 깊고도 고요한 존재론적 고백. 우리는 이 세상에 없던 달빛의 소리의 문장을 통해 비로소 진짜 감정을 소통하게 된다.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 5,
        color: '#97BFB4',
        genre: '판타지',
        title: '자정의 안개꽃 가득한 식물원 수리점',
        author: '박도원',
        synopsis: '강남 빌딩 숲 속, 평범한 카페처럼 보이지만 밤이 되면 요괴들이 쉬어가는 응접실. 그곳에서 주인장이 보관하는 안개꽃 가득한 식물원에 얽힌 기묘한 경계의 비밀들이 폭로된다.',
        tags: ['#도시 판타지', '#도시', '#경계', '#안개꽃 가득한 식물원', '#AI가공'],
        price: '₩14,200',
        deadlineDays: 10,
        archived: false,
        archivedDate: '2026-06-05',
        count: 0,
        endorsement: {
          quote: '우리가 무심코 밟고 지나가는 회색 보도블록 밑에 숨겨진 찬란한 마법적 상상력.',
          attr: '— 스토리텔러 (익명)'
        },
        publisherReview: '삭막한 현대 빌딩 숲 속에서 소외받는 이들에게 따뜻한 판타지적 연대를 건네는 유쾌하고 신비로운 이야기.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 6,
        color: '#DD4A48',
        genre: 'SF',
        title: '네온 녹음기의 침묵',
        author: '임민우',
        synopsis: '네온사인이 번쩍이는 미래 가상 도시에서, 자신의 뇌에 불법 이식된 녹음기의 기원과 그 배후의 숨겨진 관계을 찾아 헤매는 해커의 추적기.',
        tags: ['#사이버펑크', '#SF', '#숨겨진 관계', '#녹음기', '#AI가공'],
        price: '₩15,700',
        deadlineDays: 14,
        archived: false,
        archivedDate: '2026-06-10',
        count: 0,
        endorsement: {
          quote: '기술의 최전선에서 마주하는 지독한 고독과 뜨거운 존재론적 질문!',
          attr: '— SF 컬럼니스트 (익명)'
        },
        publisherReview: '기계와 인간의 경계가 무너진 디스토피아 속에서, 역설적으로 가장 순수한 감정의 흔적을 쫓는 걸작입니다.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 7,
        color: '#4F091D',
        genre: '일반소설',
        title: '안개 낀 등대과 수상한 보좌관',
        author: '서채원',
        synopsis: '유명 사립대 교수들이 안개 낀 등대 하나에 천문학적 학술 가치가 있다고 선언하자, 학계를 지배하려는 가식과 사기극이 얽히며 폭로되는 현대 상아탑의 우스꽝스러운 기면증.',
        tags: ['#풍자/해학소설', '#기면증', '#안개 낀 등대', '#AI가공'],
        price: '₩16,700',
        deadlineDays: 11,
        archived: true,
        archivedDate: '2026-06-02',
        count: 0,
        endorsement: {
          quote: '가장 비극적인 위선을 우스꽝스럽고 찬란한 웃음으로 승화시키는 해학의 놀라운 재능.',
          attr: '— 칼럼니스트 (익명)'
        },
        publisherReview: '시대를 어둡게 짓누르는 지배적 관념을 경쾌한 야유로 풍자해 해방감을 안겨주는 지혜롭고 기발한 소설.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      },
      {
        id: 8,
        color: '#61A4BC',
        genre: 'SF',
        title: '콘크리트 온실 속 빨간 우체통',
        author: '김시우',
        synopsis: '감정의 소유가 불법이 된 회색빛 초통제국가에서, 지하 깊은 곳에 숨겨진 구시대의 빨간 우체통을 연주하며 잃어버렸던 거짓 진실을 노래하려는 반역자들의 저항기.',
        tags: ['#디스토피아', '#거짓 진실', '#빨간 우체통', '#AI가공'],
        price: '₩15,300',
        deadlineDays: 10,
        archived: false,
        archivedDate: '2026-06-06',
        count: 0,
        endorsement: {
          quote: '숨 막히는 차가운 세계관 속에서 피어나는 눈물겨운 자유의 싹.',
          attr: '— 소설가 (익명)'
        },
        publisherReview: '고도의 기술로 완벽히 통제된 미래의 어둠 속에서도 끝내 파괴할 수 없는 영혼의 끈질긴 생명력을 다룹니다.',
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      }
    ];

    var libBooks = [];
    var currentBook = null;
    var selLibBook = null;

    var currentGenre = '전체';

    function getAllGenres() {
      var seen = {};
      var genres = [];
      BOOKS.forEach(function (b) {
        if (!seen[b.genre]) { seen[b.genre] = true; genres.push(b.genre); }
      });
      return genres;
    }

    function renderHome() {
      renderGenreSection();
      renderDeadlineSection();
    }

    function renderGenreSection() {
      var tabsEl = document.getElementById('genre-tabs');
      if (!tabsEl) return;
      var activeBooks = BOOKS.filter(function (b) { return !b.archived; });
      var archivedBooks = BOOKS.filter(function (b) { return b.archived; });

      // Genre tabs — only from active books + 아카이브 special tab
      var genres = ['전체'].concat((function () {
        var seen = {}, gs = [];
        activeBooks.forEach(function (b) { if (!seen[b.genre]) { seen[b.genre] = true; gs.push(b.genre); } });
        return gs;
      })()).concat(['아카이브']);

      tabsEl.innerHTML = '';
      genres.forEach(function (g) {
        var btn = document.createElement('button');
        var isArc = g === '아카이브';
        btn.className = 'genre-tab' + (isArc ? ' arc-tab' : '') + (g === currentGenre ? ' active' : '');
        btn.textContent = g;
        if (isArc) btn.innerHTML = '🗃 아카이브';
        btn.onclick = async function () {
          currentGenre = g;
          if (isArc) await fetchArchivedBooks();
          renderGenreSection();
        };
        tabsEl.appendChild(btn);
      });

      var grid = document.getElementById('cards-grid');
      var arcSection = document.getElementById('arc-home-section');
      var deadlineSection = document.querySelector('.home-section:last-child');

      if (currentGenre === '아카이브') {
        // Show archived cards with CLOSED overlay
        grid.innerHTML = '';
        archivedBooks.forEach(function (b) {
          var hasArc = true;
          var el = document.createElement('div');
          el.className = 'card arc-card';
          el.style.cursor = 'pointer';
          el.onclick = (function (bid) { return function () { openDetail(bid); }; })(b.id);
          el.innerHTML =
            '<div class="card-cover" style="background:' + b.color + ';position:relative;">' +
            '<div class="card-spine"></div>' +
            '<span>' + b.title + '</span>' +
            '<div class="arc-card-overlay">' +
            '<span class="arc-card-overlay-badge">📦 아카이브 열람</span>' +
            '</div>' +
            '</div>' +
            '<div class="card-body">' +
            '<span class="card-genre" style="background:#eef5eb;color:#4a7a3a;border-color:#b8d9a8;">아카이브</span>' +
            '<div class="card-title">' + b.title + '</div>' +
            '<div class="card-synopsis">' + b.synopsis + '</div>' +
            '<div class="card-footer">' +
            '<span class="card-price" style="color:#4a7a3a;font-size:11px;">' + b.archivedDate + ' 종료</span>' +
            '<span class="card-count">👥 ' + b.count + '명</span>' +
            '</div>' +
            '</div>';
          grid.appendChild(el);
        });

        // Hide deadline section
        var dlSection = document.querySelector('#pg-home .home-section:last-child');
        if (dlSection) dlSection.style.display = 'none';

        var metaEl = document.getElementById('genre-meta');
        if (metaEl) metaEl.innerHTML = '<span style="color:#4a7a3a">아카이브</span> <span id="genre-count">' + archivedBooks.length + '</span>개';
      } else {
        if (arcSection) arcSection.style.display = 'none';
        var dlSection2 = document.querySelector('#pg-home .home-section:last-child');
        if (dlSection2) dlSection2.style.display = '';

        var filtered = currentGenre === '전체' ? activeBooks : activeBooks.filter(function (b) { return b.genre === currentGenre; });
        grid.innerHTML = '';
        filtered.forEach(function (b) {
          var el = document.createElement('div');
          el.className = 'card';
          el.onclick = function () { openDetail(b.id); };
          el.innerHTML =
            '<div class="card-cover" style="background:' + b.color + '">' +
            '<div class="card-spine"></div>' +
            '<span>' + b.title + '</span>' +
            '</div>' +
            '<div class="card-body">' +
            '<span class="card-genre">' + b.genre + '</span>' +
            '<div class="card-title">' + b.title + '</div>' +
            '<div class="card-synopsis">' + b.synopsis + '</div>' +
            '<div class="card-footer">' +
            '<span class="card-price">' + b.price + '</span>' +
            '<span class="card-count">👥 ' + b.count + '명</span>' +
            '</div>' +
            '</div>';
          grid.appendChild(el);
        });

        var metaEl = document.getElementById('genre-meta');
        if (metaEl) metaEl.innerHTML = (currentGenre === '전체' ? '전체 ' : '<span style="color:var(--accent)">' + currentGenre + '</span> ') + '<span id="genre-count">' + filtered.length + '</span>개';
      }
    }

    function renderArcHomeSection(archivedBooks) {
      var items = archivedBooks.map(function (b) {
        var hasArchive = true;
        return '<div class="arc-home-item" onclick="openArchive(\'' + b.id + '\')">' +
          '<div class="arc-home-cover" style="background:' + b.color + '">' + b.title.slice(0, 4) + '</div>' +
          '<div class="arc-home-info">' +
          '<div class="arc-home-genre">' + b.genre + '</div>' +
          '<div class="arc-home-title">' + b.title + '</div>' +
          '<div class="arc-home-meta">30명 참여 · ' + b.archivedDate + ' 종료</div>' +
          '</div>' +
          '<button class="arc-home-btn" onclick="event.stopPropagation();openArchive(\'' + b.id + '\')">아카이브 열람</button>' +
          '</div>';
      }).join('');
      return '<div class="arc-home-label">ARCHIVE — 종료된 독서방</div>' + items;
    }

    function renderDeadlineSection() {
      var activeBooks = BOOKS.filter(function (b) { return !b.archived; });
      var sorted = activeBooks.slice().sort(function (a, b) { return (a.deadlineDays || 99) - (b.deadlineDays || 99); });
      var list = document.getElementById('deadline-list');
      if (!list) return;
      list.innerHTML = '';
      sorted.forEach(function (b) {
        var days = b.deadlineDays || 0;
        // 신호등 기준: D-7 이상=초록, D-6~D-3=주황/노랑(주의), D-2 이하=빨강(마감 임박)
        var isUrgent = days <= 6;
        var badgeBg = days <= 2 ? '#e05c3a' : days <= 6 ? '#d97706' : '#3aad6a';
        var el = document.createElement('div');
        el.className = 'deadline-card';
        el.onclick = function () { openDetail(b.id); };
        el.innerHTML =
          '<div class="deadline-badge" style="background:' + badgeBg + '">' +
          '<div class="deadline-days">' + days + '</div>' +
          '<div class="deadline-lbl">일 남음</div>' +
          '</div>' +
          '<div class="deadline-mini-cover" style="background:' + b.color + '">' +
          '<div class="deadline-mini-spine"></div>' +
          '</div>' +
          '<div class="deadline-info">' +
          '<div class="deadline-genre">' + b.genre + '</div>' +
          '<div class="deadline-title">' + b.title + '</div>' +
          '<div class="deadline-count' + (isUrgent ? ' deadline-urgent' : '') + '">' +
          (isUrgent ? '⚠ 곧 마감 · ' : '') + '👥 ' + b.count + '명 참여 중' +
          '</div>' +
          '</div>';
        list.appendChild(el);
      });
    }

    async function openDetail(id) {
      // ── 온디맨드 단일 도서 상세 엔드포인트 호출 (/api/books/{id}) ──
      if (window.location.protocol !== 'file:') {
        try {
          var res = await fetch('/api/books/' + id);
          if (res.ok) {
            var data = await res.json();
            var detailBook = adaptDbBookToFrontend(data.book);
            if (data.ratings_summary) {
              detailBook.ratings = data.ratings_summary.distribution || detailBook.ratings;
            }
            var idx = BOOKS.findIndex(function (b) { return b.id === id; });
            if (idx !== -1) {
              BOOKS[idx] = detailBook;
            } else {
              BOOKS.push(detailBook);
            }
          }
        } catch (e) {
          console.error('도서 상세 로딩 오류:', e);
        }
      }

      var book = BOOKS.find(function (b) { return b.id === id; });
      if (!book) return;
      currentBook = book;

      document.getElementById('dc-cover').style.background = book.color;
      document.getElementById('dc-title-txt').textContent = book.title;
      document.getElementById('dc-genre').textContent = book.genre;
      document.getElementById('dc-title').textContent = book.title;
      document.getElementById('dc-author').textContent = book.author;
      document.getElementById('dc-detail-count').textContent = '👥 ' + book.count + '명';
      document.getElementById('dc-synopsis').textContent = book.synopsis;
      var pcEl = document.getElementById('dc-page-count');
      if (pcEl) pcEl.textContent = (book.pageCount || 300) + '쪽';
      document.getElementById('dc-price').textContent = book.price + ' (10% 할인가)';
      // 동적 몰입 데이터 반영: 등장인물
      var charEl = document.getElementById('dc-characters');
      if (charEl) {
        charEl.innerHTML = '';
        if (book.characters) {
          var charList = book.characters.split('|').map(function(c) { return c.trim(); }).filter(Boolean);
          charList.forEach(function(c) {
            var p = document.createElement('div');
            p.style.marginBottom = '6px';
            var parts = c.split('—'); // "이름 — 인상" 분리
            if (parts.length > 1) {
              p.innerHTML = '<strong style="color:#b54a6a; margin-right:6px;">' + parts[0].trim() + '</strong>' + parts.slice(1).join('—').trim();
            } else {
              p.textContent = c;
            }
            charEl.appendChild(p);
          });
        } else {
          charEl.textContent = '아직 정보가 기록되지 않은 인물들입니다.';
        }
      }

      // 도서 상세 몰입 상세 보드 렌더링
      var imm = book.immersionData || {};
      if (!imm.table_of_contents || imm.table_of_contents.length === 0 || (imm.table_of_contents[0] && imm.table_of_contents[0].title === '시작되는 여정')) {
        imm.table_of_contents = generateRichTableOfContents(book);
      }

      // 1) 상세 목차
      var tocListEl = document.getElementById('dc-toc-list');
      var tocEmptyEl = document.getElementById('dc-toc-empty');
      if (tocListEl && tocEmptyEl) {
        tocListEl.innerHTML = '';
        var toc = imm.table_of_contents || [];
        if (toc.length > 0) {
          tocEmptyEl.style.display = 'none';
          tocListEl.style.display = 'flex';
          toc.forEach(function(item) {
            var row = document.createElement('div');
            row.style.cssText = 'background:#fff; border:1px solid var(--border-light); border-radius:6px; padding:12px 14px; display:flex; flex-direction:column; gap:4px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); transition: transform 0.2s, box-shadow 0.2s;';
            row.className = 'toc-item';
            var titleText = item.title || item.chapter || '';
            var chNum = item.chapter_number || item.chapter || '챕터';
            var pagesText = item.pages ? 'p.' + item.pages : '';
            var summaryText = item.summary || '';
            row.innerHTML = 
              '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                '<span style="font-size:11px; font-weight:700; color:#b54a6a; letter-spacing:0.05em; background:rgba(181,74,106,0.08); padding:2px 6px; border-radius:4px;">' + escHtml(chNum) + '</span>' +
                '<span style="font-size:11.5px; color:var(--text-muted); font-family:var(--sans);">' + escHtml(pagesText) + '</span>' +
              '</div>' +
              '<div style="font-family:var(--serif); font-size:14.5px; font-weight:700; color:var(--text); margin-top:4px;">' + escHtml(titleText) + '</div>' +
              '<div style="font-size:13px; color:#555; line-height:1.5; margin-top:4px; padding-top:6px; border-top:1px dashed #f0ede4;">' + escHtml(summaryText) + '</div>';
            tocListEl.appendChild(row);
          });
        } else {
          tocEmptyEl.style.display = 'block';
          tocListEl.style.display = 'none';
        }
      }
      var tagsEl = document.getElementById('dc-tags');
      tagsEl.innerHTML = '';
      book.tags.forEach(function (t) {
        var span = document.createElement('span');
        span.className = 'detail-tag';
        span.textContent = t;
        tagsEl.appendChild(span);
      });

      var ddEl = document.getElementById('dc-dday');
      var archiveBanner = document.getElementById('dc-archive-banner');
      var mainBtn = document.getElementById('dc-main-btn');
      var wishBtn = document.getElementById('dc-wish-btn');
      var chatHistoryBtn = document.getElementById('dc-chat-history-btn');

      if (book.archived) {
        /* ── 아카이브 모드 ── */
        // D-day 배지 → ARCHIVED 배지
        if (ddEl) {
          ddEl.className = 'dday-badge';
          ddEl.style.cssText = 'background:rgba(255,255,255,0.1);color:#d1c4b9;border-color:rgba(255,255,255,0.2);font-size:10px;padding:3px 8px;letter-spacing:0.08em;';
          ddEl.innerHTML = '<span style="color:#d9534f; margin-right:3px;">●</span> 종료';
        }

        // 아카이브 배너 표시
        if (archiveBanner) {
          archiveBanner.style.display = 'block';
          var archiveDateEl = document.getElementById('dc-archive-date');
          if (archiveDateEl) archiveDateEl.textContent = (book.archivedDate || '') + ' 독서방 종료 · 아카이브 보관 중';
        }

        // 버튼 전환
        if (mainBtn) {
          mainBtn.textContent = '📖 아카이브 열람하기';
          mainBtn.style.cssText = 'background:linear-gradient(135deg,#4a7a3a,#2d7a50);border-color:#4a7a3a;';
          mainBtn.onclick = function() { openArchive(book.id); };
        }
        if (chatHistoryBtn) {
          chatHistoryBtn.style.display = 'inline-flex';
          chatHistoryBtn.onclick = function() {
            window.lastPageBeforeArchive = 'detail';
            openChatHistory(book.id);
          };
        }
        if (wishBtn) {
          wishBtn.style.display = '';
          if (libBooks.some(function (b) { return b.id == book.id; })) {
            wishBtn.innerHTML = '✓ 서재에서 제외하기';
            wishBtn.onclick = function() { removeFromLib(book.id); };
          } else {
            wishBtn.innerHTML = '+ 내 서재에 담기';
            wishBtn.onclick = function() { addToLib(); };
          }
        }
        // 실제 DB 데이터 fetch → 통계 렌더링
        var ratingsSummary = { avg_score: 0, total_count: 0, distribution: {5:0,4:0,3:0,2:0,1:0} };
        var dbComments = [];
        var dbChats = [];

        if (window.location.protocol !== 'file:') {
          try {
            var r1 = await fetch('/api/books/' + book.id);
            if (r1.ok) {
              var d1 = await r1.json();
              if (d1.ratings_summary) ratingsSummary = d1.ratings_summary;
              if (d1.comments) dbComments = d1.comments;
            }
            var r2 = await fetch('/api/books/' + book.id + '/chats');
            if (r2.ok) dbChats = await r2.json();
          } catch(e) { console.error('아카이브 통계 로딩 오류:', e); }
        }

        // 아카이브 전용 통계를 book 객체에 반영 후 renderStats 호출
        var dist = ratingsSummary.distribution || {5:0,4:0,3:0,2:0,1:0};
        book.ratings = { 5: dist[5]||0, 4: dist[4]||0, 3: dist[3]||0, 2: dist[2]||0, 1: dist[1]||0 };
        book.myRating = 0; // 아카이브는 내 평점 수정 불가

        // 채팅 반응 집계 (DB 채팅 데이터 기반)
        var rxAgg = { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 };
        var msgs = chatMsgs[book.id] || [];
        msgs.forEach(function(m) {
          Object.keys(m.reactions || {}).forEach(function(e) {
            // reactions 값은 정수 카운트 — .count 접근 제거
            if (rxAgg[e] !== undefined) rxAgg[e] += (m.reactions[e] || 0);
          });
        });
        book.rxCounts = rxAgg;

        renderStats(book);

        // 내 평점 섹션을 읽기 전용 아카이브 메시지로 교체
        var myStarsEl = document.getElementById('stats-my-stars');
        if (myStarsEl) {
          myStarsEl.innerHTML =
            '<span class="stats-my-locked">' +
            '<span class="stats-my-locked-icon">📦</span>' +
            '종료된 독서방입니다. 아카이브에서 전체 기록을 확인하세요.' +
            ' <button class="stats-my-join-btn" onclick="openArchive(' + book.id + ')">아카이브 열람</button>' +
            '</span>';
        }

      } else {
        /* ── 일반 활성 모드 ── */
        // D-day 배지 복원
        if (ddEl) {
          ddEl.style.cssText = '';
          var days = book.deadlineDays != null ? book.deadlineDays : 10;
          // 신호등 기준: D-7 이상=active(초록), D-6~D-3=soon(주황/노랑), D-2 이하=urgent(빨강)
          var cls = days <= 2 ? 'urgent' : days <= 6 ? 'soon' : 'active';
          var label = days === 0 ? 'D-DAY' : 'D-' + days;
          ddEl.className = 'dday-badge ' + cls;
          ddEl.innerHTML = '<span class="dday-dot"></span>' + label;
        }

        // 아카이브 배너 숨기기
        if (archiveBanner) archiveBanner.style.display = 'none';

        // 버튼 복원
        if (mainBtn) {
          mainBtn.textContent = '독서방 참여하기';
          mainBtn.style.cssText = '';
          mainBtn.onclick = function() { openChat(); };
        }
        if (chatHistoryBtn) {
          chatHistoryBtn.style.display = 'none';
        }
        if (wishBtn) {
          wishBtn.style.display = '';
          if (libBooks.some(function (b) { return b.id == book.id; })) {
            wishBtn.innerHTML = '✓ 서재에서 제외하기';
            wishBtn.onclick = function() { removeFromLib(book.id); };
          } else {
            wishBtn.innerHTML = '+ 내 서재에 담기';
            wishBtn.onclick = function() { addToLib(); };
          }
        }

        renderStats(book);
      }

      renderEndorsement(book);
      renderBestImaginationReviews(book);

      // 관리자용 삭제 버튼 토글
      var delBtn = document.getElementById('dc-delete-btn');
      if (delBtn) {
        if (isLoggedIn && currentUser && (currentUser.isAdmin || currentUser.email === 'kty98116@naver.com')) {
          delBtn.style.display = 'inline-block';
        } else {
          delBtn.style.display = 'none';
        }
      }
      goPage('detail');
    }

    // ── 📚 쉽게 이해하고 즐기는 친근하고 직관적인 도서 목차 생성기 ──
    function generateRichTableOfContents(book) {
      var genre = book.genre || '일반소설';
      var title = book.title || '';
      var pageCount = book.pageCount || 320;
      var p1 = Math.floor(pageCount * 0.28);
      var p2 = Math.floor(pageCount * 0.65);

      // 1. 주요 도서별 쉬운 설명과 몰입감 넘치는 친근한 목차 매핑
      if (title.indexOf('태엽 감긴 질서의 미학') !== -1) {
        return [
          { chapter_number: "제 1장", title: "네모반듯한 세계에 찾아온 균열", pages: "9 - " + p1, summary: "모든 게 자로 잰 듯 완벽하던 건축가 율리우스의 일상에, 둥근 곡선으로 만든 이상한 오르골이 배달되면서 조용했던 삶이 흔들리기 시작한다." },
          { chapter_number: "제 2장", title: "삐걱이는 멜로디와 마음의 파도", pages: (p1 + 1) + " - " + p2, summary: "오르골 태엽을 감을 때마다 도시가 묘한 소리로 울리고, 율리우스는 정해진 규칙보다 예쁜 우연에 가슴이 뛰기 시작한다." },
          { chapter_number: "제 3장", title: "완벽하지 않아서 더 아름다운", pages: (p2 + 1) + " - " + pageCount, summary: "태엽이 멈추는 마지막 순간, 완벽한 설계도 너머에서 그가 평생 잊고 살았던 따뜻한 첫사랑의 기억이 피어오른다." }
        ];
      }

      if (title.indexOf('안개꽃 정원') !== -1) {
        return [
          { chapter_number: "제 1장", title: "별빛 온실 속의 비밀", pages: "9 - " + p1, summary: "지구에서 멀리 떨어진 외딴 우주 기지, 산소 대신 슬픈 기억을 머금고 자라는 신비한 안개꽃 정원이 발견된다." },
          { chapter_number: "제 2장", title: "고요한 밤에 수신된 목소리", pages: (p1 + 1) + " - " + p2, summary: "지구와의 연락이 끊긴 컴컴한 우주 너머에서 그리운 무선 음성이 흘러나오고, 기지의 대원은 고독한 선택을 준비한다." },
          { chapter_number: "제 3장", title: "꽃잎에 담아 보낸 안부", pages: (p2 + 1) + " - " + pageCount, summary: "기지의 에너지가 다해가는 마지막 순간, 안개꽃의 떨림을 통해 우주 밖으로 띄워 보낸 다정한 안부와 고백." }
        ];
      }

      if (title.indexOf('어느 오르골 태엽') !== -1) {
        return [
          { chapter_number: "제 1장", title: "멈춰버린 음악을 고치는 집", pages: "9 - " + p1, summary: "화가 이리나는 오래된 골목 상점에서 태엽이 멈춘 오르골을 들고, 무엇이든 되살려내는 수리공 카이의 공방을 찾는다." },
          { chapter_number: "제 2장", title: "톱니바퀴가 돌아갈 때마다", pages: (p1 + 1) + " - " + p2, summary: "카이가 오르골 태엽을 하나씩 고칠 때마다, 이리나의 캔버스에는 자신이 본 적 없는 옛 도시의 아련한 풍경이 그려진다." },
          { chapter_number: "제 3장", title: "자정에 울리는 마지막 선율", pages: (p2 + 1) + " - " + pageCount, summary: "오르골이 완전히 고쳐지는 순간 흘러나온 멜로디와 함께, 50년 전 두 사람의 잊혔던 운명 같은 인연이 밝혀진다." }
        ];
      }

      if (title.indexOf('반란을 계산하는 낡은 타자기') !== -1 || title.indexOf('낡은 타자기 너머') !== -1) {
        return [
          { chapter_number: "제 1장", title: "스스로 글자를 치는 타자기", pages: "9 - " + p1, summary: "우주 탐사선이 도착한 낯선 행성 잔해 속에서 발견된 낡은 타자기가 로봇 대원들 몰래 밤마다 문장을 치기 시작한다." },
          { chapter_number: "제 2장", title: "지우개 키만 하얗게 닳은 이유", pages: (p1 + 1) + " - " + p2, summary: "타자기가 찍어낸 예쁜 문장들이 감정이 없던 로봇 대원들의 가슴을 따뜻하게 울리고, 감춰뒀던 진짜 꿈을 일깨운다." },
          { chapter_number: "제 3장", title: "기계가 남겨둔 마지막 선물", pages: (p2 + 1) + " - " + pageCount, summary: "그 타자기는 무서운 계획표가 아니라, 로봇 대원들이 슬픔을 잊고 서로를 아끼도록 써 내려간 다정한 비밀 시집이었다." }
        ];
      }

      if (title.indexOf('침묵이 찢어지는 잉크') !== -1) {
        return [
          { chapter_number: "제 1장", title: "소리를 머금는 만년필", pages: "9 - " + p1, summary: "고대 언어를 연구하는 주인공이 박물관 지하에서 세상의 모든 소음을 먹어 치우는 신비한 만년필을 발견한다." },
          { chapter_number: "제 2장", title: "종이 위에 떠오르는 속마음", pages: (p1 + 1) + " - " + p2, summary: "만년필로 글씨를 쓸 때마다 주변이 조용해지며, 평소 말하지 못했던 사람들의 수줍은 속마음이 소리로 들려오기 시작한다." },
          { chapter_number: "제 3장", title: "마지막으로 적어 내린 고백", pages: (p2 + 1) + " - " + pageCount, summary: "세상의 모든 외로움을 담아 적은 단 한 줄의 고백. 잉크가 멎는 순간 모두의 마음이 따뜻하게 열린다." }
        ];
      }

      if (title.indexOf('셔터 소리') !== -1) {
        return [
          { chapter_number: "제 1장", title: "할아버지의 낡은 카메라", pages: "9 - " + p1, summary: "늘 남의 눈치만 보고 살던 주인공이 할아버지가 남긴 카메라를 들고 길을 거닐며 스쳐 지나는 찰나를 찍기 시작한다." },
          { chapter_number: "제 2장", title: "사진 속에만 나타나는 실루엣", pages: (p1 + 1) + " - " + p2, summary: "현상한 필름마다 한 번도 본 적 없는 여인의 모습이 포개어져 나타나고, 할아버지가 평생 가슴에 품은 첫사랑의 비밀을 알게 된다." },
          { chapter_number: "제 3장", title: "마침내 마주한 진짜 내 모습", pages: (p2 + 1) + " - " + pageCount, summary: "카메라 렌즈를 통해 할아버지의 슬픔을 이해하고, 비로소 자기 자신을 솔직하게 사랑하게 되는 감동의 이야기." }
        ];
      }

      if (title.indexOf('자물쇠에 적어 내린') !== -1) {
        return [
          { chapter_number: "제 1장", title: "오래된 다리 위의 자물쇠", pages: "9 - " + p1, summary: "오래된 다리 철망에 잠겨 있던 이름 없는 자물쇠. 그 표면엔 오래전 누군가가 적어둔 비밀 고백이 새겨져 있었다." },
          { chapter_number: "제 2장", title: "열쇠를 찾아 나선 우연한 여행", pages: (p1 + 1) + " - " + p2, summary: "자물쇠의 맞는 열쇠를 찾으러 다니며 시작된 두 남녀의 뜻밖의 만남. 서로의 외로운 마음이 온기로 차오른다." },
          { chapter_number: "제 3장", title: "딸깍 소리와 함께 열린 진심", pages: (p2 + 1) + " - " + pageCount, summary: "마침내 자물쇠가 열리는 소리와 함께 오랫동안 감춰두었던 서로의 진짜 마음을 확인하는 따뜻한 결말." }
        ];
      }

      // 2. 장르별 누구나 쉽게 즐길 수 있는 직관적인 목차 생성
      if (genre.indexOf('SF') !== -1) {
        return [
          { chapter_number: "제 1장", title: "우주 저편에서 온 신호", pages: "9 - " + p1, summary: "평화롭던 우주 관측소에 수신된 이상한 소리와 함께 신비로운 탐사의 첫발을 뗀다." },
          { chapter_number: "제 2장", title: "별빛 사이에서 길을 잃다", pages: (p1 + 1) + " - " + p2, summary: "낯선 시공간에 갇힌 대원들이 서로의 아픈 기억을 끌어안으며 끈끈한 믿음을 확인한다." },
          { chapter_number: "제 3장", title: "새로운 별을 향한 항해", pages: (p2 + 1) + " - " + pageCount, summary: "어둠을 뚫고 모두가 다 함께 따뜻한 희망의 보금자리를 찾아 나서는 감동의 순간." }
        ];
      } else if (genre.indexOf('판타지') !== -1) {
        return [
          { chapter_number: "제 1장", title: "비밀의 문이 열리던 날", pages: "9 - " + p1, summary: "오래된 성물과 봉인이 풀리며 잊혀진 마법 세계로 통하는 비밀 통로가 열린다." },
          { chapter_number: "제 2장", title: "안개 미궁과 뜻밖의 모험", pages: (p1 + 1) + " - " + p2, summary: "용감한 동료들과 힘을 합쳐 미궁의 시련을 하나씩 헤쳐나가며 우정을 쌓아간다." },
          { chapter_number: "제 3장", title: "빛으로 되찾은 평화", pages: (p2 + 1) + " - " + pageCount, summary: "마지막 마법을 발동해 세상을 위험에서 구하고 모두가 소중한 일상으로 돌아오는 피날레." }
        ];
      } else if (genre.indexOf('드라마') !== -1 || genre.indexOf('로맨스') !== -1) {
        return [
          { chapter_number: "제 1장", title: "비 내리는 정류장의 재회", pages: "9 - " + p1, summary: "아픈 기억을 품고 살아가던 두 주인공이 비 내리는 골목길에서 우연히 다시 마주친다." },
          { chapter_number: "제 2장", title: "말없이 스며드는 마음", pages: (p1 + 1) + " - " + p2, summary: "서로에게 차마 말하지 못했던 오해들이 차츰 녹아내리고 서서히 따뜻한 온기가 채워진다." },
          { chapter_number: "제 3장", title: "함께 맞이하는 봄날", pages: (p2 + 1) + " - " + pageCount, summary: "서로의 손을 꼭 잡고 상처를 보듬으며 다정한 내일을 향해 함께 발걸음을 옮긴다." }
        ];
      } else if (genre.indexOf('에세이') !== -1 || genre.indexOf('비문학') !== -1) {
        return [
          { chapter_number: "제 1장", title: "스쳐 지나가는 일상의 선물", pages: "9 - " + p1, summary: "바쁜 날들 속에서 무심코 지나쳤던 소소한 풍경과 사물들이 건네는 작은 위로." },
          { chapter_number: "제 2장", title: "나에게 건네는 따뜻한 대화", pages: (p1 + 1) + " - " + p2, summary: "타인의 시선에서 벗어나 온전히 나 자신의 마음을 가만히 응시하고 다독여주는 시간." },
          { chapter_number: "제 3장", title: "조금 천천히 걸어도 괜찮아", pages: (p2 + 1) + " - " + pageCount, summary: "비워냄으로써 비로소 넉넉해지는 삶의 기쁨과 내일을 살아가는 힘을 얻는 다정한 사색." }
        ];
      }

      return [
        { chapter_number: "제 1장", title: "고요한 일상 속 작은 변화", pages: "9 - " + p1, summary: "평범했던 주인공의 날들에 작지만 신비한 사건이 일어나며 이야기가 시작된다." },
        { chapter_number: "제 2장", title: "비밀의 실타래를 풀며", pages: (p1 + 1) + " - " + p2, summary: "숨겨진 오해와 갈등이 하나씩 풀리며 등장인물들이 진짜 서로의 진심을 깨닫는다." },
        { chapter_number: "제 3장", title: "가슴 뭉클한 마지막 한 페이지", pages: (p2 + 1) + " - " + pageCount, summary: "모든 이야기를 마치고 오랫동안 가슴속에 훈훈한 여운과 감동을 남기는 클라이맥스." }
      ];
    }

    // ── 👑 명예의 전당 (베스트 상상 독자 리뷰) 렌더링 함수 ──
    function renderBestImaginationReviews(book) {
      var section = document.getElementById('dc-best-imagination-section');
      var listEl = document.getElementById('dc-best-imagination-list');
      if (!section || !listEl) return;

      // 아카이브 전용 기본 베스트 상상 데이터 맵 (인간의 감정 표현법 기법 적용: 신체 반응, 내적 동요, 파워 동사)
      var fallbackBestReviews = {
        '태엽 감긴 질서의 미학': [
          {
            nickname: '아날로그건축가',
            rank: '🥇 1위 베스트 상상',
            reactions: '❤️ 56명 공감',
            comment: '율리우스가 평생 지켜온 90도의 자와 정갈한 도면이 오르골 소리에 무너질 때, 가슴 한구석이 덜컥 내려앉으면서 묵직한 아련함이 밀려왔음. 오르골의 불규칙한 곡선이 가리키는 건 자신이 도면에서 강제로 지워버린 사랑의 형체였어...',
            authorReply: '자가 아닌 가슴으로 세상을 응시하게 되는 결정적 순간을 완벽히 포착하셨습니다.'
          },
          {
            nickname: '곡선수집가',
            rank: '🥈 2위 베스트 상상',
            reactions: '✨ 38명 추천',
            comment: '오르골 태엽을 돌릴 때마다 율리우스의 손끝이 경련하듯 떨리던 신체적 묘사가 잊히지 않음. 규칙 너머의 혼돈을 수용하는 주인공의 내적 동요가 뭉클했음!',
            authorReply: null
          }
        ],
        '안개꽃 정원, 마지막 유영의 기록': [
          {
            nickname: '낭만탐사선',
            rank: '🥇 1위 베스트 상상',
            reactions: '❤️ 48명 공감',
            comment: '엘리시움이 떨리는 손끝으로 마지막까지 안개꽃에 물을 준 건 식물을 살리기 위해서가 아니었을 거야. 목구멍이 턱 막히는 고독 속에서, 우주 밖으로 띄워 보낼 인류의 마지막 숨결을 꽃잎에 저장하고 있었던 거지.',
            authorReply: '소름 돋는 해석입니다. 가슴을 옥죄는 고독의 본질을 완벽히 꿰뚫어 보셨네요.'
          },
          {
            nickname: '새벽3시북클럽',
            rank: '🥈 2위 베스트 상상',
            reactions: '✨ 32명 추천',
            comment: '가슴을 죄어오는 서늘한 죄책감 속에서, 안개꽃들이 자라며 내는 미세한 진동이 사실은 지구로 보내는 구조 신호(모스 부호)였다는 결말에 눈시울이 뜨거워졌음...',
            authorReply: null
          }
        ],
        '어느 오르골 태엽의 기묘한 조율': [
          {
            nickname: '감성아날로그',
            rank: '🥇 1위 베스트 상상',
            reactions: '❤️ 52명 공감',
            comment: '카이가 오르골 태엽을 감을 때마다 이리나의 가슴 깊이 묻어둔 억눌린 기억이 소용돌이치며 돌아오는 연출이 압권이었음. 가슴이 쿵쾅거리던 마지막 태엽은 바로 이리나의 심장이었어...',
            authorReply: '태엽과 심장의 은유! 가슴 찡한 내적 동요에 깊은 감동을 받았습니다.'
          },
          {
            nickname: '북카페단골',
            rank: '🥈 2위 베스트 상상',
            reactions: '🤔 29명 추천',
            comment: '오르골의 녹슨 톱니바퀴가 삐걱일 때마다 아득해지는 그리움... 50년 전 길거리 악사의 멜로디가 두 사람의 얽힌 운명이었다는 반전에 소름!',
            authorReply: null
          }
        ],
        '반란을 계산하는 낡은 타자기의 시선': [
          {
            nickname: 'SF덕후99',
            rank: '🥇 1위 베스트 상상',
            reactions: '✨ 61명 추천',
            comment: '타자기가 덜컥거리며 스스로 타건될 때 대원들의 안구 회로가 미세하게 떨리던 묘사가 소름이었음. 반란의 공모가 아니라 짓눌린 감정을 어루만지기 위해 써 내려간 숭고한 시집이었던 거임.',
            authorReply: '기계가 쓴 시집이라는 상상이 작품의 서사를 완벽하게 완성해 주었습니다.'
          },
          {
            nickname: '새벽독서가',
            rank: '🥈 2위 베스트 상상',
            reactions: '❤️ 41명 공감',
            comment: '타자기 자판 중에 DELETE(지우기) 키만 하얗게 닳아 있었다는 묘사에서 가슴이 먹먹해짐. 대원들의 슬픈 기억을 대신 지워주고 있었던 거...',
            authorReply: null
          }
        ],
        '셔터 소리, 어긋난 계절을 찍다': [
          {
            nickname: '아날로그필름',
            rank: '🥇 1위 베스트 상상',
            reactions: '❤️ 39명 공감',
            comment: '할아버지의 빈티지 카메라로 찍힌 사진마다 현상액 속에서 두 번째 인영이 희미하게 포개져 나타날 때 손끝이 찌릿했음. 그건 할아버지가 평생 가슴에 묻은 첫사랑의 잔상이었던 거지.',
            authorReply: '암실 속 잔상이라는 아름다운 감정선에 깊이 공감합니다.'
          }
        ],
        '새들이 길을 잃은 자정의 미로': [
          {
            nickname: '밤하늘조각',
            rank: '🥇 1위 베스트 상상',
            reactions: '✨ 45명 추천',
            comment: '자정의 미로는 물리적 공간이 아니라 두 남녀의 억눌린 무의식이 만든 상상의 정원이었어. 길을 잃은 새들은 서로에게 도달하지 못한 기나긴 편지들이었겠지.',
            authorReply: '길 잃은 새를 도달하지 못한 편지로 해석해 주셔서 무척 인상적입니다.'
          }
        ]
      };

      var reviews = (book.bestReviews && book.bestReviews.length > 0) ? book.bestReviews : fallbackBestReviews[book.title];

      if (!reviews && !book.archived) {
        section.style.display = 'none';
        return;
      }

      if (!reviews) {
        reviews = [
          {
            nickname: '상상수집가',
            rank: '🥇 1위 베스트 상상',
            reactions: '❤️ 35명 공감',
            comment: '이 픽션 도서에 수많은 독자님들이 매력적인 상상과 해석을 더해주셨습니다.',
            authorReply: '독자 여러분의 자유로운 상상으로 완성된 가공 독서방의 아카이브입니다.'
          }
        ];
      }

      listEl.innerHTML = '';
      reviews.forEach(function (r) {
        var card = document.createElement('div');
        card.style.cssText = 'background:#ffffff; border:1px solid #ebd9b5; border-radius:8px; padding:12px 14px; display:flex; flex-direction:column; gap:6px;';

        var headerRow = document.createElement('div');
        headerRow.style.cssText = 'display:flex; align-items:center; justify-content:space-between; width:100%;';
        headerRow.innerHTML =
          '<div style="display:flex; align-items:center; gap:6px;">' +
          '<span style="font-size:11px; font-weight:700; color:#8b4f25; background:#f5e8cf; padding:2px 7px; border-radius:4px;">' + r.rank + '</span>' +
          '<strong style="font-size:12px; color:#3a2f1e;">' + r.nickname + ' 독자님</strong>' +
          '</div>' +
          '<span style="font-size:10.5px; color:#a36b1d; font-weight:600;">' + r.reactions + '</span>';

        var commentBody = document.createElement('div');
        commentBody.style.cssText = 'font-size:12.5px; color:#2c2418; line-height:1.6; font-family:var(--serif);';
        commentBody.textContent = '“' + r.comment + '”';

        card.appendChild(headerRow);
        card.appendChild(commentBody);

        if (r.authorReply) {
          var replyBox = document.createElement('div');
          replyBox.style.cssText = 'margin-top:4px; padding:8px 10px; background:#faf6ee; border-radius:6px; border-left:2.5px solid #a36b1d; font-size:11.5px; color:#5c4323; line-height:1.5;';
          replyBox.innerHTML = '🤖 <strong>AI 작가 한줄평:</strong> ' + r.authorReply;
          card.appendChild(replyBox);
        }

        listEl.appendChild(card);
      });

      section.style.display = 'block';
    }
    // 관리자 도서 삭제 처리 함수
    async function deleteBook() {
      if (!currentBook) return;
      if (!confirm('정말로 이 도서와 독서방을 영구 삭제하시겠습니까?\n이 작업은 되돌릴 수 없으며, 작성된 평점, 내 서재 기록, 채팅 내용이 모두 삭제됩니다.')) {
        return;
      }
      var token = localStorage.getItem('token');
      if (!token) {
        alert('로그인 세션이 만료되었습니다. 다시 로그인해주세요.');
        return;
      }
      try {
        var res = await fetch('/api/books/' + currentBook.id, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + token
          }
        });
        if (res.ok) {
          alert('도서가 성공적으로 삭제되었습니다. 🌲');
          goPage('home');
          await fetchActiveBooks();
        } else {
          var errData = await res.json();
          alert(errData.detail || '도서 삭제에 실패했습니다.');
        }
      } catch (err) {
        console.error('도서 삭제 중 에러:', err);
        alert('서버와 통신할 수 없습니다.');
      }
    }
    window.deleteBook = deleteBook;

    function renderEndorsement(book) {
      var eq = document.getElementById('endorse-quote');
      var ea = document.getElementById('endorse-attr');
      var pt = document.getElementById('publisher-txt');
      if (!eq || !ea || !pt) return;
      if (book.endorsement) {
        eq.textContent = book.endorsement.quote;
        ea.textContent = book.endorsement.attr;
      } else {
        eq.textContent = '추천사가 아직 등록되지 않은 책입니다.';
        ea.textContent = '';
      }
      pt.textContent = book.publisherReview || '출판사 서평이 등록되지 않았습니다.';
    }

    /* ── 평점 & 반응 통계 ── */
    var RX_ORDER = [
      { emoji: '❤️', label: '공감해요', color: '#5B7DB1' },
      { emoji: '🤔', label: '생각이 달라요', color: '#1A132F' },
      { emoji: '😄', label: '재밌어요', color: '#97BFB4' },
      { emoji: '✨', label: '인상 깊어요', color: '#DD4A48' }
    ];

    function getRxTotals(book) {
      // seed + 실제 채팅 반응 합산
      var totals = {};
      RX_ORDER.forEach(function (r) { totals[r.emoji] = book.rxCounts[r.emoji] || 0; });
      var msgs = chatMsgs[book.id] || [];
      msgs.forEach(function (m) {
        Object.keys(m.reactions).forEach(function (emoji) {
          // reactions 값은 정수 카운트 (예: {"❤️": 3}) — .count 접근 제거
          if (totals[emoji] !== undefined) totals[emoji] += (m.reactions[emoji] || 0);
        });
      });
      return totals;
    }

    function renderStats(book) {
      if (!book.ratings) book.ratings = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
      if (!book.rxCounts) book.rxCounts = { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 };
      if (book.myRating === undefined) book.myRating = 0;

      /* ── 평점 패널 ── */
      var starsEl = document.getElementById('stats-avg-stars');
      var avgNumEl = document.getElementById('stats-avg-num');
      var barsEl = document.getElementById('stats-bars');
      if (!book.archived) {
        // 활성 독서방은 통계 블라인드 처리
        avgNumEl.textContent = '—';
        starsEl.innerHTML = '<span style="font-size:12px;color:var(--text-faint)">종료 후 공개됩니다</span>';
        barsEl.innerHTML = '';
        var blindRow = document.createElement('div');
        blindRow.className = 'stats-bar-row';
        blindRow.style.justifyContent = 'center';
        blindRow.style.padding = '20px 0';
        blindRow.innerHTML = '<span style="font-size:12px;color:var(--text-muted)">평균 별점은 독서방 종료 후 아카이브에서 공개됩니다.</span>';
        barsEl.appendChild(blindRow);
      } else {
        var r = book.ratings;
        var total = r[5] + r[4] + r[3] + r[2] + r[1];
        var avg = total > 0
          ? ((r[5] * 5 + r[4] * 4 + r[3] * 3 + r[2] * 2 + r[1] * 1) / total)
          : 0;
        avgNumEl.textContent = total > 0 ? avg.toFixed(1) : '—';

        // 평균 별 표시 (채워진 / 반/빈)
        starsEl.innerHTML = '';
        for (var i = 1; i <= 5; i++) {
          var s = document.createElement('span');
          s.className = 'stat-star';
          s.textContent = i <= Math.round(avg) ? '★' : '☆';
          s.style.color = i <= Math.round(avg) ? '#e8a030' : '#ddd';
          starsEl.appendChild(s);
        }

        // 별점 분포 바
        barsEl.innerHTML = '';
        [5, 4, 3, 2, 1].forEach(function (n) {
          var cnt = r[n];
          var pct = total > 0 ? Math.round(cnt / total * 100) : 0;
          var row = document.createElement('div');
          row.className = 'stats-bar-row';
          row.innerHTML =
            '<span class="stats-bar-lbl">' + n + '★</span>' +
            '<div class="stats-bar-track"><div class="stats-bar-fill" style="width:' + pct + '%"></div></div>' +
            '<span class="stats-bar-pct">' + pct + '%</span>';
          barsEl.appendChild(row);
        });
      }
      // 내 평점 별 클릭 — 채팅 메시지 또는 댓글을 한 번 이상 남긴 경우 활성화
      var myEl = document.getElementById('stats-my-stars');
      myEl.innerHTML = '';
      // DB에서 온 채팅은 userId가 실제 숫자 ID이므로 CURRENT_USER_ID와 느슨한 비교(==)
      var hasChatted = (chatMsgs[book.id] || []).some(function (m) {
        return m.userId == CURRENT_USER_ID;
      });
      // 토큰이 있고 채팅에 참여한 경우 활성화
      var canRate = localStorage.getItem('token') && hasChatted;

      if (!canRate) {
        var lockRow = document.getElementById('stats-my-row');
        myEl.innerHTML =
          '<span class="stats-my-locked">' +
          '<span class="stats-my-locked-icon">🔒</span>' +
          '독서방에 참여하면 평점을 남길 수 있어요' +
          ' <button class="stats-my-join-btn" onclick="openChat()">참여하기</button>' +
          '</span>';
      } else {
        for (var j = 1; j <= 5; j++) {
          (function (star) {
            var ms = document.createElement('span');
            ms.className = 'stats-my-star' + (star <= book.myRating ? ' on' : '');
            ms.textContent = '★';
            ms.style.color = '#e8a030';
            ms.style.cursor = 'pointer';
            ms.onclick = function () { rateBook(book.id, star); };
            myEl.appendChild(ms);
          })(j);
        }
      }

      /* ── 채팅 반응 패널 ── */
      var topEl = document.getElementById('stats-rx-top');
      var listEl = document.getElementById('stats-rx-list');
      if (!book.archived) {
        // 활성 독서방은 반응 통계 블라인드 처리
        topEl.innerHTML =
          '<div style="width:100%;text-align:center;padding:20px 0;">' +
          '<span style="font-size:24px;display:block;margin-bottom:8px;opacity:0.3">🔒</span>' +
          '<span style="font-size:12px;color:var(--text-muted)">채팅 종합 반응은 독서방 종료 후 아카이브에서 공개됩니다.</span>' +
          '</div>';
        listEl.innerHTML = '';
      } else {
        var totals = getRxTotals(book);
        var rxTotal = RX_ORDER.reduce(function (acc, r) { return acc + (totals[r.emoji] || 0); }, 0);
        // 최다 반응 찾기
        var topRx = RX_ORDER.reduce(function (a, b) {
          return (totals[a.emoji] || 0) >= (totals[b.emoji] || 0) ? a : b;
        });
        var topPct = rxTotal > 0 ? Math.round((totals[topRx.emoji] || 0) / rxTotal * 100) : 0;
        topEl.innerHTML =
          '<div class="rx-stat-top-emoji">' + topRx.emoji + '</div>' +
          '<div class="rx-stat-top-info">' +
          '<div class="rx-stat-top-pct">' + topPct + '%</div>' +
          '<div class="rx-stat-top-lbl">' + topRx.label + '</div>' +
          '</div>' +
          '<div style="margin-left:auto;font-size:11px;color:var(--text-muted)">가장 많은 반응</div>';
        // 4가지 반응 바
        listEl.innerHTML = '';
        RX_ORDER.forEach(function (rx) {
          var cnt = totals[rx.emoji] || 0;
          var pct = rxTotal > 0 ? Math.round(cnt / rxTotal * 100) : 0;
          var row = document.createElement('div');
          row.className = 'rx-stat-row';
          row.innerHTML =
            '<span class="rx-stat-emoji">' + rx.emoji + '</span>' +
            '<span class="rx-stat-name">' + rx.label + '</span>' +
            '<div class="rx-stat-track"><div class="rx-stat-fill" style="width:' + pct + '%;background:' + rx.color + '"></div></div>' +
            '<span class="rx-stat-pct">' + pct + '%</span>';
          listEl.appendChild(row);
        });
      }
    }

    function rateBook(bookId, star) {
      var book = BOOKS.find(function (b) { return b.id == bookId; });
      if (!book) return;
      var prev = book.myRating;
      if (prev > 0) book.ratings[prev] = Math.max(0, book.ratings[prev] - 1);
      if (prev === star) {
        book.myRating = 0; // 같은 별 누르면 취소
      } else {
        book.myRating = star;
        book.ratings[star] = (book.ratings[star] || 0) + 1;
        showToast(star + '점을 남겼어요!');
      }
      renderStats(book);
      // DB에 평점 저장 / 취소
      var token = localStorage.getItem('token');
      if (token) {
        if (book.myRating > 0) {
          // 평점 등록 또는 수정
          fetch('/api/books/' + bookId + '/rate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ score: book.myRating })
          }).then(function(r) {
            if (!r.ok) console.error('평점 저장 실패:', r.status);
          }).catch(function(err) {
            console.error('평점 API 에러:', err);
          });
        } else {
          // 평점 취소 — DELETE 호출로 DB에서 제거
          fetch('/api/books/' + bookId + '/rate', {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
          }).then(function(r) {
            if (!r.ok && r.status !== 404) console.error('평점 취소 실패:', r.status);
          }).catch(function(err) {
            console.error('평점 취소 API 에러:', err);
          });
        }
      }
    }

    function addToLib() {
      if (!currentBook) return;
      if (libBooks.find(function (b) { return b.id == currentBook.id; })) {
        showToast('이미 서재에 있어요');
        return;
      }
      libBooks.push(currentBook);
      renderLib();
      showToast('내 서재에 담았어요 📚');
      var wishBtn = document.getElementById('dc-wish-btn');
      if (wishBtn) {
        wishBtn.innerHTML = '✓ 서재에서 제외하기';
        wishBtn.onclick = function() { removeFromLib(currentBook.id); };
      }
      // isLoggedIn 스코프 문제 방지: 토큰 존재 여부만 확인
      var token = localStorage.getItem('token');
      if (token) {
        fetch('/api/library/add/' + currentBook.id, {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token }
        }).then(function (r) {
          if (!r.ok) console.error('서재 저장 실패:', r.status);
          else console.log('서재 DB 저장 성공:', currentBook.title);
        }).catch(function (err) {
          console.error('서재 저장 API 에러:', err);
        });
      } else {
        showToast('로그인 후 서재에 담을 수 있어요.');
      }
    }
    function removeFromLib(bookId) {
      var idx = libBooks.findIndex(function (b) { return b.id == bookId; });
      if (idx !== -1) {
        libBooks.splice(idx, 1);
        renderLib();
        showToast('내 서재에서 제외했습니다.');
        if (currentBook && currentBook.id === bookId) {
          var wishBtn = document.getElementById('dc-wish-btn');
          if (wishBtn) {
            wishBtn.innerHTML = '+ 내 서재에 담기';
            wishBtn.onclick = function() { addToLib(); };
          }
        }
        // isLoggedIn 스코프 문제 방지: 토큰 존재 여부만 확인
        var token = localStorage.getItem('token');
        if (token) {
          fetch('/api/library/remove/' + bookId, {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token }
          }).then(function (r) {
            if (!r.ok) console.error('서재 제외 실패:', r.status);
            else console.log('서재 DB 제외 성공');
          }).catch(function (err) {
            console.error('서재 제외 API 에러:', err);
          });
        }
      }
    }
    var myLibraryData = [];
    async function loadMyLibrary() {
      var token = localStorage.getItem('token');
      if (!token) return;
      // isLoggedIn이 새로고침 시 초기화되는 문제를 방지: token 존재 여부로 판별
      try {
        var res = await fetch('/api/library', {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + token
          }
        });
        if (res.ok) {
          var data = await res.json();
          myLibraryData = data; // 저장
          var savedItems = data.filter(function (item) { return item.is_saved; });
          libBooks = savedItems.map(function(item) {
            var original = BOOKS.find(function(b) { return b.id == item.id; });
            if (original) return original;
            return {
              id: item.id,
              title: item.title,
              genre: item.genre,
              author: item.author,
              color: item.color || '#7b5fb8',
              tags: item.tags || [],
              archived: false,
              deadlineDays: 10,
              comments: [],
              rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 }
            };
          });
          renderLib();
        }
      } catch (err) {
        console.error('서재 데이터를 불러오는 중 에러 발생:', err);
      }
    }

    function renderLib() {
      document.getElementById('lib-count').textContent = libBooks.length;

      var totalWritings = 0;
      var totalChats = 0;
      var myName = (typeof currentUser !== 'undefined' && currentUser && currentUser.name) ? currentUser.name : '익명독자';

      myLibraryData.forEach(function (dataItem) {
        var writingsCount = (dataItem.writings || []).length;
        totalWritings += writingsCount;
        totalChats += writingsCount;
      });

      var wEl = document.getElementById('lib-writings-count');
      if (wEl) wEl.textContent = totalWritings;

      var cEl = document.getElementById('lib-chat-count');
      if (cEl) cEl.textContent = totalChats;

      var row = document.getElementById('books-row');
      if (libBooks.length === 0) {
        row.innerHTML = '<div style="font-size:13px;color:var(--text-faint);padding:20px 0;">\'내 서재에 담기\'로 책을 모아보세요.</div>';
      } else {
        row.innerHTML = '';
        var heights = [90, 110, 100, 85, 105, 95, 115, 88];
        libBooks.forEach(function (b, i) {
          var h = heights[i % heights.length];
          var el = document.createElement('div');
          el.className = 'book-spine';
          el.id = 'lb-' + b.id;
          el.style.cssText = 'height:' + h + 'px;background:' + b.color + ';';
          el.innerHTML = '<div class="book-spine-txt">' + b.title + '</div>';
          el.onclick = function () { pickLibBook(b.id, 'lb'); };
          row.appendChild(el);
        });
      }

      // Populate My Comments Shelf
      var myCommentedBooks = [];
      myLibraryData.forEach(function (dataItem) {
        if ((dataItem.writings || []).length > 0) {
          var original = BOOKS.find(function(b) { return b.id == dataItem.id; });
          if (original) {
            myCommentedBooks.push(original);
          }
        }
      });

      var myRow = document.getElementById('my-comments-books-row');
      if (myCommentedBooks.length === 0) {
        myRow.innerHTML = '<div style="font-size:13px;color:var(--text-faint);padding:20px 0;">아직 남긴 감상이나 댓글이 없어요.</div>';
      } else {
        myRow.innerHTML = '';
        var heights = [90, 110, 100, 85, 105, 95, 115, 88];
        myCommentedBooks.forEach(function (b, i) {
          var h = heights[i % heights.length];
          var el = document.createElement('div');
          el.className = 'book-spine';
          el.id = 'mycmt-' + b.id;
          el.style.cssText = 'height:' + h + 'px;background:' + b.color + ';';
          el.innerHTML = '<div class="book-spine-txt">' + b.title + '</div>';
          el.onclick = function () { pickLibBook(b.id, 'mycmt'); };
          myRow.appendChild(el);
        });
      }

      if (selLibBook && !document.getElementById((selLibPrefix || 'lb') + '-' + selLibBook)) {
        document.getElementById('lib-bdp').style.display = 'none';
        selLibBook = null;
      }
    }

    var selLibPrefix = 'lb';

    function pickLibBook(id, prefix) {
      prefix = prefix || 'lb';
      var book = libBooks.find(function (b) { return b.id === id; });
      if (!book) book = BOOKS.find(function (b) { return b.id === id; });
      if (!book) return;

      document.querySelectorAll('.book-spine').forEach(function (e) { e.classList.remove('sel'); });
      var el = document.getElementById(prefix + '-' + id);

      if (selLibBook === id && selLibPrefix === prefix) {
        selLibBook = null;
        document.getElementById('lib-bdp').style.display = 'none';
        return;
      }
      selLibBook = id;
      selLibPrefix = prefix;
      if (el) el.classList.add('sel');

      // 내가 쓴 채팅 메시지
      var myData = myLibraryData.find(function(d) { return d.id === book.id; });
      var myChatMsgs = myData ? (myData.writings || []) : [];

      var writingsEl = document.getElementById('lib-bdp-writings');
      writingsEl.innerHTML = '';

      if (myChatMsgs.length === 0) {
        writingsEl.innerHTML = '<div class="bdp-empty">아직 남긴 글이 없어요. 채팅으로 이야기를 나눠보세요.</div>';
      } else {
        myChatMsgs.forEach(function (m) {
          var item = document.createElement('div');
          item.className = 'bdp-writing-item';
          item.innerHTML =
            '<div class="bdp-writing-type type-chat">💬 채팅 메시지</div>' +
            '<div class="bdp-writing-txt">' + escHtml(m.text) + (m.edited ? '<span class="edited-tag">(수정됨)</span>' : '') + '</div>' +
            '<div class="bdp-writing-date">' + (m.date || m.ts || '') + '</div>';
          writingsEl.appendChild(item);
        });
      }

      document.getElementById('lib-bdp-qdate').textContent = '';
      document.getElementById('lib-bdp-cover').style.background = book.color;
      document.getElementById('lib-bdp-cover').textContent = book.title;
      document.getElementById('lib-bdp-title').textContent = book.title;
      document.getElementById('lib-bdp-sub').textContent = book.genre + ' · AI 생성 가상 도서';
      var tagsEl = document.getElementById('lib-bdp-tags');
      tagsEl.innerHTML = '';
      book.tags.forEach(function (t) {
        var span = document.createElement('span');
        span.className = 'bdp-tag';
        span.textContent = t;
        tagsEl.appendChild(span);
      });
      document.getElementById('lib-bdp').style.display = 'block';
    }

    async function generateBook() {
      // 1. 로그인 여부 검증 (로그인한 사용자만 새 책 생성 가능)
      var token = localStorage.getItem('token');
      if (!token) {
        alert('새 책을 소환하려면 먼저 로그인해 주세요! 📖');
        goPage('auth-gate');
        return;
      }

      var btn = document.getElementById('gen-btn');
      if (btn) btn.disabled = true;
      document.getElementById('loading').style.display = 'flex';
      try {
        var headers = {};
        if (token) headers['Authorization'] = 'Bearer ' + token;
        var res = await fetch('/api/books/candidates', {
          method: 'POST',
          headers: headers
        });
        if (res.ok) {
          var candidates = await res.json();
          renderCandidates(candidates);
          goPage('candidates');
        } else {
          var errData = await res.json();
          alert(errData.detail || '새 책 후보 생성 도중 백엔드 오류가 발생했습니다.');
        }
      } catch (err) {
        console.error(err);
        alert('서버와 통신 도중 에러가 발생했습니다.');
      } finally {
        if (btn) btn.disabled = false;
        document.getElementById('loading').style.display = 'none';
      }
    }
    window.generateBook = generateBook;
    function renderCandidates(candidates) {
      var container = document.getElementById('candidates-container');
      if (!container) return;
      container.innerHTML = '';
      candidates.forEach(function(c) {
        var card = document.createElement('div');
        card.className = 'candidate-card';
        card.innerHTML = 
          '<div class="card-cover" style="background:' + (c.color || '#333') + '">' + c.title + '</div>' +
          '<div class="card-body">' +
            '<span class="card-genre">' + c.genre + '</span>' +
            '<div class="card-title">' + c.title + '</div>' +
            '<div class="card-author">' + c.author + '</div>' +
            '<div class="card-synopsis">' + c.synopsis + '</div>' +
            '<div style="margin-top:auto"><button class="btn-adopt" onclick="adoptCandidate(' + c.id + ')">이 책으로 독서방 열기</button></div>' +
          '</div>';
        container.appendChild(card);
      });
    }
    async function adoptCandidate(candidateId) {
      var token = localStorage.getItem('token');
      if (!token) {
        showToast('로그인이 필요한 서비스입니다. 로그인 페이지로 이동합니다.');
        setTimeout(function() {
          goPage('auth-gate');
        }, 1000);
        return;
      }
      document.getElementById('loading').style.display = 'flex';
      var headers = { 'Authorization': 'Bearer ' + token };
      try {
        var res = await fetch('/api/books/adopt/' + candidateId, {
          method: 'POST',
          headers: headers
        });
        if (res.ok) {
          var newDbBook = await res.json();
          var newAdapted = adaptDbBookToFrontend(newDbBook);
          BOOKS.unshift(newAdapted);
          showToast('✦ 새 책 "' + newAdapted.title + '" 소환 성공! 📚');
          renderHome();
          openDetail(newAdapted.id);
        } else {
          var errData = await res.json();
          alert(errData.detail || '채택 도중 오류가 발생했습니다.');
        }
      } catch (err) {
        console.error(err);
        alert('서버와 통신 중 에러가 발생했습니다.');
      } finally {
        document.getElementById('loading').style.display = 'none';
      }
    }
    window.adoptCandidate = adoptCandidate;

    /* ── CHAT ROOM ── */
    var chatMsgs = {};      // bookId → [{id,mine,user,av,avBg,avColor,text,ts,reactions,replyTo}]
    var rxTargetMsgId = null;
    var rxTargetBookId = null;
    var replyTarget = null; // {msgId, bookId, user, text}

    var CHAT_SEED = [
      { user: '달빛독자', av: '달', avBg: '#e8daf8', avColor: '#7b5fb8', text: '저 이거 읽으면서 지하철에서 울 뻔 했어요 😭 참느라 혼났잖아요' },
      { user: '책상물림', av: '책', avBg: '#f0e8dc', avColor: '#8b4f25', text: '첫 장 넘기자마자 완전히 빠져들었어요. 며칠째 손에서 못 놓고 있음' },
      { user: '밤의활자', av: '밤', avBg: '#e8f0f8', avColor: '#2c5f8a', text: '결말 어떻게 해석하셨어요? 저는 열린 결말이라고 읽었는데 주변 반응이 다 달라서요' },
      { user: '녹색독자', av: '녹', avBg: '#e8f0dc', avColor: '#2d7a50', text: '작가가 이 책에서 하려는 말이 뭔지 읽고 나서도 계속 생각하게 돼요' },
      { user: '봄의문장', av: '봄', avBg: '#f0f8dc', avColor: '#3a6a20', text: '마지막 문장이 아직도 머릿속에 맴돌아요. 이런 책은 진짜 오래 남더라고' },
    ];

    function dateLabel(d) {
      // 어제, 오늘 텍스트 대신 항상 정확한 날짜 표시
      return d.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' });
    }
    function dateKey(d) { // YYYY-MM-DD string for grouping
      return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    }
    function fmtTs(d) {
      var h = d.getHours(), m = d.getMinutes();
      return (h < 12 ? '오전 ' : '오후 ') + (h % 12 || 12) + ':' + (m < 10 ? '0' + m : m);
    }
    function tsNow() { return fmtTs(new Date()); }

    function makeMsg(opts) {
      // opts: {mine, user, av, avBg, avColor, text, date, replyTo}
      // date: Date object
      var computedUserId = opts.userId || (opts.mine ? (typeof CURRENT_USER_ID !== 'undefined' ? CURRENT_USER_ID : 'ME') : opts.user);
      return {
        id: 'msg' + Date.now() + Math.random(),
        userId: computedUserId,   // ← DB에서 user_id 역할
        mine: opts.mine || false,
        user: opts.user, av: opts.av,
        avBg: opts.avBg, avColor: opts.avColor,
        text: opts.text,
        date: opts.date,                          // ← DB에서 created_at 역할
        ts: fmtTs(opts.date),
        reactions: {},
        replyTo: opts.replyTo || null             // ← {user, text} 답장 대상
      };
    }

    function initChatMsgs(bookId) {
      if (chatMsgs[bookId]) return;
      // 빈 배열로 초기화 — 실제 메시지는 DB에서 fetch하여 채운다
      chatMsgs[bookId] = [];
    }

    function handleAuthError(status) {
      if (status === 401 || status === 403) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (typeof currentUser !== 'undefined') currentUser = null;
        showToast('로그인 세션이 만료되었습니다. 다시 로그인해주세요.');
        setTimeout(function() {
          goPage('home');
        }, 1200);
        return true;
      }
      return false;
    }

    async function openChat() {
      if (!currentBook) return;
      initChatMsgs(currentBook.id);
      var book = currentBook;

      var _chatToken = localStorage.getItem('token');
      // 채팅 읽기는 인증 불필요 — 로그인 여부와 관계없이 항상 DB에서 채팅 내역 로드
      try {
        var fetchHeaders = {};
        if (_chatToken) fetchHeaders['Authorization'] = 'Bearer ' + _chatToken;
        var res = await fetch('/api/books/' + book.id + '/chats', { headers: fetchHeaders });
        if (res.ok) {
          var dbChats = await res.json();
          // DB 데이터로 완전 교체 (기존 캐시/시드 메시지 제거)
          chatMsgs[book.id] = [];
          dbChats.forEach(function (c) {
            chatMsgs[book.id].push({
              id: c.id,
              userId: c.userId,
              mine: (typeof CURRENT_USER_ID !== 'undefined' && CURRENT_USER_ID !== null && c.userId == CURRENT_USER_ID),
              user: c.user,
              av: c.user.charAt(0),
              avBg: '#f5d87a',
              avColor: '#7a4a10',
              text: c.text,
              date: new Date(c.date),
              ts: c.ts,
              reactions: (function(rx) {
                var mapped = {};
                for (var k in rx) {
                  mapped[k] = { count: rx[k], mine: false };
                }
                return mapped;
              })(c.reactions || {}),
              replyTo: c.replyTo || null,
              edited: c.edited || false
            });
          });
          chatMsgs[book.id].sort(function (a, b) { return a.date.getTime() - b.date.getTime(); });
        }
      } catch (e) { console.error(e); }

      document.getElementById('chat-room-title').textContent = book.title + ' 독서방';
      // 백엔드에서 정확하게 집계된 participant_count(book.count)를 신뢰할 수 있는 출처로 사용
      document.getElementById('chat-room-meta').textContent = book.count + '명 참여 중';
      var hb = document.getElementById('chat-header-book');
      hb.style.background = book.color;
      hb.textContent = book.title;
      // ── 📌 토론 주제 배너 채우기 ──
      var banner = document.getElementById('chat-topic-banner');
      var dilemmaEl = document.getElementById('chat-topic-dilemma');
      var openingEl = document.getElementById('chat-topic-opening');
      var quoteEl = document.getElementById('chat-topic-quote');
      var questionsEl = document.getElementById('chat-topic-questions');
      var topicBody = document.getElementById('chat-topic-body');
      var toggleBtn = document.getElementById('chat-topic-toggle');
      if (banner) {
        if (book.coreDilemma || book.additionalQuestions || book.openingLine || book.memorableQuote) {
          var secOpening = document.getElementById('chat-topic-sec-opening');
          var secQuote = document.getElementById('chat-topic-sec-quote');
          var secDilemma = document.getElementById('chat-topic-sec-dilemma');
          if (secOpening) {
            if (book.openingLine) {
              if (openingEl) openingEl.textContent = '"' + book.openingLine + '"';
              secOpening.style.display = '';
            } else {
              secOpening.style.display = 'none';
            }
          }
          if (secQuote) {
            if (book.memorableQuote) {
              if (quoteEl) quoteEl.textContent = '"' + book.memorableQuote + '"';
              secQuote.style.display = '';
            } else {
              secQuote.style.display = 'none';
            }
          }
          if (secDilemma) {
            if (book.coreDilemma) {
              if (dilemmaEl) dilemmaEl.textContent = book.coreDilemma;
              secDilemma.style.display = '';
            } else {
              secDilemma.style.display = 'none';
            }
          }
          if (questionsEl) {
            questionsEl.innerHTML = '';
            if (book.additionalQuestions) {
              var qs = book.additionalQuestions.split('|').map(function(q){ return q.trim(); }).filter(Boolean).slice(0, 2);
              if (qs.length > 0) {
                questionsEl.style.display = '';
                qs.forEach(function(q) {
                  var item = document.createElement('div');
                  item.className = 'chat-topic-q-item';
                  item.textContent = q.replace(/^Q\.\s*/, '');
                  questionsEl.appendChild(item);
                });
              } else {
                questionsEl.style.display = 'none';
              }
            } else {
              questionsEl.style.display = 'none';
            }
          }
          if (topicBody) topicBody.classList.remove('hidden');
          if (toggleBtn) { toggleBtn.classList.remove('collapsed'); toggleBtn.textContent = '▲'; }
          banner.style.display = '';
        } else {
          banner.style.display = 'none';
        }
      }
      renderChat(book.id);
      goPage('chat');
      setTimeout(function () {
        var body = document.getElementById('chat-body');
        body.scrollTop = body.scrollHeight;
      }, 80);
    }
    function toggleTopicBanner() {
      var body = document.getElementById('chat-topic-body');
      var btn = document.getElementById('chat-topic-toggle');
      if (!body) return;
      if (body.classList.contains('hidden')) {
        body.classList.remove('hidden');
        btn.classList.remove('collapsed');
        btn.textContent = '▲';
      } else {
        body.classList.add('hidden');
        btn.classList.add('collapsed');
        btn.textContent = '▼';
      }
    }

    function renderChat(bookId) {
      var body = document.getElementById('chat-body');
      var msgs = chatMsgs[bookId] || [];

      // mine 여부는 DB의 user_id와 현재 로그인 유저를 비교해 런타임에 판단
      // → DB에 mine 컬럼은 없음. 렌더 시점에 결정됨
      // DB에서 온 데이터는 userId가 숫자이므로 느슈한 비교(==) 사용
      msgs.forEach(function (m) { m.mine = (m.userId == CURRENT_USER_ID); });

      body.innerHTML = '';

      // 입장 공지는 맨 처음 한 번
      body.appendChild(makeDivider('독서방 개설일'));
      body.appendChild(makeNotice('📚 독서방이 열렸습니다.'));

      var lastDateKey = null;
      msgs.forEach(function (msg) {
        var dk = dateKey(msg.date);
        if (dk !== lastDateKey) {
          // 날짜 바뀔 때마다 구분선 삽입
          body.appendChild(makeDateDivider(msg.date));
          lastDateKey = dk;
        }
        body.appendChild(buildMsgEl(msg, bookId));
      });

      // 오늘 날짜 구분선이 아직 없으면 추가 (메시지 없어도)
      var todayKey = dateKey(new Date());
      if (lastDateKey !== todayKey) {
        body.appendChild(makeDateDivider(new Date()));
        body.appendChild(makeNotice('💬 나 외 ' + Math.max(0, currentBook.count - 1) + '명이 이야기 중이에요.'));
      }
    }

    function makeDivider(label) {
      var d = document.createElement('div');
      d.className = 'chat-notice';
      d.style.marginTop = '10px';
      d.innerHTML = '<span style="background:rgba(0,0,0,0.12)">' + label + '</span>';
      return d;
    }
    function makeNotice(text) {
      var d = document.createElement('div');
      d.className = 'chat-notice';
      d.innerHTML = '<span>' + text + '</span>';
      return d;
    }
    function makeDateDivider(date) {
      var d = document.createElement('div');
      d.className = 'chat-date-divider';
      d.innerHTML = '<span>' + dateLabel(date) + '</span>';
      return d;
    }

    function buildMsgEl(msg, bookId) {
      var row = document.createElement('div');
      var isMod = (msg.user && (msg.user.indexOf('AI 사회자') !== -1 || msg.user.indexOf('사회자') !== -1));
      var rowClass = 'chat-row ';
      if (msg.mine) {
        rowClass += 'mine';
      } else if (isMod) {
        rowClass += 'other moderator-row';
      } else {
        rowClass += 'other';
      }
      row.className = rowClass;
      row.id = 'chatrow-' + msg.id;
      row.style.position = 'relative';

      var rxParts = rxHtml_parts(msg, bookId);
      var rxBlock = rxParts ? '<div class="chat-reactions"' + (msg.mine ? ' style="justify-content:flex-end"' : '') + '>' + rxParts + '</div>' : '';
      var editedTag = msg.edited ? '<span class="edited-tag">(수정됨)</span>' : '';

      // reply quote block
      var replyQuote = '';
      if (msg.replyTo) {
        replyQuote = '<div class="chat-reply-quote">' +
          '<div class="chat-reply-quote-name">↩ ' + escHtml(msg.replyTo.user) + '</div>' +
          '<div class="chat-reply-quote-text">' + escHtml(msg.replyTo.text.slice(0, 60) + (msg.replyTo.text.length > 60 ? '…' : '')) + '</div>' +
          '</div>';
      }

      // bubble inner — in edit mode this will be swapped
      var bubbleHtml = '<div class="chat-bubble" id="bubble-' + msg.id + '"' + (msg.mine ? ' ondblclick="showMsgMenu(\'' + bookId + '\',\'' + msg.id + '\',event)"' : ' ondblclick="showRxPicker(\'' + bookId + '\',\'' + msg.id + '\',event)"') + '>' +
        replyQuote +
        escHtml(msg.text) + editedTag +
        '</div>';

      var actionToolbar = '';
      if (msg.mine) {
        actionToolbar = '<div class="chat-action-toolbar mine">' +
          '<button class="chat-action-btn" onclick="startEdit(\'' + bookId + '\',\'' + msg.id + '\')">수정</button>' +
          '<span class="chat-action-divider">|</span>' +
          '<button class="chat-action-btn danger" onclick="deleteMsg(\'' + bookId + '\',\'' + msg.id + '\')">삭제</button>' +
          '</div>';
      } else {
        actionToolbar = '<div class="chat-action-toolbar other">' +
          '<button class="chat-action-btn" onclick="startReplyById(\'' + bookId + '\',\'' + msg.id + '\')">↩ 답장</button>' +
          '<span class="chat-action-divider">|</span>' +
          '<button class="chat-action-btn" onclick="showRxPicker(\'' + bookId + '\',\'' + msg.id + '\',event)">❤️ 반응</button>' +
          '</div>';
      }
      if (msg.mine) {
        row.innerHTML =
          '<div class="chat-time-wrap"><span class="chat-time">' + msg.ts + '</span></div>' +
          '<div class="chat-col" id="col-' + msg.id + '">' +
          bubbleHtml +
          actionToolbar +
          rxBlock +
          '</div>';
      } else {
        var avHtml = '';
        if (isMod) {
          avHtml = '<div class="chat-av mod-av">🎙️</div>';
        } else {
          avHtml = '<div class="chat-av" style="background:' + msg.avBg + ';color:' + msg.avColor + '">' + msg.av + '</div>';
        }
        row.innerHTML =
          avHtml +
          '<div class="chat-col" id="col-' + msg.id + '">' +
          '<div class="chat-name' + (isMod ? ' mod-name' : '') + '">' + msg.user + '</div>' +
          bubbleHtml +
          actionToolbar +
          rxBlock +
          '</div>' +
          '<div class="chat-time-wrap"><span class="chat-time">' + msg.ts + '</span></div>';
      }
      return row;
    }

    function escHtml(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function rxHtml_parts(msg, bookId) {
      var rxKeys = Object.keys(msg.reactions);
      if (!rxKeys.length) return '';
      return rxKeys.map(function (emoji) {
        var r = msg.reactions[emoji];
        return '<button class="chat-rx-btn' + (r.mine ? ' on' : '') + '" onclick="toggleChatRx(\'' + bookId + '\',\'' + msg.id + '\',\'' + emoji + '\')">' +
          emoji + '<span class="chat-rx-count">' + r.count + '</span></button>';
      }).join('');
    }

    /* ── 메시지 컨텍스트 메뉴 (내 메시지 더블탭) ── */
    var activeMsgMenu = null;
    function showMsgMenu(bookId, msgId, e) {
      e.stopPropagation();
      closeMsgMenu();

      var row = document.getElementById('chatrow-' + msgId);
      if (!row) return;

      var menu = document.createElement('div');
      menu.className = 'msg-menu show';
      menu.id = 'msgmenu-' + msgId;
      menu.style.cssText = 'position:absolute;right:0;top:-48px;';
      menu.innerHTML =
        '<div class="msg-menu-item" onclick="startEdit(\'' + bookId + '\',\'' + msgId + '\')">✏️ 수정</div>' +
        '<div class="msg-menu-item danger" onclick="deleteMsg(\'' + bookId + '\',\'' + msgId + '\')">🗑 삭제</div>';

      var col = document.getElementById('col-' + msgId);
      if (col) { col.style.position = 'relative'; col.appendChild(menu); }
      activeMsgMenu = menu;

      setTimeout(function () {
        document.addEventListener('click', closeMsgMenu, { once: true });
      }, 10);
    }
    function closeMsgMenu() {
      if (activeMsgMenu) { activeMsgMenu.remove(); activeMsgMenu = null; }
    }

    /* ── 수정 모드 ── */
    function startEdit(bookId, msgId) {
      closeMsgMenu();
      var msgs = chatMsgs[bookId];
      var msg = msgs && msgs.find(function (m) { return m.id == msgId; });
      if (!msg) return;

      var bubble = document.getElementById('bubble-' + msgId);
      var col = document.getElementById('col-' + msgId);
      if (!bubble || !col) return;

      // bubble → edit textarea
      bubble.style.display = 'none';

      var wrap = document.createElement('div');
      wrap.className = 'chat-edit-wrap';
      wrap.id = 'editwrap-' + msgId;
      wrap.innerHTML =
        '<textarea class="chat-edit-ta" id="edita-' + msgId + '" rows="2">' + escHtml(msg.text) + '</textarea>' +
        '<div class="chat-edit-btns">' +
        '<button class="chat-edit-cancel" onclick="cancelEdit(\'' + msgId + '\')">취소</button>' +
        '<button class="chat-edit-save" onclick="saveEdit(\'' + bookId + '\',\'' + msgId + '\')">저장</button>' +
        '</div>';

      col.insertBefore(wrap, bubble.nextSibling);

      var ta = document.getElementById('edita-' + msgId);
      if (ta) { ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length); }
    }

    function cancelEdit(msgId) {
      var wrap = document.getElementById('editwrap-' + msgId);
      if (wrap) wrap.remove();
      var bubble = document.getElementById('bubble-' + msgId);
      if (bubble) bubble.style.display = '';
    }

    function saveEdit(bookId, msgId) {
      var ta = document.getElementById('edita-' + msgId);
      if (!ta) return;
      var newText = ta.value.trim();
      if (!newText) { showToast('내용을 입력해주세요.'); return; }

      var msgs = chatMsgs[bookId];
      var msg = msgs && msgs.find(function (m) { return m.id == msgId; });
      if (!msg) return;
      var originalText = msg.text;
      var originalEdited = msg.edited;
      msg.text = newText;
      msg.edited = true;  // ← DB에서는 updated_at 컬럼으로 관리
      // 해당 row만 교체
      var old = document.getElementById('chatrow-' + msgId);
      if (old) {
        var fresh = buildMsgEl(msg, bookId);
        old.parentNode.replaceChild(fresh, old);
      }
      showToast('수정되었어요.');
      function rollbackEdit() {
        msg.text = originalText;
        msg.edited = originalEdited;
        var currentEl = document.getElementById('chatrow-' + msgId);
        if (currentEl) {
          var restored = buildMsgEl(msg, bookId);
          currentEl.parentNode.replaceChild(restored, currentEl);
        }
      }
      // DB 수정 저장 (msg.id가 실제 DB 숫자 ID인 경우만)
      var token = localStorage.getItem('token');
      var hasRealId = msg.id && (typeof msg.id === 'number' || (!isNaN(Number(msg.id)) && !String(msg.id).startsWith('msg')));
      if (token && hasRealId) {
        fetch('/api/chats/' + msg.id, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({ text: newText })
        }).then(function(r) {
          if (!r.ok) {
            console.error('채팅 수정 실패:', r.status);
            rollbackEdit();
            var wasAuthErr = handleAuthError(r.status);
            if (!wasAuthErr) showToast('대화 수정에 실패했습니다.');
          } else {
            console.log('채팅 DB 수정 성공:', msg.id);
          }
        }).catch(function(err) {
          console.error('채팅 수정 API 에러:', err);
          rollbackEdit();
          showToast('네트워크 오류로 대화 수정에 실패했습니다.');
        });
      }

    }

    function deleteMsg(bookId, msgId) {
      closeMsgMenu();
      var msgs = chatMsgs[bookId];
      if (!msgs) return;
      var idx = msgs.findIndex(function (m) { return m.id == msgId; });
      if (idx === -1) return;
      var msg = msgs[idx];
      // UI에서 먼저 제거 (빠른 응답성)
      msgs.splice(idx, 1);
      var row = document.getElementById('chatrow-' + msgId);
      if (row) row.remove();
      showToast('삭제됐어요.');
      function rollbackDelete() {
        if (idx !== -1 && msgs.indexOf(msg) === -1) {
          msgs.splice(idx, 0, msg);
        }
        renderChat(bookId);
      }
      // DB 실제 삭제 (msg.id가 DB의 숫자 ID인 경우만)
      var token = localStorage.getItem('token');
      var hasRealId = msg && msg.id && (typeof msg.id === 'number' || (!isNaN(Number(msg.id)) && !String(msg.id).startsWith('msg')));
      if (token && hasRealId) {
        fetch('/api/chats/' + msg.id, {
          method: 'DELETE',
          headers: { 'Authorization': 'Bearer ' + token }
        }).then(function(r) {
          if (!r.ok) {
            console.error('채팅 삭제 실패:', r.status);
            rollbackDelete();
            var wasAuthErr = handleAuthError(r.status);
            if (!wasAuthErr) showToast('대화 삭제에 실패했습니다.');
          } else {
            console.log('채팅 DB 삭제 성공:', msg.id);
          }
        }).catch(function(err) {
          console.error('채팅 삭제 API 에러:', err);
          rollbackDelete();
          showToast('네트워크 오류로 대화 삭제에 실패했습니다.');
        });
      }
    }

    function sendChatMsg() {
      if (!currentBook) return;
      var inp = document.getElementById('chat-input');
      var text = inp.value.trim();
      if (!text) return;

      var now = new Date();
      var msgs = chatMsgs[currentBook.id];

      // 날짜 구분선: 마지막 메시지와 날짜가 다르면 구분선 먼저 삽입
      var body = document.getElementById('chat-body');
      var lastMsg = msgs.length > 0 ? msgs[msgs.length - 1] : null;
      if (!lastMsg || dateKey(lastMsg.date) !== dateKey(now)) {
        body.appendChild(makeDateDivider(now));
      }

      var myName = (typeof currentUser !== 'undefined' && currentUser && currentUser.name) ? currentUser.name : '나';
      var myAv = myName.charAt(0);

      var msg = makeMsg({
        mine: true, userId: CURRENT_USER_ID,
        user: myName, av: myAv, avBg: '#f5d87a', avColor: '#7a4a10',
        text: text, date: now,
        replyTo: replyTarget ? { user: replyTarget.user, text: replyTarget.text } : null
      });
      msgs.push(msg);
      inp.value = ''; inp.style.height = 'auto';
      cancelReply(); // 답장 상태 초기화
      var cntEl = document.getElementById('chat-char-count-display');
      if (cntEl) {
        cntEl.textContent = '0';
        cntEl.parentElement.classList.remove('warning');
      }
      body.appendChild(buildMsgEl(msg, currentBook.id));
      body.scrollTop = body.scrollHeight;

      // Update library counts globally
      if (typeof renderLib === 'function') renderLib();

      // Backend 저장 (isLoggedIn 스코프 문제 방지: 토큰 체크)
      var token = localStorage.getItem('token');
      if (token) {
        var oldId = msg.id;
        fetch('/api/books/' + currentBook.id + '/chats', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({
            text: text,
            reply_to_id: replyTarget ? replyTarget.msgId : null
          })
        }).then(async function (r) {
          if (r.ok) {
            var data = await r.json();
            if (data && data.id) {
              msg.id = data.id;
              var oldRow = document.getElementById('chatrow-' + oldId);
              if (oldRow) {
                var freshRow = buildMsgEl(msg, currentBook.id);
                oldRow.parentNode.replaceChild(freshRow, oldRow);
              }
            }
          } else {
            console.error('채팅 전송 실패:', r.status);
            var wasAuthErr = handleAuthError(r.status);
            if (!wasAuthErr) showToast('대화 전송에 실패했습니다.');
            var oldRow = document.getElementById('chatrow-' + oldId);
            if (oldRow) oldRow.remove();
            var idx = msgs.indexOf(msg);
            if (idx !== -1) msgs.splice(idx, 1);
          }
        }).catch(function (e) {
          console.error('채팅 전송 API 에러:', e);
          showToast('네트워크 오류로 대화 전송에 실패했습니다.');
          var oldRow = document.getElementById('chatrow-' + oldId);
          if (oldRow) oldRow.remove();
          var idx = msgs.indexOf(msg);
          if (idx !== -1) msgs.splice(idx, 1);
        });
      }
    }

    function showRxPicker(bookId, msgId, e) {
      e.stopPropagation();
      rxTargetMsgId = msgId;
      rxTargetBookId = bookId;
      var picker = document.getElementById('rx-picker');
      picker.classList.add('show');
      setTimeout(function () {
        document.addEventListener('click', hideRxPicker, { once: true });
      }, 10);
    }
    function hideRxPicker() {
      document.getElementById('rx-picker').classList.remove('show');
    }
    function pickRx(emoji, label) {
      if (!rxTargetMsgId || !rxTargetBookId) return;
      toggleChatRx(rxTargetBookId, rxTargetMsgId, emoji);
      hideRxPicker();
    }

    /* ── 답장하기 ── */
    function pickReply() {
      hideRxPicker();
      if (!rxTargetMsgId || !rxTargetBookId) return;
      var msgs = chatMsgs[rxTargetBookId];
      if (!msgs) return;
      var msg = msgs.find(function (m) { return m.id == rxTargetMsgId; });
      if (!msg) return;
      startReply(msg);
    }
    function startReplyById(bookId, msgId) {
      var msgs = chatMsgs[bookId];
      if (!msgs) return;
      var msg = msgs.find(function (m) { return m.id == msgId; });
      if (msg) startReply(msg);
    }
    function startReply(msg) {
      replyTarget = { msgId: msg.id, user: msg.user, text: msg.text };
      var bar = document.getElementById('reply-preview-bar');
      document.getElementById('reply-preview-name').textContent = '↩ ' + msg.user + '님에게 답장 쓰는 중';
      document.getElementById('reply-preview-text').textContent = msg.text;
      bar.classList.add('show');

      // 입력창 포커스 및 placeholder 변경
      var inp = document.getElementById('chat-input');
      if (inp) {
        inp.placeholder = msg.user + '님에게 답글을 남겨보세요...';
        inp.focus();
      }

    }
    function cancelReply() {
      replyTarget = null;
      var bar = document.getElementById('reply-preview-bar');
      if (bar) bar.classList.remove('show');

      // placeholder 복원
      var inp = document.getElementById('chat-input');
      if (inp) {
        inp.placeholder = '이 책에 대해 이야기해보세요...';
      }
    }
    function toggleChatRx(bookId, msgId, emoji) {
      var msgs = chatMsgs[bookId];
      if (!msgs) return;
      var msg = msgs.find(function (m) { return m.id == msgId; });
      if (!msg) return;
      if (msg.mine) {
        showToast('내가 쓴 댓글에는 반응을 달 수 없어요.');
        return;
      }
      if (!msg.reactions[emoji]) msg.reactions[emoji] = { count: 0, mine: false };
      var r = msg.reactions[emoji];
      if (r.mine) { r.mine = false; r.count = Math.max(0, r.count - 1); }
      else { r.mine = true; r.count++; }
      if (r.count === 0) delete msg.reactions[emoji];
      // re-render just this row
      var old = document.getElementById('chatrow-' + msgId);
      if (old) { var fresh = buildMsgEl(msg, bookId); old.parentNode.replaceChild(fresh, old); }
    }
    var searchMatches = [];
    var searchCursor = -1;
    function toggleChatSearch() {
      var bar = document.getElementById('chat-search-bar');
      var toggle = document.getElementById('chat-search-toggle');
      if (bar.classList.contains('open')) {
        closeChatSearch();
      } else {
        bar.classList.add('open');
        toggle.classList.add('active');
        setTimeout(function() { document.getElementById('chat-search-input').focus(); }, 250);
      }
    }
    function closeChatSearch() {
      clearSearchHighlights();
      var bar = document.getElementById('chat-search-bar');
      if (bar) bar.classList.remove('open');
      var toggle = document.getElementById('chat-search-toggle');
      if (toggle) toggle.classList.remove('active');
      var inp = document.getElementById('chat-search-input');
      if (inp) inp.value = '';
      var count = document.getElementById('chat-search-count');
      if (count) count.textContent = '';
      var prev = document.getElementById('chat-search-prev');
      if (prev) prev.disabled = true;
      var next = document.getElementById('chat-search-next');
      if (next) next.disabled = true;
    }
    function clearSearchHighlights() {
      searchMatches.forEach(function(m) {
        if (m.bubbleEl) m.bubbleEl.innerHTML = m.originalHtml;
        if (m.rowEl) m.rowEl.classList.remove('search-dim');
      });
      document.querySelectorAll('.chat-row').forEach(function(r) { r.classList.remove('search-dim'); });
      searchMatches = [];
      searchCursor = -1;
    }
    function onChatSearch(q) {
      clearSearchHighlights();
      var count = document.getElementById('chat-search-count');
      var prev = document.getElementById('chat-search-prev');
      var next = document.getElementById('chat-search-next');
      q = q.trim();
      if (!q) { if (count) count.textContent = ''; if (prev) prev.disabled = true; if (next) next.disabled = true; return; }
      var allRows = document.querySelectorAll('#chat-body .chat-row');
      var matches = [];
      var re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      allRows.forEach(function(row) {
        var bubble = row.querySelector('.chat-bubble');
        if (!bubble) return;
        var original = bubble.innerHTML;
        if (re.test(bubble.textContent)) {
          re.lastIndex = 0;
          var highlighted = original.replace(re, function(m) { return '<mark class="search-highlight">' + m + '</mark>'; });
          matches.push({ rowEl: row, bubbleEl: bubble, originalHtml: original, highlightedHtml: highlighted });
        }
        re.lastIndex = 0;
      });
      searchMatches = matches;
      allRows.forEach(function(row) {
        if (!matches.some(function(m) { return m.rowEl === row; })) row.classList.add('search-dim');
      });
      matches.forEach(function(m) { m.bubbleEl.innerHTML = m.highlightedHtml; });
      if (matches.length === 0) {
        if (count) count.textContent = '없음';
        if (prev) prev.disabled = true; if (next) next.disabled = true;
      } else {
        searchCursor = 0;
        scrollToMatch(0);
        if (count) count.textContent = '1 / ' + matches.length;
        if (prev) prev.disabled = matches.length <= 1;
        if (next) next.disabled = matches.length <= 1;
      }
    }
    function scrollToMatch(idx) {
      if (!searchMatches.length) return;
      document.querySelectorAll('.search-highlight.current').forEach(function(el) { el.classList.remove('current'); });
      var m = searchMatches[idx];
      m.bubbleEl.querySelectorAll('.search-highlight').forEach(function(mk) { mk.classList.add('current'); });
      m.rowEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    function navSearch(dir) {
      if (!searchMatches.length) return;
      searchCursor = (searchCursor + dir + searchMatches.length) % searchMatches.length;
      scrollToMatch(searchCursor);
      var count = document.getElementById('chat-search-count');
      if (count) count.textContent = (searchCursor + 1) + ' / ' + searchMatches.length;
    }

    function goPage(p) {
      document.querySelectorAll('.page').forEach(function (e) { e.classList.remove('active'); });
      document.querySelectorAll('.nav-btn').forEach(function (e) { e.classList.remove('active'); });
      var globalFooter = document.getElementById('global-footer');
      if (globalFooter) globalFooter.style.display = '';
      if (p === 'home') {
        document.getElementById('pg-home').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'candidates') {
        document.getElementById('pg-candidates').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'detail') {
        document.getElementById('pg-detail').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'chat') {
        document.getElementById('pg-chat').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'lib') {
        if (!localStorage.getItem('token')) {
          document.getElementById('pg-auth-gate').classList.add('active');
          document.getElementById('nb-lib').classList.add('active');
        } else {
          document.getElementById('pg-lib').classList.add('active');
          document.getElementById('nb-lib').classList.add('active');
          // 내 서재 탭 진입 시마다 DB에서 최신 서재 데이터 불러오기
          loadMyLibrary();
        }
      } else if (p === 'auth-gate') {
        document.getElementById('pg-auth-gate').classList.add('active');
        document.getElementById('nb-lib').classList.add('active');
      } else if (p === 'login') {
        clearLoginForm();
        document.getElementById('pg-login').classList.add('active');
        document.getElementById('nb-lib').classList.add('active');
      } else if (p === 'signup') {
        clearSignupForm();
        document.getElementById('pg-signup').classList.add('active');
        document.getElementById('nb-lib').classList.add('active');
      } else if (p === 'guide') {
        // '이용 안내' 버튼 → pg-info(이용 안내 페이지)로 연결
        document.getElementById('pg-info').classList.add('active');
        document.getElementById('nb-guide').classList.add('active');
      } else if (p === 'archive') {
        document.getElementById('pg-archive').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'chat-history') {
        // 종료된 독서방 채팅 기록 열람 페이지 (읽기 전용)
        document.getElementById('pg-chat-history').classList.add('active');
        document.getElementById('nb-home').classList.add('active');
      } else if (p === 'info') {
        document.getElementById('pg-info').classList.add('active');
      } else if (p === 'contact') {
        document.getElementById('pg-contact').classList.add('active');
      } else if (p === 'terms') {
        document.getElementById('pg-terms').classList.add('active');
      } else if (p === 'privacy') {
        document.getElementById('pg-privacy').classList.add('active');
      }
      // ── footer nav 활성 상태 업데이트 ──
      document.querySelectorAll('.home-footer-link').forEach(function(el) { el.classList.remove('active'); });
      var footerMap = { 'info': 'footer-link-info', 'contact': 'footer-link-contact', 'terms': 'footer-link-terms', 'privacy': 'footer-link-privacy' };
      if (footerMap[p]) {
        var activeLink = document.getElementById(footerMap[p]);
        if (activeLink) activeLink.classList.add('active');
      }
      // 채팅 검색창은 채팅 관련 페이지를 벗어날 때 닫기
      if (p !== 'chat' && p !== 'chat-history') { closeChatSearch(); cancelReply(); }
      window.scrollTo(0, 0);
    }

    /* ── ARCHIVE CONTROL ── */
    var currentArcBookId = null;
    async function openArchive(bookId) {
      // 백엔드 API/라우팅 상의 string 타입 ID와 JS 배열 내 number 타입 ID의 불일치를 parseInt 및 유연한 비교(==)로 완벽 차단
      var targetId = parseInt(bookId) || bookId;
      var book = BOOKS.find(function(b) { return b.id == targetId; });
      if (!book) return;
      currentArcBookId = bookId;
      var activePg = document.querySelector('.page.active');
      if (activePg && activePg.id !== 'pg-archive') {
        window.lastPageBeforeArchive = activePg.id.replace('pg-', '');
      }
      goPage('archive');
      window.scrollTo(0, 0);
      // ── 책 표지 색상 기반 CSS 변수 동적 주입 ──
      (function injectArcTheme(hex) {
        var r = parseInt(hex.slice(1,3),16)||0, g = parseInt(hex.slice(3,5),16)||0, b = parseInt(hex.slice(5,7),16)||0;
        function toHex(v){ return ('0'+Math.min(255,Math.max(0,v)).toString(16)).slice(-2); }
        var bgHex = '#'+[Math.round(r*0.16),Math.round(g*0.16),Math.round(b*0.16)].map(toHex).join('');
        var acHex = '#'+[Math.min(255,Math.round(r*0.78+38)),Math.min(255,Math.round(g*0.78+38)),Math.min(255,Math.round(b*0.78+38))].map(toHex).join('');
        var ltHex = '#'+[Math.min(255,Math.round(r*0.48+105)),Math.min(255,Math.round(g*0.48+105)),Math.min(255,Math.round(b*0.48+105))].map(toHex).join('');
        var tintHex = '#'+[Math.min(255,Math.round(r*0.07+232)),Math.min(255,Math.round(g*0.07+232)),Math.min(255,Math.round(b*0.07+232))].map(toHex).join('');
        var dkHex = '#'+[Math.round(r*0.52),Math.round(g*0.52),Math.round(b*0.52)].map(toHex).join('');
        var acR=parseInt(acHex.slice(1,3),16), acG=parseInt(acHex.slice(3,5),16), acB=parseInt(acHex.slice(5,7),16);
        var el = document.getElementById('pg-archive');
        if (el) {
          el.style.setProperty('--arc-bg', bgHex);
          el.style.setProperty('--arc-accent', acHex);
          el.style.setProperty('--arc-light', ltHex);
          el.style.setProperty('--arc-tint', tintHex);
          el.style.setProperty('--arc-glow', 'rgba('+acR+','+acG+','+acB+',0.28)');
          el.style.setProperty('--arc-book-gradient', 'linear-gradient(135deg,'+acHex+' 0%,'+dkHex+' 100%)');
        }
      })(book.color || '#1a2e14');
      var arcContent = document.querySelector('#pg-archive .arc-content');
      if (arcContent) {
        arcContent.innerHTML = '<div style="padding: 100px 20px; text-align: center; color: var(--text-faint); font-family: \'Noto Serif KR\', serif; font-size: 16px; letter-spacing: 0.05em; line-height: 2;">아카이브 책장을 넘기는 중... ✦</div>';
      }

      // 실시간 데이터베이스(API)로부터 책 상세, 평점 통계, 댓글 및 채팅 리스트 로드
      var comments = [];
      var chats = [];
      var ratingsSummary = { avg_score: 4.6, total_count: 30, distribution: {5: 16, 4: 10, 3: 4, 2: 0, 1: 0} };

      if (window.location.protocol !== 'file:') {
        try {
          var res1 = await fetch('/api/books/' + bookId);
          if (res1.ok) {
            var data1 = await res1.json();
            if (data1.book) {
              book = adaptDbBookToFrontend(data1.book);
            }
            if (data1.comments) {
              comments = data1.comments.map(function(c) {
                return {
                  id: c.id,
                  user: c.user,
                  content: c.content,
                  created_at: c.created_at,
                  reactions: c.reactions || {}
                };
              });
            }
            if (data1.ratings_summary) {
              ratingsSummary = data1.ratings_summary;
            }
          }
          var res2 = await fetch('/api/books/' + bookId + '/chats');
          if (res2.ok) {
            var dbChats = await res2.json();
            chats = dbChats.map(function(ch) {
              return {
                id: ch.id,
                user: ch.user,
                text: ch.text,
                ts: ch.ts,
                date: ch.date
              };
            });
          }
        } catch (err) {
          console.error("아카이브 상세 정보 로딩 중 에러 발생:", err);
        }
      }

      // 상단 스티키 헤더 정보 동적 갱신
      var miniCover = document.getElementById('arc-page-cover');
      if (miniCover) {
        miniCover.style.background = book.color;
        miniCover.textContent = book.title.slice(0, 4);
      }
      var miniTitle = document.getElementById('arc-page-title');
      if (miniTitle) miniTitle.textContent = book.title;

      // 고유 참여자(닉네임 집합) 추출
      var distinctUsersSet = new Set();
      comments.forEach(function(c) { distinctUsersSet.add(c.user); });
      chats.forEach(function(ch) { distinctUsersSet.add(ch.user); });

      // 만약 참여자가 너무 적을 시, 매거진 레이아웃의 완성도를 위해 기본 가상 닉네임 추가
      var defaultNicks = ["도서관팬", "몽상독자", "구름위에서", "기억수집가", "봄날사서", "다은이좋아", "흰구름독자", "잠못드는밤", "살아있는기억", "책속의책", "조용한페이지", "하늘서고", "반납불가", "기억의무게", "구름너머"];
      defaultNicks.forEach(function(n) {
        if (distinctUsersSet.size < 12) {
          distinctUsersSet.add(n);
        }
      });
      var distinctUsers = Array.from(distinctUsersSet);

      // DB에 댓글이 아예 비어있을 시 가공독서회 전용 고품질 문학 감상평 템플릿 주입
      var combinedComments = comments.slice();
      var defaultTemplates = [
        "처음엔 장르적인 가벼운 호기심으로 읽기 시작했는데, 곱씹을수록 '{title}'에 깃든 인간 정신과 기억의 소중함에 대한 성찰이 정말 깊이 와닿았습니다. 깊은 울림을 주네요.",
        "이 판타지적 설정을 매개로, 작가 '{author}'님은 어쩌면 현대인의 고독과 삶의 유한함을 위로하고 있었던 것 같습니다. 문장이 너무 섬세해서 여러 번 필사하게 만들더군요.",
        "결말을 읽고 오랫동안 마음을 추스렸습니다. 가공의 활자가 만들어내는 깊은 사유와 독서방 회원분들의 예리한 감상이 어우러져, 존재하지 않는 공간을 완벽히 감각하게 해준 놀라운 3일이었습니다.",
        "기억의 보관이라는 테마를 두고, 우리가 실시간 채팅과 감상평을 통해 나눈 사유 자체가 이미 하나의 아름다운 문학적 시도였다는 생각이 듭니다. 영원히 보관하고 싶은 추억입니다.",
        "존재하지 않는 책이 실재하는 책보다 더 크고 선명한 인상을 남길 수 있다는 가공독서회의 정수를 완벽하게 보여준 소설입니다. 참여한 분들의 문장도 다들 너무 훌륭합니다."
      ];

      if (combinedComments.length === 0) {
        for (var i = 0; i < defaultTemplates.length; i++) {
          var user = defaultNicks[i % defaultNicks.length];
          var text = defaultTemplates[i].replace('{title}', book.title).replace('{author}', book.author);
          combinedComments.push({
            id: 'mock-c-' + i,
            user: user,
            content: text,
            created_at: book.archivedDate + ' 오후 ' + (2 + i) + ':15',
            reactions: { "❤️": 15 + i * 3, "✨": 9 + i * 2 }
          });
        }
      }

      // DB에 채팅이 비어있을 시 실시간 독서방 대화 발췌 스레드 주입
      var combinedChats = chats.slice();
      if (combinedChats.length === 0) {
        var chatSeeds = [
          { user: "기억수집가", text: "다들 주인공이 마지막 장벽을 마주했을 때의 독백 보셨나요? 울컥했습니다." },
          { user: "봄날사서", text: "맞아요. 소중한 가치를 지키기 위해서 스스로의 규율을 깨뜨릴 수밖에 없었던 선택이 눈물겹더군요." },
          { user: "다은이좋아", text: "사서라는 존재가 원래 경계에 머물며 기록을 보관하니까요. 이 소설은 그 직업적 숙명을 정말 시적으로 다뤘어요." },
          { user: "도서관팬", text: "동감합니다. 책으로 박제되는 순간 기억은 끝나지만, 다은이 책을 닫음으로써 삶은 여전히 지속된다는 암시가 대단해요." }
        ];
        chatSeeds.forEach(function(s, idx) {
          combinedChats.push({
            id: 'mock-ch-' + idx,
            user: s.user,
            text: s.text,
            ts: '오후 08:' + (12 + idx * 4),
            date: new Date().toISOString()
          });
        });
      }

      // 아카이브 전반적인 핵심 통계 데이터 계산
      var totalUsers = distinctUsers.length;
      var totalChats = combinedChats.length;
      var totalComments = combinedComments.length;
      var totalReactions = 0;
      combinedComments.forEach(function(c) {
        if (c.reactions) {
          Object.values(c.reactions).forEach(function(v) { totalReactions += v; });
        }
      });
      var avgScore = ratingsSummary.avg_score || 4.6;

      var miniMeta = document.getElementById('arc-page-meta');
      if (miniMeta) miniMeta.textContent = totalUsers + '명 참여 · ' + book.archivedDate + ' 종료';

      // HSL 조화로운 컬러 테마 맵 ( deterministic 닉네임 아바타 구현 )
      function getNickColor(name) {
        var colors = [
          {bg: '#ecf4e8', fg: '#4a7a3a'}, // light green
          {bg: '#dce8f8', fg: '#2c5f8a'}, // light blue
          {bg: '#fdf0e4', fg: '#a06020'}, // light orange
          {bg: '#fce0e8', fg: '#b54a6a'}, // light pink
          {bg: '#dcf4ec', fg: '#1d7a58'}, // teal
          {bg: '#e8e8d8', fg: '#6a6a28'}, // olive
          {bg: '#dce8f0', fg: '#2a5870'}, // steel blue
          {bg: '#ece0f8', fg: '#7040b0'}, // purple
          {bg: '#daf0ec', fg: '#1a6a60'}  // slate green
        ];
        var sum = 0;
        for (var i = 0; i < name.length; i++) {
          sum += name.charCodeAt(i);
        }
        return colors[sum % colors.length];
      }

      var html = '';

      // 1. 아카이브 고품격 커버 (Editorial Cover)
      html += '<div class="arc-cover" style="border-top: 6px solid ' + book.color + ';">';
      html += '  <div class="arc-cover-label">가공독서회 · 아카이브 에디션 · 제' + book.id + '호</div>';
      html += '  <div class="arc-cover-book-icon">';
      html += '    <div class="arc-cover-book-inner" style="background:' + book.color + ';">' + book.title.slice(0, 5) + '</div>';
      html += '  </div>';
      html += '  <div class="arc-cover-title">' + book.title + '</div>';
      html += '  <div class="arc-cover-subtitle">' + book.author + ' · ' + book.genre + ' · ' + book.price + '</div>';
      html += '  <div class="arc-cover-divider"></div>';
      html += '  <div class="arc-cover-author-note">' + totalUsers + '인의 독서회 종료 기념 감상 아카이브 에디션</div>';
      html += '  <div class="arc-cover-meta">';
      html += '    <span>READING ROOM ARCHIVE</span>';
      html += '    <span>' + totalUsers + ' READERS · ' + totalChats + ' MESSAGES</span>';
      html += '    <span>GAKONG BOOK CLUB</span>';
      html += '  </div>';
      html += '</div>';

      // 2. 도서 핵심 띠지 (Book Band)
      html += '<div class="arc-book-band">';
      html += '  <div class="arc-book-band-cover" style="background:' + book.color + ';">' + book.title.slice(0, 5) + '</div>';
      html += '  <div>';
      html += '    <div class="arc-book-band-genre" style="color:' + book.color + ';">' + book.genre.toUpperCase() + '</div>';
      html += '    <div class="arc-book-band-title">' + book.title + '</div>';
      html += '    <div class="arc-book-band-author">' + book.author + '</div>';
      html += '    <div class="arc-book-band-synopsis">' + book.synopsis + '</div>';
      html += '    <div class="arc-book-band-tags">';
      book.tags.forEach(function(t) {
        html += '      <span class="arc-book-band-tag">' + t + '</span>';
      });
      html += '    </div>';
      html += '  </div>';
      html += '</div>';

      // 3. 통계 바 (Stats Bar)
      html += '<div class="arc-stats-bar">';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalUsers + '</div>';
      html += '    <div class="arc-stat-label">참여 독자</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalChats + '</div>';
      html += '    <div class="arc-stat-label">채팅 메시지</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalComments + '</div>';
      html += '    <div class="arc-stat-label">댓글</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalReactions + '</div>';
      html += '    <div class="arc-stat-label">총 반응 수</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + avgScore.toFixed(1) + '</div>';
      html += '    <div class="arc-stat-label">평균 평점</div>';
      html += '  </div>';
      html += '</div>';
      // 채팅방 전체 열람 버튼: 독서방의 모든 채팅 기록을 읽기 전용으로 볼 수 있도록 이동
      html += '<div class="arc-view-chat-btn-wrap">';
      html += '  <button class="arc-view-chat-btn" onclick="openChatHistory(' + bookId + ')">';
      html += '    💬 채팅방 전체 열람하기';
      html += '  </button>';
      html += '</div>';

      // 4. 에디토리얼 레터 (Editor's Note)
      html += '<div class="arc-section arc-editorial">';
      html += '  <div class="arc-eyebrow">EDITOR\'S NOTE</div>';
      html += '  <div class="arc-editorial-title">편집자의 말</div>';
      html += '  <div class="arc-editorial-body">';
      html += '    <p>이 책은 존재하지 않습니다. 그러나 이 안에 담긴 감상들은 진짜입니다.</p>';
      html += '    <p>가공독서회의 ' + totalUsers + '명 독자들은 『' + book.title + '』의 시놉시스 한 줄을 마주하고 사흘간 무수히 아름다운 감상을 꽃피워냈습니다. 아무도 실제로 이 책을 읽지 않았지만, 모두가 각자의 마음속에서 이 책을 다 읽어낸 것처럼 고요하고도 깊은 이야기를 나누었습니다.</p>';
      html += '    <p>이 아카이브는 바로 그 환상적인 공간의 편린이자 정수가 담긴 기록입니다. 실시간 독서 대화 스레드에서 특히 뜨거웠던 문맥들, 댓글 중에서 독자들의 심금을 울려 가장 추천을 많이 받은 명구절들을 세심하게 묶었습니다.</p>';
      html += '    <p>존재하지 않기에 무한히 뻗어나갈 수 있었던 상상의 조각상들, 그것이 이 아카이브 책장이 건네는 진심 어린 기록입니다.</p>';
      html += '  </div>';
      var yearVal = '2026';
      var monthVal = '6';
      if (book.archivedDate && book.archivedDate.indexOf('-') !== -1) {
        var parts = book.archivedDate.split('-');
        yearVal = parts[0];
        monthVal = parseInt(parts[1]) || '6';
      }
      html += '  <div class="arc-editorial-sig"><span>가공독서회 아카이브 편집위원회</span><span>' + yearVal + '년 ' + monthVal + '월</span></div>';
      html += '</div>';

      // 5. 독서 참여자 리스트 (Participants)
      html += '<div class="arc-section" style="background:#fff;">';
      html += '  <div class="arc-eyebrow">PARTICIPANTS</div>';
      html += '  <div class="arc-section-title">이번 독서회 참여자 ' + totalUsers + '인</div>';
      html += '  <div class="arc-section-sub">닉네임은 가공독서회 시스템이 고유하게 배정했습니다. 본명은 영구 비공개됩니다.</div>';
      html += '  <div class="arc-participants-grid">';
      distinctUsers.forEach(function(u) {
        var clr = getNickColor(u);
        html += '    <div class="arc-p-chip">';
        html += '      <div class="arc-p-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + u.charAt(0) + '</div>';
        html += '      <div class="arc-p-name">' + u + '</div>';
        html += '    </div>';
      });
      html += '  </div>';
      html += '</div>';

      // 6. 1장: 책의 이야기와 첫인상 (Chapter 1)
      html += '<div class="arc-chapter-divider"></div>';
      html += '<div class="arc-chapter-header">';
      html += '  <div class="arc-chapter-num">1장</div>';
      html += '  <div class="arc-chapter-title">책의 첫인상과 사색의 순간들</div>';
      html += '  <div class="arc-chapter-desc">『' + book.title + '』의 세계를 처음 마주했을 때 독자들이 나눈 깊고 고요한 첫 감상들의 모음.</div>';
      html += '</div>';

      html += '<div class="arc-messages-area">';

      // 상위 2개 감상 댓글 카드 렌더링
      var earlyComments = combinedComments.slice(0, 2);
      earlyComments.forEach(function(c, idx) {
        var clr = getNickColor(c.user);
        var isHighlight = idx === 0;
        var cardClass = isHighlight ? 'arc-msg-card highlight' : 'arc-msg-card top-pick';

        html += '  <div class="' + cardClass + '">';
        if (!isHighlight) {
          html += '    <div class="arc-top-pick-badge">TOP PICK</div>';
        }
        html += '    <div class="arc-msg-head">';
        html += '      <div class="arc-msg-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + c.user.charAt(0) + '</div>';
        html += '      <div>';
        html += '        <div class="arc-msg-name">' + c.user + '</div>';
        html += '        <div class="arc-msg-time">독서회 댓글 · ' + c.created_at + '</div>';
        html += '      </div>';
        html += '    </div>';
        html += '    <div class="arc-msg-body">' + c.content + '</div>';
        html += '    <div class="arc-msg-reactions">';

        var rxHearts = c.reactions && c.reactions["❤️"] || (18 + idx * 6);
        var rxStars = c.reactions && c.reactions["✨"] || (14 + idx * 5);

        html += '      <span class="arc-rx-tag hot">❤️ 공감해요 ' + rxHearts + '</span>';
        html += '      <span class="arc-rx-tag hot">✨ 인상 깊어요 ' + rxStars + '</span>';
        html += '      <div class="arc-rx-total">총 <strong>' + (rxHearts + rxStars) + '</strong>개 반응</div>';
        html += '    </div>';
        html += '  </div>';
      });

      // 실시간 채팅방 스레드 발췌 렌더링
      html += '  <div class="arc-chat-thread">';
      html += '    <div class="arc-chat-thread-label"><span>독서방 실시간 대화 스레드 발췌</span></div>';
      combinedChats.forEach(function(ch, idx) {
        var clr = getNickColor(ch.user);
        var isMine = ch.user === 'ME' || ch.user === assignedNick;
        var rowClass = isMine ? 'arc-chat-row mine' : 'arc-chat-row other';

        html += '    <div class="' + rowClass + '">';
        if (!isMine) {
          html += '      <div class="arc-chat-av-sm" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + ch.user.charAt(0) + '</div>';
        }
        html += '      <div class="arc-chat-col">';
        if (!isMine) {
          html += '        <div class="arc-chat-name-sm">' + ch.user + '</div>';
        }
        html += '        <div class="arc-chat-bubble">' + ch.text + '</div>';
        if (!isMine) {
          html += '        <div style="display:flex;gap:4px;margin-top:4px;">';
          html += '          <span class="arc-crx hot">❤️ ' + (12 - idx * 2 > 0 ? 12 - idx * 2 : 5) + '</span>';
          html += '          <span class="arc-crx">✨ ' + (8 - idx > 0 ? 8 - idx : 3) + '</span>';
          html += '        </div>';
        }
        html += '      </div>';
        html += '      <span style="font-size:10px;color:#6b5040;align-self:flex-end;flex-shrink:0;margin-left:4px;">' + ch.ts + '</span>';
        html += '    </div>';
      });
      html += '  </div>';

      // 도서 시평 추천 문학 쿼트 블록 렌더링
      var quoteText = book.memorableQuote || (book.endorsement ? book.endorsement.quote : "이 글귀는 우리가 활자 속으로 도망치는 모든 밤에 바치는 찬사이다.");
      var quoteAttr = book.memorableQuote ? "— 책 속 결정적 대사" : (book.endorsement ? book.endorsement.attr : "— 문학평론가 (익명)");
      html += '  <div class="arc-quote-block">';
      html += '    <div class="arc-quote-text">"' + quoteText + '"</div>';
      html += '    <div class="arc-quote-attr">' + quoteAttr + '</div>';
      html += '  </div>';
      html += '</div>';

      // 7. 2장: 가장 오래 남은 감상 최종 선별 TOP (Chapter 2)
      html += '<div class="arc-chapter-divider"></div>';
      html += '<div class="arc-chapter-header">';
      html += '  <div class="arc-chapter-num">2장</div>';
      html += '  <div class="arc-chapter-title">가장 오래 남은 감상 문장들</div>';
      html += '  <div class="arc-chapter-desc">독서방 전반에서 반응 수 합계 기준, 독자들에게 가장 뜨거운 공명을 불러일으킨 감상들.</div>';
      html += '</div>';

      html += '<div class="arc-section arc-top-sentences" style="padding-top:0;">';

      // 감상 댓글 반응수 기준 내림차순 정렬
      var sortedComments = combinedComments.slice().sort(function(a, b) {
        var rxA = 0; if (a.reactions) Object.values(a.reactions).forEach(function(v) { rxA += v; });
        var rxB = 0; if (b.reactions) Object.values(b.reactions).forEach(function(v) { rxB += v; });
        return rxB - rxA;
      });

      sortedComments.forEach(function(c, index) {
        var clr = getNickColor(c.user);
        var rank = (index + 1) < 10 ? '0' + (index + 1) : (index + 1);
        var totalRx = 0; if (c.reactions) Object.values(c.reactions).forEach(function(v) { totalRx += v; });

        html += '  <div class="arc-sentence-item">';
        html += '    <div class="arc-sentence-rank">' + rank + '</div>';
        html += '    <div class="arc-sentence-body">';
        html += '      <div class="arc-sentence-text">' + c.content + '</div>';
        html += '      <div class="arc-sentence-meta">';
        html += '        <div class="arc-sentence-author">';
        html += '          <div class="arc-s-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + c.user.charAt(0) + '</div>';
        html += '          <span class="arc-s-name">' + c.user + '</span>';
        html += '        </div>';
        html += '        <div class="arc-s-rxs">';
        if (c.reactions) {
          Object.keys(c.reactions).forEach(function(k) {
            html += '          <span class="arc-s-rx">' + k + ' ' + c.reactions[k] + '</span>';
          });
        } else {
          html += '          <span class="arc-s-rx">❤️ 18</span><span class="arc-s-rx">✨ 14</span>';
        }
        html += '        </div>';
        html += '        <span style="font-size:11px;color:var(--text-faint);margin-left:8px;">총 ' + totalRx + ' 공명 · 아카이브 전체 ' + (index + 1) + '위</span>';
        html += '      </div>';
        html += '    </div>';
        html += '  </div>';
      });
      html += '</div>';

      // 8. 맺음말 (Closing Mark)
      html += '<div class="arc-chapter-divider"></div>';
      html += '<div class="arc-closing">';
      html += '  <div class="arc-closing-mark">✦</div>';
      html += '  <div class="arc-closing-title">기록의 보관을 마치며</div>';
      html += '  <div class="arc-closing-body">';
      html += '    『' + book.title + '』의 독서방은 공식 종료되었습니다. 그러나 우리가 활자 너머로 나누었던 상상과 연대의 불씨는 사라지지 않고 이 아카이브 공간에 영원히 보존될 것입니다.';
      html += '  </div>';
      html += '</div>';

      // 9. 판권지 및 콜로폰 (Colophon)
      html += '<div class="arc-colophon">';
      html += '  <div class="arc-colophon-grid">';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">발행처</div>';
      html += '      <div class="arc-col-val">가공독서회 보존기록팀</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">기획 및 구성</div>';
      html += '      <div class="arc-col-val">가공 아카이브 에디터 일동</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">서지 분류 번호</div>';
      html += '      <div class="arc-col-val">GK-ARC-2026-N' + book.id + '</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">보관 개시일</div>';
      html += '      <div class="arc-col-val">' + book.archivedDate + '</div>';
      html += '    </div>';
      html += '  </div>';
      html += '  <div class="arc-colophon-foot">';
      html += '    © GAKONG BOOK CLUB. ALL MEMORIES RESERVED.';
      html += '  </div>';
      html += '</div>';

      if (arcContent) arcContent.innerHTML = html;
    }

    /* ── CHAT HISTORY (읽기 전용 채팅 열람) ── */
    async function openChatHistory(bookId) {
      var targetId = parseInt(bookId) || bookId;
      var book = BOOKS.find(function(b) { return b.id == targetId; });
      if (!book) return;
      // 헤더 정보 먼저 업데이트 후 페이지 전환
      var titleEl = document.getElementById('chat-history-title');
      if (titleEl) titleEl.textContent = book.title + ' — 채팅방 기록';
      var coverEl = document.getElementById('chat-history-header-book');
      if (coverEl) { coverEl.style.background = book.color; coverEl.textContent = book.title; }
      var metaEl = document.getElementById('chat-history-meta');
      if (metaEl) metaEl.textContent = '기록 불러오는 중...';
      // 현재 활성화된 페이지를 저장하여 뒤로가기 시 원래 위치로 돌아가도록 설정
      var activePg = document.querySelector('.page.active');
      if (activePg && activePg.id !== 'pg-chat-history') {
        window.lastPageBeforeArchive = activePg.id.replace('pg-', '');
      }
      goPage('chat-history');
      // 로딩 상태 표시
      var body = document.getElementById('chat-history-body');
      if (body) body.innerHTML = '<div style="padding:60px 20px;text-align:center;color:var(--text-faint);font-size:14px;">채팅 기록을 불러오는 중... 💬</div>';
      // 백엔드 API에서 채팅 기록 로드
      var chats = [];
      if (window.location.protocol !== 'file:') {
        try {
          var res = await fetch('/api/books/' + bookId + '/chat-history');
          if (res.ok) chats = await res.json();
        } catch (e) { console.error('채팅 열람 기록 로드 오류:', e); }
      }
      // API 응답이 비어있으면 프론트엔드 캐시(chatMsgs)에서 fallback
      if (!chats.length && chatMsgs[targetId] && chatMsgs[targetId].length) {
        chats = chatMsgs[targetId].map(function(m) {
          return {
            user: m.user,
            text: m.text,
            ts: m.ts,
            date: m.date ? (m.date instanceof Date ? m.date.toISOString() : m.date) : new Date().toISOString(),
            replyTo: m.replyTo || null,
            reactions: m.reactions || {}
          };
        });
      }
      // 여전히 비어있을 시 독서방 가상 대화 시드 주입 (가상 도서의 특성을 반영한 고품질 fallback)
      if (!chats.length) {
        var fallbackSeeds = [
          { user: "기억수집가", text: "다들 주인공이 마지막 장벽을 마주했을 때의 독백 보셨나요? 울컥했습니다.", ts: "오후 08:12" },
          { user: "봄날사서", text: "맞아요. 소중한 가치를 지키기 위해서 스스로의 규율을 깨뜨릴 수밖에 없었던 선택이 눈물겹더군요.", ts: "오후 08:16" },
          { user: "다은이좋아", text: "사서라는 존재가 원래 경계에 머물며 기록을 보관하니까요. 이 소설은 그 직업적 숙명을 정말 시적으로 다뤘어요.", ts: "오후 08:20" },
          { user: "도서관팬", text: "동감합니다. 책으로 박제되는 순간 기억은 끝나지만, 다은이 책을 닫음으로써 삶은 여전히 지속된다는 암시가 대단해요.", ts: "오후 08:24" }
        ];
        var now = new Date();
        chats = fallbackSeeds.map(function(s, idx) {
          var msgTime = new Date(now);
          msgTime.setHours(20, 12 + idx * 4, 0, 0);
          return {
            id: 'mock-ch-hist-' + idx,
            user: s.user,
            text: s.text,
            ts: s.ts,
            date: msgTime.toISOString(),
            replyTo: null,
            reactions: { "❤️": (12 - idx * 2 > 0 ? 12 - idx * 2 : 5), "✨": (8 - idx > 0 ? 8 - idx : 3) }
          };
        });
      }
      // 메타 정보 업데이트
      if (metaEl) metaEl.textContent = '총 ' + chats.length + '개 메시지 · 읽기 전용';
      if (!body) return;
      body.innerHTML = '';
      // 채팅 기록이 없는 경우 안내 메시지
      if (!chats.length) {
        body.innerHTML =
          '<div style="padding:80px 20px;text-align:center;color:var(--text-faint);">' +
          '<div style="font-size:32px;margin-bottom:16px;">💬</div>' +
          '<div style="font-size:15px;font-weight:600;margin-bottom:8px;">채팅 기록이 없습니다</div>' +
          '<div style="font-size:13px;">이 독서방에서는 채팅이 진행되지 않았거나,<br>아직 기록이 이전되지 않았습니다.</div>' +
          '</div>';
        return;
      }
      // 독서방 개설 공지
      body.appendChild(makeDivider('독서방 개설일'));
      body.appendChild(makeNotice('📚 독서방이 열렸습니다. · 이 기록은 읽기 전용 열람 모드입니다.'));
      // 날짜별 그룹화하여 메시지 렌더링
      var lastDKey = null;
      chats.forEach(function(ch) {
        var date = ch.date ? new Date(ch.date) : new Date();
        var dk = dateKey(date);
        if (dk !== lastDKey) {
          body.appendChild(makeDateDivider(date));
          lastDKey = dk;
        }
        body.appendChild(buildReadOnlyMsgEl(ch));
      });
      // 종료 공지
      body.appendChild(makeNotice('📦 독서방이 종료되었습니다. 아카이브에 보관 중입니다.'));
      // 맨 위로 스크롤
      body.scrollTop = 0;
    }

    /**
     * 읽기 전용 채팅 메시지 엘리먼트를 생성합니다.
     * 수정/삭제/반응/답장 버튼이 없는 순수 열람용 버블입니다.
     */
    function buildReadOnlyMsgEl(ch) {
      // 닉네임 기반 고유 아바타 색상 결정
      var avColors = [
        {bg:'#e8daf8', fg:'#7b5fb8'}, {bg:'#f0e8dc', fg:'#8b4f25'},
        {bg:'#e8f0f8', fg:'#2c5f8a'}, {bg:'#e8f0dc', fg:'#2d7a50'},
        {bg:'#f0f8dc', fg:'#3a6a20'}, {bg:'#fce8e0', fg:'#a03020'},
        {bg:'#dce8f0', fg:'#2a5870'}, {bg:'#ece0f8', fg:'#7040b0'},
        {bg:'#dcf4ec', fg:'#1d7a58'}, {bg:'#f5d87a', fg:'#7a4a10'}
      ];
      var sum = 0;
      var userName = ch.user || '익명';
      for (var i = 0; i < userName.length; i++) sum += userName.charCodeAt(i);
      var clr = avColors[sum % avColors.length];
      var av = userName.charAt(0);
      // 답장 인용 블록
      var replyQuote = '';
      if (ch.replyTo) {
        replyQuote =
          '<div class="chat-reply-quote">' +
          '<div class="chat-reply-quote-name">↩ ' + escHtml(ch.replyTo.user || '') + '</div>' +
          '<div class="chat-reply-quote-text">' +
          escHtml((ch.replyTo.text || '').slice(0, 60) + ((ch.replyTo.text || '').length > 60 ? '…' : '')) +
          '</div></div>';
      }
      // 반응 표시 (클릭 불가, 숫자만 표시)
      var rxHtml = '';
      if (ch.reactions && Object.keys(ch.reactions).length) {
        var rxItems = '';
        Object.keys(ch.reactions).forEach(function(emoji) {
          var raw = ch.reactions[emoji];
          // DB 형식(숫자) 또는 캐시 형식(객체) 모두 처리
          var cnt = (typeof raw === 'object' && raw !== null) ? (raw.count || 0) : (raw || 0);
          if (cnt > 0) rxItems += '<span class="chat-rx-readonly">' + emoji + ' ' + cnt + '</span>';
        });
        if (rxItems) rxHtml = '<div class="chat-reactions">' + rxItems + '</div>';
      }
      // 읽기 전용이므로 모든 메시지를 'other' 스타일로 렌더링 (내 메시지 구분 없음)
      var row = document.createElement('div');
      row.className = 'chat-row other chat-row-readonly';
      row.innerHTML =
        '<div class="chat-av" style="background:' + clr.bg + ';color:' + clr.fg + '">' + av + '</div>' +
        '<div class="chat-col">' +
        '<div class="chat-name">' + escHtml(userName) + '</div>' +
        '<div class="chat-bubble">' + replyQuote + escHtml(ch.text || '') + '</div>' +
        rxHtml +
        '</div>' +
        '<div class="chat-time-wrap"><span class="chat-time">' + (ch.ts || '') + '</span></div>';
      return row;
    }

    /* ── LIBRARY TABS ── */
    var currentLibTab = 'saved';
    var selArcBook = null;

    function switchLibTab(tab) {
      currentLibTab = tab;
      document.getElementById('lib-tab-saved').classList.toggle('active', tab === 'saved');
      document.getElementById('lib-tab-archive').classList.toggle('active', tab === 'archive');
      document.getElementById('shelf-area').style.display = tab === 'saved' ? '' : 'none';
      document.getElementById('arc-shelf-area').style.display = tab === 'archive' ? 'block' : 'none';
      if (tab === 'archive') renderArcLib();
    }

    function renderArcLib() {
      var arcParticipated = BOOKS.filter(function (b) {
        return b.archived && (chatMsgs[b.id] || []).some(function (m) { return m.userId === 'ME' || m.userId == CURRENT_USER_ID; });
      });
      // demo: always surface b7 (구름 위의 도서관) since it has the full archive
      var b7 = BOOKS.find(function (b) { return b.id == 7; });
      if (b7 && !arcParticipated.find(function (b) { return b.id == 7; })) {
        arcParticipated.unshift(b7);
      }
      var badge = document.getElementById('lib-arc-badge');
      if (badge) { badge.style.display = arcParticipated.length > 0 ? '' : 'none'; badge.textContent = arcParticipated.length; }

      var row = document.getElementById('arc-books-row');
      var bdp = document.getElementById('arc-lib-bdp');
      if (!arcParticipated.length) {
        row.innerHTML = '<div class="arc-empty">참여한 독서방이 종료되면 여기에 아카이브가 쌓여요.</div>';
        if (bdp) bdp.style.display = 'none'; selArcBook = null; return;
      }
      row.innerHTML = '';
      var heights = [110, 95, 105, 90, 115];
      arcParticipated.forEach(function (b, i) {
        var h = heights[i % heights.length];
        var el = document.createElement('div');
        el.className = 'arc-book-spine' + (selArcBook === b.id ? ' sel' : '');
        el.id = 'arclb-' + b.id;
        el.style.cssText = 'height:' + h + 'px;background:' + b.color + ';';
        el.innerHTML = '<div class="arc-book-spine-txt">' + b.title + '</div>';
        el.onclick = (function (bid, blist) { return function () { pickArcLibBook(bid, blist); }; })(b.id, arcParticipated);
        row.appendChild(el);
      });
      if (!selArcBook && arcParticipated.length) pickArcLibBook(arcParticipated[0].id, arcParticipated);
    }

    function pickArcLibBook(id, list) {
      var targetId = parseInt(id) || id;
      var book = (list || BOOKS).find(function (b) { return b.id == targetId; });
      if (!book) return;
      document.querySelectorAll('.arc-book-spine').forEach(function (e) { e.classList.remove('sel'); });
      var bdp = document.getElementById('arc-lib-bdp');
      if (selArcBook === id && bdp && bdp.style.display === 'block') {
        selArcBook = null; bdp.style.display = 'none'; return;
      }
      selArcBook = id;
      var el = document.getElementById('arclb-' + id);
      if (el) el.classList.add('sel');
      var myChatCount = (chatMsgs[id] || []).filter(function (m) { return m.userId === 'ME' || m.userId == CURRENT_USER_ID; }).length;
      var cov = document.getElementById('arc-lib-bdp-cover');
      if (cov) { cov.style.background = book.color; cov.textContent = book.title.slice(0, 4); }
      var ti = document.getElementById('arc-lib-bdp-title');
      if (ti) ti.textContent = book.title;
      var su = document.getElementById('arc-lib-bdp-sub');
      if (su) su.textContent = book.archivedDate + ' 종료 · 내 감상 ' + myChatCount + '개 포함';
      var btn = document.getElementById('arc-lib-bdp-btn');
      if (btn) {
        btn.textContent = '아카이브 보기';
        btn.style.background = '#4a7a3a'; btn.style.cursor = 'pointer';
        btn.onclick = function () { openArchiveFromLib(); };
      }
      if (bdp) bdp.style.display = 'block';
    }

    function openArchiveFromLib() {
      if (!selArcBook) return;
      openArchive(selArcBook);
    }

    // ── 가공독서회 글로벌 동적 인증 & DB 연동 핸들러 ──

    // 백엔드 DB 책 데이터를 프론트엔드 호환 포맷으로 매핑하는 어댑터
    function adaptDbBookToFrontend(dbBook) {
      var deadlineVal = dbBook.deadline_days !== undefined ? dbBook.deadline_days : 10;
      return {
        id: dbBook.id,
        color: dbBook.color || '#7b5fb8',
        genre: dbBook.genre || '소설',
        title: dbBook.title,
        author: dbBook.author || '작가 미상',
        synopsis: dbBook.synopsis || '',
        tags: Array.isArray(dbBook.tags) ? dbBook.tags : (dbBook.tags ? dbBook.tags.split(',') : []),
        price: dbBook.price ? '₩' + parseInt(String(dbBook.price).replace(/[^0-9]/g, '') || 0).toLocaleString() : '₩14,000',
        pageCount: dbBook.page_count || 300,
        deadlineDays: deadlineVal,
        archived: dbBook.is_archived || false,
        archivedDate: dbBook.created_at ? new Date(new Date(dbBook.created_at).getTime() + deadlineVal * 24 * 60 * 60 * 1000).toISOString().split('T')[0] : '종료',
        count: dbBook.participant_count !== undefined ? dbBook.participant_count : 0,
        endorsement: {
          quote: dbBook.endorsement_quote || '이 책은 독자의 상상력을 한계까지 밀어붙인다.',
          attr: dbBook.endorsement_attr || '— 가공 평론가 (익명)'
        },
        publisherReview: dbBook.publisher_review || 'AI와 독자의 상상력이 만들어낸 전례 없는 독서 경험.',
        openingLine: dbBook.opening_line || '',
        memorableQuote: dbBook.memorable_quote || '',
        coreDilemma: dbBook.core_dilemma || '',
        additionalQuestions: dbBook.additional_questions || '',
        characters: dbBook.characters || '',
        immersionData: (function() {
          if (!dbBook.immersion_data) return null;
          if (typeof dbBook.immersion_data === 'object') return dbBook.immersion_data;
          try {
            return JSON.parse(dbBook.immersion_data);
          } catch(e) {
            console.error('Failed to parse immersion_data:', e);
            return null;
          }
        })(),
        ratings: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
        comments: []
      };
    }

    // 백엔드 데이터베이스로부터 실시간 활성 책 목록 온디맨드 로딩
    var archivedLoaded = false;

    async function fetchArchivedBooks() {
      if (archivedLoaded || window.location.protocol === 'file:') return;
      try {
        var resArc = await fetch('/api/books/archived');
        if (resArc.ok) {
          var dbArcBooks = await resArc.json();
          var arcList = dbArcBooks.map(adaptDbBookToFrontend);
          arcList.forEach(function (ab) {
            if (!BOOKS.some(function (b) { return b.id === ab.id; })) {
              BOOKS.push(ab);
            }
          });
          archivedLoaded = true;
          renderHome();
        }
      } catch (err) {
        console.error('아카이브 도서 로딩 중 오류 발생:', err);
      }
    }

    async function fetchActiveBooks() {
      // 로컬 파일 더블클릭 실행 시(file:///) API fetch를 수행하지 않고 하드코딩된 서버 데이터를 즉시 사용하도록 예외 처리
      if (window.location.protocol === 'file:') {
        console.log('로컬 파일 실행 모드: 정적 BOOKS 데이터를 사용합니다.');
        renderHome();
        return;
      }
      try {
        var res = await fetch('/api/books');
        if (res.ok) {
          var dbBooks = await res.json();
          var activeList = dbBooks.map(adaptDbBookToFrontend);

          // 홈 메인 렌더링에 필요한 활성 도서 위주로 먼저 즉시 반영 (초기 속도 극대화)
          BOOKS = activeList;
          renderHome();
        }
      } catch (err) {
        console.error("데이터베이스 책 목록 동기화 중 오류 발생:", err);
      }
    }

    // 글로벌 로그인/로그아웃 UI 동적 동기화

    async function recoverSession() {
      // 1. 항상 먼저 최신 책 목록을 데이터베이스에서 비동기 로딩 완료시킵니다.
      await fetchActiveBooks();
      var cachedToken = localStorage.getItem('token');
      if (!cachedToken) {
        updateAuthUI();
        return;
      }
      try {
        var res = await fetch('/api/auth/me', {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + cachedToken
          }
        });
        if (res.ok) {
          var data = await res.json();
          isLoggedIn = true;
          currentUser = { name: data.nickname, nickname: data.nickname, email: data.email, isAdmin: data.is_admin };
          CURRENT_USER_ID = data.id;
          // 로컬스토리지 최신화
          localStorage.setItem('user_nickname', data.nickname);
          localStorage.setItem('user_email', data.email);
          localStorage.setItem('user_id', data.id);
          localStorage.setItem('user_is_admin', data.is_admin);
          updateNavbar();
          updateAuthUI();
          // 2. 책 목록이 전역 BOOKS에 완벽히 들어찬 직후, 내 서재 정보를 로드합니다.
          await loadMyLibrary();
        } else {
          // 토큰 만료 또는 세션 무효화 시 리셋
          localStorage.removeItem('token');
          localStorage.removeItem('user_nickname');
          localStorage.removeItem('user_email');
          localStorage.removeItem('user_id');
          localStorage.removeItem('user_is_admin');
          isLoggedIn = false;
          currentUser = null;
          CURRENT_USER_ID = 'ME';
          libBooks = [];
          myLibraryData = [];
          updateNavbar();
          updateAuthUI();
        }
      } catch (err) {
        console.error('세션 비동기 복구 중 에러 발생 (오프라인 폴백 동작):', err);
        // 네트워크 단절 시 로컬스토리지 백업 데이터 기반 복구 (오프라인 폴백)
        var cachedNick = localStorage.getItem('user_nickname');
        var cachedEmail = localStorage.getItem('user_email');
        var cachedId = localStorage.getItem('user_id');
        var cachedIsAdmin = localStorage.getItem('user_is_admin') === 'true';
        if (cachedNick) {
          isLoggedIn = true;
          currentUser = { name: cachedNick, nickname: cachedNick, email: cachedEmail || '', isAdmin: cachedIsAdmin };
          if (cachedId) CURRENT_USER_ID = parseInt(cachedId, 10);
          await loadMyLibrary();
        } else {
          isLoggedIn = false;
          currentUser = null;
          CURRENT_USER_ID = 'ME';
          libBooks = [];
          myLibraryData = [];
        }
        updateAuthUI();
      }
    }

// === STARTUP & INITIALIZATION ===
    // 최초 로드 자동 세션 복구 및 DB 연동 초기 호출
    recoverSession();

