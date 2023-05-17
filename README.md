# FootBall LLM Commentary
PoC for generation of automated commentary for a football game simulation based on current game context.

## Process
1. Before a game run a call is made to a language model to generate a commentary template for the game. The template contains the text for the commentary and the trigger (python snippet which takes game state as input) for the commentary.
2. Tortoise-tts converts the commentary template to speech using TTS.(Scope for Improvement: Improve prosidy)
3. At each time step the trigger is evaluated and if it is true the commentary is played. To prevent the commentary from being played multiple times for the same trigger, the last time the commentary was played is stored in the game state and the trigger is evaluated only if the time since the last commentary is greater than a threshold.

## Future Steps
1. Generate multiple commentary templates to make it more interesting.
2. Fine tune the language model to generate better commentary templates.
3. Improve prosidy of the commentary.
4. Add more triggers to the commentary templates.