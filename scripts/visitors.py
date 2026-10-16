# -*- coding: utf-8 -*-
"""nginx 접속 로그에서 실제 방문자만 본다.

실행(서버):  sudo python3 scripts/visitors.py

 '사람'으로 보이는 방문만 추려 날짜별로 정리한다.
봇·스캐너·헬스체크·정적 파일 요청은 뺀다."""
import glob
import gzip
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(errors="replace")
LINE = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d{3}) \S+ "([^"]*)" "([^"]*)"')
BOT = re.compile(r"bot|crawl|spider|python|curl|wget|go-http|zgrab|censys|masscan|nmap|scan|fetch|headless|http-client|libwww|java/|okhttp|dataprovider|expanse|palo alto|nuclei|nikto", re.I)

visits = defaultdict(lambda: defaultdict(lambda: {"pages": 0, "api": 0, "login": 0, "gen": 0, "chat": 0, "ua": "", "first": "", "last": "", "scan404": 0}))
for path in sorted(glob.glob("/var/log/nginx/access.log*")):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", errors="replace") as f:
        for raw in f:
            m = LINE.match(raw)
            if not m:
                continue
            ip, ts, method, url, status, ref, ua = m.groups()
            day = ts.split(":")[0]
            if not ua or ua == "-" or BOT.search(ua) or "Mozilla" not in ua:
                continue
            rec = visits[day][ip]
            rec["ua"] = "모바일" if re.search(r"Mobile|Android|iPhone", ua) else "PC"
            hhmm = ts.split(":")[1] + ":" + ts.split(":")[2]
            rec["first"] = rec["first"] or hhmm
            rec["last"] = hhmm
            if status == "404" and not url.startswith("/api/"):
                rec["scan404"] += 1
            if url == "/" and status == "200":
                rec["pages"] += 1
            elif url.startswith("/api/"):
                rec["api"] += 1
                if url.startswith("/api/auth/login") and method == "POST" and status == "200":
                    rec["login"] += 1
                if url.startswith("/api/books/candidates") and method == "POST":
                    rec["gen"] += 1
                if "/chats" in url and method == "POST":
                    rec["chat"] += 1

for day in visits:
    rows = [(ip, r) for ip, r in visits[day].items() if r["pages"] > 0 and r["api"] > 0 and r["scan404"] < 5 and ip != "127.0.0.1"]
    if not rows:
        continue
    print(f"=== {day} : 실제 방문 {len(rows)}명 ===")
    for ip, r in sorted(rows, key=lambda x: x[1]["first"]):
        acts = []
        if r["login"]: acts.append("로그인")
        if r["gen"]: acts.append("책 생성")
        if r["chat"]: acts.append(f"채팅 {r['chat']}건")
        print(f"  {ip:<16} {r['ua']:<4} {r['first']}~{r['last']}  홈 {r['pages']}회, API {r['api']}회  {' · '.join(acts)}")
