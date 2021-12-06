import os
import glob
import subprocess
import re
from time import sleep

def read_subjects(subj_file="./subjects.txt", excl_file="./exclude.txt"): 
  """
  Function to read the subjects to use from a file and return them as a
  list. The file contains each subject as a single line.
  An additional exclude File lists the subjects to exclude from the list.
  """
  try:
    with open(subj_file, mode="r") as f:
      subjects = [line.rstrip("\n") for line in f.readlines()]
  except FileNotFoundError:
      subjects = []
  try:
    with open(excl_file, mode="r") as f:
      excl = [line.rstrip("\n") for line in f.readlines()]
  except FileNotFoundError:
      excl = []
  subjects = [subj for subj in subjects if subj not in excl]
  return(subjects)

def convertSequence(seq_old, seq_new, proband, session, sequence, visitnr):
  """ This function calls a process with dcm2niix for the defined sequence.
  """
  os.makedirs(os.path.join(outpath, proband[16:19]), exist_ok=True)
  os.makedirs(os.path.join(outpath, "dcm2niix-output"), exist_ok=True)
  if re.search(seq_old, sequence) is not None:
    procs.append( ( subprocess.Popen([ "dcm2niix", 
      "-z", "n", 
      "-f", proband[16:19]+"_"+seq_new+"_"+visitnr,
      "-o", os.path.join(outpath, proband[16:19]),
      os.path.join(path, proband, session, sequence) ],
      stdout=subprocess.PIPE, stderr=subprocess.PIPE),
      proband[16:19]+"_"+seq_new+"_"+visitnr) )

def checkProcFinished(procs):
  """ This function checks if the processes are finished yet and writes
      STDOUT and STDERR to a log file.
  """
  finished_procs = []
  for proc, pinfo in procs:
    if type(proc.poll()) is int: # check if proc finished
      sto, ste = proc.communicate()
      with open(os.path.join(outpath, "dcm2niix-output", pinfo+".log"), "w") as file:
        file.write("#####LOGMSG#####\n")
        file.write(pinfo)
        file.write("################\n")
        if (proc.poll() != 0):
          file.write("\n-----RETVAL-----\n")
          file.write(str(proc.poll()))
        if (len(ste) > 0):
          file.write("\n-----STDERR-----\n")
          file.write(ste.decode())
        file.write("\n-----STDOUT-----\n")
        file.write(sto.decode())
        file.write("################")
      #proc.terminate() # killed automatically after communicate command
      procs.remove((proc, pinfo))

if __name__ == "__main__":
  # read simple text-based config file with the following lines:
  # - path to the genfi images data folder
  # - path to the output folder
  with open("./config.txt", mode="r") as f:
    (path, outpath) = [line.rstrip("\n") for line in f.readlines()]

  # read subject and exclude list
  subjects = read_subjects()

  # time to wait
  wait_time = 5

  # number of max processes (actual number will be slightly higher)
  n_procs = 8

  procs = [] # empty list for processes called later
  os.chdir(path)
  probands = glob.glob("*")

  for proband in probands:
    while (len(procs) >= n_procs): # check number of processes
      sleep(wait_time) 
      checkProcFinished(procs)
    os.chdir(os.path.join(path, proband))
    sessions = glob.glob("*")
    for session in sessions:
      if (proband in subjects or not subjects):
        os.chdir(os.path.join(path, proband, session))
        sequences = glob.glob("*")
        visitnr = session[-1] # a number, stored as string
        for sequence in sequences:
          convertSequence("02_T1w_MPR", "T1w_02", proband, session, sequence, visitnr)
          convertSequence("03_T1w_MPR", "T1w_03", proband, session, sequence, visitnr)
          convertSequence("04_gre_field_mapping", "FieldMap_04", proband, session, sequence, visitnr)
          convertSequence("05_gre_field_mapping", "FieldMap_05", proband, session, sequence, visitnr)
          convertSequence("06_SpinEchoFieldMap_RS_AP", "SpinEchoFieldMap_RS_AP", proband, session, sequence, visitnr)
          convertSequence("07_SpinEchoFieldMap_RS_AP", "SpinEchoFieldMap_RS_PA", proband, session, sequence, visitnr)
          convertSequence("08_fMRI_RS_AP_SBRef", "fMRI_RS_AP_SBRef_08", proband, session, sequence, visitnr)
          convertSequence("09_fMRI_RS_AP", "fMRI_RS_AP_09", proband, session, sequence, visitnr)
          convertSequence("10_fMRI_EMO_AP_SBRef", "fMRI_EMO_AP_SBRef_10", proband, session, sequence, visitnr)
          convertSequence("11_fMRI_EMO_AP", "fMRI_EMO_AP_11", proband, session, sequence, visitnr)
          convertSequence("12_fMRI_LAUGHTER_AP_SBRef", "fMRI_LAUGHTER_AP_SBRef_12", proband, session, sequence, visitnr)
          convertSequence("13_fMRI_LAUGHTER_AP", "fMRI_LAUGHTER_AP_13", proband, session, sequence, visitnr)
          convertSequence("14_dMRI_dir65_AP_SBRef", "dMRI_dir65_AP_SBRef_14", proband, session, sequence, visitnr)
          convertSequence("15_dMRI_dir65_AP", "dMRI_dir65_AP_15", proband, session, sequence, visitnr)
          convertSequence("16_dMRI_dir65_AP_ADC", "dMRI_dir65_AP_ADC_16", proband, session, sequence, visitnr)
          convertSequence("17_dMRI_dir65_AP_TRACEW", "dMRI_dir65_AP_TRACEW_17", proband, session, sequence, visitnr)
          convertSequence("18_dMRI_dir65_AP_FA", "dMRI_dir65_AP_FA_18", proband, session, sequence, visitnr)
          convertSequence("19_dMRI_dir65_AP_ColFA", "dMRI_dir65_AP_ColFA_19", proband, session, sequence, visitnr)
          convertSequence("20_dMRI_dir65_PA_SBRef", "dMRI_dir65_PA_SBRef_20", proband, session, sequence, visitnr)
          convertSequence("21_dMRI_dir65_PA", "dMRI_dir65_PA_21", proband, session, sequence, visitnr)
          convertSequence("22_dMRI_dir65_PA_TRACEW", "dMRI_dir65_PA_TRACEW_22", proband, session, sequence, visitnr)

  while(len(procs) > 0):
    checkProcFinished(procs) # wait until all processes are done
    sleep(wait_time) 
