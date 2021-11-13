import os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--main", help="main",
                    type=ascii, default="mobot_cmdvel")


parser.add_argument("-p", "--port", help="Port",
                    type=ascii, default="/dev/ttyUSB0")

parser.add_argument("-b", "--baud", help="Baud Rate",
                    type=int, default=115200)

parser.add_argument("--src", help="Upload src", action="store_true")

parser.add_argument("--clean", help="Clean board", action="store_true")

args = parser.parse_args()

if args.clean:
    print("Cleaning the board ...")
    out = os.popen(\
        f"ampy --port {args.port[1:-1]} --baud {args.baud} ls"\
    )

    files = out.read()[:-1].split("\n")
    for f in files:
        if f != '/main.py' and f != '/boot.py' and f != '/webrepl_cfg.py':
            if len(f.split('.')) > 1:
                os.system(f"ampy --port {args.port[1:-1]} --baud {args.baud} rm {f}")
                print(f"Deleated File: {f}")
            else:
                os.system(f"ampy --port {args.port[1:-1]} --baud {args.baud} rmdir {f}")
                print(f"Deleated Directory: {f}")
    print("Cleaned!")
    sys.exit()

files = os.listdir('./src')

if f"{args.main[1:-1]}.py" not in files:
    print(f"{args.main[1:-1]}.py is not in src")
    sys.exit()

if args.src:
    for file in files:
        print(f"Uploading {file} ...")
        os.system(f"ampy --port {args.port[1:-1]} --baud {args.baud} put ./src/{file}")
        print("Uploaded!")

main_src =\
f"""from {str(args.main[1:-1])} import main

if __name__ == '__main__':
    main()
"""

main_fd = open("/tmp/main.py", "w")
main_fd.write(main_src)
main_fd.close()

print("Uploaded main.py ...")
os.system(f"ampy --port {args.port[1:-1]} --baud {args.baud} put /tmp/main.py")
print("Uploaded!")
