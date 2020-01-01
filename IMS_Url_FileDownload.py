"""Python File to Download the IMS URL """
import traceback
import urllib
import sys
import re
import subprocess
from optparse import OptionParser

if sys.version_info < (2, 8):
    import ConfigParser
else:
    import configparser

import os


def formatExceptionInfo(maxTBlevel=5):
    """Function to handle Execption """
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


class ims_obj():

    """
    Description: The IMS access class
    """

    def __init__(self):
        """Function to Intialize """

        self.Host = ""
        self.Port = ""
        self.ProjectType = "project"
        self.CpId = ""
        self.ims_username = ""
        self.ims_password = ""
        self.ims_url = ""
        self.ims_destination_path = ""
        self.member_revision = ""
        self.member_name = ""
        self.ProjectPath = ""
        self.ims_user = ""
        self.ims_password = ""


    def SetHost(self, Host):
        """Function to set the IMS Host Name."""
        self.Host = Host

    def SetPort(self, Port):
        """Function to set the IMS Port """
        self.Port = Port

    def SetUserName(self, username):
        """Function to set the IMS User Name """
        self.ims_username = username

    def SetPassword(self, password):
        """Function to set the IMS Password """
        self.ims_password = password

    def SetCpId(self, CpId):
        """Function to set the IMS Change Package ID """
        self.CpId = CpId

    def SetProjectType(self, ProjectType):
        """Function to set the IMS Project Type """
        self.ProjectType = ProjectType

    def SetUserIdPassword(self, user, pass_word):
        """Function to set the IMS UserID Password """
        if(user != ""):
            self.ims_user = '--user=' + user
        else:
            self.ims_user = '--user=' + ''

        if(pass_word != ""):
            self.ims_password = '--password=' + pass_word
        else:
            self.ims_password = '--password=' + ''

    def ims_url_download(self, arguments, ims_url):
        """Function to Download the IMS URL """
        ret = 0;
        usage = r"""usage : %prog ims_url_download [options]
        Example: python %prog ims_url_download -H ims-adas -P 7001 -u uidr2685 -p Ganapathi@54 --d D:\python\IMS_File_Download"""

        # parse the arguments
        parser = OptionParser(usage)
        parser.add_option("-H", "--Host", dest="Host",
                          help="e.g. mks-psad (mandatory)", metavar="mks-psad")
        parser.add_option("-P", "--Portconfig", dest="Port",
                          help=" e.g. 7001 (mandatory)", metavar="7001")

        parser.add_option("-u", "--user_name", dest="username",
                            help="uidr2685")
        parser.add_option("-p", "--password",
                          dest="password",
                          help = " e.g Ganadslk")
        parser.add_option("-d", "--destpath", \
                          dest="destpath", \
                          help = " e.g D:\\Test\\")
        (options, args) = parser.parse_args(arguments)

        self.Host = options.Host
        self.Port = options.Port
        self.ims_username = options.username
        self.ims_password = options.password
        self.ims_url = ims_url
        self.ims_destination_path = options.destpath
        if(args == ''):
            args = 'None'

        #Decode the http encoding
        self.ims_url = str(urllib.unquote(self.ims_url).decode('utf8'))

        #Intialize
        self.ProjectPath = ""
        self.member_name = ""
        self.member_revision = ""

        match = re.search(r'projectName=(.*?)&', self.ims_url)
        if match:
            self.ProjectPath = match.group(1)
        else:
            print("Failed the extract project path")
            return 1

        match = re.search(r'&revision=([\d.]+)', self.ims_url)
        if match:
            self.member_revision = match.group(1)
        else:
            print("Failed the extract member revision of the file")
            return 1

        match = re.search(r'&selection=([\w.-]+)', self.ims_url)
        if match:
            self.member_name = match.group(1)
        else:
            print("Failed the extract member name of the file")
            return 1

        self.ims_destination_path = self.ims_destination_path
        + "\\" + self.member_name

        print("Project Path     :   " + self.ProjectPath)
        print("Member Name      :   " + self.member_name)
        print("Member Revision  :   " + self.member_revision)
        print("Destination Path :   " + self.ims_destination_path)

        cmdline_info = 'si viewrevision --batch --hostname=%s --port=%s \
        --forceConfirm=yes --quiet --user=%s --password=%s --project=%s \
        --revision=%s %s > %s' \
        %(self.Host, self.Port,self.ims_username,self.ims_password,
        self.ProjectPath,self.member_revision,self.member_name,
        self.ims_destination_path)

        try:
            proc = subprocess.Popen(cmdline_info, 
									shell=True, 
									bufsize=-1, 
									stdout=subprocess.PIPE, 
									stderr=subprocess.PIPE)
            stdout_str, stderr_str = proc.communicate()
            stdout_str_lines = stdout_str.splitlines()
            if len(stderr_str) != 0:
                print(cmdline_info)
                stderr_str = stderr_str.replace('\r\n', "")
                print("Error", stderr_str.replace('\r\n', ""))
                return "1"
            print(stdout_str_lines)

        except(OSError, ValueError):
            print(formatExceptionInfo())
            return "1"
        print("")
        print("****************************************************")
        print("Downloaded IMS Url " + self.ims_url + " Successfully")
        print("")
        return ret


def print_help():
    """
    print_help()

    Description: Print the Help menu
    """
    print("""Usage:
    python IMS_Url_Download.py ims_url_download [options e.g. -h for help]
    """)

def main(argv):
    """
    main()

    Description: the main function
    """

    base_path = os.path.dirname(__file__)
    ini_file_path = os.path.abspath(os.path.join(base_path,"IMS_DownloadURL_List.ini"))

    ims_url = ""
    if (argv[1] == "ims_url_download"):
        if len(argv)  < 12:
            argv.append("-h")

        res = 0
        if sys.version_info < (2, 8):
            config = ConfigParser.ConfigParser()
        else:
            config = configparser.ConfigParser()

        config.read(ini_file_path)
        url_sections = config.sections()
        if(len(url_sections) > 0):
            for i in range(0, len(url_sections)):
                ims_url = config.get(url_sections[i],'IMS_URL')
                print("****************************************************")
                print("")
                print("Downloading ...")
                print("ims_url " + ims_url)
                print("")
                res = ims_obj().ims_url_download(argv, ims_url)
                if(res != 0):
                    print("**** Error in Downloading File " + ims_url)
                    sys.exit(res)
        else:
            print("**** Failed to read the IMS_DownloadURL_List.ini file")
            sys.exit(2)

    else:
        print_help()

    sys.exit(res)

# check input args
if (len(sys.argv) > 1):
    main(sys.argv)
else:
    print_help()






