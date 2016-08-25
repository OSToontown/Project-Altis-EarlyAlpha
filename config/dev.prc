# Distribution:
distribution dev

# Art assets:
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
vfs-mount resources/phase_14 /phase_14
vfs-mount resources/server /server
model-path /


# Better GL performance
gl-finish #f
gl-force-no-error #t
gl-check-errors #f
gl-force-no-flush #t
gl-force-no-scissor #t
gl-debug #f

text-minfilter linear
text-magfilter linear
text-page-size 128 128

show-frame-rate-meter #t

texture-anisotropic-degree 0
texture-magfilter linear
texture-minfilter linear
lock-to-one-cpu #f
support-threads #t
gl-immutable-texture-storage #t
gl-dump-compiled-shaders #f
gl-cube-map-seamless #t

# No stack trace on assertion
assert-abort #f

# File system should be case sensitive
# NOTICE: Set this to #f if you are using tempfile. Because it returns
# wrong cased directory paths :(
vfs-case-sensitive #f

# Trying this for performance
uniquify-transforms #t
uniquify-states #t

# Frame rate meter
frame-rate-meter-milliseconds #f
frame-rate-meter-update-interval 1.0
frame-rate-meter-text-pattern %0.2f fps
frame-rate-meter-ms-text-pattern %0.3f ms
frame-rate-meter-layer-sort 1000
frame-rate-meter-scale 0.04
frame-rate-meter-side-margins 0.4

# No stencil
support-stencil #f
framebuffer-stencil #f

# Framebuffers use SRGB
framebuffer-srgb #f

# Framebuffers need no multisamples
framebuffer-multisample #f
multisamples 0

# Don't rescale textures which are no power-of-2
textures-power-2 none

# Server:
server-version 1.0.0
min-access-level 700
accountdb-type developer
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass file:
dc-file dependencies/astron/dclass/altis.dc

# Core features:
want-pets #t
want-parties #f
want-cogdominiums #t
want-lawbot-cogdo #t
want-anim-props #t
want-game-tables #t
want-find-four #t
want-chinese-checkers #t
want-checkers #t
want-house-types #t
want-gifting #t

# Chat:
want-whitelist #f
want-sequence-list #f

# Developer options:
show-population #t
want-instant-parties #t
want-instant-delivery #t
cogdo-pop-factor 1.5
cogdo-ratio 0.5
default-directnotify-level info
