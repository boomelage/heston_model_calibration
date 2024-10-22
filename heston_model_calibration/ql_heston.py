import QuantLib as ql
class ql_heston():
    def calibrate_heston(vol_matrix,s,r,g):
        calculation_date = ql.Date.todaysDate()
        day_count = ql.Actual365Fixed()
        ql.Settings.instance().evaluationDate = calculation_date
        r_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date,float(r),day_count))
        g_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date,float(g),day_count))
        S_handle = ql.QuoteHandle(ql.SimpleQuote(float(s)))
        T = vol_matrix.columns.tolist()
        K = vol_matrix.index.tolist()
        heston_helpers = []
        v0 = 0.01; kappa = 0.2; theta = 0.02; rho = -0.75; eta = 0.5
        process = ql.HestonProcess(
            r_ts,
            g_ts,
            S_handle,
            v0,                # Initial volatility
            kappa,             # Mean reversion speed
            theta,             # Long-run variance (volatility squared)
            eta,               # Volatility of the volatility
            rho                # Correlation between asset and volatility
        )
        model = ql.HestonModel(process)
        engine = ql.AnalyticHestonEngine(model)

        for t in T:
            for k in K:
                p = ql.Period(int(t),ql.Days)
                volatility = vol_matrix.loc[k,t]
                helper = ql.HestonModelHelper(
                    p, ql.UnitedStates(ql.UnitedStates.NYSE), float(s), k, 
                    ql.QuoteHandle(ql.SimpleQuote(volatility)), 
                    r_ts, 
                    g_ts
                    )
                helper.setPricingEngine(engine)
                heston_helpers.append(helper)

        lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)


        model.calibrate(heston_helpers, lm,
                          ql.EndCriteria(500, 50, 1.0e-8,1.0e-8, 1.0e-8))

        theta, kappa, eta, rho, v0 = model.params()
        if v0 == 0.01 and kappa == 0.2 and theta == 0.02 and rho == -0.75 and eta == 0.5:
            return {'theta':None, 'kappa':None, 'eta':None, 'rho':None, 'v0':None}
        else:
            return {'theta':theta, 'kappa':kappa, 'eta':eta, 'rho':rho, 'v0':v0}