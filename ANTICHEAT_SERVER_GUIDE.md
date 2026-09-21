# WSE2 Anti-Cheat — Server Owner's Guide

This guide covers the anti-cheat built into WSE2: how to turn it on, what it detects, how to collect
statistics, and how to calibrate it on your own players before it is allowed to kick anybody.

Everything described here runs **on the server**. Nothing is installed on the client, nothing is sent
to the client, and no client is ever told that a detector fired. A cheater sees only a disconnect, and
only in enforce mode. Vanilla clients and older WSE2 clients connect and play exactly as before.

---

## 1. What it detects

| Detector | Cheat it targets | Notes |
|---|---|---|
| Seed validation | Perfect shooting accuracy | The client picks the random seed the server uses for shot spread. An honest client always sends back the value the server already holds, so mismatches are conclusive. |
| Aim snap | Aimbot with an instant flick | Requires a series of flicks, each immediately followed by an attack or a shot. |
| Aim lead | Aimbot that leads a moving target | Judged on whether the aiming error grows with shot difficulty, not on accuracy alone. |
| Spread luck | Seed exploitation that slipped past validation | The honest average is a known constant, so the threshold sits many standard deviations away. |
| Auto block | Autoblock, the most common Warband cheat | Three independent signals: direction match with inhuman reaction, feints followed instantly, and blocks of attacks coming from behind. |
| Auto attack | Autoattack / chamber bot | Always striking the uncovered side, feints that react to the defender, and an inhuman chamber rate. |
| Attack cadence | Animation speed manipulation | Off by default: it has little value on an authoritative server and fires on fast weapons. |
| Client clock skew | Cheat Engine speedhack | **Gives no gameplay advantage** on an authoritative server. Useful only as evidence that the player is running a cheat tool. |

**What it cannot detect.** ESP and wallhacks are invisible to the server: the client legitimately
receives the position of every player, and a cheat only draws what it was already sent. Nothing in
this build detects them. Modified client module files are likewise not checked in this version.

---

## 2. Turning it on

The anti-cheat is configured in the server's `rgl_config.ini`, under a new `[AntiCheat]` section, plus
one switch in `[DedicatedServer]`. A ready-made section with every key and an explanation of each is
in `server_config.ini` next to this guide — copy it into your server config.

The three settings that matter on day one:

```ini
[AntiCheat]
iMode=1

[DedicatedServer]
bLogAntiCheat=true
bAdvancedLogFormat=true
```

`bAdvancedLogFormat=true` is strongly recommended: it makes every log line machine-readable so you can
sort and filter, instead of reading prose by eye.

### The three modes

| `iMode` | Behaviour | Use it for |
|---|---|---|
| `0` | Nothing is measured, the log stays empty. | Only if you must be certain nothing runs at all. Useless for later review. |
| `1` **silent** | Every detector runs, writes to the log and fires the module trigger. **No kicks, no bans.** | Calibration, and tournaments where you want to expose cheaters afterwards rather than interrupt play. |
| `2` **enforce** | The same, plus kicks and optional bans once a threshold is crossed. | Normal public play, after calibration. |

Switch modes at runtime from the server console or RCON, no restart needed:

```
set_anticheat_mode 1     # silent
set_anticheat_mode 2     # enforce
get_anticheat_mode       # show the current mode
```

A mode change is written to the log with the fact that the console requested it.

**Important consequence of this version's scope:** there is no check at the moment a player joins.
Every detector is statistical and needs dozens of samples of actual play. "Enforce mode stops
cheaters from joining" really means "a cheater is detected while playing, then kicked, and if you also
set a ban duration, cannot come straight back". Bans are keyed to the player's unique id, so a second
serial key or a VPN evades them. IP bans, if you want them, belong in your module script using
`str_store_player_ip` together with `ti_server_player_joined`.

---

## 3. What gets written to the log

All three record types go to the dedicated server log, gated by `bLogAntiCheat`. Fields are separated
by `cLogSeparatorChar` (a comma by default) when `bAdvancedLogFormat=true`.

### Detection line

```
anticheat,<name>,<uniqueId>[,<ip>],<type>,<value>,<threshold>,<action>
```

`<type>` is the numeric detection id (see the table below). `<value>` and `<threshold>` are in the
detector's own unit: percentages are `0..100`, reaction times are milliseconds, the spread mean is
multiplied by 1000. `<action>` is `logged`, `handled by module`, `kicked` or `banned`.

| id | detection |
|---|---|
| 10 | aim snap |
| 11 | client clock skew |
| 12 | spread luck |
| 13 | attack cadence |
| 14 | auto block |
| 15 | auto attack |
| 16 | seed mismatch |
| 17 | aim lead |
| 100 | reported by your module script |

### Summary line

Written when a player leaves and for every player still connected when a mission ends. This is the
line that matters for calibration and for post-tournament review, because it is written for **every**
player, not only for the ones a detector fired on.

```
anticheat,summary,<reason>,<name>,<uniqueId>[,<ip>],mission=<n>,session=<seconds>,detections=..,seed_mismatches=..,...
```

`<reason>` is `exit` or `mission_end`. The trailing part is a list of `name=value` pairs:

| Field | Meaning |
|---|---|
| `detections` | how many times any detector fired this session |
| `seed_mismatches` | shot seeds that did not match the server's |
| `time_skew_pct` | client clock deviation over the last window, percent |
| `time_skew_max_pct` | **the worst positive deviation of the whole session** - use this one, not the last window |
| `time_skew_stall_pct` | worst negative deviation; this is client lag, never a cheat |
| `time_skew_windows` | how many windows exceeded the threshold this session |
| `max_aim_speed` | fastest look-direction change seen, degrees per second |
| `aim_snaps` | flicks that were immediately followed by an attack |
| `spread_mean_x1000` | average shot spread; **250 is the honest value** |
| `spread_shots` | shots in that average |
| `autoblock_samples` | blocks measured |
| `autoblock_match_pct` | how often the block direction was the "correct" one |
| `autoblock_reaction_ms` | median reaction, with the player's ping already subtracted |
| `autoblock_feints` | feints the player followed inside the reaction window |
| `autoblock_offscreen` | correct fast blocks of attacks from outside their field of view |
| `autoattack_open_pct` | how often their attack found the uncovered side |
| `autoattack_reaction_ms` | median reaction to the defender changing block |
| `autoattack_chamber_pct` | chamber successes out of chamber attempts |
| `aimlead_hard_shots` | difficult shots sampled |
| `aimlead_err_x100` | median aiming error on those, hundredths of a degree |
| `aimlead_flat_x100` | hard-shot error divided by easy-shot error, x100 |

### Speed modifier line

```
anticheat,modifier,<name>,<uniqueId>,<modifier>,<value x100>
```

Written whenever a script changes a player agent's speed, action speed, reload speed or use speed.
When someone reports "that player is speedhacking", this line tells you whether a script on your own
server actually granted them extra speed — which is a module exploit, not a client cheat.

---

## 4. Reading the numbers

These are the values an honest player produces. Compare anything suspicious against them.

| Field | Honest player | A bot |
|---|---|---|
| `spread_mean_x1000` | around 250, drifting a little either way | far below 100 |
| `seed_mismatches` | exactly 0 | grows with every shot |
| `autoblock_match_pct` | 50–85; a top duellist may reach 90 | 95–100 |
| `autoblock_reaction_ms` | 150–300 | under 100, often near 0 |
| `autoblock_offscreen` | 0–2 lucky guesses | steadily climbing |
| `autoattack_open_pct` | 60–85 | 95–100 |
| `aimlead_flat_x100` | 200 and up: hard shots are much worse than easy ones | around 100: difficulty makes no difference |
| `time_skew_max_pct` | 0 - a client cannot gain simulated time | 10 and up, sustained |
| `time_skew_stall_pct` | anything up to 60 on a laggy connection | irrelevant, not a cheat signal |

The single most reliable indicator is **`autoblock_offscreen`**. A human cannot block a swing coming
from behind them; the engine's automatic block direction ignores where the player is looking, so a
cheat using it blocks perfectly in situations where a human is blind. Guessing produces a handful of
matches, not a stream of them.

The second most reliable is **`seed_mismatches`**, which is not statistical at all: an honest client
cannot produce a single one.

---

### Reading the clock-skew detector

This one deserves a note, because its first version got it wrong.

The client reports its own mission clock with every packet, and the server compares how far that clock
advanced against its own over a 10-second window. The engine clamps a single frame to 0.1 seconds
before it advances that clock, which means a client that stalls, loads or is alt-tabbed can only ever
*lose* simulated time - it can never catch up. Two consequences:

- **Negative skew is lag.** It is recorded as `time_skew_stall_pct` and is never reported as a
  detection. Values of -10, or even -60, are ordinary on a bad connection.
- **Positive skew has no honest cause.** A client cannot gain simulated time unless something is
  inflating its clock. A `time_skew_max_pct` of 10 or more, sustained, means a speedhack tool is
  running.

Two things follow for calibration. Use `time_skew_max_pct`, never `time_skew_pct`: the latter is only
the last window before the player left, so a cheater who idles for ten seconds before disconnecting
shows a clean number. And do not raise `fMaxTimeSkewRatio` far above the default of 0.10 - there is no
honest population up there to protect.

Remember what this detector is worth. A client-side clock speedhack gives **no gameplay advantage** on
an authoritative server: movement, animations, hit detection and cooldowns are all computed on the
server, and an accelerated client is simply corrected back. Treat a type 11 detection as proof that
the player is running a cheat tool, not as proof that the tool is helping them win.

## 5. Calibrating on your own players

Do not skip this. Detectors are statistics, not proof, and a strong duellist can look like a weak
autoblocker. The defaults ship deliberately loose and with every kick switch turned off.

**Week 1 — collect.** Set `iMode=1` and `bLogAntiCheat=true`, and play normally. Do nothing else.
Let the log fill up across busy evenings, quiet afternoons, duel servers and battle rounds alike.

**Week 1, end — build a baseline.** Pull every `anticheat,summary` line out of the log and load them
into a spreadsheet. Look at the distribution of each field across your regular players, especially the
best ones. What you want is the ceiling your honest population reaches: the highest
`autoblock_match_pct`, the lowest `autoblock_reaction_ms`, the highest `autoattack_open_pct`.

**Set thresholds above that ceiling, with room to spare.** If your best duellist reaches 88% block
match at a 160 ms median reaction, then `fAutoBlockMatchRate=0.92` with
`iAutoBlockMaxReactionMs=120` leaves a clear gap. Never set a threshold at or below a value one of
your own honest players actually produced.

**Week 2 — verify.** Keep silent mode and watch which players the detectors now fire on. Every one of
them should be someone you already suspected. If a regular you trust shows up, raise that threshold or
increase the sample window (`iAutoBlockWindowSamples`, `iAutoAttackWindowSamples`,
`iAimLeadHardShots`); a larger window is always safer than a looser threshold, it just takes longer to
reach a verdict.

**Week 3 — enforce, one detector at a time.** Set `iMode=2` and turn on exactly one kick switch, the
one you trust most — usually `bAutoBlockKick=true`. Watch it for a few days. Then add the next.
Turning them all on at once leaves you unable to tell which one misfired.

**Recommended order of trust**, from safest to riskiest:

1. `bSeedMismatchKick` — not statistical, an honest client cannot trigger it.
2. `bSpreadLuckKick` — the honest average is a mathematical constant.
3. `bAutoBlockKick` — after calibration, and mainly because of the offscreen signal.
4. `bAimLeadKick` — solid, but the difficulty threshold needs tuning from your own log first.
5. `bAutoAttackKick` — strong duellists get close to these numbers.
6. `bAimSnapKick` — a high-DPI player really can flick 180 degrees and throw.
7. `bTimeSkewKick` - now safe in principle (only a client running fast is reported, and that has no
   honest cause), but the tool it targets gives no gameplay advantage anyway, so a kick buys little.
8. `bAttackCadenceKick` - leave off; it fires on fast weapons.

A useful middle step before kicking: set `iAutoTempBanSeconds=0` so a detection costs the player a
reconnect rather than an hour, until you are confident.

### Tuning `fAimLeadHardDifficulty`

The aim-lead detector splits shots into "easy" and "hard" using `distance x target lateral speed`.
The shipped value of 20 is a starting guess. Once you have summary lines, check
`aimlead_hard_shots`: if it barely grows on an archery-heavy server, the threshold is too high and
should come down; if almost every shot counts as hard, raise it. You want roughly a third of shots on
the hard side.

---

## 6. Running a tournament

The mode switch exists for exactly this. Two ways to run it:

**Expose afterwards.** `set_anticheat_mode 1` before the tournament starts. Every detector keeps
running and everything is logged, but nobody is interrupted. Afterwards, pull the `anticheat,summary`
lines for the tournament rounds and review them.

**Flag for the referees.** `set_anticheat_mode 2`, but handle `ti_on_cheat_detected` in your module
and return a non-zero result. The engine then takes no action at all, and your script decides what to
do — message the referees, write to your own database, mark the round. This gives you a live signal
without a kick disrupting a match.

Be aware of the trade-off in the first option: while the tournament is running in silent mode, honest
competitors are playing against active cheaters, and exposing them afterwards does not undo the
results. If the tournament outcome matters, prefer the second option.

---

## 7. Module script access

The anti-cheat exposes four operations and one trigger. Constants are in the WSE2 SDK
(`header_operations_addon.py`, `header_triggers_addon.py`).

```python
(player_get_anticheat_stat, ":value", ":player_no", acs_autoblock_match),
(server_set_anticheat_option, aco_mode, acm_silent),
(server_get_anticheat_option, ":mode", aco_mode),
(player_anticheat_report, ":player_no", ":value"),
```

`player_get_anticheat_stat` reads any field from the summary table above — useful for an admin panel
that shows a suspect's live numbers. `server_set_anticheat_option` changes any threshold at runtime,
so a module can run different settings on a duel server and a siege server, or switch modes on a
schedule. `player_anticheat_report` pushes a detection from your own script through the same log,
trigger and kick pipeline.

The trigger fires on every detection:

```python
(ti_on_cheat_detected, 0, 0, [],
 [
   (store_trigger_param, ":player_no", 1),
   (store_trigger_param, ":type", 2),
   (store_trigger_param, ":value", 3),
   (store_trigger_param, ":threshold", 4),
   # ... your own logging or notification here ...
   (assign, reg0, 1),   # non-zero: the engine does nothing, you handled it
 ]),
```

Returning a non-zero result suppresses the engine's kick entirely. Returning zero, or having no
trigger at all, leaves the engine to act according to the mode and the kick switches.

Note that values marked "(fp)" in the SDK are fixed point: divide by the module's fixed-point
multiplier to get the real number.

---

## 8. Things worth knowing

**Comments are lost on save.** The server rewrites `rgl_config.ini` when it shuts down cleanly, which
strips the `#` comments from the file. Keep an annotated copy somewhere else.

**Admins are exempt.** With `bExemptAdmins=true`, nothing is ever reported for an admin. If you want
to test detection with your own account, drop your privilege first or set this to false temporarily.

**The report cooldown is per player and per type.** With `fReportCooldownSec=30`, a player triggering
the same detector repeatedly produces one line every 30 seconds, not a flood.

**Auto block detection turns itself off** when the server allows automatic blocking
(`set_control_block_direction 0`), because then every player blocks "correctly" by design and there is
nothing to compare against. The same applies to shield users, who have only one block direction.

**The server seed option has a visible cost.** `bServerAuthoritativeSeed=true` closes spread
compensation completely, but a shooter watches their own predicted arrow steer slightly during the
first third of a second, more noticeably with throwing weapons, firearms and high ping. It is off by
default for that reason; competitive servers may still want it on.

**This has not been tested with live players yet.** It builds and runs, and the logic has been
reviewed, but the thresholds are estimates until your own log confirms them. That is precisely why
silent mode exists and why every kick switch ships off.
