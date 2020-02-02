import os
import os.path
import click
import sys
import re

from getpass import getpass
from mercurial import ui,hg,commands
import mercurial

ops = ("list", "listfull", "collect", "delete")

def foundAny(target, fragments):
	for fragment in fragments:
		if fragment and target.find(fragment) >= 0:
			return True
	return False

@click.command(help="Operate on spam-infested wiki directories")
@click.argument('dir', type=click.STRING)
@click.argument('operation', type=click.STRING)
@click.option('--include', type=click.STRING, help="Comma separated require patterns")
@click.option('--exclude', type=click.STRING, help="Comma separated ban patterns")
@click.option('--dry-run', count=True, help="Don't do anything that touches disk")
@click.option('--username', '-u', type=click.STRING, help="Username to log in with (for delete)")
@click.option('--email', '-e', type=click.STRING, help="Email account associated with username to log in with (for delete)")
def tweak(operation, dir, include, exclude, dry_run, username, email):
	if not operation in ops:
		raise click.ClickException("Operation must be one of: {}".format( ", ".join(ops)))

	mercurial_ui = None
	if operation == "delete" and not dry_run:
		if not (username and email):
			raise click.ClickException("Operation delete requires --username and --email")

		mercurial_ui = ui.ui()

	seen = None

	if include:
		include = include.split(",")
	if exclude:
		exclude = exclude.split(",")

	for layer1 in os.listdir(dir): # Public, private
		layer1full = os.path.join(dir, layer1)
		for layer2 in os.listdir(layer1full): # Repo names
			layer2full = os.path.join(os.path.join(layer1full, layer2), "wiki")
			repo = None
			def repoOp(cmd, args, opts):
				nonlocal repo
				print("In [{}]\n{} execute:\nhg {} [{}] {{{}}}\n".format(layer2full, "pretend" if dry_run else "will", cmd, ",".join(args), opts))
				if not dry_run:
					if not repo:
						repo = hg.repository(mercurial_ui, layer2full.encode('utf-8'))
					getattr(commands, cmd)(mercurial_ui, repo, *[x.encode('utf-8') for x in args], **{k.encode('utf-8'):v.encode('utf-8') for (k,v) in opts.items()})
			try:
				for layer3 in os.listdir(layer2full): # Filenames in wiki dir
					if layer3 == ".hg":
						continue
					if include and not foundAny(layer3, include):
						continue
					if exclude and foundAny(layer3, exclude):
						continue

					layer3full = os.path.join(layer2full, layer3)

					if operation == "list":
						print(layer3)
					elif operation == "listfull":
						print(layer3full)
					elif operation == "collect":
						if not seen:
							seen = {}
						seen[layer3] = layer3full
					elif operation == "delete":
						if not include:
							raise click.ClickException("Delete operation must set --include, for annoying reasons")
						for i in include:
							if i and layer3.find(i) >= 0:
								repoOp("remove", ["*" + i + "*"], {})
			except FileNotFoundError:
				pass

			if repo:
				repoOp("commit", [], {'message':"Automated removal of Bitbucket spam"})
				repoOp("push", [], {})
				print("Stop now")
				sys.exit(0)

	if seen:
		for k in sorted(seen.keys()):
			print(k)

tweak()