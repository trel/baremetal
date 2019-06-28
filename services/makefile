SCRIPT_DIR=./scripts
DHCP_TMPL_DIR=./dhcp/etc/dhcp/conf.d

%-builddir:
	mkdir -p ./build/$*

%-bind: %-builddir
	cp -r ./bind ./build/$*
	find ./build/$*/bind -type f -exec sed -i '' 's/SITE/$*/g' {} +

%-dhcpd: %-builddir
	cp -r ./dhcp ./build/$*
	LC_ALL=C find ./build/$*/dhcp -type f -exec sed -i '' 's/SITE/$*/g' {} +
	python $(SCRIPT_DIR)/merge.py -o ./build/$*/dhcp/etc/dhcp/conf.d $(DHCP_TMPL_DIR)/int.osn.conf $*
	python $(SCRIPT_DIR)/merge.py -o ./build/$*/dhcp/etc/dhcp/conf.d $(DHCP_TMPL_DIR)/mgt.osn.conf $*

build/%/macs.txt: %-builddir macs.yml
	python $(SCRIPT_DIR)/make_flat.py -o build/$* -s $* macs.yml

%-all: 
	$(MAKE) $*-dhcpd 
	$(MAKE) $*-bind
	$(MAKE) build/$*/macs.txt

all: mghp-all renc-all jhux-all sdsc-all ncsa-all

clean: 
	rm -rf ./build

