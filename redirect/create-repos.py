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

@click.command(help="Takes a list of newline-separated names, creates Bitbucket repo for each one with wiki but no issues or PRs")
@click.option('--username', '-u', type=click.STRING, required=True, help="Username to log in with")
@click.option('--email', '-e', type=click.STRING, required=True, help="Email account associated with username to log in with")
@click.option('--names', type=click.File('r'), required=True, help="Newline-separated list")
@click.option('--no-wiki', count=True, help="Don't create wiki")
def create(username, email, names, no_wiki):
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
		print("Creating: '%s'" % (name))
		payload = RepositoryPayload({'name': name, 'is_private':False, 'fork_policy': RepositoryForkPolicy.ALLOW_FORKS, 'description': "This repository has moved. See README for new link.", 'has_issues':False, 'has_wiki':not no_wiki})
		try:
			Repository.create(payload, name.lower(), None, bitbucket) # Returns repo but it isn't used. Notice lowercase "slug"
		except BadRequestError as e:
			errorHandled = False
			if e.type == "error" and hasattr(e, "error"):
				er = e.error
				if "message" in er:
					errorMessage = er["message"]
					print("Error creating repo %s: %s" % (name, errorMessage))
				if "fields" in er:
					fields = er["fields"]
					if "name" in fields:
						errorName = fields["name"][0]
						if errorName == "You already have a repository with this name.":
							print("Skipping %s" % (name))
							errorHandled = True
			if not errorHandled:
				raise e

		print()

create()
