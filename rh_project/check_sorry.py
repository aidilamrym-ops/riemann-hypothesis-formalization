import re

with open('ConreyZeroFree.lean', 'r') as f:
    content = f.read()
    sorry_lines = [(i+1, line.strip()) for i, line in enumerate(content.split('\n')) if 'sorry' in line.lower()]
    theorem_count = len(re.findall(r'(theorem|corollary|lemma)\s+\w+', content))
    def_count = len(re.findall(r'def\s+\w+', content))
    axiom_count = len(re.findall(r'axiom\s+\w+', content))
    print(f"Total theorems/corollaries/lemmas: {theorem_count}")
    print(f"Definitions: {def_count}")
    print(f"Axioms: {axiom_count}")
    print(f"\nLines with 'sorry': {len(sorry_lines)}")
    for line_no, line in sorry_lines:
        print(f"  Line {line_no}: {line}")
    print(f"\nTotal 'axiom' (zero-sorry assumptions): {axiom_count}")
