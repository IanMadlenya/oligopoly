#parameters.py
from Tools import *
import commonVar as common

import networkx as nx
import matplotlib as mplt
import numpy.random as npr

def loadParameters(self):

  print "NetworkX version %s running" % nx.__version__
  print "Matplotlib version %s running\n" % mplt.__version__

  nxv=nx.__version__.split('.')
  vOK=False
  if int(nxv[0])>1: vOK=True
  if len(nxv)>=2:
      if int(nxv[0])==1 and int(nxv[1])>9: vOK=True
  if len(nxv)>=3:
      if int(nxv[0])==1 and int(nxv[1])==9 and int(nxv[2])>=1: vOK=True

  if not vOK:
		print "NetworkX 1.9.1 or greater required"
		os.sys.exit(1)
  #sigma of the normal distribution used in randomize the position of the agents/nodes
  print "sigma of the normal distribution used in randomizing the position of the agents/nodes ", common.sigma

  mySeed = input("random number seed (1 to get it from the clock) ")
  if mySeed == 1:
        random.seed()
        npr.seed()
  else:
        random.seed(mySeed)
        npr.seed(mySeed)

  self.nAgents = 0
  print "No 'bland' agents"

  #self.worldXSize= input("X size of the world? ")
  self.worldXSize=1
  #print "X size of the world not relevant"

  #self.worldYSize= input("Y size of the world? ")
  self.worldYSize=50
  #print "y size of the world not relevant"

  # Projct version and thresholds
  try: projectVersion = str(common.projectVersion)
  except: projectVersion = "Unknown"
  try: build = str(common.build)
  except: build = "Unknown"
  print "\nProject version "+projectVersion, "build", build, "\nhiringThreshold", common.hiringThreshold, \
                                    "firingThreshold", common.firingThreshold

  # wages
  print "wage base", common.wage

  # social welfare compensation
  print "social welfare compensation", common.socialWelfareCompensation

  # revenue of sales per worker (version 0)
  #print "revenues of sales for each worker in Version 0", \
  #      common.revenuesOfSalesForEachWorker

  # laboor productivity
  print "labor productivity", common.laborProductivity


  #Poisson mean in plannedProduction
  if common.projectVersion < 3:
   print "Mean value of the Poisson distribution used in production planning "+\
         "(not used in V.0; used only at t=1 in V.3);"
   tmp=raw_input(
      "suggested Lambda=5 (enter to confirm or input a number) ")
   try: common.Lambda=int(tmp)
   except: pass
   print "Resulting value", common.Lambda
  if common.projectVersion >= 3:

   print "Lambda, mean value of the Poisson distribution used in production\n"+\
         "planning at time=1, is set internally to match the ratio\n" + \
         "between actual and potential initial employed population,"
   print "set to %3.2f" %  common.rho

  #consumption
  print
  print "consumption behavior with Ci = ai + bi Yi + u\n"+\
        "u = N(0,%5.3f)" % common.consumptionRandomComponentSD
  print \
  ("(1) entrepreneurs as consumers with a1 = %4.2f b1 = %4.2f Y1 = profit(t-1)+wage\n"+ \
   "(2) employed workers           with a2 = %4.2f b2 = %4.2f Y2 = wage\n"+  \
   "(3) unemployed workers         with a3 = %4.2f b3 = %4.2f Y3 = socialWelfareCompensation")  \
   % (common.a1, common.b1, common.a2, common.b2, common.a3, common.b3)
  print

  print ("Relative threshold to became an entrepreneur %4.2f\n" +\
  "with new entrant extra costs %4.2f and duration of the extra cost %d") % \
  (common.thresholdToEntrepreneur, common.newEntrantExtraCosts, \
  common.extraCostsDuration)

  print "Random component of planned production %4.2f%s" % \
                             (common.randomComponentOfPlannedProduction*100, "%")

  print "Absolute barrier to become entrepreneur, max number in a time step: ", \
         common.absoluteBarrierToBecomeEntrepreneur

  print "\nRelative threshold to became an unemployed worker %4.2f\n" % common.thresholdToWorker

  print "Total demand relative random shock, uniformly distributed\nbetween "+\
        "-%3.2f and +%3.2f" % (common.maxDemandRelativeRandomShock,\
                               common.maxDemandRelativeRandomShock)


  # cycles
  self.nCycles = input("How many cycles? (0 = exit) ")

  v = raw_input("verbose? (y/[n]) ")
  if v=="y" or v=="Y":
    common.verbose=True #predefined False
  print "If running in IPython, the messages of the model about che creation" +\
        "\nof each agent are automatically off, to avoid locking the run."
