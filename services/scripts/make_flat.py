import yaml
import argparse

parser = argparse.ArgumentParser(description='Create flat dhcp file from yml')

parser.add_argument('-o', '--outdir',
                    default=".",
                    help='location to output processed files')

parser.add_argument('-s', '--site',
                    help='if specified, only generate for a single site')

parser.add_argument('macfile', default='macs.yml',
                    help="yml file containing mac information")

args = parser.parse_args()

# Load the mac information from the yml file
f = open(args.macfile, "r")
mac_dict = yaml.load(f)

f = open(args.outdir + "/macs.txt", "w")
for site, node_dict in mac_dict.items():
    if args.site and (site != args.site):
        continue
    f.write("# " + site + "\n")
    for node, interfaces in node_dict.items():
        for i, mac in interfaces.items():
            parts = ["POD", node, i, "HWADDR"]
            line = "_".join(parts) + "=" + mac + "\n"
            f.write(line.upper())