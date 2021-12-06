import subprocess
from os import path
from time import time as timestamp

class ProcessHandler():
  """
  Process class to deal with process handling. 
  Serves as parent class. 
  """

  def __init__(self, qsub=False, screen=False):
    """
    Initialization of Process object.
    """
    self.proc = None
    self.screen = screen
    self.qsub = qsub

  def call(self, cmd):
    """
    Call cmd with subprocess.Popen.
    """
    if (self.proc == None):
      cmd.reverse()
      if(self.qsub):
        qsubcmd = ["qsub", "-q", "verylong.q", 
                   "-v", "SUBJECTS_DIR="+self.subjdir,
                   "-b", "y", 
                   "-wd", path.join(self.subjdir, "qsub-output")]
        qsubcmd.reverse()
        cmd.extend(qsubcmd)
      if (self.screen):
        screencmd = ["screen", "-S", self.id, "-d", "-m"]
        screencmd.reverse()
        cmd.extend(screencmd)
      cmd.reverse()
      self.proc = subprocess.Popen(" ".join(cmd), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, executable="/bin/tcsh")
      if (self.screen):
        self.wait() # otherwise the following commands will be called to quickly
        subprocess.call(["screen", "-S", self.id, "-X", "logfile",
          path.join(self.subjdir, self.id, "scripts",
            "screenlog_"+cmd[5]+"_"+self.id+"_"+str(round(timestamp(), 0))[:-2]+".log")])
        subprocess.call(["screen", "-S", self.id, "-X", "log"])
      return(True)
    else:
      return(False)

  def communicate(self):
    """
    Checks if the subprocess is finished. 
    If subprocess is finished, the variable storing the subprocess will be
    reset to None.

    returns STDOUT, STDERR and RETVAL of subprocess if it is finished;
    returns None if subprocess is not finished;
    returns None if there is no subprocess (anymore), when subprocess
      variable is None.
    """
    if (self.proc != None):
      retval = self.proc.poll()
      if (type(retval) == int):
        sto, ste = self.proc.communicate()
        self.proc = None
        return (sto, ste, retval)
    return None

  def wait(self):
    """
    Calls subprocess.wait() to wait for process to finish.
    """
    if (self.proc != None):
      self.proc.wait()
