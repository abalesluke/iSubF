try:
    import os, sys
    import requests
    import platform
    import threading
    from shutil import copyfile as cpf
except ImportError or ModuleNotFoundError as mod_err:
    modz_filter = []
    modz_filter.append(mod_err)
    mod_name = str(modz_filter[0]).replace('No module named ','')
    print("Error! Please Install Required Modules!\nRequired Module: {}".format(mod_name.replace("'",'')))
    exit()


def clear():
    if(platform.system() == "Windows"):
        print("Sorry this script only runs in linux systems!")
        os._exit(0)
    else:
        os.system("clear")

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

Usage: python3 {os.path.basename(__file__)} -s <self> -t <target>
Example: python3 {os.path.basename(__file__)} -s 127.0.0.1 -t 127.0.0.2
""")

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
    clear()
    if(os.getuid() != 0):
        print("Please this script as root!")
        os._exit(0)
    subFinder = Finder(1,2)
    subFinder.modify_hosts()


