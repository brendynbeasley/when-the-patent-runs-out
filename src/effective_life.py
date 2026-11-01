"""Extension: how long drug patents actually keep generics out, set against Nordhaus's optimum.

Nordhaus compared his optimal life with the statutory term. A drug's effective life is the time from
FDA approval of the brand to the first generic, which the Orange Book records for every approved
application, current or discontinued. This script measures it two ways:

  1. For every active ingredient (or combination) first approved under an NDA from 1985 to 2019,
     the years until the first ANDA (generic) approval, with Kaplan-Meier medians by cohort because
     many recent drugs have no generic yet.
  2. For the Part D generic entries studied in patent_expiry.py, the years from the first NDA
     approval of the active moiety to the entry year E, the first year generics reached 5% of the
     molecule's Part D pills.

Run from the repository root, after patent_expiry.py (it reads results/events.csv and
results/optimal_life.csv):
    python src/effective_life.py
"""

import re
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

OB_FILE_DATE = pd.Timestamp("2026-10-09")   # date stamped on products.txt in the downloaded zip
FIRST_COHORT, LAST_COHORT = 1985, 2019      # Hatch-Waxman (1984) created the modern ANDA route
COHORT_WIDTH = 5
HORIZONS = [10, 15, 20]


def ingredient_key(parts):
    """Same rule as patent_expiry.py: first six letters of the first word of each ingredient."""
    return frozenset(w[0][:6] for c in parts if (w := re.findall(r"[a-z]+", c.lower())))


def load_orange_book():
    with zipfile.ZipFile(RAW / "orange_book_20261101.zip") as z:
        ob = pd.read_csv(z.open("products.txt"), sep="~", dtype=str)
    n0 = len(ob)
    ob = ob[ob.Type.isin(["RX", "DISCN"])].copy()
    print(f"Orange Book products: {n0:,}; prescription or discontinued: {len(ob):,} (dropped {n0 - len(ob):,} OTC)")
    ob["key"] = [ingredient_key(s.split(";")) for s in ob.Ingredient]
    ob["date"] = pd.to_datetime(ob.Approval_Date, format="%b %d, %Y", errors="coerce")
    ob["pre1982"] = ob.Approval_Date.str.contains("Prior", na=False)
    return ob


def first_approvals(ob):
    nda = ob[ob.Appl_Type == "N"].groupby("key").agg(nda_date=("date", "min"), nda_pre1982=("pre1982", "max"),
                                                     trade_name=("Trade_Name", "first"))
    anda = ob[ob.Appl_Type == "A"].groupby("key").agg(anda_date=("date", "min"), anda_pre1982=("pre1982", "max"))
    d = nda.join(anda, how="left")
    n0 = len(d)
    d = d[~d.nda_pre1982 & d.nda_date.notna()].copy()
    print(f"Ingredient sets with an NDA: {n0:,}; kept {len(d):,} first approved after 1981")
    anda_pre = d.anda_pre1982.fillna(False).astype(bool)
    d["generic"] = d.anda_date.notna()
    end = d.anda_date.where(d.generic, OB_FILE_DATE)
    d["years"] = (end - d.nda_date).dt.days / 365.25
    bad = (d.years < 0) | anda_pre
    print(f"Dropped {bad.sum()} sets whose first ANDA predates the first listed NDA")
    d = d[~bad]
    d["nda_year"] = d.nda_date.dt.year
    return d


def kaplan_meier(t, event):
    """Survival curve S(t) for 'still no generic', as a DataFrame of (t, S)."""
    df = pd.DataFrame({"t": t, "e": event.astype(int)}).sort_values("t")
    at_risk, s, rows = len(df), 1.0, [(0.0, 1.0)]
    for tt, g in df.groupby("t"):
        if g.e.sum():
            s *= 1 - g.e.sum() / at_risk
            rows.append((tt, s))
        at_risk -= len(g)
    return pd.DataFrame(rows, columns=["t", "S"])


def km_at(curve, h):
    return curve.S[curve.t <= h].iloc[-1]


def km_median(curve):
    below = curve[curve.S <= 0.5]
    return below.t.iloc[0] if len(below) else np.inf


def cohort_table(d):
    d = d[(d.nda_year >= FIRST_COHORT) & (d.nda_year <= LAST_COHORT)].copy()
    d["cohort"] = (d.nda_year - FIRST_COHORT) // COHORT_WIDTH * COHORT_WIDTH + FIRST_COHORT
    rows, curves = [], {}
    for c, g in d.groupby("cohort"):
        curve = kaplan_meier(g.years.values, g.generic.values)
        curves[c] = curve
        row = dict(cohort=f"{c}-{c + COHORT_WIDTH - 1}", ingredient_sets=len(g), with_generic=int(g.generic.sum()),
                   km_median_years=km_median(curve))
        for h in HORIZONS:
            followed = (OB_FILE_DATE.year - (c + COHORT_WIDTH - 1)) >= h
            row[f"share_generic_by_{h}y"] = 1 - km_at(curve, h) if followed else np.nan
        rows.append(row)
    allc = kaplan_meier(d.years.values, d.generic.values)
    rows.append(dict(cohort=f"{FIRST_COHORT}-{LAST_COHORT}", ingredient_sets=len(d), with_generic=int(d.generic.sum()),
                     km_median_years=km_median(allc),
                     **{f"share_generic_by_{h}y": 1 - km_at(allc, h) for h in HORIZONS}))
    tab = pd.DataFrame(rows)
    tab.to_csv(OUT / "time_to_generic_by_cohort.csv", index=False)
    print(tab.round(3).to_string(index=False))
    return curves, allc


def event_exclusivity(d):
    ev = pd.read_csv(OUT / "events.csv")
    ev["key"] = [ingredient_key(m.split("/")) for m in ev.mol]
    ev = ev.merge(d[["nda_date", "trade_name", "anda_date"]], left_on="key", right_index=True, how="left")
    n0 = len(ev)
    print(f"Part D events: {n0}; with a post-1981 first NDA in the Orange Book: {ev.nda_date.notna().sum()}")
    ev["nda_year"] = ev.nda_date.dt.year
    ev["years_to_partd_entry"] = ev.E - ev.nda_year
    ev["years_to_first_anda"] = (ev.anda_date - ev.nda_date).dt.days / 365.25
    keep = ["brand", "mol", "E", "nda_year", "years_to_partd_entry", "years_to_first_anda", "spend_pre", "x", "T_star"]
    ev[keep].to_csv(OUT / "events_exclusivity.csv", index=False)
    ok = ev.dropna(subset=["years_to_partd_entry"])
    life = pd.read_csv(OUT / "optimal_life.csv")
    rw = life[(life.x_statistic == "x_rent_weighted") & (life.sigma == 9)].set_index("rho").T_star
    w = ok.spend_pre
    summ = dict(events_matched=len(ok),
                median_years_to_partd_entry=ok.years_to_partd_entry.median(),
                mean_years_to_partd_entry=ok.years_to_partd_entry.mean(),
                spend_weighted_mean_years=np.average(ok.years_to_partd_entry, weights=w),
                p25=ok.years_to_partd_entry.quantile(0.25), p75=ok.years_to_partd_entry.quantile(0.75),
                median_years_to_first_anda=ok.years_to_first_anda.median(),
                T_star_rho20=rw.get(0.20), T_star_rho07=rw.get(0.07), T_star_rho03=rw.get(0.03))
    pd.DataFrame([summ]).to_csv(OUT / "events_exclusivity_summary.csv", index=False)
    print(pd.DataFrame([summ]).round(2).to_string(index=False))
    return ok, rw


def make_figure(curves, ok, rw):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    ax = axes[0]
    for c, color in zip([1985, 1995, 2005, 2015], ["#999999", "#4393c3", "#2166ac", "#b2182b"]):
        cv = curves[c]
        ax.step(cv.t, (1 - cv.S) * 100, where="post", color=color, label=f"first approved {c}-{c + 4}")
    ax.set_xlim(0, 30)
    ax.set_xlabel("Years since the brand's first FDA approval")
    ax.set_ylabel("Share with an approved generic (%)")
    ax.set_title("Orange Book, every ingredient set (Kaplan-Meier)")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    ax.hist(ok.years_to_partd_entry, bins=range(0, 32, 2), color="#cccccc", edgecolor="white")
    for rho, ls in [(0.20, "-"), (0.07, "--"), (0.03, ":")]:
        t = rw.get(rho)
        if np.isfinite(t):
            ax.axvline(t, color="#2166ac", ls=ls, label=f"Nordhaus optimum, {rho:.0%} discount ({t:.0f} y)")
    ax.axvline(ok.years_to_partd_entry.median(), color="#b2182b", label="median actual")
    ax.set_xlabel("Years from first FDA approval to generic entry in Medicare")
    ax.set_ylabel("Molecules")
    ax.set_title(f"The {len(ok)} Part D entries matched to an NDA, {ok.E.min()}-{ok.E.max()}")
    ax.set_ylim(0, 40)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "effective_life.png", dpi=150)
    plt.close(fig)


def main():
    ob = load_orange_book()
    d = first_approvals(ob)
    curves, _ = cohort_table(d)
    ok, rw = event_exclusivity(d)
    make_figure(curves, ok, rw)


if __name__ == "__main__":
    main()
