all: test run

test:
	@python fogcreek.py --verbose fogcreek.test > fogcreek.result
	@diff fogcreek.expected fogcreek.result

run:
	@python fogcreek.py fogcreek.secret

.PHONY: all test run
