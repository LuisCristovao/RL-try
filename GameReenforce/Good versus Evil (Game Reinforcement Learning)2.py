import random
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt  

human_player=False


def Visualize_Matrix(Matrix):
    fig = plt.figure()
    fig.set_size_inches(50, 20)
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(Matrix, interpolation='nearest', cmap=plt.cm.seismic) #[54:108,:]   [:14,:] [106:165,:]
    plt.colorbar()
    plt.show()

def TrainNetwork(number_of_players):   
    init = tf.global_variables_initializer()
    # Set learning parameters
    e = 0.5
    #create lists to contain total rewards and steps per episode
    jList = []
    weights = []

    with tf.Session() as sess: #Costuma ser tf.Session() em vez de tf.InteractiveSession()
        
        Qnetwork = Qnetworks(number_of_players)
        #if Restart_Training:
        # Add ops to save and restore all the variables.
        saver = tf.train.Saver()
    
        uninitialized_vars = [] #As linhas seguintes inicialização variáveis que estava dentro dos objectos 
        for var in tf.all_variables(): #criados com a class Qnetwork, que não estava a conseguir inicializar com
            try: #a função tf.global_variables nem a local_variables initializer
                sess.run(var)
            except tf.errors.FailedPreconditionError:
                uninitialized_vars.append(var)
        init_new_vars_op = tf.initialize_variables(uninitialized_vars)

        sess.run(init)
        sess.run(init_new_vars_op)
        #else: 
            #saver = tf.train.import_meta_graph('C:\\Users\\lcristovao\\Desktop\\GameReenforce\\Model_file.meta')
            #saver.restore(sess,tf.train.latest_checkpoint('./'))
            
        initial_weights = sess.run(Qnetwork.W)
        
        for games_played in range(num_games):
            print('Game Number:',games_played)
            #Reset environment and get first new observation
            real_game = Enviroment()
            Q1 = []
            for i in range (number_of_players):
                Q1.append(0)
            j = 0
            
            state_memory = []
            action_memory = []
            winner_id = []
            player_1 = 0
            player_2 = 1
                
            global weight1
            while(not(real_game.game_finished)):
                weight1=  sess.run(Qnetwork.W)
                j += 1
                if real_game.game_finished == 1:
                    break;
                    
                state_0,state_1 = real_game.getStatusArray()
                state_memory.append((state_0,player_1))                
                state_memory.append((state_1,player_2))
                #Bot vs Bot
                if(not human_player):
                
                    if np.random.rand(1) < e or games_played < pre_train_games:
                        #print('Turn')
                        p1_actions = random.randint(0,8)
                        p1_actions = [p1_actions]
                        p2_actions = random.randint(0,8)
                        p2_actions = [p2_actions]
                        action_memory.append(p1_actions[0])
                        action_memory.append(p2_actions[0])
                        allQ_1=0
                        allQ_2=0
                    else:
                        #print(state_0)
                        
                        p1_actions,allQ_1 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_0})
                        action_memory.append(p1_actions[0])
                        
                        #print(state_1)
                        
                        p2_actions,allQ_2 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_1})
                        action_memory.append(p2_actions[0])
                #Player vs Bot
                else:
                    #Player Turn
                    print('Player Status:'+str(real_game.goodStatus))
                    print('Enemy Status:'+str(real_game.evilStatus))
                    p1_actions=int(input("Move: "))
                    p1_actions=[p1_actions]
                    action_memory.append(p1_actions[0])
                    allQ_1=0
                    #Bot turn
                    if np.random.rand(1) < e or games_played < pre_train_games:
                        #print('Turn')
                        #p1_actions = random.randint(0,8)
                        #p1_actions = [p1_actions]
                        p2_actions = random.randint(0,8)
                        p2_actions = [p2_actions]
                        #action_memory.append(p1_actions[0])
                        action_memory.append(p2_actions[0])
                        #allQ_1=0
                        allQ_2=0
                    else:
                        #print(state_0)
                        
                        #p1_actions,allQ_1 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_0})
                        #action_memory.append(p1_actions[0])
                        
                        #print(state_1)
                        
                        p2_actions,allQ_2 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_1})
                        action_memory.append(p2_actions[0])
                    

                if games_played == save_logs_at:
                    
                    file.write('Good:\nAttack:'+str(real_game.goodStatus[0])+'; Defense:' + str(real_game.goodStatus[1])+'; Health:'+ str(real_game.goodStatus[2])+ '; Action:'+ str(p1_actions[0]) + '\n' + 'Q-values' + str(allQ_1) + '\n')                            
                    file.write('Evil:\nAttack:'+str(real_game.evilStatus[0])+'; Defense:' + str(real_game.evilStatus[1])+'; Health:'+ str(real_game.evilStatus[2])+ '; Action:'+ str(p2_actions[0]) + '\n'+'Q-values' + str(allQ_2) + '\n')                            
                #Actions take effect on world
                _,_ = real_game.Run(p1_actions[0],p2_actions[0])
                
                #check for winner
                if real_game.goodStatus[2] <= 0:
                    real_game.evilwins = True
                    winner_id = 1
                    real_game.game_finished = 1
                if real_game.evilStatus[2] <= 0:
                    real_game.goodwins = True
                    winner_id = 0
                    real_game.game_finished = 1
                if real_game.goodStatus[2] <= 0 and real_game.evilStatus[2] <= 0:
                    winner_id = -1
                    real_game.game_finished = 1
                        
                #decision = np.asarray(sess.run([Qnetwork.decision], feed_dict= {Qnetwork.input:state_0}))
                        
                if real_game.game_finished == 1:
                    for i in range(0,len(state_memory)-1):
                        actions,allQ_1 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_memory[i][0]})
                        actions,allQ_2 = sess.run([Qnetwork.predict, Qnetwork.Qout], feed_dict= {Qnetwork.input:state_memory[i+1][0]})
                        p1_actions[0] = action_memory[i]
                        p2_actions[0] = action_memory[i+1]
                        targetQ_1 = allQ_1
                        targetQ_2 = allQ_2
                        
                        if state_memory[i][1] == winner_id:
                            targetQ_1[0,(actions[0])] = 2
                        else:
                            targetQ_1[0,(actions[0])] = 0.3
                        if state_memory[i+1][1] == winner_id:
                            targetQ_2[0,(actions[0])] = 2
                        else:
                            targetQ_2[0,(actions[0])] = 0.3
                                
                        _,_ = sess.run([Qnetwork.updateModel, Qnetwork.W], feed_dict={Qnetwork.input:state_memory[i][0], Qnetwork.nextQ:targetQ_1})
                        _,_ = sess.run([Qnetwork.updateModel, Qnetwork.W], feed_dict={Qnetwork.input:state_memory[i+1][0], Qnetwork.nextQ:targetQ_2})
                    e = 0.1 # 1./((games_played/45) + 1)
                    break;
                    #Reduce chance of random action as we train the model.
                    

            jList.append(j)

        #saver.save(sess, 'C:\\Work\\Aprendizagem\\President_Card_Game_RL\\Model_file')
        saver.save(sess, 'C:\\Users\\lcristovao\\Desktop\\GameReenforce\\Model_file')
        final_weights = sess.run(Qnetwork.W)
        learning_per_game = 0
        for value in (initial_weights - final_weights):
            for item in value:
                learning_per_game += item * item
        learning_per_game = learning_per_game / num_games
    return jList, weights,learning_per_game  #, pesos
           
class Qnetworks():
    global weight1
    def __init__(self,num_players):
        self.input_size = 78  

        #These lines establish the feed-forward part of the network used to choose actions
        self.input = tf.placeholder(shape=[1,self.input_size],dtype=tf.float32)

        tf.set_random_seed(1234) 
        if Restart_Training:
            self.W = tf.Variable(tf.random_uniform([self.input_size,9],0.01,0.03), name = 'Variable')#meti uma shape de 18 apesar de só haver 15 hipotese, para que as actions possam ser usadas directamente para como indice no targetQ
        else:
            #graph = tf.get_default_graph()
            self.W = tf.Variable(tf.random_uniform([self.input_size,9],1,1))
            self.W = self.W * weight1
            #graph.get_tensor_by_name("Variable:"+str(0))
        
        #self.decision = tf.reshape(self.input, [self.input_size, 1]) * (self.W * (self.Mask * self.variable_mask) )  
        self.Qout = tf.matmul(self.input, self.W)  
        self.predict = tf.argmax(self.Qout,1)

        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[1,9], dtype=tf.float32) #meti uma shape de 17 apesar de só haver 15 hipotese, para que as actions possam ser usadas directamente para como indice no targetQ
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        self.trainer = tf.train.GradientDescentOptimizer(learning_rate=0.0001)
        self.updateModel = self.trainer.minimize(self.loss)

def show_results(rList):
    rewards = []
    temp = []
    counter = 0
    img_1 = plt.figure(1)
    for value in rList:
        counter += 1
        temp.append(value)
        if counter % 100 == 0:
            rewards.append(sum(temp) / float(len(temp)))
            temp = []
    plt.plot(rewards)
    img_1.show()

if __name__=="__main__":
    num_games = 2 #Convem ser multiplos de 100, por causa da show_results
    save_logs_at = num_games - 1
    pre_train_games = 0 #A função de pretrain
    human_id = 20
    
    tf.reset_default_graph() #Para o tensorflow não ir acumulando variáveis, cada vez que o main é corrido
    Restart_Training = False
    file = open('GvE_Logs.txt','w')
    number_of_players = 2 

    num_jog, weights, learning_per_game = TrainNetwork(number_of_players) 
    graph_data = []
    num_jog_data = []
    weights_data = []
    for i in range (number_of_players):
        graph_data.append(0)

   
    #show_results(graph_data[0])
    #show_results(num_jog_data)

    #Visualize_Matrix(weights)
    print('Learning per Game was:',learning_per_game)
    file.close() 


class Enviroment:
    
    def __init__(self):
        #0-Attack,1-Defense,2-Health
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
        if(self.isAttack(good_input) and self.isAttack(evil_input) or self.isDefense(good_input) and self.isDefense(evil_input)):
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
                        
                        
                        
                        
                        
                        #np.asarray([state])