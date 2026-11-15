# Fail2ban jail examples

Every item below belongs under `fail2ban_services`.

## SSH

```yaml
fail2ban_services:
  - name: "sshd"
    enabled: true
    port: "ssh"
    filter: "sshd"
    logpath: "/var/log/auth.log"
    maxretry: 6
```

## Web authentication behind Docker

```yaml
fail2ban_services:
  - name: "proxy-auth"
    enabled: true
    port: "http,https"
    filter: "proxy-auth"
    backend: "systemd"
    journalmatch: "_SYSTEMD_UNIT=docker.service CONTAINER_TAG=proxy"
    maxretry: 6
    banaction: "iptables-multiport"
    chain: "DOCKER-USER"
```

## Postfix

```yaml
fail2ban_services:
  - name: "postfix"
    enabled: true
    port: "smtp,submission,465"
    filter: "postfix"
    logpath: "/var/log/mail.log"
    maxretry: 6
```

Any scalar fail2ban jail option may be supplied. Sequence values are rendered
as space-separated values.
