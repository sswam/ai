#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from duckduckgo_search import ddg_images
from fastai.vision.utils import download_images
import argparse
import re

def mkdirs(path):
	os.makedirs(path, exist_ok=True)

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def replace_bad_chars(s):
	""" replace spaces and other dubious characters with underscores """
	return re.sub(r'[^a-zA-Z0-9]+', '_', s)

def get_images(query, output_folder, n_images, license):
	""" Download images for a given query """
	search_results = ddg_images(query, max_results=n_images, license_image=license)
	urls = [r['image'] for r in search_results]
	eprint(f"Downloading {len(urls)} images for query '{query}' to folder '{output_folder}'")
	eprint(urls)
	download_images(dest=output_folder, urls=urls)

def get_topic_subtopic_images(topics, n_images_per_topic, license, topic=None):
	""" Download images for a list of topics and subtopics """
	for i, topic_line in enumerate(topics):
		# Parse main topic and subtopics
		main_topic, *subtopics = [s.strip() for s in re.split(r'[:;\t]+', topic_line)]

		eprint(main_topic, subtopics)

		# Create folder structure
		main_folder = Path(f"{i+1}_{replace_bad_chars(main_topic)}")

		for j, subtopic in enumerate(subtopics):
			sub_folder = main_folder / f"{j+1}_{replace_bad_chars(subtopic)}"
			mkdirs(sub_folder)

			# Form search query and send request
			query = f"{subtopic}, {main_topic}, {topic}"

			get_images(query, sub_folder, n_images_per_topic, license)

def main():
	""" Main function """

	# Parse command line arguments, and show defaults in help text
	parser = argparse.ArgumentParser(description='Download images for a list of topics and subtopics.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-o', '--output', type=str, default='.', help='Path to output folder.')
	parser.add_argument('-i', '--input', type=str, default='-', help='Path to file containing list of topics and subtopics.')
	parser.add_argument('-n', '--n_images_per_topic', type=int, default=10, help='Number of images to download per topic.')
	parser.add_argument('-l', '--license', type=str, default='any', help='License of images to download, see duckduckgo_search doc')
	parser.add_argument('-t', '--topic', type=str, default=None, help='Topic to download images for.')

	args = parser.parse_args()

	# Read list of topics from file
	infile = sys.stdin if args.input == '-' else open(args.input, 'r')
	with infile as f:
		topics = f.readlines()

	# Change working directory to output folder
	mkdirs(args.output)
	os.chdir(args.output)

	# Download images
	get_topic_subtopic_images(topics, args.n_images_per_topic, args.license, args.topic)

if __name__ == '__main__':
	main()
