# School Project for Open Day #

This Minecraft 1.19.4 Forge Mod sends http post requests each time the player gets healed or takes damage.
This post request simply contains (as a string) the value of health the player has after applying heal/damage changes.
When the request is accepted by server, it processes the information and sends the number of leds to turn on to the arduino.

# Note: The Http Server (python) and Arduino Script are contained in the "ext" folder
