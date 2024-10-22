import os
import sys
import argparse
from src.print import *
from src.process import *
from src.virustotal import *
from src.parse import *
from src.testsigs import *

def print_banner():
    banner = """
    __    ___  ____   ______  ___    ____  _____    __   ___  
   /  ]  /  _]|    \ |      ||   \  |    |/ ___/   /  ] /   \ 
  /  /  /  [_ |  D  )|      ||    \  |  |(   \_   /  / |     |
 /  /  |    _]|    / |_|  |_||  D  | |  | \__  | /  /  |  O  |
/   \_ |   [_ |    \   |  |  |     | |  | /  \ |/   \_ |     |
\     ||     ||  .  \  |  |  |     | |  | \    |\     ||     |
 \____||_____||__|\_|  |__|  |_____||____| \___| \____| \___/ 
                                                              
                 @ed
          Code Signing Certificate Discovery Tool
    """
    print(banner)

def main():
    print_banner()  # Print the banner at the start
    parser = argparse.ArgumentParser(description='Process and view certificates.')
    subparsers = parser.add_subparsers(dest='command')

    new_parser = subparsers.add_parser('import', help='Process new certificates')
    new_parser.add_argument('-i', '--input', required=True, help='Path to the directory containing .pfx files')

    view_parser = subparsers.add_parser('view', help='View stored certificates')
    view_parser.add_argument('-e', '--export', nargs='?', const='output.csv', help='Export certificates to a file')
    view_parser.add_argument('-s', '--silent', action='store_true', help='Silent mode (no output to console)')

    vt_parser = subparsers.add_parser('vt', help='Fetch files from VirusTotal')
    vt_parser.add_argument('--api', required=True, help='VirusTotal API key')
    vt_parser.add_argument('-q', '--quantity', type=int, default=100, help='Number of files to fetch')
    vt_parser.add_argument('-o', '--outputdir', required=True, help='Output directory for downloaded files')

    testsigs_parser = subparsers.add_parser('testsigs', help='Run limelighter with certificates')
    testsigs_parser.add_argument('-c', '--certlocation', required=True, help='Directory containing certificates')
    testsigs_parser.add_argument('-o', '--outputdir', required=True, help='Output directory for limelighter results')

    args = parser.parse_args()

    if args.command == 'import':
        if not os.path.isdir(args.input):
            print(f"Error: {args.input} is not a valid directory.")
            sys.exit(1)
        intake(args.input)
    elif args.command == 'view':
        if args.export:
            outputfile = args.export
            if not outputfile.endswith('.csv'):
                outputfile += '.csv'
            
            if not args.silent:
                print_certificate_database()
            export_certificate_database_to_csv(outputfile)
        else:
            print_certificate_database()
    elif args.command == 'vt':
        vt_download(args.api, args.quantity, args.outputdir)
    elif args.command == 'testsigs':
        testsigs(args.certlocation, args.outputdir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
