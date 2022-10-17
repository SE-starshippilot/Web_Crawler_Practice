run: download
	python get_movies.py

download:
	pip install -r requirements.txt


clear:
	rm -rf ./images/*