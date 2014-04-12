RSYNC=rsync -zcav \
	--exclude=\*~ --exclude=.\* \
	--delete-excluded --delete-after \
	--no-owner --no-group \
	--progress --stats


doc: .sphinx-stamp

upload-doc:
	$(RSYNC) build/doc/ wrobell@maszyna.it-zone.org:~/public_html/geocoon

.sphinx-stamp:
	sphinx-build doc build/doc

