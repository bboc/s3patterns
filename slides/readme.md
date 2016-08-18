# slides

This is a slide deck for teaching all patterns. The deck is built as a deckset version and as a reveal.js version.

Patterns are grouped in directories per patterns group and built using a buildscript. Input format is deckset, i.e. slide separators are "---".

The image folder is symlinked to all subfolders, so images can easily be added without relative paths.

[Reveal.js docs](https://github.com/hakimel/reveal.js/blob/master/README.md)

Build:

python build_patterns.py slides --reveal --target=../slides/reveal.js/slides.html ../slides/src/


## TODOs

TODO: create build script for deckset
TODO: compile content

