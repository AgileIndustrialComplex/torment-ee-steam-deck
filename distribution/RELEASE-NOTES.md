# PST:EE Xbox Controller Mod 0.3.5 - preview

Xbox/XInput support for the verified Windows x64 PST:EE 3.2.2.0 executable.

## Current features

- LS character/group movement, L3 WALK/RUN and R3 select all.
- Filtered small steering corrections; continuous RUN and preserved WALK
  actions during turns. Releasing the stick stops movement immediately.
- RS world camera, RT+RS zoom and working PC mouse edge scrolling.
- D-pad Up opens Attack and Down opens Select Special Ability in neutral world
  gameplay; menus, radial, dialogue and targeting retain directional navigation.
- Direct white Talk (A), Open (A), Use (A) and Inspect prompts; nearby target cycling.
- Compact opaque two-page radial, centered action name and thin yellow icon frames.
- Mage Book, Priest Book and casting Spells, alongside Inventory, Journal, Map,
  Character, Attack, Talk, Items, Abilities, Rest, Stop, Formation, loot and quick save.
- Menu/slot/list navigation; first carried-item focus and parent focus restoration.
- Inventory Y stack splitting: D-pad quantity, A confirm, B cancel.
- A skips active movies; D-pad selects confirmation buttons, with Quit starting on No.
- Real mouse click returns to PC mode; a controller button/trigger reactivates Xbox.
- No top PC/controller status text. Back/View opens Options; Start pauses.

## Changes in 0.3.5

- **Conversation follows the chat.** The mod no longer forces the chatbox to
  its "locked at bottom" state while an answer is selected: new lines scroll
  into view on their own again, and advancing with A lands on the latest text.
- **Left stick scrolls the conversation.** In dialogue, pushing LS up/down moves
  through the history at a readable pace; releasing it stops where you are. RS
  stays the free cursor.
- **Walk or run follows the stick.** A slight tilt walks, pushing through runs
  (with hysteresis so the boundary does not flap). L3 no longer toggles a
  persistent walk/run mode.
- **The stick moves the Nameless One, companions follow him.** Flow steering
  now drives only the first selected sprite - the engine's own party-follow
  moves everyone else, so the party stops clumping at doorframes when one
  character clips a corner.

## Changes in 0.3.4

- **D-pad on real hardware.** The evdev reader only understood the D-pad as
  four BTN_DPAD_* keys; pads that report it as a hat (ABS_HAT0X/ABS_HAT0Y) -
  which is how the Deck's controller and Steam's virtual pad present it - left
  the D-pad completely dead while the sticks kept working. Hats are now read
  (against the device's neutral position, not its extremes), the capabilities
  are logged (`direct pad caps:`), and if the opened device advertises no D-pad
  at all the four bits are taken from SDL, which maps hats reliably. Buttons
  are also merged across sources instead of letting one source mask them.
- **Movement stutter.** Flow steering re-planned the route every 70 ms with a
  short goal, which the engine executed as a stop-and-start every tick. It now
  keeps one goal comfortably ahead and only refreshes it on arrival, on a real
  turn, or as a slow safety net: a 4-second hold went from about 57 re-plans
  to 8.
- **Blocked directions.** When the stick points into a non-walkable area the
  engine's pathfinding routes around it, sometimes the wrong way. The bridge now
  watches where the leader actually moved: no progress, or progress against the
  stick, cancels the move and holds for 350 ms - the character stays put instead
  of running the opposite direction, and resumes the moment an open direction is
  pushed.

## Changes in 0.3.3

- **Title screen navigation.** The engine opens its START screen before the mod's
  Lua is loaded, so the main menu never registered as a navigation menu and the
  cursor floated with nothing selected. The start screen is now detected
  directly, New Game is the initial focus, and the cursor settles back onto the
  nearest gem about 180 ms after the sticks rest: exactly one button stays
  selected the whole time while the sticks still aim freely.
- **Flow steering.** Movement no longer chases a distant waypoint that has to be
  re-ordered. The goal now slides with the stick every 70 ms, its length follows
  stick deflection, and each tick prefers to move the live MoveToPoint
  destination, then re-points the sprite's own MoveToPoint, and only then issues
  one appended group order - the route is never cleared while the stick is held.
  Characters track the stick continuously, curve through turns without stopping
  and stop once on release.
- **D-pad dialogue answers.** The answer list's own mouse exit cleared the
  selection every frame, so the D-pad looked dead. The selected answer is now
  re-asserted every tick, up/down clamp to the clickable rows, and an idle chat
  whose rows the engine will not report as clickable speaks the first available
  answer instead of pressing a Continue button the stock UI disables.
- The runtime log records the answer-list shape and the dispatched answer marker
  when they change, and every steering dispatch logs whether it slid a live move,
  re-pointed a sprite or fell back to a group order.
- Windows download links point at the upstream preview that actually exists.

## Changes in 0.3.2

- **Direct evdev pad reader.** SDL's gamecontroller layer depends on a
  mapping database keyed by device GUID, and devices whose layout the
  shipped database does not expect read garbage or nothing at all. The
  bridge now keeps its own pad state straight from /dev/input/event*:
  discovery scans for a device exposing the gamepad button/axis set and
  reads EVIOCGBIT/EVIOCGABS for the real ranges, then kernel events
  update buttons, sticks and triggers directly. Steam Input action
  states still take priority when active; the SDL gamepad remains the
  last fallback. A device can be pinned with PSTPAD_EVENT=/dev/input/
  eventN for fixtures and diagnostics.
- **Diagnostics.** controller-runtime.log now carries a low-frequency
  state line (connection, focus, movie state, button bits, stick and
  trigger values, Steam Input state) and synthesized menu clicks are
  logged like the other native ops.


- **Pad debug overlay on the main menu.** A small readout in the top-left
  corner shows exactly what the mod receives: connection and input source
  (Steam Input / SDL gamepad / no pad), armed/active state, every pressed
  button by name, raw stick values and trigger levels. If the overlay
  shows your presses, input is reaching the mod; if it shows
  "no pad", the bridge sees no controller at all.


- **Native Steam Input.** The bridge resolves the game's own
  `libsteam_api.so` flat API (`SteamAPI_SteamInput_v006`) in-process,
  initializes ISteamInput, loads the mod's action manifest
  (`override/steam_input_manifest.vdf`, one "InGame" action set with
  Move/Camera analog actions, both triggers, and the fourteen digital
  actions), and reads action states directly instead of the emulated
  gamepad when Steam reports a controller with bound actions. Bindings
  you create or edit in Steam's controller configuration apply
  per-action; layouts stop mattering. Without Steam Input (no Steam
  client, no controller, nothing bound) polling falls back to the SDL
  gamecontroller path unchanged.
- **Haptics.** Native op 20 drives `TriggerVibration`; the radial menu
  ticks on every sector/page step and dialogues bump on each advance.
- The pad poll returns three extra values (Steam Input active, gyro
  pitch/yaw angular velocity) that the Lua side can adopt for
  gyro-steered camera work later; existing consumers ignore them.


- **Fixed: no controller input on a real Steam Deck.** The game's `main()`
  only ever initializes SDL with timer/audio/video, and
  `CChitin::initJoysticks()` is an empty stub in this build, so the joystick
  and gamecontroller subsystems never came up: the bridge's pad polling
  returned "no controller" forever on a physical Deck. The bridge now adds
  the subsystems itself (SDL_Init is refcounted and safe to call before or
  after the game's own init) and retries lazily at every poll. The loader
  log gains the joystick count, and the first opened pad is logged by name.
- The installer now upgrades in place when the installed version differs
  from the package version (it removes the old files first, backups kept);
  same-version installs still ask for an uninstall.

## Changes in 0.2.0

- **Native Linux support (Steam Deck default build).** The Linux `Torment`
  binary ships unstripped, so every engine function, global and vtable the
  bridge needs resolves by symbol name from its symbol table
  (`controller-lab/inspect_linux.py` generates the binding table in
  `native/linux_offsets.h`). The full executable SHA-256 and both patch-site
  prologues are verified before anything binds or patches.
- The Linux bridge is a shared object (`override/libpstcontroller.so`) loaded
  through a single `LD_PRELOAD` launch option; the installer maintains a
  space-free symlink and prints the exact line. It hooks `bootstrapLua()` to
  register `PSTPadNative` on the engine's Lua state - the same registration
  the Windows injection performs - so M_PSTPAD.lua stays unchanged. No
  Proton, no separate launcher, no compatibility-tool change.
- Movie A-button skip and post-movie Escape filtering run through a guarded
  patch of `CChitin::ProcessEvents`; cursor updates are suppressed through a
  guarded patch of `CVidMode::SetPointer` while the mod hides the cursor. The
  Windows build's steering wait/face gates and destination-marker gate are
  not ported yet; movement still routes through the stock group order path.
- The stdlib-Python installer now detects the native layout, verifies the
  Linux executable fingerprint, installs the native payload, and imports
  saves from `~/.local/share/Planescape Torment - Enhanced Edition`. The
  Proton/Windows path is unchanged.
- The native bridge's model tests (nearby interactions, 48 WALK/RUN
  renewals, 80 RUN retargets, camera follow/pan/zoom, movie guard) run on
  Linux and in CI: `python3 controller-lab/build_plugin_linux.py --check`.

## Changes in 0.1.31

- Optional existing-save import after interactive installation; decline to keep
  a fresh profile. Command-line installs can request -ImportSaves explicitly.
- Import-Saves.cmd can copy saves later without reinstalling the mod.
- Originals and existing target slots are preserved. Conflicting names get a
  free slot number; identical copies are skipped on repeat imports.
- Complete local slots are copied and hash-verified before publishing. Settings,
  cloud files and incomplete saves are excluded. Copying requires a closed game.
- Controller gameplay and native binaries are unchanged from 0.1.30.

## Changes in 0.1.30

- English-only documentation and source notes, reconciled with all current controls.
- Explicit preview ZIP versus source ZIP installation instructions.
- A source-only/incomplete installer explains the correct download before touching
  a game folder, instead of failing with a missing manifest.json message.
- Clear explanation of the intentional separate save/settings profile and manual
  save copying. Original saves are not deleted or imported automatically.
- Gameplay and native binaries are unchanged from 0.1.29.

Use **PSTEE-Xbox-Controller-v0.3.5-preview.zip** to install (Windows) or the
Deck AppImage / native preview ZIP (Linux). The source ZIP is for
GitHub/building. Close the game, uninstall an older managed version, then install.
Launch through Play-Controller-Mod.cmd or ControllerLab.exe. Disable Steam Input.
Read [README.md](README.md) and [CONTROLS.md](CONTROLS.md).

The installer checks the exact executable fingerprint and derives UI locally.
Game executables, archives, full stock UI, stock icons and saves are not bundled.
Automated checks cover input, navigation, stack splitting, guarded movement,
installer restoration/refusals and archive contents. Selected features have
in-game user validation; a complete campaign/menu audit is still pending.
The author's license choice remains deferred until publication.
