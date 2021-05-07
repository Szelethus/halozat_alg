.PHONY: all
.PHONY: clean

PDFTEX=pdflatex -interaction=nonstopmode
NAME=halozat_alg_final_report
BIBNAME=references

all: ${NAME}.tex ${BIBNAME}.bib
	latexmk -xelatex ${NAME}

show:
	evince ${NAME}.pdf > /dev/null 2>&1 &


clean:
	rm -f *.aux *.bbl *.blg *.log *.pdf *.toc *.fls *.fdb_latexmk *.out *.xdv
