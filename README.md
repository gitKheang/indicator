# SMC & ICT & Indicators + Scalping Master

TradingView Pine Script indicators that combine SMC market structure, Order
Blocks, EQH/EQL, Fair Value Gaps, previous Daily/Weekly/Monthly levels,
Premium/Equilibrium/Discount, Demand/Supply, Pivot Support/Resistance, candle
patterns, a nine-indicator dashboard, BULB, and ATR envelopes.

## Current development version

`indicator-version3-precision-focus.pine`

Version 3 preserves the Version 2 systems and adds an independent Precision
Focus layer. Existing arrows, triangles, BULB labels, drawings, and alerts are
not replaced by the new A+ signals.

### Precision Focus pipeline

1. Uses completed 15-minute and 1-hour structure for directional context.
2. Snapshots native Swing/Internal Order Blocks, Demand/Supply zones, Pivot S/R
   zones, and FVGs into one bounded immutable AOI registry.
3. Tracks AOI direction, fixed bounds, source, quality, age, touches,
   invalidation, and one-signal consumption.
4. Locks Primary and Backup BUY/SELL candidates until invalidation, expiry, or
   consumption so an active selection cannot jump to a newly closer zone.
5. Creates a SETUP on the selected AOI touch, then waits up to five bars for a
   confirmed reclaim plus displacement or BOS/CHoCH.
6. Scores HTF structure (20), zone quality (25), liquidity (20), structure and
   displacement (20), Premium/Discount location (10), and secondary
   BULB/TSI/dashboard evidence (5).
7. Prints a fixed `A+ BUY` or `A+ SELL` marker when the default score reaches
   72. This threshold is an engineering filter, not a probability or promised
   win rate.

### Validation dashboard

The Precision Focus table reports locked BUY/SELL AOIs, HTF bias, last scores,
closed outcomes, 1R/2R rates, stops, ambiguous same-bar outcomes, expirations,
and average MFE/MAE. Outcome tracking assumes entry at the next bar open and
uses the AOI boundary plus an ATR buffer as structural invalidation.

Its default position is `middle_right` so it does not overlap the original
bottom-right direction dashboard. The position is selectable in the Precision
Focus display settings.

### Default operating scope

- Entry chart: 1 minute
- Context: confirmed 15 minute and 1 hour
- Setup confirmation window: 5 bars
- Signal ATR: 20 periods
- Minimum displacement body: 0.30 ATR
- Focus score threshold: 72
- One Focus signal per consumed AOI

These defaults require TradingView replay and out-of-sample calibration for the
symbol and session being traded. Do not treat the score as a win-rate forecast
or the indicator as automatic trade execution.

## Verified build status — 2026-09-26

- Saved in TradingView as `SMC & ICT & Indicators + Scalping Master v3 Precision Focus`.
- Pine Script v5 compilation completed and the saved source updated on chart.
- Runtime checked on `OANDA:XAUUSD`, 1-minute chart, with no runtime error shown.
- Existing Version 2 compiler warnings remain warnings; they do not prevent the
  script from compiling or running.
- Historical Bar Replay, reload-position comparison, and out-of-sample accuracy
  measurement are still required before making performance claims.

## Version files

- `indicator-version3-precision-focus.pine` — current Precision Focus build.
- `indicator-version2 tune value small-symbole.pine` — Version 2 baseline with
  compact raw markers.
- `indicator-version2 tune value large symbole.pine` — Version 2 baseline with
  normal-sized raw markers.
- `indicator-version1.pine` — earlier comparison baseline.

## TradingView verification checklist

1. Paste the complete Version 3 source into Pine Editor.
2. Save and confirm a successful Pine v5 compilation.
3. Add it to a standard 1-minute chart.
4. Confirm the table reports the expected 15-minute/1-hour bias and locked AOIs.
5. Replay historical data and verify SETUP/A+ markers remain fixed after reload.
6. Compare Version 3 with Version 2 over the same periods and record signal
   count, 1R/2R first-hit rates, MFE, MAE, and ambiguous bars.
7. Validate on unseen data before changing the default weights or threshold.
