# ANXS.fail2ban

[![Molecule CI](https://github.com/ANXS/fail2ban/actions/workflows/ci.yml/badge.svg)](https://github.com/ANXS/fail2ban/actions/workflows/ci.yml)

Install and configure fail2ban on supported Debian and Ubuntu releases.

## Requirements

- Ansible 2.14 or newer
- Debian 12 or 13
- Ubuntu 20.04, 22.04, or 24.04

## Usage

```yaml
- hosts: servers
  become: true
  roles:
    - role: ANXS.fail2ban
      fail2ban_bantime: "1h"
      fail2ban_findtime: "10m"
      fail2ban_maxretry: 5
      fail2ban_services:
        - name: "sshd"
          enabled: true
          port: "ssh"
          filter: "sshd"
          logpath: "/var/log/auth.log"
```

Each `fail2ban_services` item requires `name`. Every other key is rendered as
an option in that jail, so supported fail2ban options do not need corresponding
role releases.

Docker-published services usually require jail-specific firewall settings:

```yaml
fail2ban_services:
  - name: "proxy-auth"
    enabled: true
    filter: "proxy-auth"
    backend: "systemd"
    journalmatch: "_SYSTEMD_UNIT=docker.service CONTAINER_TAG=proxy"
    port: "http,https"
    banaction: "iptables-multiport"
    chain: "DOCKER-USER"
```

See [services_examples.md](services_examples.md) for additional examples.

## Variables

The defaults are documented in [defaults/main.yml](defaults/main.yml). The main
groups are:

- package selection: `fail2ban_package_version`
- global jail defaults: `fail2ban_bantime`, `fail2ban_findtime`,
  `fail2ban_maxretry`, `fail2ban_backend`, `fail2ban_banaction`
- daemon paths and database retention: `fail2ban_socket`,
  `fail2ban_pidfile`, `fail2ban_dbfile`, `fail2ban_dbpurgeage`
- structured jails: `fail2ban_services`
- controller-side files: `fail2ban_extra_filters`,
  `fail2ban_extra_jails`, `fail2ban_extra_configs`

The role records the basenames it deploys under
`fail2ban_managed_state_dir`. A later run removes recorded files that are no
longer configured without touching package or operator-owned files.

## Validation

Every run:

1. validates each extra filter with `fail2ban-regex`;
2. checks configured sample lines from `fail2ban_filter_test_lines`; and
3. runs `fail2ban-client -t` against the assembled configuration before any
   reload or restart handler runs.

For example:

```yaml
fail2ban_filter_test_lines:
  proxy-auth: "192.0.2.25 authentication failed"
```

## Prometheus textfile collector

Set `fail2ban_textfile_enabled: true` to install a systemd timer that writes
metrics atomically for node_exporter's textfile collector.

The node_exporter-owned `fail2ban_textfile_dir` must already exist. Persistent
metrics live in `fail2ban_textfile_state_dir`; a systemd-tmpfiles rule links
them into the collector directory after boot.

The schedule is evaluated in `fail2ban_textfile_timezone`, which defaults to
`UTC`. This matters: a `systemd` calendar spec without a timezone is evaluated
in local time, and at a DST fall-back it skips the **entire repeated hour**.
The timer stays `active` and `enabled` throughout, so the only symptom is ~60
minutes of unchanging metrics — which reads as a dead collector to any
staleness alert. Pinning the schedule to a zone without DST removes the gap.

Set `fail2ban_textfile_timezone: ""` to evaluate in local wall-clock time
instead. Do that only if you also widen any staleness alerting past an hour,
and note that an explicit DST-observing zone (`Europe/Berlin`) is exposed to
the same stall as local time.

## Development

```console
make lint
make test-debian12
make test
```

`make test` runs lint plus the Molecule/Testinfra suite on Debian 12/13 and
Ubuntu 20.04/22.04/24.04. Tags trigger the Ansible Galaxy release workflow.

## License

MIT. See [LICENSE](LICENSE).
