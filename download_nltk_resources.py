#!/usr/bin/env python3
"""
Download NLTK Resources

This script downloads the required NLTK resources for the sentiment analyzer.
"""

import nltk
import ssl

# Handle SSL certificate verification issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except AttributeError:
    pass

# Download required resources
print("Downloading NLTK resources...")
nltk.download('vader_lexicon')
nltk.download('punkt')
print("Download complete!")

print("\nVerifying resources...")
try:
    nltk.data.find('vader_lexicon')
    print("✓ vader_lexicon is installed")
except LookupError:
    print("✗ vader_lexicon is NOT installed")

try:
    nltk.data.find('tokenizers/punkt')
    print("✓ punkt is installed")
except LookupError:
    print("✗ punkt is NOT installed") 