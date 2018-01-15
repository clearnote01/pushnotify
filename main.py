from subprocess import call
from importlib import import_module
from threading import Event, Thread
from time import sleep

config  = { 
    'accessToken' : 'o.o9TnYvEXOfma8DSzeU21nZgHaMfOcEXB',
    'plugins': {
        'battery': 5,
        'mpd': 5,
        'monitor': 5
    },
    'run_for': 100000
}

class Plugins():
    def __init__(self,config):
        self.plugins = config['plugins']
        self.count = len(self.plugins)
    def get_f(self, f_name):
        if f_name in self.plugins:
            module = import_module('plugins.'+f_name)
            plugin = module.Plugin()
            def funcer():
                title, body = plugin.status()
                pobj.send(title,body)
            return funcer
    def all_funcs(self):
        li = []
        for f_name in self.plugins:
            interval = self.plugins[f_name]
            func = self.get_f(f_name)
            li.append((func, interval))
        return li


plugins = Plugins(config)
class PushObject():
    def __init__(self):
        self.command = """curl --header 'Access-Token: """ + config['accessToken'] + """' \
                    --header 'Content-Type: application/json' \
                    --data-binary '{"body":"<bodyHere>","title": "<titleHere>","type":"note"}' \
                    --request POST \
                     https://api.pushbullet.com/v2/pushes"""
    def send(self,title,body):
        cmd = self.command.replace('<bodyHere>', body)
        cmd = cmd.replace('<titleHere>', title)
        call(cmd,shell=True)

pobj = PushObject()

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval):
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

try:
    threads = []
    for func,interval in plugins.all_funcs():
        t = call_repeatedly(interval,func)
        threads.append(t)
    sleep(config['run_for'])
finally:
    for thread in threads:
        thread()
