import os
import subprocess
import time

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
            os.system('nohup bash <nubit.sh > $HOME/nubit-light.log 2>&1 &')
            is_running('true')
            print("NODE STARTED RUNNING... the first start it takes time")
            time.sleep(5)
        else:
            print("Already running")
    print("###########################")
    main()


def status_node():
    os.system('clear')
    os.system('lsof -i :2121 | grep LISTEN')
    print("###########################")
    main()

def show_log_node():
    os.system('clear')
    os.system('tail -n 20 $HOME/nubit-light.log')
    print("###########################")
    main()

def further_check():
    os.system('clear')
    os.system('$HOME/nubit-node/bin/nubit das sampling-stats --node.store $HOME/.nubit-light-nubit-alphatestnet-1')
    print("###########################")
    main()

def show_pubkey():
    os.system('clear')
    os.system('$HOME/nubit-node/bin/nkey list --p2p.network nubit-alphatestnet-1 --node.type light')
    print("###########################")
    main()

def show_mnemonic():
    os.system('clear')
    os.system('cat $HOME/nubit-node/mnemonic.txt')
    print("###########################")
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
    print("###########################")

def stop_node():
    os.system('clear')
    os.system('kill $(lsof -t -i:2121)')
    is_running('false')
    print("NODE STOPED")
    print("###########################")
    main()

def exit_():
    os.system('exit')

def main():
    print("")
    print("Welcome NUBIT node manager...")
    print("")
    print("###########################")
    print("")
    print("1. Start NUBIT node. !!the first start it takes time. wait a few minutes!! Node will start automatically in background mode.")
    print("2. Status NUBIT node. Check whether the node is running or not. (wait a little after launch node)")
    print("3. Show log NUBIT node. Check the latest log.")
    print("*")
    print("4. For further check (Make sure your light node is running!)")
    print("5. Show Nubit node ADDRESS and PUBKEY (Make sure your light node is running!)")
    print("6. Show mnemonic words")
    print("*")
    print("7. !!!Stop NUBIT node!!!")
    print("8. !!!Delete mnemonic.txt!!!")
    print("-")
    print("0. Exit")
    print("")
    
    choice = int(input("Enter your choice: "))
    if choice == 1:
        start_node()
    elif choice == 2:
        status_node()
    elif choice == 3:
        show_log_node()
    elif choice == 4:
        further_check()
    elif choice == 5:
        show_pubkey()
    elif choice == 6:
        show_mnemonic()
    elif choice == 7:
        stop_node()
    elif choice == 8:
        delete_mnemonic()
    elif choice == 0:
        exit_()
    else:
        os.system('clear')
        print("Invalid choice. Please try again.")
        print("###########################")
        main()


if __name__ == '__main__':
    os.system('clear')
    os.system('curl https://nubit.sh > nubit.sh')

    main()
