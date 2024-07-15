import os
import subprocess


welcome = """
#######################################
#                                     #
#    Welcome NUBIT node manager...    #
#                                     #
#######################################
"""

file = 'running'
path = os.path.join(os.getcwd(), file)
if not os.path.exists(path):
    with open(path, 'w') as f:
        f.write('false\n')
    print(f"file {file} created")
else:
    pass


def is_running(param:str):
    with open(path, 'w') as f:
        f.write(f'{param}\n')


def start_node():
    os.system('clear')
    with open(path, 'r') as f:
        if f.read().strip() == 'false':
            chars = ["-", "\\", "|", "/"]
            index = 0
            out_ = ''
            os.system('nohup bash <nubit.sh > $HOME/nubit-light.log 2>&1 &')
            is_running('true')
            print("NODE RUNNING... the first start it takes time")
            while out_ == '':
                char = chars[index % len(chars)]
                print(f"Выполнение: [{char}] ", end='\r')
                index += 1
                out = subprocess.run("lsof -i :2121 | grep LISTEN", shell=True, capture_output=True, text=True)
                out_ = out.stdout
            print("NODE STARTED")
        else:
            print("Already running")
    main()


def status_node():
    os.system('clear')
    out = subprocess.run("lsof -i :2121 | grep LISTEN", shell=True, capture_output=True, text=True)
    print(out.stdout)
    main()

def show_log_node():
    os.system('clear')
    os.system('tail -n 20 $HOME/nubit-light.log')
    main()

def further_check():
    os.system('clear')
    os.system('$HOME/nubit-node/bin/nubit das sampling-stats --node.store $HOME/.nubit-light-nubit-alphatestnet-1')
    main()

def show_pubkey():
    os.system('clear')
    # os.system('$HOME/nubit-node/bin/nkey list --p2p.network nubit-alphatestnet-1 --node.type light')
    out = subprocess.run("$HOME/nubit-node/bin/nkey list --p2p.network nubit-alphatestnet-1 --node.type light", shell=True, capture_output=True, text=True)
    print(out.stdout)

    main()

def show_mnemonic():
    os.system('clear')
    os.system('cat $HOME/nubit-node/mnemonic.txt')
    main()

def delete_mnemonic():
    os.system('clear')
    print("Are you sure you want to delete mnemonic.txt?")
    print("1. Yes")
    print("2. No")
    if int(input("Enter your choice: ")) == 1:
        # os.system('clear')
        os.system('rm $HOME/nubit-node/mnemonic.txt')
        main()
    elif int(input("Enter your choice: ")) == 2:
        # os.system('clear')
        main()
    else:
        print("Invalid choice. Please try again.")
        delete_mnemonic()

def stop_node():
    os.system('clear')
    os.system('kill $(lsof -t -i:2121)')
    is_running('false')
    print("NODE STOPED")
    main()

def exit_():
    os.system('exit')

def main():
    print("")
    print(welcome)
    print("""
1. Start NUBIT node. Node will start automatically in background mode.
2. Status NUBIT node. Check whether the node is running or not.
3. Show log NUBIT node. Check the latest log.

4. For further check. (Make sure your light node is running!)
5. Show Nubit node ADDRESS and PUBKEY. (Make sure your light node is running!)
6. Show mnemonic words.

7. !!!Stop NUBIT node!!!
8. !!!Delete mnemonic.txt!!!
 
0. Exit
""")
    
    choice = input("Enter your choice: ")
    if choice == "1": start_node()
    elif choice == "2": status_node()
    elif choice == "3": show_log_node()
    elif choice == "4": further_check()
    elif choice == "5": show_pubkey()
    elif choice == "6": show_mnemonic()
    elif choice == "7": stop_node()
    elif choice == "8": delete_mnemonic()
    elif choice == "0": exit_()
    else: main()


if __name__ == '__main__':
    os.system('clear')
    # os.system('cd ~')
    os.system('curl https://nubit.sh > nubit.sh')
    os.system('clear')
    main()
