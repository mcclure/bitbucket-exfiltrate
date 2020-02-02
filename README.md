Script(s) to back up my BitBucket Mercurial repos

# Usage

## First run

I suggest using a virtualenv for this script. Before first running the script, run:

	python3 -m venv env
	source env/bin/activate
	pip3 install -r requirements.txt

## Running

I'm on a mac, so I had to run this first so I wouldn't have to keep entering my ssh password:

    ssh-add -K ~/.ssh/id_rsa

I ran this to get a sense of what it was I was gonna be backing up:

    python3 backup.py -u MYUSERNAME -e "MY@EMAIL.ADDRESS" --info --sort-access --sort-scm

I ran this to actually do the backup:

    python3 backup.py -u runhello -e "andi.m.mcclure@gmail.com" --info --outdir /Volumes/PATH/TO/BACKUPDIR
