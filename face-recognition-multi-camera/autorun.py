from subprocess import Popen
import sys
import datetime
import os

filename = sys.argv[1]

try:
    while True:
        # print("\nStarting " + filename)
        # p = Popen("python3 " + filename, shell=True)    
        # timeout
        print('start')
        now = datetime.datetime.now()
        target = 'log/{}'.format(str(now)[:19])

        if not os.path.exists(target):
            os.mkdir(target)

        outPath = '{}/out.log'.format(target)
        errPath = '{}/err.log'.format(target)

        p = Popen([sys.executable, filename, target], 
            stdout=open(outPath, 'a+'), 
            stderr=open(errPath, 'a+'),
            )
        print('wait')
        p.wait()
        print('end')
except:
    print('Terminate long running script')
    p.terminate()