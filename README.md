# WSE2 Anti-Cheat Findings

This repository brings together the design of an anti-cheat system for a non-public WSE2 1.5.2 server
build, real server logs, and the cheater watchlist created during review.

> **What is this repository?** It is not a ready-to-install package. It is a research archive that documents WSE2 anti-cheat behavior, preserves log evidence, and describes the Module System decision logic.

## Start Here

Choose the path that matches your goal:

| Goal | Read |
| --- | --- |
| Enable and calibrate anti-cheat on a server | [ANTICHEAT_SERVER_GUIDE.md](ANTICHEAT_SERVER_GUIDE.md) |
| Understand Module System integration and threat decisions | [MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md) |
| Review accounts confirmed in real sessions | [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) |
| Inspect raw evidence | Dated logs in the [63rd Server](63rd%20Server) directory |

### If you are a server owner

- [ ] Read [ANTICHEAT_SERVER_GUIDE.md](ANTICHEAT_SERVER_GUIDE.md) first.
- [ ] Collect data in silent mode with `iMode=1` for the first week.
- [ ] Build a baseline for your own player population from `anticheat,summary` lines.
- [ ] Compare thresholds against your logs before switching to enforce mode.
- [ ] Enable kick or ban switches one at a time; do not enable all of them simultaneously.

### If you are a Module System developer

- [ ] Read the current source behavior section in [MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md).
- [ ] Verify that `ti_on_cheat_detected` suppresses the native action with `reg0=1`.
- [ ] Evaluate seed mismatch, offscreen autoblock, and positive clock-skew counters separately.
- [ ] Keep JSON configuration, admin GUIDs, and player whitelist responsibilities separate.
- [ ] Compare the documented source differences against the actual code.

### If you are reviewing a log event

1. Use the unique ID rather than the player name; names can change.
2. Do not treat one statistical detection as conclusive evidence.
3. Look for `autoblock_offscreen`, `seed_mismatches`, and repeated detection patterns.
4. Treat negative clock skew as lag, not as evidence of a speedhack.
5. Support every addition to [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) with raw log evidence.

## Project Purpose

The purpose of this work is to record server-observable behavior without installing software on the client or revealing which detector fired. The system is considered in two layers:

1. **WSE2 server detector layer:** The non-public WSE2 1.5.2 engine build collects signals such as seed validation, aim snap, aim lead, spread luck, auto block, auto attack, attack cadence, and client clock skew.
2. **Module System decision layer:** Receives `ti_on_cheat_detected` events and manages detection counters, threat levels, the whitelist, GUID-based history, and silent/enforce behavior.

The central goal is not to punish a player for one suspicious action. It is to measure the statistical range of real players and make stronger decisions from repeated, mutually consistent signals. Deterministic violations such as seed mismatches are handled differently and are treated as zero-tolerance events.

## What Does It Monitor?

| Signal | What it indicates | Confidence note |
| --- | --- | --- |
| Seed mismatch (`type 16`) | The client sent a value different from the server seed | Not statistical; strongest signal |
| Auto block (`type 14`) | Match rate, instant feint-follow, and out-of-view block signals | Read multiple signals together |
| Aim snap (`type 10`) | A sudden look-direction change followed by an attack or shot | High-DPI players can create false positives |
| Aim lead (`type 17`) | Unusually low aim error on difficult moving-target shots | Requires server-specific calibration |
| Spread luck (`type 12`) | Shot spread far below the honest baseline | Complements seed validation |
| Auto attack (`type 15`) | Finding the uncovered side and reacting to feints/chambers | Strong duelists require care |
| Attack cadence (`type 13`) | Suspicious animation speed | Disabled by default; fast weapons can trigger it |
| Clock skew (`type 11`) | Positive client clock deviation | Negative skew is lag; ESP/wallhacks are not detected |
| Client integrity (`types 20-24`) | SDK-defined client module, thread, hook, signature, and text-hash checks | Available in the SDK; runtime behavior is not evidenced by the logs in this archive |

## Decision Flow

```text
WSE2 detector
      |
      v
 ti_on_cheat_detected
      |
      +--> Module System counters and live statistics
      |          |
      |          +--> noise / watchlist / suspected
      |          |
      |          +--> confirmed --> silent: log + alert
      |                         --> enforce: action according to kick/ban settings
      |
      +--> anticheat summary: baseline evidence at exit or mission_end
```

Important behavior:

- `iMode=0`: No measurements are taken.
- `iMode=1`: Measurements, logs, and the module trigger run; there are no kicks or bans.
- `iMode=2`: Enforcement can be applied when a configured threshold is crossed.
- There is no general anti-cheat verdict at join time; detectors need gameplay samples.
- GUID-based history can be restored after reconnecting within a short time window.
- When player-whitelist admission is enabled, unlisted players cannot join; the whitelist does not bypass anti-cheat.

## Reading the Logs

Detection records generally contain these fields:

```text
anticheat|name|unique_id|ip|type|value|threshold|action
```

Summary records are written for every player at the end of a session:

```text
anticheat|summary|reason|name|unique_id|ip|mission=...|detections=...|...
```

Start with these fields:

- `seed_mismatches`: Expected to be zero for an honest client.
- `autoblock_offscreen`: Read as a repeated pattern supported by other signals, not in isolation.
- `autoblock_match_pct` and `autoblock_reaction_ms`: Compare them with your player-population baseline.
- `time_skew_max_pct`: Repeated positive deviation is significant.
- `time_skew_stall_pct`: Lag or frame-stall information; it should not be a ban reason.

The sample logs contain silent-mode detections recorded as `logged`, while summary lines also include players who never triggered a detector. This makes the system useful for measuring normal player behavior, not only suspected cheaters.

## Evidence Status

This repository contains 63rd Server logs dated September 11-16, 2026. They show detection records, player summaries, admin-whitelist events, and the surrounding test or operational conditions. [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) is the short list of accounts considered confirmed from real sessions.

This list is not a universal cheat database or a legal judgment. The same name can appear with different GUIDs, so reviews should preserve both the GUID and the raw log evidence.

## Known Limitations and Risks

- ESP and wallhacks are invisible to the server; this version does not detect them.
- The WSE2 SDK defines client-integrity detections for client modules, threads, hooks, signatures, and text hashes (`types 20-24`). This archive does not include the non-public engine source or log evidence proving which of these checks are active in the deployed build; their runtime behavior must be verified against that build before being treated as enabled or disabled.
- Statistical detectors can produce false positives; enforcement must not be enabled without calibration.
- Bans are tied to the unique ID and may be bypassed with another serial key or a VPN.
- The source may not exactly match this archive's specification. Documented differences include the seed mismatch counter not being incremented, the JSON clock threshold not being used by the handler, the `max_matchrate_spikes` setting not being read, and the whitelist file being recreated.
- [CHEATER_WATCHLIST.md](CHEATER_WATCHLIST.md) references `CHEAT_TEST_FINDINGS.md`, which is not present in the current file tree. Use the available server logs as the source for full evidence until that file is added.

## Project Status

This directory is currently more of a documentation and log-evidence archive than a source distribution:

```text
.
├── ANTICHEAT_SERVER_GUIDE.md   # Server-owner guide
├── MODULE_ANTICHEAT_SPEC.md    # Module System decision and integration reference
├── CHEATER_WATCHLIST.md        # Short confirmed-account list
├── 63rd Server/                # Dated raw server logs
└── README.md                   # This overview and navigation document
```

The non-public WSE2 1.5.2 engine automatically creates `server_config.ini`, `anticheat_config.json`,
admin GUID, and player-whitelist files. WSE2 itself is not open source and its engine source will not be
published. The open-source Module System code and its decision logic are documented in
[MODULE_ANTICHEAT_SPEC.md](MODULE_ANTICHEAT_SPEC.md). This README is therefore a navigation point for
the available evidence and technical decisions rather than a setup guide with installation commands.

## Project Decisions

The current project scope and distribution decisions are:

- The project uses a non-public WSE2 1.5.2 engine build.
- WSE2 is not open source and its engine source code will not be published.
- Only the Module System implementation is open source; it is documented in `MODULE_ANTICHEAT_SPEC.md`.
- The WSE2 engine creates the server configuration, anti-cheat configuration, admin GUID, and player-whitelist files automatically.
- Silent mode is the default operating goal for observation and evidence collection.
- IP bans, admin notifications, and log parsers are within the scope of this project.
- The documentation will remain in English for the WSE2 community.
- `CHEAT_TEST_FINDINGS.md` will not be added. The dated server logs and `CHEATER_WATCHLIST.md` are the maintained evidence sources.

## License and Upstream

The Module System code in this project is open source and released under the
[Unlicense](https://unlicense.org/). WSE2 1.5.2 is a non-public, non-open-source engine build and is not
part of this license grant.

## Forum Thread
https://www.fsegames.eu/forum/index.php?topic=50194.0
