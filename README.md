# Hλsnake
![logo](https://repository-images.githubusercontent.com/349798787/da66a280-89d9-11eb-8e54-3f066a9d5d28)

Hasnake is a pure-impure functional scripting language based on Haskell, implemented in Python. It supports and even builds on top of the already existing Standard Haskell base syntax. It serves as my second semester "Scripting languages" project.
## Overview
While Hasnake, like Standard Haskell, is mostly a pure functional language, it supports impure functionalities within their pure counterparts.<br>
That means that I/O within pure functions returns results which can be used within the very same function without wrapping the impurities in a do-block. These innovations will ease the user's life marginally, since do-blocks will no longer be needed to access impure results(i.e. IOString, etc.).
## Documentation
Check the 'docs' folder for a full documentation on the Hasnake language or click [here](https://anomalouss247.gitbook.io/hasnake/) for an online documentation.<br>
