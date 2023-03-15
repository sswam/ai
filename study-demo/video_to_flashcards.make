#!/usr/bin/make -sf

img_rate=1

# threads=$(shell nproc)

default: goal

post.txt: topic.txt summary.txt flashcards.txt
	catpg $^ > $@

flashcards.txt: audio.txt
	< $< chatgpt_flashcards > $@

topic.txt: audio.txt
	< $< chatgpt_topic > $@

summary.txt: audio.txt
	< $< chatgpt_summary > $@

audio.txt: audio.webm
	whisper $<

audio.webm: video.webm
	ffmpeg -i $< -vn -c copy -threads $(threads) $@

# get images from the video, one every $img_rate seconds
images: video.webm
	mkdir -p images
	ffmpeg -i $< -vf fps=1/$(imgrate) -qscale:v 2 images/%06d.jpeg

video.webm: url.txt
	yt-dlp -f bestvideo+bestaudio -o $@ $(shell cat $<)
	touch $@

url.txt:
	read -p "Enter URL: " url; echo $$url >$@

goal: post.txt images

.PRECIOUS:
