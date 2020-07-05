## This is essentially a config handling file
## It replaces the old 'basic-conf' and 'linux-pam-conf' files

## We (ab)use namespaces to try hide abstracct some of the logic
## away from the actual templates.

## Any variables which you want to access, that are defined
## with an if, must be stored in the ns (or another namespace)
{% set ns = namespace(debug_value="", authtok="use_authtok", unix_authtok="", unix_extended_encryption="", likeauth="", nullok="") -%}

## basic-conf
{% if krb5 and passwdqc -%}
	{% set ns.krb5_authtok=ns.authtok -%}
{% endif -%}

{% if krb5 or passwdqc -%}
	{% set ns.unix_authtok=ns.authtok -%}
{% endif -%}

## Blank string if not explicitly enabled
{% if debug == "yes" -%}
	{% set ns.debug_value = "debug" -%}
{% endif -%}

{% if not 'unix-extended-encryption' == "yes" -%}
	{% set ns.unix_extended_encryption="" -%}
{% endif -%}

{% if not likeauth == "yes" -%}
	{% set ns.likeauth="" -%}
{% endif -%}

{% if nullok == "yes" -%}
	{% set ns.nullok="nullok" -%}
{% endif -%}

{% if krb5 -%}
	{% set ns.krb5_params = ns.debug_value -%}
	{% set ns.krb5_params = ns.krb5_params + " ignore_root try_first_pass" -%}
{% endif -%}
