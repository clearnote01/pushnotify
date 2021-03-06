from subprocess import check_output

class Plugin():
    def __init__(self):
        self.command = "mpc | head -n2"
        self.title = 'Music'
    def status(self):
        try:
            stat = check_output(self.command,shell=True).decode()
            print("stat: ", stat)
            self.title, stat,_ = stat.split("\n")
            self.title = self.title.replace("'","")
            stat = stat.replace("\n"," ")
            print(stat)
            return self.title, stat
        except ValueError:
            return self.title,'None'

if __name__ == '__main__':
    p = Plugin()
    print(p.status())
