### ANXS - fail2ban: List of service examples

###### ssh/dropbear/...
```yaml
  - name: ssh
    enabled: "true"
    port: ssh
    filter: sshd
    logpath: /var/log/auth.log
```

###### Generic filter for pam
```yaml
fail2ban_services:
  - name: pam-generic
    enabled: "true"
    port: all
    filter: pam-generic
    logpath: /var/log/auth.log
    maxretry: 6
    banaction: iptables-allports
```

###### xinetd-fail
```yaml
fail2ban_services:
  - name: xinetd-fail
    enabled: "true"
    port: all
    filter: xinetd-fail
    logpath: /var/log/daemon.log
    maxretry: 2
    banaction: iptables-multiport-log
```

###### ssh-ddos
```yaml
fail2ban_services:
  - name: ssh-ddos
    enabled: "true"
    port: ssh
    filter: ssh-ddos
    logpath: /var/log/auth.log
    maxretry: 6
```

###### apache
```yaml
fail2ban_services:
  - name: apache
    enabled: "true"
    port: http,https
    filter: apache-auth
    logpath: /var/log/apache*/*error.log
    maxretry: 6
```

###### apache-multiport
```yaml
fail2ban_services:
  - name: apache-multiport
    enabled: "true"
    port: http,https
    filter: apache-auth
    logpath: /var/log/apache*/*error.log
    maxretry: 6
    banaction:
```

###### apache-noscript
```yaml
fail2ban_services:
  - name: apache-noscript
    enabled: "true"
    port: http,https
    filter: apache-noscript
    logpath: /var/log/apache*/*error.log
    maxretry: 6
```

###### apache-overflows
```yaml
fail2ban_services:
  - name: apache-overflows
    enabled: "true"
    port: http,https
    filter: apache-overflows
    logpath: /var/log/apache*/*error.log
    maxretry: 2
```

###### vsftpd
```yaml
fail2ban_services:
  - name: vsftpd
    enabled: "true"
    port: ftp,ftp-data,ftps,ftps-data
    filter: vsftpd
    logpath: /var/log/vsftpd.log
    maxretry: 6
```

###### proftpd
```yaml
fail2ban_services:
  - name: proftpd
    enabled: "true"
    port: ftp,ftp-data,ftps,ftps-data
    filter: proftpd
    logpath: /var/log/proftpd/proftpd.log
    maxretry: 6
```

###### postfix
```yaml
fail2ban_services:
  - name: postfix
    enabled: "true"
    port: smtp, ssmtp
    filter: postfix
    logpath: /var/log/mail.log
    maxretry: 6
```

###### couriersmtp
```yaml
fail2ban_services:
  - name: couriersmtp
    enabled: "true"
    port: smtp,ssmtp
    filter: couriersmtp
    logpath: /var/log/mail.log
    maxretry: 6
```

###### courierauth
```yaml
fail2ban_services:
  - name: courierauth
    enabled: "true"
    port: smtp,ssmtp,imap2,imap3,imaps,pop3,pop3s
    filter: courierlogin
    logpath: /var/log/mail.log
    maxretry: 6
```

###### sasl
```yaml
fail2ban_services:
  - name: sasl
    enabled: "true"
    port: smtp,ssmtp,imap2,imap3,imaps,pop3,pop3s
    filter: sasl
    logpath: /var/log/mail.log
    maxretry: 6
```

###### dovecot
```yaml
fail2ban_services:
  - name: dovecot
    enabled: "true"
    port: smtp,ssmtp,imap2,imap3,imaps,pop3,pop3s
    filter: dovecot
    logpath: /var/log/mail.log
    maxretry: 6
```
