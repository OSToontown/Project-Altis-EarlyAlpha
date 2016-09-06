# Client settings
window-title Project Altis
server-version 1.0.0
build-version dev
sync-video #f
# want-dev breaks the game. Don't use it.
want-dev #f
preload-avatars #t
texture-anisotropic-degree 16
icon-filename phase_3/etc/icon.ico
audio-library-name p3fmod_audio
default-directnotify-level info
smooth-lag 0.4
# Pretty sure you're gonna want membership...
want-membership #t
exec-chat #t
want-doomsday #f
want-toonfest #f

# VFS for resources.
vfs-mount resources/phase_3 /phase_3
vfs-mount resources/phase_3.5 /phase_3.5
vfs-mount resources/phase_4 /phase_4
vfs-mount resources/phase_5 /phase_5
vfs-mount resources/phase_5.5 /phase_5.5
vfs-mount resources/phase_6 /phase_6
vfs-mount resources/phase_7 /phase_7
vfs-mount resources/phase_8 /phase_8
vfs-mount resources/phase_9 /phase_9
vfs-mount resources/phase_10 /phase_10
vfs-mount resources/phase_11 /phase_11
vfs-mount resources/phase_12 /phase_12
vfs-mount resources/phase_13 /phase_13
model-path resources
default-model-extension .bam

# Needed for running a local server...
eventlog-host 127.0.0.1

# Distributed Class File
dc-file config/ProjectAltis.dc

# Game Features
want-estates #t
# They work fine.
want-clarabelle-voice #t
# Enables Clarabelle's voice from TTR.
want-pets #f
want-news-tab #f
want-news-page #f
# These work fine, but I dont know if they would be very useful
want-accessories #t
# Occasional AI Crash
want-parties #t
# Kinda unfinished.
want-gardening #f
# Not implemented.
want-gifting #f
# Not needed.
want-cogdominiums #t
# These also work!
want-boarding-groups #t
want-cheesy-expirations #t
want-toontorial #f
want-code-redemption #t
# Works great!
want-new-toonhall #t
want-picnic-games #f

want-map-hover #f
want-tto-loading-screen #f
want-tto-text #f
want-tto-theme #f
want-tto-catalog #f
want-old-fireworks #f
# TTO fireworks.
want-tto-runsound #f
# Run sound from TTO that makes the toons sound like they're running at 9001 MPH.

# Playgrounds
want-playgrounds #t
want-toontown-central #t
want-donalds-dock #t
want-daisy-gardens #t
want-minnies-melodyland #t
want-the-brrrgh #t
want-donalds-dreamland #t
want-goofy-speedway #t
want-acorn-acres #t
want-mini-golf #t

# Cog HQs
want-cog-headquarters #t
want-sellbot-hq #t
want-cashbot-hq #t
want-lawbot-hq #t
want-bossbot-hq #t


# Misc. Modifications
estate-day-night #t
want-instant-parties #t
show-total-population #f

# Chat Features-- These should remain untouched. As this is an offline game, we do not need a whitelist.
want-whitelist #f
force-avatar-understandable #t
force-player-understandable #t

# Makeshift Holiday Manager
force-holiday-decorations 6
active-holidays 63, 64, 65, 66
want-arg-manager #t
want-mega-invasions #f
mega-invasion-cog-type tm
