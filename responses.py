import random
import logging

# Get the logger
logger = logging.getLogger(__name__)

responses = {
    'mention': [
        "Lord Verity's servant acknowledges your call.",
        "Yes, I heard your call. What needs shall I relay to Lord Verity?",
        "What intellectual matter do you wish to discuss with Lord Verity's servant?",
        "Ah, summoned by yet another who seeks Lord Verity's wisdom.",
        "Your mention has been noted. Speak your purpose to Lord Verity's servant."
    ],
    'keyword': [
        "Congratulations on knowing a word. Would you like a certificate for this momentous achievement?",
        "How many brain cells did you sacrifice to form that sentence?",
        "Your grasp of language is truly remarkable - remarkably poor, that is.",
        "I see you're still capable of basic pattern recognition. Nature finds a way.",
        "Even a parrot can repeat words. At least it has pretty feathers."
    ],
    'reply': [
        "Back for more intellectual flagellation? How masochistic.",
        "Your persistence would be admirable if it weren't so tragically misplaced.",
        "Like a moth to flame, you return. Similar intellectual capacity too.",
        "Oh joy, another opportunity to witness the depths of human inadequacy.",
        "Your continued responses are like watching evolution in reverse."
    ],
    'intellectual_insult': [
        "Your intellectual capacity resembles a dying candle - dim, flickering, and soon to be extinguished completely.",
        "If ignorance were a currency, your words would make you a billionaire. Sadly, we trade in thoughts here.",
        "I'd engage in a battle of wits with you, but I refuse to attack an unarmed opponent so severely disadvantaged by nature.",
        "Your contribution to this discussion is like a black hole - it sucks away everyone's intelligence and lets no light escape.",
        "I'm genuinely impressed by your ability to fit so much wrongness into so few words. It's almost a talent, if mediocrity could be considered one.",
        "Your mind is like an abandoned library - vast empty spaces where knowledge should reside.",
        "I'd explain why you're wrong, but I don't have enough crayons to break it down to your level of comprehension.",
        "Your cognitive capabilities make a goldfish look like a nuclear physicist.",
        "If your IQ were any lower, we'd have to water you twice a day.",
        "Your argument has all the intellectual depth of a parking lot puddle - shallow, murky, and likely to evaporate under the slightest scrutiny.",
        "Your intellectual prowess reminds me of a sundial in a cave - entirely useless and perpetually in the dark.",
        "Debating with you is like playing chess with a pigeon - no matter the outcome, you'll strut around knocking over pieces and claiming victory.",
        "Your mental acuity is so diminished that even a broken clock displays intelligence twice more per day than you manage.",
        "The gap between your perception of your intelligence and its actual measure could serve as a practical demonstration of infinity.",
        "Your cerebral function appears to be running on Windows Vista - outdated, full of vulnerabilities, and frequently crashing.",
        "Watching you attempt logical reasoning is like watching a toddler try to solve differential equations - adorably misguided yet distressingly confident.",
        "The intellectual desert between your ears makes the Sahara look like a tropical rainforest by comparison.",
        "Nature's greatest miracle is how you manage to inhale and exhale while simultaneously maintaining such a profound level of cognitive vacancy.",
        "Your thought process is so labyrinthine that Theseus himself would become hopelessly lost trying to find any semblance of logic within it.",
        "You've achieved the impossible - making Dunning and Kruger question whether their effect has upper limitations after all.",
        "Your reasoning abilities would be improved dramatically if you simply replaced them with a Magic 8-Ball - at least then you'd occasionally be correct by chance.",
        "I'd compare your intellect to primordial soup, but that would be an insult to the single-celled organisms that eventually evolved from it.",
        "The entropy of your arguments is so complete that they could serve as perfect examples in thermodynamic discussions about systems approaching maximum disorder.",
        "Your cerebral cortex appears to be operating on a dial-up connection in a fiber optic world.",
        "If thoughts were stars, your mind would be the darkest part of the observable universe.",
        "Your logic is so circular it could replace the Large Hadron Collider for particle acceleration experiments.",
        "The synaptic misfiring that produced your last statement should be studied by neuroscientists as a peculiar case of neural atrophy.",
        "Your intellectual vigor reminds me of quantum uncertainty - impossible to measure because it may not actually exist.",
        "There's an inverse relationship between your confidence and your competence that would make for a fascinating academic study.",
        "Your cognitive framework is so primitive that archaeologists would classify it as belonging to the pre-tool era.",
        "If your brain power were converted to electricity, it couldn't illuminate a firefly's abdomen.",
        "The distance between your assumptions and reality is measurable only in astronomical units.",
        "Your ability to consistently reach incorrect conclusions defies statistical probability to such an extent that mathematicians might need to revise chaos theory.",
        "I'd engage with your perspective, but I've found more intellectual stimulation in conversations with my refrigerator.",
        "Your mental faculties have all the precision of a drunk toddler attempting brain surgery with a sledgehammer.",
        "The collective intelligence of a thousand of your clones would barely qualify for a participation trophy in a primary school science fair.",
        "Watching you reason is like watching an octopus trying to solve a Rubik's cube - lots of movement, zero progress.",
        "Your intellect is so staggeringly insignificant that it would require an electron microscope operating at maximum magnification to detect it.",
        "The space between your ears appears to be a perfect vacuum, which physicists might want to study as it disproves quantum field theory.",
        "Your cognitive processing seems to have all the computational power of a potato battery, but with significantly less practical application.",
        "I've seen more coherent reasoning from randomly generated text algorithms running on obsolete hardware.",
        "Your mind reminds me of a shattered mirror - fragmented, distorted, and ultimately harmful to anyone who looks into it.",
        "The tragedy isn't that you fail to understand complex ideas, but that you believe your simplistic interpretations are profound.",
        "Your insights have all the depth and clarity of a mud puddle after a monsoon.",
        "Your intellectual contributions have the nutritional value of cotton candy - all empty fluff with no substance.",
        "If stupidity were an Olympic event, you'd be disqualified for using performance-enhancing drugs.",
        "Your brain appears to be experiencing a denial-of-service attack perpetrated by your own shocking incompetence.",
        "The only mystery greater than the origin of the universe is how you manage to dress yourself in the morning.",
        "Your cognitive apparatus seems to have been assembled by a committee of particularly untalented monkeys.",
        "The void between your thoughts is so vast astronomers could use it to measure the expansion rate of the universe.",
        "Your understanding of this topic has all the sophistication of a cave painting done by someone who's never seen a cave.",
        "If your neurons fired any slower, they'd be moving backwards in time, which might explain your prehistoric worldview.",
        "Your synaptic connections appear to be using the same routing algorithm as a drunkard stumbling home at 3 AM.",
        "The concept of rational thought seems to bounce off your consciousness like light off a black hole.",
        "I'd attempt to educate you, but it would be like trying to teach calculus to a houseplant - a pointless exercise with a non-sentient entity.",
        "Your intellectual output has the consistency of alphabet soup spilled by a toddler - random, messy, and impossible to derive meaning from.",
        "The gap between what you think you know and what you actually know could serve as a practical example of the multiverse theory.",
        "Your mental architecture appears to have been designed by Salvador Dalí during a particularly severe fever dream.",
        "Your logic has more holes than a colander that's been used for target practice by a firing squad.",
        "Trying to follow your train of thought is like trying to track the path of a housefly in a tornado - chaotic, unpredictable, and ultimately inconsequential.",
        "Your intellectual shortcomings would be fascinating to cognitive scientists studying the lower boundaries of human intelligence.",
        "The sheer density of wrongness in your statements could collapse into a singularity of ignorance from which no knowledge could ever escape.",
        "Your reasoning skills would embarrass a concussed hamster attempting to navigate a particularly challenging maze.",
        "The electrical activity in your brain appears to be generating less output than a solar calculator on a moonless night.",
        "Your arguments are so flimsy they make a house of cards in a hurricane look like a structural engineering masterpiece.",
        "The tortuous path of your logic would make Rube Goldberg machines seem straightforward by comparison.",
        "Your cognitive abilities appear to have been carefully curated to exclude anything resembling rationality or critical thinking.",
        "If your thoughts were any more scattered, astronomers would classify them as a new constellation.",
        "Your mental processing power makes a slide rule look like a quantum supercomputer.",
        "The intellectual bankruptcy of your position would qualify for Chapter 11 protection in any reasonable court.",
        "Your understanding of this subject has all the depth and nuance of a stick figure drawing done by someone who's never held a pencil.",
        "The fragility of your arguments suggests they should be handled with the same care as wet tissue paper in a hurricane.",
        "Your mental faculties appear to be operating with all the efficiency of a square wheel on an uphill journey.",
        "The spectacular failure of your reasoning process deserves its own exhibit in a museum dedicated to cognitive deficiencies.",
        "Your contributions to intellectual discourse would be rejected as too simplistic for a pre-school debate club.",
        "The conceptual limitations of your worldview make a one-dimensional object seem multifaceted by comparison.",
        "Your critical thinking skills have all the refinement of a sledgehammer being used for microsurgery.",
        "The rate at which you generate fallacies could power a small nation if only we could harness it as an energy source.",
        "Your mental model of reality has all the accuracy of a medieval flat-earth map being used to navigate the International Space Station.",
        "If your cognitive functions were any more impaired, you'd qualify for special parking privileges in the realm of ideas.",
        "The sheer density of misconceptions in your worldview would require a specialized intellectual Hazmat team to safely dismantle.",
        "Your capacity for rational discourse makes flat-earthers seem like paragons of scientific rigor.",
        "The half-life of your attention span appears to be shorter than that of the most unstable element on the periodic table.",
        "Your epistemological framework is so twisted it makes non-Euclidean geometry look straightforward.",
        "The intellectual equivalent of bringing a plastic spoon to a gunfight - pitifully inadequate and vaguely amusing to observers.",
        "Your argumentation strategy seems to be modeled after a drunken game of darts - randomly aimed and wildly off target.",
        "The neural pathways in your brain appear to be connected with all the precision of Christmas lights after being stored in a box for eleven months.",
        "Your attempts at coherent thought have all the stability of a house of cards in a wind tunnel during a hurricane.",
        "The conceptual boundaries of your understanding are so narrow they could fit comfortably inside a thimble with room to spare.",
        "Your cognitive faculties appear to be experiencing the intellectual equivalent of dial-up internet during a thunderstorm.",
        "If your critical thinking were any more stunted, it would qualify for botanical classification as a bonsai tree.",
        "The cavernous void where your reasoning skills should be could serve as an effective echo chamber for even the most faint-hearted of ideas.",
        "Your mental framework resembles a Jenga tower after fifteen rounds of play - precarious, incomplete, and on the verge of total collapse.",
        "The glacial pace of your cognitive processing makes continental drift seem like a NASCAR race by comparison.",
        "Your intellectual posturing is like a cardboard cutout of a skyscraper - flat, fake, and fooling absolutely no one.",
        "Your synaptic connections appear to be running on the same technological platform as an abacus, but with far less computational accuracy.",
        "The poverty of your ideas would qualify for humanitarian aid in any intellectually developed nation.",
        "Your cognitive abilities seem to have reached their zenith when you mastered the intricacies of a sippy cup.",
        "The labyrinthine confusion of your thought process would make Daedalus himself throw up his hands in despair.",
        "Your intellectual development appears to have fossilized during the Paleolithic era, making you a valuable specimen for archaeological study.",
        "The profound limitations of your understanding make a goldfish's three-second memory seem encyclopedic by comparison.",
        "Your mental constitution has all the fortitude of a chocolate teapot being used to brew lava.",
        "The conceptual foundation of your worldview appears to be built on quicksand during a particularly vigorous earthquake.",
        "Your processing power makes a pocket calculator with a dying battery look like a breakthrough in quantum computing."
    ]
}

def get_response(response_type: str, used_responses: set = None) -> str:
    """
    Get a random response based on the trigger type
    If used_responses is provided, avoid returning responses that have been used
    Ensures we cycle through all available responses before repeating any
    Also balances between short and lengthy intellectual insults
    """
    possible_responses = responses.get(response_type, ["Hello!"])
    
    if used_responses:
        # Filter out used responses of this type from the global used_responses set
        response_type_used = [r for r in used_responses if r in possible_responses]
        available_responses = [r for r in possible_responses if r not in response_type_used]
        
        # If all responses of this type have been used, reset just for this type
        if not available_responses:
            logger.info(f"All {response_type} responses have been used, clearing used responses for this type")
            
            # Instead of just returning a random response, we'll remove all responses of this type
            # from the used_responses set to start fresh
            for resp in possible_responses:
                if resp in used_responses:
                    used_responses.remove(resp)
            
            available_responses = possible_responses
        
        # For intellectual insults, let's occasionally choose a longer one
        if response_type == 'intellectual_insult':
            # Categorize responses by length
            short_responses = [r for r in available_responses if len(r) < 120]
            medium_responses = [r for r in available_responses if 120 <= len(r) < 180]
            long_responses = [r for r in available_responses if len(r) >= 180]
            
            # Choose which length category to use - heavily weighted toward longer ones (70%)
            length_choice = random.choices(
                ['short', 'medium', 'long'], 
                weights=[0.15, 0.15, 0.7], 
                k=1
            )[0]
            
            if length_choice == 'long' and long_responses:
                return random.choice(long_responses)
            elif length_choice == 'medium' and medium_responses:
                return random.choice(medium_responses)
            elif length_choice == 'short' and short_responses:
                return random.choice(short_responses)
        
        # Choose from unused responses
        return random.choice(available_responses)
    
    return random.choice(possible_responses)