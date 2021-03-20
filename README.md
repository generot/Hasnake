# Hasnake
Hasnake is a pure-impure functional scripting language based on Haskell, implemented in Python. It supports and even builds on top of the already existing Standard Haskell base syntax. It serves as my second semester "Scripting languages" project.
## Overview
While Hasnake, like Standard Haskell, is mostly a pure functional language, it supports impure functionalities within their pure counterparts.<br>
That means that I/O within pure functions returns results which can be used within the very same function without wrapping the impurities in a do-block. These innovations will ease the user's life marginally, since do-blocks will no longer be needed to access impure results(i.e. IOString, etc.).
## Documentation
As of now, there is no documentation describing the Hasnake language.<br>
After the project is entirely implemented, a proper documentation will be released.
