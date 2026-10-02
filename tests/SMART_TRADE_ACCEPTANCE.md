# TradingView acceptance record

Status: historical evidence for the first-version configuration on 2026-10-02, NOT acceptance of the latest revision.
These observations are validation evidence, not proof of a trading edge.

Follow-up: current local generation/source tests pass (8 tests). The generated
fixture now contains 63 assertions for structural stops, reclaim resets and
the optional touch-candle confirmation anchor. Its current TradingView run,
full indicator/strategy compilation and same-period frequency comparison are
pending. Text-transfer failures and a TradingView error-code-5 page crash
prevented completing that validation. The prior 42-assertion result below must
not be attributed to the new fixture. No increase in accepted positions has
yet been established for the new confirmation option.

The baseline used standard OANDA:XAUUSD candles, HTF 60, pip 0.10,
`Area + structure`, structure targets, zero native slippage, close execution
and no Bar Magnifier. Private test copies were used; nothing was published and
no broker orders were placed.

| Check | Result | Observed evidence |
| --- | --- | --- |
| Local generation/source checks | **Pass** | Eight unit tests pass; generated files are synchronized; whitespace check passes. |
| Production function fixture | **Pass** | Green `PASS: 42 runtime assertions` panel. Covers state transitions, frozen anchors, both directions, target qualification, fixed/breakeven stop timing, partial/gap exits and duplicate settlement. |
| Full strategy | **Pass** | `indicator-based-version1-backtest` compiled and was added with no current runtime error under baseline settings. |
| Full indicator | **Pass** | `indicator-based-version1-smart-trade` separately compiled and was added. With the strategy hidden, its ledger matched the strategy: one completed position, 9.14R, TP1/TP2 1/1, zero ambiguous trades, same target sources. Legacy SMC, Demand/Supply, pivot S/R, BULB, ATR and dashboard drawings remained visible. |
| Normal 1m sample | **Pass, insufficient performance sample** | The actual entry window was Sep 20–Oct 2 (about 12.5k bars, increasing with live bars), not 2–3 months. One short position produced two half-exit legs, a 9.14R ledger and zero divergence flags. TradingView's `2 trades` therefore means one position, not two entries or wins. |
| Entry funnel diagnostics | **Pass** | 247 areas selected, 191 touched, 27 reached confirmation checking and 26 were rejected by the final planner. Outcomes included 111 invalidations, 92 expiries and 16 cancellations; the accepted position occupied 4,098 bars. The most frequent planner veto was nearest TP1 below 2R (11). |
| Requested 90-day period | **Unavailable on current plan** | TradingView requested Deep Backtesting and displayed an upgrade dialog for the signed-in Essential plan. Date inputs cannot manufacture bars that TradingView did not load. No subscription purchase was made. |
| 5m / 15m | **Pass** | No runtime error and zero completed trades in the loaded windows. Filters were not relaxed to create trades. |
| Unsupported 1h / 4h | **Pass** | With HTF 60, panel displayed `Use standard intraday chart below HTF`; no Smart Trade entries. |
| Symbol/pip guard | **Pass** | Temporary `EURUSD` convention on XAUUSD displayed `Verify symbol / pip size`; no entries. `XAUUSD` restored. |
| Disabled module | **Pass** | Panel displayed `Disabled`; no Smart Trade entries; legacy systems remained. Module restored. |
| Area + structure | **Pass** | Reproduced the one completed position in the loaded 1m sample. |
| Area + structure + BULB | **Pass** | 223 selected / 0 rejected and zero completed trades in the comparison window; no runtime error. |
| BULB first appearance | **Pass** | 223 selected / 136 rejected and zero completed trades; last rejection `Baseline HTF mismatch`; no runtime error. |
| Fixed 2R / 3R benchmark | **Pass** | Same structurally eligible entry; +100 USD 2R half and +150 USD 3R half, +250 USD gross total. Structure targets restored. |
| Stop-management experiment | **Pass** | Default `Fixed original stop` preserves the baseline. Production contracts verify that `Breakeven after TP1 (next bar)` moves only the remaining half after TP1 and never before or retroactively within the TP1 candle. |
| Slippage / delayed-fill guard | **Pass** | One-tick slippage and delayed/next-open settings triggered the intended confirmation-close fill runtime error. Baseline restoration recovered the original trade. |
| Reload / re-add | **Pass for loaded sample** | Reload preserved the native trade list. Separately added current indicator source reproduced the strategy research ledger. |
| Replay / future-data leakage | **Pass for cutoff test** | Replay cutoff before the known entry recalculated completed/open, R and TP counts to zero; exiting replay restored the historical result. The UI test did not manually advance every one-minute bar; lifecycle edge cases are covered by the 42 production assertions. |

Final baseline was restored: XAUUSD 1m, pip 0.10, HTF 60,
`Area + structure`, `Structure` targets, `Fixed original stop`, module enabled,
zero slippage and close execution. The Strategy Report is open.

The single completed position is not evidence of profitability, improved
accuracy, live-fill reliability or robust drawdown. An untouched out-of-sample
period and verified broker costs/contract sizing are still required for any
performance conclusion.
