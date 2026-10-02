# Smart Trade research feature

Status: the first-version baseline was tested on OANDA:XAUUSD. The follow-up audit below supersedes blanket completion claims: a post-touch reclaim rejection needed correction, and the structural-stop experiment needs its own performance evidence. The observed sample is far too small to establish a profitable edge, universal market coverage, or absence of all bugs.

## Trade-frequency follow-up — 2026-10-02

- The chart still used the older fixed-stop source while local files already contained `Structure + buffer`. The current source was compiled and tested separately.
- Before the reclaim repair, structural stops on the loaded 5-minute Aug 9–Oct 2 window produced 200 selections, 137 touches, 12 entry checks and zero positions. The leading planner rejection was `Confirmation too far from area` (5). Wider stops alone therefore do not solve the low-frequency design.
- On the loaded 1-minute Sep 20–Oct 2 window, structural stops still produced one position, with two partial exit legs and zero displayed divergence flags. More R from a smaller stop is not more independent trade evidence.
- Fixed an overly broad cancellation: when price was already beyond the frozen swing before the touch, the engine previously rejected the area even if the touch candle closed back through the swing. A later reclaim now remains eligible. If both the pre-touch and touch closes remain beyond the swing, rejection is retained. Same-touch-bar entries remain prohibited. Four production-function regression cases cover the long and short reset/reclaim paths.
- `Initial stop experiment = Fixed 100 pips` remains the default. `Structure + buffer` uses the raw invalidation/touch wick plus buffer, a 20-pip minimum and 500-pip maximum, with quantity rounded down against the same cash-risk budget. Targets, R accounting and estimated costs use the frozen actual initial stop distance. These are research settings, not validated frequency or performance improvements.
- Added a separate `Confirmation anchor = Touch candle break` experiment. It freezes the first touch candle high/low and requires a later close beyond it and outside the area. It can qualify a reaction before a distant internal swing breaks. The original `Internal swing` remains the default. HTF alignment, freshness, structural stop clearance, nearest-obstacle 2R and distinct TP2 remain mandatory; more trades are not guaranteed.
- Current local checks: eight source/build tests pass; the generated Pine fixture contains 63 assertions (including four touch-candle-anchor cases). This is not a Pine compiler result. The latest fixture and confirmation option still require TradingView runtime validation and a measured same-period comparison. Editor text transfer failed repeatedly and the TradingView page crashed with error code 5 during validation; the page was reloaded. Do not treat the previous 42-assertion runtime pass as a pass for this revision.

## Plan completion audit

| Planned item | Status | Evidence |
| --- | --- | --- |
| Preserve the original indicator | Complete | Source regression compares the legacy code with commit `8bea838`; only marked Smart Trade blocks and the Demand/Supply snapshot hook are additive. |
| Locked fresh-area selector | Complete | Confirmed Demand/Supply snapshots, closed-HTF bias, immutable IDs/bounds and one live lock per direction are implemented. |
| Area lifecycle and timestamps | Complete | Waiting, touched, used, invalid, expired, rejected and tested-before-selection states retain birth, selection, touch and confirmation times. |
| Post-touch confirmation | Complete | A later close must break the internal swing frozen at touch; BULB is optional and terminal areas cannot rearm. |
| Fixed SL and two-target planner | Complete | Exact 100-pip SL, structural clearance, nearest-obstacle 2R, distinct TP2, fixed targets and 50/50 exits are enforced. |
| Chart information and alerts | Complete | Locked-area/status drawings, fixed plan levels, rejection reasons, diagnostics and separate area/touch/BUY/SELL alerts are present. |
| Matching backtest and comparisons | Complete | The generated strategy shares the signal engine and provides the three entry modes, structural/fixed-target modes, fixed/breakeven stop modes and fill guards. |
| Behaviour verification | Baseline checked; latest revision pending | Previous baseline compilation/replay evidence is retained below. The 63-assertion fixture and new confirmation experiment have local checks only; repeat live compilation, replay and parity checks. |
| Performance evaluation | Incomplete by evidence, not code | Only about 12 days of 1-minute bars were loaded. One completed position cannot establish an edge; a genuine untouched multi-month dataset is still required. |

## Files

- `indicator-based-version1.pine`: original engines plus the additive module.
- `indicator-based-version1-backtest.pine`: generated native TradingView strategy with the **same** signal engine.
- `modules/`: authoritative new-feature source. Edit these, then run `python3 tools/build_smart_trade.py`.
- `tests/smart_trade_contract.pine`: generated Pine runtime contract tests, using the production functions, not a reimplementation.
- `tests/test_smart_trade.py`: source-preservation and generation checks.

Existing README edits and deleted alternate versions were already present and are not part of this change.

## Deliberate first-version scope

Standard intraday candles with chart timeframe strictly below the selected HTF. Default HTF: 1 hour; defaults are starting research parameters, not optimized settings. XAUUSD pip convention was explicitly confirmed by the user: 0.10 per pip, hence 100 pips = 10.00 price units. A symbol-match guard prevents quietly applying that convention to another instrument. Unsupported charts suppress new signals, not the original engines.

No news filter, automatic broker connection, or real order placement. No guarantee of entry, exit, maximum monetary loss, or improved accuracy. A fixed stop order can fill worse than its price through a gap.

## Areas and confirmation

1. Copy the existing Demand/Supply detection event, after visual bounds are calculated, into an independent bounded registry. Preserve uncompressed wick invalidation. Do not change the original zone engine or BULB movement.
2. Use the existing SMC swing detector algorithm on the chosen HTF, with an explicit length (default 10), and closed-HTF close breaks. Read the previous confirmed HTF result with a one-bar offset; never use developing HTF state.
3. Select the nearest eligible untouched Demand area for bullish bias or Supply area for bearish bias. The area must fit within the fixed stop budget. Display it at selection time, not at the earlier origin candle. Freeze bounds and ID. Keep at most one lock per direction; a bias change cancels the incompatible setup.
4. A touch on a later chart bar arms the setup. Store the prior bar's confirmed internal swing, wick extreme and touch time. A birth-bar touch cannot arm a trade. Unselected zones touched before selection are not fresh entry candidates.
5. A subsequent closed candle must break the frozen internal level and close back outside the area. Close invalidation, HTF misalignment and expiry take precedence. Track the worst wick from touch through confirmation when checking the SL. No same-touch-bar entry; no repeated entry from a used/rejected/expired zone.
6. Optional BULB filter: RSI(13) must have reached <=30 for a buy or >=65 for a sell between touch and confirmation, then recovered out of that extreme at confirmation. This is not required in the default mode.

For the separate faster-confirmation experiment, select `Touch candle break` in both indicator and strategy. It substitutes the frozen touch candle high/low for the internal swing anchor in steps 4–5, without enabling same-bar entries. Compare it on the same loaded dates, with identical stop/target settings. `Structure + buffer` is a separate variable-stop experiment, not the original exact-100-pip promise.

Freshness means untouched **since confirmed detection**, not that the indicator could have identified the base before displacement completed. A default lifetime of 240 chart bars and confirmation window of 12 chart bars are explicit research parameters. Origins, birth, selection, touch and confirmation are distinct.

## Stop and targets

- Fixed 100-pip stop. Tick conversion must be exact; invalid configuration suppresses entries.
- Stop must clear the raw zone edge and touch-to-confirmation wick extreme by the configured buffer (default 5 pips). Reject, never widen.
- Reject entries more than 0.75R beyond the area's proximal edge (configurable).
- Targets use unswept confirmed SMC swing highs/lows, enabled EQH/EQL events, confirmed prior D/W/M highs/lows, and opposing valid Demand/Supply snapshots. Tested Demand/Supply zones remain possible obstacles until their raw boundary is invalidated by a close or their explicit lifetime ends. The legacy display's "hit" status and an entry setup's cancellation are not the same as price invalidation.
- Reject entry inside a valid opposing Demand/Supply zone.
- Sort by directional distance, merge overlapping/nearby levels (default 5 pips), take the first two distinct groups. Never discard the nearest group just because it fails 2R.
- Place exits before the near edge by a tick-rounded buffer (default 2 pips). Require buffered TP1 >=2R gross and TP2 farther than TP1. Show estimated cost-adjusted TP1 reward/risk in the fixed entry tooltip.
- Period references last until taken or the corresponding period rolls; they do not disappear after the short chart-bar zone lifetime.
- 50% exits at each target. `Fixed original stop` remains the default. The separate `Breakeven after TP1 (next bar)` experiment moves only the remaining TP2 half to entry starting on the candle after TP1; it cannot retroactively improve the TP1 candle. No trailing stop is implemented.
- Fixed 2R/3R exit experiment retains identical structural eligibility. It does not qualify trades that failed the structural-target screen.

## Execution assumptions and limitations

The initial research baseline assumes execution at the confirmation **close**, with zero entry slippage. The native strategy explicitly uses `process_orders_on_close=true`, not a next-open fill backdated to the signal. It is a model: a live alert received after that close does not guarantee that price. There is **no live execution adapter**. Late/gapped live entries must be requalified rather than blindly taking an old marker.

The indicator's research ledger uses the broker emulator's ordinary OHLC path convention (high first if open is closer to high, otherwise low first), with opening gaps filled at the open. Ambiguous stop-and-target candles are counted and flagged. This cannot establish the true intrabar order; rerun the native strategy with lower-timeframe Bar Magnifier as a sensitivity check. Equal-distance OHLC ties should also be treated as ambiguous.

Native strategy partial exits use relative stop ticks, so the native initial SL distance remains 100 pips from the actual simulated entry fill. Keep zero slippage/close-fill/no-magnifier settings for initial engine-parity testing. The native adapter checks both open and newly closed legs against the submitted order's own confirmation-close price and bar. A later or slipped entry deliberately stops the script with an explanatory runtime error: it was not qualified by this close-entry model. This also catches an entry and exit that both occur between script evaluations. Slippage/next-open entry experiments need a separate entry-requalification model; they are not supported by merely changing Properties.

Bar Magnifier can be used to investigate exit sensitivity, but may change subsequent position availability. Native fills are authoritative for that configuration; the indicator ledger remains an OHLC approximation. Divergence flags are limited diagnostics, not an exhaustive parity proof. Compare the actual entry and exit list as well, including rejected/unfilled native entries, margin events, quantities and costs. Do not change recalculation-on-fill/every-tick settings for the baseline. Diverged runs must not be advertised as parity-validated.

The default research ledger subtracts an **unverified starting estimate** of 4 pips round trip per whole position. Set this to the broker's actual spread/commission/slippage assumptions. Native Strategy Tester costs are configured separately in Properties (default native commission/slippage zero). Do not mistake its default gross result for a cost-adjusted result or subtract both estimates from the same result. Fixed cash risk and a quantity increment are research settings, not account-risk advice; verify contract point value, quantity step and account currency. Size is rounded down to an even number of increments for 50/50 exits.

No pyramiding; one open research trade; no new entry on a trade-exit bar. Existing trades remain open past the entry date cutoff until their actual exits; an open end-of-data trade is reported separately, never counted as a winner. Closed-equity drawdown in the small indicator panel excludes intratrade excursions; use the native tester for fuller drawdown analysis.

Registries and drawings are bounded. Capacity saturation blocks further entries instead of silently dropping an obstacle. Old decision drawings are intentionally limited; reducing visual history does not remove losses from the ledger. The platform also imposes a shared 500-object limit on the original and added drawings.

Use the **indicator** version for the four named Smart Trade alert conditions. TradingView ignores `alertcondition()` inside strategies; the strategy's order-fill alerts are a different event type. Existing legacy `alert()` calls remain intact and must not be confused with Smart Trade confirmation alerts.

## Validation record — 2026-10-02

Verified during this task:

- Eight local source/build regression tests pass. The original engine source matches commit `8bea838` after excluding only the new marked blocks and Demand/Supply snapshot hook. Indicator and strategy share identical generated types and signal engine. Generated files are synchronized, and `git diff --check` passes.
- TradingView's production-function contract fixture displayed **PASS: 42 runtime assertions** in UTC+7. The fixture covers lifecycle transitions, expiry, HTF cancellation, frozen anchors, delayed confirmation, both directions, target qualification, fixed/breakeven stop timing, gap/partial exits and duplicate settlement. It does not replace validation of the native execution adapter or live data pipeline.
- The generated strategy compiled and was added privately as `indicator-based-version1-backtest`. The full indicator separately compiled, was added, and was saved privately as `indicator-based-version1-smart-trade`. With identical settings and loaded history, both displayed the same one-position ledger: 9.14R, TP1/TP2 1/1, zero ambiguous trades, and target sources `Previous Day Low / Previous Week Low`.
- The loaded OANDA:XAUUSD 1m entry window was only Sep 20–Oct 2 (about 12.5k available bars; the live-bar count continues increasing), not two or three months. One short position entered Sep 23 at 08:01 at 4355.310, quantity 10 split into two quantity-5 exits. TP1 filled at 4291.695 on Sep 23 at 20:42 and TP2 at 4235.365 on Sep 28 at 07:31. Native gross P/L was 917.80 USD; the research ledger reported 9.14R after its separate 0.04R estimated-cost deduction. TradingView's `2 trades` are the two partial-exit legs of **one** position, not two independent entries or wins.
- The new panel diagnostics showed 247 selected areas, 191 touches, 27 confirmation checks, 26 entry-plan rejections, 111 invalidations, 92 expiries, 16 cancellations and 4,098 bars occupied by the accepted position. The most frequent final planner veto was `Nearest TP1 below 2R` (11). This confirms the entry loop is active; the low accepted-position count comes from the intentionally strict 100-pip structural-stop, nearest-obstacle 2R and distinct-TP2 rules plus the single-position lock.
- Requesting a 90-day Strategy Tester period opened TradingView's Deep Backtesting upgrade dialog. The signed-in Essential plan only permits data loaded on the chart, so a genuine 90-day 1m result could not be produced without changing subscription or using a separate external data/backtest pipeline. The script's start/end inputs filter loaded bars; they cannot load missing chart history.
- The 5m and 15m loaded windows produced no completed trades. Unsupported 1h and 4h charts, with the HTF left at 60 minutes, displayed `Use standard intraday chart below HTF` and produced no Smart Trade entries.
- Temporarily changing the pip-convention symbol to `EURUSD` on XAUUSD displayed `Verify symbol / pip size` and produced no entries. Disabling the module displayed `Disabled`, produced no Smart Trade entries, and left the legacy chart systems visible. Both settings were restored.
- Entry-mode checks completed without runtime errors. `Area + structure` reproduced the one completed position. In the loaded comparison window, `Area + structure + BULB` showed 223 selected / 0 rejected and no completed trade; `BULB first appearance` showed 223 selected / 136 rejected, no completed trade, and `Baseline HTF mismatch` as the last rejection. Zero trades were retained as a valid result rather than weakening the filters.
- The fixed 2R/3R benchmark reused the structurally eligible entry and produced exactly +250 USD gross: +100 USD on the 2R half and +150 USD on the 3R half. Structure targets were restored afterward.
- One-tick slippage and delayed/next-open execution negative tests stopped with the intended confirmation-close fill error. Restoring zero slippage and close execution recovered the original entry and both exits without a guard error.
- A page reload restored the same trade list. A separate re-add of the current indicator source reproduced the strategy ledger. Replay was cut off before the known Sep 23 entry: completed/open, R and TP counts recalculated to zero, so the later trade did not leak backward. Exiting replay restored the one position, 9.14R and TP1/TP2 1/1. Production contract assertions separately cover frozen IDs/bounds, birth/touch-bar exclusion and duplicate settlement; the UI replay did not manually step every intervening one-minute candle.
- The chart was returned to standard XAUUSD 1m, `Area + structure`, `Structure` targets, `Fixed original stop`, pip symbol `XAUUSD`, module enabled, zero slippage and close execution. The updated indicator and strategy both compiled, the default historical result stayed unchanged, and the Strategy Report was left open. No scripts were published and no broker orders were submitted.

Acceptance is complete for this first-version tested configuration and the trade-count reporting is now explicit, but performance evaluation is **inconclusive**. One completed position from the loaded 12-day window is insufficient to claim improved accuracy, profitability, drawdown reliability or robustness. Broker-specific spread, commission, slippage, point value and quantity increment remain unverified, and a genuinely loaded untouched out-of-sample period is still required before tuning or deployment.

## Revalidation and future comparison

Run locally:

```sh
python3 tools/build_smart_trade.py --check
python3 -m unittest discover -s tests -v
git diff --check
```

After any engine change, run `tests/smart_trade_contract.pine` in TradingView on standard XAUUSD: it must show a green PASS panel. This checks target sorting/clustering, closer-obstacle rejection, both trade directions, fixed stops, missing TP2, inside-zone rejection, tested/invalid zone distinctions, half exits, gap fills and duplicate settlement.

For later revisions, compile both full scripts; inspect standard 1m/5m/15m, unsupported 1h/4h at default HTF, wrong-symbol suppression, module disabled, replay, reload, and remove/re-add. Compare stable IDs, bounds, event timestamps and native fills. Compilation alone is insufficient. Preserve original chart instances hidden, not deleted.

Compare three entry experiments with identical filters and exits: first-observable BULB, area+structure, area+structure+BULB. The BULB baseline is **filtered**, not a claim to replicate every old displayed label as a trade. Use identical symbol/timeframe/date/cost/quantity settings. Then test the fixed-target and next-bar-breakeven experiments separately, changing only one exit dimension at a time. Count full-position outcomes rather than treating each partial exit as an independent winning trade. Reserve a genuinely unseen time period before tuning. Report inadequate trade counts and failed configurations; do not relax safety filters merely to produce more signals.
