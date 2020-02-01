from pybitbucket.auth import *
from pybitbucket.bitbucket import *
from pybitbucket.repository import *
import click
from getpass import getpass

@click.command(help="List or download all repos on a bitbucket account")
@click.option('--username', '-u', type=click.STRING, required=True, help="Username to log in with")
@click.option('--email', '-e', type=click.STRING, required=True, help="Email account associated with username to log in with")
@click.option('--info', '-v', count=True, help="Print info on each repo")
@click.option('--outdir', default=None, type=click.Path(file_okay=False), help="Directory to backup into")
def backup(info, outdir, username, email):
	if not (info or outdir):
		raise click.ClickException("Please pass EITHER --info, --outdir or --help")

	password = getpass()
	bitbucket = Client(
	    BasicAuthenticator(
    	    username,
        	password,
        	email))
	password = None

	repos = Repository.find_repositories_by_owner_and_role(role="owner", client=bitbucket)
	for repo in repos:
		print(repo)

backup()
