from threading import Thread
from queue import Queue
import random
from Threads.max_attempt_integrate_attempt.AIPredictor import predict_model
from Color import print_message

#ACTIONS = ["shoot", "shield", "bomb", "reload", "basket", "soccer", "volley", "bowl"] 
#TODO Figure out eval server for non AI actions 


#format to send out = action + ":player_id" 

ACTIONS = ["basket", "soccer", "volley", "bowl", "bomb", "shield", "reload", "logout"]

class AI(Thread):
    def __init__(self,IMU_queue,phone_action_queue,fire_queue):
        Thread.__init__(self)
        self.IMU_queue = IMU_queue
        self.fire_queue = fire_queue  
        self.phone_action_queue = phone_action_queue
    
    #def detectAction(self, message):
    #    if LOWERTHRESHOLD <= message['gyro'][0] <= UPPERTHRESHOLD and LOWERTHRESHOLD <= message['gyro'][1] <= UPPERTHRESHOLD and LOWERTHRESHOLD <= message['gyro'][2] <= UPPERTHRESHOLD:
    #        return True
    #    return False
    
    def sendData(self, messages):
       return predict_model.get_action(messages)
       
    def run(self):
      while True:
        message_IMU = self.IMU_queue.get() #get from IMU
        message_Shoot = self.fire_queue.get() #get from Shoot_queue
        if message_Shoot['isFire']: #only care abt is fired and not is hit
           action = 'gun'
           number = 1
           combined_action = f"{{'playerID': '{number}', 'action': {action}}}"
           self.phone_action_queue.put(combined_action) 
        
        messages_IMU = []
        while len(messages_IMU) < 20:
            messages_IMU.append(message_IMU)
            if ~message_Shoot['isFire']:
                action = ACTIONS[self.sendData(messages_IMU) - 1]
                number = 1 #Check again for this part
                combined_action = f"{{'playerID': '{number}', 'action': {action}}}"
                self.phone_action_queue.put(combined_action)
                message_Shoot['isFire'] = False


    
    