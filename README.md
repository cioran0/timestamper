I always wind up getting out my epoch calculator when I run my weekly music trivia night on thursdays on my discord server. And it's annoying to tab away and convert and figure ut GMT/UTC and what timezone, so I figured I'd come up with a bot that takes care of that where you just enter in your localtime what time something is at. It spits out the epoch time, which discord uses for the UTC, which it then will convert into each user's localtime. Basically I obviate most of the timezone stuff using python's "date" library functionality. This runs locally. 

I tried some others, but most of them don't even have basic errorchecking. This has a the leap year algorithm and related validation and checking implemented. I'm sure there are still some problems, but I ironed out most of them.

The timestamper bot uses discord.py and the API. Takes a time in your localtime in 24H time mm/dd/yy and converts it to a discord usable epoch timestamp in the format <t:xyz > which can be easily copypasted and a verification next to it. The only library I used was python's "time" besides "discord" and "asyncio" which you need for a discord bot. datetime actually makes it more complicated with timezones and naive and non-naive functionality. Has an algorithm that accounts for leap year and related to prevented odd errors. Credit me if you use it. Feel free to messgae me with questions. MIT license.

Have fun!
