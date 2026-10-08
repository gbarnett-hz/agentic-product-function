#!/usr/bin/env python3
"""usage: watch-dir.py <watch-root> <seen-file> [TAG]

Event-driven directory watcher. Prints `NEW_<TAG> <path>` (TAG defaults to PRD; the EM also uses RESEARCH) once per new *.md under <watch-root>
(recursively) and records it in <seen-file> so a restart never re-reports it. On first
start (no <seen-file>) every existing file is marked seen, not reported. Never exits:
run it under Monitor so each line is a notification. Uses kqueue (macOS/BSD) and wakes
only on directory changes. Elsewhere it falls back to a 2s poll.
"""
import os, select, sys, time

SETTLE = 2.0  # a file is reported once unmodified this long (lets writers finish)
root, seen_path = os.path.abspath(sys.argv[1]), sys.argv[2]
tag = (sys.argv[3] if len(sys.argv) > 3 else "PRD").upper()
seen = set(open(seen_path).read().split("\n")) if os.path.exists(seen_path) else set()

def scan():
    dirs, found = [], []
    for d, sub, files in os.walk(root):
        sub[:] = [s for s in sub if s not in (".git", ".claude")]
        dirs.append(d)
        found += [os.path.join(d, f) for f in files if f.endswith(".md")]
    return dirs, found

def report(found):
    """Emit settled unseen files; return True if some are still being written."""
    pending, now = False, time.time()
    for p in sorted(found):
        if p in seen:
            continue
        try:
            if now - os.stat(p).st_mtime < SETTLE:
                pending = True
                continue
        except FileNotFoundError:
            continue
        seen.add(p)
        with open(seen_path, "a") as f:
            f.write(p + "\n")
        print(f"NEW_{tag} {p}", flush=True)
    return pending

if not os.path.exists(seen_path):  # first start: what's already there isn't new work
    seen.update(scan()[1])
    open(seen_path, "w").write("".join(p + "\n" for p in sorted(seen)))

if not hasattr(select, "kqueue"):
    while True:  # ponytail: polling fallback off macOS; use inotify (pyinotify/inotifywait) if Linux matters
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
