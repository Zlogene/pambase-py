## This is essentially a config handling file

## We (ab)use namespaces to try hide abstract some of the logic
## away from the actual templates.

## Any variables which you want to access, that are defined
## with an if, must be stored in the ns (or another namespace)
{% set ns = namespace(motd=0, mail=0, lastlog=0, faillock=0) -%}

## linux-pam-conf

{% if minimal == "no" -%}
        {% set ns.motd = 1 %}
        {% set ns.mail = 1 %}
        {% set ns.lastlog = 1 %}
        {% set ns.faillock = 1 %}
{% endif -%}
