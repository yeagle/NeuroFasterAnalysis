from Process import ProcessHandler
import os

class Convert2Nifti(ProcessHandler):
  """
  Provides functions to convert from dicom to nifti format.
  """

  def __init__(self, sourcedir, outputdir, subjects=False, exclude=False, qsub=False, screen=False):
    """
    Initialization of Process object.
    """
    ProcessHandler.__init__(self, qsub, screen)

    self.sourcedir = sourcedir
    self.outputdir = outputdir
    self.subjects = subjects
    self.exclude = exclude

    os.makedirs(os.path.join(self.outputdir, "log_dcm2niix"), exist_ok=True)
    if (self.qsub):
      os.makedirs(os.path.join(self.outputdir, "log_qsub"), exist_ok=True)

  def convertSequence(seq_old, seq_new, proband, session, sequence, visitnr):
    """ 
    This function calls a process with dcm2niix for the defined sequence.
    """
    os.makedirs(os.path.join(outpath, proband[16:19]), exist_ok=True)
    if (self.proc == None):
      cmd = []
      cmd.extend([ "dcm2niix", 
        "-z", "n", 
        "-f", proband[16:19]+"_"+seq_new+"_"+visitnr,
        "-o", os.path.join(self.outputdir, proband[16:19]),
        os.path.join(self.sourcedir, proband, session, sequence) ])
