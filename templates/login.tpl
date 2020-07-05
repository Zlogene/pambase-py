{% import "templates/config/basic-conf.tpl" as config with context -%}

{% if securetty -%}
auth       required     pam_securetty.so
{% endif -%}

auth       include	system-local-login
account	   include	system-local-login
password   include	system-local-login
session	   optional     pam_lastlog.so {{ config.ns.debug_value }}
session	   include      system-local-login
