"""Nordhaus (1967/1969) optimal patent life, replicated and then tested at real patent expiries.

Part 1 recomputes Nordhaus's Table 1 (optimal life of a patent for run-of-the-mill process
inventions) from his equations (13) and (14) and compares every cell with the printed value.

Part 2 measures the one number his formula needs from the world, the proportional rise in
output when a patent ends (x = d * B), at generic entries in Medicare Part D from 2014 to 2022,
and converts it into an optimal patent life. Each entry is measured inside a single CMS release
(each release covers five calendar years), so that changes in how CMS counts a drug between
releases cannot masquerade as a change in use.

Run from the repository root:
    python src/patent_expiry.py
The first run downloads the CMS historical Part D file (55 MB) into data/raw/partd/.
Other inputs are committed in data/. Outputs go to results/.
"""

import io
import re
import urllib.request
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PARTD = RAW / "partd"
OUT = ROOT / "results"
PARTD_URL = ("https://data.cms.gov/sites/default/files/2026-06/"
             "Medicare%20Part%20D%20Spending%20by%20Drug-Excel%20Reports%20including%20Historical%20Data%20RY26.zip")

# Nordhaus's own parameter values (CFDP 241, pp. 27-28): sigma = (1 - alpha)/alpha with alpha = 0.10,
# and a 20% social discount rate. Alternatives: his sensitivity values for sigma (4 and 20) and the
# 7% and 3% real rates of OMB Circular A-4 (2003).
SIGMA = 9.0
RHO = 0.20
SIGMAS = [4.0, 9.0, 20.0]
RHOS = [0.20, 0.07, 0.03]

# Event rules, fixed before estimating: a molecule "goes generic" in year E when generic products are
# under 5% of its Part D dosage units in E-2 and E-1, at least 5% in E, and at least 50% in E+1.
PRE_MAX_GSHARE = 0.05
ENTRY_MIN_GSHARE = 0.05
POST_MIN_GSHARE = 0.50
MIN_SPEND = 10e6          # Part D gross spending in E-1, dollars; drops tiny products
RELEASES = range(2016, 2025)   # CMS release years; release Y covers calendar years Y-4 to Y
SOLID_SHARE = 0.5         # at least half of the molecule's Orange Book listings are oral tablets/capsules,
                          # so that a Part D "dosage unit" is mostly a pill
K_NEIGHBORS = 10          # controls matched on the outcome's own pre-entry change
N_BOOT = 2000
SEED = 1969


# ----------------------------------------------------------------------------- Nordhaus's formula
def optimal_life(x, sigma=SIGMA, rho=RHO):
    """Equations (13)-(14): phi = (x+1)/(x(1+sigma/2)+1), T = -ln(1-phi)/rho, where x = d*B."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        one_minus_phi = (x * sigma / 2) / (x * (1 + sigma / 2) + 1)
        t = -np.log(one_minus_phi) / rho
    return np.where(x > 0, t, np.inf)


def replicate_table1():
    printed = pd.read_csv(ROOT / "data" / "nordhaus_1967_table1.csv")
    rows = []
    for _, r in printed.iterrows():
        for col in printed.columns[1:]:
            b = float(col.split("_")[1])
            p = r[col]
            rows.append(dict(d=r.d, B=b, x=r.d * b, T_printed=None if p == "n" else float(p),
                             T_rerun=round(float(optimal_life(r.d * b)), 2),
                             drastic_by_text_rule=r.d * b > 1, drastic_by_table_rule=b > r.d))
    t1 = pd.DataFrame(rows)
    t1["diff"] = t1.T_rerun - t1.T_printed
    t1.to_csv(OUT / "table1_replication.csv", index=False)
    shown = t1.dropna(subset=["T_printed"])
    print(f"Table 1: {len(shown)} printed cells, {len(t1) - len(shown)} marked 'n'. "
          f"Max |rerun - printed| = {shown['diff'].abs().max():.2f} years; "
          f"cells off by more than 0.1: {(shown['diff'].abs() > 0.1 + 1e-9).sum()}")
    sens = pd.DataFrame([dict(case=f"d=1, B=0.05, sigma={s:g}", T_rerun=round(float(optimal_life(0.05, s)), 2))
                         for s in SIGMAS])
    sens["T_printed"] = [12.2, 8.7, 5.6]   # CFDP 241, p. 28 (sigma = 4 and 20) and Table 1 (sigma = 9)
    sens.to_csv(OUT / "table1_sigma_check.csv", index=False)
    print(sens.to_string(index=False))


# ----------------------------------------------------------------------------- Part D releases
def fetch_partd():
    if PARTD.exists() and len(list(PARTD.glob("*.xlsx"))) == len(RELEASES):
        return
    PARTD.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {PARTD_URL}")
    data = urllib.request.urlopen(PARTD_URL, timeout=300).read()
    with zipfile.ZipFile(io.BytesIO(data)) as outer:
        for name in outer.namelist():
            year = re.search(r"DYT(\d{4})", name).group(1)
            with zipfile.ZipFile(io.BytesIO(outer.read(name))) as inner:
                xl = [n for n in inner.namelist() if n.endswith(".xlsx")][0]
                (PARTD / f"partd_release_{year}.xlsx").write_bytes(inner.read(xl))
    print(f"Saved {len(list(PARTD.glob('*.xlsx')))} release files to data/raw/partd/")


def first_word(s):
    w = re.findall(r"[a-z]+", str(s).lower())
    return w[0] if w else ""


def read_release(year):
    """One release's 'Spending & Utilization' sheet, reshaped to brand x generic x calendar year."""
    df = pd.read_excel(PARTD / f"partd_release_{year}.xlsx", sheet_name=1, header=None, engine="openpyxl")
    hdr = df.index[df.iloc[:, 0].astype(str).str.strip() == "Brand Name"][0]
    labels = df.iloc[hdr].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
    body = df.iloc[hdr + 1:]
    starts = [(i, int(re.search(r"(\d{4})", v).group(1))) for i, v in enumerate(df.iloc[hdr - 1])
              if isinstance(v, str) and "Calendar Year" in v]
    out = []
    for j, (i, cal) in enumerate(starts):
        end = starts[j + 1][0] if j + 1 < len(starts) else len(labels)
        blk = body.iloc[:, i:end]
        blk.columns = labels[i:end]
        out.append(pd.DataFrame({
            "brand": body.iloc[:, 0].astype(str).str.strip(), "generic": body.iloc[:, 1].astype(str).str.strip(),
            "year": cal, "spend": pd.to_numeric(blk["Total Spending"], errors="coerce"),
            "units": pd.to_numeric(blk["Total Dosage Units"], errors="coerce"),
            "claims": pd.to_numeric(blk["Total Claims"], errors="coerce")}))
    p = pd.concat(out, ignore_index=True)
    n0 = len(p)
    p = p[p.units > 0].copy()
    p["mol"] = p.generic.str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    p["is_brand"] = [first_word(x) != first_word(y) for x, y in zip(p.brand, p.generic)]
    print(f"  release {year}: {n0:,} product-years, kept {len(p):,} with positive units "
          f"(dropped {n0 - len(p):,} blank or suppressed), {p.mol.nunique():,} molecules, "
          f"years {p.year.min()}-{p.year.max()}")
    return p


def brand_makers(year):
    """Brand name -> manufacturer, from the release's 'Manufacturer Summary' sheet."""
    df = pd.read_excel(PARTD / f"partd_release_{year}.xlsx", sheet_name=2, header=None, engine="openpyxl")
    df = df.iloc[:, [0, 2]].dropna().astype(str).apply(lambda c: c.str.strip())
    df = df[df.iloc[:, 1] != "Manufacturer"]
    return df.groupby(df.columns[0])[df.columns[1]].agg(lambda m: "; ".join(sorted(set(m))))


def wide_tables(p):
    m = p.groupby(["mol", "year", "is_brand"])[["spend", "units", "claims"]].sum().unstack("is_brand", fill_value=0)
    tot = m.T.groupby(level=0).sum().T
    W = {v: tot[v].unstack("year").where(lambda t: t > 0) for v in ["spend", "units", "claims"]}
    W["gshare"] = (m["units"][False] / tot["units"]).unstack("year")
    W["lnq"] = np.log(W["units"])
    W["lnc"] = np.log(W["claims"])
    W["lnp"] = np.log(W["spend"] / W["units"])
    return W


def ingredient_key(parts):
    """Active moiety: first six letters of the first word of each ingredient (salts merged)."""
    return frozenset(w[0][:6] for c in parts if (w := re.findall(r"[a-z]+", c.lower())))


SALT_ABBR = {"hcl": "hydrochloride", "hbr": "hydrobromide", "mag": "magnesium", "bes": "besylate",
             "med": "medoxomil", "sod": "sodium"}   # Part D abbreviations of Orange Book salt names


def salt_key(parts):
    """Ingredient with its salt: first six letters of the first two words of each ingredient."""
    out = []
    for c in parts:
        w = [SALT_ABBR.get(x, x) for x in re.findall(r"[a-z]+", c.lower())]
        if w:
            out.append((w[0][:6], w[1][:6] if len(w) > 1 else ""))
    return frozenset(out)


def orange_book_solid_share():
    """Function giving the share of a Part D molecule's Orange Book listings (all applicants, current
    and discontinued) that are oral tablets or capsules. It matches on ingredient and salt first, so that
    a salt sold only as a patch (diclofenac epolamine) or a base sold only as a patch (rivastigmine) is not
    credited with the tablets of its sister salts, and falls back to the active moiety when the salt
    name does not match. Returns None for molecules not in the Orange Book."""
    with zipfile.ZipFile(RAW / "orange_book_20261101.zip") as z:
        ob = pd.read_csv(z.open("products.txt"), sep="~", dtype=str)
    ob["solid"] = ob["DF;Route"].str.match(r"^(TABLET|CAPSULE)[^;]*;ORAL")
    by_salt = ob.groupby([salt_key(s.split(";")) for s in ob.Ingredient]).solid.mean()
    by_moiety = ob.groupby([ingredient_key(s.split(";")) for s in ob.Ingredient]).solid.mean()

    def lookup(mol):
        parts = mol.split("/")
        s = by_salt.get(salt_key(parts))
        return s if s is not None else by_moiety.get(ingredient_key(parts))
    return lookup


# ----------------------------------------------------------------------------- events and matching
def find_events(W, E, share):
    """Molecules in this release that go generic in year E (needs E-2 to E+2 in the release)."""
    yrs = list(range(E - 2, E + 3))
    gs = W["gshare"].reindex(columns=yrs)
    full = W["units"].reindex(columns=yrs).notna().all(axis=1)
    hit = (full & (gs[E - 2] < PRE_MAX_GSHARE) & (gs[E - 1] < PRE_MAX_GSHARE) & (gs[E] >= ENTRY_MIN_GSHARE)
           & (gs[E + 1] >= POST_MIN_GSHARE))
    ev = pd.DataFrame({"mol": gs.index[hit], "E": E})
    ev["spend_pre"] = W["spend"].loc[ev.mol, E - 1].values
    ev["solid"] = [share(m) for m in ev.mol]
    return ev


def controls(W, E, yrs, exclude, solid_ok):
    """Molecules present in every window year, over $10M in E-1, whose generic share stays on one side
    of the entry thresholds for the whole window, that never qualify as an entry, and (unless
    solid_ok is None) that are mainly pills."""
    U = W["units"].reindex(columns=yrs)
    gs = W["gshare"].reindex(columns=yrs)
    ok = U.notna().all(axis=1) & (W["spend"][E - 1] >= MIN_SPEND)
    ok &= (gs < PRE_MAX_GSHARE).all(axis=1) | (gs > POST_MIN_GSHARE).all(axis=1)
    if solid_ok is not None:
        ok &= W["units"].index.isin(list(solid_ok))
    return W["units"].index[ok].difference(list(exclude))


def matched_did(Ws, ev, var, exclude, solid_ok, horizon=2, pre=1, k_nn=K_NEIGHBORS, matched=True):
    """Per event, within release E+horizon: change in var from E-1 to E+k, minus the mean change of the
    k_nn control molecules whose change from E-1-pre to E-1 is closest to the treated molecule's."""
    rows = []
    for _, r in ev.iterrows():
        mol, E = r.mol, r.E
        W = Ws.get(E + horizon)
        yrs = list(range(E - 1 - pre, E + horizon + 1))
        if W is None or mol not in W["units"].index or W["units"].loc[mol].reindex(yrs).isna().any():
            continue
        X = W[var]
        C = controls(W, E, yrs, exclude, solid_ok)
        pre_c = X.loc[C, E - 1] - X.loc[C, E - 1 - pre]
        pre_t = X.loc[mol, E - 1] - X.loc[mol, E - 1 - pre]
        nn = (pre_c - pre_t).abs().nsmallest(k_nn).index if matched else C
        for y in yrs:
            if y == E - 1:
                continue
            dt = X.loc[mol, y] - X.loc[mol, E - 1]
            dc = (X.loc[nn, y] - X.loc[nn, E - 1]).mean()
            rows.append(dict(mol=mol, E=E, var=var, k=y - E, treated=dt, control=dc, did=dt - dc, n_controls=len(nn)))
    return pd.DataFrame(rows)


def summarize_x(q, p, spend):
    """x = proportional output rise at expiry, B = proportional price fall, both relative to controls."""
    x, B = np.exp(q) - 1, 1 - np.exp(p)
    rent = B * spend
    return dict(x_mean=x.mean(), x_median=np.median(x), x_rent_weighted=(x * rent).sum() / rent.sum(),
                B_mean=B.mean(), B_spend_weighted=(B * spend).sum() / spend.sum())


def run_variant(Ws, ev, exclude, solid_ok, qvar="lnq", horizon=2, pre=1, k_nn=K_NEIGHBORS, matched=True):
    q = matched_did(Ws, ev, qvar, exclude, solid_ok, horizon, pre, k_nn, matched)
    p = matched_did(Ws, ev, "lnp", exclude, solid_ok, horizon, pre, k_nn, matched)
    qh = q[q.k == horizon].set_index("mol").did
    ph = p[p.k == horizon].set_index("mol").did
    keep = ev[ev.mol.isin(qh.index) & ev.mol.isin(ph.index)].reset_index(drop=True)
    s = summarize_x(qh.reindex(keep.mol).values, ph.reindex(keep.mol).values, keep.spend_pre.values)
    return q, p, keep, s


def main():
    OUT.mkdir(exist_ok=True)
    print("== Part 1: Nordhaus Table 1")
    replicate_table1()

    print("\n== Part 2: generic entry in Medicare Part D")
    fetch_partd()
    panels = {y: read_release(y) for y in RELEASES}
    Ws = {y: wide_tables(p) for y, p in panels.items()}
    agree = []
    for cal in range(2016, 2021):   # each calendar year appears in five releases; compare first and last
        a, b = Ws[cal]["units"][cal], Ws[cal + 4]["units"][cal]
        gap = np.log(b / a).dropna().abs()
        agree.append(dict(calendar_year=cal, first_release=cal, last_release=cal + 4, molecules_in_both=len(gap),
                          share_within_1pct=(gap < 0.01).mean(), share_within_5pct=(gap < 0.05).mean(),
                          total_spend_first=Ws[cal]["spend"][cal].sum(), total_spend_last=Ws[cal + 4]["spend"][cal].sum()))
    pd.DataFrame(agree).to_csv(OUT / "partd_release_agreement.csv", index=False)
    share = orange_book_solid_share()
    solid = {m: share(m) for W in Ws.values() for m in W["units"].index}
    solid_ok = {m for m, s in solid.items() if s is not None and s >= SOLID_SHARE}
    print(f"Molecules across releases: {len(solid):,}; in the Orange Book: "
          f"{sum(s is not None for s in solid.values()):,}; mainly pills: {len(solid_ok):,}")

    ev_all = pd.concat([find_events(Ws[y], y - 2, share) for y in RELEASES], ignore_index=True)
    ev_all = ev_all.sort_values("E").drop_duplicates("mol").reset_index(drop=True)
    exclude = set(ev_all.mol)
    print(f"Generic entries meeting the share rules, 2014-2022: {len(ev_all)}")
    big = ev_all.spend_pre >= MIN_SPEND
    pill = ev_all.solid >= SOLID_SHARE
    ev = ev_all[big & pill].reset_index(drop=True)
    print(f"Kept {len(ev)}: dropped {(~big).sum()} under $10M, {(big & ev_all.solid.isna()).sum()} not in the "
          f"Orange Book, {(big & (ev_all.solid < SOLID_SHARE)).sum()} mainly non-pill forms")

    q, pr, ev, head = run_variant(Ws, ev, exclude, solid_ok)
    path = pd.concat([q, pr])
    path.to_csv(OUT / "event_did_by_event.csv", index=False)
    agg = path.groupby(["var", "k"]).agg(treated=("treated", "mean"), control=("control", "mean"),
                                         did=("did", "mean"), did_median=("did", "median"),
                                         sd=("did", "std"), n=("did", "size")).reset_index()
    agg["se"] = agg.sd / np.sqrt(agg.n)
    agg.to_csv(OUT / "event_path.csv", index=False)
    print(agg.round(3).to_string(index=False))

    q2 = q[q.k == 2].set_index("mol").did.reindex(ev.mol).values
    p2 = pr[pr.k == 2].set_index("mol").did.reindex(ev.mol).values
    S = ev.spend_pre.values
    rng = np.random.default_rng(SEED)
    boots = pd.DataFrame([summarize_x(q2[i], p2[i], S[i])
                          for i in (rng.integers(0, len(ev), len(ev)) for _ in range(N_BOOT))])
    xs = pd.DataFrame([dict(statistic=s, estimate=head[s], ci_low=np.percentile(boots[s], 2.5),
                            ci_high=np.percentile(boots[s], 97.5), se_boot=boots[s].std(), n_events=len(ev))
                       for s in head])
    xs.to_csv(OUT / "headline_x.csv", index=False)
    print(xs.round(4).to_string(index=False))

    life = []
    for stat in ["x_mean", "x_median", "x_rent_weighted"]:
        r = xs.set_index("statistic").loc[stat]
        for s in SIGMAS:
            for rho in RHOS:
                life.append(dict(x_statistic=stat, sigma=s, rho=rho, x=r.estimate,
                                 T_star=float(optimal_life(r.estimate, s, rho)),
                                 T_at_x_ci_high=float(optimal_life(r.ci_high, s, rho)),
                                 T_at_x_ci_low=float(optimal_life(r.ci_low, s, rho))))
    life.append(dict(x_statistic="nordhaus_1967_typical", sigma=SIGMA, rho=RHO, x=0.05,
                     T_star=float(optimal_life(0.05)), T_at_x_ci_high=np.nan, T_at_x_ci_low=np.nan))
    pd.DataFrame(life).to_csv(OUT / "optimal_life.csv", index=False)

    # per-event table with names and dollars
    ev["x"], ev["B"] = np.exp(q2) - 1, 1 - np.exp(p2)
    ev["d_implied"] = ev.x / ev.B
    ev["rent_per_year"] = ev.B * ev.spend_pre
    ev["dwl_per_year"] = 0.5 * ev.x * ev.rent_per_year
    ev["T_star"] = optimal_life(ev.x.values)
    ev["T_star_rho07"] = optimal_life(ev.x.values, rho=0.07)
    names, makers, raw_q, raw_p, maker_tables = [], [], [], [], {}
    for m, e in zip(ev.mol, ev.E):
        p, W = panels[e + 2], Ws[e + 2]
        b = p[(p.mol == m) & p.is_brand & (p.year == e - 1)].sort_values("units")
        brand = b.brand.iloc[-1] if len(b) else ""
        if e + 2 not in maker_tables:
            maker_tables[e + 2] = brand_makers(e + 2)
        makers.append(maker_tables[e + 2].get(brand, ""))
        names.append(brand.replace("*", "").strip())
        raw_q.append(np.exp(W["lnq"].loc[m, e + 2] - W["lnq"].loc[m, e - 1]) - 1)
        raw_p.append(np.exp(W["lnp"].loc[m, e + 2] - W["lnp"].loc[m, e - 1]) - 1)
    ev["brand"], ev["maker"], ev["raw_units_change"], ev["raw_price_change"] = names, makers, raw_q, raw_p
    ev.drop(columns=["solid"]).sort_values("spend_pre", ascending=False).to_csv(OUT / "events.csv", index=False)
    pos = ev.dwl_per_year.clip(lower=0)
    tot = dict(events=len(ev), spend_pre=ev.spend_pre.sum(), rent=ev.rent_per_year.sum(), dwl=ev.dwl_per_year.sum(),
               dwl_per_dollar_rent=ev.dwl_per_year.sum() / ev.rent_per_year.sum(),
               share_x_positive=(ev.x > 0).mean(), share_x_below_10pct=(ev.x < 0.10).mean(),
               share_x_at_least_1=(ev.x >= 1).mean(),
               dwl_top2_share_of_positive=pos.nlargest(2).sum() / pos.sum(),
               dwl_top5_share_of_positive=pos.nlargest(5).sum() / pos.sum())
    pd.DataFrame([tot]).to_csv(OUT / "dollars_summary.csv", index=False)
    print(pd.DataFrame([tot]).round(3).to_string(index=False))

    # robustness
    rob = [dict(variant="primary: pills, 10 matched controls, pills dispensed, E+2", n=len(ev), **head)]

    def add(label, events, ok=solid_ok, **kw):
        _, _, kept, s = run_variant(Ws, events, exclude, ok, **kw)
        rob.append(dict(variant=label, n=len(kept), **s))
    add("prescriptions (claims) instead of pills", ev, qvar="lnc")
    add("25 matched controls", ev, k_nn=25)
    add("all eligible controls, no matching", ev, matched=False)
    add("pills only (every listing a tablet or capsule)", ev[ev.solid == 1])
    add("events with at least $100M pre-entry spending", ev[ev.spend_pre >= 100e6])
    add("every event and control, any dosage form", ev_all[big], ok=None)
    add("horizon E+1 in release E+1, matched on E-3 to E-1", ev, horizon=1, pre=2)
    robust = pd.DataFrame(rob)
    robust.to_csv(OUT / "robustness.csv", index=False)
    print(robust.round(3).to_string(index=False))
    q1 = matched_did(Ws, ev, "lnq", exclude, solid_ok, horizon=1, pre=2)
    q1.groupby("k").did.agg(["mean", "median", "std", "size"]).to_csv(OUT / "pretrend_check_horizon1.csv")
    print("Horizon-1 design, pills, by year relative to entry:")
    print(q1.groupby("k").did.agg(["mean", "median", "size"]).round(3).to_string())

    make_figures(agg, xs, len(ev))


def make_figures(agg, xs, n_events):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for var, label, color in [("lnp", "Price per pill", "#b2182b"), ("lnq", "Pills dispensed", "#2166ac")]:
        a = agg[agg["var"] == var].set_index("k").reindex([-2, -1, 0, 1, 2]).fillna({"did": 0, "se": 0})
        y = (np.exp(a.did) - 1) * 100
        lo, hi = (np.exp(a.did - 1.96 * a.se) - 1) * 100, (np.exp(a.did + 1.96 * a.se) - 1) * 100
        ax.plot(a.index, y, marker="o", color=color, label=label)
        ax.fill_between(a.index, lo, hi, color=color, alpha=0.15)
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(-0.5, color="grey", ls=":", lw=0.8)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_xlabel("Years since generic entry (0 = first year generics reach 5% of pills)")
    ax.set_ylabel("Change since the year before entry, relative to\nmatched controls (%)")
    ax.set_title(f"When the patent runs out: Medicare Part D, {n_events} molecules, 2014-2022 entries")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "event_path.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = np.linspace(0.001, 0.6, 400)
    for rho, ls in zip(RHOS, ["-", "--", ":"]):
        ax.plot(x, optimal_life(x, SIGMA, rho), color="#333333", ls=ls, label=f"discount rate {rho:.0%}")
    ax.axhline(20, color="#b2182b", lw=0.8)
    ax.text(0.45, 21, "US statutory term, 20 years", color="#b2182b", fontsize=9)
    marks = xs.set_index("statistic").estimate
    for stat, lab, y0, dx, ha in [("x_mean", "average drug", 30, -0.004, "right"),
                                  ("x_rent_weighted", "rent-weighted", 15.5, 0.004, "left")]:
        if marks[stat] > 0:
            ax.axvline(marks[stat], color="#2166ac", lw=0.8)
            ax.text(marks[stat] + dx, y0, lab, color="#2166ac", fontsize=9, rotation=90, va="bottom", ha=ha)
    ax.axvline(0.05, color="#999999", lw=0.8)
    ax.text(0.054, 27, "Nordhaus 1967", color="#777777", fontsize=9, rotation=90, va="bottom")
    ax.set_ylim(0, 55)
    ax.set_xlabel("x = proportional rise in output when the patent ends")
    ax.set_ylabel("Optimal patent life (years)")
    ax.set_title("Nordhaus's optimal life as a function of x (sigma = 9)")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "optimal_life_curve.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
