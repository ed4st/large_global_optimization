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
        self.k=0 # Position of the memory to be updated
        self.A=[] # Archive
        self.S=[]

    def FixCR(self,CR):
        CR=np.where(CR>1,1,CR)
        CR=np.where(CR<0,0,CR)
        return CR

    def FixF(self,F,rpi):
        F=np.where(F>1,1,F)
        neg_index=np.argwhere(F<0)
        for i in neg_index:
            while(F[i]<=0): #cambiar igualdad a cero por abs
                F[i]=cauchy(self.MF[rpi[i]],0.1)
        return F

    def PBest1(self,F):
        '''
        Performs the mutation strategy current-to-pbest/1
        vi=xi+Fi(x_pbest-xi)+Fi(x_r1-x_r2)
        '''
        pbest=np.random.uniform(self.pmin,0.2,size=self.NP)
        V=[]
        for i,p in enumerate(pbest):
            length=int(p*self.NP)
            low=np.random.randint(0,self.NP-length)
            xbest=np.argmin(self.PopFitness[low:low+length])
            newPop=np.delete(range(self.NP),[i,xbest])
            #rand2 cambia si A no es vacío
            rand=np.random.choice(newPop,size=2,replace=False)
            vi=self.Pop[i]+F[i]*(self.Pop[xbest]-self.Pop[i])+F[i]*(self.Pop[rand[0]]-self.Pop[rand[1]])
            V.append(vi)
        return V

    def BinCrossover(self,V,CR):
        '''
        Binomial Crossover
        '''
        U=np.zeros((self.NP,self.D))
        randJ=np.random.randint(0,self.D,size=self.NP)
        for i in range(self.D):
            rand=np.random.rand(self.NP)
            U[:,i]=np.where(rand<=CR,V[:,i],self.Pop[:,i])
        for i in range(self.NP):
            U[i,randJ[i]]=V[i,randJ[i]]
        return U


    def FixA(self):
        "Fix the size of the archive if exceeds |Pop|"
        while(len(self.A)>self.Pop.shape[0]):
            r=np.random.randint(0,len(self.A))
            del self.A[r]

    #Reiniciar los arreglos U y V despues de usarlos

    def meanWA(self,FitnessU,CR):
        FitnessU_S=FitnessU[self.S]
        FitnessPop_S=self.PopFitness[self.S]
        diff=np.abs(FitnessU_S-FitnessPop_S)
        sum=np.sum(diff)
        w=diff/sum
        mean=np.dot(w,CR[self.S])
        return mean

    def meanWL(self,FitnessU,F):
        FitnessU_S=FitnessU[self.S]
        FitnessPop_S=self.PopFitness[self.S]
        diff=np.abs(FitnessU_S-FitnessPop_S)
        sum=np.sum(diff)
        w=diff/sum
        SF=F[self.S]
        mean=np.dot(w,np.square(SF))/np.dot(w,SF)
        return mean
        
    def solve(self):
        self.SCR=[]
        self.SF=[]
        #detalle de que evals puede pasar a max_FE si max_FE no es 
        #multiplo de NP
        while(self.evals<self.max_FE):
            rpi=np.random.randint(low=0,high=self.LP,size=self.NP)
            CRi=np.random.normal(self.MCR[rpi],0.1,size=self.NP)
            CRi=self.FixCR(CRi)
            Fi=cauchy(self.MF[rpi],0.1,size=self.NP)
            Fi=self.FixF(Fi,rpi)
            V=self.PBest1(Fi)
            U=self.BinCrossover(V,CRi)
            Fitness_trials=self.Fun(U)
            self.evals+=self.NP
            for i in range(self.NP):
                if (Fitness_trials[i]<=self.PopFitness[i]):
                    self.Pop[i]=U[i]
                    if (Fitness_trials[i]<self.PopFitness[i]):
                        self.A.append(self.Pop[i])
                        self.S.append(i)
                    self.PopFitness[i]=Fitness_trials[i]
            self.FixA()
            if self.S:
                self.MCR[self.k]=self.meanWA(Fitness_trials,CRi)
                self.MF[self.k]=self.meanWL(Fitness_trials,Fi)
                self.k=(self.k+1)%self.LP
