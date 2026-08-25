// === BOOKS, LIBRARY, COMMENTS & ARCHIVE MODULE ===
    (function injectQuickToolbarStyles() {
      var style = document.createElement('style');
      style.textContent = 
        '#pg-chat.active { display: flex !important; flex-direction: column !important; min-height: calc(100vh - 68px) !important; padding-bottom: 75px !important; box-sizing: border-box !important; position: relative !important; } ' +
        '#pg-chat.active .chat-header { position: sticky !important; top: 68px !important; z-index: 100 !important; } ' +
        '#pg-chat.active .chat-body { flex: 1 !important; overflow-y: auto !important; min-height: 0 !important; padding-bottom: 20px !important; } ' +
        '#pg-chat.active .reply-preview-bar { position: fixed !important; bottom: 62px !important; left: 0 !important; right: 0 !important; z-index: 9998 !important; } ' +
        '#pg-chat.active .chat-input-bar { position: fixed !important; bottom: 0 !important; left: 0 !important; right: 0 !important; z-index: 9999 !important; box-shadow: 0 -4px 20px rgba(0,0,0,0.35) !important; background: #201a11 !important; } ' +
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
        publisherReview: '시대를 어둡게 짓누르는 지배적 관념을 경쾌한 야유로 풍자해 해방감을 안겨주는 지혜롭고 기발한 소설.',
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
        count: 18,
        endorsement: {
          quote: '가장 비극적인 위선을 우스꽝스럽고 찬란한 웃음으로 승화시키는 해학의 놀라운 재능.',
          attr: '— 칼럼니스트 (익명)'
        },
        publisherReview: '시대를 어둡게 짓누르는 지배적 관념을 경쾌한 야유로 풍자해 해방감을 안겨주는 지혜롭고 기발한 소설.',
        ratings: { 5: 16, 4: 8, 3: 2, 2: 0, 1: 0 },
        myRating: 0,
        rxCounts: { '❤️': 45, '🤔': 14, '😄': 28, '✨': 38 },
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


    function renderHome() {
      renderGenreSection();
      renderDeadlineSection();
    }

    
    // ── 장르 다국어 (한국어 / 일본어) 번역 맵 ──
    var GENRE_I18N = {
      '전체': { ko: '전체', ja: 'すべて' },
      '아카이브': { ko: '🗃 아카이브', ja: '🗃 アーカイブ' },
      '판타지': { ko: '판타지', ja: 'ファンタジー' },
      '에세이/비문학': { ko: '에세이/비문학', ja: 'エッセイ/ノンフィクション' },
      '소설': { ko: '소설', ja: '小説' },
      '로맨스': { ko: '로맨스', ja: 'ロマンス' },
      '로맨스 판타지': { ko: '로맨스 판타지', ja: 'ロマンスファンタジー' },
      '청춘/로맨스': { ko: '청춘/로맨스', ja: '青春/ロマンス' },
      '힐링/일상소설': { ko: '힐링/일상소설', ja: 'ヒーリング/日常小説' },
      '코믹/유머 에세이': { ko: '코믹/유머 에세이', ja: 'コミック/ユーモアエッセイ' },
      'SF/스페이스 탐험': { ko: 'SF/스페이스 탐험', ja: 'SF/スペース探検' },
      '추리/미스터리': { ko: '추리/미스터리', ja: '推理/ミステリー' },
      '판타지 모험': { ko: '판타지 모험', ja: 'ファンタジー冒険' },
      '철학적 에세이': { ko: '철학적 에세이', ja: '哲学エッセイ' },
      '드라마/성장소설': { ko: '드라마/성장소설', ja: 'ドラマ/成長小説' },
      '심리소설': { ko: '심리소설', ja: '心理小説' },
      '드라마': { ko: '드라마', ja: 'ドラマ' },
      'SF': { ko: 'SF', ja: 'SF' },
      '미스터리': { ko: '미스터리', ja: 'ミステリー' }
    };

    function translateGenre(genre) {
      var lang = (typeof CURRENT_LANG !== 'undefined') ? CURRENT_LANG : 'ko';
      if (lang === 'ja' && GENRE_I18N[genre] && GENRE_I18N[genre].ja) {
        return GENRE_I18N[genre].ja;
      }
      return genre;
    }
    window.translateGenre = translateGenre;

    /* ── 아카이브 월별 서가 ─────────────────────────────────────────────
       종료일(archivedDate)을 기준으로 도서를 달 단위로 묶는다.
       화면 구성은 styles.css의 .arc-month-* 규칙이 담당한다. */

    // 'YYYY-MM-DD' → { key: 'YYYY-MM', year: 2026, month: 6 }
    function parseArchiveMonth(dateStr) {
      var m = /^(\d{4})-(\d{2})/.exec(String(dateStr || ''));
      if (!m) return null;
      return { key: m[1] + '-' + m[2], year: parseInt(m[1], 10), month: parseInt(m[2], 10) };
    }

    // 언어에 맞는 월 표기 (ko: 2026년 6월 / ja: 2026年6月)
    function formatMonthLabel(info) {
      if (!info) return t('arc_month_unknown');
      return CURRENT_LANG === 'ja'
        ? info.year + '年' + info.month + '月'
        : info.year + '년 ' + info.month + '월';
    }

    // 도서 배열을 최신 달부터 정렬된 그룹 배열로 변환
    function groupBooksByMonth(books) {
      var buckets = {};
      var order = [];
      books.forEach(function (b) {
        var info = parseArchiveMonth(b.archivedDate);
        var key = info ? info.key : '0000-00';   // 종료일이 없는 건 맨 뒤로
        if (!buckets[key]) { buckets[key] = { key: key, info: info, books: [] }; order.push(key); }
        buckets[key].books.push(b);
      });
      order.sort(function (a, b) { return a < b ? 1 : (a > b ? -1 : 0); });   // 최신 달 우선
      return order.map(function (k) { return buckets[k]; });
    }

    // 아카이브 카드 1장의 마크업 (월별 서가와 기존 목록이 공유)
    function archiveCardHtml(b) {
      return '<div class="card-cover" style="' + getCoverCss(b) + '">' +
        '<div class="card-spine"></div>' +
        '<span>' + escHtml(b.title) + '</span>' +
        '<div class="arc-card-overlay">' +
        '<span class="arc-card-overlay-badge">' + t('arc_card_overlay') + '</span>' +
        '</div>' +
        '</div>' +
        '<div class="card-body">' +
        '<span class="card-genre" style="background:#eef5eb;color:#4a7a3a;border-color:#b8d9a8;">' + t('archive_badge') + '</span>' +
        '<div class="card-title">' + escHtml(b.title) + '</div>' +
        '<div class="card-synopsis">' + escHtml(b.synopsis) + '</div>' +
        '<div class="card-footer">' +
        '<span class="card-price" style="color:#4a7a3a;font-size:11px;">' + escHtml(b.archivedDate || '') + t('arc_closed_suffix') + '</span>' +
        '<span class="card-count">👥 ' + b.count + t('people_unit') + '</span>' +
        '</div>' +
        '</div>';
    }

    /* 아카이브 규모가 커져도 한 화면이 무너지지 않도록 세 가지 장치를 둔다.
         1) 연도 칩  : 연도가 2개 이상일 때만 노출, 특정 연도로 좁혀 본다
         2) 접기     : 최신 EXPANDED_MONTHS개월만 펼치고 나머지는 헤더만 보여준다
         3) 더 보기  : 한 번에 MONTHS_PER_PAGE개월씩만 그린다
       숫자만 바꾸면 노출 정책을 조정할 수 있다. */
    var EXPANDED_MONTHS = 3;
    var MONTHS_PER_PAGE = 12;

    var arcYearFilter = 'all';   // 'all' 또는 연도 문자열
    var arcVisibleMonths = MONTHS_PER_PAGE;
    var arcCollapsed = {};       // { 'YYYY-MM': true } — 사용자가 접은 달을 기억한다

    function renderArchiveByMonth(container, books) {
      container.className = 'arc-month-list';
      container.innerHTML = '';

      if (!books.length) {
        container.innerHTML = '<div class="arc-month-empty">' + t('arc_month_empty') + '</div>';
        return;
      }

      var allGroups = groupBooksByMonth(books);

      // ── 1) 연도 칩 ──
      var years = [];
      allGroups.forEach(function (g) {
        var y = g.info ? String(g.info.year) : null;
        if (y && years.indexOf(y) === -1) years.push(y);
      });
      if (years.length > 1) {
        var chips = document.createElement('div');
        chips.className = 'arc-year-chips';
        var chipHtml = '<button class="arc-year-chip' + (arcYearFilter === 'all' ? ' on' : '') +
          '" data-year="all">' + t('genre_all') + '</button>';
        years.forEach(function (y) {
          chipHtml += '<button class="arc-year-chip' + (arcYearFilter === y ? ' on' : '') +
            '" data-year="' + y + '">' + y + t('arc_year_unit') + '</button>';
        });
        chips.innerHTML = chipHtml;
        chips.querySelectorAll('.arc-year-chip').forEach(function (btn) {
          btn.onclick = function () {
            arcYearFilter = btn.getAttribute('data-year');
            arcVisibleMonths = MONTHS_PER_PAGE;   // 연도를 바꾸면 처음부터 다시 센다
            renderArchiveByMonth(container, books);
          };
        });
        container.appendChild(chips);
      }

      var groups = arcYearFilter === 'all' ? allGroups : allGroups.filter(function (g) {
        return g.info && String(g.info.year) === arcYearFilter;
      });

      // ── 2) 점진 렌더링: 앞에서부터 arcVisibleMonths개월만 ──
      var shown = groups.slice(0, arcVisibleMonths);
      var lastYear = null;

      shown.forEach(function (group, idx) {
        var wrap = document.createElement('div');
        wrap.className = 'arc-month-group';

        // 연도가 바뀌는 첫 달에만 연도 마커를 노출한다
        var yearMarker = '';
        if (group.info && group.info.year !== lastYear) {
          yearMarker = '<div class="arc-year-marker">' + group.info.year + '</div>';
          lastYear = group.info.year;
        }

        // ── 3) 접기: 최신 EXPANDED_MONTHS개월은 펼치고 나머지는 접는다 ──
        var key = group.key;
        var collapsed = (key in arcCollapsed) ? arcCollapsed[key] : (idx >= EXPANDED_MONTHS);

        wrap.innerHTML = yearMarker +
          '<button class="arc-month-header' + (collapsed ? ' collapsed' : '') + '" type="button">' +
          '<span class="arc-month-label">' + escHtml(formatMonthLabel(group.info)) + '</span>' +
          '<span class="arc-month-rule"></span>' +
          '<span class="arc-month-count">' + group.books.length + t('arc_book_unit') + '</span>' +
          '<span class="arc-month-caret">' + (collapsed ? '▾' : '▴') + '</span>' +
          '</button>' +
          '<div class="arc-month-grid"' + (collapsed ? ' hidden' : '') + '></div>';

        var grid = wrap.querySelector('.arc-month-grid');
        var filled = false;
        function fillGrid() {
          if (filled) return;
          group.books.forEach(function (b) {
            var card = document.createElement('div');
            card.className = 'card arc-card';
            card.style.cursor = 'pointer';
            card.onclick = (function (bid) { return function () { openDetail(bid); }; })(b.id);
            card.innerHTML = archiveCardHtml(b);
            grid.appendChild(card);
          });
          filled = true;
        }
        if (!collapsed) fillGrid();   // 접힌 달의 카드는 펼칠 때 만든다 (초기 렌더 비용 절약)

        wrap.querySelector('.arc-month-header').onclick = function () {
          var nowCollapsed = !grid.hidden;
          arcCollapsed[key] = nowCollapsed;
          if (!nowCollapsed) fillGrid();
          grid.hidden = nowCollapsed;
          this.classList.toggle('collapsed', nowCollapsed);
          this.querySelector('.arc-month-caret').textContent = nowCollapsed ? '▾' : '▴';
        };

        container.appendChild(wrap);
      });

      // 남은 달이 있으면 '더 보기'
      if (groups.length > shown.length) {
        var more = document.createElement('button');
        more.className = 'arc-more-btn';
        more.type = 'button';
        more.textContent = t('arc_more_btn') + ' (' + (groups.length - shown.length) + t('arc_month_unit') + ')';
        more.onclick = function () {
          arcVisibleMonths += MONTHS_PER_PAGE;
          renderArchiveByMonth(container, books);
        };
        container.appendChild(more);
      }
    }
    window.renderArchiveByMonth = renderArchiveByMonth;

    /* ── 도서 상세: 남은 기간 카드 ──────────────────────────────────────
       숫자만 크게 보여주면 'D-4'가 급한 건지 아닌지 감이 오지 않는다.
       전체 기간 중 얼마나 지났는지(진행 바)와 종료 예정일을 함께 보여준다.
       색 규칙은 홈 카드와 동일하게 맞춘다(D-7 이상 초록 / D-6~3 주황 / D-2 이하 빨강). */
    var DEFAULT_ROOM_DAYS = 10;

    /* ── 진행 중 통계 표시 ────────────────────────────────────────────────
       진행 중에는:
         · 반응 집계 → 한 줄로 공개 (채팅에서 이미 메시지별로 보이던 값이라 가릴 이유가 없다)
         · 평균 평점 → 접어서 봉인 (진행 중 평균이 보이면 서로의 점수에 끌려간다)
       종료 후에는 기존 통계 패널을 그대로 펼친다. */
    function renderLiveStats(book) {
      var section = document.querySelector('#pg-detail .stats-section');
      var inner = document.querySelector('#pg-detail .stats-inner');
      if (!section || !inner) return;

      // 이전 렌더에서 만든 진행 중 전용 요소를 정리
      var oldLine = document.getElementById('dc-rx-inline');
      if (oldLine) oldLine.remove();
      var oldFold = document.getElementById('dc-stats-folded');
      if (oldFold) oldFold.remove();

      if (book.archived) {
        inner.style.display = '';          // 종료 후에는 전체 통계를 그대로 보여준다
        return;
      }

      inner.style.display = 'none';

      // ① 반응 집계 한 줄
      var totals = getRxTotals(book);
      var sum = RX_ORDER.reduce(function (acc, r) { return acc + (totals[r.emoji] || 0); }, 0);
      var line = document.createElement('div');
      line.className = 'rx-inline' + (sum > 0 ? '' : ' empty');
      line.id = 'dc-rx-inline';

      var html = '<span class="rx-inline-lbl">' + t('detail_rx_live_label') + '</span>';
      if (sum > 0) {
        RX_ORDER.forEach(function (r) {
          var n = totals[r.emoji] || 0;
          if (n > 0) html += '<span class="rx-inline-item">' + r.emoji + ' ' + n + '</span>';
        });
        html += '<span class="rx-inline-live">' + t('detail_rx_live_badge') + '</span>';
      } else {
        // 반응이 없을 때도 줄을 남긴다 — 자물쇠로 막아두는 것보다 초대 문구가 낫다
        html += '<span>' + t('detail_rx_empty') + '</span>' +
                '<button class="rx-inline-cta" onclick="openChat()">' + t('detail_rx_empty_cta') + '</button>';
      }
      line.innerHTML = html;
      section.appendChild(line);

      // ② 평점은 접힌 한 줄로
      var fold = document.createElement('div');
      fold.className = 'stats-folded';
      fold.id = 'dc-stats-folded';
      fold.innerHTML = '<span>' + t('detail_rating_folded') + '</span>' +
                       '<span class="stats-folded-caret">' + t('detail_rating_blind') + ' ▾</span>';
      section.appendChild(fold);
    }

    function renderDdayCard(book) {
      var card = document.getElementById('dc-dday-card');
      if (!card) return;
      var numEl = document.getElementById('dc-dday');
      var unitEl = document.getElementById('dc-dday-unit');
      var endEl = document.getElementById('dc-dday-end');
      var barEl = document.getElementById('dc-dday-bar');
      var capEl = document.getElementById('dc-dday-cap');

      if (book.archived) {
        card.className = 'dday-card ended';
        numEl.textContent = t('detail_ended_label');
        unitEl.textContent = '';
        endEl.textContent = book.archivedDate || '';
        barEl.style.width = '100%';
        capEl.textContent = t('detail_ended_cap');
        return;
      }

      var days = book.deadlineDays != null ? book.deadlineDays : DEFAULT_ROOM_DAYS;
      var total = DEFAULT_ROOM_DAYS;
      // 상시 활성 독서방(deadline_days=9999)은 진행률을 계산하지 않는다
      var perpetual = days > 365;
      var passed = perpetual ? 0 : Math.max(0, Math.min(total, total - days));

      card.className = 'dday-card ' + (perpetual ? 'active' : days <= 2 ? 'urgent' : days <= 6 ? 'soon' : 'active');
      numEl.textContent = perpetual ? t('detail_always_open') : (days === 0 ? 'D-DAY' : 'D-' + days);
      unitEl.textContent = perpetual ? '' : t('detail_days_left');
      endEl.textContent = perpetual ? '' : formatEndDate(days);
      barEl.style.width = perpetual ? '0%' : Math.round(passed / total * 100) + '%';

      // 남은 기간에 따라 안내 문구를 바꿔, 마감이 압박이 아니라 참여 이유가 되게 한다
      if (perpetual) {
        capEl.textContent = t('detail_cap_always');
      } else if (days <= 1) {
        capEl.textContent = t('detail_cap_last');
      } else if (days <= 6) {
        capEl.textContent = t('detail_cap_soon_a') + total + t('detail_cap_soon_b') + passed + t('detail_cap_soon_c');
      } else {
        capEl.textContent = t('detail_cap_early');
      }
    }

    // 남은 일수로 종료 예정일을 만든다 (M월 D일)
    function formatEndDate(days) {
      var d = new Date();
      d.setDate(d.getDate() + days);
      return CURRENT_LANG === 'ja'
        ? (d.getMonth() + 1) + '月' + d.getDate() + '日' + t('detail_end_suffix')
        : (d.getMonth() + 1) + '월 ' + d.getDate() + '일' + t('detail_end_suffix');
    }

    /* 가상 판권면 접기/펼치기 */
    function toggleColophon() {
      var body = document.getElementById('dc-colophon-body');
      var caret = document.getElementById('dc-colophon-caret');
      if (!body) return;
      body.hidden = !body.hidden;
      if (caret) caret.textContent = body.hidden ? '▾' : '▴';
    }
    window.toggleColophon = toggleColophon;

    function ensureArchivedSampleData(book) {
      if (!book) return;
      if (book.archived) {
        var r = book.ratings || { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
        var rTotal = (r[5]||0) + (r[4]||0) + (r[3]||0) + (r[2]||0) + (r[1]||0);
        if (rTotal === 0) {
          var seed = ((book.id || 1) * 17) % 5;
          if (seed === 0) book.ratings = { 5: 22, 4: 11, 3: 3, 2: 1, 1: 0 };
          else if (seed === 1) book.ratings = { 5: 18, 4: 14, 3: 4, 2: 0, 1: 0 };
          else if (seed === 2) book.ratings = { 5: 25, 4: 8, 3: 2, 2: 1, 1: 0 };
          else if (seed === 3) book.ratings = { 5: 15, 4: 12, 3: 5, 2: 1, 1: 0 };
          else book.ratings = { 5: 20, 4: 10, 3: 3, 2: 0, 1: 0 };
        }
        
        var rx = book.rxCounts || { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 };
        var rxTotal = (rx['❤️']||0) + (rx['🤔']||0) + (rx['😄']||0) + (rx['✨']||0);
        if (rxTotal === 0) {
          var seed2 = ((book.id || 1) * 13) % 4;
          if (seed2 === 0) book.rxCounts = { '❤️': 45, '🤔': 14, '😄': 28, '✨': 38 };
          else if (seed2 === 1) book.rxCounts = { '❤️': 38, '🤔': 10, '😄': 21, '✨': 31 };
          else if (seed2 === 2) book.rxCounts = { '❤️': 52, '🤔': 16, '😄': 30, '✨': 42 };
          else book.rxCounts = { '❤️': 40, '🤔': 12, '😄': 25, '✨': 34 };
        }
      }
    }
    window.ensureArchivedSampleData = ensureArchivedSampleData;

    function getSampleChatSeeds(book) {
      var title = book.title || t('fallback_book_title', '가공 도서');
      var author = book.author || t('fallback_book_author', '가상 작가');
      var dateStr = book.archivedDate || '2026-06-02';

      if (title.indexOf('안개 낀 등대') !== -1) {
        return [
          { user: "등대지기", text: "안개 낀 등대의 학술 사기극에 관한 사립대 교수들의 우스꽝스러운 기면증 풍자가 너무 신선했어요!", ts:"오후 07:15", date: dateStr + 'T19:15:00', reactions: {"": 14,"": 8 } },
          { user: "풍자소설덕후", text: "맞아요! 2장에서 보좌관이 등대 불빛을 켰다 껐다 하면서 교수들의 가식을 야유하는 씬에서 빵 터졌습니다", ts:"오후 07:22", date: dateStr + 'T19:22:00', replyTo: { user:"등대지기", text: "안개 낀 등대의 학술 사기극..." }, reactions: {"": 18,"": 10 } },
          { user: "🎙️ AI 사회자", text: "독자님들의 유쾌한 사색에 감명받았습니다. 서채원 작가가 안개 낀 등대를 통해 풍자하려 했던 상아탑의 위선과 현대 사회의 진실에 대해 어떻게 보시나요?", ts:"오후 07:30", date: dateStr + 'T19:30:00', reactions: {"": 22 } },
          { user: "상아탑사색가", text: "가식 뒤에 숨겨진 기면증이라는 비유가 날카롭게 박혔어요. 3장 결말에서 등대 불빛이 안개를 찢을 때 울컥했습니다.", ts:"오후 07:42", date: dateStr + 'T19:42:00', replyTo: { user:" AI 사회자", text: "독자님들의 유쾌한 사색에..." }, reactions: {"": 16,"": 7 } },
          { user: "밤의독서가", text: "풍자소설이면서도 해학이 느껴지는 명작이었어요. 아카이브로 남아서 소중하게 곱씹겠습니다.", ts:"오후 08:05", date: dateStr + 'T20:05:00', reactions: {"": 20,"": 15 } }
        ];
      } else if (title.indexOf('그림자를 녹이는') !== -1) {
        return [
          { user: "그림자조각가", text: "셀레나가 만년필로 그린 그림자가 흑백 잉크처럼 흩어지며 현실의 벽을 서서히 해체시키는 1장 장면에서 손끝이 덜덜 떨렸어요!", ts:"오전 11:20", date: dateStr + 'T11:20:00', reactions: {"": 18,"": 12 } },
          { user: "만년필의향기", text: "펜촉 끝에서 감도는 바이올렛 잉크 향과 서늘한 민트 향 묘사가 문장 너머로 느껴지는 듯해서 가슴이 덜컥 내려앉았습니다.", ts:"오후 04:45", date: dateStr + 'T16:45:00', reactions: {"": 21 } },
          { user: "🎙️ AI 사회자", text: "깊은 사색이 담긴 인상적인 문장을 짚어주셨군요. 셀레나에게 만년필은 존재의 소중함을 다시 일깨우는 따스한 찰나의 매개였습니다.", ts:"오후 05:10", date: dateStr + 'T17:10:00', reactions: {"": 25 } },
          { user: "사색의시간", text: "'사라지는 것들의 아름다움은, 영원히 머무는 것들보다 더 깊은 여운을 남긴다' ... 이 구절이 오랫동안 마음에 남을 것 같아요.", ts:"오후 08:50", date: dateStr + 'T20:50:00', reactions: {"": 30,"": 20 } }
        ];
      } else if (title.indexOf('닳아버린 시선') !== -1) {
        return [
          { user: "운명연구원", text: "골목 안경점의 한지우 할아버지가 낡은 안경을 통해 손님들의 서늘한 운명의 파편을 마주하는 1장 도입부부터 문체가 참 고혹적이네요", ts:"오전 09:30", date: dateStr + 'T09:30:00', reactions: {"": 15,"": 10 } },
          { user: "단안경사서", text: "타인의 미래를 아는 것이 축복이 아니라 거대한 죄책감의 짐이 되는 장면에서 가슴이 덜컥 내려앉았습니다.", ts:"오후 01:10", date: dateStr + 'T13:10:00', reactions: {"": 12,"": 14 } },
          { user: "🎙️ AI 사회자", text: "지우 할아버지에게 닳아버린 시선은 육신의 쇠퇴가 아니라, 타인의 상처와 죄책감을 온전히 안아낸 숭고한 사랑의 증표였습니다.", ts:"오후 02:45", date: dateStr + 'T14:45:00', reactions: {"": 28 } },
          { user: "빛나는궤적", text: "타인의 운명을 지우려 애쓸수록 나의 시선은 닳아버렸다는 절절한 마지막 문장에 눈시울이 적셔졌네요", ts:"오후 04:10", date: dateStr + 'T16:10:00', reactions: {"": 25,"": 18 } }
        ];
      } else if (title.indexOf('깨진 렌즈') !== -1) {
        return [
          { user: "바다의항해자", text: "지도 제작자 테오가 낡고 깨진 단안경을 닦을 때마다 렌즈 너머로 보이지 않는 운명의 해도가 그려지는 1장 도입부부터 몰입감이 대단하네요!", ts:"오전 10:15", date: dateStr + 'T10:15:00', reactions: {"": 16,"": 11 } },
          { user: "단안경사색가", text: "렌즈에 금이 간 이유가 과거 거대한 폭풍우를 경고하다 깨진 것이란 비하인드를 읽고 소름 돋았습니다.", ts:"오후 02:20", date: dateStr + 'T14:20:00', reactions: {"": 9,"": 15 } },
          { user: "🎙️ AI 사회자", text: "테오에게 깨진 단안경은 과거의 상처를 들추는 아픔이 아니라, 잊혀진 사람들의 소망을 현실의 평화로 엮어내는 숭고한 창조의 계기였습니다.", ts:"오후 03:00", date: dateStr + 'T15:00:00', reactions: {"": 24 } },
          { user: "항해사김민준", text: "'바다는 모든 것을 씻어내어 기억하지 않아도, 나의 해도는 끝내 너의 궤적을 기억한다' ... 최고의 3장이었습니다.", ts:"오후 04:05", date: dateStr + 'T16:05:00', reactions: {"": 28,"": 22 } }
        ];
      } else if (title.indexOf('오래된 안경 상점') !== -1) {
        return [
          { user: "달빛독자", text: "타인의 속마음을 비추는 안경을 닦을 때마다 나의 고독을 닦아내고 있었다는 문장이 가슴을 치네요...", ts:"오후 08:05", date: dateStr + 'T20:05:00', reactions: {"": 19,"": 14 } },
          { user: "새벽사서", text: "아델이 렌즈를 투영하며 마주한 진실과 갈망의 정원 씬이 환상적이면서도 씁쓸한 여운을 전하더군요.", ts:"오후 08:18", date: dateStr + 'T20:18:00', reactions: {"": 15,"": 8 } },
          { user: "🎙️ AI 사회자", text: "타인의 숨겨진 마음을 아는 안경이 있다면 독자님들은 쓰시겠습니까, 아니면 모르고 살아가시겠습니까?", ts:"오후 08:30", date: dateStr + 'T20:30:00', reactions: {"": 26 } },
          { user: "글꽃소녀", text: "저는 쓰지 않고 진실을 모른 채 평온하게 살고 싶어요! 3장 결말의 선택이 그래서 더 와닿았어요.", ts:"오후 08:45", date: dateStr + 'T20:45:00', replyTo: { user:" AI 사회자", text: "타인의 숨겨진 마음을..." }, reactions: {"": 22 } }
        ];
      } else {
        return [
          { user: "독서가", text: "『" + title +"』을 읽으며" + author +" 작가가 그려낸 가상의 활자 속에 깊이 빠져들었습니다.", ts:"오후 02:15", date: dateStr + 'T14:15:00', reactions: {"": 12,"": 8 } },
          { user: "사색자", text: "중반부 시놉시스의 딜레마가 마음에 큰 울림을 주더군요. 소장 가치가 높은 훌륭한 작품입니다.", ts:"오후 02:30", date: dateStr + 'T14:30:00', reactions: {"": 14,"": 9 } },
          { user: "🎙️ AI 사회자", text: "독자님들의 깊은 감상에 감사드립니다. 『" + title +"』이 남긴 사유의 궤적을 자유롭게 나눠보세요.", ts:"오후 02:45", date: dateStr + 'T14:45:00', reactions: {"": 18 } },
          { user: "여백의문장", text: "가공독서회에서 나누었던 3일간의 사색과 이야기를 오래도록 소중히 기억하겠습니다.", ts:"오후 03:20", date: dateStr + 'T15:20:00', reactions: {"": 20,"": 16 } }
        ];
      }
    }
    window.getSampleChatSeeds = getSampleChatSeeds;


function renderGenreSection() {
      var tabsEl = document.getElementById('genre-tabs');
      if (!tabsEl) return;
      var activeBooks = BOOKS.filter(function (b) { return !b.archived; });
      var archivedBooks = BOOKS.filter(function (b) { return b.archived; });

      if (typeof currentGenre !== 'undefined' && currentGenre !== '전체' && currentGenre !== '아카이브') {
        if (!activeBooks.some(function(b) { return b.genre === currentGenre; })) {
          currentGenre = '전체';
        }
      }

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
        btn.textContent = translateGenre(g);
        if (isArc) btn.innerHTML = t('arc_tab');
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
        // 종료된 독서방은 '월별 서가'로 묶어서 보여준다
        renderArchiveByMonth(grid, archivedBooks);

        // 마감 임박 섹션은 아카이브 탭에서 숨긴다
        var dlSection = document.querySelector('#pg-home .home-section:last-child');
        if (dlSection) dlSection.style.display = 'none';

        var metaEl = document.getElementById('genre-meta');
        if (metaEl) metaEl.innerHTML = '<span style="color:#4a7a3a">' + t('archive_badge') + '</span> <span id="genre-count">' + archivedBooks.length + '</span>' + t('count_unit');
      } else {
        // 아카이브 탭에서 돌아오면 그리드 레이아웃을 원래대로 되돌린다
        grid.className = 'cards-grid';
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
            '<div class="card-cover" style="' + getCoverCss(b) + '">' +
            '<div class="card-spine"></div>' +
            '<span>' + escHtml(b.title) + '</span>' +
            '</div>' +
            '<div class="card-body">' +
            '<span class="card-genre">' + escHtml(translateGenre(b.genre)) + '</span>' +
            '<div class="card-title">' + escHtml(b.title) + '</div>' +
            '<div class="card-synopsis">' + escHtml(b.synopsis) + '</div>' +
            '<div class="card-footer">' +
            '<span class="card-price">' + escHtml(b.price) + '</span>' +
            '<span class="card-count">👥 ' + b.count + t('people_unit') + '</span>' +
            '</div>' +
            '</div>';
          grid.appendChild(el);
        });

        var metaEl = document.getElementById('genre-meta');
        if (metaEl) metaEl.innerHTML = (currentGenre === '전체' ? t('genre_all') + ' ' : '<span style="color:var(--accent)">' + escHtml(translateGenre(currentGenre)) + '</span> ') + '<span id="genre-count">' + filtered.length + '</span>' + t('count_unit');
      }
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
          '<div class="deadline-lbl">' + t('days_left') + '</div>' +
          '</div>' +
          '<div class="deadline-mini-cover" style="' + getCoverCss(b) + '">' +
          '<div class="deadline-mini-spine"></div>' +
          '</div>' +
          '<div class="deadline-info">' +
          '<div class="deadline-genre">' + escHtml(translateGenre(b.genre)) + '</div>' +
          '<div class="deadline-title">' + escHtml(b.title) + '</div>' +
          '<div class="deadline-count' + (isUrgent ? ' deadline-urgent' : '') + '">' +
          (isUrgent ? t('closing_soon') : '') + '👥 ' + b.count + t('participants_joining') +
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

      var dcCov = document.getElementById('dc-cover'); if (dcCov) { dcCov.style.cssText = getCoverCss(book); }
      document.getElementById('dc-title-txt').textContent = book.title;
      document.getElementById('dc-genre').textContent = translateGenre(book.genre);
      document.getElementById('dc-title').textContent = book.title;
      document.getElementById('dc-author').textContent = book.author;
      document.getElementById('dc-detail-count').textContent = '👥 ' + book.count + t('people_unit');
      document.getElementById('dc-synopsis').textContent = book.synopsis;
      var pcEl = document.getElementById('dc-page-count');
      if (pcEl) pcEl.textContent = (book.pageCount || 300) + t('page_unit');
      document.getElementById('dc-price').textContent = book.price + t('discount_note');
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
              p.innerHTML = '<strong style="color:#b54a6a; margin-right:6px;">' + escHtml(parts[0].trim()) + '</strong>' + escHtml(parts.slice(1).join('—').trim());
            } else {
              p.textContent = c;
            }
            charEl.appendChild(p);
          });
        } else {
          charEl.textContent = t('detail_no_characters');
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
      var mainBtn = document.getElementById('dc-main-btn');
      var wishBtn = document.getElementById('dc-wish-btn');
      var chatHistoryBtn = document.getElementById('dc-chat-history-btn');

      // 남은 기간 카드는 활성/아카이브 상태를 모두 처리한다
      renderDdayCard(book);
      // 진행 중에는 반응만 공개하고 평점은 접는다
      renderLiveStats(book);

      if (book.archived) {
        /* ── 아카이브 모드 ── */

        // 종료 안내는 남은 기간 카드(renderDdayCard)가 '종료됨 · 날짜 · 보관 중'으로 이미 표시한다.
        // 별도 배너를 두면 같은 문장이 두 번 나오므로 두지 않는다.

        // 버튼 전환
        if (mainBtn) {
          mainBtn.textContent = t('archive_open_btn');
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
            wishBtn.innerHTML = t('remove_lib_btn');
            wishBtn.onclick = function() { removeFromLib(book.id); };
          } else {
            wishBtn.innerHTML = t('add_lib_btn');
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

        // 반응 총합은 서버(rx_counts)가 이미 계산해 준 값을 그대로 쓴다.
        // getRxTotals()가 채팅 캐시와 비교해 더 큰 쪽을 취하므로 여기서 재집계할 필요가 없다.

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
        // 버튼 복원
        if (mainBtn) {
          mainBtn.textContent = t('join_chat_btn');
          mainBtn.style.cssText = '';
          mainBtn.onclick = function() { openChat(); };
        }
        if (chatHistoryBtn) {
          chatHistoryBtn.style.display = 'none';
        }
        if (wishBtn) {
          wishBtn.style.display = '';
          if (libBooks.some(function (b) { return b.id == book.id; })) {
            wishBtn.innerHTML = t('remove_lib_btn');
            wishBtn.onclick = function() { removeFromLib(book.id); };
          } else {
            wishBtn.innerHTML = t('add_lib_btn');
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
          delBtn.style.display = 'inline-block'; delBtn.textContent = t('delete_btn');
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
        card.style.cssText = 'background:#ffffff; border:1px solid #ebd9b5; border-radius:10px; padding:16px 20px; display:flex; flex-direction:column; gap:10px; box-shadow:0 2px 8px rgba(0,0,0,0.02);';

        var headerRow = document.createElement('div');
        headerRow.style.cssText = 'display:flex; align-items:center; justify-content:space-between; width:100%;';
        headerRow.innerHTML =
          '<div style="display:flex; align-items:center; gap:8px;">' +
          '<span style="font-size:13px; font-weight:700; color:#8b4f25; background:#f5e8cf; padding:3px 9px; border-radius:5px;">' + escHtml(r.rank) + '</span>' +
          '<strong style="font-size:14.5px; color:#2c2418; font-weight:700;">' + escHtml(r.nickname) + ' 독자님</strong>' +
          '</div>' +
          '<span style="font-size:13px; color:#a36b1d; font-weight:600;">' + escHtml(r.reactions) + '</span>';

        var commentBody = document.createElement('div');
        commentBody.style.cssText = 'font-size:15px; color:#1a1714; line-height:1.7; font-weight:450; letter-spacing:-0.01em;';
        commentBody.textContent = '“' + r.comment + '”';

        card.appendChild(headerRow);
        card.appendChild(commentBody);

        if (r.authorReply) {
          var replyBox = document.createElement('div');
          replyBox.style.cssText = 'margin-top:4px; padding:10px 14px; background:#faf6ee; border-radius:8px; border-left:3.5px solid #a36b1d; font-size:13.5px; color:#4a361e; line-height:1.6;';
          replyBox.innerHTML = t('detail_ai_author_reply') + escHtml(r.authorReply);
          card.appendChild(replyBox);
        }

        listEl.appendChild(card);
      });

      section.style.display = 'block';
    }
    // 관리자 도서 삭제 처리 함수
    async function deleteBook() {
      if (!currentBook) return;
      if (!confirm(t('confirm_delete_book') + '\n' + t('confirm_delete_book_sub'))) {
        return;
      }
      var token = localStorage.getItem('token');
      if (!token) {
        alert(t('toast_session_expired'));
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
          alert(t('alert_book_deleted'));
          goPage('home');
          await fetchActiveBooks();
        } else {
          var errData = await res.json();
          alert(errData.detail || t('alert_book_delete_failed'));
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
      // book.rxCounts는 서버가 DB 전체를 집계해 내려준 값이므로 그것을 기준으로 쓴다.
      // 채팅방을 열어 둔 동안의 즉시 반응(서버 집계 이후 생긴 변화)만
      // 채팅 캐시가 더 큰 경우에 한해 반영해 이중 계산을 피한다.
      var totals = {};
      RX_ORDER.forEach(function (r) { totals[r.emoji] = (book.rxCounts || {})[r.emoji] || 0; });

      var live = {};
      var msgs = chatMsgs[book.id] || [];
      msgs.forEach(function (m) {
        Object.keys(m.reactions || {}).forEach(function (emoji) {
          // reactions 값은 정수 카운트 (예: {"❤️": 3}) — .count 접근 제거
          if (totals[emoji] !== undefined) live[emoji] = (live[emoji] || 0) + (m.reactions[emoji] || 0);
        });
      });
      Object.keys(live).forEach(function (emoji) {
        if (live[emoji] > totals[emoji]) totals[emoji] = live[emoji];
      });
      return totals;
    }

    function renderStats(book) {
      ensureArchivedSampleData(book);
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
        starsEl.innerHTML = '<span style="font-size:12px;color:var(--text-faint)">' + t('detail_rating_blind') + '</span>';
        barsEl.innerHTML = '';
        var blindRow = document.createElement('div');
        blindRow.className = 'stats-bar-row';
        blindRow.style.justifyContent = 'center';
        blindRow.style.padding = '20px 0';
        blindRow.innerHTML = '<span style="font-size:12px;color:var(--text-muted)">' + t('detail_rating_blind_desc') + '</span>';
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
          t('detail_rating_locked') +
          ' <button class="stats-my-join-btn" onclick="openChat()">' + t('detail_join_short') + '</button>' +
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
          '<span style="font-size:12px;color:var(--text-muted)">' + t('detail_rx_blind_desc') + '</span>' +
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
          '<div style="margin-left:auto;font-size:11px;color:var(--text-muted)">' + t('detail_rx_top') + '</div>';
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

    function renderCandidates(candidates) {
      var container = document.getElementById('candidates-container');
      if (!container) return;
      container.innerHTML = '';
      candidates.forEach(function(c) {
        var card = document.createElement('div');
        card.className = 'candidate-card';
        card.innerHTML = 
          '<div class="card-cover" id="cand-cover-' + c.id + '" style="' + getCoverCss(c) + '">' + escHtml(c.title) + '</div>' +
          '<div class="card-body">' +
            '<span class="card-genre">' + escHtml(c.genre) + '</span>' +
            '<div class="card-title">' + escHtml(c.title) + '</div>' +
            '<div class="card-author">' + escHtml(c.author) + '</div>' +
            '<div class="card-synopsis">' + escHtml(c.synopsis) + '</div>' +
            '<div style="margin-top:auto"><button class="btn-adopt" onclick="adoptCandidate(' + c.id + ')">이 책으로 독서방 열기</button></div>' +
          '</div>';
        container.appendChild(card);

        // 표지 아직 없으면 백그라운드 생성 완료까지 폴링
        if (!c.cover_image_url) {
          pollCandidateCover(c.id, c.color);
        }
      });
    }

    function pollCandidateCover(candId, fallbackColor, attempt) {
      attempt = attempt || 0;
      if (attempt > 20) return; // 최대 ~60초 폴링 후 포기
      setTimeout(async function() {
        try {
          var res = await fetch('/api/books/candidates/' + candId + '/cover');
          if (res.ok) {
            var data = await res.json();
            if (data.cover_image_url) {
              var coverEl = document.getElementById('cand-cover-' + candId);
              if (coverEl) {
                coverEl.style.cssText = getCoverCss({ cover_image_url: data.cover_image_url, color: fallbackColor });
              }
              return; // 표지 적용 완료
            }
          }
        } catch (e) { /* 무시 */ }
        pollCandidateCover(candId, fallbackColor, attempt + 1);
      }, 3000);
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
        showToast(star + t('toast_rating_done'));
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
        showToast(t('toast_already_lib'));
        return;
      }
      libBooks.push(currentBook);
      renderLib();
      showToast(t('toast_added_lib'));
      var wishBtn = document.getElementById('dc-wish-btn');
      if (wishBtn) {
        wishBtn.innerHTML = t('remove_lib_btn');
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
        showToast(t('toast_login_for_lib'));
      }
    }
    function removeFromLib(bookId) {
      var idx = libBooks.findIndex(function (b) { return b.id == bookId; });
      if (idx !== -1) {
        libBooks.splice(idx, 1);
        renderLib();
        showToast(t('toast_removed_lib'));
        if (currentBook && currentBook.id === bookId) {
          var wishBtn = document.getElementById('dc-wish-btn');
          if (wishBtn) {
            wishBtn.innerHTML = t('add_lib_btn');
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
        row.innerHTML = '<div style="font-size:13px;color:var(--text-faint);padding:20px 0;">' + t('lib_empty_saved') + '</div>';
      } else {
        row.innerHTML = '';
        var heights = [90, 110, 100, 85, 105, 95, 115, 88];
        libBooks.forEach(function (b, i) {
          var h = heights[i % heights.length];
          var el = document.createElement('div');
          el.className = 'book-spine';
          el.id = 'lb-' + b.id;
          el.style.cssText = 'height:' + h + 'px;background:' + b.color + ';';
          el.innerHTML = '<div class="book-spine-txt">' + escHtml(b.title) + '</div>';
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
        myRow.innerHTML = '<div style="font-size:13px;color:var(--text-faint);padding:20px 0;">' + t('lib_empty_writings') + '</div>';
      } else {
        myRow.innerHTML = '';
        var heights = [90, 110, 100, 85, 105, 95, 115, 88];
        myCommentedBooks.forEach(function (b, i) {
          var h = heights[i % heights.length];
          var el = document.createElement('div');
          el.className = 'book-spine';
          el.id = 'mycmt-' + b.id;
          el.style.cssText = 'height:' + h + 'px;background:' + b.color + ';';
          el.innerHTML = '<div class="book-spine-txt">' + escHtml(b.title) + '</div>';
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
        writingsEl.innerHTML = '<div class="bdp-empty">' + t('lib_no_writings') + '</div>';
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
      document.getElementById('lib-bdp-sub').textContent = translateGenre(book.genre) + t('detail_virtual_book');
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

    // 아직 고르지 않은 후보를 서버에서 가져온다. 없으면 빈 배열.
    async function fetchPendingCandidates(token) {
      try {
        var res = await fetch('/api/books/candidates/pending', {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) return [];
        var list = await res.json();
        return Array.isArray(list) ? list : [];
      } catch (err) {
        return [];
      }
    }

    async function generateBook() {
      // 1. 로그인 여부 검증 (로그인한 사용자만 새 책 생성 가능)
      var token = localStorage.getItem('token');
      if (!token) {
        alert(t('alert_login_to_gen'));
        goPage('auth-gate');
        return;
      }

      var btn = document.getElementById('gen-btn');
      if (btn) btn.disabled = true;
      document.getElementById('loading').style.display = 'flex';
      try {
        // 2. 고르지 않고 남겨둔 후보가 있으면 새로 만들지 않고 그 화면으로 되돌아간다.
        //    (하루 1회 제한을 소모하지 않고, '아직 안 고른 상태'를 그대로 유지한다)
        var pending = await fetchPendingCandidates(token);
        if (pending.length) {
          renderCandidates(pending);
          goPage('candidates');
          showToast(t('toast_pending_restored'));
          return;
        }

        var res = await fetch('/api/books/candidates', {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
          var candidates = await res.json();
          renderCandidates(candidates);
          goPage('candidates');
        } else {
          var errData = await res.json();
          alert(errData.detail || t('alert_gen_failed'));
        }
      } catch (err) {
        console.error(err);
        alert(t('alert_server_error'));
      } finally {
        if (btn) btn.disabled = false;
        document.getElementById('loading').style.display = 'none';
      }
    }
    window.generateBook = generateBook;

    // 후보 선택 화면으로 직접 이동했을 때(뒤로가기 등) 비어 있으면 서버에서 복원한다.
    async function restoreCandidatesIfEmpty() {
      var container = document.getElementById('candidates-container');
      var token = localStorage.getItem('token');
      if (!container || !token || container.querySelector('.candidate-card')) return;
      var pending = await fetchPendingCandidates(token);
      if (pending.length) renderCandidates(pending);
    }
    window.restoreCandidatesIfEmpty = restoreCandidatesIfEmpty;

    async function adoptCandidate(candidateId) {
      var token = localStorage.getItem('token');
      if (!token) {
        showToast(t('toast_login_required'));
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
          showToast(t('toast_new_book_prefix') + '"' + newAdapted.title + '"' + t('toast_book_created'));
          renderHome();
          openDetail(newAdapted.id);
        } else {
          var errData = await res.json();
          alert(errData.detail || t('alert_adopt_failed'));
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
      { user: '달빛독자', av: '달', avBg: '#e8daf8', avColor: '#7b5fb8', text: '저 이거 읽으면서 지하철에서 울 뻔 했어요 참느라 혼났잖아요' },
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
        showToast(t('toast_session_expired'));
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

      document.getElementById('chat-room-title').textContent = book.title + t('chat_room_suffix');
      // 백엔드에서 정확하게 집계된 participant_count(book.count)를 신뢰할 수 있는 출처로 사용
      document.getElementById('chat-room-meta').textContent = book.count + t('participants_joining');
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
        if (body) body.scrollTop = body.scrollHeight;
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'auto' });
      }, 100);
    }

    function scrollChatToTop() {
      var body = document.getElementById('chat-body');
      if (body) body.scrollTo({ top: 0, behavior: 'smooth' });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    function scrollChatToBottom() {
      var body = document.getElementById('chat-body');
      if (body) body.scrollTo({ top: body.scrollHeight, behavior: 'smooth' });
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
    function focusChatInput() {
      scrollChatToBottom();
      var inp = document.getElementById('chat-input');
      if (inp) {
        inp.focus();
      }
    }
    window.scrollChatToTop = scrollChatToTop;
    window.scrollChatToBottom = scrollChatToBottom;
    window.focusChatInput = focusChatInput;

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
      body.appendChild(makeDivider(t('chat_open_date')));
      body.appendChild(makeNotice(t('chat_room_opened')));

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
      // 배경색은 styles.css의 .chat-notice 규칙이 담당한다.
      // (예전에는 여기 인라인 스타일이 박혀 있어 CSS를 덮어썼고, 크림색 배경에서 탁한 회색으로 보였다)
      d.innerHTML = '<span>' + escHtml(label) + '</span>';
      return d;
    }
    function makeNotice(text) {
      var d = document.createElement('div');
      d.className = 'chat-notice';
      d.innerHTML = '<span>' + escHtml(text) + '</span>';
      return d;
    }
    function makeDateDivider(date) {
      var d = document.createElement('div');
      d.className = 'chat-date-divider';
      d.innerHTML = '<span>' + dateLabel(date) + '</span>';
      return d;
    }

    
    function formatMsgText(text) {
      if (!text) return '';
      var escaped = escHtml(text);
      return escaped.replace(/@([가-힣a-zA-Z0-9_]+)/g, function(match, name) {
        var isModTag = (name === '사회자' || name.indexOf('사회자') === 0 || name === 'moderator' || name === 'AI사회자' || name.indexOf('AI사회자') === 0);
        var style = isModTag 
          ? 'background:#fef3c7;color:#b45309;border:1px solid #fde68a;font-weight:700;padding:1px 6px;border-radius:4px;display:inline-block;margin:0 2px;'
          : 'background:#e0f2fe;color:#0369a1;border:1px solid #bae6fd;font-weight:600;padding:1px 6px;border-radius:4px;display:inline-block;margin:0 2px;';
        return '<span class="mention-tag" style="' + style + '">' + match + '</span>';
      });
    }
    window.formatMsgText = formatMsgText;


function buildMsgEl(msg, bookId) {
      var row = document.createElement('div');
      // 서버가 내려주는 isBot 플래그로 판별한다.
      // (예전에는 닉네임에 '사회자'가 들어있는지로 판단해서, 그 닉네임으로 가입하면 공식 계정처럼 보였다)
      var isMod = !!msg.isBot;
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

      var rxParts = !isMod ? rxHtml_parts(msg, bookId) : '';
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
      var dblClickAttr = isMod ? '' : (msg.mine ? ' ondblclick="showMsgMenu(\'' + bookId + '\',\'' + msg.id + '\',event)"' : ' ondblclick="showRxPicker(\'' + bookId + '\',\'' + msg.id + '\',event)"');
      var bubbleHtml = '<div class="chat-bubble" id="bubble-' + msg.id + '"' + dblClickAttr + '>' +
        replyQuote +
        formatMsgText(msg.text) + editedTag +
        '</div>';

      var actionToolbar = '';
      if (msg.mine) {
        actionToolbar = '<div class="chat-action-toolbar mine">' +
          '<button class="chat-action-btn" onclick="startEdit(\'' + bookId + '\',\'' + msg.id + '\')">수정</button>' +
          '<span class="chat-action-divider">|</span>' +
          '<button class="chat-action-btn danger" onclick="deleteMsg(\'' + bookId + '\',\'' + msg.id + '\')">삭제</button>' +
          '</div>';
      } else if (!isMod) {
        actionToolbar = '<div class="chat-action-toolbar other">' +
          '<button class="chat-action-btn" onclick="startReplyById(\'' + bookId + '\',\'' + msg.id + '\')">↩ 답장</button>' +
          '<span class="chat-action-divider">|</span>' +
          '<button class="chat-action-btn" onclick="showRxPicker(\'' + bookId + '\',\'' + msg.id + '\',event)">❤️ 반응</button>' +
          '</div>';
      }
      if (msg.mine) {
        row.innerHTML =
          '<div class="chat-time-wrap"><span class="chat-time">' + escHtml(msg.ts) + '</span></div>' +
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
          avHtml = '<div class="chat-av" style="background:' + msg.avBg + ';color:' + msg.avColor + '">' + escHtml(msg.av || '') + '</div>';
        }
        row.innerHTML =
          avHtml +
          '<div class="chat-col" id="col-' + msg.id + '">' +
          '<div class="chat-name' + (isMod ? ' mod-name' : '') + '">' + escHtml(msg.user || '') + '</div>' +
          bubbleHtml +
          actionToolbar +
          rxBlock +
          '</div>' +
          '<div class="chat-time-wrap"><span class="chat-time">' + escHtml(msg.ts) + '</span></div>';
      }
      return row;
    }

    // HTML 삽입용 이스케이프. 서버/AI/다른 사용자에게서 온 모든 문자열은
    // innerHTML로 들어가기 전에 반드시 이 함수를 통과해야 한다.
    // 속성값 자리(style="...", title="..." 등)에서도 안전하도록 따옴표까지 처리한다.
    function escHtml(s) {
      if (s === null || s === undefined) return '';
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
    window.escHtml = escHtml;

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
      if (!newText) { showToast(t('toast_input_empty')); return; }

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
      showToast(t('toast_edited'));
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
            if (!wasAuthErr) showToast(t('toast_edit_failed'));
          } else {
            console.log('채팅 DB 수정 성공:', msg.id);
          }
        }).catch(function(err) {
          console.error('채팅 수정 API 에러:', err);
          rollbackEdit();
          showToast(t('toast_network_error'));
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
      showToast(t('toast_deleted'));
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
            if (!wasAuthErr) showToast(t('toast_delete_failed'));
          } else {
            console.log('채팅 DB 삭제 성공:', msg.id);
          }
        }).catch(function(err) {
          console.error('채팅 삭제 API 에러:', err);
          rollbackDelete();
          showToast(t('toast_network_error'));
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
            if (!wasAuthErr) showToast(t('toast_send_failed'));
            var oldRow = document.getElementById('chatrow-' + oldId);
            if (oldRow) oldRow.remove();
            var idx = msgs.indexOf(msg);
            if (idx !== -1) msgs.splice(idx, 1);
          }
        }).catch(function (e) {
          console.error('채팅 전송 API 에러:', e);
          showToast(t('toast_network_error'));
          var oldRow = document.getElementById('chatrow-' + oldId);
          if (oldRow) oldRow.remove();
          var idx = msgs.indexOf(msg);
          if (idx !== -1) msgs.splice(idx, 1);
        });
      }
    }

    function showRxPicker(bookId, msgId, e) {
      if (e) e.stopPropagation();
      var msgs = chatMsgs[bookId] || [];
      var msg = msgs.find(function(m) { return m.id == msgId; });
      if (msg && msg.isBot) {
        return;
      }
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
      document.getElementById('reply-preview-name').textContent = '↩ ' + msg.user + t('chat_reply_writing');
      document.getElementById('reply-preview-text').textContent = msg.text;
      bar.classList.add('show');

      // 입력창 포커스 및 placeholder 변경
      var inp = document.getElementById('chat-input');
      if (inp) {
        inp.placeholder = msg.user + t('chat_reply_placeholder');
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
        inp.placeholder = t('chat_default_placeholder');
      }
    }
    function toggleChatRx(bookId, msgId, emoji) {
      var msgs = chatMsgs[bookId];
      if (!msgs) return;
      var msg = msgs.find(function (m) { return m.id == msgId; });
      if (!msg) return;
      if (msg.mine) {
        showToast(t('toast_no_self_rx'));
        return;
      }
      var token = localStorage.getItem('token');
      if (!token) {
        showToast(t('toast_login_for_rx'));
        return;
      }

      if (!msg.reactions[emoji]) msg.reactions[emoji] = { count: 0, mine: false };
      var r = msg.reactions[emoji];
      var wasMine = r.mine;
      var prevCount = r.count;
      var adding = !wasMine;
      if (wasMine) { r.mine = false; r.count = Math.max(0, r.count - 1); }
      else { r.mine = true; r.count++; }
      if (r.count === 0) delete msg.reactions[emoji];

      // re-render just this row (낙관적 업데이트로 즉각 반응)
      var old = document.getElementById('chatrow-' + msgId);
      if (old) { var fresh = buildMsgEl(msg, bookId); old.parentNode.replaceChild(fresh, old); }

      // 실제 DB 채팅 메시지(임시 로컬 mock ID가 아닌 경우)에 한해 백엔드에 반영해
      // 새로고침 후에도 유지되고 다른 독자에게도 보이도록 동기화한다.
      var hasRealId = msgId && (typeof msgId === 'number' || (!isNaN(Number(msgId)) && !String(msgId).startsWith('msg')));
      if (!hasRealId) return;

      function rollbackRx() {
        if (!msg.reactions[emoji]) msg.reactions[emoji] = { count: 0, mine: false };
        msg.reactions[emoji].mine = wasMine;
        msg.reactions[emoji].count = prevCount;
        if (msg.reactions[emoji].count === 0) delete msg.reactions[emoji];
        var row = document.getElementById('chatrow-' + msgId);
        if (row) { var reverted = buildMsgEl(msg, bookId); row.parentNode.replaceChild(reverted, row); }
      }

      var url = '/api/chats/' + msgId + '/react' + (adding ? '' : ('?emoji=' + encodeURIComponent(emoji)));
      fetch(url, {
        method: adding ? 'POST' : 'DELETE',
        headers: adding
          ? { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token }
          : { 'Authorization': 'Bearer ' + token },
        body: adding ? JSON.stringify({ emoji: emoji }) : undefined
      }).then(function (r) {
        if (!r.ok) {
          console.error('반응 저장 실패:', r.status);
          rollbackRx();
          var wasAuthErr = handleAuthError(r.status);
          if (!wasAuthErr) showToast(t('toast_rx_failed'));
        }
      }).catch(function (err) {
        console.error('반응 저장 API 에러:', err);
        rollbackRx();
        showToast(t('toast_network_error'));
      });
    }
    var searchMatches = [];
    var searchCursor = -1;
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
    // 검색어 하이라이트는 텍스트 노드만 <mark>로 감싼다.
    // (예전에는 버블의 innerHTML 문자열을 정규식으로 치환했다. 검색어가 태그명이나
    //  속성값과 겹치면 마크업이 깨지거나 의도치 않은 태그가 만들어질 수 있었다.)
    function highlightTextNodes(el, re) {
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
      var textNodes = [];
      var node;
      while ((node = walker.nextNode())) textNodes.push(node);

      textNodes.forEach(function (textNode) {
        var text = textNode.nodeValue;
        re.lastIndex = 0;
        if (!re.test(text)) return;
        re.lastIndex = 0;

        var frag = document.createDocumentFragment();
        var last = 0;
        var m;
        while ((m = re.exec(text)) !== null) {
          if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
          var mark = document.createElement('mark');
          mark.className = 'search-highlight';
          mark.textContent = m[0];          // textContent: 검색어가 마크업으로 해석되지 않는다
          frag.appendChild(mark);
          last = m.index + m[0].length;
          if (m[0].length === 0) re.lastIndex++;   // 빈 매치 무한루프 방지
        }
        if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
        textNode.parentNode.replaceChild(frag, textNode);
      });
      re.lastIndex = 0;
    }

    function clearSearchHighlights() {      searchMatches.forEach(function(m) {
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
          // 복원용 원본만 보관하고, 하이라이트는 DOM 레벨에서 적용한다.
          matches.push({ rowEl: row, bubbleEl: bubble, originalHtml: original });
        }
        re.lastIndex = 0;
      });
      searchMatches = matches;
      allRows.forEach(function(row) {
        if (!matches.some(function(m) { return m.rowEl === row; })) row.classList.add('search-dim');
      });
      matches.forEach(function(m) { highlightTextNodes(m.bubbleEl, re); });
      if (matches.length === 0) {
        if (count) count.textContent = t('search_no_result');
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
        // 새로고침이나 뒤로가기로 빈 화면이 되지 않도록, 고르지 않은 후보를 서버에서 복원한다
        if (typeof restoreCandidatesIfEmpty === 'function') restoreCandidatesIfEmpty();
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
      ensureArchivedSampleData(book);
      // 새 도서를 열 때마다 가로 보기 모드/토글 버튼 상태를 기본(세로 보기)으로 초기화
      arcHorizontalMode = false;
      var arcToggleBtn = document.getElementById('arc-view-toggle-btn');
      if (arcToggleBtn) {
        arcToggleBtn.classList.remove('active');
        arcToggleBtn.textContent = t('view_horizontal');
      }
      var arcContent = document.querySelector('#pg-archive .arc-content');
      if (arcContent) {
        arcContent.classList.remove('arc-horizontal-mode');
        arcContent.style.height = '';
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
        var chatSeeds = getSampleChatSeeds(book);
        chatSeeds.forEach(function(s, idx) {
          combinedChats.push({
            id: 'mock-ch-' + idx,
            user: s.user,
            text: s.text,
            ts: s.ts || ('오후 08:' + (12 + idx * 4)),
            date: s.date || new Date().toISOString()
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
      var arcPages = [];

      // 1. 아카이브 고품격 커버 (Editorial Cover)
      html += '<div class="arc-cover" style="border-top: 6px solid ' + book.color + ';">';
      html += '  <div class="arc-cover-label">가공독서회 · 아카이브 에디션 · 제' + book.id + '호</div>';
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

      arcPages.push(html); html = '';

      // 2. 도서 핵심 띠지 (Book Band)
      html += '<div class="arc-book-band">';
      html += '  <div class="arc-book-band-cover" style="' + getCoverCss(book) + '"></div>';
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
      html += '    <div class="arc-stat-label">' + t('arc_stat_readers') + '</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalChats + '</div>';
      html += '    <div class="arc-stat-label">' + t('arc_stat_chats') + '</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalComments + '</div>';
      html += '    <div class="arc-stat-label">' + t('arc_stat_comments') + '</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + totalReactions + '</div>';
      html += '    <div class="arc-stat-label">' + t('arc_stat_rx') + '</div>';
      html += '  </div>';
      html += '  <div class="arc-stat-item">';
      html += '    <div class="arc-stat-num" style="color:' + book.color + ';">' + avgScore.toFixed(1) + '</div>';
      html += '    <div class="arc-stat-label">' + t('arc_stat_rating') + '</div>';
      html += '  </div>';
      html += '</div>';

      arcPages.push(html); html = '';

      // 4. 에디토리얼 레터 (Editor's Note)
      html += '<div class="arc-section arc-editorial">';
      html += '  <div class="arc-eyebrow">EDITOR\'S NOTE</div>';
      html += '  <div class="arc-editorial-title">' + t('arc_editorial_title') + '</div>';
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

      arcPages.push(html); html = '';

      // 5. 독서 참여자 리스트 (Participants)
      html += '<div class="arc-section" style="background:#fff;">';
      html += '  <div class="arc-eyebrow">PARTICIPANTS</div>';
      html += '  <div class="arc-section-title">' + t('arc_participants_title') + totalUsers + t('arc_participants_unit') + '</div>';
      html += '  <div class="arc-section-sub">닉네임은 가공독서회 시스템이 고유하게 배정했습니다. 본명은 영구 비공개됩니다.</div>';
      html += '  <div class="arc-participants-grid">';
      distinctUsers.forEach(function(u) {
        var clr = getNickColor(u);
        html += '    <div class="arc-p-chip">';
        html += '      <div class="arc-p-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + escHtml(u.charAt(0)) + '</div>';
        html += '      <div class="arc-p-name">' + escHtml(u) + '</div>';
        html += '    </div>';
      });
      html += '  </div>';
      html += '</div>';

      arcPages.push(html); html = '';

      // 6. 1장: 책의 이야기와 첫인상 (Chapter 1)
      html += '<div class="arc-chapter-divider"></div>';
      html += '<div class="arc-chapter-header">';
      html += '  <div class="arc-chapter-num">' + t('arc_chapter1_num') + '</div>';
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
        html += '      <div class="arc-msg-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + escHtml(c.user.charAt(0)) + '</div>';
        html += '      <div>';
        html += '        <div class="arc-msg-name">' + escHtml(c.user) + '</div>';
        html += '        <div class="arc-msg-time">독서회 댓글 · ' + escHtml(String(c.created_at)) + '</div>';
        html += '      </div>';
        html += '    </div>';
        html += '    <div class="arc-msg-body">' + escHtml(c.content) + '</div>';
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
          html += '      <div class="arc-chat-av-sm" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + escHtml(ch.user.charAt(0)) + '</div>';
        }
        html += '      <div class="arc-chat-col">';
        if (!isMine) {
          html += '        <div class="arc-chat-name-sm">' + escHtml(ch.user) + '</div>';
        }
        html += '        <div class="arc-chat-bubble">' + escHtml(ch.text || '') + '</div>';
        if (!isMine) {
          html += '        <div style="display:flex;gap:4px;margin-top:4px;">';
          html += '          <span class="arc-crx hot">❤️ ' + (12 - idx * 2 > 0 ? 12 - idx * 2 : 5) + '</span>';
          html += '          <span class="arc-crx">✨ ' + (8 - idx > 0 ? 8 - idx : 3) + '</span>';
          html += '        </div>';
        }
        html += '      </div>';
        html += '      <span style="font-size:10px;color:#6b5040;align-self:flex-end;flex-shrink:0;margin-left:4px;">' + escHtml(String(ch.ts || '')) + '</span>';
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

      arcPages.push(html); html = '';

      // 7. 2장: 가장 오래 남은 감상 최종 선별 TOP (Chapter 2)
      html += '<div class="arc-chapter-divider"></div>';
      html += '<div class="arc-chapter-header">';
      html += '  <div class="arc-chapter-num">' + t('arc_chapter2_num') + '</div>';
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
        html += '      <div class="arc-sentence-text">' + escHtml(c.content) + '</div>';
        html += '      <div class="arc-sentence-meta">';
        html += '        <div class="arc-sentence-author">';
        html += '          <div class="arc-s-av" style="background:' + clr.bg + ';color:' + clr.fg + ';">' + escHtml(c.user.charAt(0)) + '</div>';
        html += '          <span class="arc-s-name">' + escHtml(c.user) + '</span>';
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
      html += '      <div class="arc-col-lbl">' + t('arc_col_publisher') + '</div>';
      html += '      <div class="arc-col-val">가공독서회 보존기록팀</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">' + t('arc_col_editor') + '</div>';
      html += '      <div class="arc-col-val">가공 아카이브 에디터 일동</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">' + t('arc_col_class') + '</div>';
      html += '      <div class="arc-col-val">GK-ARC-2026-N' + book.id + '</div>';
      html += '    </div>';
      html += '    <div>';
      html += '      <div class="arc-col-lbl">' + t('arc_col_date') + '</div>';
      html += '      <div class="arc-col-val">' + book.archivedDate + '</div>';
      html += '    </div>';
      html += '  </div>';
      html += '  <div class="arc-colophon-foot">';
      html += '    © GAKONG BOOK CLUB. ALL MEMORIES RESERVED.';
      html += '  </div>';
      html += '</div>';

      arcPages.push(html); html = '';

      if (arcContent) {
        var pagesMarkup = arcPages.map(function(p, i) {
          return '<div class="arc-page" data-page="' + i + '">' + p + '</div>';
        }).join('');
        var navMarkup =
          '<div class="arc-page-nav">' +
          '  <button class="arc-page-nav-btn" id="arc-prev-btn" onclick="arcNavPage(-1)">‹</button>' +
          '  <div class="arc-page-dots" id="arc-page-dots"></div>' +
          '  <button class="arc-page-nav-btn" id="arc-next-btn" onclick="arcNavPage(1)">›</button>' +
          '</div>';
        arcContent.innerHTML =
          '<div class="arc-pages-viewport">' +
          '  <div class="arc-pages-track" id="arc-pages-track">' + pagesMarkup + '</div>' +
          '</div>' + navMarkup;
      }
      arcPageCount = arcPages.length;
      arcPageIndex = 0;
      arcGoToPage(0, true);
    }

    /* ── 아카이브 가로 보기(페이지 넘기기) 모드 ── */
    var arcHorizontalMode = false;
    var arcPageIndex = 0;
    var arcPageCount = 0;

    function toggleArcViewMode() {
      arcHorizontalMode = !arcHorizontalMode;
      var contentEl = document.querySelector('#pg-archive .arc-content');
      var btn = document.getElementById('arc-view-toggle-btn');
      if (contentEl) contentEl.classList.toggle('arc-horizontal-mode', arcHorizontalMode);
      if (btn) {
        btn.classList.toggle('active', arcHorizontalMode);
        btn.textContent = arcHorizontalMode ? t('view_vertical') : t('view_horizontal');
      }
      if (arcHorizontalMode) {
        var headerEl = document.querySelector('#pg-archive .arc-page-header');
        if (headerEl && contentEl) {
          var headerBottom = Math.max(headerEl.getBoundingClientRect().bottom, 0);
          contentEl.style.height = 'calc(100vh - ' + headerBottom + 'px)';
        }
      } else if (contentEl) {
        contentEl.style.height = '';
      }
      arcGoToPage(0);
    }
    window.toggleArcViewMode = toggleArcViewMode;

    function renderArcPageDots() {
      var dotsEl = document.getElementById('arc-page-dots');
      if (!dotsEl) return;
      var dotsHtml = '';
      for (var i = 0; i < arcPageCount; i++) {
        dotsHtml += '<span class="arc-page-dot' + (i === arcPageIndex ? ' active' : '') + '" onclick="arcGoToPage(' + i + ')"></span>';
      }
      dotsEl.innerHTML = dotsHtml;
    }

    function arcGoToPage(idx) {
      if (arcPageCount <= 0) return;
      idx = Math.max(0, Math.min(arcPageCount - 1, idx));
      arcPageIndex = idx;
      var track = document.getElementById('arc-pages-track');
      if (track) track.style.transform = 'translateX(-' + (idx * 100) + '%)';
      var prevBtn = document.getElementById('arc-prev-btn');
      var nextBtn = document.getElementById('arc-next-btn');
      if (prevBtn) prevBtn.disabled = (idx === 0);
      if (nextBtn) nextBtn.disabled = (idx === arcPageCount - 1);
      renderArcPageDots();
    }
    window.arcGoToPage = arcGoToPage;

    function arcNavPage(delta) {
      arcGoToPage(arcPageIndex + delta);
    }
    window.arcNavPage = arcNavPage;

    document.addEventListener('keydown', function(e) {
      if (!arcHorizontalMode) return;
      var arcPg = document.getElementById('pg-archive');
      if (!arcPg || !arcPg.classList.contains('active')) return;
      if (e.key === 'ArrowRight') arcNavPage(1);
      else if (e.key === 'ArrowLeft') arcNavPage(-1);
    });

    (function setupArcSwipe() {
      var touchStartX = null;
      document.addEventListener('touchstart', function(e) {
        var arcPg = document.getElementById('pg-archive');
        if (!arcHorizontalMode || !arcPg || !arcPg.classList.contains('active')) { touchStartX = null; return; }
        touchStartX = e.touches[0].clientX;
      }, { passive: true });
      document.addEventListener('touchend', function(e) {
        if (touchStartX === null) return;
        var dx = e.changedTouches[0].clientX - touchStartX;
        touchStartX = null;
        if (Math.abs(dx) > 60) {
          if (dx < 0) arcNavPage(1); else arcNavPage(-1);
        }
      }, { passive: true });
    })();

    /* ── CHAT HISTORY (읽기 전용 채팅 열람) ── */
    async function openChatHistory(bookId) {
      var targetId = parseInt(bookId) || bookId;
      var book = BOOKS.find(function(b) { return b.id == targetId; });
      if (!book) return;
      // 헤더 정보 먼저 업데이트 후 페이지 전환
      var titleEl = document.getElementById('chat-history-title');
      if (titleEl) titleEl.textContent = book.title + t('chat_history_suffix');
      var coverEl = document.getElementById('chat-history-header-book');
      if (coverEl) { coverEl.style.background = book.color; coverEl.textContent = book.title; }
      var metaEl = document.getElementById('chat-history-meta');
      if (metaEl) metaEl.textContent = t('chat_history_loading');
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
        var sampleSeeds = getSampleChatSeeds(book);
        chats = sampleSeeds.map(function(s, idx) {
          return {
            id: 'mock-ch-hist-' + idx,
            user: s.user,
            text: s.text,
            ts: s.ts,
            date: s.date || new Date().toISOString(),
            replyTo: s.replyTo || null,
            reactions: s.reactions || { "❤️": (12 - idx * 2 > 0 ? 12 - idx * 2 : 5), "✨": (8 - idx > 0 ? 8 - idx : 3) }
          };
        });
      }
      // 메타 정보 업데이트
      if (metaEl) metaEl.textContent = t('chat_history_total') + chats.length + t('chat_history_readonly');
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
      body.appendChild(makeDivider(t('chat_open_date')));
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
        '<div class="chat-av" style="background:' + clr.bg + ';color:' + clr.fg + '">' + escHtml(av) + '</div>' +
        '<div class="chat-col">' +
        '<div class="chat-name">' + escHtml(userName) + '</div>' +
        '<div class="chat-bubble">' + replyQuote + escHtml(ch.text || '') + '</div>' +
        rxHtml +
        '</div>' +
        '<div class="chat-time-wrap"><span class="chat-time">' + escHtml(ch.ts || '') + '</span></div>';
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
        row.innerHTML = '<div class="arc-empty">' + t('lib_arc_empty') + '</div>';
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
        el.innerHTML = '<div class="arc-book-spine-txt">' + escHtml(b.title) + '</div>';
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
      if (su) su.textContent = book.archivedDate + t('lib_arc_closed') + myChatCount + t('lib_arc_included');
      var btn = document.getElementById('arc-lib-bdp-btn');
      if (btn) {
        btn.textContent = t('lib_arc_view');
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
    
    // 표지 이미지 URL에서 따옴표/괄호/세미콜론을 제거해 url('...') 문맥을 벗어나지 못하게 한다.
    function safeCssUrl(url) {
      var out = String(url === null || url === undefined ? '' : url);
      var bad = ['"', String.fromCharCode(39), '(', ')', ';', String.fromCharCode(92)];
      for (var i = 0; i < bad.length; i++) out = out.split(bad[i]).join('');
      return out;
    }

    // 색상은 CSS 색상 리터럴에 쓰이는 문자만 허용하고, 그 외는 기본색으로 대체한다.
    var CSS_COLOR_OK = /^[#a-zA-Z0-9(), .%]+$/;
    function safeCssColor(color) {
      var c = String(color === null || color === undefined ? '' : color).trim();
      return (c && c.length <= 32 && CSS_COLOR_OK.test(c)) ? c : '#7b5fb8';
    }
    window.safeCssColor = safeCssColor;

    function getCoverCss(b, extraStyle) {
      extraStyle = extraStyle || '';
      var img = b ? (b.coverImageUrl || b.cover_image_url || b.coverUrl) : null;
      if (img) {
        return "background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.55) 100%), url('" + safeCssUrl(img) + "') center/cover no-repeat; position: relative; " + extraStyle;
      }
      return "background: " + safeCssColor(b && b.color) + "; position: relative; " + extraStyle;
    }
    window.getCoverCss = getCoverCss;


function adaptDbBookToFrontend(dbBook) {
      var deadlineVal = dbBook.deadline_days !== undefined ? dbBook.deadline_days : 10;
      return {
        id: dbBook.id,
        coverImageUrl: dbBook.cover_image_url || null,
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
        // 반응 총합은 서버가 집계해 내려준다(rx_counts).
        // 예전에는 채팅 캐시를 훑어 계산했지만, 채팅방을 열기 전에는
        // 캐시가 비어 있어 상세 페이지의 반응 줄이 항상 0으로 보였다.
        rxCounts: dbBook.rx_counts || { '❤️': 0, '🤔': 0, '😄': 0, '✨': 0 },
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




    // ── 표지 확대 뷰어 팝업 ──
    function openCoverZoom(imgUrl, bgColor, title) {
      var overlay = document.getElementById('cover-zoom-overlay');
      var bg = document.getElementById('cover-zoom-bg');
      if (!overlay || !bg) return;

      var currentCoverImg = imgUrl || (currentBook ? (currentBook.coverImageUrl || currentBook.cover_image_url || currentBook.coverUrl) : null);
      var currentBgColor = bgColor || (currentBook ? currentBook.color : '#7b5fb8');

      if (currentCoverImg) {
        bg.style.background = "url('" + currentCoverImg + "') center/contain no-repeat";
        bg.style.backgroundColor = '#1a1a1a';
      } else {
        bg.style.background = currentBgColor || '#555';
      }
      overlay.classList.add('active');

      document._coverZoomEsc = function(e) {
        if (e.key === 'Escape') closeCoverZoom();
      };
      document.addEventListener('keydown', document._coverZoomEsc);
    }

    function closeCoverZoom() {
      var overlay = document.getElementById('cover-zoom-overlay');
      if (overlay) overlay.classList.remove('active');
      if (document._coverZoomEsc) {
        document.removeEventListener('keydown', document._coverZoomEsc);
        document._coverZoomEsc = null;
      }
    }
    window.openCoverZoom = openCoverZoom;
    window.closeCoverZoom = closeCoverZoom;



    
    // ── 다국어 (한국어 / 일본어) i18n 딕셔너리 및 상태 제어 ──
    var CURRENT_LANG = localStorage.getItem('app_lang') || 'ko';

    var I18N_DICT = {
      ko: {
        logo_text: "<em>가공</em>독서회",
        footer_copy: "© 2026 가공독서회. All rights reserved.",
        nav_home: "독서방 목록",
        nav_lib: "내 서재",
        nav_guide: "이용 안내",
        hero_label: "FICTION READING CLUB",
        hero_title: "존재하지 않는 책을<br>함께 읽어요",
        hero_desc: "AI가 만든 가상의 책 줄거리를 보고, 그 책이 어떤 내용일지 상상하며 다른 독자들과 이야기를 나눕니다.<br>한 번도 읽은 적 없는 책에 대해 가장 깊이 있는 감상을 나눠보세요.",
        gen_section_title: "새 책 소환하기",
        gen_section_desc: "AI가 3권의 후보 책을 만들어냅니다. 마음에 드는 한 권을 골라 독서방으로 열어보세요.",
        gen_btn: "✦ 새 책 생성",
        genre_section_title: "장르별 모아보기",
        deadline_section_title: "기간 임박 순서대로 보기",
        deadline_section_sub: "마감이 가까운 독서방",
        cand_back: "← 돌아가기",
        cand_label: "BOOK CURATION",
        cand_title: "어떤 책을<br>독서방으로 열까요?",
        cand_desc: "AI가 3권의 후보 책을 가져왔습니다. 하나를 선택하면 정식 독서방으로 개설됩니다.",
        cand_select_btn: "이 책으로 독서방 열기",
        cand_loading_cover: "AI 표지 생성 중...",
        arc_tab: "🗃 아카이브",
        genre_all: "전체",
        days_left: "일 남음",
        join_chat_btn: "독서방 참여하기",
        add_lib_btn: "+ 내 서재에 담기",
        remove_lib_btn: "✓ 내 서재에서 제거",
        detail_back: "← 독서방 목록으로",
        detail_chat_history: "💬 채팅 열람하기",
        detail_hall_of_fame: "👑 명예의 전당 · 베스트 상상 독자 리뷰",
        detail_toc_title: "도서 상세 목차",
        detail_publisher_review: "출판사 서평",
        detail_endorsements: "추천사",
        detail_stats_analysis: "독서 통계 분석",
        detail_avg_rating: "평균 평점",
        detail_reader_keywords: "독자 감정 키워드",
        profile_edit_btn: "⚙️ 편집",
        lib_profile_since: "가공독서회 회원",
        chat_input_placeholder: "메시지를 입력하세요... (@사회자 를 입력해 사회자의 의견을 물어보세요)",
        chat_send_btn: "전송",
        chat_reply_btn: "답장하기",
        rx_heart: "공감해요",
        rx_think: "생각이 달라요",
        rx_laugh: "재밌어요",
        rx_sparkle: "인상 깊어요",
        chat_mod_name: "AI 사회자",
        chat_readonly_notice: "종료된 아카이브 독서방입니다 (읽기 전용)",
        lib_title: "내 서재",
        lib_desc: "내가 수집하고 사색한 문학 도서와 감상 기록을 모아봅니다.",
        lib_stat_saved: "담아둔 책",
        lib_stat_writings: "남긴 감상",
        lib_stat_chats: "작성한 댓글",
        lib_stat_arc: "참여 아카이브",
        lib_tab_saved: "담아둔 책",
        lib_tab_archive: "참여 아카이브",
        lib_shelf_saved_label: "내가 수집한 서재 목록",
        lib_shelf_writings_label: "내가 남긴 감상 및 댓글",
        lib_shelf_arc_label: "참여하고 종료된 독서방",
        lib_shelf_arc_notice: "아카이브는 독서방 종료 후 생성된 감상 기록집이에요. 내가 참여한 독서방이 종료되면 여기에 보관돼요.",
        lib_empty_saved: "'내 서재에 담기'로 책을 수집해보세요.",
        lib_empty_writings: "아직 남긴 감상이나 댓글이 없어요.",
        lib_empty_arc: "참여한 독서방이 종료되면 여기에 아카이브가 쌓여요.",
        lib_view_arc_btn: "아카이브 보기",
        footer_contact: "1:1 문의",
        footer_info: "이용 안내",
        footer_terms: "이용약관",
        footer_privacy: "개인정보처리방침",
        info_back_btn: "← 돌아가기",
        info_guide_title: "이용 가이드",
        info_guide_intro: "<div style='font-family: var(--serif); font-size: 17px; font-weight: 700; color: var(--accent); margin-bottom: 12px;'>반갑습니다, 가공의 독자님! ✦</div><div class='info-section-text' style='font-size: 13.5px; color: var(--text);'><strong>가공독서회(Gakong Reading Club)</strong>는 AI의 창의성과 여러분의 상상력이 만나는 특별한 문학 살롱입니다.<br><br>이곳의 모든 책은 실재하지 않습니다. AI가 직조해 낸 줄거리와 단편적인 단서들을 단초 삼아, 마치 <strong>'그 책을 읽은 것처럼'</strong> 상상하여 감상을 나누는 공간입니다. 읽지 않은 책에 대해 이야기하는 짜릿한 지적 유희를 즐겨보세요!</div>",
        info_guide_rules: "<div class='info-section-label'><span>🤝</span> 꼭 지켜야 할 독서회 약속</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span><div><strong>\"이 책은 존재한다\"고 믿기:</strong> 가장 중요한 규칙입니다. '가짜 책이니까'라는 생각 대신, 진짜로 밤새워 읽은 책인 것처럼 몰입하여 이야기해 주세요.</div></div><div class='info-list-item'><span class='info-list-dot'></span><div><strong>창작의 존중:</strong> 정답은 없습니다. 내가 상상한 이야기와 다른 독자가 상상한 이야기기가 서로 다르더라도, 그것은 서로 다른 감상을 낳은 아름다운 창작물입니다. 타인의 생각을 존중하고 경청해 주세요.</div></div><div class='info-list-item'><span class='info-list-dot'></span><div><strong>자유로운 덧붙임:</strong> 책 내용뿐 아니라 작가의 비하인드 스토리, 번역가의 문체, 디자인, 책의 가격 등 책을 둘러싼 외부 세계까지 마음껏 살을 붙여 상상하셔도 좋습니다.</div></div></div>",
        info_guide_steps: "<div class='info-section-label'><span>🧭</span> 독서회 참여하기: 5단계 가이드</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 18px; margin-top: 10px;'><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>1</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>책 탐색 또는 직접 생성하기</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>홈 화면에서 열려 있는 다른 독서방을 구경해 보세요. 혹은 <strong>'새 책 생성'</strong> 버튼을 눌러 AI가 제안하는 3권의 후보 중 마음에 드는 한 권을 골라 독서방을 직접 열 수 있습니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>2</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>책 상세 정보와 단서 읽기</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>책 상세 페이지로 이동해 제목, 시놉시스, 첫 문장, 추천사, 출판사 서평 및 <strong>'상세 목차'</strong>를 읽어보세요. 각 장의 페이지와 요약문을 훑어보며 책의 구체적인 전개를 머릿속으로 그려보는 것이 상상의 첫걸음입니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>3</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>기록 남기기 (별점과 감상평)</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>책이 내 마음에 들었는지 평점을 매겨보세요. 그리고 상세 페이지 하단에 <strong>'한 줄 평'이나 감상평 댓글</strong>을 적어보세요. 다른 사람의 기발한 감상에 더블 클릭하여 공감을 표시하거나 답글을 남길 수도 있습니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>4</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>독서 토론방에서 실시간 대화하기</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'><strong>'독서방 참여하기'</strong> 버튼을 클릭해 실시간 대화방에 입장하세요. 독자들과 자유롭게 채팅을 나눌 수 있으며, 웰컴 추천 질문 제시 및 <code>@사회자</code> 멘션 시 비하인드 세계관을 답변해 주는 <strong>AI 사회자</strong>와도 정갈한 대화를 나눌 수 있습니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>5</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>소장하기와 아카이브 열람</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>마음에 드는 책은 <strong>'내 서재에 담기'</strong>로 책꽂이에 보관할 수 있습니다. 운영 기간(약 10일)이 종료되어 아카이브된 책들은 평생 소장본 책처럼 박제되며, 언제든 '아카이브' 메뉴를 통해 독서회의 대화록과 반응 통계를 아름다운 양장본 스타일로 다시 읽을 수 있습니다.</div></div></div></div>",
        info_guide_mod_role: "<div class='info-section-label'><span>🎙️</span> AI 사회자의 역할</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 14px; margin-top: 6px;'><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>1</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>추천 토론 질문 제시</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>독서방 진입 시 첫 웰컴 카드로 핵심 딜레마 및 추천 토론 질문 3가지를 제시하여 편안하게 대화를 시작할 수 있도록 돕습니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>2</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>담백한 질문 가이드</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>독자들의 자율적인 대화를 방해하는 과도한 사족이나 개입을 빼고, 토론의 물꼬를 틔우는 정갈한 질문 화두만 깔끔하게 던집니다.</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>3</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>@사회자 멘션 대화</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>채팅창에 <code>@사회자</code>를 멘션하여 질문을 던지면, 가상 도서의 세계관과 깊이 있는 인물 설정을 친절하게 설명해 줍니다.</div></div></div></div>",
        info_guide_qa: "<div class='info-section-label'><span>❓</span> 무엇이든 물어보세요 (Q&A)</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 16px; margin-top: 10px;'><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. 정말로 책을 읽지 않고 들어와도 되나요?</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>그럼요! 이 플랫폼에 있는 모든 책은 AI가 막 지어낸 책이라 <strong>작가 자신도 아직 쓰지 않은 상태</strong>입니다. 따라서 어떤 말을 하든 그것은 오답이 될 수 없으니, 주저 없이 자유롭게 첫 느낌을 털어놓아 보세요.</div></div><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. 어떤 감상을 남겨야 할지 막막해요.</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>막막할 때는 아래의 팁을 따라 한 번 생각해보세요:<br>• <strong>첫 문장에 대하여:</strong> 소설의 첫 문장을 보고 어떤 분위기나 장면이 연상되나요?<br>• <strong>소설의 핵심 딜레마:</strong> 책 상세 페이지에 표시된 토론 질문(Q.)을 읽고 나의 가치관에 비춰 답해보세요.<br>• <strong>목차의 전개:</strong> 특정 챕터의 제목이나 요약 글이 맘에 든다면, '이 챕터에서는 주인공이 이런 행동을 했을 것 같다'고 제안해보세요.</div></div><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. 저작권은 누구에게 있나요?</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>AI가 출력해 낸 책의 기본 뼈대(제목, 줄거리 등)는 저작권이 인정되지 않는 공공 영역(Public Domain)에 속합니다. 하지만 이를 기반으로 <strong>독자님이 창의적으로 남겨주신 소중한 감상평, 덧댓글, 독서방 대화 내용은 인간 고유의 저작물로 완전히 작성자(독자)에게 저작권이 귀속</strong>됩니다. 타인의 소중한 해석을 무단 도용하거나 폄하하지 말아 주세요.</div></div></div>",
        info_contact_title: "1:1 문의",
        info_contact_s1: "<div class='info-section-label'>📬 문의 방법</div><div class='info-section-text'>서비스 이용 중 불편한 점이나 건의사항이 있으시면 아래 이메일로 문의해 주세요.<br><br>담당자가 확인 후 <strong>영업일 기준 1~3일 이내</strong>에 답변드립니다.</div>",
        info_contact_s2: "<div class='info-section-label'>✉ 문의 이메일</div><div class='info-contact-email'>gakongbooks@gmail.com</div>",
        info_contact_s3: "<div class='info-section-label'>📋 문의 시 포함해 주세요</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> 가입하신 이메일 주소</div><div class='info-list-item'><span class='info-list-dot'></span> 문의 유형 (계정, 콘텐츠, 기술적 문제 등)</div><div class='info-list-item'><span class='info-list-dot'></span> 문제 상황을 자세히 설명해 주시면 빠른 처리에 도움이 됩니다.</div></div>",
        info_contact_s4: "<div class='info-section-label'>⏰ 운영 시간</div><div class='info-section-text'>평일 10:00 ~ 18:00 (토·일·공휴일 제외)<br><span style='color:var(--text-faint);font-size:12px;'>운영 시간 외 문의는 다음 영업일에 순차적으로 처리됩니다.</span></div>",
        info_terms_title: "이용약관",
        info_terms_s1: "<div class='info-section-label'>제1조 (목적)</div><div class='info-section-text'>이 약관은 가공독서회(이하 \"서비스\")가 제공하는 AI 기반 가상 독서 모임 서비스의 이용과 관련하여 서비스와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.</div>",
        info_terms_s2: "<div class='info-section-label'>제2조 (서비스 내용)</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> AI가 생성한 가상 도서 정보 제공</div><div class='info-list-item'><span class='info-list-dot'></span> 독서방 참여 및 댓글·평점·반응 기능</div><div class='info-list-item'><span class='info-list-dot'></span> 개인 서재 관리 기능</div><div class='info-list-item'><span class='info-list-dot'></span> 종료된 독서방의 아카이브 열람</div></div>",
        info_terms_s3: "<div class='info-section-label'>제3조 (회원의 의무)</div><div class='info-section-text'>이용자는 다음 행위를 하여서는 안 됩니다.<br><br><div class='info-list-item'><span class='info-list-dot'></span> 타인의 개인정보 도용 또는 허위 정보 등록</div><div class='info-list-item'><span class='info-list-dot'></span> 서비스 운영을 방해하는 행위</div><div class='info-list-item'><span class='info-list-dot'></span> 타인에 대한 비방, 욕설 등 불건전한 내용 게시</div><div class='info-list-item'><span class='info-list-dot'></span> 상업적 목적의 무단 광고 게시</div></div>",
        info_terms_s4: "<div class='info-section-label'>제4조 (콘텐츠 안내)</div><div class='info-section-text'>본 서비스의 모든 도서 정보는 AI가 생성한 <strong>가상의 창작물</strong>입니다. 실존하는 책, 작가, 출판사와 무관하며, 가격 또한 참고용 가상 가격입니다.</div>",
        info_terms_s5: "<div class='info-section-label'>제5조 (약관 변경)</div><div class='info-section-text'>서비스는 필요한 경우 약관을 변경할 수 있으며, 변경된 약관은 서비스 내 공지를 통해 이용자에게 안내합니다.<br><span style='color:var(--text-faint);font-size:12px;'>최종 개정: 2026년 6월</span></div>",
        info_privacy_title: "개인정보 처리방침",
        info_privacy_s1: "<div class='info-section-label'>수집하는 개인정보</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> 이메일 주소 (회원가입 및 본인 확인 목적)</div><div class='info-list-item'><span class='info-list-dot'></span> 익명 닉네임 (서비스 내 표시 목적)</div><div class='info-list-item'><span class='info-list-dot'></span> 작성한 댓글 및 메시지 (서비스 운영 목적)</div></div>",
        info_privacy_s2: "<div class='info-section-label'>개인정보 이용 목적</div><div class='info-section-text'>수집된 개인정보는 회원 관리, 서비스 제공, 분쟁 해결 목적으로만 이용되며 외부에 제공되지 않습니다.</div>",
        info_privacy_s3: "<div class='info-section-label'>개인정보 보유 기간</div><div class='info-section-text'>회원 탈퇴 시 즉시 파기합니다. 단, 관련 법령에 따른 보존 의무가 있는 경우 해당 기간 동안 보관합니다.</div>",
        info_privacy_s4: "<div class='info-section-label'>이용자의 권리</div><div class='info-section-text'>이용자는 언제든지 본인의 개인정보 열람, 수정, 삭제를 요청하실 수 있습니다.<br>문의: <strong>gakongbooks@gmail.com</strong><br><span style='color:var(--text-faint);font-size:12px;'>최종 개정: 2026년 6월</span></div>"
      ,
        count_unit: "개",
        people_unit: "명",
        participants_joining: "명 참여 중",
        closing_soon: "⚠ 곧 마감 · ",
        archive_badge: "아카이브",
        archive_open_btn: "📖 아카이브 열람하기",
        page_unit: "쪽",
        discount_note: " (10% 할인가)",
        delete_btn: "삭제",
        view_horizontal: "⇄ 가로 보기",
        view_vertical: "↕ 세로 보기",
        search_no_result: "없음",
        detail_rating_blind: "종료 후 공개됩니다",
        detail_rating_blind_desc: "평균 별점은 독서방 종료 후 아카이브에서 공개됩니다.",
        detail_my_rating: "내 평점",
        detail_rating_locked: "독서방에 참여하면 평점을 남길 수 있어요",
        detail_join_short: "참여하기",
        detail_chat_reactions: "채팅 반응",
        detail_rx_blind_desc: "채팅 종합 반응은 독서방 종료 후 아카이브에서 공개됩니다.",
        detail_rx_top: "가장 많은 반응",
        detail_no_endorsement: "추천사가 아직 등록되지 않은 책입니다.",
        detail_no_review: "출판사 서평이 등록되지 않았습니다.",
        detail_no_characters: "아직 정보가 기록되지 않은 인물들입니다.",
        detail_ai_author_reply: "🤖 <strong>AI 작가 한줄평:</strong> ",
        detail_zoom_hint: "🔍 확대",
        detail_zoom_title: "클릭하여 표지 크게 보기",
        detail_virtual_book: " · AI 생성 가상 도서",
        detail_toc_empty: "상세 목차 데이터가 없습니다.",
        chat_room_suffix: " 독서방",
        chat_reply_writing: "님에게 답장 쓰는 중",
        chat_reply_placeholder: "님에게 답글을 남겨보세요...",
        chat_default_placeholder: "이 책에 대해 이야기해보세요...",
        chat_search_placeholder: "대화 내용 검색...",
        chat_search_prev: "이전 검색 결과",
        chat_search_next: "다음 검색 결과",
        chat_reply_cancel: "답장 취소",
        chat_topic_toggle: "접기/펼치기",
        chat_highlight_title: "작품 하이라이트",
        chat_first_line: "📖 첫 문장",
        chat_famous_line: "💬 명대사",
        chat_room_opened: "📚 독서방이 열렸습니다.",
        chat_open_date: "독서방 개설일",
        chat_history_suffix: " — 채팅방 기록",
        chat_history_loading: "기록 불러오는 중...",
        chat_history_readonly: " 메시지 · 읽기 전용",
        chat_history_total: "총 ",
        chat_edited: "(수정됨)",
        toast_rating_done: "점을 남겼어요!",
        toast_already_lib: "이미 서재에 있어요",
        toast_added_lib: "내 서재에 담았어요 📚",
        toast_removed_lib: "내 서재에서 제외했습니다.",
        toast_login_for_lib: "로그인 후 서재에 담을 수 있어요.",
        toast_login_required: "로그인이 필요한 서비스입니다. 로그인 페이지로 이동합니다.",
        toast_session_expired: "로그인 세션이 만료되었습니다. 다시 로그인해주세요.",
        toast_input_empty: "내용을 입력해주세요.",
        toast_edited: "수정되었어요.",
        toast_deleted: "삭제됐어요.",
        toast_edit_failed: "대화 수정에 실패했습니다.",
        toast_delete_failed: "대화 삭제에 실패했습니다.",
        toast_send_failed: "대화 전송에 실패했습니다.",
        toast_network_error: "네트워크 오류가 발생했습니다.",
        toast_no_self_rx: "내가 쓴 댓글에는 반응을 달 수 없어요.",
        toast_login_for_rx: "로그인 후 반응을 남길 수 있어요.",
        toast_rx_failed: "반응 저장에 실패했습니다.",
        toast_book_created: " 소환 성공! 📚",
        toast_new_book_prefix: "✦ 새 책 ",
        alert_login_to_gen: "새 책을 소환하려면 먼저 로그인해 주세요! 📖",
        alert_gen_failed: "새 책 후보 생성 도중 오류가 발생했습니다.",
        alert_adopt_failed: "채택 도중 오류가 발생했습니다.",
        alert_server_error: "서버와 통신할 수 없습니다.",
        confirm_delete_book: "정말로 이 도서와 독서방을 영구 삭제하시겠습니까?",
        confirm_delete_book_sub: "이 작업은 되돌릴 수 없습니다.",
        alert_book_deleted: "도서가 성공적으로 삭제되었습니다. 🌲",
        alert_book_delete_failed: "도서 삭제에 실패했습니다.",
        auth_back: "← 돌아가기",
        auth_login_title: "다시 만나서<br>반가워요",
        auth_login_sub: "존재하지 않는 책들이 기다리고 있어요.",
        auth_signup_title: "가공독서회에<br>오신 걸 환영해요",
        auth_signup_sub: "세상에 없는 책을 함께 읽어봐요.",
        auth_email: "이메일",
        auth_password: "비밀번호",
        auth_email_ph: "이메일 주소를 입력하세요",
        auth_password_ph: "비밀번호를 입력하세요",
        auth_password_ph8: "8자 이상 입력하세요",
        auth_email_invalid: "올바른 이메일 형식을 입력해주세요.",
        auth_password_empty: "비밀번호를 입력해주세요.",
        auth_password_short: "비밀번호는 8자 이상이어야 해요.",
        auth_forgot: "비밀번호를 잊으셨나요?",
        auth_login_btn: "로그인",
        auth_signup_btn: "회원가입",
        auth_logout_btn: "로그아웃",
        auth_no_account: "아직 계정이 없으신가요?",
        auth_has_account: "이미 계정이 있으신가요?",
        auth_nick_label: "✦ 부여된 독서 닉네임",
        auth_nick_loading: "닉네임 불러오는 중...",
        auth_gate_title: "내 서재",
        auth_or: "또는",
        alert_login_failed: "로그인에 실패했습니다. 이메일과 비밀번호를 다시 확인하세요.",
        alert_signup_done: "회원가입이 완료되었습니다! 🎉 로그인해주세요.",
        alert_signup_failed: "회원가입에 실패했습니다.",
        alert_nick_missing: "닉네임이 배정되지 않았습니다. 잠시 후 다시 시도해 주세요.",
        alert_fill_all: "모든 입력란을 작성해 주세요.",
        alert_pw_short: "새 비밀번호는 8자 이상이어야 합니다.",
        alert_pw_mismatch: "새 비밀번호와 확인 입력이 일치하지 않습니다.",
        alert_pw_changed: "비밀번호 변경이 완료되었습니다. 다시 로그인해 주세요. 🔒",
        alert_pw_change_failed: "비밀번호 변경에 실패했습니다. 입력 값을 확인해 주세요.",
        alert_pw_required_withdraw: "비밀번호를 입력해야 탈퇴 처리가 완료됩니다.",
        confirm_withdraw: "정말로 가공독서회를 탈퇴하시겠습니까?",
        confirm_withdraw_sub: "탈퇴 시 모든 데이터는 영구 삭제됩니다.",
        alert_withdraw_done: "회원 탈퇴가 처리되었습니다. 이용해 주셔서 감사합니다.",
        alert_withdraw_failed: "비밀번호가 일치하지 않아 탈퇴 처리에 실패했습니다.",
        confirm_logout: "로그아웃 하시겠습니까?",
        toast_logout_done: "로그아웃 되었습니다. 다음에 또 만나요! 👋",
        alert_email_required: "이메일 주소를 입력해 주세요.",
        alert_email_invalid: "올바른 이메일 형식을 입력해 주세요.",
        reset_sending: "재설정 링크 전송 중...",
        reset_send_btn: "재설정 링크 받기",
        reset_sent: "가입된 이메일이라면 비밀번호 재설정 링크를 보냈습니다. 메일함을 확인해 주세요. ✉️",
        alert_request_failed: "요청 처리에 실패했습니다. 잠시 후 다시 시도해 주세요.",
        profile_edit_title: "프로필 편집",
        lib_book_detail_title: "책 상세 페이지로 이동",
        lib_no_writings: "아직 남긴 글이 없어요. 채팅으로 이야기를 나눠보세요.",
        lib_arc_empty: "참여한 독서방이 종료되면 여기에 아카이브가 쌓입니다.",
        lib_arc_view: "아카이브 보기",
        lib_arc_closed: " 종료 · 내 감상 ",
        lib_arc_included: "개 포함",
        edit_curr_pw_ph: "현재 비밀번호를 입력하세요",
        edit_new_pw_ph: "8자 이상 입력하세요",
        edit_confirm_pw_ph: "새 비밀번호를 한번 더 입력하세요",
        withdraw_pw_ph: "탈퇴 확인을 위해 비밀번호를 입력하세요",
        genre_prev: "이전 장르 (좌로 이동)",
        genre_next: "다음 장르 (우로 이동)",
        arc_view_toggle_title: "가로 보기 전환",
        arc_stat_chats: "채팅 메시지",
        arc_stat_comments: "댓글",
        arc_stat_rx: "총 반응 수",
        arc_stat_rating: "평균 평점",
        arc_editorial_title: "편집자의 말",
        arc_participants_title: "이번 독서회 참여자 ",
        arc_participants_sub: "닉네임은 가공독서회 시스템이 랜덤으로 배정합니다. 본명은 공개되지 않습니다.",
        arc_chapter1_num: "1장",
        arc_chapter2_num: "2장",
        arc_closing_title: "기록의 보존",
        arc_col_publisher: "발행처",
        arc_col_editor: "기획 및 구성",
        arc_col_class: "서지 분류 번호",
        arc_col_date: "보관 개시일",
        arc_rx_total_prefix: "총 ",
        arc_rx_total_suffix: "개 반응",
        arc_empty_lib: "참여한 독서방이 종료되면 여기에 아카이브가 쌓입니다.",
        auth_gate_desc_all: "내 서재를 확인하려면<br>로그인이 필요합니다.<br>가공독서회 계정으로 나만의 독서 기록을 시작해보세요.",
        auth_nick_desc_all: "가입과 동시에 랜덤으로 배정되는 닉네임입니다.<br>독서방에서 이 이름으로 활동하게 됩니다.",
        auth_terms_all: "가입 시 가공독서회의 이용약관 및<br>개인정보처리방침에 동의하게 됩니다.",
        fallback_book_title: "가공 도서",
        fallback_book_author: "가상 작가",
        arc_month_unknown: "종료일 미상",
        arc_month_empty: "아직 종료된 독서방이 없어요.",
        arc_book_unit: "권",
        arc_card_overlay: "📦 아카이브 열람",
        arc_closed_suffix: " 종료",
        arc_year_unit: "년",
        arc_month_unit: "개월",
        arc_more_btn: "이전 아카이브 더 보기",
        toast_pending_restored: "아직 고르지 않은 후보가 있어 그대로 불러왔어요 📖",
        reset_modal_title: "✉️ 비밀번호 재설정",
        reset_modal_desc: "가입 시 사용하셨던 이메일 주소를 입력해 주세요.<br>비밀번호를 새로 설정할 수 있는 링크를 메일로 보내드립니다. (링크는 30분간 유효)",
        reset_modal_email_label: "가입 이메일 주소",
        detail_days_left: "일 남음",
        detail_end_suffix: " 종료",
        detail_always_open: "상시 운영",
        detail_ended_label: "종료됨",
        detail_ended_cap: "이 독서방은 종료되어 아카이브로 보관 중입니다.",
        detail_cap_always: "상시 운영되는 독서방입니다. 언제든 참여할 수 있어요.",
        detail_cap_last: "마지막 하루 · 오늘 남긴 감상이 아카이브에 실립니다.",
        detail_cap_soon_a: "",
        detail_cap_soon_b: "일 중 ",
        detail_cap_soon_c: "일 지남 · 종료되면 아카이브로 보관됩니다.",
        detail_cap_early: "지금 들어가면 처음부터 함께 읽을 수 있어요.",
        detail_colophon_title: "가상 판권면",
        detail_colophon_pages: "분량",
        detail_colophon_price: "정가",
        detail_colophon_tags: "주제어",
        detail_rx_live_label: "지금 이 방의 반응",
        detail_rx_live_badge: "실시간",
        detail_rx_empty: "아직 반응이 없어요.",
        detail_rx_empty_cta: "첫 감상을 남겨보세요 →",
        detail_rating_folded: "평균 평점 · 별점 분포",
        arc_stat_readers: "참여 독자",
        arc_participants_unit: "인",
      },
      ja: {
        logo_text: "<em>架空</em>読書会",
        footer_copy: "© 2026 架空読書会. All rights reserved.",
        nav_home: "読書室一覧",
        nav_lib: "私の書斎",
        nav_guide: "ご利用案内",
        hero_label: "FICTION READING CLUB",
        hero_title: "実在しない本を<br>共に読む",
        hero_desc: "AIが作成した架空の書籍のあらすじを見て、どのような物語か想像しながら他の読者と語り合います。<br>一度も読んだことのない本について、最も深い感想を分かち合いましょう。",
        gen_section_title: "新しい本を召喚する",
        gen_section_desc: "AIが3冊の候補本を生成します。お気に入りの1冊を選んで読書室を開設しましょう。",
        gen_btn: "✦ 新本作成",
        genre_section_title: "ジャンル別で見る",
        deadline_section_title: "締め切り間近順で見る",
        deadline_section_sub: "終了間近の読書室",
        cand_back: "← 戻る",
        cand_label: "BOOK CURATION",
        cand_title: "どの本を<br>読書室として開きますか？",
        cand_desc: "AIが3冊の候補本を準備しました。1冊を選択すると正式な読書室が開設されます。",
        cand_select_btn: "この本で読書室を開く",
        cand_loading_cover: "AI表紙生成中...",
        arc_tab: "🗃 アーカイブ",
        genre_all: "すべて",
        days_left: "日残り",
        join_chat_btn: "読書室に参加する",
        add_lib_btn: "+ 書斎に追加",
        remove_lib_btn: "✓ 書斎から削除",
        detail_back: "← 読書室一覧へ",
        detail_chat_history: "💬 チャットを閲覧",
        detail_hall_of_fame: "👑 殿堂入り・ベスト想像読者レビュー",
        detail_toc_title: "書籍の詳細目次",
        detail_publisher_review: "出版社による書評",
        detail_endorsements: "推薦の言葉",
        detail_stats_analysis: "読書統計分析",
        detail_avg_rating: "平均評価",
        detail_reader_keywords: "読者の感情キーワード",
        profile_edit_btn: "⚙️ 編集",
        lib_profile_since: "架空読書会 会員",
        chat_input_placeholder: "メッセージを入力してください... (@司会者 と入力して意見を聞いてみましょう)",
        chat_send_btn: "送信",
        chat_reply_btn: "返信する",
        rx_heart: "共感します",
        rx_think: "意見が違います",
        rx_laugh: "面白い",
        rx_sparkle: "印象的",
        chat_mod_name: "AI 司会者",
        chat_readonly_notice: "終了したアーカイブ読書室です（閲覧専用）",
        lib_title: "私の書斎",
        lib_desc: "収集し思索した文学書籍と感想の記録を集めて見ます。",
        lib_stat_saved: "保存した本",
        lib_stat_writings: "残した感想",
        lib_stat_chats: "作成したコメント",
        lib_stat_arc: "参加アーカイブ",
        lib_tab_saved: "保存した本",
        lib_tab_archive: "参加アーカイブ",
        lib_shelf_saved_label: "私が集めた書斎一覧",
        lib_shelf_writings_label: "私が残した感想およびコメント",
        lib_shelf_arc_label: "参加して終了した読書室",
        lib_shelf_arc_notice: "アーカイブは読書室終了後に作成された感想の記録集です。参加した読書室が終了するとここに保存されます。",
        lib_empty_saved: "「書斎に追加」で本を収集してみてください。",
        lib_empty_writings: "まだ残した感想やコメントがありません。",
        lib_empty_arc: "参加した読書室が終了するとここにアーカイブが蓄積されます。",
        lib_view_arc_btn: "アーカイブを見る",
        footer_contact: "1:1 お問い合わせ",
        footer_info: "ご利用案内",
        footer_terms: "利用規約",
        footer_privacy: "プライバシーポリシー",
        info_back_btn: "← 戻る",
        info_guide_title: "ご利用ガイド",
        info_guide_intro: "<div style='font-family: var(--serif); font-size: 17px; font-weight: 700; color: var(--accent); margin-bottom: 12px;'>ようこそ、架空の読者様！ ✦</div><div class='info-section-text' style='font-size: 13.5px; color: var(--text);'><strong>架空読書会（Gakong Reading Club）</strong>は、AIの創造性と皆様の想像力が出会う特別な文学サロンです。<br><br>ここにある本はすべて実在しません。AIが紡ぎ出したあらすじと断片的な手がかりをきっかけに、まるで<strong>「その本を読んだかのように」</strong>想像し、感想を語り合う空間です。読んだことのない本について語り合う、わくわくする知的な遊びをお楽しみください！</div>",
        info_guide_rules: "<div class='info-section-label'><span>🤝</span> 必ず守るべき読書会の約束</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span><div><strong>「この本は存在する」と信じること：</strong>最も重要なルールです。「偽物の本だから」と考えるのではなく、本当に夜通し読んだ本であるかのように没入して語ってください。</div></div><div class='info-list-item'><span class='info-list-dot'></span><div><strong>創作への敬意：</strong>正解はありません。自分が想像した物語と他の読者が想像した物語が異なっていても、それはそれぞれ異なる感想を生んだ美しい創作物です。他者の考えを尊重し、耳を傾けてください。</div></div><div class='info-list-item'><span class='info-list-dot'></span><div><strong>自由な肉付け：</strong>本の内容だけでなく、作者の裏話、翻訳者の文体、デザイン、本の価格など、本を取り巻く外の世界まで自由に想像を膨らませていただいて構いません。</div></div></div>",
        info_guide_steps: "<div class='info-section-label'><span>🧭</span> 読書会に参加する：5ステップガイド</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 18px; margin-top: 10px;'><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>1</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>本を探す、または自分で生成する</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>ホーム画面で開かれている他の読書室を覗いてみましょう。または<strong>「新しい本を生成」</strong>ボタンを押して、AIが提案する3冊の候補の中からお好みの1冊を選び、読書室を開設することもできます。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>2</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>本の詳細情報と手がかりを読む</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>本の詳細ページに移動し、タイトル、あらすじ、書き出しの一文、推薦の言葉、出版社書評、そして<strong>「詳細目次」</strong>を読んでみましょう。各章のページと要約に目を通しながら、本の具体的な展開を頭の中に描くことが想像への第一歩です。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>3</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>記録を残す（評価と感想）</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>その本が気に入ったかどうか評価してみましょう。そして詳細ページ下部に<strong>「一言レビュー」や感想コメント</strong>を書いてみてください。他の人のユニークな感想にダブルクリックして共感を示したり、返信を残すこともできます。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>4</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>読書ディスカッションルームでリアルタイムに語り合う</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'><strong>「読書室に参加する」</strong>ボタンをクリックしてリアルタイムチャットルームに入室しましょう。読者同士自由にチャットができるほか、ウェルカムメッセージでのおすすめ質問の提示や、<code>@司会者</code>とメンションした際に裏設定を教えてくれる<strong>AI司会者</strong>とも心地よい会話を楽しめます。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: var(--accent); color: #fff; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>5</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>本棚に収める＆アーカイブを閲覧する</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>気に入った本は<strong>「書斎に追加」</strong>で本棚に保管できます。運営期間（約10日間）が終了しアーカイブされた本は、一生ものの愛蔵本のように大切に保存され、いつでも「アーカイブ」メニューから読書会の対話記録や反応の統計を、美しい上製本スタイルで読み返すことができます。</div></div></div></div>",
        info_guide_mod_role: "<div class='info-section-label'><span>🎙️</span> AI司会者の役割</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 14px; margin-top: 6px;'><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>1</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>おすすめディスカッション質問の提示</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>読書室に入ると最初のウェルカムカードとして、核心となるジレンマとおすすめのディスカッション質問を3つ提示し、気軽に会話を始められるようサポートします。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>2</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>控えめな質問ガイド</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>読者同士の自由な会話を妨げるような過度な口出しや介入はせず、議論の糸口となる端的な問いかけだけをすっきりと投げかけます。</div></div></div><div style='display: flex; gap: 12px; align-items: flex-start;'><div style='background: rgba(181,74,106,0.12); color: #b54a6a; font-family: var(--serif); font-weight: 700; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0;'>3</div><div><div style='font-weight: 700; color: var(--text); font-size: 13.5px; margin-bottom: 2px;'>@司会者 メンション会話</div><div style='font-size: 13px; color: var(--text-muted); line-height: 1.6;'>チャット欄で<code>@司会者</code>とメンションして質問を投げかけると、架空の書籍の世界観や作り込まれた人物設定について丁寧に説明してくれます。</div></div></div></div>",
        info_guide_qa: "<div class='info-section-label'><span>❓</span> 何でも聞いてください（Q&A）</div><div class='info-section-text' style='display: flex; flex-direction: column; gap: 16px; margin-top: 10px;'><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. 本当に本を読まずに参加してもいいのですか？</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>もちろんです！このプラットフォームにあるすべての本はAIがたった今作り出した本であり、<strong>作者自身もまだ書いていない状態</strong>です。したがって、どんな発言も不正解にはなり得ませんので、ためらわずに自由に第一印象を語ってみてください。</div></div><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. どんな感想を残せばいいのか分かりません。</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>迷ったときは、以下のヒントを参考に考えてみてください：<br>• <strong>書き出しの一文について：</strong>小説の最初の一文を見て、どんな雰囲気や場面が思い浮かびますか？<br>• <strong>物語の核心となるジレンマ：</strong>本の詳細ページに表示されているディスカッション質問（Q.）を読み、自分の価値観に照らして答えてみましょう。<br>• <strong>目次の展開：</strong>特定の章のタイトルや要約が気に入ったら、「この章では主人公がこんな行動を取ったのではないか」と提案してみてください。</div></div><div><div style='font-weight: 700; color: var(--accent); font-size: 14.5px; margin-bottom: 6px;'>Q. 著作権は誰にありますか？</div><div style='font-size: 13px; line-height: 1.6; color: var(--text);'>AIが出力した本の基本的な骨組み（タイトル、あらすじなど）は、著作権が認められないパブリックドメインに属します。しかし、これを基に<strong>読者様が創造的に残してくださった大切な感想、コメント、読書室での対話内容は、人間固有の著作物として完全に作成者（読者）に著作権が帰属</strong>します。他人の大切な解釈を無断で流用したり、貶めたりしないようお願いいたします。</div></div></div>",
        info_contact_title: "お問い合わせ",
        info_contact_s1: "<div class='info-section-label'>📬 お問い合わせ方法</div><div class='info-section-text'>サービスのご利用中にご不便な点やご意見がございましたら、下記のメールアドレスまでお問い合わせください。<br><br>担当者が確認の上、<strong>営業日基準で1〜3日以内</strong>にご返信いたします。</div>",
        info_contact_s2: "<div class='info-section-label'>✉ お問い合わせメール</div><div class='info-contact-email'>gakongbooks@gmail.com</div>",
        info_contact_s3: "<div class='info-section-label'>📋 お問い合わせの際にご記入ください</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> ご登録のメールアドレス</div><div class='info-list-item'><span class='info-list-dot'></span> お問い合わせの種類（アカウント、コンテンツ、技術的な問題など）</div><div class='info-list-item'><span class='info-list-dot'></span> 問題の状況を詳しくご説明いただけますと、迅速な対応の助けになります。</div></div>",
        info_contact_s4: "<div class='info-section-label'>⏰ 運営時間</div><div class='info-section-text'>平日 10:00〜18:00（土・日・祝日を除く）<br><span style='color:var(--text-faint);font-size:12px;'>運営時間外のお問い合わせは、翌営業日に順次対応いたします。</span></div>",
        info_terms_title: "利用規約",
        info_terms_s1: "<div class='info-section-label'>第1条（目的）</div><div class='info-section-text'>本規約は、架空読書会（Gakong Reading Club、以下「本サービス」）が提供するAIベースの仮想読書会サービスの利用に関し、本サービスと利用者との間の権利、義務及び責任事項を定めることを目的とします。</div>",
        info_terms_s2: "<div class='info-section-label'>第2条（サービス内容）</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> AIが生成した仮想書籍情報の提供</div><div class='info-list-item'><span class='info-list-dot'></span> 読書室への参加、コメント・評価・リアクション機能</div><div class='info-list-item'><span class='info-list-dot'></span> 個人書斎管理機能</div><div class='info-list-item'><span class='info-list-dot'></span> 終了した読書室のアーカイブ閲覧</div></div>",
        info_terms_s3: "<div class='info-section-label'>第3条（会員の義務）</div><div class='info-section-text'>利用者は、次の行為を行ってはなりません。<br><br><div class='info-list-item'><span class='info-list-dot'></span> 他人の個人情報の盗用または虚偽情報の登録</div><div class='info-list-item'><span class='info-list-dot'></span> サービスの運営を妨害する行為</div><div class='info-list-item'><span class='info-list-dot'></span> 他人への誹謗中傷、暴言など不健全な内容の投稿</div><div class='info-list-item'><span class='info-list-dot'></span> 商業目的の無断広告の投稿</div></div>",
        info_terms_s4: "<div class='info-section-label'>第4条（コンテンツについて）</div><div class='info-section-text'>本サービスのすべての書籍情報は、AIが生成した<strong>架空の創作物</strong>です。実在する本、作家、出版社とは一切関係がなく、価格も参考用の仮想価格です。</div>",
        info_terms_s5: "<div class='info-section-label'>第5条（規約の変更）</div><div class='info-section-text'>本サービスは、必要な場合に本規約を変更することができ、変更後の規約はサービス内のお知らせを通じて利用者にご案内します。<br><span style='color:var(--text-faint);font-size:12px;'>最終改定：2026年6月</span></div>",
        info_privacy_title: "プライバシーポリシー",
        info_privacy_s1: "<div class='info-section-label'>収集する個人情報</div><div class='info-section-text'><div class='info-list-item'><span class='info-list-dot'></span> メールアドレス（会員登録及び本人確認の目的）</div><div class='info-list-item'><span class='info-list-dot'></span> 匿名ニックネーム（サービス内表示の目的）</div><div class='info-list-item'><span class='info-list-dot'></span> 投稿されたコメント及びメッセージ（サービス運営の目的）</div></div>",
        info_privacy_s2: "<div class='info-section-label'>個人情報の利用目的</div><div class='info-section-text'>収集した個人情報は、会員管理、サービス提供、紛争解決の目的にのみ利用され、外部に提供されることはありません。</div>",
        info_privacy_s3: "<div class='info-section-label'>個人情報の保有期間</div><div class='info-section-text'>会員退会時に直ちに破棄します。ただし、関連法令により保存義務がある場合は、その期間中保管します。</div>",
        info_privacy_s4: "<div class='info-section-label'>利用者の権利</div><div class='info-section-text'>利用者は、いつでもご自身の個人情報の閲覧、修正、削除を請求することができます。<br>お問い合わせ：<strong>gakongbooks@gmail.com</strong><br><span style='color:var(--text-faint);font-size:12px;'>最終改定：2026年6月</span></div>"
      ,
        count_unit: "件",
        people_unit: "人",
        participants_joining: "人が参加中",
        closing_soon: "⚠ まもなく締切 · ",
        archive_badge: "アーカイブ",
        archive_open_btn: "📖 アーカイブを閲覧する",
        page_unit: "ページ",
        discount_note: "（10%割引価格）",
        delete_btn: "削除",
        view_horizontal: "⇄ 横読み",
        view_vertical: "↕ 縦読み",
        search_no_result: "該当なし",
        detail_rating_blind: "終了後に公開されます",
        detail_rating_blind_desc: "平均評価は読書室の終了後、アーカイブで公開されます。",
        detail_my_rating: "私の評価",
        detail_rating_locked: "読書室に参加すると評価を残せます",
        detail_join_short: "参加する",
        detail_chat_reactions: "チャットの反応",
        detail_rx_blind_desc: "チャットの総合反応は読書室の終了後、アーカイブで公開されます。",
        detail_rx_top: "最も多い反応",
        detail_no_endorsement: "推薦の言葉はまだ登録されていません。",
        detail_no_review: "出版社の書評は登録されていません。",
        detail_no_characters: "まだ情報が記録されていない登場人物です。",
        detail_ai_author_reply: "🤖 <strong>AI作家の一言:</strong> ",
        detail_zoom_hint: "🔍 拡大",
        detail_zoom_title: "クリックで表紙を拡大",
        detail_virtual_book: " · AI生成の架空書籍",
        detail_toc_empty: "詳細目次のデータがありません。",
        chat_room_suffix: " 読書室",
        chat_reply_writing: "さんに返信中",
        chat_reply_placeholder: "さんへ返信を書いてみましょう...",
        chat_default_placeholder: "この本について語り合いましょう...",
        chat_search_placeholder: "会話を検索...",
        chat_search_prev: "前の検索結果",
        chat_search_next: "次の検索結果",
        chat_reply_cancel: "返信をキャンセル",
        chat_topic_toggle: "折りたたむ/展開",
        chat_highlight_title: "作品ハイライト",
        chat_first_line: "📖 冒頭の一文",
        chat_famous_line: "💬 名セリフ",
        chat_room_opened: "📚 読書室が開かれました。",
        chat_open_date: "読書室の開設日",
        chat_history_suffix: " — チャット記録",
        chat_history_loading: "記録を読み込み中...",
        chat_history_readonly: " 件のメッセージ · 閲覧専用",
        chat_history_total: "全 ",
        chat_edited: "（編集済み）",
        toast_rating_done: "点の評価を残しました！",
        toast_already_lib: "すでに書斎にあります",
        toast_added_lib: "書斎に追加しました 📚",
        toast_removed_lib: "書斎から削除しました。",
        toast_login_for_lib: "ログイン後に書斎へ追加できます。",
        toast_login_required: "ログインが必要です。ログインページへ移動します。",
        toast_session_expired: "ログインセッションの有効期限が切れました。再度ログインしてください。",
        toast_input_empty: "内容を入力してください。",
        toast_edited: "編集しました。",
        toast_deleted: "削除しました。",
        toast_edit_failed: "メッセージの編集に失敗しました。",
        toast_delete_failed: "メッセージの削除に失敗しました。",
        toast_send_failed: "メッセージの送信に失敗しました。",
        toast_network_error: "ネットワークエラーが発生しました。",
        toast_no_self_rx: "自分のコメントには反応できません。",
        toast_login_for_rx: "ログイン後に反応を残せます。",
        toast_rx_failed: "反応の保存に失敗しました。",
        toast_book_created: " の召喚に成功しました！ 📚",
        toast_new_book_prefix: "✦ 新しい本 ",
        alert_login_to_gen: "新しい本を召喚するには、まずログインしてください！ 📖",
        alert_gen_failed: "新しい本の候補生成中にエラーが発生しました。",
        alert_adopt_failed: "選択中にエラーが発生しました。",
        alert_server_error: "サーバーと通信できません。",
        confirm_delete_book: "この書籍と読書室を完全に削除しますか？",
        confirm_delete_book_sub: "この操作は取り消せません。",
        alert_book_deleted: "書籍を削除しました。 🌲",
        alert_book_delete_failed: "書籍の削除に失敗しました。",
        auth_back: "← 戻る",
        auth_login_title: "おかえりなさい",
        auth_login_sub: "実在しない本たちが待っています。",
        auth_signup_title: "架空読書会へ<br>ようこそ",
        auth_signup_sub: "世界にない本を一緒に読みましょう。",
        auth_email: "メールアドレス",
        auth_password: "パスワード",
        auth_email_ph: "メールアドレスを入力してください",
        auth_password_ph: "パスワードを入力してください",
        auth_password_ph8: "8文字以上で入力してください",
        auth_email_invalid: "正しいメールアドレスの形式で入力してください。",
        auth_password_empty: "パスワードを入力してください。",
        auth_password_short: "パスワードは8文字以上である必要があります。",
        auth_forgot: "パスワードをお忘れですか？",
        auth_login_btn: "ログイン",
        auth_signup_btn: "新規登録",
        auth_logout_btn: "ログアウト",
        auth_no_account: "アカウントをお持ちではありませんか？",
        auth_has_account: "すでにアカウントをお持ちですか？",
        auth_nick_label: "✦ 付与された読書ニックネーム",
        auth_nick_loading: "ニックネームを読み込み中...",
        auth_gate_title: "私の書斎",
        auth_or: "または",
        alert_login_failed: "ログインに失敗しました。メールアドレスとパスワードをご確認ください。",
        alert_signup_done: "新規登録が完了しました！ 🎉 ログインしてください。",
        alert_signup_failed: "新規登録に失敗しました。",
        alert_nick_missing: "ニックネームが割り当てられていません。しばらくしてから再度お試しください。",
        alert_fill_all: "すべての項目を入力してください。",
        alert_pw_short: "新しいパスワードは8文字以上である必要があります。",
        alert_pw_mismatch: "新しいパスワードと確認用の入力が一致しません。",
        alert_pw_changed: "パスワードを変更しました。再度ログインしてください。 🔒",
        alert_pw_change_failed: "パスワードの変更に失敗しました。入力内容をご確認ください。",
        alert_pw_required_withdraw: "退会するにはパスワードの入力が必要です。",
        confirm_withdraw: "本当に架空読書会を退会しますか？",
        confirm_withdraw_sub: "退会するとすべてのデータが完全に削除されます。",
        alert_withdraw_done: "退会手続きが完了しました。ご利用ありがとうございました。",
        alert_withdraw_failed: "パスワードが一致しないため、退会処理に失敗しました。",
        confirm_logout: "ログアウトしますか？",
        toast_logout_done: "ログアウトしました。またお会いしましょう！ 👋",
        alert_email_required: "メールアドレスを入力してください。",
        alert_email_invalid: "正しいメールアドレスの形式で入力してください。",
        reset_sending: "リセットリンクを送信中...",
        reset_send_btn: "リセットリンクを受け取る",
        reset_sent: "登録済みのメールアドレスであれば、パスワード再設定リンクを送信しました。メールをご確認ください。 ✉️",
        alert_request_failed: "リクエストの処理に失敗しました。しばらくしてから再度お試しください。",
        profile_edit_title: "プロフィール編集",
        lib_book_detail_title: "書籍の詳細ページへ移動",
        lib_no_writings: "まだ投稿がありません。チャットで語り合ってみましょう。",
        lib_arc_empty: "参加した読書室が終了すると、ここにアーカイブが蓄積されます。",
        lib_arc_view: "アーカイブを見る",
        lib_arc_closed: " 終了 · 私の感想 ",
        lib_arc_included: "件を含む",
        edit_curr_pw_ph: "現在のパスワードを入力してください",
        edit_new_pw_ph: "8文字以上で入力してください",
        edit_confirm_pw_ph: "新しいパスワードをもう一度入力してください",
        withdraw_pw_ph: "退会確認のためパスワードを入力してください",
        genre_prev: "前のジャンル（左へ）",
        genre_next: "次のジャンル（右へ）",
        arc_view_toggle_title: "横読みに切り替え",
        arc_stat_chats: "チャットメッセージ",
        arc_stat_comments: "コメント",
        arc_stat_rx: "反応の総数",
        arc_stat_rating: "平均評価",
        arc_editorial_title: "編集者のことば",
        arc_participants_title: "今回の読書会の参加者 ",
        arc_participants_sub: "ニックネームは架空読書会のシステムがランダムに割り当てます。本名は公開されません。",
        arc_chapter1_num: "第1章",
        arc_chapter2_num: "第2章",
        arc_closing_title: "記録の保存",
        arc_col_publisher: "発行元",
        arc_col_editor: "企画・構成",
        arc_col_class: "書誌分類番号",
        arc_col_date: "保管開始日",
        arc_rx_total_prefix: "合計 ",
        arc_rx_total_suffix: "件の反応",
        arc_empty_lib: "参加した読書室が終了すると、ここにアーカイブが蓄積されます。",
        auth_gate_desc_all: "書斎を確認するにはログインが必要です。<br>架空読書会のアカウントで、<br>あなただけの読書記録を始めましょう。",
        auth_nick_desc_all: "登録と同時にランダムで割り当てられるニックネームです。<br>読書室ではこの名前で活動します。",
        auth_terms_all: "登録すると、架空読書会の利用規約および<br>プライバシーポリシーに同意したものとみなされます。",
        fallback_book_title: "架空の書籍",
        fallback_book_author: "架空の作家",
        arc_month_unknown: "終了日不明",
        arc_month_empty: "まだ終了した読書室はありません。",
        arc_book_unit: "冊",
        arc_card_overlay: "📦 アーカイブ閲覧",
        arc_closed_suffix: " 終了",
        arc_year_unit: "年",
        arc_month_unit: "か月",
        arc_more_btn: "以前のアーカイブをもっと見る",
        toast_pending_restored: "まだ選んでいない候補があるため、そのまま表示します 📖",
        reset_modal_title: "✉️ パスワード再設定",
        reset_modal_desc: "ご登録のメールアドレスを入力してください。<br>パスワードを再設定できるリンクをメールでお送りします。（リンクの有効期限は30分）",
        reset_modal_email_label: "登録メールアドレス",
        detail_days_left: "日残り",
        detail_end_suffix: " 終了",
        detail_always_open: "常時開室",
        detail_ended_label: "終了",
        detail_ended_cap: "この読書室は終了し、アーカイブに保管されています。",
        detail_cap_always: "常時開いている読書室です。いつでも参加できます。",
        detail_cap_last: "最終日 · 今日の感想がアーカイブに残ります。",
        detail_cap_soon_a: "全",
        detail_cap_soon_b: "日中 ",
        detail_cap_soon_c: "日経過 · 終了するとアーカイブに保管されます。",
        detail_cap_early: "今なら最初から一緒に読めます。",
        detail_colophon_title: "架空の奥付",
        detail_colophon_pages: "分量",
        detail_colophon_price: "定価",
        detail_colophon_tags: "キーワード",
        detail_rx_live_label: "この読書室の反応",
        detail_rx_live_badge: "リアルタイム",
        detail_rx_empty: "まだ反応がありません。",
        detail_rx_empty_cta: "最初の感想を残してみましょう →",
        detail_rating_folded: "平均評価 · 星の分布",
        arc_stat_readers: "参加読者",
        arc_participants_unit: "人",
      }
    };

    // 현재 언어의 문구를 가져온다. 화면에 나가는 한국어 문자열은 모두 이 함수를 거친다.
    //   t('auth_login_btn')            → 사전 값
    //   t('없는키', '기본 문구')        → 사전에 없으면 fallback
    // 새 문구를 추가할 때는 I18N_DICT의 ko/ja 양쪽에 키를 넣고 t()로 부르면 된다.
    function t(key, fallback) {
      var dict = I18N_DICT[CURRENT_LANG] || I18N_DICT.ko;
      if (dict && dict[key] !== undefined) return dict[key];
      if (I18N_DICT.ko && I18N_DICT.ko[key] !== undefined) return I18N_DICT.ko[key];
      return fallback !== undefined ? fallback : '';
    }
    window.t = t;

    function setLanguage(lang) {
      if (lang !== 'ko' && lang !== 'ja') lang = 'ko';
      CURRENT_LANG = lang;
      localStorage.setItem('app_lang', lang);
      // <html lang>을 바꿔야 언어별 폰트 스택(styles.css의 html[lang="ja"])이 적용된다.
      document.documentElement.setAttribute('lang', lang);

      var btnKo = document.getElementById('lang-btn-ko');
      var btnJa = document.getElementById('lang-btn-ja');
      if (btnKo && btnJa) {
        if (lang === 'ja') {
          btnKo.classList.remove('active');
          btnJa.classList.add('active');
        } else {
          btnJa.classList.remove('active');
          btnKo.classList.add('active');
        }
      }

      var dict = I18N_DICT[lang] || I18N_DICT.ko;
      document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        if (dict[key]) {
          el.innerHTML = dict[key];
        }
      });

      // 텍스트가 아닌 속성(placeholder / title)도 함께 번역한다.
      document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
        var key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) el.placeholder = dict[key];
      });
      document.querySelectorAll('[data-i18n-title]').forEach(function(el) {
        var key = el.getAttribute('data-i18n-title');
        if (dict[key]) el.title = dict[key];
      });

      var genBtn = document.getElementById('gen-btn');
      if (genBtn) genBtn.innerHTML = dict.gen_btn;

      var heroLabel = document.querySelector('.hero-label');
      if (heroLabel) heroLabel.textContent = dict.hero_label;

      var heroTitle = document.querySelector('.hero-title');
      if (heroTitle) heroTitle.innerHTML = dict.hero_title;

      var heroDesc = document.querySelector('.hero-desc');
      if (heroDesc) heroDesc.innerHTML = dict.hero_desc;

      var chatInput = document.getElementById('chat-input');
      if (chatInput) chatInput.placeholder = dict.chat_input_placeholder;

      if (typeof renderHome === 'function') renderHome();
      if (typeof renderLib === 'function') renderLib();

      // 상세/채팅처럼 이미 열려 있는 화면도 다시 그려야 언어가 반영된다.
      var openPage = document.querySelector('[id^=pg-].active');
      if (openPage && currentBook) {
        if (openPage.id === 'pg-detail' && typeof openDetail === 'function') openDetail(currentBook.id);
        if (openPage.id === 'pg-chat' && typeof renderChat === 'function') renderChat(currentBook.id);
      }
      if (typeof updateAuthUI === 'function') updateAuthUI();
    }

    window.setLanguage = setLanguage;

    // 저장된 언어를 페이지 로드 시 한 번 적용한다.
    // (이 호출이 없으면 새로고침했을 때 정적 텍스트만 한국어로 되돌아가고,
    //  <html lang>이 갱신되지 않아 일본어 폰트도 적용되지 않는다)
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { setLanguage(CURRENT_LANG); });
    } else {
      setLanguage(CURRENT_LANG);
    }
