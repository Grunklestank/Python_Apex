from    random                  import  choice
from    numpy                   import  mean, std
from    time                    import  time
import  plotly.graph_objects    as      go


CONFIG      = {
    "EVAL": {
        "target":       3000,
        "drawdown":     2500,
        "cost_win":     -34,
        "cost_lose":    -34
    },
    "PA": {
        "target":       3240,
        "drawdown":     2500,
        "cost_win":     2000 - 85,
        "cost_lose":    -85
    },
    "PA_SMALL": {
        "target":       200,
        "drawdown":     800,
        "cost_win":     2000 - 85,
        "cost_lose":    -85
    }
}
EVAL_CONTRACTS   = 10
PA_CONTRACTS   = 6
PA_SMALL_CONTRACTS   = 6
TICK_VAL    = 5
SPREAD      = 2
COMMISSIONS = 4.64
EVAL_COSTS       = (SPREAD * TICK_VAL + COMMISSIONS) * EVAL_CONTRACTS
PA_COSTS       = (SPREAD * TICK_VAL + COMMISSIONS) * PA_CONTRACTS
PA_SMALL_COSTS       = (SPREAD * TICK_VAL + COMMISSIONS) * PA_CONTRACTS
POPULATION  = [ 1, -1 ]
EVAL_TP_TICKS    = 60
EVAL_SL_TICKS    = 50
PA_TP_TICKS    = 28
PA_SL_TICKS    = 83
PA_SMALL_TP_TICKS    = 7
PA_SMALL_SL_TICKS    = 7
EVAL_TP_DOLLARS  = EVAL_TP_TICKS * EVAL_CONTRACTS * TICK_VAL
EVAL_SL_DOLLARS  = EVAL_SL_TICKS * EVAL_CONTRACTS * TICK_VAL
PA_TP_DOLLARS  = PA_TP_TICKS * PA_CONTRACTS * TICK_VAL
PA_SL_DOLLARS  = PA_SL_TICKS * PA_CONTRACTS * TICK_VAL
PA_SMALL_TP_DOLLARS  = PA_SMALL_TP_TICKS * PA_SMALL_CONTRACTS * TICK_VAL
PA_SMALL_SL_DOLLARS  = PA_SMALL_SL_TICKS * PA_SMALL_CONTRACTS * TICK_VAL
TRIALS      = 10_000


def runEVAL(mode: str):

    results     = []
    cost        = []
    #fig         = go.Figure()

    for i in range(TRIALS):

        curve               = []
        dd                  = []
        equity              = 0
        tp                  = equity + EVAL_TP_DOLLARS
        sl                  = equity - EVAL_SL_DOLLARS
        target              = CONFIG[mode]["target"]
        drawdown            = CONFIG[mode]["drawdown"]
        trailing_drawdown   = -drawdown

        while(True):

            pnl_tick            =   choice(POPULATION) * EVAL_CONTRACTS * TICK_VAL
            equity              +=  pnl_tick
            trailing_drawdown   =   max(trailing_drawdown, -drawdown + equity)

            if equity >= tp or equity <= sl:

                equity -= EVAL_COSTS
                tp      = equity + EVAL_TP_DOLLARS
                sl      = equity - EVAL_SL_DOLLARS

            curve.append(equity)
            dd.append(trailing_drawdown)

            if (equity >= target):

                results.append(1)
                cost.append(CONFIG[mode]["cost_win"])
                
                break

            elif (equity <= trailing_drawdown):

                results.append(0)
                cost.append(CONFIG[mode]["cost_lose"])

                break

    pass_rate   = mean(results)
    ev          = mean(cost)

    print(f"{mode + ' pass rate':30}{pass_rate:<10.2f}")
    print(f"{mode + ' EV':30}{ev:<10.2f}")

    return pass_rate, ev
        
def runPA(mode: str):

    results     = []
    cost        = []
    #fig         = go.Figure()

    for i in range(TRIALS):

        curve               = []
        dd                  = []
        equity              = 0
        tp                  = equity + PA_TP_DOLLARS
        sl                  = equity - PA_SL_DOLLARS
        target              = CONFIG[mode]["target"]
        drawdown            = CONFIG[mode]["drawdown"]
        trailing_drawdown   = -drawdown

        while(True):

            pnl_tick            =   choice(POPULATION) * PA_CONTRACTS * TICK_VAL
            equity              +=  pnl_tick
            trailing_drawdown   =   max(trailing_drawdown, -drawdown + equity)

            if equity >= tp or equity <= sl:

                equity -= PA_COSTS
                tp      = equity + PA_TP_DOLLARS
                sl      = equity - PA_SL_DOLLARS

            curve.append(equity)
            dd.append(trailing_drawdown)

            if (equity >= target):

                results.append(1)
                cost.append(CONFIG[mode]["cost_win"])
                
                break

            elif (equity <= trailing_drawdown):

                results.append(0)
                cost.append(CONFIG[mode]["cost_lose"])

                break

    pass_rate   = mean(results)
    ev          = mean(cost)

    print(f"{mode + ' pass rate':30}{pass_rate:<10.2f}")
    print(f"{mode + ' EV':30}{ev:<10.2f}")

    return pass_rate, ev

def runPA_SMALL(mode: str):

    results     = []
    cost        = []
    #fig         = go.Figure()

    for i in range(TRIALS):

        curve               = []
        dd                  = []
        equity              = 0
        tp                  = equity + PA_SMALL_TP_DOLLARS
        sl                  = equity - PA_SMALL_SL_DOLLARS
        target              = CONFIG[mode]["target"]
        drawdown            = CONFIG[mode]["drawdown"]
        trailing_drawdown   = -drawdown

        while(True):

            pnl_tick            =   choice(POPULATION) * PA_SMALL_CONTRACTS * TICK_VAL
            equity              +=  pnl_tick
            trailing_drawdown   =   max(trailing_drawdown, -drawdown + equity)

            if equity >= tp or equity <= sl:

                equity -= PA_SMALL_COSTS
                tp      = equity + PA_SMALL_TP_DOLLARS
                sl      = equity - PA_SMALL_SL_DOLLARS

            curve.append(equity)
            dd.append(trailing_drawdown)

            if (equity >= target):

                results.append(1)
                cost.append(CONFIG[mode]["cost_win"])
                
                break

            elif (equity <= trailing_drawdown):

                results.append(0)
                cost.append(CONFIG[mode]["cost_lose"])

                break

    pass_rate   = mean(results)
    ev          = mean(cost)

    print(f"{mode + ' pass rate':30}{pass_rate:<10.2f}")
    print(f"{mode + ' EV':30}{ev:<10.2f}")

    return pass_rate, ev

if __name__ == "__main__":

    t0 = time()

    print("EVALs")
    print(f"{'contracts:':30}{EVAL_CONTRACTS:<10}")
    print(f"{'tick val ($):':30}{TICK_VAL:<10.2f}")
    print(f"{'spread (ticks):':30}{SPREAD:<10.2f}")
    print(f"{'commissions ($):':30}{COMMISSIONS:<10.2f}")
    print(f"{'trade cost ($):':30}{EVAL_COSTS:<10.2f}")
    print(f"{'tp (ticks):':30}{EVAL_TP_TICKS:<10.2f}")
    print(f"{'tp ($):':30}{EVAL_TP_DOLLARS:<10.2f}")
    print(f"{'sl (ticks):':30}{EVAL_SL_TICKS:<10.2f}")
    print(f"{'sl ($):':30}{EVAL_SL_DOLLARS:<10.2f}")
    print(f"{'trials:':30}{TRIALS:<10}\n")

    print("PA BIGS")
    print(f"{'contracts:':30}{PA_CONTRACTS:<10}")
    print(f"{'tick val ($):':30}{TICK_VAL:<10.2f}")
    print(f"{'spread (ticks):':30}{SPREAD:<10.2f}")
    print(f"{'commissions ($):':30}{COMMISSIONS:<10.2f}")
    print(f"{'trade cost ($):':30}{PA_COSTS:<10.2f}")
    print(f"{'tp (ticks):':30}{PA_TP_TICKS:<10.2f}")
    print(f"{'tp ($):':30}{PA_TP_DOLLARS:<10.2f}")
    print(f"{'sl (ticks):':30}{PA_SL_TICKS:<10.2f}")
    print(f"{'sl ($):':30}{PA_SL_DOLLARS:<10.2f}")
    print(f"{'trials:':30}{TRIALS:<10}\n")

    print("PA SMALLS")
    print(f"{'contracts:':30}{PA_SMALL_CONTRACTS:<10}")
    print(f"{'tick val ($):':30}{TICK_VAL:<10.2f}")
    print(f"{'spread (ticks):':30}{SPREAD:<10.2f}")
    print(f"{'commissions ($):':30}{COMMISSIONS:<10.2f}")
    print(f"{'trade cost ($):':30}{PA_SMALL_COSTS:<10.2f}")
    print(f"{'tp (ticks):':30}{PA_SMALL_TP_TICKS:<10.2f}")
    print(f"{'tp ($):':30}{PA_SMALL_TP_DOLLARS:<10.2f}")
    print(f"{'sl (ticks):':30}{PA_SMALL_SL_TICKS:<10.2f}")
    print(f"{'sl ($):':30}{PA_SMALL_SL_DOLLARS:<10.2f}")
    print(f"{'trials:':30}{TRIALS:<10}\n")

    p_eval_pass, eval_ev    = runEVAL("EVAL")
    p_pa_pass, pa_ev        = runPA("PA")
    p_paS_pass, paS_ev      = runPA_SMALL("PA_SMALL")



    p_eval_fail             = 1 - p_eval_pass
    p_pa_fail               = 1 - (p_pa_pass * p_paS_pass)
    c_eval_fail             = CONFIG["EVAL"]["cost_lose"]
    e_eval_fail             = p_eval_fail * c_eval_fail
    
    p_eval_pass_pa_fail     = p_eval_pass * p_pa_fail
    c_eval_pass_pa_fail     = CONFIG["EVAL"]["cost_win"] + CONFIG["PA"]["cost_lose"]
    e_eval_pass_pa_fail     = p_eval_pass_pa_fail * c_eval_pass_pa_fail
    
    p_eval_pass_pa_pass     = p_eval_pass * p_pa_pass * p_paS_pass
    c_eval_pass_pa_pass     = CONFIG["EVAL"]["cost_win"] + CONFIG["PA"]["cost_win"]
    e_eval_pass_pa_pass     = p_eval_pass_pa_pass * c_eval_pass_pa_pass
    
    p_total                 = p_eval_fail + p_eval_pass_pa_fail + p_eval_pass_pa_pass
    e_total                 = e_eval_fail + e_eval_pass_pa_fail + e_eval_pass_pa_pass



    print("\n")
    print(f"{'case:':30}{'prob':10}{'cost':10}{'ev':10}")
    print(f"{'eval fail:':30}{p_eval_fail:<10.2f}{c_eval_fail:<10.2f}{e_eval_fail:<10.2f}")
    print(f"{'eval pass, pa_fail:':30}{p_eval_pass_pa_fail:<10.2f}{c_eval_pass_pa_fail:<10.2f}{e_eval_pass_pa_fail:<10.2f}")
    print(f"{'eval pass, pa_pass:':30}{p_eval_pass_pa_pass:<10.2f}{c_eval_pass_pa_pass:<10.2f}{e_eval_pass_pa_pass:<10.2f}")
    print(f"{'total:':30}{p_total:<10.2f}{'':10}{e_total:<10.2f}")

    print(f"\n{time() - t0:0.1f}s")