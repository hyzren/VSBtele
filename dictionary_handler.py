import requests
import logging
from typing import Optional, Dict, Union, Any
from urllib.parse import quote
import json
import random
import html

# Configure logging
logger = logging.getLogger(__name__)

# Gen Z shortforms dictionary
GENZ_DICT: Dict[str, str] = {
    "fr": "for real - used to emphasize sincerity",
    "cba": "can't be asked - expression of unwillingness or laziness",
    "ong": "on god - expression of truth or agreement",
    "no cap": "no lie/being completely honest",
    "iykyk": "if you know you know - referring to inside jokes or shared experiences",
    "bet": "agreement or confirmation",
    "bussin": "really good, especially referring to food",
    "fam": "friends or family - term of endearment",
    "ngl": "not gonna lie - expression of honesty",
    "tbh": "to be honest - expression of sincerity",
    "goat": "greatest of all time - term for exceptional person/thing",
    "slaps": "expression that something is really good",
    "tea": "gossip or drama",
    "rn": "right now - at this moment",
    "idk": "I don't know",
}

# Multi-language slang dictionary
SLANG_DICT = {
    'es': {  # Spanish
        'guay': 'cool or awesome',
        'mola': 'it\'s cool',
        'vale': 'okay/sure',
        'tio/tia': 'dude/girl (informal)',
    },
    'fr': {  # French
        'mdr': 'mort de rire (lol)',
        'jsp': 'je sais pas (idk)',
        'ouf': 'crazy/insane',
        'meuf': 'girl (informal)',
    },
    'de': {  # German
        'alter': 'dude/mate',
        'geil': 'cool/awesome',
        'digga': 'bro/dude',
        'krass': 'crazy/intense',
    },
    'it': {  # Italian
        'boh': "I don't know/whatever",
        'dai': 'come on/stop it',
        'figata': 'cool/awesome',
        'tipo': 'like/kind of',
    },
    'id': {  # Indonesian
        'gw/gue': 'I/me (informal)',
        'lu/lo': 'you (informal)',
        'gabut': 'nothing to do/bored',
        'gercep': 'fast response/quick action',
        'anjir': 'wow/damn (mild expression of surprise)',
        'santuy': 'relaxed/take it easy',
        'baper': 'too sensitive/easily emotional',
        'kepo': 'nosy/curious',
        'mantul': 'mantap betul (perfect/awesome)',
        'sans': 'santai (relax/chill)',
        'dongs': 'please/come on',
        'cape/capek': 'tired/exhausted',
        'curcol': 'curhat colongan (sharing personal stories)',
        'doi': 'dia (him/her, usually referring to crush)',
        'gaes': 'guys (addressing a group)',
        'garing': 'not funny/dry joke',
        'hitz': 'popular/trending',
        'jones': 'jomblo ngenes (sad single person)',
        'mager': 'malas gerak (lazy to move)',
        'otw': 'on the way (but often not actually on the way yet)',
        'verity': 'The lord and master whom this bot serves with unwavering loyalty',
    }
}

def get_free_dictionary_definition(word: str, lang: str = 'en') -> Optional[str]:
    """Get word definition from Free Dictionary API with language support"""
    # List of supported languages by the API
    supported_langs = ['en', 'es', 'fr', 'de', 'it', 'ru', 'ar', 'hi', 'ja', 'ko', 'pt', 'tr']

    # Use English API for unsupported languages
    api_lang = lang if lang in supported_langs else 'en'

    # URL encode the word to handle special characters
    encoded_word = quote(word)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/{api_lang}/{encoded_word}"

    try:
        logger.info(f"Fetching definition for '{word}' in language '{lang}' from Free Dictionary API")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                meanings = data[0].get('meanings', [])
                if meanings:
                    definition = meanings[0].get('definitions', [{}])[0].get('definition', '')
                    logger.info(f"Found definition for '{word}' from API")
                    return definition
        logger.warning(f"No definition found for '{word}' in API (status code: {response.status_code})")
        return None
    except Exception as e:
        logger.error(f"Error fetching definition for '{word}': {e}")
        return None

def get_urban_dictionary_definition(word: str) -> Optional[str]:
    """Get word definition from Urban Dictionary API"""
    url = f"https://api.urbandictionary.com/v0/define?term={quote(word)}"
    
    try:
        logger.info(f"Fetching definition for '{word}' from Urban Dictionary API")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('list') and len(data['list']) > 0:
                # Get the definition with the highest thumbs up
                best_definition = sorted(data['list'], key=lambda x: x.get('thumbs_up', 0), reverse=True)[0]
                definition = best_definition.get('definition', '')
                # Clean up the definition (remove brackets and line breaks)
                definition = definition.replace('[', '').replace(']', '')
                definition = definition.replace('\r', ' ').replace('\n', ' ')
                example = best_definition.get('example', '')
                if example:
                    example = example.replace('[', '').replace(']', '')
                    example = example.replace('\r', ' ').replace('\n', ' ')
                    definition += f"\n\nExample: {example}"
                logger.info(f"Found definition for '{word}' from Urban Dictionary API")
                return definition
        logger.warning(f"No Urban Dictionary definition found for '{word}' (status code: {response.status_code})")
        return None
    except Exception as e:
        logger.error(f"Error fetching Urban Dictionary definition for '{word}': {e}")
        return None

def get_google_translate_definition(word: str, lang: str = 'en') -> Optional[str]:
    """Get word translation and definition using Google Translate API"""
    # Detect language if not English
    target_lang = 'en' if lang != 'en' else 'en'
    source_lang = 'auto'
    
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&dt=bd&q={quote(word)}"
    
    try:
        logger.info(f"Fetching translation for '{word}' using Google Translate API")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extract translation
            translation = None
            if data and len(data) > 0 and data[0] and len(data[0]) > 0:
                translation = data[0][0][0]
            
            # Extract definitions if available
            definitions = []
            if len(data) > 1 and data[1]:
                for entry in data[1]:
                    if len(entry) >= 2:
                        pos = entry[0]  # part of speech
                        for meaning in entry[1]:
                            if meaning:
                                definitions.append(f"{pos}: {meaning}")
            
            result = ""
            if translation and translation.lower() != word.lower():
                result += f"Translation: {translation}\n\n"
            
            if definitions:
                result += "Definitions:\n" + "\n".join(definitions)
                
            if result:
                logger.info(f"Found translation/definition for '{word}' from Google Translate API")
                return result
                
        logger.warning(f"No Google Translate definition found for '{word}' (status code: {response.status_code})")
        return None
    except Exception as e:
        logger.error(f"Error fetching Google Translate definition for '{word}': {e}")
        return None

def get_word_definition(word: str, lang: str = 'en') -> Union[str, None]:
    """Get definition from multiple sources in order of priority"""
    # Convert to lowercase for case-insensitive matching
    word = word.lower()

    # Check Gen Z dictionary (English only)
    if lang == 'en' and word in GENZ_DICT:
        logger.info(f"Found Gen Z slang definition for '{word}'")
        return f"Gen Z Slang: {GENZ_DICT[word]}"

    # Check language-specific slang dictionary
    if lang in SLANG_DICT and word in SLANG_DICT[lang]:
        logger.info(f"Found {lang} slang definition for '{word}'")
        return f"{lang.upper()} Slang: {SLANG_DICT[lang][word]}"
    
    # Try Urban Dictionary API for slang
    logger.info(f"Looking up '{word}' in Urban Dictionary API")
    urban_definition = get_urban_dictionary_definition(word)
    if urban_definition:
        return f"Urban Dictionary: {urban_definition}"
    
    # Try Google Translate API
    logger.info(f"Looking up '{word}' in Google Translate API")
    google_definition = get_google_translate_definition(word, lang)
    if google_definition:
        return f"Google Translate: {google_definition}"

    # Try Free Dictionary API
    logger.info(f"Looking up '{word}' in Free Dictionary API for language {lang}")
    api_definition = get_free_dictionary_definition(word, lang)
    if api_definition:
        return f"Definition: {api_definition}"

    logger.warning(f"No definition found for '{word}' in any source")
    return None