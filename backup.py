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

@click.command(help="List or download all repos on a bitbucket account")
@click.option('--username', '-u', type=click.STRING, required=True, help="Username to log in with")
@click.option('--email', '-e', type=click.STRING, required=True, help="Email account associated with username to log in with")
@click.option('--info', '-v', count=True, help="Print info on each repo")
@click.option('--raw', '-vv', count=True, help="Print full data dump for every repo")
@click.option('--sort-access', count=True, help="Privates first")
@click.option('--sort-scm', count=True, help="Gits first")
@click.option('--outdir', default=None, type=click.Path(file_okay=False), help="Directory to backup into")
def backup(info, raw, outdir, username, email, sort_access, sort_scm):
	if not (info or raw or outdir):
		raise click.ClickException("Please pass at least one: --outdir, --info, --raw or --help")

	password = getpass()
	bitbucket = Client(
	    BasicAuthenticator(
    	    username,
        	password,
        	email))
	password = None

	mercurial_ui = None

	repos = [x for x in Repository.find_repositories_by_owner_and_role(role="owner", client=bitbucket)]
	if sort_access:
		repos.sort(key=lambda x:x.data['is_private'])
	if sort_scm:
		repos.sort(key=lambda x:x.data['scm'])
	
	for repo in repos:
		name = repo.data['name']
		scm = repo.data['scm']
		is_private = repo.data['is_private']
		description = repo.data['description']
		has_wiki = repo.data['has_wiki']

		def hgDownload(path, url):
			try:
				repo = hg.repository(mercurial_ui, path)
			except mercurial.error.RepoError:
				commands.clone(mercurial_ui, url, path)
				return True

			commands.pull(mercurial_ui, repo, url)
			return False

		if raw:
			print(repo.data)
		if info:
			print("name:[{}] {} {} {}{}{}{}\n".format(name, scm,
				"PRIVATE" if is_private else "public",
				"\n[" if description else "", description, "]" if description else "",
				"\n(+ wiki)" if has_wiki else ""))
		if outdir:
			if not mercurial_ui:
				mercurial_ui = ui.ui()
			basepath = os.path.join(os.path.join(outdir, "private" if is_private else "public"), name)
			descpath = os.path.join(basepath, "description.txt")
			repopath = os.path.join(basepath, scm)
			wikipath = os.path.join(basepath, "wiki")
			if scm == "hg":
				os.makedirs(basepath, exist_ok=True)

				# Write description to file (but only if the description has "changed")
				if description:
					already = False
					try:
						with open(descpath) as f:
							already = f.read() == description
					except FileNotFoundError:
						pass
					if not already:
						with open(descpath, "w") as f:
							f.write(description)

				# Load main repo
				cloned = False
				cloned = hgDownload(repopath.encode('utf-8'), "ssh://hg@bitbucket.org/{}/{}".format(username, name).encode('utf-8')) or cloned

				if has_wiki:
					cloned = hgDownload(wikipath.encode('utf-8'), bytes("ssh://hg@bitbucket.org/{}/{}/wiki".format(username, name).encode('utf-8'))) or cloned

				if cloned:
					print("DID A CLONE!")
					return
			else:
				print("Warning: Did nothing for git repo {}".format(name))

backup()
