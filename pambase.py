#!/usr/bin/env python3

import argparse
from jinja2 import Template, Environment, FileSystemLoader

def main():
	parser = argparse.ArgumentParser(description='basic Gentoo PAM configuration files')
	# These are actual module options
	parser.add_argument('--libcap', help='enable pam_caps.so module')
	parser.add_argument('--passwdqc', help='enable pam_passwdqc.so module')
	parser.add_argument('--elogind', help='enable pam_elogind.so module')
	parser.add_argument('--systemd', help='enable pam_systemd.so module')
	parser.add_argument('--selinux', help='enable pam_selinux.so module')
	parser.add_argument('--nullok', help='enable nullok option for pam_unix.so module')
	parser.add_argument('--mktemp', help='enable pam_mktemp.so module')
	parser.add_argument('--pam-ssh', help='enable pam_ssh.so module')
	parser.add_argument('--securetty', help='enable pam_securetty.so module')
	parser.add_argument('--sha512', help='enable sha512 option for pam_unix.so module')
	parser.add_argument('--krb5', help='enable pam_krb5.so module')
	parser.add_argument('--minimal', help='install minimalistic PAM stack')

	# Settings which can change behaviour
	# TODO: Maybe use a different argument type here vs modules? e.g. --add-modules?
	parser.add_argument('--debug', help='add debug option to the stack')
	parser.add_argument('--unix-extended-encryption')
	parser.add_argument('--likeauth')

	load = FileSystemLoader('')
	env = Environment(loader=load)
	args = parser.parse_args()

	tmpl = env.get_template('templates/login.tpl')
	with open("stack/login", "w+") as output:
		render = tmpl.render(vars(args).items())
		if render:
			output.write(render)
			output.write("\r\n")

	tmpl = env.get_template('templates/system-auth.tpl')
	with open("stack/system-auth", "w+") as output:
		render = tmpl.render(vars(args).items())
		if render:
			output.write(render)
			output.write("\r\n")

if __name__ == "__main__":
	main()
