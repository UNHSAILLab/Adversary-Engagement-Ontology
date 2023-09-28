#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

all:

top_srcdir := ..

.PHONY: \
  check-master \
  check-attack \
  check-engagement \
  check-identity \
  check-objective \
  check-role \
  check-vocabulary \
  clean-master \
  clean-identity \
  clean-objective \
  clean-role \
  clean-time \
  clean-vocabulary

check: \
  check-master \
  check-engagement \
  check-identity \
  check-objective \
  check-role \
  check-vocabulary


check-master: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory master \
	  check
check-engagement: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory engagement \
	  check
check-identity: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory identity \
	  check
check-objective: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory objective \
	  check
check-role: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory role \
	  check
check-vocabulary: \
  $(top_srcdir)/.lib.done.log
	$(MAKE) \
	  --directory vocabulary \
	  check

clean: \
  clean-master \
  clean-engagement \
  clean-identity \
  clean-objective \
  clean-role \
  clean-vocabulary

clean-master:
	@$(MAKE) \
	  --directory master \
	  clean
clean-engagement:
	@$(MAKE) \
	  --directory engagement \
	  clean
clean-identity:
	@$(MAKE) \
	  --directory identity \
	  clean
clean-objective:
	@$(MAKE) \
	  --directory objective \
	  clean
clean-role:
	@$(MAKE) \
	  --directory role \
	  clean
clean-vocabulary:
	@$(MAKE) \
	  --directory vocabulary \
	  clean
