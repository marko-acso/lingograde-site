/**
 * Phoneme Tools — LingoGrade
 * Maps letters/digraphs to phoneme families per language.
 * Provides minimal pair flashcard suggestions per phoneme.
 *
 * Structure is designed for easy extension:
 *   phonemeFamilyMap[lang][grapheme] = family
 *   minimalPairSuggestions[phoneme] = [ [wordA, wordB], ... ]
 */
var PhonemeTools = (function () {
  'use strict';

  // ── Phoneme family constants ──
  var FAMILIES = {
    PLOSIVE:      'plosive',
    FRICATIVE:    'fricative',
    NASAL:        'nasal',
    APPROXIMANT:  'approximant',
    AFFRICATE:    'affricate',
    VOWEL:        'vowel',
    DIPHTHONG:    'diphthong',
    LIQUID:       'liquid'
  };

  // ── Digraph detection order (longest match wins) ──
  // Each language defines its digraphs so we know to group them before single letters.
  var digraphs = {
    de: ['sch', 'tsch', 'ch', 'ng', 'nk', 'pf', 'qu', 'ei', 'au', 'eu', 'äu', 'ie', 'ck', 'tz', 'st', 'sp'],
    en: ['th', 'sh', 'ch', 'wh', 'ph', 'ng', 'nk', 'gh', 'qu', 'oo', 'ee', 'ea', 'ou', 'oi', 'oy', 'ai', 'ay', 'au', 'aw', 'ue', 'ui', 'ew'],
    es: ['ll', 'rr', 'ch', 'qu', 'gu', 'ei', 'ai', 'oi', 'au', 'eu', 'ue', 'ie'],
    fr: ['ch', 'ou', 'au', 'eau', 'eu', 'oi', 'ai', 'ei', 'an', 'en', 'in', 'on', 'un', 'gn', 'ph', 'qu', 'ng'],
    it: ['ch', 'gh', 'sc', 'gl', 'gn', 'ci', 'gi', 'ei', 'ai', 'oi', 'au', 'ou'],
    bg: ['ш', 'ж', 'ч', 'щ', 'дж', 'дз', 'тс', 'кс'],
    hr: ['dž', 'lj', 'nj', 'dz', 'ch', 'sh'],
    pt: ['ch', 'lh', 'nh', 'rr', 'ss', 'qu', 'gu', 'ei', 'ai', 'oi', 'au', 'ou', 'ão', 'ãe', 'ão'],
    ru: ['ш', 'ж', 'ч', 'щ', 'ц', 'тс', 'кс'],
    sr: ['dž', 'lj', 'nj', 'dz'],
    ro: ['ch', 'gh', 'ce', 'ci', 'ge', 'gi'],
    pl: ['sz', 'cz', 'rz', 'ch', 'dz', 'dź', 'dż', 'si', 'zi', 'ci', 'ni', 'ść', 'szcz']
  };

  // ── Phoneme family maps by language ──
  // Key: grapheme (lowercase), Value: phoneme family
  var phonemeFamilyMap = {

    // ─── German ───────────────────────────────────────────────────────────────
    de: {
      // Digraphs first
      'sch':  FAMILIES.FRICATIVE,
      'tsch': FAMILIES.AFFRICATE,
      'ch':   FAMILIES.FRICATIVE,
      'ng':   FAMILIES.NASAL,
      'nk':   FAMILIES.NASAL,
      'pf':   FAMILIES.AFFRICATE,
      'qu':   FAMILIES.PLOSIVE,
      'ei':   FAMILIES.DIPHTHONG,
      'au':   FAMILIES.DIPHTHONG,
      'eu':   FAMILIES.DIPHTHONG,
      'äu':   FAMILIES.DIPHTHONG,
      'ie':   FAMILIES.VOWEL,
      'ck':   FAMILIES.PLOSIVE,
      'tz':   FAMILIES.AFFRICATE,
      'st':   FAMILIES.FRICATIVE,
      'sp':   FAMILIES.FRICATIVE,
      // Single letters
      'a':    FAMILIES.VOWEL,
      'ä':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.APPROXIMANT,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'ö':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'ü':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'w':    FAMILIES.FRICATIVE,
      'x':    FAMILIES.FRICATIVE,
      'y':    FAMILIES.VOWEL,
      'z':    FAMILIES.FRICATIVE,
      'ß':    FAMILIES.FRICATIVE
    },

    // ─── English ──────────────────────────────────────────────────────────────
    en: {
      // Digraphs first
      'th':   FAMILIES.FRICATIVE,
      'sh':   FAMILIES.FRICATIVE,
      'ch':   FAMILIES.AFFRICATE,
      'wh':   FAMILIES.APPROXIMANT,
      'ph':   FAMILIES.FRICATIVE,
      'ng':   FAMILIES.NASAL,
      'nk':   FAMILIES.NASAL,
      'gh':   FAMILIES.FRICATIVE,
      'qu':   FAMILIES.PLOSIVE,
      'oo':   FAMILIES.VOWEL,
      'ee':   FAMILIES.VOWEL,
      'ea':   FAMILIES.VOWEL,
      'ou':   FAMILIES.DIPHTHONG,
      'oi':   FAMILIES.DIPHTHONG,
      'oy':   FAMILIES.DIPHTHONG,
      'ai':   FAMILIES.DIPHTHONG,
      'ay':   FAMILIES.DIPHTHONG,
      'au':   FAMILIES.VOWEL,
      'aw':   FAMILIES.VOWEL,
      'ue':   FAMILIES.VOWEL,
      'ui':   FAMILIES.VOWEL,
      'ew':   FAMILIES.DIPHTHONG,
      // Single letters
      'a':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.PLOSIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.AFFRICATE,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'q':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.APPROXIMANT,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'w':    FAMILIES.APPROXIMANT,
      'x':    FAMILIES.FRICATIVE,
      'y':    FAMILIES.APPROXIMANT,
      'z':    FAMILIES.FRICATIVE
    },

    // ─── Spanish ──────────────────────────────────────────────────────────────
    es: {
      'll':   FAMILIES.APPROXIMANT,
      'rr':   FAMILIES.LIQUID,
      'ch':   FAMILIES.AFFRICATE,
      'qu':   FAMILIES.PLOSIVE,
      'gu':   FAMILIES.PLOSIVE,
      'ei':   FAMILIES.DIPHTHONG,
      'ai':   FAMILIES.DIPHTHONG,
      'oi':   FAMILIES.DIPHTHONG,
      'au':   FAMILIES.DIPHTHONG,
      'eu':   FAMILIES.DIPHTHONG,
      'ue':   FAMILIES.DIPHTHONG,
      'ie':   FAMILIES.DIPHTHONG,
      'a':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.FRICATIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.FRICATIVE,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'ñ':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'x':    FAMILIES.FRICATIVE,
      'y':    FAMILIES.APPROXIMANT,
      'z':    FAMILIES.FRICATIVE
    },

    // ─── French ───────────────────────────────────────────────────────────────
    fr: {
      'ch':   FAMILIES.FRICATIVE,
      'ou':   FAMILIES.VOWEL,
      'au':   FAMILIES.VOWEL,
      'eau':  FAMILIES.VOWEL,
      'eu':   FAMILIES.VOWEL,
      'oi':   FAMILIES.DIPHTHONG,
      'ai':   FAMILIES.VOWEL,
      'ei':   FAMILIES.VOWEL,
      'an':   FAMILIES.NASAL,
      'en':   FAMILIES.NASAL,
      'in':   FAMILIES.NASAL,
      'on':   FAMILIES.NASAL,
      'un':   FAMILIES.NASAL,
      'gn':   FAMILIES.NASAL,
      'ph':   FAMILIES.FRICATIVE,
      'qu':   FAMILIES.PLOSIVE,
      'ng':   FAMILIES.NASAL,
      'a':    FAMILIES.VOWEL,
      'â':    FAMILIES.VOWEL,
      'à':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.FRICATIVE,
      'ç':    FAMILIES.FRICATIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'é':    FAMILIES.VOWEL,
      'è':    FAMILIES.VOWEL,
      'ê':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.FRICATIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'î':    FAMILIES.VOWEL,
      'j':    FAMILIES.FRICATIVE,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'ô':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'û':    FAMILIES.VOWEL,
      'ù':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'w':    FAMILIES.APPROXIMANT,
      'x':    FAMILIES.FRICATIVE,
      'y':    FAMILIES.VOWEL,
      'z':    FAMILIES.FRICATIVE
    },

    // ─── Italian ──────────────────────────────────────────────────────────────
    it: {
      'ch':   FAMILIES.PLOSIVE,
      'gh':   FAMILIES.PLOSIVE,
      'sc':   FAMILIES.FRICATIVE,
      'gl':   FAMILIES.APPROXIMANT,
      'gn':   FAMILIES.NASAL,
      'ci':   FAMILIES.AFFRICATE,
      'gi':   FAMILIES.AFFRICATE,
      'a':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.PLOSIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'è':    FAMILIES.VOWEL,
      'é':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'ì':    FAMILIES.VOWEL,
      'j':    FAMILIES.APPROXIMANT,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'ò':    FAMILIES.VOWEL,
      'ó':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'q':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'ù':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'z':    FAMILIES.AFFRICATE
    },

    // ─── Bulgarian ────────────────────────────────────────────────────────────
    bg: {
      'ш':    FAMILIES.FRICATIVE,
      'ж':    FAMILIES.FRICATIVE,
      'ч':    FAMILIES.AFFRICATE,
      'щ':    FAMILIES.AFFRICATE,
      'дж':   FAMILIES.AFFRICATE,
      'дз':   FAMILIES.AFFRICATE,
      'тс':   FAMILIES.AFFRICATE,
      'кс':   FAMILIES.FRICATIVE,
      'а':    FAMILIES.VOWEL,
      'б':    FAMILIES.PLOSIVE,
      'в':    FAMILIES.FRICATIVE,
      'г':    FAMILIES.PLOSIVE,
      'д':    FAMILIES.PLOSIVE,
      'е':    FAMILIES.VOWEL,
      'з':    FAMILIES.FRICATIVE,
      'и':    FAMILIES.VOWEL,
      'й':    FAMILIES.APPROXIMANT,
      'к':    FAMILIES.PLOSIVE,
      'л':    FAMILIES.LIQUID,
      'м':    FAMILIES.NASAL,
      'н':    FAMILIES.NASAL,
      'о':    FAMILIES.VOWEL,
      'п':    FAMILIES.PLOSIVE,
      'р':    FAMILIES.LIQUID,
      'с':    FAMILIES.FRICATIVE,
      'т':    FAMILIES.PLOSIVE,
      'у':    FAMILIES.VOWEL,
      'ф':    FAMILIES.FRICATIVE,
      'х':    FAMILIES.FRICATIVE,
      'ц':    FAMILIES.AFFRICATE,
      'ъ':    FAMILIES.VOWEL,
      'ь':    FAMILIES.APPROXIMANT,
      'ю':    FAMILIES.DIPHTHONG,
      'я':    FAMILIES.DIPHTHONG
    },

    // ─── Croatian ─────────────────────────────────────────────────────────────
    hr: {
      'dž':   FAMILIES.AFFRICATE,
      'lj':   FAMILIES.APPROXIMANT,
      'nj':   FAMILIES.NASAL,
      'dz':   FAMILIES.AFFRICATE,
      'a':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.AFFRICATE,
      'č':    FAMILIES.AFFRICATE,
      'ć':    FAMILIES.AFFRICATE,
      'd':    FAMILIES.PLOSIVE,
      'đ':    FAMILIES.AFFRICATE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.APPROXIMANT,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      'š':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'z':    FAMILIES.FRICATIVE,
      'ž':    FAMILIES.FRICATIVE
    },

    // ─── Portuguese ───────────────────────────────────────────────────────────
    pt: {
      'ch':   FAMILIES.FRICATIVE,
      'lh':   FAMILIES.APPROXIMANT,
      'nh':   FAMILIES.NASAL,
      'rr':   FAMILIES.LIQUID,
      'ss':   FAMILIES.FRICATIVE,
      'qu':   FAMILIES.PLOSIVE,
      'gu':   FAMILIES.PLOSIVE,
      'ão':   FAMILIES.NASAL,
      'ãe':   FAMILIES.NASAL,
      'a':    FAMILIES.VOWEL,
      'ã':    FAMILIES.VOWEL,
      'â':    FAMILIES.VOWEL,
      'á':    FAMILIES.VOWEL,
      'à':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.PLOSIVE,
      'ç':    FAMILIES.FRICATIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'é':    FAMILIES.VOWEL,
      'ê':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'í':    FAMILIES.VOWEL,
      'j':    FAMILIES.FRICATIVE,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'ó':    FAMILIES.VOWEL,
      'ô':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'q':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'ú':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'x':    FAMILIES.FRICATIVE,
      'z':    FAMILIES.FRICATIVE
    },

    // ─── Russian ──────────────────────────────────────────────────────────────
    ru: {
      'ш':    FAMILIES.FRICATIVE,
      'ж':    FAMILIES.FRICATIVE,
      'ч':    FAMILIES.AFFRICATE,
      'щ':    FAMILIES.FRICATIVE,
      'ц':    FAMILIES.AFFRICATE,
      'тс':   FAMILIES.AFFRICATE,
      'кс':   FAMILIES.FRICATIVE,
      'а':    FAMILIES.VOWEL,
      'б':    FAMILIES.PLOSIVE,
      'в':    FAMILIES.FRICATIVE,
      'г':    FAMILIES.PLOSIVE,
      'д':    FAMILIES.PLOSIVE,
      'е':    FAMILIES.VOWEL,
      'ё':    FAMILIES.VOWEL,
      'з':    FAMILIES.FRICATIVE,
      'и':    FAMILIES.VOWEL,
      'й':    FAMILIES.APPROXIMANT,
      'к':    FAMILIES.PLOSIVE,
      'л':    FAMILIES.LIQUID,
      'м':    FAMILIES.NASAL,
      'н':    FAMILIES.NASAL,
      'о':    FAMILIES.VOWEL,
      'п':    FAMILIES.PLOSIVE,
      'р':    FAMILIES.LIQUID,
      'с':    FAMILIES.FRICATIVE,
      'т':    FAMILIES.PLOSIVE,
      'у':    FAMILIES.VOWEL,
      'ф':    FAMILIES.FRICATIVE,
      'х':    FAMILIES.FRICATIVE,
      'ъ':    FAMILIES.APPROXIMANT,
      'ы':    FAMILIES.VOWEL,
      'ь':    FAMILIES.APPROXIMANT,
      'э':    FAMILIES.VOWEL,
      'ю':    FAMILIES.DIPHTHONG,
      'я':    FAMILIES.DIPHTHONG
    },

    // ─── Serbian ──────────────────────────────────────────────────────────────
    sr: {
      'dž':   FAMILIES.AFFRICATE,
      'lj':   FAMILIES.APPROXIMANT,
      'nj':   FAMILIES.NASAL,
      'dz':   FAMILIES.AFFRICATE,
      'a':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.AFFRICATE,
      'č':    FAMILIES.AFFRICATE,
      'ć':    FAMILIES.AFFRICATE,
      'd':    FAMILIES.PLOSIVE,
      'đ':    FAMILIES.AFFRICATE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.APPROXIMANT,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      'š':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'z':    FAMILIES.FRICATIVE,
      'ž':    FAMILIES.FRICATIVE
    },

    // ─── Romanian ─────────────────────────────────────────────────────────────
    ro: {
      'ch':   FAMILIES.PLOSIVE,
      'gh':   FAMILIES.PLOSIVE,
      'a':    FAMILIES.VOWEL,
      'ă':    FAMILIES.VOWEL,
      'â':    FAMILIES.VOWEL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.PLOSIVE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'î':    FAMILIES.VOWEL,
      'j':    FAMILIES.FRICATIVE,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      'ș':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'ț':    FAMILIES.AFFRICATE,
      'u':    FAMILIES.VOWEL,
      'v':    FAMILIES.FRICATIVE,
      'x':    FAMILIES.FRICATIVE,
      'z':    FAMILIES.FRICATIVE
    },

    // ─── Polish ───────────────────────────────────────────────────────────────
    pl: {
      'sz':   FAMILIES.FRICATIVE,
      'cz':   FAMILIES.AFFRICATE,
      'rz':   FAMILIES.FRICATIVE,
      'ch':   FAMILIES.FRICATIVE,
      'dz':   FAMILIES.AFFRICATE,
      'dź':   FAMILIES.AFFRICATE,
      'dż':   FAMILIES.AFFRICATE,
      'si':   FAMILIES.FRICATIVE,
      'zi':   FAMILIES.FRICATIVE,
      'ci':   FAMILIES.AFFRICATE,
      'ni':   FAMILIES.NASAL,
      'ść':   FAMILIES.FRICATIVE,
      'szcz': FAMILIES.FRICATIVE,
      'a':    FAMILIES.VOWEL,
      'ą':    FAMILIES.NASAL,
      'b':    FAMILIES.PLOSIVE,
      'c':    FAMILIES.AFFRICATE,
      'ć':    FAMILIES.AFFRICATE,
      'd':    FAMILIES.PLOSIVE,
      'e':    FAMILIES.VOWEL,
      'ę':    FAMILIES.NASAL,
      'f':    FAMILIES.FRICATIVE,
      'g':    FAMILIES.PLOSIVE,
      'h':    FAMILIES.FRICATIVE,
      'i':    FAMILIES.VOWEL,
      'j':    FAMILIES.APPROXIMANT,
      'k':    FAMILIES.PLOSIVE,
      'l':    FAMILIES.LIQUID,
      'ł':    FAMILIES.APPROXIMANT,
      'm':    FAMILIES.NASAL,
      'n':    FAMILIES.NASAL,
      'ń':    FAMILIES.NASAL,
      'o':    FAMILIES.VOWEL,
      'ó':    FAMILIES.VOWEL,
      'p':    FAMILIES.PLOSIVE,
      'r':    FAMILIES.LIQUID,
      's':    FAMILIES.FRICATIVE,
      'ś':    FAMILIES.FRICATIVE,
      't':    FAMILIES.PLOSIVE,
      'u':    FAMILIES.VOWEL,
      'w':    FAMILIES.FRICATIVE,
      'y':    FAMILIES.VOWEL,
      'z':    FAMILIES.FRICATIVE,
      'ź':    FAMILIES.FRICATIVE,
      'ż':    FAMILIES.FRICATIVE
    }
  };

  // ── Minimal pair suggestions ──
  // Key: grapheme or phoneme label, Value: array of [word, contrast_word] pairs
  // Each pair illustrates a minimal contrast for that phoneme.
  var minimalPairSuggestions = {

    // ─── German phonemes ──────────────────────────────────────────────────────
    'de:th':  [], // not a native German phoneme
    'de:w':   [['Wein','Bein'], ['Wasser','Passer'], ['Wald','kalt'], ['weit','Zeit']],
    'de:v':   [['Vogel','Vogel'], ['voll','toll'], ['vier','hier']],
    'de:ü':   [['über','Iber'], ['Stück','Stock'], ['müde','Mode'], ['Brücke','Brücke']],
    'de:ö':   [['Höhle','Höhle'], ['König','könnte'], ['Öl','Aal'], ['schön','schon']],
    'de:ä':   [['Mädchen','Märchen'], ['Käse','Kasse'], ['Bär','Bar'], ['wählen','wahlen']],
    'de:ch':  [['ich','ick'], ['Bach','Fach'], ['Licht','Wicht'], ['mich','dich']],
    'de:sch': [['Schule','Stule'], ['Fisch','Tisch'], ['waschen','wachen'], ['Schiff','Stift']],
    'de:r':   [['Rad','Bad'], ['Regen','wegen'], ['fahren','lachen'], ['richtig','dichtig']],
    'de:z':   [['Zeit','weit'], ['Zahn','Bahn'], ['Salz','alts'], ['zu','du']],
    'de:pf':  [['Pferd','Berd'], ['Topf','Tod'], ['Pfanne','Wanne'], ['Kopf','Hof']],
    'de:ng':  [['lang','lank'], ['Junge','Bunge'], ['singen','sinken'], ['Finger','Winter']],
    'de:ei':  [['Eis','aus'], ['mein','Main'], ['Bein','Bahn'], ['heim','Heim']],
    'de:eu':  [['neu','nau'], ['heute','haue'], ['Leute','Laute'], ['treu','Tau']],
    'de:au':  [['Haus','Heis'], ['Baum','Bein'], ['laut','Leid'], ['Maus','Mais']],
    'de:ie':  [['viel','Biel'], ['Liebe','Lübe'], ['Wiese','Wüste'], ['fiel','fühl']],
    'de:b':   [['Ball','Tall'], ['Bach','Fach'], ['Brot','Grot'], ['Bein','Kein']],
    'de:p':   [['Pass','Bass'], ['Post','Bost'], ['Paar','Bar'], ['Pein','Bein']],
    'de:d':   [['Dach','Fach'], ['Dose','Hose'], ['Damm','Kamm'], ['Dieb','Lieb']],
    'de:t':   [['Tisch','Fisch'], ['Tage','Dage'], ['toll','Doll'], ['tut','gut']],
    'de:g':   [['gut','But'], ['Geld','Weld'], ['gehen','sehen'], ['Gast','Last']],
    'de:k':   [['Kalt','alt'], ['Kunst','Gunst'], ['klar','Bar'], ['Kuchen','suchen']],
    'de:l':   [['lang','Gang'], ['laut','haut'], ['Licht','nicht'], ['lieben','sieben']],
    'de:m':   [['Maus','Haus'], ['mehr','leer'], ['Mann','Dann'], ['Mist','List']],
    'de:n':   [['Nacht','Macht'], ['nein','sein'], ['Nase','Vase'], ['nun','nun']],
    'de:s':   [['Sonne','Wonne'], ['Stein','Bein'], ['sagen','lagen'], ['Sinn','Binn']],
    'de:f':   [['Foto','Bodo'], ['fallen','ballen'], ['Fisch','Tisch'], ['Feuer','treuer']],
    'de:h':   [['Haus','Maus'], ['hier','vier'], ['Hut','gut'], ['Hund','bunt']],
    'de:j':   [['ja','ba'], ['jung','bung'], ['Jagd','Sagt'], ['Jahr','Bar']],

    // ─── English phonemes ─────────────────────────────────────────────────────
    'en:th':  [['think','sink'], ['three','tree'], ['thin','tin'], ['thank','tank'], ['this','dis'], ['that','dat'], ['them','dem']],
    'en:th_v': [['this','dis'], ['them','dem'], ['the','de'], ['bathe','babe']],
    'en:sh':  [['ship','chip'], ['shop','chop'], ['shoe','chew'], ['sheep','cheap'], ['wash','watch']],
    'en:ch':  [['chip','ship'], ['chop','shop'], ['chair','share'], ['cheer','sheer']],
    'en:w':   [['wine','vine'], ['west','vest'], ['wet','vet'], ['worse','verse'], ['wear','veer']],
    'en:v':   [['vine','wine'], ['vet','wet'], ['vest','west'], ['vote','boat']],
    'en:r':   [['red','led'], ['right','light'], ['road','load'], ['race','lace']],
    'en:l':   [['led','red'], ['light','right'], ['load','road'], ['lake','rake']],
    'en:p':   [['pat','bat'], ['pit','bit'], ['pen','ben'], ['park','bark']],
    'en:b':   [['bat','pat'], ['bit','pit'], ['ben','pen'], ['bark','park']],
    'en:t':   [['ten','den'], ['tip','dip'], ['torn','dorn'], ['town','down']],
    'en:d':   [['den','ten'], ['dip','tip'], ['down','town'], ['dog','log']],
    'en:k':   [['cat','bat'], ['cold','bold'], ['coat','goat'], ['back','bag']],
    'en:g':   [['goat','coat'], ['gold','cold'], ['bag','back'], ['game','came']],
    'en:f':   [['fat','vat'], ['fine','vine'], ['leaf','leave'], ['safe','save']],
    'en:s':   [['sip','zip'], ['seal','zeal'], ['sink','zinc'], ['bus','buzz']],
    'en:z':   [['zip','sip'], ['zeal','seal'], ['zinc','sink'], ['buzz','bus']],
    'en:n':   [['night','might'], ['nail','mail'], ['know','mow'], ['name','game']],
    'en:m':   [['might','night'], ['mail','nail'], ['mow','know'], ['map','nap']],
    'en:ng':  [['sing','sin'], ['ring','rin'], ['thing','thin'], ['song','son']],
    'en:h':   [['hat','at'], ['hill','ill'], ['hear','ear'], ['have','Dave']],
    'en:j':   [['jet','yet'], ['jam','yam'], ['joke','yoke'], ['jell','yell']],
    'en:y':   [['yet','jet'], ['yam','jam'], ['yoke','joke'], ['yell','jell']],
    'en:oo':  [['food','foot'], ['pool','pull'], ['fool','full'], ['boot','book']],
    'en:th_pairs': [['think','sink'], ['three','tree'], ['thin','tin']],

    // ─── German-specific common problem pairs ─────────────────────────────────
    'de:sch_ch': [['waschen','wachen'], ['Fisch','Fach'], ['schön','schon']],

    // ─── Shared/generic (language-agnostic fallback) ──────────────────────────
    vowel:    [['bit','bat'], ['bet','bat'], ['boot','boat'], ['sit','set']],
    plosive:  [['pat','bat'], ['ten','den'], ['cat','got']],
    fricative:[['fine','vine'], ['think','sink'], ['ship','sip']],
    nasal:    [['name','game'], ['night','might'], ['sing','sin']],
    approximant: [['wine','vine'], ['led','red'], ['wet','yet']],
    affricate:[['chip','ship'], ['jet','yet'], ['choice','voice']],
    liquid:   [['led','red'], ['road','load'], ['lake','rake']],
    diphthong:[['boat','boot'], ['bay','bee'], ['boy','bar']]
  };

  // ── Tokenize a word into graphemes for a given language ──
  // Returns an array of { grapheme, index } objects, longest match first.
  function tokenize(word, lang) {
    var map = phonemeFamilyMap[lang] || phonemeFamilyMap['en'];
    var knownDigraphs = (digraphs[lang] || []).slice().sort(function(a, b) {
      return b.length - a.length; // longest first
    });
    var lower = word.toLowerCase();
    var tokens = [];
    var i = 0;
    while (i < lower.length) {
      var matched = false;
      for (var d = 0; d < knownDigraphs.length; d++) {
        var dg = knownDigraphs[d];
        if (lower.substr(i, dg.length) === dg) {
          tokens.push({ grapheme: lower.substr(i, dg.length), originalIndex: i });
          i += dg.length;
          matched = true;
          break;
        }
      }
      if (!matched) {
        tokens.push({ grapheme: lower[i], originalIndex: i });
        i++;
      }
    }
    return tokens;
  }

  // ── Get the phoneme family for a grapheme in a given language ──
  function getFamily(grapheme, lang) {
    var map = phonemeFamilyMap[lang] || phonemeFamilyMap['en'];
    return map[grapheme.toLowerCase()] || 'unknown';
  }

  // ── Determine position: initial / medial / final ──
  function getPosition(tokenIndex, totalTokens) {
    if (totalTokens <= 1) return 'initial';
    if (tokenIndex === 0) return 'initial';
    if (tokenIndex === totalTokens - 1) return 'final';
    return 'medial';
  }

  // ── Get minimal pair suggestions for a phoneme in a language ──
  // Tries lang-specific key first, then generic family key.
  function getSuggestions(grapheme, lang, family) {
    var key = lang + ':' + grapheme.toLowerCase();
    if (minimalPairSuggestions[key] && minimalPairSuggestions[key].length) {
      return minimalPairSuggestions[key];
    }
    // Try family fallback
    if (minimalPairSuggestions[family] && minimalPairSuggestions[family].length) {
      return minimalPairSuggestions[family];
    }
    return [];
  }

  // ── Get top N suggested pairs from a list of logged phonemes ──
  // phonemes: array of { grapheme, lang, family }
  function getTopSuggestions(phonemes, maxPairs) {
    maxPairs = maxPairs || 5;
    var seen = {};
    var results = [];
    phonemes.forEach(function(p) {
      var key = p.grapheme + '|' + p.lang;
      if (seen[key]) return;
      seen[key] = true;
      var pairs = getSuggestions(p.grapheme, p.lang, p.family);
      pairs.slice(0, 2).forEach(function(pair) {
        if (results.length < maxPairs) results.push({ grapheme: p.grapheme, pair: pair });
      });
    });
    return results;
  }

  // ── List all supported languages ──
  var LANGUAGES = Object.keys(phonemeFamilyMap);

  return {
    FAMILIES: FAMILIES,
    LANGUAGES: LANGUAGES,
    phonemeFamilyMap: phonemeFamilyMap,
    minimalPairSuggestions: minimalPairSuggestions,
    digraphs: digraphs,
    tokenize: tokenize,
    getFamily: getFamily,
    getPosition: getPosition,
    getSuggestions: getSuggestions,
    getTopSuggestions: getTopSuggestions
  };
})();
