from subprocess import check_output

class Plugin():
    def __init__(self):
        self.command = "acpi -t"
    def status(self):
        stat = check_output(self.command,shell=True).decode()
        stat = stat.replace('\n',' ')
        self.title = 'Thermals'
        print(stat)
        return self.title,stat
