# Nordhaus (1967/1969) on Medicare drug data: findings

## In plain English

William Nordhaus showed in 1967 that the best length for a patent depends, once two hard-to-measure research
parameters are fixed, on one observable number: how much more of a product people buy when its patent ends. I
measured that number at 95 brand-name pills that went generic in Medicare Part D between 2014 and 2022.

- **Prices collapse, use mostly does not.** Two years after generics arrive, the price per pill is down 55% for the
  average drug against matched controls, but the typical drug sells only about 2% more pills. Nexium (AstraZeneca)
  and Gleevec (Novartis) sold fewer.
- **A few blockbusters carry the loss.** Crestor (AstraZeneca, +75% pills) and Zetia (Merck, +58%) account for 48% of
  the deadweight loss among drugs whose use rose. Lyrica (Pfizer) rose 15%, Abilify (Otsuka) 18%, Cymbalta (Eli Lilly)
  22%.
- **Eight cents of loss per dollar of reward.** Across the 95 drugs the monopoly rent in the last patent year is
  $26.9 billion and the deadweight loss $2.2 billion.
- **The discount rate decides the optimal life.** With Nordhaus's 20% rate the rent-weighted estimate implies 4.8
  years; at 7%, 13.6 years, almost exactly the 14-year median these drugs actually had between first FDA approval and
  generic entry; at 3%, 32 years. The average drug's rise of 5% gives 8.8 years at 20%, close to Nordhaus's 8.7.

The essay is in the [README](../README.md); methods are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels below.** *B* = proportional fall in price per pill two years after entry, net of matched
controls. *x* = proportional rise in pills dispensed over the same years, net of controls. *d* = x/B, the implied
demand elasticity. *Rent* = B times Part D spending in the year before entry. *DWL* = deadweight loss, x times rent
divided by 2. *T\** = Nordhaus's optimal patent life in years at sigma = 9 and the stated discount rate rho. *E* or
*entry* = first year generics reach 5% of the molecule's pills. Dollar figures are Part D gross spending, before
manufacturer rebates.

## 1. Nordhaus's Table 1, printed and recomputed

Each cell shows his printed value / the value recomputed from his equations (13) and (14) with rho = 0.20 and
sigma = 9. "n" marks cells he left out as drastic inventions; the recomputed run-of-the-mill value is in brackets.
Source: `table1_replication.csv`.

| d \ B | 0.001 | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.5 | 0.75 | 0.9 |
|---|---|---|---|---|---|---|---|---|---|
| 0.25 | 34.0 / 33.96 | 22.5 / 22.51 | 19.1 / 19.11 | 14.7 / 14.72 | 11.6 / 11.57 | 8.7 / 8.67 | n (5.49) | n (4.39) | n (3.96) |
| 0.5 | 30.5 / 30.50 | 19.1 / 19.11 | 15.8 / 15.77 | 11.6 / 11.57 | 8.6 / 8.67 | 6.2 / 6.18 | 3.7 / 3.74 | n (2.98) | n (2.70) |
| 0.75 | 28.5 / 28.48 | 17.1 / 17.15 | 13.9 / 13.87 | 9.8 / 9.83 | 7.2 / 7.16 | 5.0 / 4.97 | 2.9 / 2.98 | 2.4 / 2.40 | n (2.20) |
| 1.0 | 27.0 / 27.05 | 15.8 / 15.77 | 12.6 / 12.56 | 8.7 / 8.67 | 6.2 / 6.18 | 4.2 / 4.24 | 2.5 / 2.55 | 2.0 / 2.09 | 1.9 / 1.92 |
| 1.5 | 25.0 / 25.03 | 13.9 / 13.87 | 10.8 / 10.78 | 7.2 / 7.16 | 5.0 / 4.97 | 3.4 / 3.37 | 2.1 / 2.09 | 1.7 / 1.75 | 1.6 / 1.64 |
| 2.0 | 23.6 / 23.61 | 12.6 / 12.56 | 9.6 / 9.57 | 6.2 / 6.18 | 4.2 / 4.24 | 2.9 / 2.88 | 1.8 / 1.84 | 1.5 / 1.58 | 1.4 / 1.48 |
| 4.0 | 20.2 / 20.20 | 9.6 / 9.57 | 6.9 / 6.93 | 4.2 / 4.24 | 2.9 / 2.88 | 2.0 / 2.03 | 1.4 / 1.44 | 1.2 / 1.30 | 1.2 / 1.25 |
| 10.0 | 15.8 / 15.77 | 6.2 / 6.18 | 4.2 / 4.24 | 2.6 / 2.55 | 1.8 / 1.84 | 1.4 / 1.44 | 1.2 / 1.18 | 1.1 / 1.12 | 1.1 / 1.10 |

Sensitivity values quoted on page 28 of the discussion paper (`table1_sigma_check.csv`):

| case | T_rerun | T_printed |
|---|---|---|
| d=1, B=0.05, sigma=4 | 12.21 | 12.2 |
| d=1, B=0.05, sigma=9 | 8.67 | 8.7 |
| d=1, B=0.05, sigma=20 | 5.66 | 5.6 |

## 2. Part D release agreement

The same calendar year appears in five CMS releases. Share of molecules whose dosage units agree between the first
and last release, which is why each event is measured inside a single release (`partd_release_agreement.csv`):

| calendar_year | first_release | last_release | molecules_in_both | share_within_1pct | share_within_5pct | spend_first_$B | spend_last_$B |
|---|---|---|---|---|---|---|---|
| 2016 | 2016 | 2020 | 1355 | 0.542 | 0.676 | 141.4 | 141.2 |
| 2017 | 2017 | 2021 | 1413 | 0.527 | 0.674 | 151.6 | 149.8 |
| 2018 | 2018 | 2022 | 1562 | 0.651 | 0.749 | 168.1 | 163.5 |
| 2019 | 2019 | 2023 | 1599 | 0.663 | 0.785 | 183.2 | 178.9 |
| 2020 | 2020 | 2024 | 1633 | 0.690 | 0.792 | 198.7 | 194.1 |

## 3. Event path

Mean and median contrast with matched controls, in log points, relative to the year before entry (k = -1), for the
95 drugs (`event_path.csv`). lnp = log gross spending per dosage unit, lnq = log dosage units.

| var | k | treated | control | did | did_median | sd | n | se |
|---|---|---|---|---|---|---|---|---|
| lnp | -2 | -0.111 | -0.108 | -0.003 | -0.000 | 0.010 | 95 | 0.001 |
| lnp | 0 | -0.061 | 0.077 | -0.139 | -0.108 | 0.189 | 95 | 0.019 |
| lnp | 1 | -0.495 | 0.134 | -0.629 | -0.540 | 0.450 | 95 | 0.046 |
| lnp | 2 | -0.789 | 0.165 | -0.954 | -0.821 | 0.584 | 95 | 0.060 |
| lnq | -2 | 0.043 | 0.022 | 0.021 | 0.001 | 0.107 | 95 | 0.011 |
| lnq | 0 | -0.095 | -0.029 | -0.066 | -0.029 | 0.162 | 95 | 0.017 |
| lnq | 1 | -0.116 | -0.066 | -0.049 | -0.026 | 0.283 | 95 | 0.029 |
| lnq | 2 | -0.134 | -0.106 | -0.027 | 0.020 | 0.388 | 95 | 0.040 |

## 4. Headline estimates of x and B

Bootstrap percentile intervals over drugs, 2,000 draws (`headline_x.csv`):

| statistic | estimate | ci_low | ci_high | se_boot | n_events |
|---|---|---|---|---|---|
| x_mean | 0.048 | -0.036 | 0.141 | 0.045 | 95 |
| x_median | 0.020 | -0.081 | 0.087 | 0.043 | 95 |
| x_rent_weighted | 0.162 | 0.042 | 0.288 | 0.064 | 95 |
| B_mean | 0.552 | 0.504 | 0.597 | 0.023 | 95 |
| B_spend_weighted | 0.700 | 0.632 | 0.753 | 0.031 | 95 |

## 5. Optimal patent life implied by each estimate

T at the interval ends of x are in the last two columns; "unbounded" means x is zero or negative there
(`optimal_life.csv`):

| x_statistic | sigma | rho | x | T_star | T_at_x_ci_high | T_at_x_ci_low |
|---|---|---|---|---|---|---|
| x_mean | 4.0 | 0.2 | 0.048 | 12.35 | 8.10 | unbounded |
| x_mean | 4.0 | 0.07 | 0.048 | 35.27 | 23.16 | unbounded |
| x_mean | 4.0 | 0.03 | 0.048 | 82.30 | 54.03 | unbounded |
| x_mean | 9.0 | 0.2 | 0.048 | 8.79 | 5.15 | unbounded |
| x_mean | 9.0 | 0.07 | 0.048 | 25.13 | 14.73 | unbounded |
| x_mean | 9.0 | 0.03 | 0.048 | 58.63 | 34.36 | unbounded |
| x_mean | 20.0 | 0.2 | 0.048 | 5.76 | 2.97 | unbounded |
| x_mean | 20.0 | 0.07 | 0.048 | 16.45 | 8.49 | unbounded |
| x_mean | 20.0 | 0.03 | 0.048 | 38.38 | 19.81 | unbounded |
| x_median | 4.0 | 0.2 | 0.020 | 16.35 | 9.90 | unbounded |
| x_median | 4.0 | 0.07 | 0.020 | 46.71 | 28.28 | unbounded |
| x_median | 4.0 | 0.03 | 0.020 | 108.98 | 65.98 | unbounded |
| x_median | 9.0 | 0.2 | 0.020 | 12.52 | 6.64 | unbounded |
| x_median | 9.0 | 0.07 | 0.020 | 35.78 | 18.97 | unbounded |
| x_median | 9.0 | 0.03 | 0.020 | 83.50 | 44.26 | unbounded |
| x_median | 20.0 | 0.2 | 0.020 | 9.01 | 4.05 | unbounded |
| x_median | 20.0 | 0.07 | 0.020 | 25.74 | 11.57 | unbounded |
| x_median | 20.0 | 0.03 | 0.020 | 60.05 | 27.00 | unbounded |
| x_rent_weighted | 4.0 | 0.2 | 0.162 | 7.61 | 5.87 | 12.97 |
| x_rent_weighted | 4.0 | 0.07 | 0.162 | 21.75 | 16.76 | 37.07 |
| x_rent_weighted | 4.0 | 0.03 | 0.162 | 50.75 | 39.11 | 86.49 |
| x_rent_weighted | 9.0 | 0.2 | 0.162 | 4.76 | 3.45 | 9.37 |
| x_rent_weighted | 9.0 | 0.07 | 0.162 | 13.61 | 9.85 | 26.76 |
| x_rent_weighted | 9.0 | 0.03 | 0.162 | 31.76 | 22.98 | 62.44 |
| x_rent_weighted | 20.0 | 0.2 | 0.162 | 2.70 | 1.85 | 6.23 |
| x_rent_weighted | 20.0 | 0.07 | 0.162 | 7.72 | 5.27 | 17.81 |
| x_rent_weighted | 20.0 | 0.03 | 0.162 | 18.02 | 12.31 | 41.56 |
| nordhaus_1967_typical | 9.0 | 0.2 | 0.050 | 8.67 |  |  |

## 6. Dollars and concentration

`dollars_summary.csv`:

| events | spend_pre_$B | rent_$B | dwl_$B | dwl_per_dollar_rent | share_x_positive | share_x_below_10pct | share_x_at_least_1 | dwl_top2_share_of_positive | dwl_top5_share_of_positive |
|---|---|---|---|---|---|---|---|---|---|
| 95 | 38.49 | 26.93 | 2.18 | 0.081 | 0.516 | 0.611 | 0.032 | 0.479 | 0.688 |

## 7. Robustness

`robustness.csv`. The unmatched-control row shows why matching matters: drugs approaching expiry were already growing
more slowly than the average stable drug.

| variant | n | x_mean | x_median | x_rent_weighted | B_mean | B_spend_weighted |
|---|---|---|---|---|---|---|
| primary: pills, 10 matched controls, pills dispensed, E+2 | 95 | 0.048 | 0.020 | 0.162 | 0.552 | 0.700 |
| prescriptions (claims) instead of pills | 95 | -0.009 | -0.099 | 0.007 | 0.552 | 0.700 |
| 25 matched controls | 95 | 0.040 | -0.005 | 0.169 | 0.551 | 0.695 |
| all eligible controls, no matching | 95 | -0.125 | -0.167 | 0.057 | 0.465 | 0.615 |
| pills only (every listing a tablet or capsule) | 65 | 0.044 | -0.038 | 0.222 | 0.548 | 0.697 |
| events with at least $100M pre-entry spending | 63 | 0.012 | 0.010 | 0.163 | 0.639 | 0.711 |
| every event and control, any dosage form | 123 | 0.168 | 0.060 | 0.198 | 0.501 | 0.676 |
| horizon E+1 in release E+1, matched on E-3 to E-1 | 81 | 0.031 | -0.029 | 0.062 | 0.423 | 0.550 |

Placebo check in the alternative design (release E+1, matched on the change from E-3 to E-1), log points
(`pretrend_check_horizon1.csv`):

| k | mean | median | std | size |
|---|---|---|---|---|
| -3 | 0.040 | 0.000 | 0.127 | 81 |
| -2 | 0.038 | 0.018 | 0.134 | 81 |
| 0 | -0.031 | -0.008 | 0.157 | 81 |
| 1 | -0.020 | -0.029 | 0.300 | 81 |

## 8. Extension: how long exclusivity actually lasts

Orange Book, every ingredient set first approved under an NDA from 1985 to 2019; time to first ANDA approval,
Kaplan-Meier (`time_to_generic_by_cohort.csv`). Shares are reported only where every drug in the cohort could have
been followed that long.

| cohort | ingredient_sets | with_generic | km_median_years | share_generic_by_10y | share_generic_by_15y | share_generic_by_20y |
|---|---|---|---|---|---|---|
| 1985-1989 | 130 | 84 | 18.30 | 0.15 | 0.43 | 0.53 |
| 1990-1994 | 127 | 86 | 14.70 | 0.20 | 0.52 | 0.63 |
| 1995-1999 | 202 | 153 | 14.91 | 0.17 | 0.51 | 0.66 |
| 2000-2004 | 151 | 118 | 13.39 | 0.29 | 0.58 | 0.73 |
| 2005-2009 | 127 | 92 | 14.00 | 0.35 | 0.58 | not yet observable |
| 2010-2014 | 158 | 86 | 13.00 | 0.34 | not yet observable | not yet observable |
| 2015-2019 | 201 | 45 | not reached | not yet observable | not yet observable | not yet observable |
| 1985-2019 | 1096 | 664 | 14.50 | 0.25 | 0.55 | 0.67 |

The Part D entries, from first NDA approval to the entry year, against Nordhaus's optimum at the rent-weighted x
(`events_exclusivity_summary.csv`):

| events_matched | median_years_to_partd_entry | mean_years_to_partd_entry | spend_weighted_mean_years | p25 | p75 | median_years_to_first_anda | T_star_rho20 | T_star_rho07 | T_star_rho03 |
|---|---|---|---|---|---|---|---|---|---|
| 91 | 14.00 | 13.65 | 13.19 | 11.00 | 15.00 | 12.07 | 4.76 | 13.61 | 31.76 |

## 9. Every event

The year-by-year contrast for each drug, quantity and price, is in `event_did_by_event.csv`.

All 95 drugs, sorted by Part D spending in the year before entry (`events.csv`, `events_exclusivity.csv`).
raw_units and raw_price are the unadjusted proportional changes from E-1 to E+2. first_NDA is the first NDA approval
year of the active moiety in the Orange Book.

| brand | maker | molecule | entry | spend_pre_$M | B | x | d | rent_$M | dwl_$M | T*_20% | T*_7% | raw_units | raw_price | first_NDA | years_to_entry |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Lyrica | Pfizer/Viatris | pregabalin | 2019 | 2951 | 0.906 | 0.154 | 0.17 | 2673 | 205.5 | 4.9 | 14.0 | 0.217 | -0.888 | 2004 | 15 |
| Crestor | Astrazeneca | rosuvastatin calcium | 2016 | 2883 | 0.884 | 0.747 | 0.85 | 2549 | 952.3 | 2.1 | 6.0 | 0.668 | -0.874 | 2003 | 13 |
| Nexium | Astrazeneca | esomeprazole magnesium | 2015 | 2651 | 0.617 | -0.066 | -0.11 | 1635 | -53.9 | unbounded | unbounded | -0.309 | -0.431 | 2001 | 14 |
| Abilify | Otsuka America | aripiprazole | 2015 | 2578 | 0.808 | 0.176 | 0.22 | 2082 | 183.5 | 4.5 | 13.0 | 0.118 | -0.679 | 2002 | 13 |
| Cymbalta | Eli Lilly & Co. | duloxetine hcl | 2014 | 1992 | 0.878 | 0.221 | 0.25 | 1749 | 193.0 | 4.0 | 11.5 | 0.519 | -0.826 | 2004 | 10 |
| Namenda | Forest/Allergan | memantine hcl | 2015 | 1886 | 0.545 | 0.206 | 0.38 | 1028 | 106.1 | 4.2 | 11.9 | -0.009 | -0.394 | 2003 | 12 |
| Zytiga | Janssen Biotech; Janssen Pharm. | abiraterone acetate | 2019 | 1502 | 0.737 | 0.096 | 0.13 | 1108 | 53.4 | 6.3 | 18.0 | 0.450 | -0.665 | 2011 | 8 |
| Zetia | Merck Sharp & D | ezetimibe | 2017 | 1462 | 0.900 | 0.583 | 0.65 | 1315 | 383.5 | 2.4 | 6.7 | 0.532 | -0.876 | 2002 | 15 |
| Gleevec | Novartis | imatinib mesylate | 2016 | 1233 | 0.539 | -0.086 | -0.16 | 664 | -28.6 | unbounded | unbounded | -0.044 | -0.326 | 2001 | 15 |
| Diovan | Novartis | valsartan | 2014 | 1223 | 0.827 | 0.082 | 0.10 | 1011 | 41.4 | 6.9 | 19.6 | -0.049 | -0.770 | 1996 | 18 |
| Celebrex | Pfizer US Pharm | celecoxib | 2015 | 1083 | 0.829 | 0.247 | 0.30 | 897 | 110.7 | 3.8 | 10.8 | 0.034 | -0.718 | 1998 | 17 |
| Vimpat | UCB Pharma* | lacosamide | 2022 | 788 | 0.823 | 0.020 | 0.02 | 649 | 6.5 | 12.5 | 35.8 | 0.420 | -0.843 | 2008 | 14 |
| Vesicare | Astellas Pharma | solifenacin succinate | 2019 | 692 | 0.874 | 0.158 | 0.18 | 604 | 47.8 | 4.8 | 13.8 | -0.100 | -0.856 | 2004 | 15 |
| Dexilant | Takeda Pharmace | dexlansoprazole | 2022 | 676 | 0.444 | -0.226 | -0.51 | 300 | -33.9 | unbounded | unbounded | -0.250 | -0.484 | 2009 | 13 |
| Esbriet | Genentech, Inc. | pirfenidone | 2022 | 662 | 0.747 | -0.110 | -0.15 | 494 | -27.1 | unbounded | unbounded | -0.152 | -0.698 | 2014 | 8 |
| Ranexa | Gilead Sciences | ranolazine | 2019 | 658 | 0.812 | 0.145 | 0.18 | 535 | 38.7 | 5.1 | 14.5 | 0.243 | -0.788 | 2006 | 13 |
| Letairis | Gilead Sciences | ambrisentan | 2019 | 608 | 0.482 | 0.363 | 0.75 | 293 | 53.3 | 3.0 | 8.7 | 0.088 | -0.427 | 2007 | 12 |
| Evista | Eli Lilly & Co. | raloxifene hcl | 2014 | 481 | 0.571 | -0.338 | -0.59 | 275 | -46.4 | unbounded | unbounded | -0.371 | -0.430 | 1997 | 17 |
| Bystolic | Forest/Allergan | nebivolol hcl | 2021 | 480 | 0.752 | 0.075 | 0.10 | 361 | 13.6 | 7.1 | 20.4 | -0.006 | -0.712 | 2007 | 14 |
| Zortress | Novartis | everolimus | 2020 | 470 | 0.503 | 0.083 | 0.17 | 236 | 9.8 | 6.8 | 19.4 | 0.198 | -0.404 | 2009 | 11 |
| Lovaza | Glaxosmithkline | omega-3 acid ethyl esters | 2014 | 453 | 0.335 | -0.298 | -0.89 | 152 | -22.6 | unbounded | unbounded | -0.245 | -0.246 | 2004 | 10 |
| Cialis | Eli Lilly & Co. | tadalafil | 2018 | 453 | 0.510 | 0.010 | 0.02 | 231 | 1.1 | 15.9 | 45.3 | -0.084 | -0.540 | 2003 | 15 |
| Benicar | Daiichi Sankyo, | olmesartan medoxomil | 2016 | 434 | 0.818 | 0.192 | 0.23 | 355 | 34.1 | 4.3 | 12.4 | 0.107 | -0.755 | 2002 | 14 |
| Gilenya | Novartis | fingolimod hcl | 2022 | 409 | 0.714 | -0.241 | -0.34 | 292 | -35.2 | unbounded | unbounded | -0.211 | -0.664 | 2010 | 12 |
| Aggrenox | Boehringer Ing. | aspirin/dipyridamole | 2015 | 326 | 0.270 | -0.345 | -1.28 | 88 | -15.2 | unbounded | unbounded | -0.632 | 0.075 | 1999 | 16 |
| Uloric | Takeda Pharmace | febuxostat | 2019 | 322 | 0.665 | -0.340 | -0.51 | 214 | -36.4 | unbounded | unbounded | -0.312 | -0.611 | 2009 | 10 |
| Avodart | Glaxosmithkline | dutasteride | 2015 | 318 | 0.801 | 0.157 | 0.20 | 255 | 20.0 | 4.8 | 13.9 | -0.350 | -0.700 | 2001 | 14 |
| Colcrys | Takeda Pharmace | colchicine | 2015 | 313 | 0.115 | -0.204 | -1.77 | 36 | -3.7 | unbounded | unbounded | -0.074 | 0.064 | 2009 | 6 |
| Sensipar | Amgen | cinacalcet hcl | 2019 | 309 | 0.492 | 1.464 | 2.97 | 152 | 111.4 | 1.6 | 4.5 | 0.170 | -0.599 | 2004 | 15 |
| Chantix | Pfizer US Pharm | varenicline tartrate | 2021 | 299 | 0.284 | 0.087 | 0.31 | 85 | 3.7 | 6.6 | 19.0 | -0.087 | -0.167 | 2006 | 15 |
| Welchol | Daiichi Sankyo, | colesevelam hcl | 2018 | 293 | 0.292 | -0.042 | -0.14 | 86 | -1.8 | unbounded | unbounded | -0.156 | -0.270 | 2000 | 18 |
| Invega | Janssen Pharm. | paliperidone | 2015 | 283 | 0.446 | 0.133 | 0.30 | 126 | 8.4 | 5.3 | 15.2 | 0.077 | -0.075 | 2006 | 9 |
| Amitiza | Takeda Pharmace | lubiprostone | 2021 | 279 | 0.385 | -0.332 | -0.86 | 108 | -17.9 | unbounded | unbounded | -0.400 | -0.389 | 2006 | 15 |
| Vytorin | Merck Sharp & D | ezetimibe/simvastatin | 2017 | 277 | 0.639 | -0.139 | -0.22 | 177 | -12.3 | unbounded | unbounded | -0.408 | -0.552 | 2004 | 13 |
| Benicar HCT | Daiichi Sankyo, | olmesartan/hydrochlorothiazide | 2016 | 268 | 0.814 | 0.100 | 0.12 | 218 | 10.9 | 6.2 | 17.7 | -0.048 | -0.750 | 2003 | 13 |
| Jadenu | Novartis | deferasirox | 2019 | 250 | 0.606 | -0.031 | -0.05 | 151 | -2.4 | unbounded | unbounded | -0.180 | -0.565 | 2005 | 14 |
| Truvada | Gilead Sciences | emtricitabine/tenofovir (tdf) | 2020 | 247 | 0.787 | -0.147 | -0.19 | 194 | -14.3 | unbounded | unbounded | -0.385 | -0.760 | 2004 | 16 |
| Northera | Lundbeck Inc. | droxidopa | 2021 | 241 | 0.739 | 0.386 | 0.52 | 178 | 34.3 | 2.9 | 8.4 | 0.359 | -0.713 | 2014 | 7 |
| Ampyra | Acorda Therapeu | dalfampridine | 2018 | 239 | 0.560 | 0.046 | 0.08 | 134 | 3.1 | 9.0 | 25.7 | 0.373 | -0.520 | 2010 | 8 |
| Effient | Eli Lilly & Co. | prasugrel hcl | 2017 | 238 | 0.849 | -0.021 | -0.02 | 202 | -2.1 | unbounded | unbounded | -0.091 | -0.813 | 2009 | 8 |
| Actonel | Actavis/Allerga | risedronate sodium | 2015 | 219 | 0.522 | -0.292 | -0.56 | 115 | -16.7 | unbounded | unbounded | -0.570 | -0.379 | 1998 | 17 |
| Lunesta | Sunovion Pharma | eszopiclone | 2014 | 219 | 0.868 | -0.249 | -0.29 | 190 | -23.6 | unbounded | unbounded | -0.332 | -0.803 | 2004 | 10 |
| Azilect | Teva Neuroscien | rasagiline mesylate | 2017 | 217 | 0.583 | -0.038 | -0.07 | 126 | -2.4 | unbounded | unbounded | -0.068 | -0.452 | 2006 | 11 |
| Atripla | Gilead Sciences | efavirenz/emtricit/tenofovr df | 2020 | 214 | 0.693 | -0.406 | -0.59 | 148 | -30.0 | unbounded | unbounded | -0.546 | -0.655 | 2006 | 14 |
| Epzicom | Viiv Healthcare | abacavir sulfate/lamivudine | 2016 | 211 | 0.708 | -0.295 | -0.42 | 149 | -22.0 | unbounded | unbounded | -0.549 | -0.661 | 2004 | 12 |
| Tracleer | Actelion Pharma | bosentan | 2019 | 207 | 0.555 | -0.167 | -0.30 | 115 | -9.6 | unbounded | unbounded | -0.415 | -0.459 | 2001 | 18 |
| Daliresp | Astrazeneca | roflumilast | 2022 | 199 | 0.747 | 0.249 | 0.33 | 149 | 18.5 | 3.7 | 10.7 | 0.245 | -0.748 | 2011 | 11 |
| Pristiq | Wyeth/Pfizer | desvenlafaxine succinate | 2017 | 197 | 0.789 | 0.502 | 0.64 | 155 | 39.0 | 2.5 | 7.3 | 0.419 | -0.727 | 2008 | 9 |
| Xenazine | Lundbeck Inc. | tetrabenazine | 2015 | 194 | 0.129 | -0.081 | -0.63 | 25 | -1.0 | unbounded | unbounded | 0.078 | 0.109 | 2008 | 7 |
| Valcyte | Genentech, Inc. | valganciclovir hcl | 2015 | 194 | 0.494 | 0.152 | 0.31 | 96 | 7.3 | 4.9 | 14.1 | 0.179 | -0.408 | 2001 | 14 |
| Tarceva | Genentech, Inc. | erlotinib hcl | 2019 | 181 | 0.697 | -0.439 | -0.63 | 126 | -27.7 | unbounded | unbounded | -0.626 | -0.628 | 2004 | 15 |
| Viread | Gilead Sciences | tenofovir disoproxil fumarate | 2018 | 167 | 0.853 | -0.057 | -0.07 | 142 | -4.0 | unbounded | unbounded | -0.194 | -0.831 | 2001 | 17 |
| Toviaz | Pfizer US Pharm | fesoterodine fumarate | 2022 | 163 | 0.777 | -0.389 | -0.50 | 127 | -24.6 | unbounded | unbounded | -0.343 | -0.806 | 2008 | 14 |
| Exforge | Novartis | amlodipine/valsartan | 2014 | 160 | 0.688 | -0.295 | -0.43 | 110 | -16.2 | unbounded | unbounded | -0.301 | -0.646 | 2007 | 7 |
| Reyataz | BMS Primarycare | atazanavir sulfate | 2018 | 145 | 0.680 | -0.529 | -0.78 | 99 | -26.1 | unbounded | unbounded | -0.626 | -0.674 | 2003 | 15 |
| Viibryd | Allergan Inc. | vilazodone hcl | 2022 | 135 | 0.760 | 0.039 | 0.05 | 102 | 2.0 | 9.7 | 27.8 | 0.217 | -0.734 | 2011 | 11 |
| Onfi | Lundbeck Inc. | clobazam | 2018 | 124 | 0.745 | 0.183 | 0.25 | 92 | 8.4 | 4.4 | 12.7 | 0.529 | -0.694 | 2011 | 7 |
| Sutent | Pfizer US Pharm | sunitinib malate | 2021 | 120 | 0.374 | -0.086 | -0.23 | 45 | -1.9 | unbounded | unbounded | -0.195 | -0.296 | 2006 | 15 |
| Banzel | Eisai Inc. | rufinamide | 2021 | 117 | 0.548 | -0.027 | -0.05 | 64 | -0.9 | unbounded | unbounded | 0.046 | -0.499 | 2008 | 13 |
| Tikosyn | Pfizer US Pharm | dofetilide | 2016 | 113 | 0.320 | 0.035 | 0.11 | 36 | 0.6 | 10.1 | 28.8 | 0.279 | -0.050 | 1999 | 17 |
| Micardis | Boehringer Ing. | telmisartan | 2014 | 105 | 0.778 | 0.038 | 0.05 | 82 | 1.6 | 9.8 | 27.9 | -0.114 | -0.681 | 1998 | 16 |
| Azor | Daiichi Sankyo, | amlodipine bes/olmesartan med | 2016 | 105 | 0.715 | 0.426 | 0.60 | 75 | 16.0 | 2.8 | 7.9 | -0.154 | -0.617 | 2007 | 9 |
| Norvir | Abbvie US LLC | ritonavir | 2018 | 101 | 0.641 | -0.461 | -0.72 | 65 | -14.9 | unbounded | unbounded | -0.541 | -0.631 | 1996 | 22 |
| Tamiflu | Genentech, Inc.; Roche Labs. | oseltamivir phosphate | 2016 | 88 | 0.232 | 0.696 | 3.00 | 20 | 7.1 | 2.2 | 6.2 | 1.233 | -0.178 | 1999 | 17 |
| Fosrenol | Shire US Inc. | lanthanum carbonate | 2017 | 85 | 0.309 | 0.033 | 0.11 | 26 | 0.4 | 10.4 | 29.7 | -0.277 | -0.136 | 2004 | 13 |
| Noxafil | Merck Sharp & D* | posaconazole | 2019 | 82 | 0.421 | 0.317 | 0.75 | 35 | 5.5 | 3.3 | 9.3 | 0.480 | -0.294 | 2006 | 13 |
| Nexavar | Bayer,Pharm Div | sorafenib tosylate | 2022 | 77 | 0.511 | -0.013 | -0.03 | 39 | -0.3 | unbounded | unbounded | -0.353 | -0.482 | 2005 | 17 |
| Coreg Cr | Glaxosmithkline | carvedilol phosphate | 2017 | 75 | 0.254 | 0.123 | 0.48 | 19 | 1.2 | 5.6 | 15.9 | -0.251 | -0.122 | 1995 | 22 |
| Nuvigil | Cephalon,Inc.-T | armodafinil | 2016 | 74 | 0.753 | 0.104 | 0.14 | 56 | 2.9 | 6.1 | 17.3 | 0.091 | -0.704 | 2007 | 9 |
| Strattera | Eli Lilly & Co. | atomoxetine hcl | 2017 | 70 | 0.672 | 0.327 | 0.49 | 47 | 7.7 | 3.2 | 9.2 | 0.437 | -0.614 | 2002 | 15 |
| Micardis HCT | Boehringer Ing. | telmisartan/hydrochlorothiazid | 2014 | 69 | 0.549 | -0.272 | -0.50 | 38 | -5.2 | unbounded | unbounded | -0.352 | -0.352 | 2000 | 14 |
| Intelence | Janssen Product | etravirine | 2021 | 68 | 0.269 | -0.276 | -1.02 | 18 | -2.5 | unbounded | unbounded | -0.418 | -0.211 | 2008 | 13 |
| Baraclude | BMS Primarycare | entecavir | 2014 | 67 | 0.354 | 0.223 | 0.63 | 24 | 2.7 | 4.0 | 11.4 | 0.361 | -0.170 | 2005 | 9 |
| Sustiva | BMS | efavirenz | 2018 | 57 | 0.398 | -0.273 | -0.69 | 23 | -3.1 | unbounded | unbounded | -0.503 | -0.363 | 1998 | 20 |
| Rozerem | Takeda Pharmace | ramelteon | 2019 | 57 | 0.674 | 0.593 | 0.88 | 38 | 11.4 | 2.3 | 6.7 | 0.164 | -0.622 | 2005 | 14 |
| Jalyn | Glaxosmithkline | dutasteride/tamsulosin hcl | 2016 | 51 | 0.353 | -0.279 | -0.79 | 18 | -2.5 | unbounded | unbounded | -0.459 | -0.297 | 2010 | 6 |
| Duexis | Horizon/Amgen | ibuprofen/famotidine | 2021 | 49 | 0.557 | -0.189 | -0.34 | 27 | -2.6 | unbounded | unbounded | -0.118 | -0.549 | 2011 | 10 |
| Enablex | Actavis/Allerga | darifenacin hydrobromide | 2016 | 47 | 0.185 | 0.292 | 1.58 | 9 | 1.3 | 3.4 | 9.8 | -0.394 | -0.198 | 2004 | 12 |
| Daraprim | Vyera Pharmaceu | pyrimethamine | 2020 | 41 | 0.485 | -0.421 | -0.87 | 20 | -4.1 | unbounded | unbounded | -0.414 | -0.448 |  |  |
| Selzentry | Viiv Healthcare | maraviroc | 2022 | 40 | 0.137 | -0.084 | -0.61 | 5 | -0.2 | unbounded | unbounded | -0.245 | -0.247 | 2007 | 15 |
| Trizivir | Viiv Healthcare | abacavir/lamivudine/zidovudine | 2014 | 37 | 0.225 | -0.083 | -0.37 | 8 | -0.3 | unbounded | unbounded | -0.501 | -0.206 | 2000 | 14 |
| Relpax | Pfizer US Pharm | eletriptan hydrobromide | 2017 | 36 | 0.683 | -0.201 | -0.29 | 24 | -2.4 | unbounded | unbounded | -0.084 | -0.602 | 2002 | 15 |
| Tykerb | Novartis | lapatinib ditosylate | 2020 | 35 | 0.245 | -0.609 | -2.48 | 9 | -2.6 | unbounded | unbounded | -0.634 | -0.131 | 2007 | 13 |
| Cuprimine | Bausch Health U | penicillamine | 2019 | 35 | 0.573 | 0.149 | 0.26 | 20 | 1.5 | 5.0 | 14.3 | -0.193 | -0.434 |  |  |
| Edecrin | Valeant/Bausch | ethacrynic acid | 2016 | 34 | 0.383 | 0.258 | 0.67 | 13 | 1.7 | 3.7 | 10.5 | -0.195 | -0.245 |  |  |
| Vimovo | Horizon Pharma | naproxen/esomeprazole mag | 2020 | 33 | 0.407 | 2.332 | 5.73 | 13 | 15.6 | 1.4 | 3.9 | 1.835 | -0.388 | 2010 | 10 |
| Renagel | Genzyme | sevelamer hcl | 2019 | 28 | 0.286 | 0.998 | 3.49 | 8 | 4.0 | 1.8 | 5.3 | 0.331 | -0.256 | 1998 | 21 |
| Lexiva | Viiv Healthcare | fosamprenavir calcium | 2017 | 26 | 0.319 | -0.289 | -0.91 | 8 | -1.2 | unbounded | unbounded | -0.704 | -0.109 | 2003 | 14 |
| Tekturna | Noden Pharma D. | aliskiren hemifumarate | 2019 | 25 | 0.211 | -0.540 | -2.55 | 5 | -1.5 | unbounded | unbounded | -0.337 | -0.095 | 2007 | 12 |
| Zyflo Cr | Chiesi USA, Inc | zileuton | 2017 | 22 | 0.344 | 0.182 | 0.53 | 8 | 0.7 | 4.5 | 12.8 | -0.081 | -0.137 | 1996 | 21 |
| Rapamune | Wyeth Pharm | sirolimus | 2014 | 22 | 0.248 | 0.151 | 0.61 | 5 | 0.4 | 5.0 | 14.1 | 0.260 | -0.093 | 1999 | 15 |
| Bidil | Arbor/Azurity | isosorbide dinit/hydralazine | 2022 | 14 | 0.592 | -0.688 | -1.16 | 8 | -2.8 | unbounded | unbounded | 0.132 | -0.639 | 2005 | 17 |
| Syprine | Valeant/Bausch | trientine hcl | 2018 | 13 | 0.380 | 0.618 | 1.63 | 5 | 1.5 | 2.3 | 6.6 | 0.517 | -0.454 | 1985 | 33 |
| Lodosyn | Valeant | carbidopa | 2014 | 12 | -0.324 | -0.643 | 1.99 | -4 | 1.2 | unbounded | unbounded | -0.398 | 0.892 |  |  |
| Albenza | Amedra Pharmace | albendazole | 2018 | 10 | 0.450 | 1.289 | 2.87 | 5 | 3.0 | 1.7 | 4.8 | 0.688 | -0.288 | 1996 | 22 |