auth            required	pam_faillock.so preauth silent audit deny=3 unlock_time=600
auth            sufficient	pam_unix.so {{ nullok }} try_first_pass
auth            [default=die]   pam_faillock.so authfail audit deny=3 unlock_time=600
{% if passwdqc -%}
password	required	pam_passwdqc.so min=8,8,8,8,8 retry=3
{% endif -%}
{% if krb5 -%}
password	[success=1 default=ignore]	pam_krb5.so {{ krb5_params }}
{% endif -%}
password	required	pam_unix.so try_first_pass {{ unix_authtok|default('', true) }} {{ nullok }} {{ unix_extended_encryption|default('', true) }} {{ debug }}
password	optional	pam_permit.so
