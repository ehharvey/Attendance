#! /usr/bin/python3


import subprocess

DEVELOPERS = {
    "Emil": ("Emil Harvey", "ehharvey3704@conestogac.ca"),
    "Cole": ("Cole Foster", "Cfoster5841@conestogac.on.ca"),
    "Amanuel": ("Amanuel Negussie", "Anegussie9077@conestogac.on.ca"),
    "Justin": ("Justin Langevin", "Jlangevin@conestogac.on.ca")
}


def main():
    """
    Takes in user input and configures git config
    """
    
    while (True):
        dev = input("Please enter your FIRST name: ")
        dev.capitalize()
        if dev in DEVELOPERS:
            break
    
    subprocess.run(["git", "config", "user.name", DEVELOPERS[dev][0]])
    subprocess.run(["git", "config", "user.email", DEVELOPERS[dev][1]])

    print(f"Configured git use identity: {DEVELOPERS[dev]}")

if __name__ == "__main__":
    main()
