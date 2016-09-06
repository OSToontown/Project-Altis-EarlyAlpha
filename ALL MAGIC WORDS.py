~system
##Broadcast a message to your entire district!

~correctlaff()
##A magic word that attempts to correct a toons laff.
##This includes any external admin modifications to the toon (such as setMaxHp).

~nametag(styleName)
##Set the style of the target's nametag to the specified ID.
##Examples are 100 for basic, 0 for simple.

~animations()
##Unlock all of the animations on the target toon.
##This excludes the "Toons of the world unite!" phrase.

~phrase(phraseStringOrId)
##Unlocks a new phrase and adds it to target's list of "My Phrases".
##If the phrase list is full, the top item will be knocked off and the requested one will be appended to the bottom.

~setCE(CEValue, CEHood, CEExpire)
##Set Cheesy Effect of the target.

~setHp(hpVal)
##Set target's current laff.

~setMaxHp(hpVal)
##Set target's laff.

~setTrackAccess(toonup, trap, lure, sound, throw, squirt, drop)
##Set target's gag track access.

~maxToon(hasConfirmed)
##Max out the toons stats, for end-level gameplay.
##Should only be (and is restricted to) casting on Administrators only.

~setMaxMoney(moneyVal)
##Set target's money and maxMoney values.

~setFishingRod(rodVal)
##Set target's fishing rod value.

~setMaxFishTank(tankVal)
##Set target's max fish tank value.

~setName(nameStr)
##Set target's name.

~setHat(hatId, hatTex=0)
##Set hat of target toon.

~setGlasses(glassesId, glassesTex=0)
##Set glasses of target toon.

~setBackpack(bpId, bpTex=0)
##Set backpack of target toon.

~setShoes(shoesId, shoesTex=0)
##Set shoes of target toon.

~kick(reason)
##Kick the player from the game server.

~ban(reason, confirmed, overrideSelfBan)
##Ban the player from the game server.

~togGM()
##Toggle GM Icon for toon.

~ghost()
##Set toon to invisible.

~badName()
##Set target's name to the 'REJECTED' state and rename them to their <COLOR SPECIES> name.

~setGM(gmId)
##Set the target's GM level (used for icon).

~setTickets(tixVal)
##Set the target's racing ticket's value.

~setCogIndex(indexVal)
##Transform into a cog/suit.

~dna(part, value)
##Set a specific part of DNA for the target toon
##Be careful, you don't want to break anyone!

~setTrophyScore(value)
##Set the trophy score of target.

~givePies(pieType, numPies)
##Give target Y number of X pies.

~setQP(questId, progress)
##Get current questId in progress via ~setQP.
##Set questId progress via ~setQP questId value.

~locate(avIdShort, returnType)
##Locate an avatar anywhere on the [CURRENT] AI.

~online(doId)
##Check if a toon is online.

~unlimitedGags()
##Restock avatar's gags at the start of each round.

~immortal()
##Make target (if 500+) or self (if 499-) immortal.

~sostoons()
##Restock all *good* VP SOS toons.

~unites()
##Restock all CFO phrases.

~summons()
##Restock all CJ summons.

~pinkslips()
##Restock (to 99) CEO pink slips.

~questTier(tier)
##Set toon's tier to specified value. Note that this does not give the
##toon the rewards they would normally require to be in this tier, so
##use this magic word with caution. This will also reset all of the
##target's quests, so they will lose any progress on any tasks that
##they are currently working on.

~tracks(toonup, trap, lure, sound, throw, squirt, drop)
##Set access for each of the 7 gag tracks.

~exp(track, amt)
##Set your experience to the amount specified for a single track.

~disguise(corp, type, level)
##Set disguise type and level.

~merits(corp, amount)
##Set the target's merits to the value specified.

~fanfare()
##Give target toon a fanfare.

~catalog()
##Delivers target's catalog.

~pouch(amt)
##Set the target's max gag limit.

~goto(avIdShort)
##Teleport to the avId specified.

~dump_doId2do()
##Please note that this MW should NOT be used more than it needs to be on a live
##cluster. This is very hacked together and is purely so we can get a dump of doId2do
##to get an idea of where the huge memory usage is coming from.

~pstats(host, port)
##Tell the AI to connect a PStatsClient to the server specified.

~cpu(percpu)
##Return the current CPU usage of the AI server as a percentage.
##This will return a list if percpu is enabled. (~cpu percpu)

~mem()
##Return the current memory usage of the AI server as a percentage.

~garbage(arg)
##Reports the total garbage use for this process.

~heap()
##Counts the number of objects in Python's object memory.

~objects(minimum)
##Write the objects down to log.

~containers(limit)
##Write the container report to log.

~clickNametag(avId)
##Simulate a click on an avatar's nametag, given their ID.

~showTarget()
##Show the moderators current Magic Word target.

~accId()
##Get the accountId from the target player.

~run()
##Toggle "running", which makes you move much faster.

~collisionsOff()
##Turn off collisions. This allows you to run through things, and walk in air.

~collisionsOn()
##Re-enable collisions.

~enableAFGravity()
##Turn on Estate April Fools gravity.

~setGravity(gravityValue, overrideWarning)
##Set your gravity value!

~normalGravity()
##Turn off Estate April Fools gravity.

~getPos()
##Get current position of your toon.

~setPos(toonX, toonY, toonZ)
##Set position of your toon.

~chatmode(mode=)
##Set the chat mode of the current avatar.

~truefriend(avIdShort)
##Automagically add a toon as a true friend.

~oobe()
##Toggle "out of body experience" view.

~oobeCull()
##Toggle "out of body experience" view, with culling debugging.

~wire()
##Toggle wireframe view.

~textures()
##Toggle textures on and off.

~fps()
##Toggle frame rate meter on or off.

~showAvIds()
##Show avId in Nametags.

~showNames()
##Remove avIds in Nametags.

~showAccess()
##Show access level.

~toga2d()
##No explanation.

~placer()
##No explanation.

~explorer()
##No explanation.

~reloadTextures(textureName)
##No explanation.

~gibfish(fishName)
##Sets a flag on the avatar,
##that upon casting a fishing rod (that is valid),
##gives the avatar the requested fish.

~nogibfish()
##Deletes a request for a fish if it exists.

~invasionstatus()
##Returns the number of cogs available in an invasion in a pretty way.

~setBattleSkip(bs)
##Skip battle.

~rollCredits()
##Request that the credits sequence play back.
##This will disconnect you.

~fireworks(showName)
##Start fireworks.

~houseType(type)
##Set target house type (must be spawned!).
##Default (if left blank) is 0 (normal house).

~stopBingo()
##Really? You need an Explanation?

~startBingo()
##Really? You need an Explanation?

~requestBingoCard(cardName, seed)
##Send request for bingo card.

~abortMinigame()
##Abort any minigame you are currently in.

~winMinigame()
##Win the current minigame you are in.

~requestMinigame(minigameName, minigameKeep, minigameDiff, minigamePG)
#Minigame creator.

~leaveRace()
##Leave the current race you are in.

~travel(target)
##Trolley tracks.

~togpop()
##Moderation command to toggle shard population.

~boss(cmd, val, val2)
##A bunch of commands that can be run on the current boss in the invoker's zone.

~spShow()
##Show suit paths.

~spHide()
##Hide suit paths.

~spawn(name, level, specialSuit)
##Spawn cog.

~invasion(cmd, name, num, specialSuit)
##Spawn an invasion on the current AI if one doesn't exist.

~sleep()
##Never fall asleep.

~gardenGame()
##Start garden game. (it isn't as good as Toontown House's, though :P)

~election (state)
##ONLY USABLE DURING THE ELECTIONS
##Start the elections in a certain state.
##States: PreShow, Begin, AlecSpeech, VoteBuildup, WinnerAnnounce, CogLanding, Invasion

~skipCEO
##Skip a ceo round.

~skipVP
##Skip a VP round.

~skipCJ
##Skip a CJ round.

~skipCFO
##You know what this shit does by now, but it skips the CFO.

~endCJ
##Kills the CJ

~endVP
##Kills the VP

~endCEO
##Kills the CEO

~endCFO
##God damn, what do you know, it kills the CFO!

~sos (toon)
##Gives the player the sos toon, such as ~sos flippy

