work environment:

	- ✓ use i3
		- learn to use it properly
		- ** disable gdm
		- startup setup?

	- need a better command line search tool
		- for my use
		- for my chat to use

	- text files:
		- write in markdown by default not text!
		- vim warn if open a .txt file in my working dirs
		- need to enumerate my working dirs, maybe use high-level folder/s for that (code? ai?)
		- markdown validator, or rely on syntax highlighting
		- make Cz similar

	- vim:
		- make flashcards from the manual!!
		- shortcut to open ideas / scratch / snip file
		- shortcut to cut and append selected to that file

	- sort out my old code
		- separate good from unknown from junk
		- hide the junk somewhere I won't see it
		- analyse and document everything using GPT
			- do a title and detailed summary and inline comments all in one request to save tokens?
		- can it automatically add nice things like help text?

	- I need a pomodoro thing for my new environment
		- a simple script that sleeps for 55 minutes, then starts gently flashing the screen

shell scripting:

	- opts script
		- ask GPT to help me improve it
		- auto help
		- short option support with long var-names used?
		- or just add adequate shell functionality to python with concise syntax

	- see blog ideas below

	- Can I use the same code for shell scripts as sourceable shell libraries?
		# move functions to separate scripts
		# Need to detect if sourced or executed, and if executed, run main().

		# check if sourced

		if [ -n "$BASH_SOURCE" ]; then
			# sourced
			# TODO
			:
		else
			# executed
			main "$@"
		fi

	- ideally perhaps, the script would use functions from separate libs if they are available,
		- and also update them in the script itself for a stand-alone publishable version
		- That would be good for very small scripts like one-liners
		- or have a separate dev script vs stand alone script
		- good for things like v q and such

	- how to check if not running in bash or a highly compatible shell
		# q. what other shells are compatible with bash?
		# a. zsh, dash, ksh, mksh, pdksh, posh, yash, ash, busybox ash, busybox sh, busybox sh, busybox a
		# q. what's the fastest and lightest bash-like or bourne shell?
		# a. das

		if [ -z "$BASH_VERSION" ]; then
			# not running in bash
			# TODO
			:
		fi

	- visual shell / make / multi-mode / net2sh thing
		- great if it was shell compatible, i.e. translates to regular shell script like net2sh does
		- don't use pipes and parallelism by default, use files like make; pipes are optional
		- could render to makefiles instead?
		- tsort


python scripting:

	- see blog ideas below


chatgpt script:

	- just call it chat or maybe cha as chat is in use
		- about renaming scripts, don't include the script name in the header comment?
		- or maybe it's good to identify the usual name

	- use an env format config file for e.g. preferred default LLM engine

	- safety: don't lose the user's input
	- run arcs for safety
	- check that I'm not clobbering the input file

	- fill ...?!

	- optionally pass input and output through a filter, a single wrapper program with options:
		- input:
			- fix up the layout (done?)
			- fix up the role names
			- allow blank role for the user, i.e. start with : or unindented final line (bot replies are always indented)
			- don't send commented sections in the input to GPT, what sort of comment style to use though, # in the first column I guess
			- add colons on end of lines before indented sections, like in Python
			- options to remove blank lines, repeated spaces
		- output:
			- don't indent blank lines, so I can navigate with { and } in vim
			- option to echo the original input (when running a script from vim):
				- option to run through uniqo to dedup input and output
			- option to clean up the original input file
			- fix up the role names, using user's preferred names from the input
				- i.e. Sam: and bot:  or  I: and you: 
				- bot names could be Elion, Fenyman
			- options I'm not sure about:
				- change the layout
				- remove the role names, colons and indents
			- convert code, spaces to tabs, or generally user's preferred code style
			- detect actual type of code, for correct display / syntax highlighting in markdown

	- use as a library in my chat app

	- cache responses?  or something like that

	- translate the shell scripts to Python so I can use them in a library or notebook?

chatgpt_loop script:

	- ideally would handle files changed even while it's waiting
	- does it need to wait or just fire jobs and trust them?

	- find all newly changed files,
		- process .chat files
		- process files having some marker such as, CHAT?  like ok google for text files!
		- in future use inotify or whatever
		- .chat is a pretty rare extension, on my PC `locate .chat | grep '\.chat$' | grep -v '/\.'` gives only my chat files
		- also no .cha files; look it up though

sundry GPT / AI scripts:

- search.py
	- finish it and use it!

- notebooks / nbdev
	- automatically convert shell scripts and Python scripts to notebooks
	- blog notebook vs organized library
		- just have a post for each library, and update them
		- I could even re-publish them, i.e. change the date
		- I could use some diff process to make a blog post with only the new stuff, i.e. part 2 of a series
			- basically this means the new notebook would append to the same library
			- to edit a function
				- if a bug, just fix it in the original post and comment on it; and re-release the lib
				- if a major change, make a new post and use a special directive to replace the function?
					- or it could do that automatically if they have the same name
					- the directive could list previous names, if renaming a function / symbol
				- if rebuilding the library from scratch
					- need to read all relevant blog posts, need an index
					- need to apply them in order, by date I guess
				- build doc notebooks from the libs?  can just append all the relevant blog posts together I guess?
					- ideal doc might be better organized, but if I consider the blog to be a living document, I can edit it to make it better, including structural changes.  Revisionism!!


		- or just have a single notebook with a table of contents (copilot suggestion?)


- blogging

- script to remind me what I've been doing today
	- just find files changed lately, or dirs having such
- call it a dlog or devlog?


Copilot in nvim:

	- * shortcut key to turn on or off (:Copilot disable, :Copilot enable)
	- change the colour of suggestions to be less distracting (shortcut option perhaps)
	- can I collect suggestions without showing them inline?
	- avoid duplicate suggestions?
	- https://stackoverflow.com/questions/71224911/can-github-copilot-stop-auto-suggesting-instead-be-triggered-by-a-keystroke


Not important right now:

try using sam or acme editors?  or emacs again?



- shell template files


random:
	- Copilot prefers tabs!  or not, seems to depend, it's not a consistent persona, probably for the best!
	- use home directory for current work, then file it away later
		- move all
		- move needed back
		- could change home
		- could use multiple user accounts for different projects
			- good to test deps / requirements
			- docker good to test deps too
