
# build reveal.js
python _python/build_patterns.py slides --reveal --target=slides/reveal.js/slides.html slides/src/

# build deckset
python _python/build_patterns.py slides --deckset --target=slides/slides.md slides/src/