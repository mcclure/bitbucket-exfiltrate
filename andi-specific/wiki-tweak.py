import os
import os.path
import click

ops = ("list", "listfull", "collect")

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
			try:
				for layer3 in os.listdir(layer2full): # Repo names
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
			except FileNotFoundError:
				pass

		if seen:
			for k in sorted(seen.keys()):
				print(k)

tweak()