#!/usr/bin/env python3

import argparse
from jinja2 import Template, Environment, FileSystemLoader

def main():
	parser = argparse.ArgumentParser(description='basic Gentoo PAM configuration files')
	# These are actual module options
	parser.add_argument('--libcap', action="store_true", help='enable pam_caps.so module')
	parser.add_argument('--passwdqc', action="store_true", help='enable pam_passwdqc.so module')
	parser.add_argument('--elogind', action="store_true", help='enable pam_elogind.so module')
	parser.add_argument('--systemd', action="store_true", help='enable pam_systemd.so module')
	parser.add_argument('--selinux', action="store_true", help='enable pam_selinux.so module')
	parser.add_argument('--nullok', action="store_true", help='enable nullok option for pam_unix.so module')
	parser.add_argument('--mktemp', action="store_true", help='enable pam_mktemp.so module')
	parser.add_argument('--pam-ssh', action="store_true", help='enable pam_ssh.so module')
	parser.add_argument('--securetty', action="store_true", help='enable pam_securetty.so module')
	parser.add_argument('--sha512', action="store_true", help='enable sha512 option for pam_unix.so module')
	parser.add_argument('--krb5', action="store_true", help='enable pam_krb5.so module')
	parser.add_argument('--minimal', action="store_true", help='install minimalistic PAM stack')

	# Settings which can change behaviour
	# TODO: Maybe use a different argument type here vs modules? e.g. --add-modules?
	parser.add_argument('--debug', action="store_true", help='add debug option to the stack')
	parser.add_argument('--unix-extended-encryption', action="store_true")
	parser.add_argument('--likeauth', action="store_true")

	parsed_args = parser.parse_args()
	processed = process_args(parsed_args)

	parse_templates(processed)

def process_args(args):
	blank_variables = ["krb5_authtok", "unix_authtok", "unix_extended_encryption",
					   "likeauth", "nullok"]

	# Create a blank dictionary
	# Then add in our parsed args
	output = dict.fromkeys(blank_variables, "")
	output.update(vars(args))

	# basic-conf logic
	if args.krb5 and args.passwdqc:
		output["krb5_authtok"] = "use_authtok"

	if args.krb5 or args.passwdqc:
		output["unix_authtok"] = "use_authtok"

	if args.debug:
		output["debug"] = "debug"

	# TODO: noop (it's a noop in pambase too)
	if args.unix_extended_encryption:
		pass

	if args.nullok:
		output["nullok"] = "nullok"

	if args.krb5:
		output["krb5_params"] = "{0} ignore_root try_first_pass".format("debug" if args.debug else "").strip()

	return output


def parse_templates(processed_args):
	load = FileSystemLoader('')
	env = Environment(loader=load)

	templates = ["login", "system-auth"]

	for template_name in templates:
		template = env.get_template('templates/{0}.tpl'.format(template_name))

		with open('stack/{0}'.format(template_name), "w+") as output:
			rendered_template = template.render(processed_args)

			if rendered_template:
				output.write(rendered_template + "\r\n")

if __name__ == "__main__":
	main()
