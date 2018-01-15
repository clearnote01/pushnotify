from subprocess import check_output, CalledProcessError

processes = ['bash', 'banana', 'firefox']
class Plugin():
    def __init__(self):
        self.command = "pgrep -acx "
    def status(self):
        body = ''
        for p in processes:
            try:
                output = check_output('pgrep -xc '+p,shell=True).decode()
            except CalledProcessError:
                output = '0'
            body += p + ' : ' + output.strip('\n') + '              '
        self.title = 'Monitoring process'
        return (self.title, body)
