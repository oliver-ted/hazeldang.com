# hazeldang.com

Portfolio site for Han (Hazel) Dang, served by GitHub Pages at https://hazeldang.com.

## What lives where
- `index.html` is the live site. It is generated, so don't edit it by hand.
- `source/src.html` is the page itself (text, styles, animations). Images are written as `{{name}}` placeholders.
- `source/assets/` holds the photo, logos, tool icons and Anatomi screenshots that get inlined.
- `source/build.py` turns the source into `index.html`.
- `CNAME` tells GitHub Pages to serve the site on hazeldang.com. Keep it.

## Making a change
1. Edit `source/src.html` (or swap a file in `source/assets/`, keeping the same name).
2. Run `python3 source/build.py`.
3. Commit and push to `main`. GitHub Pages republishes in about a minute.
