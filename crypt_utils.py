import os


def update_UI():
    exit_code = os.system("pyuic5 -x FinApp_v1.ui -o designer.py")
    print("command ran with exit code %d" % exit_code)