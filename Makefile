.PHONY: test
test:
	py.test *.py

.PHONY: watch
watch:
	reflex -d none -g '*.py' -- py.test -x {}
