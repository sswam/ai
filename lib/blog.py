import jq
import re

def quarto_post_date(post_file):
	"""Get the date of a quarto post."""
	with open(post_file) as f:
		text = f.read()
	metadata = jq.compile('.cells[] | select(.cell_type == "raw") | .source | join("")').input(text=text).first()
	match = re.search(r'^date: "(.*?)"$', metadata, re.MULTILINE)
	if not match:
		raise Exception('no date found in post metadata for ' + post_file)
	date = match.group(1)
	return date
