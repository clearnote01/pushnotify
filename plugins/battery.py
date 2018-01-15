from subprocess import check_output

class Plugin():
    def __init__(self):
        self.command = "acpi"
    def status(self):
        stat = check_output(self.command,shell=True).decode()
        stat = stat.replace('\n',' ')
        print(stat)
        self.title = 'Battery'
        return self.title, stat
