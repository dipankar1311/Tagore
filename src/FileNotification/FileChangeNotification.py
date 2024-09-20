import os
import time
import glob

import sys
sys.path.append('../ocr')
#print(sys.path);
from ocr import detect_text

from speech_model_adaptation_beta import model_adaptation
class Watcher(object):
    running = True
    refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            print('New image file received')
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop        
    def watch(self):
        while self.running: 
            try: 
                # Look for changes
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])

# Call this function each time a change happens
def custom_action(text):
        filename = "../../resources/touchfile/*"
        detect_text(filename)
        model_adaptation()

        print("Removing touch file after processing")
        ff = glob.glob("../../resources/touchfile/*")
        for f in ff:
          os.remove(f)

if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
    watch_file = sys.argv[1]
else:
    watch_file = '../../resources/touchfile/filefortouch.txt'

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, custom_action, text='File is changed')  # also call custom action function
watcher.watch()  # start the watch going
