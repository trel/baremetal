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
  * Build boot disk instructions:
    * cribbed from https://serverfault.com/questions/517908/how-to-create-a-custom-iso-image-in-centos
    * download centos 7 minimal iso file
    * Copy iso contents locally 
      * mkdir /tmp/bootiso
      * mount -o loop /path/to/the.iso /tmp/bootiso
      * mkdir /tmp/bootisoks
      * cp -r /tmp/bootiso/* /tmp/bootisoks/
      * umount /tmp/bootiso && rmdir /tmp/bootiso
      * chmod -R u+w /tmp/bootisoks
    * Modify image files
      * cp /path/to/someks.cfg /tmp/bootisoks/isolinux/ks.cfg
      * cp /path/to/isolinux.cfg /tmp/bootisoks/isolinux/isolinux.cfg
    * Build new iso
      * cd /tmp/bootisoks
      * mkisofs -o /tmp/boot.iso -b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -V "CentOS 7 x86_64" -R -J -v -T isolinux/. .
      * isohybrid /tmp/boot.iso
      * implantisomd5 /tmp/boot.iso
    * Copy to USB
      * locate the USB drive using lsblk - look for the device with the right size
      * unmount the sucker if mounted
      * sudo dd bs=4M if=path/to/input.iso of=/dev/sd<?> conv=fdatasync  status=progress
      * without blocksize, this will crawl...
    * NOTES
      * the mkisofs -V option adds the volume label to the image this is needed by the bootloader when locating the ks file (specified as ks=hd:LABEL=CentOS\x207\x20x86_64:/ks.cfg)