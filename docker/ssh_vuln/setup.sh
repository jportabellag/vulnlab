#!/bin/sh
set -eu

mkdir -p /var/run/sshd /srv/backups /opt/scripts /opt/staging/helpdesk

useradd -m -s /bin/bash user
echo "user:password" | chpasswd

useradd -m -s /bin/bash analyst
echo "analyst:Winter2024!" | chpasswd

cat <<'EOF' > /etc/motd
Authorized systems only.
Reminder: archive exports still run through the legacy reporting path.
EOF

cat <<'EOF' > /opt/staging/helpdesk/vpn-reset.txt
VPN refresh completed for Q4.
Assigned operator: analyst
Temporary password: Winter2024!
Rotate after the archive migration window.
EOF

cat <<'EOF' > /opt/staging/helpdesk/ticket-1048.txt
User reports that the weekly support bundle still contains authentication notes.
Action item: move the export out of /srv/backups before the next release.
EOF

tar -czf /srv/backups/helpdesk-export.tgz -C /opt/staging/helpdesk .
chmod 644 /srv/backups/helpdesk-export.tgz
rm -rf /opt/staging/helpdesk

cat <<'EOF' > /usr/local/bin/backup_reports.sh
#!/bin/sh
set -eu

cd /home/analyst/reports
/bin/tar -czf /srv/backups/reports-archive.tgz *
echo "Report archive refreshed"
EOF

chmod 755 /usr/local/bin/backup_reports.sh
chown root:root /usr/local/bin/backup_reports.sh

echo 'analyst ALL=(root) NOPASSWD: /usr/local/bin/backup_reports.sh' > /etc/sudoers.d/vulnlab
chmod 440 /etc/sudoers.d/vulnlab

cat <<'EOF' > /etc/cron.daily/logrotate-backup
#!/bin/sh
/usr/local/bin/backup_reports.sh >/dev/null 2>&1
EOF

chmod 755 /etc/cron.daily/logrotate-backup

cat <<'EOF' > /home/user/readme.txt
Initial foothold account.
Look for archive leftovers and account reuse after access.
EOF

cat <<'EOF' > /home/analyst/.bash_history
sudo -l
sudo /usr/local/bin/backup_reports.sh
EOF

cat <<'EOF' > /home/analyst/notes.txt
Weekly reports are packed from ~/reports by the legacy root wrapper.
Do not leave temporary files behind after QA runs.
EOF

mkdir -p /home/analyst/reports
cat <<'EOF' > /home/analyst/reports/weekly-summary.txt
Revenue trend is stable.
Archive again before Friday.
EOF

chown user:user /home/user/readme.txt
chown analyst:analyst /home/analyst/.bash_history
chown analyst:analyst /home/analyst/notes.txt
chown -R analyst:analyst /home/analyst/reports
