#!/bin/bash
# 운영 DB를 날마다 떠 둔다.
#
# 인스턴스가 날아가면 쌓인 책과 대화가 함께 사라진다. 저장소의
# data/full_backup.json은 한 시점의 자료라 그 뒤의 기록은 들어 있지 않다.
#
# cron에 걸어 쓴다(새벽 4시):
#   0 4 * * * /home/ubuntu/-Gakongbooks-/scripts/backup_db.sh >> /var/log/gakong-backup.log 2>&1
#
# 되돌릴 때:
#   gunzip -c ~/backups/gakong_db_2026-10-07.sql.gz | mysql -u gakong -p gakong_db

set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups}"
KEEP_DAYS="${KEEP_DAYS:-14}"
STAMP="$(date +%F)"

# 접속 정보는 .env의 DATABASE_URL에서 꺼낸다. 비밀번호를 이 파일에 적지 않는다.
# 형식: mysql+pymysql://사용자:비밀번호@호스트:포트/DB이름
DB_URL="$(grep -E '^DATABASE_URL=' "$APP_DIR/.env" | head -1 | cut -d= -f2- | tr -d '"'"'"'')"
if [ -z "$DB_URL" ]; then
  echo "[backup] .env에서 DATABASE_URL을 찾지 못했습니다." >&2
  exit 1
fi

CRED="${DB_URL#*://}"            # 사용자:비밀번호@호스트:포트/DB
USERPASS="${CRED%%@*}"
HOSTDB="${CRED#*@}"
DB_USER="${USERPASS%%:*}"
DB_PASS="${USERPASS#*:}"
DB_NAME="${HOSTDB##*/}"
DB_NAME="${DB_NAME%%\?*}"        # 뒤에 ?옵션이 붙어 있으면 떼어낸다
DB_HOST="${HOSTDB%%:*}"

mkdir -p "$BACKUP_DIR"
OUT="$BACKUP_DIR/${DB_NAME}_${STAMP}.sql.gz"

# 비밀번호를 명령줄에 쓰면 ps로 다른 사용자에게 보인다. 환경변수로 넘긴다.
# --no-tablespaces: 앱 계정은 자기 DB에만 권한이 있어 테이블스페이스를 읽지 못한다.
# 권한을 올리는 대신 필요 없는 조회를 끈다(최소 권한 계정을 그대로 둔다).
MYSQL_PWD="$DB_PASS" mysqldump \
  --host="$DB_HOST" --user="$DB_USER" \
  --single-transaction --quick --default-character-set=utf8mb4 \
  --no-tablespaces \
  "$DB_NAME" | gzip > "$OUT"

SIZE="$(du -h "$OUT" | cut -f1)"
echo "[backup] $(date '+%F %T') $OUT ($SIZE)"

# 오래된 것은 지운다. 디스크가 차면 서비스까지 멈춘다.
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -mtime "+$KEEP_DAYS" -delete
echo "[backup] 보관 중인 백업: $(find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" | wc -l)개 (최근 ${KEEP_DAYS}일)"
