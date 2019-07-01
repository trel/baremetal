import yaml
import re
import argparse
from os.path import basename

# Locally administered default for 
# filling missing macs
DEFAULT_MAC = "fa:65:5f:71:a9:fd"

parser = argparse.ArgumentParser(description='Create site specific dhcp '
                                             'files from templates')

parser.add_argument('-p', '--prefix', default='',
                    help='prefix to append to output files')

parser.add_argument('-m', '--macfile', default='macs.yml',
                    help="yml file containing mac information")

parser.add_argument('-o', '--outdir',
                    default=".",
                    help='location to output processed files')

parser.add_argument("templates", nargs="+",
                    help="template files to process")

parser.add_argument("site",
                    help="site to generate dhcp information for")

parser.add_argument("-i", "--ignore",
                    action='store_true',
                    help="ignore missing macs and use dummy address")

args = parser.parse_args()

repl_match = re.compile("^\s*host SITE-(\w\w\w\d\d).*ethernet (\w*);.*")

# Load the mac information from the yml file
f = open(args.macfile, "r")
mac_dict = yaml.load(f)

# Doit...
for tmpl in args.templates:

    with open(tmpl, "r") as dhcp_tmpl:
        lines = dhcp_tmpl.readlines()

    prefix = args.prefix + "." if len(args.prefix) > 0 else ''
    outfile = args.outdir + "/" + prefix + basename(tmpl)
    print("Creating file: %s with template %s and macfile %s" %
          (outfile, tmpl, args.macfile))

    with open(outfile, "w") as conf_file:
        for l in lines:
            m = re.match(repl_match, l)
            if m:
                node = m.group(1)
                interface = m.group(2)
                try:
                    mac = mac_dict[args.site][node][interface]
                except KeyError as e:
                    if args.ignore:
                        mac = DEFAULT_MAC
                    else:
                        raise e
                l = re.sub(interface, mac, l)
                l = re.sub(r'SITE', args.site, l)
            conf_file.write(l)
