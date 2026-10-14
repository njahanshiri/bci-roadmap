"""Summarize results and compare them with published state-of-the-art numbers (sota.csv)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent


def fold_means(res):
    """Mean over seeds for each fold, so the bootstrap resamples folds (subjects), not seeds."""
    return res.groupby(["dataset", "protocol", "model", "metric", "fold"], as_index=False)["value"].mean()


def bootstrap_ci(values, n=2000, seed=0):
    values = np.asarray(values, dtype=float)
    if len(values) < 2:
        return values.mean(), values.mean()
    rng = np.random.default_rng(seed)
    means = rng.choice(values, (n, len(values))).mean(1)
    return np.percentile(means, 2.5), np.percentile(means, 97.5)


def summarize(res):
    """mean ± std over seeds of the per-seed fold average."""
    per_seed = res.groupby(["dataset", "protocol", "model", "metric", "seed"])["value"].mean().reset_index()
    g = per_seed.groupby(["dataset", "protocol", "model", "metric"])["value"]
    return g.agg(["mean", "std", "count"]).reset_index().rename(columns={"count": "seeds"})


def compare(res, sota):
    fm = fold_means(res)
    rows = []
    for _, s in sota.iterrows():
        ours = fm[(fm.dataset == s.dataset) & (fm.protocol == s.protocol) & (fm.metric == s.metric)]
        if ours.empty:
            continue
        by_model = ours.groupby("model")["value"]
        model = s.our_model if isinstance(s.our_model, str) and s.our_model in by_model.groups else by_model.mean().idxmax()
        vals = by_model.get_group(model).values
        mean, (lo, hi) = vals.mean(), bootstrap_ci(vals)
        status = "within CI" if lo <= s.value <= hi else ("above SOTA" if lo > s.value else "below SOTA")
        rows.append(dict(dataset=s.dataset, protocol=s.protocol, metric=s.metric, sota_model=s.model,
                         sota=s.value, our_model=model, matched="same model" if model == s.our_model else "our best",
                         ours=round(mean, 4), ci=f"[{lo:.3f}, {hi:.3f}]", gap=round(mean - s.value, 4), status=status,
                         sota_flags=s.flags if isinstance(s.flags, str) else ""))
    return pd.DataFrame(rows)


def to_md(df):
    df = df.copy()
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if pd.isna(v) else (f"{v:.4f}" if isinstance(v, float) else str(v))
                                       for v in r.values) + " |")
    return "\n".join(lines)


def main(results_csv, out_md):
    results_csv, out_md = Path(results_csv), Path(out_md)
    if not results_csv.exists():
        print(f"no results at {results_csv}")
        return
    res = pd.read_csv(results_csv).dropna(subset=["value"])
    sota = pd.read_csv(ROOT / "sota.csv")
    summ = summarize(res)
    comp = compare(res, sota)
    parts = [f"# Benchmark summary\n\nResults: `{results_csv.name}` ({len(res)} rows). "
             "Values are fractions (0.85 = 85%). Our numbers: mean over folds, then mean ± std over seeds.\n",
             "## Comparison with published results\n",
             "Status uses a 95% bootstrap confidence interval over folds (subjects). "
             "`same model` compares like with like; `our best` compares our best model with the published number. "
             "Read `sota_flags` before drawing conclusions.\n",
             to_md(comp) if not comp.empty else "_No overlapping dataset/protocol/metric yet._", ""]
    for (ds, proto), g in summ.groupby(["dataset", "protocol"]):
        piv = g.assign(v=g["mean"].map("{:.4f}".format) + " ± " + g["std"].fillna(0).map("{:.4f}".format))
        piv = piv.pivot(index="model", columns="metric", values="v").reset_index()
        parts += [f"## {ds} — `{proto}`\n", to_md(piv), ""]
    out_md.write_text("\n".join(parts))
    comp.to_csv(out_md.with_suffix(".csv"), index=False)
    print(f"report written to {out_md}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "results" / "benchmark.csv",
         sys.argv[2] if len(sys.argv) > 2 else ROOT / "results" / "summary.md")
