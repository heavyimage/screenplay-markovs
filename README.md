An unholy mashup of screenplay parsing ([jouvence](https://bolt80.com/jouvence/)) and markov chain production ([markovify](https://github.com/jsvine/markovify), [spaCy](https://spacy.io/)), this program analyzes TV / Film scripts, finds recurring characters, and build markov models that generate text which sounds like them.

I used to think markov chain output was just total nonsense but it turns out that if characters written differently enough, it's very easy to see differences in chains built from their dialog!

# Sample Output
This program was built using the scripts from Star Trek: TNG; I hope it isn't overfit for that dataset...

> Rather than excitement or anticipation at being rescued, I sense a ... presence on the planet.
>
> &mdash;<cite>Troi</cite>

> If you ever need help just use one of the planets in the Mericor system.
>
> &mdash;<cite>Riker</cite>

> I thought he should run an Ico - spectrogram run on the Selcundi Drema system.
>
> &mdash;<cite>Wesley</cite>

> It's tough to get accurate sensor readings ... there's no way it could affect something up on Deck Twelve.
>
> &mdash;<cite>Geordi</cite>

> You did know he's attracted to me -- his thoughts became truly pornographic.
>
> &mdash;<cite>Lwaxana Troi</cite>

> I have more than I dreamed possible, my brother, I spent nearly two years drifting in space.
>
> &mdash;<cite>Lore</cite>

> You kind of enjoy it, don't look at me.
>
> &mdash;<cite>Guinan</cite>

# Instructions
* (pip3) install jouvence, spacy, markovify
* run `python3 -m spacy download en` to download the english model
* Download some TV / Film scripts and extact them as a series of plain text files in the "scripts" directory
* Fix any insane unicode / line ending problems -- this script isn't that robust in that department yet...
* Run the python script to read the scripts / train the models (this may take some time!)
* Now that you've got cached per-character models, you can load them in and generate text!

# Ideas:
* Use for twitter bots.
* Use for 'which character guessing game'.
* Use to check your own scripts for saminess; do your characters "sound" different?

# Caveats + Tweaks
* Parsing scripts is not a solved problem; depending on the script quality you may get some parsing errors / stage directions that parse as character dialog.  In particular, the jouvence parser requires proper screenplay formatting -- whitespace matters and is used to help it determine the types of blocks in a script which this program relies on.
* The output of the chain puts spaces in some strange places, often around punctuation marks.  Fixing this is left as an exercise to the forker :-)
* Determining which characters are important is hard based on show type / scale.  Currently, deems any character with > 100 lines a "major" character but this might be wrong.  Another approach might be to take the top N characters by number of lines.
* There are a lot of options for how to construct models once all the text is parsed out; more reading [here](https://github.com/jsvine/markovify/blob/master/README.md).

## Resources
* [SpaCy and Markovify for maximum hilarity](https://joshuanewlan.com/spacy-and-markovify)
* [Create a twitter bot using these methods](https://github.com/cdorsey/twitter-simulator)
* [More about spaCy](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)
