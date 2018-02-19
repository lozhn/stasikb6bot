install: pips spacy

pips:
	pip install -r libs.txt

spacy:
	python -m spacy download en

run:
	python run.py
