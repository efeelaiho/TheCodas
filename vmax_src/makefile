FILES :=                         	      \
	.travis.yml                  		  \
	apiary.apib							  \
	# netflix-tests/jw34846-RunNetflix.in   \
	# netflix-tests/jw34846-RunNetflix.out  \
	# netflix-tests/jw34846-TestNetflix.py  \
	# netflix-tests/jw34846-TestNetflix.out \
	models.html                  		  \
	IDB.log								  \
	models.py                         	  \
	#RunNetflix.py              		  \
	#RunNetflix.in         		          \
	#RunNetflix.out             		  \
	tests.py                 		  	  \
	tests.out

all:

check:
	@for i in $(FILES);                                         \
	do                                                          \
		[ -e $$i ] && echo "$$i found" || echo "$$i NOT FOUND"; \
	done

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  models.html
	rm -f  IDB.log
	rm -rf __pycache__

config:
	git config -l

#test: RunNetflix.out TestNetflix.out

# netflix-tests:
# 	git clone https://github.com/cs373-summer-2015/netflix-tests.git

models.html: models.py
	pydoc3 -w models

IDB.log:
	git log > IDB.log

# #RunNetflix.out: RunNetflix.py
# 	cat RunNetflix.in
# 	./RunNetflix.py < RunNetflix.in > RunNetflix.out
# 	cat RunNetflix.out

tests.out: tests.py
	coverage3 run    --branch tests.py >  tests.out 2>&1
	coverage3 report -m                      >> tests.out
	cat tests.out
