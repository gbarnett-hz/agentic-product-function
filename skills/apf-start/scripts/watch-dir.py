#!/usr/bin/env python3
"""usage: watch-dir.py <watch-root> <seen-file> [TAG] [edits]

Event-driven directory watcher. Prints `NEW_<TAG> <path>` (TAG defaults to PRD; the EM also uses RESEARCH) once per new *.md under <watch-root>
(recursively) and records it in <seen-file> so a restart never re-reports it. On first
start (no <seen-file>) every existing file is marked seen, not reported. Never exits:
with `edits` it also prints `MOD_<TAG> <path>` when a seen file's content changes (and polls every 2s, since an
in-place edit does not wake kqueue). Never exits: run it under Monitor so each line is a notification. Uses kqueue (macOS/BSD) and wakes
only on directory changes. Elsewhere it falls back to a 2s poll.
"""
import hashlib, os, select, sys, time

SETTLE = 2.0  # a file is reported once unmodified this long (lets writers finish)
root, seen_path = os.path.abspath(sys.argv[1]), sys.argv[2]
tag = (sys.argv[3] if len(sys.argv) > 3 else "PRD").upper()
edits = len(sys.argv) > 4 and sys.argv[4] == "edits"
sha_path = seen_path + ".sha"
shas = dict(l.split("\t") for l in open(sha_path).read().splitlines() if "\t" in l) if os.path.exists(sha_path) else {}
seen = set(open(seen_path).read().split("\n")) if os.path.exists(seen_path) else set()

def scan():
    dirs, found = [], []
    for d, sub, files in os.walk(root):
        sub[:] = [s for s in sub if s not in (".git", ".claude")]
        dirs.append(d)
        found += [os.path.join(d, f) for f in files if f.endswith(".md")]
    return dirs, found

def sha(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()

def save_shas():
    open(sha_path, "w").write("".join(f"{p}\t{h}\n" for p, h in sorted(shas.items())))

def report(found):
    """Emit settled unseen files; return True if some are still being written."""
    pending, now = False, time.time()
    for p in sorted(found):
        try:
            if now - os.stat(p).st_mtime < SETTLE:
                pending = pending or p not in seen or edits
                continue
            h = sha(p) if edits else None
        except FileNotFoundError:
            continue
        if p in seen:
            if edits and shas.get(p, h) != h:  # unknown sha (older seen-file) is recorded, not reported
                print(f"MOD_{tag} {p}", flush=True)
            if edits and shas.get(p) != h:
                shas[p] = h
                save_shas()
            continue
        seen.add(p)
        with open(seen_path, "a") as f:
            f.write(p + "\n")
        if edits:
            shas[p] = h
            save_shas()
        print(f"NEW_{tag} {p}", flush=True)
    return pending

if not os.path.exists(seen_path):  # first start: what's already there isn't new work
    seen.update(scan()[1])
    open(seen_path, "w").write("".join(p + "\n" for p in sorted(seen)))
    if edits:
        shas.update({p: sha(p) for p in seen})
        save_shas()

if edits or not hasattr(select, "kqueue"):
    while True:  # ponytail: polling fallback (always with `edits`; off macOS otherwise); use inotify (pyinotify/inotifywait) if Linux matters
        report(scan()[1]); time.sleep(2)

kq, fds = select.kqueue(), {}
while True:
    dirs, found = scan()
    for d in dirs:
        if d not in fds:
            try:
                fds[d] = os.open(d, os.O_RDONLY)
            except OSError:
                continue
            kq.control([select.kevent(fds[d], select.KQ_FILTER_VNODE, select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                                      select.KQ_NOTE_WRITE | select.KQ_NOTE_DELETE | select.KQ_NOTE_RENAME)], 0)
    for d in [d for d in fds if d not in dirs]:
        os.close(fds.pop(d))
    pending = report(found)
    kq.control(None, 8, SETTLE if pending else None)  # blocks until a watched dir changes
