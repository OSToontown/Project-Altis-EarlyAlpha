# Window settings:
window-title Project Altis
win-origin -1 -1
icon-filename phase_3/etc/icon.ico
cursor-filename phase_3/etc/toonmono.cur

# Audio:
audio-library-name p3fmod_audio

# Graphics:
aux-display pandagl
aux-display pandadx9
aux-display p3tinydisplay

# Quality...
framebuffer-multisample 1
multisamples 2

# Models:
model-cache-models #f
model-cache-textures #f
default-model-extension .bam

# Textures:
texture-anisotropic-degree 16

# Preferences:
preferences-filename preferences.json

# Content packs:
content-packs-filepath contentpacks/
content-packs-sort-filename sort.yaml

# Backups:
backups-filepath backups/
backups-extension .json

# Server:
server-timezone EST/EDT/-5
server-port 7199
account-server-endpoint https://toontowninfinite.com/api/
account-bridge-filename astron/databases/account-bridge.db

# Performance:
sync-video #f
texture-power-2 none
gl-check-errors #f
garbage-collect-states #f

# Egg object types:
egg-object-type-barrier <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend }
egg-object-type-trigger <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend intangible }
egg-object-type-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend }
egg-object-type-trigger-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend intangible }
egg-object-type-floor <Scalar> collide-mask { 0x02 } <Collide> { Polyset descend }
egg-object-type-dupefloor <Scalar> collide-mask { 0x02 } <Collide> { Polyset keep descend }
egg-object-type-camera-collide <Scalar> collide-mask { 0x04 } <Collide> { Polyset descend }
egg-object-type-camera-collide-sphere <Scalar> collide-mask { 0x04 } <Collide> { Sphere descend }
egg-object-type-camera-barrier <Scalar> collide-mask { 0x05 } <Collide> { Polyset descend }
egg-object-type-camera-barrier-sphere <Scalar> collide-mask { 0x05 } <Collide> { Sphere descend }
egg-object-type-model <Model> { 1 }
egg-object-type-dcs <DCS> { 1 }

# Safe and Cog zones:
want-safe-zones #t
want-toontown-central #t
want-donalds-dock #t
want-daisys-garden #t
want-minnies-melodyland #t
want-the-burrrgh #t
want-donalds-dreamland #t
want-goofy-speedway #t
want-outdoor-zone #t
want-golf-zone #t
want-cog-headquarters #t
want-sellbot-headquarters #t
want-cashbot-headquarters #t
want-lawbot-headquarters #t
want-bossbot-headquarters #t

#Safezone Settings
want-treasure-planners #t
want-suit-planners #t
want-butterflies #f
want-new-toonhall #t

# Classic characters:
want-classic-chars #f
want-mickey #f
want-donald-dock #f
want-daisy #f
want-minnie #f
want-pluto #f
want-donald-dreamland #f
want-chip-and-dale #f
want-goofy #f

#Core Game Features
want-parties #f
want-game-tables #t
want-resistance-toonup #f
want-resistance-restock #f
want-resistance-dance #f
base-xp-multiplier 3
want-cogbuildings #t
show-total-population #t
want-mat-all-tailors #t
want-long-pattern-game #f
want-talkative-tyler #f
want-yin-yang #f
want-toonhall-cats #t
estate-day-night #t
want-gifting #f
want-old-fireworks #t
want-phone-quest #f
want-live-updates #t
force-skip-tutorial #t
want-minigames #t
want-photo-game #f
want-travel-game #f
want-pets #t
cogdo-want-barrel-room #t 
want-butterflies #t
want-sellbot-cogdo #t
want-lawbot-cogdo #t
show-population #t

# Developer options:
want-dev #f
want-pstats 0

# Temporary:
smooth-lag 0.4
gl-force-no-flush #t
gl-max-errors -1
adaptive-lru-max-updates-per-frame 1
prefer-single-buffer #f
rescale-normals none
display-list-animation 1
display-lists 1

#Holidays
want-halloween #f
want-christmas #f
want-old-fireworks #f