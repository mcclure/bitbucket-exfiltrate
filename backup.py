from pybitbucket.auth import *
from pybitbucket.bitbucket import *
from pybitbucket.repository import *
import click
from getpass import getpass

@click.command(help="List or download all repos on a bitbucket account")
@click.option('--username', '-u', type=click.STRING, required=True, help="Username to log in with")
@click.option('--email', '-e', type=click.STRING, required=True, help="Email account associated with username to log in with")
@click.option('--info', '-v', count=True, help="Print info on each repo")
@click.option('--raw', '-vv', count=True, help="Print full data dump for every repo")
@click.option('--sort-access', count=True, help="Privates first")
@click.option('--outdir', default=None, type=click.Path(file_okay=False), help="Directory to backup into")
def backup(info, raw, outdir, username, email, sort_access):
	if not (info or raw or outdir):
		raise click.ClickException("Please pass at least one: --outdir, --info, --raw or --help")

	password = getpass()
	bitbucket = Client(
	    BasicAuthenticator(
    	    username,
        	password,
        	email))
	password = None

	repos = [x for x in Repository.find_repositories_by_owner_and_role(role="owner", client=bitbucket)]
	if sort_access:
		repos.sort(key=lambda x:x.data['is_private'])

	for repo in repos:
		if raw:
			print(repo.data)
		if info:
			print("name:[{}] {} {} {}{}{}{}\n".format(repo.data['name'], repo.data['scm'],
				"PRIVATE" if repo.data['is_private'] else "public",
				"\n[" if repo.data['description'] else "", repo.data['description'], "]" if repo.data['description'] else "",
				"\n(+ wiki)" if repo.data['has_wiki'] else ""))

backup()
