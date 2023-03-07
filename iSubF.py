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

def default_wlist():
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

def help():
    banner()
    print(f"""
Required Arguments:
    -t, --target       : Target ip
    -d, --domain       : Domain

Usage: python3 {os.path.basename(__file__)} -s <self> -t <target>
Example: python3 {os.path.basename(__file__)} -s 127.0.0.1 -t 127.0.0.2
""")

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
        self.new_args[arg] = arg_val
    
    def get_args(self)->exec:return self.new_args



class Finder:
    def __init__(self,target, wpath):
        self.target = target
        self.wlist = wpath
        self.hostpath = '/etc/hosts'
        self.hostbak = self.hostpath+'.iSubF.bak'

    def backup(self, status):
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

    def modify_hosts(self):
        self.backup(0)
        host_file = open("/etc/hosts",'a')
        host_file.write("\n#iSubF modifications\n")
        self.backup(1)


if(__name__=="__main__"):
    parser = FoxParse()
    parser.parse_args()
    args = parser.get_args()
    print(args)
    exit(0)
    clear()
    if(os.getuid() != 0):
        print("Please this script as root!")
        os._exit(0)
    subFinder = Finder(domain, wordlist_path)
    subFinder.modify_hosts()

