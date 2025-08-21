# src/ab_test.py
from statsmodels.stats.proportion import proportions_ztest
import math

def ab_test(clicks_control, impressions_control, clicks_treatment, impressions_treatment, alpha=0.05):
    counts = [clicks_control, clicks_treatment]
    nobs = [impressions_control, impressions_treatment]
    stat, pval = proportions_ztest(counts, nobs)
    ctr_control = clicks_control / impressions_control
    ctr_treatment = clicks_treatment / impressions_treatment
    lift = (ctr_treatment - ctr_control) / ctr_control if ctr_control > 0 else math.nan
    return {
        "ctr_control": ctr_control,
        "ctr_treatment": ctr_treatment,
        "lift": lift,
        "z_stat": stat,
        "p_value": pval,
        "significant": pval < alpha
    }

if __name__ == "__main__":
    c_control, i_control = 120, 2000
    c_treat, i_treat = 140, 2000
    print(ab_test(c_control, i_control, c_treat, i_treat))
