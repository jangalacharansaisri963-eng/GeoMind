# Living World — Minecraft Java Edition Mod

**Living World** is a production-quality Minecraft Java Edition mod built on the **Fabric** toolchain. Its primary goal is to make Minecraft feel like a living world that remembers events, reacts to players, develops changing behaviors, and produces believable emergent situations — enhancing vanilla Minecraft rather than replacing it.

---

## Technical Specifications

- **Target Minecraft Version**: `1.21.1`
- **Mod Loader**: `Fabric` (Loader `>=0.16.10`)
- **Fabric API**: `0.107.0+1.21.1`
- **Build System & Loom**: `Fabric Loom 1.8.11` / `Gradle 8.10.2`
- **Java Version**: `Java 21` (Source & Target compatibility 21, toolchain release 21)
- **Mappings**: Mojang Official Mappings (`mappings loom.officialMojangMappings()`)

---

## Mod Identity

- **Mod Name**: Living World
- **Mod ID**: `livingworld`
- **Root Package**: `com.livingworld`
- **License**: MIT

---

## Architecture & Subsystems

```
src/main/java/com/livingworld/
├── LivingWorld.java                 # Main Fabric ModInitializer and lifecycle wiring
├── behavior/
│   ├── MobReactionHandler.java      # Tactical responses to health, memories & traits
│   └── ReactionType.java            # Reaction taxonomy (FLEE, INVESTIGATE, PURSUE, etc.)
├── command/
│   └── LivingWorldCommands.java     # In-game Brigadier commands (/livingworld ...)
├── config/
│   └── ModConfig.java               # Config manager for config/livingworld.json
├── debug/
│   └── DebugLogger.java             # Config-gated diagnostic logger
├── ecology/
│   └── EcologyManager.java          # Wildlife weather shelter & grazing behaviors
├── event/
│   ├── EventType.java               # Emergent situation categories
│   ├── LivingWorldEvent.java        # Localized active event instance
│   └── WorldEventManager.java       # Cooldown-guarded event scheduler
├── group/
│   └── GroupBehaviorManager.java    # Localized ally alert and group dynamics
├── memory/
│   ├── MemoryEntry.java             # Individual decayed memory unit with intensity
│   ├── MemoryType.java              # Taxonomy (THREAT, DAMAGE, PLAYER_POS, ALLY_ALERT)
│   ├── MobMemory.java               # Per-mob bounded memory container
│   └── MobMemoryManager.java        # Server-wide registry with LRU bounds
├── reputation/
│   ├── PlayerReputationRecord.java  # Player karma score and action counter
│   ├── PlayerReputationData.java    # SavedData & Codec persistence for player karma
│   └── PlayerReputationManager.java # Karma modifier on kills, defenses and raids
├── traits/
│   ├── MobTrait.java                # SKITTISH, AGGRESSIVE, GUARDIAN, CURIOUS, STOIC
│   └── MobPersonalityManager.java   # Deterministic trait assigner based on UUID
├── util/
│   └── SpatialMath.java             # Fast squared distance & proximity checks
├── village/
│   ├── VillageSafetyManager.java    # Village threat tracker & golem alerting
│   └── VillageState.java            # PEACEFUL, ALERT, DEFENSIVE, COMPROMISED
└── world/
    ├── WorldEventRecord.java        # Serializable historical event record
    ├── WorldMemoryData.java         # SavedDataType & Codec persistence (SAVE/LOAD)
    └── WorldMemoryManager.java      # Historical world event coordinator
```

---

## Key Features

1. **Short-Term Mob Memory & Trauma Decay**:
   - Entities form individual memory records when damaged or when spotting threats.
   - Memories retain location, intensity, and decay progressively over 60 seconds (configurable).
2. **Individual Mob Traits & Personalities**:
   - Mobs possess innate personalities (`SKITTISH`, `AGGRESSIVE`, `GUARDIAN`, `CURIOUS`, `STOIC`).
   - Traits influence fleeing thresholds, pursuit vigor, and assist ranges.
3. **Group Dynamics & Ally Alerts**:
   - When attacked, mobs broadcast panic/distress signals to nearby kindred within 16 blocks.
   - Throttled alerting prevents cascade storms.
4. **Dynamic Village Vigilance & Iron Golem Mobilization**:
   - Villages maintain dynamic safety states: `PEACEFUL`, `ALERT`, `DEFENSIVE`, `COMPROMISED`.
   - Iron Golems actively dispatch to reported breach positions.
5. **Player Karma & Regional Reputation**:
   - Defending villagers and slaying hostiles earns karma ("Hero of the Realm", "Trusted Friend").
   - Slaughtering villagers or peaceful wildlife incurs severe karma penalties ("Feared Outlaw", "Notorious Marauder").
   - Saved across server restarts using Minecraft 1.21.1 `SavedData.Factory` and `CompoundTag` NBT storage.
6. **Wildlife Ecology & Weather Sensitivity**:
   - Animals detect rain and thunderstorms and actively seek tree canopies and overhangs.
7. **In-Game Brigadier Commands**:
   - `/livingworld status`: Check active tracked memories and emergent world situations.
   - `/livingworld reputation`: Inspect your karma level and titles.
   - `/livingworld events`: Browse historical battles and notable world events.

---

## Building

```bash
# Build mod JAR with Gradle and Java 21
./gradlew build
```
Artifacts are generated in `build/libs/`.
