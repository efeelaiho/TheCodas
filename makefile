FILES :=                         	      \
    .travis.yml                  		  \
    makefile							  \
    IDB.log  	                    	  \
    Netflix.py                         	  \
    tests.py  	            		      \
    apiary.apib         		          \
    models.html                  		  \
    models.py          		       		  \
    UML.pdf

all:

check:
	@for i in $(FILES);                                         \
    do                                                          \
        [ -e $$i ] && echo "$$i found" || echo "$$i NOT FOUND"; \
    done

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

Models.html: models.py
	pydoc3 -w models

IDB.log:
	git log > IDB.log
