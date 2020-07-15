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

	parse_templates(parser.parse_args())

def parse_templates(args):
	load = FileSystemLoader('')
	env = Environment(loader=load)

	templates = ["login", "system-auth"]

	for template_name in templates:
		template = env.get_template('templates/{0}.tpl'.format(template_name))

		with open('stack/{0}'.format(template_name), "w+") as output:
			rendered_template = template.render(vars(args).items())

			if rendered_template:
				output.write(rendered_template + "\r\n")

if __name__ == "__main__":
	main()
