import subprocess
import sys
import getpass
import re

# ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"
YELLOW = "\033[33m"

def print_banner():
    banner = f"""
{CYAN}{BOLD}========================================
AWS CLI Setup Script
========================================
This script will install and configure the AWS CLI on your Linux machine.
========================================{RESET}
"""
    print(banner)

def install_aws_cli():
    try:
        print(f"{YELLOW}Updating package list...{RESET}")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        print(f"{YELLOW}Installing AWS CLI...{RESET}")
        subprocess.run(["sudo", "apt-get", "install", "-y", "awscli"], check=True)
        
        print(f"{GREEN}AWS CLI installed successfully.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error during AWS CLI installation: {e}{RESET}")
        sys.exit(1)

def configure_aws_cli(aws_access_key, aws_secret_key, region):
    try:
        print(f"{YELLOW}Configuring AWS CLI...{RESET}")
        subprocess.run(["aws", "configure", "set", "aws_access_key_id", aws_access_key], check=True)
        subprocess.run(["aws", "configure", "set", "aws_secret_access_key", aws_secret_key], check=True)
        subprocess.run(["aws", "configure", "set", "region", region], check=True)
        
        print(f"{GREEN}AWS CLI configured successfully.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error during AWS CLI configuration: {e}{RESET}")
        sys.exit(1)

def is_valid_aws_access_key(key):
    return bool(re.match(r'AKIA[0-9A-Z]{16}', key))

def is_valid_aws_secret_key(key):
    return bool(re.match(r'[A-Za-z0-9/+=]{40}', key))

def is_valid_region(region):
    valid_regions = ['us-east-1', 'us-west-1', 'us-west-2', 'eu-west-1', 'eu-central-1', 'ap-southeast-1', 'ap-northeast-1']
    return region in valid_regions

def main():
    print_banner()

    aws_access_key = input(f"{CYAN}Enter your AWS Access Key ID: {RESET}").strip()
    if not is_valid_aws_access_key(aws_access_key):
        print(f"{RED}Invalid AWS Access Key ID format.{RESET}")
        sys.exit(1)

    aws_secret_key = getpass.getpass(f"{CYAN}Enter your AWS Secret Access Key: {RESET}").strip()
    if not is_valid_aws_secret_key(aws_secret_key):
        print(f"{RED}Invalid AWS Secret Access Key format.{RESET}")
        sys.exit(1)

    region = input(f"{CYAN}Enter your preferred AWS region (e.g., us-east-1): {RESET}").strip()
    if not is_valid_region(region):
        print(f"{RED}Invalid AWS region. Please enter a valid region.{RESET}")
        sys.exit(1)

    print(f"\n{MAGENTA}Starting setup...\n{RESET}")
    install_aws_cli()
    configure_aws_cli(aws_access_key, aws_secret_key, region)

    print(f"\n{GREEN}Setup complete. You can now use the AWS CLI with your configured credentials.{RESET}")

if __name__ == "__main__":
    main()
