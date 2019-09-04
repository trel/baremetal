**POD “Bootstrap” Proposal**

* *POD changes*
  * Make netgear switch "unmanaged" (i.e., leave it alone as it shipped)
  * Add 5 management interface (eno1) cables to dat01-dat05, connect to netgear
  * Change boot order
    * Disk
    * Usb (will need an inserted usb to have this available?)

* *Boot image*
  * Minimal centos USB with tiny kickstart. KS has:
    * root pwd
    * install disk target (/dev/disk/by-id is stable and the same for all pods)
      * /dev/disk/by-path/pci-0000:00:17.0-ata-1.0 == mon first HD 
      * /dev/disk/by-path/pci-0000:00:17.0-ata-3.0 == dat first HD
    * Configure mgmt IP on each node
      * Include table in the ks that has 25 MACS
        * 5 eno1 macs X 5 sites
      * use mac of eno1 to detect machine identity (mon01, mon02, etc.) and site (mghp, ncsa, etc.)
      * Use predefined mapping to assign eno1 interface (e.g. zzzz-mon01-mgt == 172.16.3.11, etc.)
      * Use mon02 as gw (see next section)
    * Configure OOB access - mon02 is oob gw w/NAT
      * use previous mac detection to ID the site
      * include map of 10 IPs in ks - (1 mon02 oob IP + 1 mon02 gw IP) x 5 sites
      * Use the site ID to assign oob addresses to eno2 interface
      * configure mon02 node as NAT
    * Provision ansible user
      * Create ansible user
      * Install temporary public key
      * Add ansible to sudoers
      * SSH
        * Disable root login
        * Disable password login
        * UseDNS = no

* *Install from stick*
  * doit

* *Initial config (after install)*
  * connect to newly built mon2 via oob interface and run "bootstrap" ansible scripts
    * Note that this assumes that you use mon02 as the bastion host and that you execute ansible scripts jumping through that host. If you're new to this, I found this article helpful for setup:
      * https://blog.scottlowe.org/2015/12/24/running-ansible-through-ssh-bastion-host/
  * bootstrap.yml - This playbook simply replaces the temporary ssh key with a permanent one (That you need to specify in the script)
  * networking.yml - runs as ansible user
    * configure networking on all the nodes
    * Configure BMC as well
    * yum update all machines from centos mirror
  * Mellanox.yml (TBD)
    * Configure mellanox pod-local networking
    * Uplink configuration will be manual and site specific
    * This step may be manual

* *Node now ready for:*
  * Ceph ansible (kevin)
  * General services ansible (gavin)
  * etc.
