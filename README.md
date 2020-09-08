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

### Debugging

For a couple repos with git subrepos, I had to edit an hg/.hg/hgrc file and add this at the end:

    [subrepos]
    git:allowed = true

## Forwarding

After Bitbucket deleted the repos, I needed to create placeholders at the old BitBucket URLs so links I'd previously distributed wouldn't just be dead. Here's how I created my forwarding URLs.

First off I needed to create dummy repos. There's a create-repos script that takes the names of the repos and creates them on the Bitbucket side; I sourced these from the bitbucket backup directory I made:

    ls /Volumes/PATH/TO/BACKUPDIR/public > reponames.txt
    python3 redirect/create-repos.py -u runhello -e "andi.m.mcclure@gmail.com" --names reponames.txt

Then I needed to fill out the landing pages (the README.MDs) of those repos:

    python3 redirect/populate.py --prefix=https://github.com/mcclure/bitbucket-backup/tree/archive/repos --user=runhello /Volumes/PATH/TO/BACKUPDIR/public tmp > populatescript.bash
    bash -e populatescript.bash

This is a *little* more awkward then the other scripts, so notice these oddities:

* "create-repos" takes the repo names as a file containing names whereas "populate" takes a directory as argument and does ls itself
* With "populate" you should of course replace the "prefix" URL with whereever your new repos are; each repo name will be appended to the end of the URL
* If you add a "redirect.txt" to the backup directory, next to "contents", "wiki" and "description.txt", the contents of that text file will be used instead of prefix/repo.
* By default, populate.py and create-repos.py will create both a README.MD and a wiki (we could skip the README.MD but unfortunately BitBucket no longer lets wikis be landing pages). If you want to skip the wiki, pass `--nowiki`.

If you mess something up while running these scripts, you may find the included mass delete script useful:

    python3 redirect/delete-repos.py -u runhello -e "andi.m.mcclure@gmail.com" --names reponames.txt

Because this last script is dangerous, an `--i-know-what-this-does` argument is required.

## Andi-specific scripts

I had a problem with spammers putting stuff in my BitBucket wikis. For this reason there is a script named wiki-tweak in the "andi-specific" directory that lists the unique names of wiki pages and creates scripts for hg removing pages matching certain patterns.

There is also a script named branch-check that prints the current and alternate heads of every repo dir. Both of these tools work on the directory output by backup.py.

# License

The scripts in this directory are by Andi McClure and are available to you under [Creative Commons Zero](https://creativecommons.org/publicdomain/zero/1.0/legalcode), which is to say they are public domain.
