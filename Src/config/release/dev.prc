# Distribution:
distribution dev

# Art assets:
model-path ../resources

# Server:
server-version altis-dev
accountdb-type local
shard-low-pop 50
shard-mid-pop 100

# RPC:
rpc-server-secret rpcisgreat123456
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/

# DClass files (in reverse order):
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Core features:
want-pets #t
want-parties #f
want-cogdominiums #f
want-achievements #f
cogdo-want-barrel-room #t 
want-butterflies #t

want-sellbot-cogdo #t
want-lawbot-cogdo #t
want-game-tables #t

#Till we fix
want-phone-quest #f

# Chat:
want-whitelist #t

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Optional:
want-yin-yang #f

#Temporary
want-phone-quest #f
gl-force-no-flush #t
gl-max-errors -1
adaptive-lru-max-updates-per-frame 1
prefer-single-buffer #f
rescale-normals none
display-list-animation 1
display-lists 1

# Developer options:
show-population #t
force-skip-tutorial #t
want-instant-parties #t

#Holidays
want-halloween #f
want-christmas #f
want-old-fireworks #f