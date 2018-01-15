from subprocess import call
from importlib import import_module
from threading import Event, Thread
from time import sleep
import sys

# Set your pushbullet access token and other settings here
# Remove plugins you don't want to use
# Available plugins
# battery thermal uptime mpd monitor
# the value corresponding to plugin is the
# interval for notification for that notification

config  = { 
    'accessToken' : '',
    'plugins': {
        'battery': 50,
        'thermal': 80,
        'uptime': 120,
        'mpd': 150,
        'monitor': 180
    },
    'run_for': 100000
}

if config['accessToken'] == '':
    print('set config var accessToken to proceed')
    print('see project README for more info')
    sys.exit(0)

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
