#!/usr/bin/env python3
"""usage: render-status.py [state.json] [status.md]

Renders the EM's state.json (default .agentic-team/state.json) into the markdown progress
dashboard (default .agentic-team/status.md). A pure function of the state: the EM reruns it
after every state change, and `watch cat .agentic-team/status.md` gives a live board.
"""
import json, os, sys

state_path = sys.argv[1] if len(sys.argv) > 1 else ".agentic-team/state.json"
out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(state_path) or ".", "status.md")
S = json.load(open(state_path))
PHASES = ["queued", "prd-gap", "spec-review", "architecture", "sop-review", "planned", "engineering", "verifying", "gap", "pr-open"]

def g(d, k, default="-"):
    v = d.get(k)
    return default if v in (None, "", []) else v

def bar(done, total, width=10):
    done, total = int(done or 0), int(total or 0)
    if total <= 0:
        return "-"
    n = round(width * done / total)
    return f"[{'#' * n}{'.' * (width - n)}] {done}/{total} ({100 * done // total}%)"

def pipeline(phase):
    return " → ".join(f"**[{p}]**" if p == phase else p for p in PHASES)

prds, lanes = S.get("prds", {}), S.get("lanes", {})
researchers, requests = S.get("researchers", {}), S.get("requests", {})
busy = lambda d: sum(1 for v in d.values() if v.get("state") == "working")
L = ["# Status", "",
     f"Updated {g(S, 'updated')} · engineering lanes {busy(lanes)}/{len(lanes)} busy"
     + (f" · researcher lanes {busy(researchers)}/{len(researchers)} busy" if researchers else ""), ""]

need = [f"- **{i}**: {g(p, 'waiting_for')}" for i, p in sorted(prds.items()) if p.get("waiting_on") == "you"]
need += [f"- **Lane {i}** ({g(v, 'prd')}) is {v['state']}: {g(v, 'note')}" for i, v in sorted(lanes.items()) if v.get("state") in ("blocked", "failed")]
need += [f"- **Researcher {i}** ({g(v, 'request')}) is {v['state']}: {g(v, 'note')}" for i, v in sorted(researchers.items()) if v.get("state") in ("blocked", "failed")]
L += ["## Needs you", ""] + (need or ["Nothing. The team is running."]) + [""]

L += ["## PRDs", ""]
if prds:
    L += ["| PRD | Title | Phase | Progress | Waiting on | Updated |", "|---|---|---|---|---|---|"]
    for i, p in sorted(prds.items()):
        st, w = p.get("steps") or {}, p.get("wave") or {}
        prog = bar(st.get("done"), st.get("total")) + (f" · wave {w.get('current')}/{w.get('total')}" if w else "") if st else "-"
        L.append(f"| {i} | {g(p, 'title')} | {g(p, 'phase')} | {prog} | {g(p, 'waiting_on', 'nothing')} | {g(p, 'updated')} |")
    for i, p in sorted(prds.items()):
        L += ["", f"### {i}: {g(p, 'title', '')}".rstrip(": "), "", pipeline(p.get("phase")), ""]
        if p.get("waiting_for"):
            L.append(f"- Waiting for: {p['waiting_for']}")
        if p.get("gap_round") is not None:
            L.append(f"- PRD gap analysis: round {p['gap_round']}, open gaps {g(p, 'open_gaps', 0)}")
        for k, label in (("spec", "Spec"), ("sop", "SOP"), ("plan", "Plan")):
            if p.get(k):
                L.append(f"- {label}: `{p[k]}`")
        if p.get("steps"):
            L.append(f"- Steps: {bar(p['steps'].get('done'), p['steps'].get('total'))}")
        if p.get("wave"):
            L.append(f"- Wave: {p['wave'].get('current')} of {p['wave'].get('total')}")
        for li, v in sorted(lanes.items()):
            if v.get("prd") == i and v.get("state") != "idle":
                L.append(f"- Lane {li} ({v['state']}): steps {g(v, 'unit')}, round {g(v, 'round')}/3")
        if p.get("gap_cycles"):
            L.append(f"- Requirement Gap cycles: {p['gap_cycles']}/2")
        if p.get("pr"):
            L.append(f"- PR: {p['pr']}")
else:
    L.append("No PRDs yet.")

L += ["", "## Engineering lanes", "", "| Lane | State | PRD | Steps | Round | Worktree |", "|---|---|---|---|---|---|"]
L += [f"| {i} | {g(v, 'state')} | {g(v, 'prd')} | {g(v, 'unit')} | {g(v, 'round')} | {g(v, 'worktree')} |" for i, v in sorted(lanes.items())]

if researchers or requests:
    L += ["", "## Research", "", "| Lane | State | Request | Stage |", "|---|---|---|---|"]
    L += [f"| {i} | {g(v, 'state')} | {g(v, 'request')} | {g(v, 'stage')} |" for i, v in sorted(researchers.items())]
    L += ["", "| Request | Phase | Lane | Artifact |", "|---|---|---|---|"]
    L += [f"| {i} | {g(v, 'phase')} | {g(v, 'lane')} | {g(v, 'artifact')} |" for i, v in sorted(requests.items())]

L += ["", "## Recent events", ""]
ev = S.get("events", [])[-20:][::-1]
L += [f"- {e.get('ts', '')} {('[' + e['prd'] + '] ') if e.get('prd') else ''}{e.get('text', '')}" for e in ev] or ["None yet."]
open(out_path, "w").write("\n".join(L) + "\n")
