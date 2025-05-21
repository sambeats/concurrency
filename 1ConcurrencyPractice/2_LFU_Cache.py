from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Maps key to a tuple: (value, frequency)
        self.key_to_val_freq = {}
        # Maps frequency to keys with that frequency, keeping keys in order of usage (LRU)
        self.freq_to_keys = defaultdict(OrderedDict)
        # Tracks the minimum frequency of any key currently in the cache
        self.min_freq = 0

    def _update_freq(self, key):
        # Get current value and frequency of the key
        value, freq = self.key_to_val_freq[key]
        
        # Remove the key from the current frequency list
        del self.freq_to_keys[freq][key]
        
        # If no keys left with this frequency, remove that frequency bucket
        # Also, if this frequency was the minimum, update min_freq
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        
        # Add the key to the next higher frequency bucket
        self.freq_to_keys[freq + 1][key] = None
        
        # Update the key's frequency
        self.key_to_val_freq[key] = (value, freq + 1)

    def get(self, key: int) -> int:
        # If key doesn't exist, return -1
        if key not in self.key_to_val_freq:
            return -1
        
        # Increase the frequency of the key and return its value
        self._update_freq(key)
        return self.key_to_val_freq[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        
        # If key exists, update its value and frequency
        if key in self.key_to_val_freq:
            _, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = (value, freq)
            self._update_freq(key)
            return
        
        # If capacity reached, evict least frequently used key
        if len(self.key_to_val_freq) >= self.capacity:
            # Evict the least recently used key from the lowest frequency bucket
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[evict_key]
            
            # If that frequency bucket is now empty, remove it
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
        
        # Insert the new key with frequency 1
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
