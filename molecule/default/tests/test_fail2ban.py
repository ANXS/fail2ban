"""Behavioral tests for the ANXS.fail2ban role."""

import time


def _banned_ips(host, jail):
    result = host.run("fail2ban-client get %s banip", jail)
    assert result.rc == 0, result.stderr
    return set(result.stdout.split())


def _wait_for_server(host, attempts=30):
    """Block until the daemon answers on its client socket.

    systemctl returns once the server has forked, which is before the server
    has created the socket that every fail2ban-client call needs.
    """
    for _ in range(attempts):
        if host.run("fail2ban-client ping").rc == 0:
            return
        time.sleep(1)
    result = host.run("fail2ban-client ping")
    assert result.rc == 0, result.stdout + result.stderr


def _wait_for_ban(host, jail, address, expected, attempts=10):
    for _ in range(attempts):
        if (address in _banned_ips(host, jail)) == expected:
            return
        time.sleep(1)
    assert (address in _banned_ips(host, jail)) == expected


def test_fail2ban_package_and_service(host):
    package = host.package("fail2ban")
    service = host.service("fail2ban")

    assert package.is_installed
    assert service.is_running
    assert service.is_enabled


def test_assembled_configuration_is_valid(host):
    result = host.run("fail2ban-client -t")
    assert result.rc == 0, result.stdout + result.stderr


def test_structured_jail_supports_per_jail_firewall_options(host):
    content = host.file("/etc/fail2ban/jail.local").content_string
    section = content.split("[structured-service]", 1)[1]

    assert "banaction = dummy" in section
    assert "chain = DOCKER-USER" in section
    assert "port = 443" in section


def test_managed_files_are_reconciled(host):
    manifest = host.file(
        "/var/lib/fail2ban/ansible-managed/filters.list"
    ).content_string.splitlines()

    assert manifest
    assert not host.file("/etc/fail2ban/filter.d/retired.conf").exists
    for name in manifest:
        managed_file = host.file("/etc/fail2ban/filter.d/" + name)
        assert managed_file.exists
        assert managed_file.user == "root"
        assert managed_file.mode == 0o644


def test_reload_preserves_active_ban(host):
    address = "198.51.100.41"
    jail = "test-role"

    try:
        result = host.run("fail2ban-client set %s banip %s", jail, address)
        assert result.rc == 0, result.stdout + result.stderr
        _wait_for_ban(host, jail, address, True)

        result = host.run("fail2ban-client reload")
        assert result.rc == 0, result.stdout + result.stderr
        _wait_for_ban(host, jail, address, True)
    finally:
        host.run("fail2ban-client set %s unbanip %s", jail, address)

    _wait_for_ban(host, jail, address, False)


def test_ban_persists_across_restart(host):
    address = "198.51.100.42"
    jail = "test-role"

    try:
        result = host.run("fail2ban-client set %s banip %s", jail, address)
        assert result.rc == 0, result.stdout + result.stderr
        _wait_for_ban(host, jail, address, True)

        result = host.run("systemctl restart fail2ban")
        assert result.rc == 0, result.stdout + result.stderr
        _wait_for_server(host)
        _wait_for_ban(host, jail, address, True)
    finally:
        host.run("fail2ban-client set %s unbanip %s", jail, address)


def test_textfile_collector_publishes_metrics(host):
    result = host.run("systemctl start fail2ban-textfile.service")
    assert result.rc == 0, result.stdout + result.stderr

    metric = host.file(
        "/var/lib/fail2ban-exporter/metrics/fail2ban.prom"
    )
    link = host.file("/opt/prometheus/textfiles/fail2ban.prom")
    timer = host.service("fail2ban-textfile.timer")

    assert metric.exists
    assert "f2b_jail_count" in metric.content_string
    assert link.is_symlink
    assert timer.is_running
    assert timer.is_enabled


def _normalized_form(analyze_stdout):
    for line in analyze_stdout.splitlines():
        if line.strip().startswith("Normalized form:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError("no normalized form in: " + analyze_stdout)


def test_textfile_timer_schedule_is_timezone_pinned(host):
    """An unpinned OnCalendar spec skips the entire repeated hour at DST
    fall-back, stalling the collector for ~60min and staling every metric it
    writes -- while the timer still reports active and enabled."""
    unit = host.file("/etc/systemd/system/fail2ban-textfile.timer")
    spec = next(
        line.split("=", 1)[1].strip()
        for line in unit.content_string.splitlines()
        if line.startswith("OnCalendar=")
    )

    pinned = host.run("systemd-analyze calendar %s", spec)
    assert pinned.rc == 0, pinned.stdout + pinned.stderr

    # Drop the trailing token and re-normalize. If the suffix were absent or
    # inert, both forms would match -- so this fails iff the pin is missing,
    # without restating which timezone the role defaults to.
    bare = host.run("systemd-analyze calendar %s", spec.rsplit(" ", 1)[0])
    assert bare.rc == 0, bare.stdout + bare.stderr
    assert _normalized_form(pinned.stdout) != _normalized_form(bare.stdout)
