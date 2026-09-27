"""Regression tests for the lab's checkers (review #5, Codex 2026-09-27). Run: cd bench && python3 -m pytest -q tests  (or call the test_* functions directly; pytest is optional)"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solcheck import check  # noqa: E402
from hard import pdgi  # noqa: E402
from primal import primal_integral, first_time, feasible_by_t  # noqa: E402

INF = math.inf


def lp1(x, cl, cu, integ):
    # one row: x0 + x1 <= 10 (column-wise CSC)
    return check(x, cl, cu, integ, [-INF], [10.0], [0, 1, 2], [0, 0], [1.0, 1.0])


def test_large_unrelated_variable_does_not_widen_bound_tolerance():
    # x1 = 1e9 (continuous, unbounded above, no row) must not excuse x0 = 1000 over its bound of 1
    r = check([1001.0, 1e9], [0, 0], [1.0, INF], [0, 0], [], [], [0, 0, 0], [], [])
    assert not r["ok"] and r["bound_abs"] == 1000.0 and r["bound_abs_at"] == 0


def test_out_of_bounds_binary_is_rejected():
    # binary = 2 is integral but violates its upper bound 1
    r = lp1([2.0, 0.0], [0, 0], [1, 1], [1, 1])
    assert not r["ok"] and r["int"] == 0 and r["bound_abs"] == 1.0


def test_feasible_passes_and_row_violation_fails():
    assert lp1([1.0, 9.0], [0, 0], [INF, INF], [1, 0])["ok"]
    r = lp1([1.0, 9.5], [0, 0], [INF, INF], [1, 0])
    assert not r["ok"] and r["row_abs"] == 0.5


def test_bound_tolerance_scales_with_the_bound_itself():
    # 1e-3 over a bound of 1e4 is within tol 1e-6 * 1e4 = 1e-2
    assert check([10000.001], [0], [10000.0], [0], [], [], [0, 0], [], [])["ok"]


def test_pdgi_final_bound_only_from_completion():
    # gap 0.5 from t=0 (d=1, p=2), optimum proven at t=80, T=100 -> (0.5*80 + 0*20)/100 = 0.4
    r = {"time_limit": 100, "trajectory": [[0.0, 1.0, 2.0]], "solver_time": 80.0, "dual_bound": 2.0, "primal_bound": 2.0}
    assert abs(pdgi(r) - 0.4) < 1e-12


def test_primal_incumbent_after_horizon():
    # T=60, first incumbent only at t=80: P=2 and no incumbent by T, although feasible at termination
    r = {"time_limit": 60, "trajectory": [[10.0, 0.0, INF]], "solver_time": 80.0, "primal_bound": 5.0, "dual_bound": 0.0}
    assert primal_integral(r, 5.0) == 2.0
    assert first_time(r, 5.0, None) is None and not feasible_by_t(r)
