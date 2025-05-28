def player(prev_play, history=[]):
    if not hasattr(player, "setup"):
        player.setup = True
        player.moves = []
        player.opponent = []
        player.turn = 0
        player.beats = {"R": "P", "P": "S", "S": "R"}
        player.memory = {}

    if prev_play:
        player.opponent.append(prev_play)

    player.turn += 1

    if prev_play == '':
        first_move = "P"
        player.moves.append(first_move)
        return first_move

    seq = ["R", "R", "P", "P", "S"]
    seq_guess = player.beats[seq[player.turn % 5]]

    abbey_guess = "P"
    if len(player.moves) >= 2:
        pair = player.moves[-2] + player.moves[-1]
        if pair not in player.memory:
            player.memory[pair] = {"R": 0, "P": 0, "S": 0}
        player.memory[pair][prev_play] += 1

        if pair in player.memory:
            predicted = max(player.memory[pair], key=player.memory[pair].get)
            counter_guess = player.beats[predicted]
            abbey_guess = player.beats[counter_guess]

    mirror_read = player.beats[player.moves[-1]]
    anti_mirror = player.beats[mirror_read]

    mrugesh_guess = "S"
    if len(player.moves) >= 10:
        recent = player.moves[-10:]
        freq = {"R": 0, "P": 0, "S": 0}
        for m in recent:
            freq[m] += 1
        popular = max(freq, key=freq.get)
        prediction = player.beats[popular]
        mrugesh_guess = player.beats[prediction]

    pattern_likelihood = {
        "quincy": 0,
        "kris": 0,
        "abbey": 0,
        "mrugesh": 0
    }

    if len(player.opponent) >= 5:
        matches = 0
        for i in range(5):
            expected = seq[(player.turn - i - 1) % 5]
            if i < len(player.opponent) and player.opponent[-i-1] == expected:
                matches += 1
        pattern_likelihood["quincy"] = matches / 5

    if len(player.moves) >= 3 and len(player.opponent) >= 3:
        counter_hits = 0
        for i in range(1, min(10, len(player.moves))):
            if i < len(player.opponent):
                if player.opponent[-i] == player.beats[player.moves[-i-1]]:
                    counter_hits += 1
        pattern_likelihood["kris"] = counter_hits / max(1, min(9, len(player.moves)-1))

    if len(player.moves) >= 10 and len(player.opponent) >= 10:
        correct_preds = 0
        for i in range(2, min(10, len(player.moves)-2)):
            seq_key = player.moves[-i-2] + player.moves[-i-1]
            if seq_key in player.memory:
                likely = max(player.memory[seq_key], key=player.memory[seq_key].get)
                expected = player.beats[likely]
                if player.opponent[-i] == expected:
                    correct_preds += 1
        pattern_likelihood["abbey"] = correct_preds / max(1, min(8, len(player.moves)-2))

    if len(player.moves) >= 10 and len(player.opponent) >= 10:
        match_score = 0
        for i in range(1, min(10, len(player.opponent))):
            sample = player.moves[-i-10:-i]
            if sample:
                count = {"R": 0, "P": 0, "S": 0}
                for s in sample:
                    count[s] += 1
                dominant = max(count, key=count.get)
                if player.opponent[-i] == player.beats[dominant]:
                    match_score += 1
        pattern_likelihood["mrugesh"] = match_score / max(1, min(9, len(player.opponent)-1))

    if len(player.opponent) < 10:
        cycle = [seq_guess, abbey_guess, anti_mirror, mrugesh_guess]
        choice = cycle[len(player.opponent) % 4]
    else:
        likely_bot = max(pattern_likelihood, key=pattern_likelihood.get)
        confidence = pattern_likelihood[likely_bot]
        if likely_bot == "quincy" and confidence > 0.6:
            choice = seq_guess
        elif likely_bot == "kris" and confidence > 0.6:
            choice = anti_mirror
        elif likely_bot == "abbey" and confidence > 0.3:
            choice = abbey_guess
        elif likely_bot == "mrugesh" and confidence > 0.6:
            choice = mrugesh_guess
        else:
            recent = player.opponent[-10:]
            tally = {"R": 0, "P": 0, "S": 0}
            for m in recent:
                tally[m] += 1
            common = max(tally, key=tally.get)
            choice = player.beats[common]

    player.moves.append(choice)
    return choice
