def council_vote(scores: dict):
    return max(scores.items(), key=lambda x: x[1])[0]
