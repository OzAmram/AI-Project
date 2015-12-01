def ab_max((v1, mov1), (v2, mov2)):
    if (v1 <= v2): return (v2, mov2)
    else: return (v1, mov1)

def ab_min((v1, mov1), (v2, mov2)):
    if (v1 <= v2): return (v1, mov1)
    else: return (v2, mov2)


def alphabeta(gs,depth, alpha, beta, maxiplayer):
    if (depth ==0): return est(gs)
    if maxiplayer:
        v=(null_move, -99999999)
        for move,state in gen_moves(gs):
            v = ab_max(v, (move, alphabeta(state,depth-1, alpha,beta,False)[1]))
            alpha = max(alpha, v[1])
            if beta <= alpha: break
        return v
    else:
        v=(null_move, 99999999)
        for move,state in gen_moves(gs):
            v = ab_min(v, (move, alphabeta(state, depth-1, alpha, beta, True)[1]))
            beta= min(beta,v[1])
            if beta <= alpha:
                break
        return v


