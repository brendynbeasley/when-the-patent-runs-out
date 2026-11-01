# Technical notes

This is the technical companion to the [README](README.md). Every table is in [results/FINDINGS.md](results/FINDINGS.md),
and a review of the original paper's methods is in [METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

William D. Nordhaus, *Invention, Growth, and Welfare: A Theoretical Treatment of Technological Change*, MIT Press,
1969. The patent-life model and its numerical tables first circulated as "The Optimal Life of a Patent," Cowles
Foundation Discussion Paper No. 241, Yale University, November 27, 1967 (free at cowles.yale.edu), which is the text
I worked from. With demand elasticity $`d = 1`$, a 5% cost reduction, $`\sigma = 9`$ and a 20% discount rate, his
Table 1 gives an optimal life of 8.7 years, which his text rounds to about nine, against a 17-year statutory term.

## Headline results

| Quantity | Estimate | 95% interval | N |
|---|---|---|---|
| Table 1 cells reproduced within 0.1 years | 66 of 66 | | 66 |
| Price fall two years after entry, mean $`\hat{B}`$ | 0.552 | [0.504, 0.597] | 95 |
| Rise in pills, mean $`\hat{x}`$ | 0.048 | [−0.036, 0.141] | 95 |
| Rise in pills, median | 0.020 | [−0.081, 0.087] | 95 |
| Rise in pills, rent-weighted $`\hat{x}^{R}`$ | 0.162 | [0.042, 0.288] | 95 |
| Deadweight loss per dollar of rent | 0.081 | | 95 |
| $`T^{*}`$ at $`\hat{x}^{R}`$, $`\sigma = 9`$, $`\rho`$ = 20% / 7% / 3% | 4.8 / 13.6 / 31.8 years | | |
| $`T^{*}`$ at mean $`\hat{x}`$, $`\sigma = 9`$, $`\rho`$ = 20% / 7% / 3% | 8.8 / 25.1 / 58.6 years | | |
| Median years from first NDA approval to generic entry year in Part D | 14 | IQR 11 to 15 | 91 |
| Kaplan-Meier median years from first NDA to first ANDA, 1985-2019 approvals | 14.5 | | 1,096 |

## Data

- **Medicare Part D Spending by Drug**, CMS, "Excel Reports including Historical Data RY26" (data.cms.gov),
  downloaded November 1, 2026. Nine releases (2016 to 2024), each with five calendar years of gross spending, dosage
  units and claims by brand name and generic name. Fetched by the script into `data/raw/partd/partd_release_YYYY.xlsx`
  (55 MB, not committed).
- **FDA Orange Book**, `data/raw/orange_book_20261101.zip` (products.txt dated October 9, 2026), committed.
- **Nordhaus's Table 1**, transcribed to `data/nordhaus_1967_table1.csv` from page 29 of the discussion paper.

## Method

Rules fixed before estimation:

- **Brand or generic.** A Part D product is a brand if the first word of its brand name differs from the first word of
  its generic name (Lyrica and pregabalin; not "Abacavir" and "abacavir sulfate").
- **Entry.** Molecule (generic name) goes generic in year $`E`$ if generic products are under 5% of its dosage units in
  $`E-2`$ and $`E-1`$, at least 5% in $`E`$ and at least 50% in $`E+1`$.
- **Sample.** At least half of the molecule's Orange Book listings (all applicants, current and discontinued) are
  oral tablets or capsules; at least $10 million of Part D spending in $`E-1`$. Listings are matched on ingredient and
  salt (first six letters of the first two words of each ingredient, with Part D abbreviations such as "hcl" expanded),
  falling back to the active moiety when no salt name matches. Of 171 entries, 48 fail the spending rule, 4 are not in
  the Orange Book and 24 are mainly other dosage forms, leaving 95.
- **One release per event.** Each entry is measured inside release $`E+2`$, which covers $`E-2`$ to $`E+2`$. For the same
  calendar year, the first and last releases agree within 5% on units for only 67% to 79% of molecules.
- **Controls.** Molecules in the same release with data in every window year, at least $10 million in $`E-1`$, mainly
  pills, generic share below 5% or above 50% throughout, and never an entry. The 10 whose change from $`E-2`$ to $`E-1`$ in
  the outcome is closest to the treated drug's are used, separately for quantity and price.

For drug $`i`$ and controls $`\mathcal{C}_i`$,

```math
\hat{\delta}_{ik} = \left(\ln Q_{i,E_i+k} - \ln Q_{i,E_i-1}\right)
  - \frac{1}{10}\sum_{j \in \mathcal{C}_i}\left(\ln Q_{j,E_i+k} - \ln Q_{j,E_i-1}\right)
```

```math
\hat{x}_i = e^{\hat{\delta}_{i2}} - 1, \qquad \hat{B}_i = 1 - e^{\hat{\delta}^{P}_{i2}}, \qquad
R_i = \hat{B}_i S_i, \qquad L_i = \tfrac{1}{2}\hat{x}_i R_i
```

where $`\hat{\delta}^{P}`$ is the same contrast in log gross spending per dosage unit and $`S_i`$ is Part D spending in
$`E_i - 1`$. The rent-weighted aggregate $`\hat{x}^{R} = \sum_i \hat{x}_i R_i / \sum_i R_i`$ equals twice the ratio of total
deadweight loss to total rent, the object in Nordhaus's trade-off. Intervals are percentile bootstraps over drugs
(2,000 draws, seed 1969), holding each drug's matched controls fixed. Quantity and price each have their own
10 controls. Nordhaus's optimal life is

```math
T^{*} = -\frac{1}{\rho}\ln\left(1 - \varphi^{*}\right), \qquad
\varphi^{*} = \frac{x + 1}{x\,(1 + \sigma/2) + 1}, \qquad x = dB
```

evaluated at $`\sigma \in \{4, 9, 20\}`$ (his central value and sensitivity cases) and $`\rho \in \{0.20, 0.07, 0.03\}`$
(his rate and the two real rates of OMB Circular A-4, 2003). For $`x \le 0`$ the optimum is unbounded.

**Extension.** Ingredient sets are keyed by the first six letters of the first word of each ingredient, so salts of
one active moiety share a key (sevelamer carbonate shares the 1998 approval of sevelamer hydrochloride). For each key
with a first NDA after 1981, time to first ANDA is censored at October 9, 2026 and summarized by Kaplan-Meier medians
in five-year approval cohorts. OTC-only listings are dropped, as are 23 keys whose first ANDA predates the first listed
NDA.

## Full test statistics

Event path, mean contrast over 95 drugs (standard error), from `results/event_path.csv`:

| Years from entry | −2 | 0 | 1 | 2 |
|---|---|---|---|---|
| Log price per pill | −0.003 (0.001) | −0.139 (0.019) | −0.629 (0.046) | −0.954 (0.060) |
| Log pills | 0.021 (0.011) | −0.066 (0.017) | −0.049 (0.029) | −0.027 (0.040) |

The mean log change in pills at year 2 is slightly negative while the mean of $`\hat{x}_i`$ is positive, because a few
large proportional rises dominate the mean of levels.

Robustness, from `results/robustness.csv`:

| Variant | N | Mean x | Median x | Rent-weighted x | Mean B |
|---|---|---|---|---|---|
| Primary | 95 | 0.048 | 0.020 | 0.162 | 0.552 |
| Prescriptions instead of pills | 95 | −0.009 | −0.099 | 0.007 | 0.552 |
| 25 matched controls | 95 | 0.040 | −0.005 | 0.169 | 0.551 |
| All eligible controls, unmatched | 95 | −0.125 | −0.167 | 0.057 | 0.465 |
| Every listing a tablet or capsule | 65 | 0.044 | −0.038 | 0.222 | 0.548 |
| At least $100M pre-entry spending | 63 | 0.012 | 0.010 | 0.163 | 0.639 |
| Every dosage form | 123 | 0.168 | 0.060 | 0.198 | 0.501 |
| Horizon E+1, matched on E−3 to E−1 | 81 | 0.031 | −0.029 | 0.062 | 0.423 |

In the horizon-1 design the placebo contrast at $`E-2`$ has mean 0.038 and median 0.018 (`results/pretrend_check_horizon1.csv`).
Unmatched controls make expiry look harmful to use, because drugs approaching expiry were already growing more slowly
than the average stable drug, which is why the primary design matches on pre-entry growth.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/patent_expiry.py      # Table 1, Part D test; downloads CMS file on first run
python src/effective_life.py     # Orange Book extension; reads results/events.csv
```

Python 3.12 or later. Both scripts print what they loaded, kept and dropped.

## References

- Arrow, K. J. (1962). Economic welfare and the allocation of resources for invention. In *The Rate and Direction of
  Inventive Activity*, Princeton University Press.
- Comanor, W. S. (1964). Research and competitive product differentiation in the pharmaceutical industry in the
  United States. *Economica* 31.
- Gilbert, R. & Shapiro, C. (1990). Optimal patent length and breadth. *RAND Journal of Economics* 21(1), 106-112.
- Klemperer, P. (1990). How broad should the scope of patent protection be? *RAND Journal of Economics* 21(1), 113-130.
- Nordhaus, W. D. (1967). The optimal life of a patent. Cowles Foundation Discussion Paper No. 241.
- Nordhaus, W. D. (1969). *Invention, Growth, and Welfare*. MIT Press.
- Office of Management and Budget (2003). Circular A-4, Regulatory Analysis.
- Scherer, F. M. (1972). Nordhaus' theory of optimal patent life: a geometric reinterpretation. *American Economic
  Review* 62(3), 422-427.
- Scotchmer, S. (1991). Standing on the shoulders of giants. *Journal of Economic Perspectives* 5(1), 29-41.
