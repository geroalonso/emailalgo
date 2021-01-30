import bfs
import yelp

yelp.yelp()

c = 0
for i in conglomerado:
	pag = conglomerado[c]['website']
	bfs.crawling(pag)
	c += 1

