import subprocess
import sys
from threading import *
import traceback
from queue import Queue,Empty
#ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
class ThreadExec(Thread):
    def __init__(self,programmeName,args,stdout,stdin,events):
        Thread.__init__(self)
        self.programmeName=programmeName
        self.args=args
        self.stdin=stdin
        self.stdout=stdout
        self.result=None
        self.events=events
    def run(self):

            

        
        subProcess=subprocess.Popen(self.programmeName,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        
        
        q = Queue()
        t = Thread(target=enqueue_output,args=(subProcess.stdout,q))
        t.daemon = True
        t.start()
      
        try:
            while(1):
                if subProcess.returncode != None:
                    break
                try:
                    line = q.get(timeout=2)
                    print(line)
                    line = line.decode("utf-8")
                    for i in range(len(events)):
                        if events[i]["MOTIF"] in line and len(events[i]["ACTION"]) > 0 :

                            subProcess.stdin.write(events[i]["ACTION"][0].encode("utf-8"))
                            print(events[i]["ACTION"][0].encode("utf-8"))
                            subProcess.stdin.write("\n".encode("utf-8"))
                            events[i]["ACTION"].pop(0)
                            subProcess.stdin.flush()
                except Empty:
                    for i in range(len(events)):
                        if events[i]["MOTIF"] == "EMPTY" and len(events[i]["ACTION"]) > 0 :
                            print("EMPTY")
                            subProcess.stdin.write(events[i]["ACTION"][0].encode("utf-8"))
                            print(events[i]["ACTION"][0].encode("utf-8"))
                            subProcess.stdin.write("\n".encode("utf-8"))
                            events[i]["ACTION"].pop(0)
                            subProcess.stdin.flush()


            self.result=subProcess.returncode
        except IOError:
            ##print(traceback.format_exc())
            pass
        subProcess.wait()
        self.result=subProcess.returncode
    def getResult(self):
        return self.result

def createEvent(motif,actions):
    if len(actions) ==1:
        return {"MOTIF":motif,"ACTION":[actions]}
    else:
        return {"MOTIF":motif,"ACTION":[actions]}
class SubprocessGenerator:
    def __init__(self):
        self.processList=[]
        self.processEndedStatus=[]
    def addProcess(self,programmeName,events,args=None,stdout=None,stdin=None,):
        thread=ThreadExec(programmeName,args,stdout,stdin,events)
        self.processList.append(thread)
        thread.start()
        
    def __getitem__(self,key):
        return self.processEndedStatus[key]

    def waitAll(self):
        for i in range(len(self.processList)):
            self.processList[i].join()
            result=self.processList[i].getResult()
            self.processEndedStatus.append({"number":i,"code":result})
        return self.processEndedStatus



## Test code 
generator=SubprocessGenerator()

event=createEvent("?","5")
event2=createEvent("EMPTY","5")
events=[event,event2]
generator.addProcess(programmeName="/tmp/test",events=events)
result=generator.waitAll()
print(result)
print(generator[0])
