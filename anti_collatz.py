"""anti_collatz.py

Reference implementation for:
- Classical Collatz: even -> n/2, odd -> 3n+1
- Anti-Collatz (parity-inverted): even -> 3n+1, odd -> n/2 (floor)

Includes basic trajectory generation, cycle detection, and a small CLI demo.

Usage:
    python anti_collatz.py --demo
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse


def collatz_step(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def anti_collatz_step(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    return 3 * n + 1 if n % 2 == 0 else n // 2


def iterate(f, n: int, max_steps: int = 10_000) -> List[int]:
    seq = [n]
    for _ in range(max_steps):
        seq.append(f(seq[-1]))
    return seq


@dataclass
class CycleResult:
    seed: int
    prefix: List[int]
    cycle: List[int]
    steps: int


def detect_cycle(f, seed: int, max_steps: int = 50_000) -> Optional[CycleResult]:
    """Detect the first repeated state using a visited-index map.

    Returns prefix + cycle (where cycle is the repeating segment), or None if not found.
    """
    seen: Dict[int, int] = {}
    seq: List[int] = []
    x = seed

    for _ in range(max_steps):
        if x in seen:
            start = seen[x]
            prefix = seq[:start]
            cycle = seq[start:]
            return CycleResult(seed=seed, prefix=prefix, cycle=cycle, steps=len(seq))
        seen[x] = len(seq)
        seq.append(x)
        x = f(x)

    return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true", help="Run a small demo on both maps")
    p.add_argument("--seed", type=int, default=6, help="Seed for cycle demo")
    p.add_argument("--max_steps", type=int, default=5000)
    args = p.parse_args()

    if args.demo:
        cr = detect_cycle(collatz_step, args.seed, max_steps=args.max_steps)
        ar = detect_cycle(anti_collatz_step, args.seed, max_steps=args.max_steps)

        print("Classical Collatz (seed=%d):" % args.seed)
        if cr is None:
            print("  No repetition detected within max_steps (unexpected for small seeds).")
        else:
            print("  prefix length:", len(cr.prefix))
            print("  cycle:", cr.cycle)

        print("
Anti-Collatz (seed=%d):" % args.seed)
        if ar is None:
            print("  No repetition detected within max_steps.")
        else:
            print("  prefix length:", len(ar.prefix))
            print("  cycle:", ar.cycle)
            print("  (example cycle often includes: 6 -> 19 -> 9 -> 4 -> 13 -> 6)")
    else:
        p.print_help()


if __name__ == "__main__":
    main()
