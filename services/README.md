**NOTES ON SERVICES DIR**

This directory contains the /etc layout for bind and dhcpd for the OSN pod. There are template files in the 
respective trees that are used to create site-specific files.

Site specific mac information is contained in a single yml file named macs.yml. To create the site-specific files, 
there is a simple makefile that, when run, will create a tree with one directory per site. The directory has the following
contents:
```
- site/
  - macs.txt
  - bind/
    - etc/
      - named.conf
      - named.rfc1912.zones
      - named/
        - zones/
          - db.ext.osn
          - db.mgt.osn
          - db.172.16.2.reverse
          - db.172.16.4.reverse
- dhcp/
  - etc/
    - dhcp/
      - dhcp.conf
      - conf.d/
        - ext.osn.conf
        - mgt.osn.conf
```

Note that the macs.txt file is a convenience file that lists all the macs for a given site in a flat-file format.

The relavant files that are used to create the tree are:

* macs.yml - this is a yml file that contains mac entries for each site
* scripts/merge.py - this is a python script that takes a macs yml file and dhcp templates and generates
dhcp config files
  * Note that this script requires the pyyaml module that can be installed wit `pip install pyyaml`
* scripts/make_flat.py - this script takes the yml file and outputs a flattened version. This script
also requires pyyaml.
* makefile - there is a simple makefile that is run to create the configs for all the sites. The "all" target will
make the configs for all sites

