from pybitbucket.auth import *
from pybitbucket.bitbucket import *
from pybitbucket.repository import *
import click
from getpass import getpass
from mercurial import ui,hg,commands
import mercurial
import os
import os.path
import sys

@click.command(help="Takes a list of newline-separated names, DELETES Bitbucket repo for each one")
@click.option('--username', '-u', type=click.STRING, required=True, help="Username to log in with")
@click.option('--email', '-e', type=click.STRING, required=True, help="Email account associated with username to log in with")
@click.option('--names', type=click.File('r'), required=True, help="Newline-separated list")
@click.option('--i-know-what-this-does', count=True, required=True, help="Include this flag so I know this isn't an accident")
def delete(username, email, names, i_know_what_this_does):
	if not i_know_what_this_does:
		raise click.ClickException("Must include --i-know-what-this-does flag")
	password = getpass()
	bitbucket = Client(
	    BasicAuthenticator(
    	    username,
        	password,
        	email))
	password = None

	print("IN")
	for line in names:
		name = line.rstrip()
		print("Deleting: %s" % (name))
		try:
			repo = Repository.find_repository_by_name_and_owner(name, owner=username, client=bitbucket)
			repo.delete()
		except BadRequestError as e:
			errorHandled = False
			if e.type == "error" and hasattr(e, "error"):
				er = e.error
				if "message" in er:
					errorMessage = er["message"]
					print("Error deleting repo %s: %s" % (name, errorMessage))
			if not errorHandled:
				raise e
		except HTTPError as e:
			if str(e).startswith("404 Client"): # THANKS FOR PARSING THE ERROR, MYSTERY ERROR CLASS
				print("Error deleting repo %s: %s" % (name, e)) # THAT WAS SARCASM, BY THE WAY
			else:
				raise e

		print()

delete()
