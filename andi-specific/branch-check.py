import os
import os.path
import click
import sys
import re
from mercurial import ui,hg,commands
import mercurial

# When running this you'll want to somehow disable pagination.
# I could only figure out how to do this by actually editing the mercurial source

@click.command(help="Emit hg commands to archive a directory tree created by backup.py")
@click.argument('dir', type=click.STRING)
@click.option('--only', type=click.STRING, help="enter 'public' or 'private'")
def check(dir, only):
	mercurial_ui = ui.ui()

	for layer1 in os.listdir(dir): # Public, private
		if only and layer1 != only:
			continue
		inlayer1full = os.path.join(dir, layer1)

		for layer2 in os.listdir(inlayer1full): # Repo names
			inlayer2full = os.path.join(inlayer1full, layer2)

			for layer3 in os.listdir(inlayer2full): # Repo artifacts (repo, wiki etc)
				inlayer3full = os.path.join(inlayer2full, layer3)
				if layer3 != "hg" or os.path.isfile(inlayer3full):
					continue

				repo = hg.repository(mercurial_ui, inlayer3full.encode('utf-8'))
				print("-----------\nrepo " + layer2 + "\n")
				commands.summary(mercurial_ui, repo)
				commands.bookmark(mercurial_ui, repo)
				print("-- Heads --")
				commands.heads(mercurial_ui, repo)
				print("")

check()