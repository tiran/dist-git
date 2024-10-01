.PHONY: clean
clean:
	find $(CURDIR) -name '*.rpm' -or -name '*.tar.gz' -delete
