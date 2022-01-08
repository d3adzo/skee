import paramiko
import socket
import argparse
import getpass

# query ldap for any rit username's classes

def main():
    dns = socket.gethostbyname("banjo.rit.edu")
    print(f"\nconnecting to {dns} (banjo.rit.edu)")

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-u', '--username', action='store', help="your RIT id (abc1234) that you will use to log in", type=str, required=True)
    my_parser.add_argument('-t', '--target', action='store', help="target RIT id (abc1234) being searched", type=str, required=True)

    args = my_parser.parse_args()

    print("creating paramiko ssh client.")
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    try:
        print(f"attempting ssh connection to query {args.target}")
        ssh.connect(dns.strip(), username=args.username, password=getpass.getpass())
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"id {args.target}",  get_pty=True)
    except paramiko.SSHException as e:
        print(e)
        exit()

    section = str(ssh_stdout.read()).split(",")

    print("listing classes...\n")

    for p in section:
        if "rit-section-current" in p and "-s)" not in p:
            start = p.find("rit-section-current")
            end = p.find(")")
            print(f"  {p[start+20:end]}")

    print("head to https://schedulemaker.csh.rit.edu/generate ;)")

if __name__ == "__main__":
    main()