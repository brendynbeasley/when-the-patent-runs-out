# Methods review of Nordhaus (1967/1969)

**Paper.** William D. Nordhaus, *Invention, Growth, and Welfare: A Theoretical Treatment of Technological Change*,
MIT Press, 1969 (MIT Monographs in Economics 10). The optimal-patent-life analysis reviewed here is the version
circulated as William D. Nordhaus, "The Optimal Life of a Patent," Cowles Foundation Discussion Paper No. 241, Yale
University, November 27, 1967 (38 pages).

**Statistical focus.** The optimal patent life of 8.7 years (rounded in the text to about nine) for a run-of-the-mill process
invention with demand elasticity 1 and a 5% cost reduction (Table 1), and the parameter values behind it
(sigma = 9, rho = 0.20).

**Review standard.** Internal consistency of the formal results, explicit statement of assumptions, transparency of
the numerical calibration, and the testability of the model's predictions. Current data-and-code norms are applied
only where they make sense for a 1967 theory paper.

**What was read.** The full text of Cowles Foundation Discussion Paper No. 241 (scanned PDF, 39 pages including the
cover sheet), from the Cowles Foundation website. I did not have access to the 1969 book; its bibliographic details
come from library catalog records. Everything below refers to the discussion paper, and page numbers are its own.

## Research design

A static partial-equilibrium welfare model in the tradition of Arrow (1962). A competitive industry with constant
unit cost and linear demand; an outside inventor chooses research spending R, which buys a unit cost reduction B(R),
and collects a per-unit royalty for T years. The planner chooses T to maximize discounted consumer plus producer
surplus net of research cost, subject to the inventor's profit-maximizing choice of R (equations 2 to 14). Extensions
treat drastic process inventions (section 2, equation 17), product inventions (equation 18), several sources of
spillover and rivalry (section 3), patent breadth (pp. 22-24) and fiscal incentives (section 5, equation 22). Section 4
gives numerical "estimates," which the author describes as somewhere between firm estimates and numerical examples.

## Sampling strategy

Not applicable. No data are sampled. Parameter values are chosen from the literature or by judgment.

## Sample size

Not applicable. The numerical tables are grids over chosen parameter values (Table 1 has 72 cells, 66 filled).

## Inclusion and exclusion criteria

The only exclusion rule is the classification of cells as "drastic" (marked n and omitted from Table 1, moved to
Table 2). The rule used in the tables is not the one stated in the text (see interpretation notes).

## Independent and dependent variables

The policy variable is patent life T (through phi = 1 - exp(-rho T)). Parameters are the demand elasticity d (or b),
the proportional cost reduction B, the curvature of the invention possibility function sigma = -B''B/B'^2, the
discount rate rho, and in section 5 the fiscal parameter k. The outcome is the welfare-maximizing T.

## Statistical methods

None in the inferential sense. The "statistics" are closed-form first-order conditions (equations 12 and 13) solved
numerically for each parameter combination. Second-order conditions are not checked; footnote 7 says they are
ignored, and footnote 27 suggests their failure may explain irregular results in Table 3.

## Reported effect sizes

The numerical optimal lives in Tables 1 to 4, summarized in the extraction table below. No uncertainty is attached to
them; sensitivity is shown by varying one parameter at a time.

## Confidence intervals

None reported, and none could be, since parameters are not estimated. The author calls the empirical results
fanciful (p. 26) and the run-of-the-mill conclusion highly uncertain (p. 28).

## P-values, if applicable

Not applicable.

## Missing data treatment

Not applicable. The omitted cells in Tables 1 to 3 are by design (classification or infeasibility), not missing data.

## Stated limitations

The paper is unusually candid. It lists as problems the assumption that the supply of inventions is unaffected by the
rate of invention, global and local spillovers (imitation and depletion effects), competing patents and the race to
the patent office, inventing around and the breadth of patents, technological progress during the patent's life,
risk aversion, and the static character of the model, which footnote 10 says produces unacceptable results when the
optimal life is infinite. It says sigma is probably impossible to estimate with much confidence and that the average B
had not been examined.

## Methods summary

A carefully derived theory result with a transparent closed form, followed by an explicitly speculative calibration.
The central formula (13) is internally consistent with its derivation, and the printed Table 1 can be recomputed
from equations (13) and (14) to within rounding (the repository's `results/table1_replication.csv` reproduces all
66 printed cells within 0.1 years). The weakest links are the parameter choices, two of which (B = 0.05 and sigma = 9)
rest on judgment, and a classification rule for drastic inventions that differs between text and tables.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Optimal life, run-of-the-mill process invention | 8.7 years (text rounds to about nine) | Table 1, p. 29; text p. 28 | T maximizing welfare at d = 1, B = 0.05, sigma = 9, rho = 0.20 | That 8.7 years is optimal for any real invention; all four inputs are assumed |
| Range of optimal lives at d = 1 | 27 years (B = 0.001) to 1.5 years (B = 1.0) | Text p. 28 | How T falls with invention size | Table 1 stops at B = 0.90 (1.9 years); the 1.5-year figure is not in Table 1 |
| Sensitivity to sigma | 5.6 years (sigma = 20), 12.2 years (sigma = 4) | Text p. 28 | Effect of research curvature on T at d = 1, B = 0.05 | Which sigma is right |
| Curvature parameter | sigma = 9 (alpha = 0.10) | Equation (19), p. 27; footnote 24 | Elasticity of cost reduction with respect to research, from the author's dissertation | An estimate for any specific industry; no standard error |
| Typical cost reduction | B = 0.05 | p. 27 | Assumed average invention | Any measurement; the paper says no examination exists |
| Demand elasticity | d = 1.0 | p. 27 | Assumed average elasticity | Elasticity for any market |
| Discount rate | rho = 0.20 | p. 28, footnote 26 | Social rate of return, from 1960s capital studies | That this is the right rate for intergenerational welfare |
| Optimal life, drastic process inventions | 1.0 to 1.9 years (most cells 1.4 to 1.5) | Table 2, p. 30; text p. 32 | T under equation (17) with sigma = 9, rho = 0.20 | Robustness; text calls it about one-tenth of actual life |
| Optimal life, product inventions | 0 years to unbounded, irregular | Table 3, p. 31; footnote 27 | T under equation (18) | A usable rule; author suggests second-order conditions may fail |
| Fiscal parameter for corporations | k = 1.20 (delta = -0.48, gamma = -0.58) | p. 34 | Effect of tax treatment of research on the inventor's return | Current tax law |
| Optimal life with fiscal incentives | 6.2 years (k = 1.2), 3.1 years (k = 2.0), at b = 1 | Table 4, p. 35 | T under equation (22) | The size of actual research subsidies |
| Risk premium case | about 30 years for B = 0.05 when rho*/rho = 2 | Footnote 30, p. 36 | T when inventors demand twice the social return | The actual risk premium |

## Interpretation notes

- The tables classify an invention as drastic when B > d (stated in the notes to Table 2), while the text defines a
  drastic invention as one where output more than doubles (pp. 3 and 10), which with the paper's normalization means
  dB > 1. The six omitted cells of Table 1 have dB well below 1 and 11 printed cells have dB above 1. This is a
  reporting inconsistency; it does not affect the 8.7-year headline cell.
- Equation (13) depends on d and B only through their product. Table 1 is therefore a one-dimensional function of dB
  displayed as a two-dimensional grid, which the paper does not point out. It means the model's whole empirical
  content, given sigma and rho, is the proportional output response at expiry, which is measurable.
- On p. 6 the definition is printed as phi(T) = 1 - e^(rho T); the derivation and equation (14) require
  1 - e^(-rho T). This is a typographical slip, not an error in the results.
- The notes to Table 2 (p. 30) say its values come from equation (18), but the text (p. 14) assigns drastic process
  inventions to equation (17) and product inventions to equation (18), and the notes to Table 3 also cite (18). The
  equation number (19) is also used twice, for sigma on p. 27 and for the fiscal Lagrangean on p. 33. Both are
  numbering slips in a preliminary paper.
- The 17-year comparison is with the statutory term, not with effective market life, which for many products is
  shorter. Footnote 17 notes this for pharmaceuticals, citing Comanor (1964).
- The welfare criterion is unweighted surplus, valid under constant marginal utility of income (footnote 6).

## Unanswered questions

- How sensitive is the optimal life to the joint uncertainty in sigma, B and rho, rather than one parameter at a time?
- Do the second-order conditions hold at the reported optima, particularly in Tables 3 and 4?
- How would the numbers change if the 1969 book revised the calibration? The discussion paper is preliminary by its
  own cover note.
- What value of sigma do modern estimates of the responsiveness of research to expected market size imply?
- How should the run-of-the-mill formula be applied to product inventions whose price under the patent is set by
  monopoly rather than by the old technology's cost?

## Items requiring expert verification

- Whether Table 1 and the 8.7-year figure appear unchanged in Chapter 5 (or wherever the analysis sits) of the 1969
  book, which I did not read.
- Whether the B > d classification in the tables reflects a different normalization intended by the author rather
  than an inconsistency.
- The provenance of alpha = 0.10, which cites the author's unpublished 1967 MIT dissertation (section 3-C).
- Whether later published versions correct the sign of the exponent in the definition of phi.

## Relation to the modern rerun

This repository does not reproduce the paper's results from data, because the paper has no data. It recomputes Table
1 from the paper's own equations and then supplies the one input the formula needs from observation, the output
response at patent expiry, using Medicare Part D records for 95 drugs. That exercise measures a parameter Nordhaus
had to assume; it does not test his model's assumptions about research behavior, which remain as he left them.
