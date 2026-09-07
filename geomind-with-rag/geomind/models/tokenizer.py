"""
GeoMind Tokenizer: Custom subword and domain vocabulary tokenizer for GeoMind models.
"""
import re
from typing import Dict, List, Optional, Tuple


SPECIAL_TOKENS = [
    "<pad>",    # Padding token (id: 0)
    "<unk>",    # Unknown token (id: 1)
    "<s>",      # Beginning of sequence (id: 2)
    "</s>",     # End of sequence (id: 3)
    "<geo>",    # Geography domain tag (id: 4)
    "<hist>",   # History domain tag (id: 5)
    "<soc>",    # Social studies domain tag (id: 6)
    "<query>",  # User query tag (id: 7)
    "<thought>",# Reasoning/thought tag (id: 8)
    "<response>"# Response generation tag (id: 9)
]


class GeoMindTokenizer:
    """
    Subword-aware and domain-specialized tokenizer for GeoMind foundation models.
    Supports token encoding, decoding, padding, special tokens, and vocabulary inspection.
    """

    def __init__(self, vocab_file: Optional[str] = None):
        self.special_tokens = SPECIAL_TOKENS
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self._build_base_vocabulary()

    def _build_base_vocabulary(self) -> None:
        """Initializes vocabulary with special tokens and essential root vocabulary."""
        # 1. Add special tokens
        for idx, token in enumerate(self.special_tokens):
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token

        # 2. Add domain keywords and high-frequency subwords
        core_vocab = [
            "the", "of", "and", "in", "to", "a", "is", "was", "for", "as", "on", "with", "by", "at",
            "from", "between", "distance", "capital", "country", "city", "population", "borders", "currency",
            "history", "war", "revolution", "causes", "consequences", "impact", "leader", "empire", "era",
            "world", "france", "germany", "japan", "india", "china", "united", "states", "delhi", "mumbai",
            "tokyo", "paris", "london", "berlin", "beijing", "rome", "athens", "cairo", "moscow", "washington",
            "government", "democracy", "republic", "federalism", "capitalism", "socialism", "constitution",
            "rights", "economy", "feudalism", "napoleon", "gandhi", "caesar", "churchill", "lincoln",
            "treaty", "versailles", "alliances", "militarism", "imperialism", "nationalism", "monarchy",
            "compare", "difference", "versus", "km", "miles", "degrees", "bearing", "hours", "flight",
            "located", "north", "south", "east", "west", "continent", "europe", "asia", "africa", "america",
            "ocean", "river", "mountain", "ancient", "modern", "medieval", "century", "battle", "declaration",
            "citizens", "law", "power", "separation", "executive", "legislative", "judicial", "checks", "balances",
            "free", "market", "public", "private", "property", "state", "production", "trade", "resources",
            "who", "what", "where", "when", "why", "how", "tell", "me", "about", "define", "explain",
            "it", "its", "they", "their", "are", "were", "been", "has", "have", "had", "which", "that",
            # Geography entities & landforms from Wikipedia datasets
            "everest", "kilimanjaro", "aconcagua", "denali", "elbrus", "fuji", "k2", "kangchenjunga",
            "himalayas", "andes", "alps", "rockies", "nile", "amazon", "yangtze", "mississippi",
            "danube", "volga", "ganges", "rhine", "congo", "mekong", "pacific", "atlantic", "indian",
            "arctic", "southern", "mediterranean", "caribbean", "sahara", "gobi", "kalahari", "atacama",
            "greenland", "madagascar", "borneo", "baffin", "sumatra", "honshu", "superior", "baikal",
            "victoria", "tanganyika", "huron", "michigan", "caspian", "sea", "pyramid", "giza", "taj",
            "mahal", "colosseum", "machu", "picchu", "petra", "angkor", "wat", "stonehenge", "acropolis",
            "mesopotamia", "egypt", "indus", "greece", "renaissance", "industrial", "alexander", "curie",
            "mandela", "totalitarianism", "theocracy", "mercantilism", "parliamentary", "nations", "nato",
            "asean", "habeas", "corpus", "suez", "canal", "panama", "gibraltar", "malacca", "bosporus",
            "bering", "strait", "lake", "desert", "island", "highest", "lowest", "deepest", "longest",
            "driest", "waterfall", "elevation", "trench", "mariana", "dead", "angel", "falls", "peak",
            "landform", "landmark", "wonder", "extreme", "area", "depth", "length", "origin", "outflow"
        ]

        # Add single character fallbacks (a-z, 0-9, common punctuation)
        chars = list("abcdefghijklmnopqrstuvwxyz0123456789.,:;!?-/()&°\"'")
        all_initial = core_vocab + chars

        for word in all_initial:
            if word not in self.token_to_id:
                new_id = len(self.token_to_id)
                self.token_to_id[word] = new_id
                self.id_to_token[new_id] = word

    @property
    def vocab_size(self) -> int:
        return len(self.token_to_id)

    @property
    def pad_token_id(self) -> int:
        return self.token_to_id["<pad>"]

    @property
    def unk_token_id(self) -> int:
        return self.token_to_id["<unk>"]

    @property
    def bos_token_id(self) -> int:
        return self.token_to_id["<s>"]

    @property
    def eos_token_id(self) -> int:
        return self.token_to_id["</s>"]

    def tokenize(self, text: str) -> List[str]:
        """Splits raw text into a sequence of vocabulary tokens and subword fragments."""
        if not text:
            return []
        
        # Normalize and split into words/punctuation
        words = re.findall(r"<[^>]+>|[a-zA-Z0-9]+|[.,:;!?-]", text.lower())
        tokens: List[str] = []

        for w in words:
            if w in self.token_to_id:
                tokens.append(w)
            else:
                # Subword character fragmentation for unknown words
                matched = False
                for i in range(len(w), 1, -1):
                    prefix = w[:i]
                    if prefix in self.token_to_id:
                        tokens.append(prefix)
                        suffix = w[i:]
                        if suffix:
                            for ch in suffix:
                                tokens.append(ch if ch in self.token_to_id else "<unk>")
                        matched = True
                        break
                if not matched:
                    for ch in w:
                        tokens.append(ch if ch in self.token_to_id else "<unk>")

        return tokens

    def encode(
        self,
        text: str,
        add_special_tokens: bool = True,
        max_length: Optional[int] = None,
        pad_to_max: bool = False
    ) -> List[int]:
        """Encodes text into token ID integers."""
        tokens = self.tokenize(text)
        token_ids: List[int] = []

        if add_special_tokens:
            token_ids.append(self.bos_token_id)

        for t in tokens:
            token_ids.append(self.token_to_id.get(t, self.unk_token_id))

        if add_special_tokens:
            token_ids.append(self.eos_token_id)

        if max_length is not None:
            if len(token_ids) > max_length:
                token_ids = token_ids[:max_length]
            elif pad_to_max:
                pad_len = max_length - len(token_ids)
                token_ids.extend([self.pad_token_id] * pad_len)

        return token_ids

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decodes token IDs back into human-readable text."""
        words: List[str] = []
        for tid in token_ids:
            token = self.id_to_token.get(tid, "<unk>")
            if skip_special_tokens and (token in self.special_tokens or token.startswith("<")):
                continue
            words.append(token)

        text = " ".join(words)
        # Format punctuation
        text = re.sub(r"\s+([.,:;!?-])", r"\1", text)
        return text.strip()

    def add_token(self, token: str) -> int:
        """Adds a new token to the vocabulary if not present."""
        token = token.lower()
        if token not in self.token_to_id:
            new_id = len(self.token_to_id)
            self.token_to_id[token] = new_id
            self.id_to_token[new_id] = token
            return new_id
        return self.token_to_id[token]
