import numpy as np
import scipy.stats.cauchy.rvs as cauchy

class SHADE:
    '''
    Implementation of the Success-History based Adaptative DE (SHADE)
    '''

    def __init__(self,Fun,lower_limit,upper_limit,max_FE,NP=100,LP=100,D=1000):
        self.Fun=Fun #Objective function 
        self.lower=lower_limit
        self.upper=upper_limit
        self.max_FE=max_FE #Maximum number of function evaluations
        self.evals=0 #current number of function evaluations
        self.NP=NP #Population size
        self.LP=LP #Memory size for parameters CR and F
        self.D=D #Dimension of the problem
        self.pmin=2/NP # Parameter for mutation

     
    def initialize(self):
        '''
        Function that initialize the population randomly
        Set the initial values of MCR and MF to 0.5
        '''
        self.Pop=np.random.random_sample((self.NP,self.D))*(self.upper-self.lower)+self.lower
        self.PopFitness=self.Fun(self.Pop) #fitness of population
        # si no funciona lo anterior usar lambdfy
        self.evals+=self.NP #update number of evaluations
        self.MCR=np.array([0.5]*self.LP) #initialize Crossover memory
        self.MF=np.array([0.5]*self.LP) #initialize F memory
        self.k=1 
        self.A=[]
        self.SCR=[]
        self.SF=[]

    def PBest1(self,rp,F):
        '''
        Performs the mutation strategy current-to-pbest/1
        vi=xi+Fi(x_pbest-xi)+Fi(x_r1-x_r2)
        '''
        pbest=np.random.uniform(self.pmin,0.2,size=self.NP)
        xbest=[]
        newPop=[]
        V=[]
        for i,p in enumerate(pbest):
            # ¿Puede ser x_pbest igual xi?
            xbest=np.argmin(self.PopFitness[:int(p*self.NP)])
            newPop=np.delete(range(self.NP),[i,xbest])
            #rand2 cambia si A no es vacío
            rand=np.random.choice(newPop,size=2)
            vi=self.Pop[i]+F[i]*(self.Pop[xbest]-self.Pop[i])+F[i]*(self.Pop[rand[0]]-self.Pop[rand[1]])
            V.append(vi)
        return V

    def BinCrossover(self,V,CR):
        '''
        Binomial Crossover
        '''
        U=np.zeros((self.NP,self.D))
        randJ=np.random.randint(0,self.D,size=self.NP)
        for i in range(self.NP):

        for i in range(self.D):
            rand=np.random.rand(self.NP)
            U[:,i]=np.where(rand<=CR,V[:,i],self.Pop[:,i])
        return U


    def solve(self):
        self.SCR=[]
        self.SF=[]
        #detalle de que evals puede pasar a max_FE si max_FE no es 
        #multiplo de NP
        while(self.evals<self.max_FE):
            rpi=np.random.randint(low=0,high=self.LP,size=self.NP)
            CRi=np.random.normal(self.MCR[rpi],0.1,size=self.NP)
            Fi=cauchy(self.MF[rpi],0.1,size=self.NP)
            V=self.PBest1(rpi,Fi)
            U=self.BinCrossover(V,CRi)
            Fitness_trials=self.Fun(U)
            self.evals+=self.NP
            for i in range(self.NP):
                if (Fitness_trials[i]<=self.PopFitness[i]):
                    self.Pop[i]=U[i]
                    if (Fitness_trials[i]<self.PopFitness[i]):
                        self.A.append(self.Pop[i])


