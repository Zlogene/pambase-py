#if HAVE_SHELLS
auth		required	pam_shells.so DEBUG
#endif
#if SUPPORT_NOLOGIN_AUTH
auth		required	pam_nologin.so DEBUG_NOLOGIN
#endif
auth		include		system-auth

#if HAVE_FAILLOCK
auth            required        pam_faillock.so preauth silent audit deny=3 unlock_time=600
auth            sufficient      pam_unix.so nullok try_first_pass
auth            [default=die]   pam_faillock.so authfail audit deny=3 unlock_time=600
#endif

#if HAVE_ACCESS
account		required	pam_access.so DEBUG
#endif
#if HAVE_LOGIN_ACCESS
account		required	pam_login_access.so
#endif
#if SUPPORT_NOLOGIN_ACCOUNT
account		required	pam_nologin.so DEBUG_NOLOGIN
#endif
account		include		system-auth

#if HAVE_FAILLOCK
account         required        pam_faillock.so
#endif

password	include		system-auth

#if HAVE_LOGINUID
session         optional        pam_loginuid.so
#endif
#if HAVE_SELINUX
session		required	pam_selinux.so close
#endif
#if HAVE_ENV
session		required	pam_env.so envfile=/etc/profile.env DEBUG
#endif
#if HAVE_LASTLOG
session		optional	pam_lastlog.so silent DEBUG
#endif
session		include		system-auth
#if HAVE_CONSOLEKIT
session		optional	pam_ck_connector.so nox11
#endif
#if HAVE_SELINUX
 # Note: modules that run in the user's context must come after this line.
session		required	pam_selinux.so multiple open
#endif
#if HAVE_MOTD
session		optional	pam_motd.so motd=/etc/motd
#endif
#if HAVE_MAIL
session		optional	pam_mail.so
#endif
