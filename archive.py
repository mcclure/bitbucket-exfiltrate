import os
import os.path
import click
import sys
import re

@click.command(help="Emit hg commands to archive a directory tree created by backup.py")
@click.argument('indir', type=click.STRING)
@click.argument('outdir', type=click.STRING)
@click.option('--only', type=click.STRING, help="enter 'public' or 'private'")
def archive(indir, outdir, only):
	for layer1 in os.listdir(indir): # Public, private
		if only and layer1 != only:
			continue
		inlayer1full = os.path.join(indir, layer1)
		outlayer1full = os.path.join(outdir, layer1)

		for layer2 in os.listdir(inlayer1full): # Repo names
			inlayer2full = os.path.join(inlayer1full, layer2)
			outlayer2full = os.path.join(outlayer1full, layer2)

			for layer3 in os.listdir(inlayer2full): # Repo artifacts (repo, wiki etc)
				inlayer3full = os.path.join(inlayer2full, layer3)
				outlayer3full = os.path.join(outlayer2full, "contents" if layer3=="hg" else layer3)

				os.makedirs(outlayer3full, exist_ok=True)

				if os.path.isfile(inlayer3full):
					os.makedirs(outlayer2full, exist_ok=True)
					print("cp \"{}\" \"{}\"".format(inlayer3full,outlayer3full))
				else: # Directory
					os.makedirs(outlayer3full, exist_ok=True)
					outlayer3full = os.path.abspath(outlayer3full)
					print("pushd \"{}\"".format(inlayer3full))
					print("hg archive \"{}/\"".format(outlayer3full))
					print("popd")

archive()