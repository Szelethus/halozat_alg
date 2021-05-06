.PHONY: all
.PHONY: clean

PDFTEX=pdflatex -interaction=nonstopmode
NAME=control-dep
BIBNAME=references

all: ${NAME}.tex ${BIBNAME}.bib
	${PDFTEX}  ${NAME}.tex
	bibtex  ${NAME}.aux
	${PDFTEX} ${NAME}.tex
	${PDFTEX} ${NAME}.tex

show:
	evince ${NAME}.pdf > /dev/null 2>&1 &

abs: abstract.tex
	${PDFTEX} abstract.tex
	bibtex abstract.aux
	${PDFTEX} abstract.tex
	${PDFTEX} abstract.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.pdf *.toc *.fls *.fdb_latexmk *.out *.xdv
