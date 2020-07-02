import os
import os.path
import click
import sys
import re

@click.command(help="Takes the backup/public directory created by backup.py and a place to store a temp directory, outputs the git commands to create wikis for each repo in the backup")
@click.argument('indir', type=click.Path(file_okay=False))
@click.argument('outdir', type=click.STRING)
@click.option('--user', type=click.STRING, required=True, help="Your bitbucket username")
@click.option('--prefix', type=click.STRING, required=True, help="URL prefix for new repos")

def populate(indir, outdir, prefix, user):
	if not prefix.endswith("/"):
		prefix += "/"

	for repo in os.listdir(indir): # Repo names
		outrepo = os.path.join(outdir, repo)
		os.makedirs(outrepo, mode=0o777, exist_ok=True)
		
		redirect = None
		description = None

		try:
			with open(os.path.join(indir, repo, 'redirect.txt')) as f:
			  redirect = f.read().rstrip()
		except FileNotFoundError:
			pass
		if not redirect:
			redirect = prefix + repo

		try:
			with open(os.path.join(indir, repo, 'description.txt')) as f:
			  description = f.read().rstrip()
		except FileNotFoundError:
			pass
		if description and not (description.endswith(".") or description.endswith("!") or description.endswith("?")):
			description += "."
		
		with open(os.path.join(outrepo, "Home.md"), "w") as f:
			f.write('# %s\n\n%s%s**This repository has [moved](%s).**\n' % (repo, description if description is not None else "", "\n\n" if description else "", redirect))

		fullpath = os.path.abspath(outrepo)
		print('pushd "%s"' % (fullpath))
		print('git init .')
		print('git add Home.md')
		print('git commit -m "Initial commit created by script"')
		print('git push -f git@bitbucket.org:%s/%s.git/wiki master' % (user, repo))
		print('popd')

populate()