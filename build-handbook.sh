# prepare handbook build
python _python/prepare_handbook.py

if [ "$?" != "0" ]; then
	echo "---error while preparing handbook! --" 1>&2
	exit 1
fi

cd handbook
# set filename and add current date to output-files
NAME=s3-patterns-handbook
# OUTPUT=../$NAME--$(date +%Y-%m-%d)


# render mmd file to latex trough master.md with metadata
multimarkdown --to=latex --output=$NAME.tex master.md
# make the pdf (pdflatex required to read image dimensions)
pdflatex -pdf -silent $NAME.tex
# copy pdf to output folder
mv $NAME.pdf ../$NAME.pdf

# clean up latex artefacts
latexmk -c $NAME.tex

# render markdown to HTML
multimarkdown --to=html --output=$NAME.html master-epub.md
# use pandoc to create epub file
pandoc --epub-stylesheet=buttondown.css --epub-metadata=epub-metadata.xml --epub-cover-image=img/s3-handbook-cover.png  -S -o ../$NAME.epub $NAME.html


# Old version
# # transclude all to one file 
# multimarkdown --to=mmd --output=handbook/handbook-compiled.md handbook/handbook--master.md
# multimarkdown --to=mmd --output=handbook/handbook-epub-compiled.md handbook/handbook-epub--master.md


# multimarkdown --to=latex --output=handbook/handbook-compiled.tex handbook/handbook-compiled.md
# cd handbook
# latexmk -pdf master.tex 
# mv master.pdf ../S3-patterns-handbook.pdf
# # clean up
# latexmk -C
# pandoc handbook-epub-compiled.md -f markdown -t epub3 -s -o ../S3-patterns-handbook.epub







