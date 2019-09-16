# Building a Pod

1) **Boot mon02 from usb:** Mon02 acts as a provisioning/gateway node for the rest of the pod. When building a new pod or starting from "scratch" download an create a bootable USB. The iso image is hosted on github as a release for the baremetal repo. To retrieve it, visit the repo (https://github.com/OpenStorageNetwork/baremetal) then select the releases section. There you will find up-to-date boot images for mon02. Once booted, mon02 will be listening on the IP address specfied for your site. There is a temporary ssh key in the repo (baremetal/provisioning/roles/common/files) that you will use to login to mon02 via ansible to run the provisioning playbooks.


2) **Bootstrap remaining node**: You can choose to build the pod manually or via PXE

    2a) **Boot nodes from usb** 
      * Using the same image/USB as was used to create mon02, boot the remaining servers.

    2b) **Boot nodes via PXE**
      * *Run the bootstrap.yml playbook*: This playbook bundles bootstrap_gw.yml and boostrap_common.yml you can run them separately (gateway must run first) if you want/need to.
```Note the bootstrap playbooks assume that you leave the USB stick in mon02```

        * *bootstrap_gw.yml*: This playbook does the following:
          * Downloads the iso from github
          * Copies the iso to the USB
          * Boots mon02 from the USB
          * Configures mon02 as PXE server using files unpacked from the USB
            * Applies the common and gateway roles to mon02

        * *bootstrap_common.yml*: This playbook does the following:
          * Sets all non-gateway nodes to PXE boot on next start
          * Restarts all non-gateway nodes.
          * Applies the common role to all non-gateway nodes


3) **Provision Nodes**: 
    * *Run site.yml playbook* This playbook applies the monitor and osd specific roles to the appropriate machines. For the most part, this consists of configuring networking (IPs and firewall)

## Configuration Variables

All configuration for the nodes is contained in the *defaults* directory of each role. The following are values that can/should be changed at each site.

1) **common**: 
    * ansible_user_key: This is the "secure" key that will be provisioned on all nodes replacing the temporary one ; this is a public key that you create.

2) **gateway**: The user modifiable variables here all pertain to which iso image is pulled from git to provision the gateway node. This is only needed for PXE setups. Manual installs do not need to worry about these variables.
   * release_tag: The release that you want to bring you cluster up to
   * iso_asset: The specifc name of the iso file (listed in the release notes at git)
    * checksum: The expected checksum of the downloaded iso (also listed in the release notes)

3) **monitor**: 
   * dmz_allowed_ip4_list: This is a list of IPs that are allowed to contact the monitor nodes. A site should configrure this as appropriate.

## Files to Modify

The following are the location of files that can/should be modified at each site.
1) **common**
   * ansible_user_key: place the actual public and private keys here


## Previous Notes

* *Ansible through a bastion host*
  * The pod will be configured using mon02 as a bastion host to provision the machines in the pod. To do this you need to:
    * Add settings to your ansible.cfg file. The relavant settings are:
    ```
    [ssh_connection]
    ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s
    control_path_dir = ~/.ansible/cp
    control_path = %(directory)s/%%h-%%r
    ```
    * Create a ~/.ssh/config file that implements the proxy e.g.:
    ```
    Host 172.16.3.*
      ProxyCommand ssh -W %h:%p mghpcc-osn-mon02
      IdentityFile ~/.ssh/osn_ansible_id_rsa

    Host mghpcc-osn-mon02
            HostName 192.69.102.29
            User ansible
            IdentityFile ~/.ssh/osn_ansible_id_rsa
            ControlMaster auto
            ControlPath ~/.ansible/cp/%%h-%%r
            ControlPersist 5m
    ```
    * Run the ssh agent and add the ansible key to it.
    ```
    # eval "$(ssh-agent -s)"
    # ssh-add ~/.ssh/mghpcc_osn_id_rsa
    ```
* There is a temporary task in the osd role that cleans up /dev/sda. This is for initial ceph testing where we are just installing on one disk. Repeated installs require the disks be wiped.

* Manual build boot disk instructions:
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
