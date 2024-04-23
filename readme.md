# Blackjack Cheats - Works Everywhere (we used at stake.com)
[Join the Discord](https://discord.gg/rootkitorg)

### Read this you idiot
Gambiling is bad and you will typically always lose in the long run. **You are not special, just very stupid.**

If you use your programming skills, you might be able to find a way to beat the odds, and bot it. Basically printing money. 

You probably are not that smart or good at programming though, or don't understand the underlying metrics/statics if you think this will be easy or will make you money out of the box.

If you like spending money, you can do it by donating to us. So at least you will be helping a charity and get a tax break.

### For the real fun
Ok, well if you now understand you are a idiot, and you will most likely lose money, we can chat about how to use it.

#### Simulator
Will add more to it later. Check out the `main.py`, it is what you configure. The `blackjack.py` file is the lib for how the game works.

Run it easily by
1. `cd` into the simulator folder
2. If you haven't already, run `pip install -r requirements.txt`. Only need to do 1x
3. Run `python main.py`
4. This will also output graphs using matplotlib. Check the folder for the images.

#### Card Counter
This is a website that allows you to easily count cards in your game. It is set up for the hi-lo method.

They keys Z, X, C are hotkeys with the following bindings.
- Z - 2-6
- X - 7-9
- C - 10+

It's best to use the keybinds in real games since it is way faster than doing the button presses.

Run the website by first
1. Make sure you have node.js installed
2. `npm i`
3. `npm run dev` or `npm run build` + `npm run start`