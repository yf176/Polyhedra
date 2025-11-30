import sys
from pathlib import Path
sys.path.insert(0, 'src')

from polyhedra.services.citation_manager import CitationManager

# Create manager in current directory
manager = CitationManager(Path('.'))

# Add a sample citation
bibtex = '''@article{vaswani2017attention,
  title={Attention is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam},
  year={2017},
  venue={NeurIPS}
}'''

key, added = manager.add_entry(bibtex)
print(f'Added citation: {key} (new: {added})')

# List all citations
keys = manager.get_all_keys()
print(f'Total citations: {len(keys)}')
print(f'Keys: {keys}')

# Get full entries
entries = manager.get_all_entries()
for entry in entries:
    print(f'  {entry["key"]}: {entry["title"]} ({entry["year"]})')
