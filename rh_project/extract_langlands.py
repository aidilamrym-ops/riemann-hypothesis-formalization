import os
import fitz
import sys

path = r'D:\WORKSPACE\Langlands'
print(f"Path exists: {os.path.exists(path)}")
print(f"Files: {os.listdir(path)}")

for f in os.listdir(path):
    if f.endswith('.pdf'):
        fp = os.path.join(path, f)
        print(f"\n==========================================")
        print(f"FILE: {f}")
        print(f"==========================================")
        doc = fitz.open(fp)
        print(f"Total Pages: {len(doc)}")
        text = doc[0].get_text()
        print(text[:600])
        sys.stdout.flush()
