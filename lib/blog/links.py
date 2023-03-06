#!/usr/bin/env python3

"""
This script creates numbered symlinks for blog posts.
"""

import os
from os.path import basename, islink
import re
from glob import glob
from pathlib import Path
import argparse
from os import environ as env

from lib import cd, show_locals, caller_locals, kv_dump, eprint, is_notebook
from blog import quarto_post_date

def update_links_in_cwd(digits=3, dry_run=False, verbose=False, debug=False):
	"""Update blog symlinks in the current working directory."""
	_params = caller_locals()

	# get list of blog symlinks
	blog_links = sorted(filter(islink, glob('*.ipynb')))

	# get list of blog posts under posts/foo/foo.ipynb
	posts = glob('posts/*/*.ipynb')

	# get link targets for each blog symlink
	link_targets = [os.readlink(link) for link in blog_links]

	# get list of posts which don't have symlinks yet
	new_posts = [post for post in posts if post not in link_targets]

	# sort posts by date
	new_posts_by_date = sorted(new_posts, key=quarto_post_date)

	# get the number of the last post
	n_posts = int(re.match(r'^\d+', basename(blog_links[-1])).group(0)) if blog_links else 0

	if not digits:
		digits = len(blog_links[0].split('_')[0])

	if debug:
		show_locals(exclude=_params)

	# create a numbered symlink for each post which doesn't have one yet
	for post in new_posts_by_date:
		n_posts += 1
		post_number = str(n_posts).zfill(digits)
		link_name = f'{post_number}_{os.path.basename(post)}'
		if not dry_run:
			os.symlink(post, link_name)
		if verbose:
			print(f'created symlink {link_name} -> {post}')

def update_links(blog_dir, *args, **kwargs):
	"""Update blog symlinks, wrapper to cd into blog_dir and show errors."""
	try:
		with cd(blog_dir):
			return update_links_in_cwd(*args, **kwargs)
	except Exception as e:
		if kwargs.get('debug'):
			raise
		else:
			eprint(f'error: {e}')

def main():
	"""Main function, handles command line arguments."""
	parser = argparse.ArgumentParser(description='Update blog symlinks') #, formatter_class=argparse.ArgumentDefaultsHelpFormatter, argument_default=argparse.SUPPRESS)
	default_blog_dir = env.get("BLOG_DIR", ".")
	parser.add_argument('--dir', type=str, help='blog directory', default=default_blog_dir, nargs='?')
	parser.add_argument('--digits', '-w', type=int, help='pad numbering to digits')
	parser.add_argument('--dry-run', '-n', action='store_true', help='dry run')
	parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
	parser.add_argument('--debug', '-d', action='store_true', help='debug')
	args = parser.parse_args()
	update_links(args.dir, digits=args.digits, dry_run=args.dry_run, verbose=args.verbose, debug=args.debug)

if __name__ == '__main__' and not is_notebook():
	main()
