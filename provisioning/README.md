This directory contains scripts to bootstrap a pod with a minimal config the main files are:

* **ks.cfg** - this minimal kickstart boots the node and detects and configures the mgt interface (eno1) via a table of macs. It also enables the OOB interface on mon02.

* **bootstrap.yml**: an ansible script to install the ansible user/key add her to wheel and config wheel for sudo. It also configures ssh:
  * disable root access
  * disallow password login

* **network.yml** - sets up networking and routing:
  * default networking on the mgt interface proxies through mon02
  * default routing table for dmz interface setup to support proper outbuond routing on traffic received on the dmz.

* **hosts.yml** - basic ansible host config to support network.yml playbook.

* **Notes**:
  * There is a temporary task in the networking playbook that cleans up /dev/sda. This is for initial ceph testing where we are just installing on one disk. Repeated installs require the disks be wiped.
  * The /etc/ansible dir for this was pulled from the the ceph-anisble-root repo