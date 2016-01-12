#Agent.py
from Tools import *
from agTools import *
from random import *
import graphicDisplayGlobalVarAndFunctions as gvf
import commonVar as common
import numpy.random as npr

class Agent(superAgent):
    def __init__(self, number,myWorldState,
                 xPos=0, yPos=0, agType=""):

        #print xPos,yPos

        # the graph
        if gvf.getGraph() == 0: gvf.createGraph()
        common.g.add_node(self)

        # the environment

        self.agOperatingSets=[]
        self.number = number
        self.agType=agType
        self.numOfWorkers=0 #never use it directly to make calculations
        self.profit=0
        self.plannedProduction=0
        self.consumption=0
        self.employed=False
        self.extraCostsResidualDuration=0

        if agType == 'workers':
            common.orderedListOfNodes.append(self)
            #use to keep the order
            #in output (ex. adjacency matrix)

            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self]="OrangeRed"

            self.employed=False

        if agType == 'entrepreneurs':
            common.orderedListOfNodes.append(self)
            #use to keep the order
            #in output (ex. adjacency matrix)

            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self]="LawnGreen"

            self.employed=True
            self.plannedProduction=-100 #not used in plots if -100

        self.myWorldState = myWorldState
        self.agType=agType

        # the agents
        if common.verbose: print "agent of type", self.agType, \
               "#", self.number, "has been created at", xPos, ",", yPos

        gvf.pos[self]=(xPos,yPos)
        common.g_labels[self]=str(number)
        # to be used to clone (if any)
        self.xPos=xPos
        self.yPos=yPos

    # talk
    def talk(self):
	    print self.agType, self.number

    # reset values, redefining the method of agTools.py in $$slapp$$
    def setNewCycleValues(self):
        common.totalProductionInA_TimeStep=0
        common.totalPlannedConsumptionInValueInA_TimeStep=0

    # hireIfProfit
    def hireIfProfit(self):

        # workers do not hire
        if self.agType == "workers": return

        if self.profit<=common.hiringThreshold: return

        tmpList=[]
        for ag in self.agentList:
            if ag != self:
               if ag.agType=="workers" and not ag.employed:
                  tmpList.append(ag)

        if len(tmpList) > 0:
            hired=tmpList[randint(0,len(tmpList)-1)]

            hired.employed=True
            gvf.colors[hired]="Aqua"
            gvf.createEdge(self, hired) #self, here, is the hiring firm

        # count edges (workers) of the firm, after hiring (the values is
        # recorded, but not used directly)
        self.numOfWorkers=gvf.nx.degree(common.g, nbunch=self)
        # nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.
        print "entrepreneur", self.number, "has", \
              self.numOfWorkers, "edge/s after hiring"

    def hireFireWithProduction(self):

        # workers do not hire/fire
        if self.agType == "workers": return

        # to decide to hire/fire we need to know the number of employees
        # the value is calcutated on the fly, to be sure of accounting for
        # modifications coming from outside
        # (nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.)

        laborForce0=gvf.nx.degree(common.g, nbunch=self) + \
                           1 # +1 to account for the entrepreneur itself

        # required labor force
        laborForceRequired=int(
                    self.plannedProduction/common.laborProductivity)

        #???????????????????
        #countUnemployed=0
        #for ag in self.agentList:
        #    if not ag.employed: countUnemployed+=1

        #print "I'm entrepreneur %d laborForce %d and required %d unemployed are %d" %\
        #(self.number, laborForce0, laborForceRequired, countUnemployed)

        # no action
        if laborForce0 == laborForceRequired: return

        # hire
        if laborForce0 < laborForceRequired:
            n = laborForceRequired - laborForce0
            tmpList=[]
            for ag in self.agentList:
              if ag != self:
                 if ag.agType=="workers" and not ag.employed:
                    tmpList.append(ag)

            if len(tmpList) > 0:
                k = min(n, len(tmpList))
                shuffle(tmpList)
                for i in range(k):
                    hired=tmpList[i]
                    hired.employed=True
                    gvf.colors[hired]="Aqua"
                    gvf.createEdge(self, hired)
                    #self, here, is the hiring firm

            # count edges (workers) of the firm, after hiring (the values is
            # recorded, but not used directly)
            self.numOfWorkers=gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through once.
            print "entrepreneur", self.number, "is applying prod. plan and has", \
                  self.numOfWorkers, "edge/s after hiring"

        # fire
        if laborForce0 > laborForceRequired:
            n = laborForce0 - laborForceRequired

            # the list of the employees of the firm
            entrepreneurWorkers=gvf.nx.neighbors(common.g,self)
            #print "entrepreneur", self.number, "could fire", entrepreneurWorkers

            if len(entrepreneurWorkers) > 0: # has to be, but ...
                 shuffle(entrepreneurWorkers)
                 for i in range(n):
                    fired=entrepreneurWorkers[i]

                    gvf.colors[fired]="OrangeRed"
                    fired.employed=False

                    #common.g_edge_labels.pop((self,fired)) no labels in edges
                    common.g.remove_edge(self, fired)

            # count edges (workers) after firing (recorded, but not used
            # directly)
            self.numOfWorkers=gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through once.
            print "entrepreneur", self.number, "is applying prod. plan and has", \
                  self.numOfWorkers, "edge/s after firing"



    # fireIfProfit
    def fireIfProfit(self):

        # workers do not fire
        if self.agType == "workers": return

        if self.profit>=common.firingThreshold: return

        # the list of the employees of the firm
        entrepreneurWorkers=gvf.nx.neighbors(common.g,self)
        #print "entrepreneur", self.number, "could fire", entrepreneurWorkers

        if len(entrepreneurWorkers) > 0:
            fired=entrepreneurWorkers[randint(0,len(entrepreneurWorkers)-1)]

            gvf.colors[fired]="OrangeRed"
            fired.employed=False

            #common.g_edge_labels.pop((self,fired)) no label in edges
            common.g.remove_edge(self, fired)

            # count edges (workers) after firing (recorded, but not used
            # directly)
            self.numOfWorkers=gvf.nx.degree(common.g, nbunch=self)
            # nbunch : iterable container, optional (default=all nodes)
            # A container of nodes. The container will be iterated through once.
            print "entrepreneur", self.number, "has", \
                  self.numOfWorkers, "edge/s after firing"



    # produce
    def produce(self):

        # this is an entrepreneur action
        if self.agType == "workers": return


        # to produce we need to know the number of employees
        # the value is calcutated on the fly, to be sure of accounting for
        # modifications coming from outside
        # (nbunch : iterable container, optional (default=all nodes)
        # A container of nodes. The container will be iterated through once.)

        laborForce=gvf.nx.degree(common.g, nbunch=self) + \
                   1 # +1 to account for the entrepreneur itself
        print "I'm entrepreneur", self.number, "my laborforce is", laborForce

        # productivity is set to 1 in the benginning from common space
        self.production = common.laborProductivity * \
                          laborForce

        # totalProductionInA_TimeStep
        common.totalProductionInA_TimeStep += self.production


    # makeProductionPlan
    def makeProductionPlan(self):

        # this is an entrepreneur action
        if self.agType == "workers": return

        self.plannedProduction=npr.poisson(common.Lambda,1)[0] # 1 is the number
        # of element of the returned matrix (vector)



    # calculateProfit V0
    def evaluateProfitV0(self):

        # this is an entrepreneur action
        if self.agType == "workers": return

        # the number of pruducing workers is obtained indirectly via
        # production/laborProductivity
        #print self.production/common.laborProductivity
        self.profit=(self.production/common.laborProductivity) * \
                     (common.revenuesOfSalesForEachWorker - \
                      common.wage) + gauss(0,0.05)

    # calculateProfit
    def evaluateProfit(self):

        # this is an entrepreneur action
        if self.agType == "workers": return

        # backward compatibily to version 1
        try: XC=common.newEntrantExtraCosts
        except: XC=0
        try: k=self.extraCostsResidualDuration
        except: k=0

        if k==0: XC=0
        if k>0: self.extraCostsResidualDuration-=1

        # the number of pruducing workers is obtained indirectly via
        # production/laborProductivity
        #print self.production/common.laborProductivity
        self.profit=common.price * self.production - \
                    common.wage * (self.production/common.laborProductivity) - \
                    XC
        #print "profit", self.profit


    # compensation
    def planConsumptionInValue(self):
        self.consumption=0
        #case (1)
        #Y1=profit(t-1)+wage NB no negative consumption if profit(t-1) < 0
        # this is an entrepreneur action
        if self.agType == "entrepreneurs":
            self.consumption = common.a1 + \
                               common.b1 * (self.profit + common.wage) + \
                               gauss(0,common.consumptionRandomComponentSD)
            if self.consumption < 0: self.consumption=0
            #profit, in V2, is at time -1 due to the sequence in schedule2.xls

        #case (2)
        #Y2=wage
        if self.agType == "workers" and self.employed:
            self.consumption = common.a2 + \
                               common.b2 * common.wage + \
                               gauss(0,common.consumptionRandomComponentSD)

        #case (3)
        #Y3=socialWelfareCompensation
        if self.agType == "workers" and not self.employed:
            self.consumption = common.a3 + \
                               common.b3 * common.socialWelfareCompensation + \
                               gauss(0,common.consumptionRandomComponentSD)

        #update totalPlannedConsumptionInValueInA_TimeStep
        common.totalPlannedConsumptionInValueInA_TimeStep+=self.consumption
        #print "C sum", common.totalPlannedConsumptionInValueInA_TimeStep

    #to entrepreneur
    def toEntrepreneur(self):
        if self.agType != "workers" or not self.employed: return

        myEntrepreneur=gvf.nx.neighbors(common.g, self)[0]
        myEntrepreneurProfit=myEntrepreneur.profit
        if myEntrepreneurProfit >= common.thresholdToEntrepreneur:
            print "I'm worker %2.0f and myEntrepreneurProfit is %4.2f" %\
                  (self.number, myEntrepreneurProfit)
            common.g.remove_edge(myEntrepreneur, self)

            #originally, it was a worker
            if self.xPos>0:gvf.pos[self]=(self.xPos-15,self.yPos)
            #originally, it was an entrepreneur
            else:gvf.pos[self]=(self.xPos,self.yPos)
            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self]="LawnGreen"
            self.agType="entrepreneurs"
            self.employed=True
            self.extraCostsResidualDuration=common.extraCostsDuration


    #to workers
    def toWorker(self):
        if self.agType != "entrepreneurs": return

        if self.profit <= common.thresholdToWorker:
            print "I'm entrepreneur %2.0f and my profit is %4.2f" %\
                  (self.number, self.profit)



            # the list of the employees of the firm, IF ANY
            entrepreneurWorkers=gvf.nx.neighbors(common.g,self)
            print "entrepreneur", self.number, "has", len(entrepreneurWorkers),\
             "workers to be fired"

            if len(entrepreneurWorkers) > 0:
                for aWorker in entrepreneurWorkers:
                    gvf.colors[aWorker]="OrangeRed"
                    aWorker.employed=False

                    common.g.remove_edge(self, aWorker)

            self.numOfWorkers=0

            #originally, it was an entrepreneur
            if self.xPos<0:gvf.pos[self]=(self.xPos+15,self.yPos)
            #originally, it was a worker
            else:gvf.pos[self]=(self.xPos,self.yPos)
            # colors at http://www.w3schools.com/html/html_colornames.asp
            gvf.colors[self]="OrangeRed"
            self.agType="workers"
            self.employed=False


    # get graph
    def getGraph(self):
        return common.g
