import subprocess
import printipigeon as pp
from pathlib import Path
import random
from trim import trim_file, trim_and_name_file

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


legals = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"


def printHTML(contents, recipients, channel_name=None, verbose=True):
	legalid = "".join(random.choice(legals) for _ in range(64))
	filename = legalid + ".html"
	filepath = "/root/mail/" + filename
	with open(filepath, "w") as f:
		f.write(contents)
	printURL("http://localhost:1234/" + filename, recipients, channel_name, verbose)


def printURL(url, recipients, channel_name=None, verbose=True):
	def gobble(*a,**b):
		return

	p = print if verbose else gobble

	p("Sending " + url + " to: [" + ", ".join(recipients) + "]")
	legalid = "".join(random.choice(legals) for _ in range(64))
	path_prefix = "/root/mail/" + legalid

	if not recipients:
		p("ERROR: no printi recipients")
		return False

	width = lambda r: 576 if r == "printi" else 384

	for w in set(width(r) for r in recipients):
		filepath = path_prefix + str(w) + ".png"
		p(subprocess.check_output("firefox --screenshot \"" + filepath + "\" \"" + url + "\" --window-size=" + str(w), shell=True))
		trim_result = trim_and_name_file(filepath, channel_name, w) if channel_name else trim_file(filepath)
		if trim_result == "all white":
			print("a render turned out empty, aborting")
			return "all white"

	p("website rendered to png!")

	for i, recipient in enumerate(recipients):
		p("({} of {}) sending to printi.me/{}".format(i+1, len(recipients), recipient))

		pp.send_from_path(path_prefix + str(width(recipient)) + ".png", recipient)
		p(" ~~ !done! ~~ ")
	return "OK!"


def print_all_channels():
	creds = credentials.Certificate("/root/firebasekey.json")
	firebase_admin.initialize_app(creds)
	db = firestore.client()

	channels_collection = db.collection("channels")
	channels = channels_collection.list_documents()

	for c in channels:
		doc = c.get()
		doc_dict = doc.to_dict()

		channel_name = doc.id
		channel_script = doc_dict["script"]
		# We prepend an iframe that loads very slowly to allow the script to finish any long-lasting requests
		channel_script = "<iframe src=\"http://slowwly.robertomurray.co.uk/delay/10000/url/https://api.printi.me/\" width=0 height=0 style=\"display: none;\" ></iframe>\n" + channel_script

		# printURL("https://channels.printi.me/view?" + channel_name, doc_dict["subscribers"])
		printHTML(channel_script, doc_dict["subscribers"], channel_name)


if __name__ == "__main__":
	print_all_channels()
