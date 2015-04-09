## ANXS - fail2ban [![Build Status](https://travis-ci.org/ANXS/fail2ban.png)](https://travis-ci.org/ANXS/fail2ban)

Ansible role which installs and configures fail2ban, a utility that watches logs for failed login attempts and blocks repeat offenders with firewall rules.


#### Requirements & Dependencies
- Tested on Ansible 1.4 or higher.


#### Variables

- `fail2ban_loglevel` - sets the loglevel output (1 = ERROR, 2 = WARN, 3 = INFO, 4 = DEBUG; default is 3)
- `fail2ban_logtarget1` - set the log target. This could be a file, SYSLOG, STDERR or STDOUT
- `fail2ban_syslog_target`
- `fail2ban_syslog_facility`
- `fail2ban_socket` - sets the socket file, which is used to communicate with the daemon

- `fail2ban_ignoreip` - which IP address/CIDR mask/DNS host should be ignored from fail2ban's actions
- `fail2ban_bantime` - sets the bantime
- `fail2ban_maxretry` - maximum number of retries before the host is put into jail
- `fail2ban_backend` - specifies the backend used to get files modification
- `fail2ban_email` - email address which can be used in the interpolation of the `fail2ban_services`
- `fail2ban_banaction` - sets the global/default banaction (can be overriden on a per role basis)
- `fail2ban_mta` - email action
- `fail2ban_protocol` - sets the default protocol
- `fail2ban_chain` - specifies the chain where jumps would need to be added in iptables-* actions
- `fail2ban_action` - default action

For each of the services you wish to protect/put a jail or ban up for, you need to add it to the `fail2ban_services` list of hashes:

```yaml
fail2ban_services:
  - name: "ssh"
    enabled: "true"
    port: "ssh"
    filter: "sshd"
    logpath: "/var/log/auth.log"
    maxretry: 6
    protocol: "tcp"                     (optional)
    action: "action_ "                  (optional)
    banaction: "iptables-multiport"     (optional)
```

There's a list of [service examples](services_examples.md) to help you.


#### Testing
This project comes with a VagrantFile, this is a fast and easy way to test changes to the role, fire it up with `vagrant up`

See [vagrant docs](https://docs.vagrantup.com/v2/) for getting setup with vagrant


#### License

Licensed under the MIT License. See the LICENSE file for details.


#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/ANXS/fail2ban/issues)!
