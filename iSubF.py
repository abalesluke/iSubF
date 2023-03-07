try:
    import os, sys
    import requests
    import threading
    from shutil import copyfile as cpf
    from platform import system as my_system
    from socket import gethostbyname as get_dom_ip
except ImportError or ModuleNotFoundError as mod_err:
    mod_name = str(mod_err).replace('No module named ','')
    print("Error! Please Install Required Modules!\nRequired Module: {}".format(mod_name.replace("'",'')))
    exit()


def clear():
    # This windows feature is coming soon! 
    # But if you wish to contribute to this part
    # feel free to do so.!
    if(my_system == "Windows"):
        print("Sorry this script only runs in linux systems!")
        os._exit(0)
    else:
        os.system("clear")

def default_wlist(args):
    wlist_name = args.get('-w')
    if(os.path.exists(wlist_name)):
        return wlist_name

    wlist_name = './Subdomain.txt'
    if(not os.path.exists(wlist_name)):
        wlist_url = 'https://raw.githubusercontent.com'
        wlist_url+= '/danTaler/WordLists/master'
        wlist_url+= '/Subdomain.txt'
        open('Subdomain.txt','wb').write(requests.get(wlist_url).content)
    return wlist_name

def banner():
    clear()
    banner = "================================"
    banner+= "HackTheBox SubBrute"
    banner+= "By: Anikin Luke"
    banner+= "================================"
    print(banner)

def help(err_msg=''):
    banner()
    print(f"""
Required Arguments:
________________________________
    -d       |     : Domain Name
    -w       |     : Wordlist Path

Usage: python3 {os.path.basename(__file__)} -d <self> -w <target>
Example: python3 {os.path.basename(__file__)} -d example.com -w /usr/share/wordlists/Subdomain.txt
\n{err_msg}""")

class FoxParse:
    def __init__(self):
        self.args = {}
        self.new_args = {}

    def __parser(self, num, arg):
        try:
            self.args[arg] = sys.argv[(num+1)]
        except IndexError:
            self.args[arg] = True

    def parse_args(self):
        num = 0
        for arg in sys.argv[1:]:
            num+=1
            if((num % 2) == 1):
                if(not arg.startswith('-')):
                    continue
                self.__parser(num, arg)

    def set_args(self, arg):
        arg_val = self.args.get(arg)
        if(arg_val != None):
            self.new_args[arg] = arg_val
    
    def get_args(self)->exec:return (self.new_args if(bool(self.new_args)) else 0) # 0 means dictionary is empty


class Finder:
    def __init__(self,target, wpath):
        self.target = target
        self.wlist = wpath
        self.hostpath = '/etc/hosts'
        self.hostbak = self.hostpath+'.iSubF.bak'
        self.main = len(requests.get(f'http://{target}').content)

    def __backup(self, status):
        # 0 = backup the current hosts file
        # 1 = restore backup.
        hosts_b = self.hostbak
        hosts_p = self.hostpath
        pathExist = os.path.exists(hosts_b)
        if(status == 0):
            if(pathExist == False):
                cpf(hosts_p, hosts_b)
        elif(status == 1):
            if(pathExist):
                os.remove(hosts_p)
                os.rename(hosts_b, hosts_p)

    def __modify_hosts(self):
        self.__backup(0)
        subdomains = open(self.wlist)
        subdomains = subdomains.read()
        subdomains = subdomains.splitlines()
        domain_ip = get_dom_ip(self.target)
        host_file = open("/etc/hosts",'a')
        host_file.write("\n#iSubF modifications\n")
        for subdomain in subdomains:
            host = f"{domain_ip}\t"
            host+= f"{subdomain}."
            host+= f"{self.target}\n"
            host_file.write(host)

        host_file.close()

    def __brute(self,main_page, domain, target):
        try:
            r = requests.get(f"http://{domain}.{target}")
            if(len(r.content) != main_page):
                print(f"[Live]: {domain}.{target}")
        except KeyboardInterrupt:
            self.__backup(1)
            os._exit(0)
        except:
            pass

    def find(self):
        threads = []
        self.__modify_hosts()
        target = self.target
        main_page = self.main
        print("Adding threads.")
        for domain in open(self.wlist).read().splitlines():
            new_thread = threading.Thread(target=self.__brute, args=[main_page, domain, target])
            new_thread.daemon = True
            threads.append(new_thread)
        print("Finding..\n"+"="*20)
        for thread in threads:
            thread.start()

        self.__backup(1)
    

if(__name__=="__main__"):
    clear()
    parser = FoxParse()
    parser.parse_args()
    parser.set_args('-t')
    parser.set_args('-d')
    parser.set_args('-w')
    args = parser.get_args()
    if(args == 0):
        help()
        exit(0)
    elif((args.get('-d') == True) or (args.get('-d') == None)):
        help("[ERROR]: '-d' argument is required, please specify your target domain!")
        exit(0)
        
    wordlist_path = default_wlist(args)

    if(os.getuid() != 0):
        print("Please this script as root!")
        os._exit(0)
    subFinder = Finder(args.get('-d'), wordlist_path)
    subFinder.find()
