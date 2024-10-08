from threading import Thread
import queue
import random
import time 
from Color import print_message

class GameEngine(Thread):
    def __init__(self, eval_queue, viz_queue,phone_action_queue,from_eval_queue,action_queue):
        Thread.__init__(self)
        
        self.eval_queue = eval_queue 
        self.viz_queue = viz_queue 
        self.phone_action_queue = phone_action_queue  # New queue for phone actions
        self.from_eval_queue = from_eval_queue
        self.action_queue = action_queue


        # Player 1 Variables
        self.hp_p1 = 100
        self.shieldHp_p1 = 0
        self.shieldCharges_p1 = 3
        self.bullets_p1 = 6
        self.bomb_p1 = 2
        self.deaths_p1 = 0

        # Player 2 Variables
        self.hp_p2 = 100
        self.shieldHp_p2 = 0
        self.shieldCharges_p2 = 3
        self.bullets_p2 = 6
        self.bomb_p2 = 2
        self.deaths_p2 = 0

        # Damage constants
        self.hp_bullet = 5
        self.hp_bomb = 5



    def get_player_state(self, player_id):
        if player_id == 1:
            return [self.hp_p1, self.shieldHp_p1, self.shieldCharges_p1, self.bullets_p1, self.bomb_p1, self.deaths_p1,
                    self.hp_p2, self.shieldHp_p2, self.shieldCharges_p2, self.bullets_p2, self.bomb_p2, self.deaths_p2]
        elif player_id == 2:
            return [self.hp_p2, self.shieldHp_p2, self.shieldCharges_p2, self.bullets_p2, self.bomb_p2, self.deaths_p2,
                    self.hp_p1, self.shieldHp_p1, self.shieldCharges_p1, self.bullets_p1, self.bomb_p1, self.deaths_p1]
        else:
            print("Game Engine: Invalid player_id")
            return []

    def shoot(self, player_id):
        if player_id == 1 and self.bullets_p1 > 0:
            self.bullets_p1 -= 1
            self.update_both_players_game_state()
            return True
        elif player_id == 2 and self.bullets_p2 > 0:
            self.bullets_p2 -= 1
            self.update_both_players_game_state()
            return True
        return False

    def reload(self, player_id):
        if player_id == 1:
            if self.bullets_p1 == 0:  # Only reload if bullets are empty
                self.bullets_p1 = 6
                self.update_both_players_game_state()
                return True
            else:
                return False  # Cannot reload if bullets are not empty
        elif player_id == 2:
            if self.bullets_p2 == 0:  # Only reload if bullets are empty
                self.bullets_p2 = 6
                self.update_both_players_game_state()
                return True
            else:
                return False  # Cannot reload if bullets are not empty
        return False


    def take_ai_damage(self, player_id):
        if player_id == 1:
            if self.shieldHp_p1 > 0:
                self.shieldHp_p1 = max(0, self.shieldHp_p1 - 10)
            else:
                self.hp_p1 = max(0, self.hp_p1 - 10)
            if self.hp_p1 <= 0:
                self.respawn(player_id)
        elif player_id == 2:
            if self.shieldHp_p2 > 0:
                self.shieldHp_p2 = max(0, self.shieldHp_p2 - 10)
            else:
                self.hp_p2 = max(0, self.hp_p2 - 10)
            if self.hp_p2 <= 0:
                self.respawn(player_id)
        self.update_both_players_game_state()


    # Right now this function does nth
    def update_both_players_game_state(self):
        self.log_game_state()

    def log_game_state(self):
        game_state_info = (
            "[Game State Log] Player 1 Stats:\n"
            f"HP: {self.hp_p1}, Shield HP: {self.shieldHp_p1}, Shield Charges: {self.shieldCharges_p1}, Bullets: {self.bullets_p1}, Bombs: {self.bomb_p1}, Deaths: {self.deaths_p1}\n"
            "[Game State Log] Player 2 Stats:\n"
            f"HP: {self.hp_p2}, Shield HP: {self.shieldHp_p2}, Shield Charges: {self.shieldCharges_p2}, Bullets: {self.bullets_p2}, Bombs: {self.bomb_p2}, Deaths: {self.deaths_p2}\n"
        )
        print(game_state_info)

    def respawn(self, player_id):
        if player_id == 1:
            self.hp_p1 = 100
            self.bomb_p1 = 2
            self.shieldCharges_p1 = 3
            self.shieldHp_p1 = 0
            self.bullets_p1 = 6
            self.deaths_p1 += 1
        elif player_id == 2:
            self.hp_p2 = 100
            self.bomb_p2 = 2
            self.shieldCharges_p2 = 3
            self.shieldHp_p2 = 0
            self.bullets_p2 = 6
            self.deaths_p2 += 1

    def take_bullet_damage(self, player_id):
        if player_id == 1:
            if self.shieldHp_p1 > 0:
                self.shieldHp_p1 = max(0, self.shieldHp_p1 - self.hp_bullet)
            else:
                self.hp_p1 = max(0, self.hp_p1 - self.hp_bullet)

            if self.hp_p1 <= 0:
                self.respawn(player_id)
            self.update_both_players_game_state()
            return True
        elif player_id == 2:
            if self.shieldHp_p2 > 0:
                self.shieldHp_p2 = max(0, self.shieldHp_p2 - self.hp_bullet)
            else:
                self.hp_p2 = max(0, self.hp_p2 - self.hp_bullet)

            if self.hp_p2 <= 0:
                self.respawn(player_id)
            self.update_both_players_game_state()
            return True
        return False

    def take_rain_bomb_damage(self, player_id):
        if player_id == 1:
            if self.shieldHp_p1 > 0:
                self.shieldHp_p1 = max(0, self.shieldHp_p1 - self.hp_bomb)
            else:
                self.hp_p1 = max(0, self.hp_p1 - self.hp_bomb)

            if self.hp_p1 <= 0:
                self.respawn(player_id)
            self.update_both_players_game_state()
            return True
        elif player_id == 2:
            if self.shieldHp_p2 > 0:
                self.shieldHp_p2 = max(0, self.shieldHp_p2 - self.hp_bomb)
            else:
                self.hp_p2 = max(0, self.hp_p2 - self.hp_bomb)

            if self.hp_p2 <= 0:
                self.respawn(player_id)
            self.update_both_players_game_state()
            return True
        return False

    def charge_shield(self, player_id):
        if player_id == 1 and self.shieldCharges_p1 > 0:
            self.shieldHp_p1 = 30
            self.shieldCharges_p1 -= 1
            self.update_both_players_game_state()
            return True
        elif player_id == 2 and self.shieldCharges_p2 > 0:
            self.shieldHp_p2 = 30
            self.shieldCharges_p2 -= 1
            self.update_both_players_game_state()
            return True
        return False




    def random_game_state(self):
        return {
            'player': 1,
            'hp': random.randint(10, 90),
            'bullets': random.randint(0, 6),
            'bombs': random.randint(0, 2),
            'shield_hp': random.randint(0, 30),
            'deaths': random.randint(0, 3),
            'shields': random.randint(0, 3)
        }


    def process_phone_action(self, action):
        print_message('Game Engine', f"Processing phone action: {action}")

        # Check if it's an FOV response (expected format: 'fov:<player_id>:<opponent_player_id>:<hit_or_miss>:<is_bomb>')
        # Process FOV response itself place something in the viz queue
        if action.startswith("fov:"):
            self.process_fov_response(action)
            return
        #else:
            #self.eval_queue.put()
        

        # If not an FOV response, proceed with regular action processing
        action_p1 = "none"  # Default action for player 1
        action_p2 = "none"  # Default action for player 2

        # Validate and split the action string (e.g., "shoot:1", "reload:2")
        if ":" in action:
            parts = action.split(":")
            if len(parts) != 2:
                print_message('Game Engine', f"Invalid action format: {action}")
                return None

            action_type, player_id = parts
            player_id = int(player_id)

            if action_type == "shoot":
                success = self.shoot(player_id)
                if success:
                    if player_id == 1:
                        action_p1 = "shoot"
                    else:
                        action_p2 = "shoot"
                print_message('Game Engine', f"Player {player_id} attempted to shoot: {'Success' if success else 'Failed'}")

            elif action_type == "reload":
                success = self.reload(player_id)
                if success:
                    if player_id == 1:
                        action_p1 = "reload"
                    else:
                        action_p2 = "reload"
                print_message('Game Engine', f"Player {player_id} attempted to reload: {'Success' if success else 'Failed'}")

            elif action_type in ["basket", "soccer", "volley", "bowl", "bomb"]:
                # Handle the AI actions for sports or bomb
                print_message('Game Engine', f"Player {player_id} performed AI action: {action_type}")
                if player_id == 1:
                    action_p1 = action_type
                else:
                    action_p2 = action_type
                print_message('Game Engine', f"Player {player_id} performed {action_type}")

            elif action_type == "ai_damage":
                self.take_ai_damage(player_id)
                if player_id == 1:
                    action_p1 = "ai_damage"
                else:
                    action_p2 = "ai_damage"
                print_message('Game Engine', f"Player {player_id} took AI damage")

            elif action_type == "bullet_damage":
                success = self.take_bullet_damage(player_id)
                if success:
                    if player_id == 1:
                        action_p1 = "bullet_damage"
                    else:
                        action_p2 = "bullet_damage"
                print_message('Game Engine', f"Player {player_id} took bullet damage: {'Success' if success else 'Failed'}")

            elif action_type == "rain_bomb_damage":
                success = self.take_rain_bomb_damage(player_id)
                if success:
                    if player_id == 1:
                        action_p1 = "rain_bomb_damage"
                    else:
                        action_p2 = "rain_bomb_damage"
                print_message('Game Engine', f"Player {player_id} took rain bomb damage: {'Success' if success else 'Failed'}")

            elif action_type == "charge_shield":
                success = self.charge_shield(player_id)
                if success:
                    if player_id == 1:
                        action_p1 = "charge_shield"
                    else:
                        action_p2 = "charge_shield"
                print_message('Game Engine', f"Player {player_id} charged their shield: {'Success' if success else 'Failed'}")

            else:
                print_message('Game Engine', f"Unknown action type: {action_type}")
        else:
            print_message('Game Engine', "Invalid action format received from phone")

        # After processing the action, update the game state for the visualizer with actions included
        viz_format = (
            f"p1_hp:{self.hp_p1},p1_bombs:{self.bomb_p1},p1_shieldCharges:{self.shieldCharges_p1},"
            f"p1_shieldHp:{self.shieldHp_p1},p1_bullets:{self.bullets_p1},p1_deaths:{self.deaths_p1},"
            f"p2_hp:{self.hp_p2},p2_bombs:{self.bomb_p2},p2_shieldCharges:{self.shieldCharges_p2},"
            f"p2_shieldHp:{self.shieldHp_p2},p2_bullets:{self.bullets_p2},p2_deaths:{self.deaths_p2},"
            f"p1_action:{action_p1},p2_action:{action_p2}"
        )

        return viz_format


    

    # def format_viz(self, player_id):
    #     # No need to flip based on player_id, always send both Player 1 and Player 2 states
    #     action_p1 = ""
    #     action_p2 = ""

    #     game_state = {
    #         'p1_hp': self.hp_p1,
    #         'p1_bombs': self.bomb_p1,
    #         'p1_shieldCharges': self.shieldCharges_p1,
    #         'p1_shieldHp': self.shieldHp_p1,
    #         'p1_bullets': self.bullets_p1,
    #         'p1_deaths': self.deaths_p1,
    #         'p2_hp': self.hp_p2,
    #         'p2_bombs': self.bomb_p2,
    #         'p2_shieldCharges': self.shieldCharges_p2,
    #         'p2_shieldHp': self.shieldHp_p2,
    #         'p2_bullets': self.bullets_p2,
    #         'p2_deaths': self.deaths_p2
    #     }

    #     # Format the string with explicit player 1 and player 2 labels
    #     viz_format = (
    #         f"p1_hp:{game_state['p1_hp']},p1_bombs:{game_state['p1_bombs']},p1_shieldCharges:{game_state['p1_shieldCharges']},"
    #         f"p1_shieldHp:{game_state['p1_shieldHp']},p1_bullets:{game_state['p1_bullets']},p1_deaths:{game_state['p1_deaths']},"
    #         f"p2_hp:{game_state['p2_hp']},p2_bombs:{game_state['p2_bombs']},p2_shieldCharges:{game_state['p2_shieldCharges']},"
    #         f"p2_shieldHp:{game_state['p2_shieldHp']},p2_bullets:{game_state['p2_bullets']},p2_deaths:{game_state['p2_deaths']},"
    #         f"p1_action:{action_p1},p2_action:{action_p2}"
    #     )
        
    #     return viz_format


    def process_fov_response(self, response):
        print_message('Game Engine', f"Processing FOV response: {response}")

        # Parse response in the format: "fov:<player_id>:<opponent_player_id>:<hit_or_miss>:<is_bomb>"
        if ":" in response:
            _, player_id, opponent_player_id, hit_or_miss, is_bomb = response.split(":")
            player_id = int(player_id)  # The player who performed the action
            opponent_player_id = int(opponent_player_id)  # The opponent who will take damage
            hit_or_miss = int(hit_or_miss)  # 1 for hit, 0 for miss
            is_bomb = int(is_bomb)  # 1 if it's a bomb, 0 if it's another AI move

            if hit_or_miss == 1:
                print_message('Game Engine', f"Player {player_id} hit Player {opponent_player_id} with their action")

                # Apply bomb damage or regular AI damage to the opponent
                if is_bomb == 1:
                    print_message('Game Engine', f"Player {opponent_player_id} takes bomb damage")
                    self.take_rain_bomb_damage(opponent_player_id)  # Apply bomb damage to the opponent
                else:
                    print_message('Game Engine', f"Player {opponent_player_id} takes AI damage")
                    self.take_ai_damage(opponent_player_id)  # Apply regular AI damage to the opponent
            else:
                print_message('Game Engine', f"Player {player_id}'s action missed Player {opponent_player_id}")

        # Update game state after processing FOV
        self.update_both_players_game_state()

        # Note, the actions are always none here bcs we already did it, and are just updating the game state here
        action_p1 = "none"
        action_p2 = "none"

        action = self.action_queue.get()

        eval_server_format = {
                'player_id': 1,
                'action': action,
                'game_state': {
                    'p1': {
                        'hp': self.hp_p1,
                        'bullets': self.bullets_p1,
                        'bombs': self.bomb_p1,
                        'shield_hp': self.shieldHp_p1,
                        'deaths': self.deaths_p1,
                        'shields': self.shieldCharges_p1
                    },
                    'p2': {  
                        'hp': self.hp_p2,
                        'bullets': self.bullets_p2,
                        'bombs': self.bomb_p2,
                        'shield_hp': self.shieldHp_p2,
                        'deaths': self.deaths_p2,
                        'shields': self.shieldCharges_p2
                    }
                }
            }



        self.eval_queue.put(eval_server_format)
        # TODO: Add checking with Eval_server code


        






    def run(self):
        while True:
        
            #print("Reached Game Engine Main Loop")
            #print("Checking if phone action queue is empty")
            
            # Handle phone action if it's not empty
            #if not self.phone_action_queue.empty():
            phone_action = self.phone_action_queue.get()
                
                #print_message('Game Engine', f"Received action '{phone_action}' from phone")
            viz_format = self.process_phone_action(phone_action)
            self.viz_queue.put(viz_format)
            #waiting for phone to reply 
            # TODO we need to think about what happens if MQTT disconnects or anything happens such that phone cannot reply, need to timeout the queue.get() and do what? hardcode a value? reconnect MQTT and? 
            phone_action = self.phone_action_queue.get()
            temp_viz_format = self.process_phone_action(phone_action) # viz format returned not used as need eval server response to send updated info to viz 
            time.sleep(5)
            updated_game_state = self.from_eval_queue.get()
            print_message('Game Engine',f"Received {updated_game_state} from eval server")

                #TODO make new game state with response from eval server and then put in viz queue 
            ''' 
            maybe a new function to update_game_state() 
            viz_format = update_game_state(updated_game_state)

            print_message('Game Engine', f"Sending updated game state to visualizer: {viz_format}")
            self.viz_queue.put(viz_format)  # Send updated state to the visualizer AFTER eval server replies 
   
            '''
                
                
    # # Before
    # def run(self):
    #     while True:
        
    #         #print("Reached Game Engine Main Loop")
    #         #print("Checking if phone action queue is empty")
            
    #         # Handle phone action if it's not empty
    #         if not self.phone_action_queue.empty():
    #             phone_action = self.phone_action_queue.get()
                
    #         #print_message('Game Engine', f"Received action '{phone_action}' from phone")
    #         viz_format = self.process_phone_action(phone_action)
    #         self.viz_queue.put(viz_format)
    #         #waiting for phone to reply 
    #         # TODO we need to think about what happens if MQTT disconnects or anything happens such that phone cannot reply, need to timeout the queue.get() and do what? hardcode a value? reconnect MQTT and? 
    #         phone_action = self.phone_action_queue.get()
    #         temp_viz_format = self.process_phone_action(phone_action) # viz format returned not used as need eval server response to send updated info to viz 
    #         updated_game_state = self.from_eval_queue.get()
    #         print_message('Game Engine',f"Received {updated_game_state} from eval server")

    #         #TODO make new game state with response from eval server and then put in viz queue 
    #         ''' 
    #         maybe a new function to update_game_state() 
    #         viz_format = update_game_state(updated_game_state)

    #         print_message('Game Engine', f"Sending updated game state to visualizer: {viz_format}")
    #         self.viz_queue.put(viz_format)  # Send updated state to the visualizer AFTER eval server replies 
   
    #         '''
        

