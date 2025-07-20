#!/usr/bin/env python
# Test script to run md2tex directly

from md2tex import md2tex

# Call the function directly
result = md2tex(
    "../SDPAF_Academic_Paper.md",
    outpath="../SDPAF_Academic_Paper.tex",
    tex=True,
    template="utils/template.tex",
    french_quote=False,
    unnumbered=False,
    document_class="article"
)

print("Conversion completed")