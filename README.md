# WSE2 Anti-Cheat Findings

This repository is a documentation and evidence archive for a non-public WSE2 1.5.2 server build, the open-source Module System integration, and the findings gathered from real server logs.

> This is not a ready-to-install package or a public engine release. It is a research archive that documents engine behavior, module decision logic, and the evidence trail behind the conclusions.

## Start Here

| Goal | Read |
| --- | --- |
| Learn the server-side operational model and calibration rules | [ANTICHEAT_SERVER_GUIDE.md](ANTICHEAT_SERVER_GUIDE.md) |
| Understand the Module System threat logic and recent fixes | [MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md) |
| Review confirmed accounts vs. offscreen-only observations | [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) |
| Inspect raw evidence | Dated logs in the [63rd Server](63rd%20Server) directory |

## What This Project Covers

This work is intentionally split into two layers:

1. WSE2 engine layer: the non-public WSE2 1.5.2 build generates the detectors and the server-side anti-cheat runtime.
2. Module System layer: the module receives `ti_on_cheat_detected` events, applies scoring logic, preserves GUID-based history, and decides whether to log, notify, or enforce a ban.

The project purpose is not to punish on a single suspicious value. It is to preserve evidence, compare live player behavior against baseline ranges, and only escalate once multiple signals point in the same direction. Deterministic issues such as seed mismatch are handled as zero-tolerance events; statistical issues such as autoblock need corroboration.

## Action Steps for Server Owners

- Read [ANTICHEAT_SERVER_GUIDE.md](ANTICHEAT_SERVER_GUIDE.md) before enabling anything.
- Start in silent mode with `iMode=1` and collect a week of baseline data.
- Compare `anticheat,summary` rows and detection patterns against your normal player population before switching to enforce mode.
- Treat offscreen warnings as a pattern check, not a final verdict by themselves.
- Apply enforcement gradually: first one threshold, then another, rather than flipping all settings on at once.
- Keep the GUID and raw evidence together when reviewing suspicious sessions.

## Action Steps for Module System Developers

- Read [MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md) first for the current decision logic and exception handling.
- Verify that the trigger suppresses native action only for the scored types and leaves unhandled types to the native WSE2 fallback.
- Review seed mismatch, autoblock sub-signals, and clock-skew logic separately; they are not interchangeable signals.
- Check the JSON config, whitelist, admin GUIDs, and history files as separate responsibilities.
- Validate the module against the exact deployed WSE2 build because the engine source is not included here.
- Compare the documented behavior with the actual runtime logs before treating a fix as complete.

## Current Scope and Decisions

- WSE2 1.5.2 is a non-public build and is not open source.
- The Module System implementation is the open-source part of the project and is documented in [MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md).
- The engine and the Module System are separate concerns; the repo documents both, but does not publish engine source.
- Silent mode is the default observation mode for evidence collection.
- The GUID is the identity key; names are not reliable evidence by themselves.
- Increasing the default FOV can create offscreen detections without proving cheating.
- Offscreen-only crossings are retained as observations, not as confirmed cheater verdicts.
- Confirmed cheaters and offscreen observations are kept in separate sections in [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md).
- The project documentation is intentionally in English for the WSE2 community and the server-operator audience.

## What the Module Evaluates

| Signal | Interpretation | Confidence note |
| --- | --- | --- |
| Seed mismatch (`type 16`) | Client returned a mismatched random seed | Deterministic; strongest signal |
| Auto block (`type 14`) | Match-rate spikes, feint-follow reactions, and offscreen crossings | Requires combined signals or corroboration |
| Client clock skew (`type 11`) | Positive skew indicates speedhack; negative skew is lag | Negative skew must not be treated as a cheat |
| Offscreen-only readings | Attack appears outside the assumed view cone | Low-confidence alone; FOV variance is a real source of noise |
| Client integrity checks (`types 20-24`) | SDK-defined module/thread/hook/signature/text-hash checks | Present in the SDK but not proven by this archive |

## Key Behavioral Rules

- `iMode=0`: no anti-cheat measurements are taken.
- `iMode=1`: detections are collected and logged in silent mode; no enforcement is applied.
- `iMode=2`: enforce mode can trigger the ban path when configured thresholds are crossed.
- The module owns the `acd_auto_block`, `acd_time_skew`, and `acd_seed_mismatch` handling paths and suppresses native fallback for those types.
- Sub-signals are counted separately: offscreen, feint-follow, and match-rate spikes are not all equal evidentiary weight.
- History is keyed by GUID and relies on UNIX time rather than mission timer values, so reconnect history survives map changes and restarts within the configured window.
- The join gate checks the permanent seed-mismatch blacklist before whitelist admission; a blacklisted GUID is denied even if also present in the whitelist.

## Reading the Logs

The relevant log format is close to:

```text
anticheat|name|unique_id|ip|type|value|threshold|action
```

The end-of-session summary is also important:

```text
anticheat|summary|reason|name|unique_id|ip|mission=...|detections=...|...
```

The important fields to check are:

- `seed_mismatches`: should stay at zero for honest clients.
- `autoblock_offscreen`: important as a repeated pattern, not as a standalone verdict.
- `autoblock_match_pct` and `autoblock_reaction_ms`: compare with your population baseline.
- `time_skew_max_pct`: repeated positive skew is significant.
- `time_skew_stall_pct`: lag or frame stall, not a speedhack signal.

## Evidence Status

This repo contains the 63rd Server logs from September 11-16, 2026. They document the detector activity, the summary lines, the admin/whitelist events, and the surrounding test or operational conditions.

The current evidence model is intentionally strict:

- [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) contains the confirmed cheater roster.
- The offscreen table in [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) is a detector inventory, not a confirmed-ban list.
- A player with repeated offscreen crossings is not automatically confirmed; corroboration is required.
- The same nickname can appear under different GUIDs. The GUID and raw evidence remain the source of truth.

## Offscreen Caveat

The offscreen signal is kept separate for a reason: higher-than-default FOV settings can create these readings without proof of cheating. The repository therefore records offscreen crossings as observations with the matching detector counts and keeps the confirmed verdicts in the separate roster above it.

This was one of the major corrections in the current documentation: `Flo` and similar low-confidence examples remain in the offscreen inventory, not in the confirmed-cheater list, unless independent evidence such as match-rate spikes, feint-follow crossings, or owner confirmation is present.

## Project Status

This directory is a documentation and log-evidence archive rather than a source distribution:

```text
.
├── ANTICHEAT_SERVER_GUIDE.md   # Server-owner guide
├── MODULE_ANTICHEAT_SPEC.md    # Module System decision/reference document
├── CHEATER_WATCHLIST.md        # Confirmed cheaters + offscreen observations + thanks
├── 63rd Server/                # Dated raw server logs
├── README.md                   # Overview and navigation
└── LICENSE                     # Project license status is described in the docs
```

The open-source portion of this project is the Module System logic. The WSE2 engine itself is not open source and is not published here. The source archive therefore focuses on the module behavior, the server-side configuration model, and the raw evidence that supports the conclusions.

## License and Upstream

The Module System code in this project is released under the [Unlicense](https://unlicense.org/). The WSE2 1.5.2 engine is a non-public, non-open-source build and is not covered by this license grant.

## Forum Thread

https://www.fsegames.eu/forum/index.php?topic=50194.0

## Special Thanks

The current watchlist also records the tester and sponsor contributions that helped validate the detector during calibration. Those names are listed separately from the confirmed cheater roster in [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md).
