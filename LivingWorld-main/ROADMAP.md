# Living World — Development Roadmap

This document outlines the 10 development phases for the **Living World** Minecraft Java Edition Fabric mod (Minecraft 1.21.1, Java 21).

---

## Phase Status Summary

| Phase | Description | Status | Key Artifacts |
|---|---|---|---|
| **Phase 1** | Project Foundation | **Completed** | `build.gradle`, `fabric.mod.json`, `livingworld.mixins.json` |
| **Phase 2** | Mob Memory System | **Completed** | `MobMemory`, `MemoryEntry`, `MemoryType`, `MobMemoryManager` |
| **Phase 3** | Mob Reactions | **Completed** | `ReactionType`, `MobReactionHandler` |
| **Phase 4** | Group Behavior | **Completed** | `GroupBehaviorManager` |
| **Phase 5** | World Memory | **Completed** | `WorldMemoryData`, `WorldEventRecord`, `WorldMemoryManager` |
| **Phase 6** | Dynamic Villages | **Completed** | `VillageState`, `VillageSafetyManager` |
| **Phase 7** | World Events | **Completed** | `EventType`, `LivingWorldEvent`, `WorldEventManager` |
| **Phase 8** | Configuration | **Completed** | `ModConfig`, `livingworld.json` |
| **Phase 9** | Debugging & Optimization | **Completed** | `DebugLogger`, spatial throttles, LRU bounds |
| **Phase 10** | Polishing & Integration | **Completed** | `LivingWorld.java`, lifecycle hooks, complete docs |

---

## Detailed Phase Breakdown

### Phase 1: Project Foundation (Completed)
- Gradle and Fabric Loom 1.8 configuration targeting Minecraft 1.21.1 with official Mojang mappings.
- Java 21 source and target compatibility.
- Fabric Loader 0.16.10 and Fabric API 0.107.0+1.21.1.
- Clean manifest (`fabric.mod.json`) and Mixin configuration (`livingworld.mixins.json`).

### Phase 2: Mob Memory System (Completed)
- Bounded mob memory container (`MobMemory`) preventing memory leaks.
- Diverse memory types (`THREAT`, `RECENT_DAMAGE`, `LAST_KNOWN_PLAYER_POS`, `DANGEROUS_LOCATION`, `ALLY_ALERT`).
- Temporal intensity decay with configurable lifetime.
- Non-omniscient perception bounds (maximum visual and acoustic radii).

### Phase 3: Mob Reactions (Completed)
- Tactical mob responses (`MobReactionHandler`) responding to health thresholds and active memories.
- Low health (< 35%) triggers strategic retreat/fleeing.
- High health with remembered threat triggers investigation and repositioning.
- Seamless compatibility with vanilla pathfinding (`mob.getNavigation().moveTo`).

### Phase 4: Group Behavior (Completed)
- Localized social alert propagation (`GroupBehaviorManager`).
- When a mob is attacked, alerts nearby allies within a bounded spherical/AABB box.
- Group dynamics: isolated mobs scatter when outmatched; clustered allies regroup to counter-attack.
- Strict limit on maximum alerted entities per tick to eliminate lag spikes.

### Phase 5: World Memory (Completed)
- Persistent world-level event records (`WorldMemoryData` implementing Minecraft 1.21.1 `SavedData.Factory` and `CompoundTag` NBT storage).
- Survives **SAVE -> EXIT -> RELOAD** cycles cleanly in level storage.
- Records major battles, village sieges, and environmental disturbances with coordinates and intensity.
- Automatic pruning of historical records older than configured retention threshold (default: 7 in-game days).

### Phase 6: Dynamic Villages (Completed)
- Village vigilance manager (`VillageSafetyManager`) tracking village centers.
- Dynamic states: `PEACEFUL`, `ALERT`, `DEFENSIVE`, `COMPROMISED`.
- Iron Golems mobilize proactively towards reported threat coordinates.
- Gradual recovery to peaceful state during sustained tranquility.

### Phase 7: World Events (Completed)
- Controlled emergent world event framework (`WorldEventManager`).
- Events: `MIGRATION_SURGE`, `PREDATOR_PROWL`, `VILLAGE_CURFEW`, `ANCIENT_RESTLESSNESS`, `TRANQUIL_PERIOD`.
- Minimum 5-minute cooldown between events, probability gating, and active player proximity centering.

### Phase 8: Configuration (Completed)
- Zero-dependency JSON configuration system (`ModConfig`) stored in `config/livingworld.json`.
- Configurable memory limits, group alert radii, retention duration, and event frequency.
- Safe fallbacks and boundary validation for missing or corrupted configs.

### Phase 9: Debugging and Optimization (Completed)
- Dedicated diagnostic logger (`DebugLogger`) disabled by default to avoid log spam.
- Spatial math acceleration (`SpatialMath`) minimizing vector allocations.
- 20-tick throttled reaction evaluation around loaded player chunks only.
- Automatic cache eviction on mob death and server shutdown.

### Phase 10: Polishing and Integration (Completed)
- Main Fabric entry point (`LivingWorld.java`) wiring all event listeners cleanly.
- Clean separation of concerns with zero hard dependencies on external mod ecosystems.
