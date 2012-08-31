
.PHONE: help clean

help:
	cat Makefile


clean:
	-rm -r _trial_temp
	-find . -name "*.pyc" -exec rm {} \;

