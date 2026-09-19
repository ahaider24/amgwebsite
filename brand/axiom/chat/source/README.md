# Geist outlines

The 400 and 500 JSON files are genuine Geist outlines extracted from `brand/fonts/Geist-googlefonts-latin.woff2` using `brand/source/font-outlines.c`. Geist 700 is read directly from the existing `brand/source/geist-700-outlines.json`. All sources remain unchanged.

Use FreeType with WOFF2 support to regenerate. This machine's Homebrew FreeType lacks WOFF2 support; the cached Pillow FreeType has it. From the repository root:

```sh
cc brand/source/font-outlines.c -I/opt/homebrew/include/freetype2 /Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/PIL/.dylibs/libfreetype.6.dylib -o /private/tmp/agl-chat-font-outlines
DYLD_LIBRARY_PATH=/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/PIL/.dylibs /private/tmp/agl-chat-font-outlines brand/fonts/Geist-googlefonts-latin.woff2 400 > brand/axiom/chat/source/geist-400-outlines.json
DYLD_LIBRARY_PATH=/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/site-packages/PIL/.dylibs /private/tmp/agl-chat-font-outlines brand/fonts/Geist-googlefonts-latin.woff2 500 > brand/axiom/chat/source/geist-500-outlines.json
```

Do not accept an empty output file. The builder parses both JSON files before drawing, and records their hashes. Source font licensing is at `brand/fonts/OFL.txt`.
