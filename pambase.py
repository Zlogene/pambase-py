#!/usr/bin/env python3

import argparse
from jinja2 import Template, Environment, FileSystemLoader
import pathlib


def main():
	parser = argparse.ArgumentParser(description='basic Gentoo PAM configuration files')
	parser.add_argument('--libcap', action="store_true", help='enable pam_caps.so module')
	parser.add_argument('--passwdqc', action="store_true", help='enable pam_passwdqc.so module')
	parser.add_argument('--elogind', action="store_true", help='enable pam_elogind.so module')
	parser.add_argument('--systemd', action="store_true", help='enable pam_systemd.so module')
	parser.add_argument('--selinux', action="store_true", help='enable pam_selinux.so module')
	parser.add_argument('--mktemp', action="store_true", help='enable pam_mktemp.so module')
	parser.add_argument('--pam-ssh', action="store_true", help='enable pam_ssh.so module')
	parser.add_argument('--securetty', action="store_true", help='enable pam_securetty.so module')
	parser.add_argument('--sha512', action="store_true", help='enable sha512 option for pam_unix.so module')
	parser.add_argument('--krb5', action="store_true", help='enable pam_krb5.so module')
	parser.add_argument('--minimal', action="store_true", help='install minimalistic PAM stack')
	parser.add_argument('--debug', action="store_true", help='enable debug for selected modules')
	parser.add_argument('--nullok', action="store_true", help='enable nullok option for pam_unix.so module')

	parsed_args = parser.parse_args()
	processed = process_args(parsed_args)

	parse_templates(processed)

def process_args(args):
	# make sure that output directory exists
	pathlib.Path("stack").mkdir(parents=True, exist_ok=True)

	blank_variables = ["krb5_authtok", "unix_authtok", "unix_extended_encryption", "likeauth", "nullok"]

	# create a blank dictionary
	# then add in our parsed args
	output = dict.fromkeys(blank_variables, "")
	output.update(vars(args))

	output["likeauth"] = "likeauth"
	output["unix_authok"] = "use_authok"

	if args.debug:
		output["debug"] = "debug"

	if args.nullok:
		output["nullok"] = "nullok"

	if args.krb5:
		output["krb5_params"] = "{0} ignore_root try_first_pass".format("debug").strip()

	if args.sha512:
		output["unix_extended_encryption"] = "sha512 shadow"
	else:
		output["unix_extended_encryption"] = "md5 shadow"

	return output


def parse_templates(processed_args):
	load = FileSystemLoader('')
	env = Environment(loader=load)

	templates = ["login", "other", "passwd", "system-local-login", "system-remote-login", "su", "system-auth", "system-service"]

	for template_name in templates:
		template = env.get_template('templates/{0}.tpl'.format(template_name))

		with open('stack/{0}'.format(template_name), "w+") as output:
			rendered_template = template.render(processed_args)

			if rendered_template:
				output.write(rendered_template + "\r\n")


if __name__ == "__main__":
	main()
