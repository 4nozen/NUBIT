import os
import re
import subprocess


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALICS = '\033[3m'
    FADED = '\033[2m'
    UNDERLINE = '\033[4m'


class Text:
    welcome = Color.HEADER + """
            ####################################################
            #                                                  #
            #             Welcome NUBIT node manager           #
            #              For full documentaion on            #
            #    https://docs.nubit.org/nubit-da/run-a-node    #
            #          discord https://discord.gg/nubit        #
            #                                                  #
            ####################################################
                """ + Color.ENDC
    menu = f"""
        1. {Color.OKBLUE}{Color.BOLD}Start NUBIT NODE.{Color.ENDC}
           {Color.ITALICS} node will start automatically in background mode.{Color.ENDC}
        2. {Color.OKBLUE}{Color.BOLD}Status NUBIT NODE.{Color.ENDC}
           {Color.ITALICS} check whether the node is running or not.{Color.ENDC}
        3. {Color.OKBLUE}{Color.BOLD}Show NUBIT node logs.{Color.ENDC}
           {Color.ITALICS} check the latest log.{Color.ENDC}
        ---------------------------------------------------------------------------
        4. {Color.OKBLUE}{Color.BOLD}For further check.{Color.ENDC}
           {Color.ITALICS} make sure your light node is running!{Color.ENDC}
        5. {Color.OKBLUE}{Color.BOLD}Show Nubit node ADDRESS and PUBKEY.{Color.ENDC}
           {Color.ITALICS} make sure your light node is running!{Color.ENDC}
        6. {Color.OKBLUE}{Color.BOLD}Show mnemonic words.{Color.ENDC}
        ---------------------------------------------------------------------------
        7. {Color.WARNING}!!! Stop NUBIT node !!!{Color.ENDC}
        8. {Color.WARNING}!!! Delete mnemonic.txt !!!{Color.ENDC}
        ---------------------------------------------------------------------------
        0. Exit
        """

class Console:
    def __init__(self):
        self.log_lines = '2'
        self.run_flag: bool = None

    def start_node(self):
        os.system('clear')
        if console.run_flag is False:
            chars = ["-", "\\", "|", "/"]
            index = 0
            out_ = ''
            os.system('nohup bash <nubit.sh > $HOME/nubit-light.log 2>&1 &')
            print(f"NODE RUNNING... {Color.FADED}the first start it takes time{Color.ENDC}")
            while out_ == '':
                char = chars[index % len(chars)]
                print(f"in progress: [{char}] ", end='\r')
                index += 1
                out = subprocess.run("lsof -i :2121 | grep LISTEN", shell=True, capture_output=True, text=True)
                out_ = out.stdout
            print(f"{Color.BOLD}{Color.OKGREEN}NODE STARTED{Color.ENDC}")
        else:
            os.system(f'echo "{Color.FADED}checking status...{Color.ENDC}"')
            print(f"{Color.BOLD}{Color.OKGREEN}Already running{Color.ENDC}")
        self.run_flag = True
        menu()

    def node_running(self):
        os.system('clear')
        os.system(f'echo "{Color.FADED}checking status...{Color.ENDC}"')
        if subprocess.run("lsof -i :2121 | grep LISTEN", shell=True, capture_output=True, text=True).stdout == '':
            print(f'node is {Color.BOLD}{Color.FAIL}NOT RUNNING{Color.ENDC}')
            self.run_flag = False
            menu()
        else:
            print(f'node is {Color.BOLD}{Color.OKGREEN}RUNNING{Color.ENDC} on:')
            print(subprocess.run("lsof -i :2121 | grep LISTEN", shell=True, capture_output=True, text=True).stdout)
            self.run_flag = True
            menu()
        return self.run_flag

    def show_log(self):
        os.system('clear')
        print(subprocess.run(f"tail -n {self.log_lines} $HOME/nubit-light.log", shell=True, capture_output=True, text=True).stdout)
        menu()

    def further_check(self):
        os.system('clear')
        if self.run_flag:
            print(subprocess.run('$HOME/nubit-node/bin/nubit das sampling-stats --node.store $HOME/.nubit-light-nubit-alphatestnet-1', shell=True, capture_output=True, text=True).stdout)
            menu()
        else:
            print(f'node is {Color.BOLD}{Color.FAIL}NOT RUNNING{Color.ENDC}')
            print(f'please {Color.HEADER}{Color.BOLD}Start NUBIT NODE.{Color.ENDC}')
            menu()
    
    def show_info(self):
        os.system('clear')
        out = subprocess.run('$HOME/nubit-node/bin/nkey list --p2p.network nubit-alphatestnet-1 --node.type light', shell=True, capture_output=True, text=True).stdout
        print(re.search(r'address.*\n', out)[0])
        out = subprocess.run('$HOME/nubit-node/bin/nkey list --p2p.network nubit-alphatestnet-1 --node.type light', shell=True, capture_output=True, text=True).stdout
        print(re.search(r'"key":"([^}]*)', out)[0])
        menu()

    def show_mnemonic(self):
        os.system('clear')
        os.system('cat $HOME/nubit-node/mnemonic.txt')
        menu()

    def delete_mnemonic(self):
        os.system('clear')
        print(f"{Color.WARNING}### Are you sure you want to delete mnemonic.txt? ###{Color.ENDC}")
        print("1. Yes")
        print("2. No")
        answ = input("Enter your choice: ")
        if answ == "1":
            os.system('clear')
            os.system('rm $HOME/nubit-node/mnemonic.txt')
            menu()
        elif answ == "2":
            os.system('clear')
            menu()
        else:
            os.system('clear')
            print("Invalid choice. Please try again.")
            self.delete_mnemonic()

    def stop_node(self):
        os.system('clear')
        if self.run_flag:
            os.system('kill $(lsof -t -i:2121)')
            print(f"node is {Color.BOLD}{Color.FAIL}NODE STOPED{Color.ENDC}")
            self.run_flag = False
            menu()
        else:
            print(f"node is not {Color.BOLD}{Color.FAIL}NOT RUNNING{Color.ENDC}")
            menu()


def exit_manager():
    os.system('exit')


def menu():
    print("")
    print(Text.welcome)
    print(Text.menu)
    choice = input("Enter your choice: ")
    if choice == "1": console.start_node()
    elif choice == "2": console.node_running()
    elif choice == "3": console.show_log()
    elif choice == "4": console.further_check()
    elif choice == "5": console.show_info()
    elif choice == "6": console.show_mnemonic()
    elif choice == "7": console.stop_node()
    elif choice == "8": console.delete_mnemonic()
    elif choice == "0": exit_manager()
    else:
        os.system('clear')
        menu()


if __name__ == '__main__':
    os.system('clear')
    os.system(f'echo "{Color.FADED}copying from https://nubit.sh{Color.ENDC}"')
    os.system('echo ""')
    os.system('curl https://nubit.sh > nubit.sh')
    os.system('clear')
    console = Console()
    console.node_running()
