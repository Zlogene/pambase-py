{% import "templates/config/basic-conf.tpl" as basic with context -%}
{% import "templates/config/linux-pam-conf.tpl" as linux with context -%}

{% if linux.ns.faillock -%}
auth            required	pam_faillock.so preauth silent audit deny=3 unlock_time=600
auth            sufficient	pam_unix.so {{basic.ns.nullok}} try_first_pass
auth            [default=die]   pam_faillock.so authfail audit deny=3 unlock_time=600
{% endif -%}

{% if passwdqc -%}
password	required	pam_passwdqc.so min=8,8,8,8,8 retry=3
{% endif -%}

{% if krb5 -%}
password	[success=1 default=ignore]	pam_krb5.so {{basic.ns.krb5_params}}
{% endif -%}

password	required	pam_unix.so try_first_pass {{basic.ns.unix_authtok}} {{basic.ns.nullok}} {{basic.ns.unix_extended_encryption}} {{basic.ns.debug_value}}
## This is needed to make sure that the Kerberos skip-on-success won't cause a bad jump.
password	optional	pam_permit.so
