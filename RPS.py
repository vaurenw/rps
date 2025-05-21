def player(prev_play, opponent_history=[]):
   
    if not hasattr(player, "initialized"):
        player.initialized = True
        player.my_moves = [] 
        player.opponent_moves = []  
        player.quincy_counter = 0  
        player.counter_move = {"R": "P", "P": "S", "S": "R"} 
        player.abbey_pairs = {}  

   
    if prev_play:
        player.opponent_moves.append(prev_play)

    
    player.quincy_counter += 1

   
    if prev_play == '':
        response = "P"
        player.my_moves.append(response)
        return response

    
    quincy_pattern = ["R", "R", "P", "P", "S"]
    current_quincy_pos = player.quincy_counter % 5
    next_quincy_move = quincy_pattern[current_quincy_pos]
    quincy_counter = player.counter_move[next_quincy_move]
    
   
    abbey_response = "P"
    
    
    if len(player.my_moves) >= 2:
        last_pair = player.my_moves[-2] + player.my_moves[-1]
        
        if last_pair not in player.abbey_pairs:
            player.abbey_pairs[last_pair] = {"R": 0, "P": 0, "S": 0}
            
        player.abbey_pairs[last_pair][prev_play] += 1
        
        potential_moves = {"R": 0, "P": 0, "S": 0}
        
        if len(player.my_moves) >= 2:
            last_pair = player.my_moves[-2] + player.my_moves[-1]
            
            if last_pair in player.abbey_pairs:
                most_likely = max(player.abbey_pairs[last_pair], 
                                  key=player.abbey_pairs[last_pair].get)
                
                abbey_ideal_response = player.counter_move[most_likely]
                
               
                abbey_response = player.counter_move[abbey_ideal_response]
    

    kris_expected = player.counter_move[player.my_moves[-1]]
    kris_counter = player.counter_move[kris_expected]
    
    mrugesh_response = "S" 
    if len(player.my_moves) >= 10:
        last_ten = player.my_moves[-10:]
        
        
        move_counts = {"R": 0, "P": 0, "S": 0}
        for move in last_ten:
            move_counts[move] += 1
        
        most_common = max(move_counts, key=move_counts.get)
        
        
        mrugesh_expected = player.counter_move[most_common]
        
        mrugesh_response = player.counter_move[mrugesh_expected]
    
   
    
    
    quincy_probability = 0
    if len(player.opponent_moves) >= 5:
        
        matches = 0
        for i in range(5):
            if i < len(player.opponent_moves):
                expected_idx = (player.quincy_counter - i - 1) % 5
                if player.opponent_moves[-i-1] == quincy_pattern[expected_idx]:
                    matches += 1
        
        quincy_probability = matches / 5
    
    
    kris_probability = 0
    if len(player.my_moves) >= 3 and len(player.opponent_moves) >= 3:
        matches = 0
        for i in range(1, min(10, len(player.my_moves))):
            if i < len(player.opponent_moves):
                if player.opponent_moves[-i] == player.counter_move[player.my_moves[-i-1]]:
                    matches += 1
        
        kris_probability = matches / min(9, len(player.my_moves) - 1)
    
   
    abbey_probability = 0
   
    if len(player.my_moves) >= 10 and len(player.opponent_moves) >= 10:
        matches = 0
        for i in range(2, min(10, len(player.my_moves)-2)):
            pair = player.my_moves[-i-2] + player.my_moves[-i-1]
            if pair in player.abbey_pairs:
                predicted = max(player.abbey_pairs[pair], key=player.abbey_pairs[pair].get)
                abbey_ideal_response = player.counter_move[predicted]
                if player.opponent_moves[-i] == abbey_ideal_response:
                    matches += 1
        
        abbey_probability = matches / min(8, len(player.my_moves)-2)
    
   
    mrugesh_probability = 0
    if len(player.my_moves) >= 10 and len(player.opponent_moves) >= 10:
        correct_predictions = 0
        for i in range(1, min(10, len(player.opponent_moves))):
            last_i_moves = player.my_moves[-i-10:-i]
            if last_i_moves:
                move_counts = {"R": 0, "P": 0, "S": 0}
                for move in last_i_moves:
                    move_counts[move] += 1
                
                most_common = max(move_counts, key=move_counts.get)
                if player.opponent_moves[-i] == player.counter_move[most_common]:
                    correct_predictions += 1
        
        mrugesh_probability = correct_predictions / min(9, len(player.opponent_moves)-1)
    
    
    probabilities = {
        "quincy": quincy_probability,
        "kris": kris_probability,
        "abbey": abbey_probability,
        "mrugesh": mrugesh_probability
    }
    
   
    if len(player.opponent_moves) < 10:
       
        strategies = [quincy_counter, abbey_response, kris_counter, mrugesh_response]
        response = strategies[len(player.opponent_moves) % 4]
    else:
       
        most_likely = max(probabilities, key=probabilities.get)
        
        if most_likely == "quincy" and probabilities["quincy"] > 0.6:
            response = quincy_counter
        elif most_likely == "kris" and probabilities["kris"] > 0.6:
            response = kris_counter
        elif most_likely == "abbey" and probabilities["abbey"] > 0.3:
            response = abbey_response
        elif most_likely == "mrugesh" and probabilities["mrugesh"] > 0.6:
            response = mrugesh_response
        else:
            move_counts = {"R": 0, "P": 0, "S": 0}
            for move in player.opponent_moves[-10:]:
                move_counts[move] += 1
            
            most_common = max(move_counts, key=move_counts.get)
            response = player.counter_move[most_common]
    
    
    player.my_moves.append(response)
    
    return response