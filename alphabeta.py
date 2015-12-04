def alphabeta(gs, depth, alpha, beta, maxiplayer):
    if (depth ==0): return est(gs)
    if maxiplayer:
        v= -99999999
        for state in gen_moves(gs):
            v = max(v, alphabeta(state,depth-1, alpha,beta,False))
            alpha = max(alpha, v)
            if beta <= alpha: break
        return v
    else:
        v= 99999999
        for state in gen_moves(gs):
            v = min(v,  alphabeta(state, depth-1, alpha, beta, True))
            beta= min(beta,v)
            if beta <= alpha:
                break
        return v


