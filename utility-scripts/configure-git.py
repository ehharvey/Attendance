#! /usr/bin/python3


from pathlib import Path
import subprocess

CACHE_PATH = "./utility-scripts/.configured-developer"

DEVELOPERS = {
    "Emil": ("Emil Harvey", "ehharvey3704@conestogac.ca"),
    "Cole": ("Cole Foster", "Cfoster5841@conestogac.on.ca"),
    "Amanuel": ("Amanuel Negussie", "Anegussie9077@conestogac.on.ca"),
    "Justin": ("Justin Langevin", "Jlangevin@conestogac.on.ca"),
}


def main():
    """
    Takes in user input and configures git config
    """

    if Path(CACHE_PATH).is_file():
        with open(CACHE_PATH, "r", encoding="UTF-8") as f:
            dev = f.read().capitalize()
    else:
        dev = None

    while dev not in DEVELOPERS:
        dev = input("Please enter your FIRST name: ")
        dev.capitalize()

    with open(CACHE_PATH, "w+", encoding="UTF-8") as f:
        f.write(dev)

    subprocess.run(["git", "config", "user.name", DEVELOPERS[dev][0]], check=True)
    subprocess.run(["git", "config", "user.email", DEVELOPERS[dev][1]], check=True)

    print(f"Configured git use identity: {DEVELOPERS[dev]}")


if __name__ == "__main__":
    main()
