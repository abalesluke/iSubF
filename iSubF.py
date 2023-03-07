try:
    import os, sys
    import requests
    import platform
    import threading
    from shutil import copyfile as cpf
    from socket import gethostbyname as get_dom_ip
except ImportError or ModuleNotFoundError as mod_err:
    mod_name = str(mod_err).replace('No module named ','')
    print("Error! Please Install Required Modules!\nRequired Module: {}".format(mod_name.replace("'",'')))
    exit()


def clear():
    if(platform.system() == "Windows"):
        print("Sorry this script only runs in linux systems!")
        os._exit(0)
        # This feature is coming soon! But if you wish to contribute to this part, feel free to do so.!
    else:
        os.system("clear")

def default_wlist(args):
    wlist_name = args.get('-w')
    # if((wlist_name != True) or (wlist_name != None)):
    if(os.path.exists(wlist_name)):
        return wlist_name

    wlist_name = './Subdomain.txt'
    if(not os.path.exists(wlist_name)):
        wlist_url = 'https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt'
        open('Subdomain.txt','wb').write(requests.get(wlist_url).content)
    return wlist_name

def run(call):
    banner()
    threading.Thread(target=call).start()

def banner():
    clear()
    print("""
================================
 HackTheBox SubBrute
 By: Anikin Luke
================================
""")

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

    def __backup(self, status):
        # 0 = backup the current hosts file
        # 1 = restore backup.
        pathExist = os.path.exists(self.hostbak)
        if(status == 0):
            if(pathExist == False):
                cpf(self.hostpath, self.hostbak)
        elif(status == 1):
            if(pathExist):
                os.remove(self.hostpath)
                os.rename(self.hostbak, self.hostpath)

    def __modify_hosts(self):
        self.__backup(0)
        subdomains = open(self.wlist).read().splitlines()
        domain_ip = get_dom_ip(self.target)
        host_file = open("/etc/hosts",'a')

        host_file.write("\n#iSubF modifications\n")
        for subdomain in subdomains:
            host_file.write(f"{domain_ip}   {subdomain}.{self.target}\n")
        host_file.close()

    def find(self):
        print("Finding..\n"+"="*20)
        self.__modify_hosts()
        # self.__backup(1)
        main_page = len(requests.get(f'http://{self.target}').content)
        for domain in open(self.wlist).read().splitlines():
            url = f"http://{domain}.{self.target}"
            try:
                r = requests.get(url)
                if(len(r.content) != main_page):
                    print(f"[Live]: {domain}.{self.target}")
            except KeyboardInterrupt:
                self.__backup(1)
                os._exit(0)
            except:
                pass

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

