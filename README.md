# Dungeon-Larper
That time I got reincarnated as a Dungeon Slime after living my life as a Larper

# UPDATE

### Boss Fight (Room 5)
- The Amalgam Boss has 30 HP, a large 38px hitbox with rotating spikes, and an HP bar above it
- Cycles through weaknesses (Vine/Fire/Droplet) every 4 seconds — shorter as it loses HP
- Fires 3-way projectile spreads that deal 2 damage; spread rate increases as HP drops
- It orbits the player at medium range, making it feel dynamic rather than a punching bag
- Exit stays locked until the boss is dead; killing it awards +500 score

### Score System
- +50 per regular enemy kill, +500 for the boss
- -10 per hit taken (floors at -999)
- Score shown live in the HUD; floating popup text for every gain/loss
- Final score shown on the win/death screen

### Combat Changes
- Attack cooldown of 0.55 seconds — a visible cooldown bar fills under the HUD so timing is always readable
- Single active attack logic: can't queue multiple slashes
- Damage only lands if form matches enemy weakness AND player is in range

### Form Selection
- 1 = Vine, 2 = Fire, 3 = Droplet — only unlocked forms respond
- Q cycling removed entirely

### Progression
- Every room has an EXIT zone on the right wall instead of portal puzzles
- Room 4 and Room 5 EXIT stays locked (grayed out) until combat is cleared

# Audio System Fix

The audio system has been updated to improve stability and ensure that audio settings function correctly.

### Safe Audio Loading

Background music and sound effects are now loaded with proper file validation. Missing audio files no longer cause the game to crash during startup, allowing the game window to open normally even when audio assets are unavailable.

### Sound Effect Integration

Previously unused sound effects (`sfx_slash` and `sfx_hit`) have been connected to the appropriate gameplay events and now play when triggered during combat interactions.

### Functional Volume Control

The `audio_volume` setting (1–5) is now applied to the audio mixer. Changes made through the Settings or Pause menu immediately affect both background music and sound effects.

### Proper Mixer Initialization

The audio subsystem is now initialized using `pygame.mixer.init()` before any music or sound assets are loaded, ensuring more reliable audio playback across different systems and configurations.

## Result

The audio system is now more robust, user settings are respected, sound effects are fully utilized, and missing audio files no longer prevent the game from launching.
