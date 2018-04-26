# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:29:32 2018

@author: lcristovao
"""
import numpy as np


class Enviroment:
    
    def __init__(self):
        #0-Attack,1-Defense,2-Health
        self.prev_goodStatus=[100,100,100]
        self.prev_evilStatus=[100,100,100]
        self.goodStatus=[100,100,100]
        self.evilStatus=[100,100,100]
        self.goodWins=False
        self.eviWins=False
        self.game_finished=0
        self.possibleStatus={
                             100:np.array([1,0,0,0,0,0,0,0,0,0,0,0,0]),
                             90:np.array([0,1,0,0,0,0,0,0,0,0,0,0,0]),
                             80:np.array([0,0,1,0,0,0,0,0,0,0,0,0,0]),
                             70:np.array([0,0,0,1,0,0,0,0,0,0,0,0,0]),
                             60:np.array([0,0,0,0,1,0,0,0,0,0,0,0,0]),
                             50:np.array([0,0,0,0,0,1,0,0,0,0,0,0,0]),
                             40:np.array([0,0,0,0,0,0,1,0,0,0,0,0,0]),
                             30:np.array([0,0,0,0,0,0,0,1,0,0,0,0,0]),
                             20:np.array([0,0,0,0,0,0,0,0,1,0,0,0,0]),
                             10:np.array([0,0,0,0,0,0,0,0,0,1,0,0,0]),
                             0:np.array([0,0,0,0,0,0,0,0,0,0,1,0,0])
                             
                             }
        self.code_to_bet={
                           0:10,
                           1:20,
                           2:30,
                           3:10,
                           4:20,
                           5:30,
                           6:20,
                           7:20,
                           8:20
                
                         }
        
        
        
    #@staticmethod    
    def individualStatusToArray(self,number):
        if(number>=0 and number<=100):
            return self.possibleStatus[number]
        else:
            if(number<0):
                return np.array([0,0,0,0,0,0,0,0,0,0,0,0,1])
            if(number>100):
                return np.array([0,0,0,0,0,0,0,0,0,0,0,1,0])
                
    
    def StatusToArray(self,good):
        out=[]
        if(good):
            for i in range(len(self.goodStatus)):    
                out.append(self.individualStatusToArray(self.goodStatus[i]))
        else:
             for i in range(len(self.evilStatus)):    
                out.append(self.individualStatusToArray(self.evilStatus[i]))
        
        return np.array(out).reshape(1,39)
    @staticmethod 
    def isAttack(number):    
        if(number>=0 and number<=2):
            return True
        else:
            return False
    
    @staticmethod 
    def isDefense(number):    
        if(number>=3 and number<=5):
            return True
        else:
            return False
    
    @staticmethod 
    def isPowerUp(number):    
        if(number>=6 and number<=8):
            return True
        else:
            return False
    
    
    def codeToBet(self,number):    
        return self.code_to_bet[number]
    
    
    def consumeResources(self,number,good):
        #consume good resources
        if good:
            if self.isAttack(number):
                #consume attack resources
                self.goodStatus[0]-=self.codeToBet(number)
                if(self.goodStatus[0]<0):
                    #take Damage
                    self.goodStatus[2]+=self.goodStatus[0]
            if self.isDefense(number):
                #consume defense resources
                self.goodStatus[1]-=self.codeToBet(number)
                if self.goodStatus[1]<0:
                    #take Damage
                    self.goodStatus[2]+=self.goodStatus[1]
            if self.isPowerUp(number):
                
                if(number==6):
                    self.goodStatus[0]+=self.codeToBet(number)
                if(number==7):
                    self.goodStatus[1]+=self.codeToBet(number)
                if(number==8):
                    self.goodStatus[2]+=self.codeToBet(number)    
        #consume evil resources    
        else:
            if self.isAttack(number):
                #consume attack resources
                self.evilStatus[0]-=self.codeToBet(number)
                if(self.evilStatus[0]<0):
                    #take Damage
                    self.evilStatus[2]+=self.evilStatus[0]
            if self.isDefense(number):
                #consume defense resources
                self.evilStatus[1]-=self.codeToBet(number)
                if self.evilStatus[1]<0:
                    #take Damage
                    self.evilStatus[2]+=self.evilStatus[1]
            if self.isPowerUp(number):
                if(number==6):
                    self.evilStatus[0]+=self.codeToBet(number)
                if(number==7):
                    self.evilStatus[1]+=self.codeToBet(number)
                if(number==8):
                    self.evilStatus[2]+=self.codeToBet(number)    
            
    def getStatusArray(self):
        out=[]
        final_array=np.array([])
        #good status
        final_array=self.StatusToArray(True)
        final_array=np.concatenate((final_array,self.StatusToArray(False)),axis=0)
        out.append(final_array.reshape(1,78))
        #reverse operation
        final_array=self.StatusToArray(False)
        final_array=np.concatenate((final_array,self.StatusToArray(True)),axis=0)
        out.append(final_array.reshape(1,78))
        return out           
        
    
    def Run(self,good_input,evil_input):
        #if both attack or defense
        if(self.isAttack(good_input) and self.isAttack(evil_input) ):
            #if both did choose same option then we need to see who gave the highest bet
            #consume resources is needed always
            #consume good resources
            self.consumeResources(good_input,True)
            #consume evil resources
            self.consumeResources(evil_input,False)
            #if options are from different lvs
            if(good_input!=evil_input):
                #need to do damage to the one with lowest bet
                #if it entered in this if it means they both choose attack or defense
                #Calculate the difference
                good_value= self.codeToBet(good_input)
                evil_value= self.codeToBet(evil_input)
                difference=abs(good_value-evil_value)
                
                if(good_input>evil_input):
                    #evil takes damage
                    self.evilStatus[2]-=difference
                else:
                    #good takes damage
                    self.goodStatus[2]-=difference
             #if both choose same level of same option then they just consume resources       
        else: 
            #if both defense
            if self.isDefense(good_input) and self.isDefense(evil_input):
                #consume good resources
                self.consumeResources(good_input,True)
                #consume evil resources
                self.consumeResources(evil_input,False)
            else:
                #if both choose powerUp!
                if(self.isPowerUp(good_input) and self.isPowerUp(evil_input)):
                    #just consume resources in this case both receive resources
                    #consume good resources
                    self.consumeResources(good_input,True)
                    #consume evil resources
                    self.consumeResources(evil_input,False)
                #Here Players Choose Different Options AD|DA|PA|AP|
                else:
                    #good-A and evil-D 
                    if(self.isAttack(good_input) and self.isDefense(evil_input) or self.isDefense(good_input) and self.isAttack(evil_input) ):
                        #consume good resources
                        self.consumeResources(good_input,True)
                        #consume evil resources
                        self.consumeResources(evil_input,False)
                        #need to do damage to the one with lowest bet
                        #if it entered in this if it means they both choose attack or defense
                        #Calculate the difference
                        good_bet= self.codeToBet(good_input)
                        evil_bet= self.codeToBet(evil_input)
                        difference=abs(good_bet-evil_bet)
                        
                        #same lv of attack or defense
                        if difference==0:
                            #if good-A and evil-D
                            #evil wins
                            if self.isAttack(good_input) and self.isDefense(evil_input):
                                self.goodStatus[2]-=good_bet
                            #if good-D and evil-A
                            #good wins
                            if self.isDefense(good_input) and self.isAttack(evil_input):
                                self.evilStatus[2]-=evil_bet
                        #difference!=0
                        else:
                            #see who did the highest bet
                            if good_bet>evil_bet:
                                self.evilStatus[2]-=difference
                            else:
                                self.goodStatus[2]-=difference
                                
                    #if one of them did powerUp options AP|PA|PD|DP
                    else:
                        #if AP
                        if(self.isAttack(good_input) and self.isPowerUp(evil_input) ):
                            #good consume resources
                            self.consumeResources(good_input,True)
                            #evil takes damage
                            self.evilStatus[2]-=self.codeToBet(good_input)
                        #if PA
                        if(self.isPowerUp(good_input) and self.isAttack(evil_input)):
                            #evil consume resources
                            self.consumeResources(evil_input,False)
                            #good takes damage
                            self.goodStatus[2]-=self.codeToBet(evil_input)
                        #if PD|DP
                        #if PD
                        if(self.isPowerUp(good_input) and self.isDefense(evil_input)  or self.isPowerUp(evil_input) and self.isDefense(good_input) ):
                            #both consume resources
                            #good consume resources
                            self.consumeResources(good_input,True)
                            #evil consume resources
                            self.consumeResources(evil_input,False)
        #now for the last things
        
        return self.getStatusArray()            

#Main----------------------------
print(__name__)                
                
'''                
            
env=Enviroment()
#env.goodStatus=[90,10,100]
#env.evilStatus=[30,40,80]
#print(env.goodStatus,env.evilStatus)
#print('D3 PH')
#result=env.Run(5,8)
#print(env.goodStatus,env.evilStatus)
#print('...')
#print(result)  



print('both Attack same lv 1')
result=env.Run(0,0)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)
print('A3 D2')
#result=env.Run(2,3)
print(env.goodStatus,env.evilStatus)
print('...')
print(result) 
print('A1 D1')
#result=env.Run(0,3)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)
print('PA A3')
#result=env.Run(6,2)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)   
print('PH PH')
#result=env.Run(8,8)
print(env.goodStatus,env.evilStatus)
print('...')
print(result) 
print('PA D2')
result=env.Run(6,4)
print(env.goodStatus,env.evilStatus)
print('...')
print(result) 
print('PA D2')
result=env.Run(6,4)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)   
print('D3 A3')
result=env.Run(5,2)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)  
print('PH PA')
result=env.Run(8,6)
print(env.goodStatus,env.evilStatus)
print('...')
print(result) 
print('D3 A2')
result=env.Run(5,1)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)   
print('D3 PH')
result=env.Run(5,8)
print(env.goodStatus,env.evilStatus)
print('...')
#print(result)    
print('D3 PH')
result=env.Run(5,8)
print(env.goodStatus,env.evilStatus)
print('...')
print(result)       
'''