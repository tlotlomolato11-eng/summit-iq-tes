# Pine indicators

## `ict_killzones.pine`

Draws Asian / London / New York killzones on a TradingView chart, marks each
closed session's high and low as resting liquidity, and extends those levels
until price sweeps them.

### The bug this fixes

Killzones stored as UTC constants are only correct while New York is on EST:

| Window (NY local) | EST (Nov–Mar) | EDT (Mar–Nov) |
|---|---|---|
| NY 07:00–10:00 | 12:00–15:00 UTC | **11:00–14:00 UTC** |
| London 02:00–05:00 | 07:00–10:00 UTC | **06:00–09:00 UTC** |

A fixed `12:00-15:00 UTC` NY window is therefore an hour late for roughly eight
months a year — it excludes the NY open hour and includes an hour of post-open
drift instead.

This indicator takes the session in its own local zone and passes that zone to
`time()`, so TradingView resolves DST per bar:

```pine
inSession(string sess) =>
    not na(time(timeframe.period, sess + ":" + days, tz))
```

Change `tz` and the windows follow that zone's clock. Nothing needs adjusting
twice a year.

### Use

1. TradingView → Pine Editor → paste the file → **Add to chart**.
2. Intraday timeframes only (a label says so on higher ones).
3. Defaults are Mon–Fri (`23456`); day mask is `1=Sun … 7=Sat`.

Session windows are inputs, so if your own convention differs (08:00–11:00 for
the NY open, say) change it in settings rather than in the source — the point is
that whatever you pick stays anchored to New York's clock.

### Not included

Judas-swing detection. It needs an explicit definition — how far past the
session extreme counts as a sweep, and how much displacement back counts as the
reversal — and guessing those in code just hides the choice. Worth doing next,
with the thresholds as inputs.
