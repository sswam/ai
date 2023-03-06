#!/usr/bin/env python3

"""
This script creates a new blank blog post from a template.
"""

import os
from os.path import basename, islink
import re
from glob import glob
from pathlib import Path
import argparse
from os import environ as env
import json
import datetime
import uuid

from lib import cd, show_locals, caller_locals, kv_dump, eprint, map_, is_notebook
from blog.links import update_links

python_kernelspec = {
	"display_name": "python3",
	"language": "python",
	"name": "python3"
}

bash_kernelspec = {
	"display_name": "bash",
	"language": "bash",
	"name": "bash"
}

def new_post_in_cwd(lang, name, title, dry_run=False, verbose=False, debug=False, template_file="template.ipynb"):
	"""Create a new blog post."""

	with open(template_file) as f:
		post = json.loads(f.read())

	if lang == "python":
		post["metadata"]["kernelspec"] = python_kernelspec
	elif lang == "bash":
		post["metadata"]["kernelspec"] = bash_kernelspec

	cell0 = post["cells"][0]

	date = datetime.date.today().isoformat()

	v = locals().copy()

	def replace_vars(line):
		return re.sub(r'\$(\w+)', lambda m: v.get(m.group(1)), line)

	map_(cell0["source"], replace_vars)

	for cell in post["cells"]:
		cell["id"] = str(uuid.uuid4())

	post_dir = Path("posts")/name
	post_dir.mkdir(parents=True)
	post_file = post_dir/f"{name}.ipynb"

	with open(post_file, "w") as f:
		print(json.dumps(post, indent=1), file=f)
	if verbose:
		eprint(f"Created blog file {post_file}")

def new_post(blog_dir, *args, **kwargs):
	"""Create a new blog post, wrapper to cd into blog_dir and show errors."""
	try:
		with cd(blog_dir):
			return new_post_in_cwd(*args, **kwargs)
	except Exception as e:
		if kwargs.get('debug'):
			raise
		else:
			eprint(f'error: {e}')

def main():
	"""Main function, handles command line arguments."""
	parser = argparse.ArgumentParser(description='Update blog symlinks') # , formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	default_blog_dir = env.get("BLOG_DIR", ".")
	parser.add_argument('name', help='filename of the post')
	parser.add_argument('title', help='title of the post')
	parser.add_argument('--lang', '-l', help='notebook language', default="python")
	parser.add_argument('--dir', type=str, help='blog directory', default=default_blog_dir, nargs='?')
	parser.add_argument('--dry-run', '-n', action='store_true', help='dry run')
	parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
	parser.add_argument('--debug', '-d', action='store_true', help='debug')

	args = parser.parse_args()
	new_post(args.dir, args.lang, args.name, args.title, dry_run=args.dry_run, verbose=args.verbose, debug=args.debug)
	update_links(args.dir, dry_run=args.dry_run, verbose=args.verbose, debug=args.debug)

if __name__ == '__main__' and not is_notebook():
	main()

