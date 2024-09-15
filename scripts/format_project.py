import subprocess


def format_project():
    print("Running Black formatter...")
    subprocess.run(["black", "."])


if __name__ == "__main__":
    format_project()
