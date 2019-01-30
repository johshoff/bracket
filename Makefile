bracket.png: bracket.dot
	dot -Tpng -o bracket.png bracket.dot

bracket.dot: main.py
	./main.py > bracket.dot

show: bracket.png
	open bracket.png
