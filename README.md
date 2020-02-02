BitBucket announced they were deleting their Mercurial repos. I had a bunch. I wrote these scripts to help me mass-export all my Mercurial repos off Bitbucket and back them up to my hard drive.

# Usage

## First run

I suggest using a virtualenv for this script. Before first running the script, run:

	python3 -m venv env
	source env/bin/activate
	pip3 install -r requirements.txt

## Running

I'm on a mac, so I had to run this first so I wouldn't have to keep entering my ssh password:

    ssh-add -K ~/.ssh/id_rsa

I ran this (it asks for my Bitbucket password) to get a sense of what it was I was gonna be backing up:

    python3 backup.py -u MYUSERNAME -e "MY@EMAIL.ADDRESS" --info --sort-access --sort-scm

I ran this (it also asks for my Bitbucket password) to actually do the backup:

    python3 backup.py -u runhello -e "andi.m.mcclure@gmail.com" --info --outdir /Volumes/PATH/TO/BACKUPDIR

I wanted to have a "flat" version of the backup with no mercurial, only the files, so then I ran this:

	python3 archive.py --only public /Volumes/PATH/TO/BACKUPDIR /Volumes/PATH/TO/BACKUPDIR-FLAT > archivescript.bash
	bash -e archivescript.bash

## Debugging

For a couple repos with git subrepos, I had to edit an hg/.hg/hgrc file and add this at the end:

    [subrepos]
    git:allowed = true

## Andi-specific scripts

I had a problem with spammers putting stuff in my BitBucket wikis. For this reason there is a script named wiki-tweak in the "andi-specific directory" that lists the unique names of wiki pages and creates scripts for hg removing pages matching certain patterns. There is also a directory named branch-check that prints the current and alternate heads of every repo dir. Both of these tools work on the directory output by backup.py.

# License

The scripts in this directory are by Andi McClure and are available to you under [Creative Commons Zero](https://creativecommons.org/publicdomain/zero/1.0/legalcode), which is to say they are public domain.