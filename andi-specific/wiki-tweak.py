import os
import os.path
import click
import sys
import re

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
def tweak(operation, dir, include, exclude):
	if not operation in ops:
		raise click.ClickException("Operation must be one of: {}".format( ", ".join(ops)))

	seen = None

	if include:
		include = include.split(",")
	if exclude:
		exclude = exclude.split(",")

	for layer1 in os.listdir(dir): # Public, private
		layer1full = os.path.join(dir, layer1)
		for layer2 in os.listdir(layer1full): # Repo names
			layer2full = os.path.join(os.path.join(layer1full, layer2), "wiki")
			deleteFound = None
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
					elif operation == "delete": # The mercurial python interface doesn't work so well so just print out the hg commands to run
						if not include:
							raise click.ClickException("Delete operation must set --include")
						for i in include:
							if i and layer3.find(i) >= 0:
								if deleteFound is None:
									deleteFound = {}
									print("pushd " + layer2full)
								deleteFound[i] = True
								break
				if deleteFound is not None:
					for i in deleteFound.keys():
						print("hg remove " + "*" + i + "*")
			except FileNotFoundError:
				pass

			if deleteFound is not None:
				print('hg commit -m "Automated removal of Bitbucket spam"')
				print("hg push")
				print("popd")

	if seen:
		for k in sorted(seen.keys()):
			print(k)

tweak()