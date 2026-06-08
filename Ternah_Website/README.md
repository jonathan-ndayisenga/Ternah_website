# Ternah Software Company Ltd — Website (multi-page)

Plain, standalone HTML pages sharing one stylesheet and one script. No build step,
no framework, easy to edit and maintain.

## Structure
```
/
├── index.html          ← Home
├── about.html          ← About
├── solutions.html      ← Solutions
├── industries.html     ← Industries
├── projects.html       ← Projects
├── insights.html       ← Insights
├── contact.html        ← Contact
└── assets/
    ├── css/styles.css   ← all styling (one file)
    └── js/main.js       ← nav, scroll reveals, hero waves, contact form
```

Each `.html` file is fully self-contained markup. They all link the same
`assets/css/styles.css` and `assets/js/main.js`, so a change to the look or behaviour
is made once and applies everywhere.

## How navigation / active link works
Every page sets `<body data-page="…">` (e.g. `data-page="about"`). `main.js` reads that
and highlights the matching nav link automatically. To add a page, copy an existing file,
change the `data-page` value, the `<title>`, and the content.

## Editing content
- **Text & sections:** edit directly in the relevant `.html` file — it's normal HTML.
- **Colors / spacing / fonts:** the CSS variables at the top of `assets/css/styles.css`
  (`--navy`, `--blue`, `--blue-soft`, etc.).
- **Hero animation:** the wavy canvas lives in `main.js` (the `#waves` block). It only runs
  on pages that contain a `<canvas id="waves">` — currently just the home page.

## How to publish
- **Netlify (easiest):** drag the whole folder onto https://app.netlify.com/drop
- **GitHub Pages:** push the folder to a repo → Settings → Pages → deploy from branch (root)
- **Any host / cPanel:** upload the folder to your web root. `index.html` is the entry point.
- **Local preview:** double-click `index.html`.

## Fonts
Manrope + Sora load from Google Fonts. Want it fully offline? Tell me and I'll bundle the
font files into `assets/fonts/` and switch the CSS to local `@font-face`.

## Contact details wired in
- Email: ternah22@gmail.com
- Phone: +256 787 770007

The contact form opens the visitor's email app pre-filled to that address. To receive
submissions automatically instead, connect it to Netlify Forms or Formspree (ask me and
I'll wire it up).

## Note on the builder file
`build_pages.py` is the optional generator I used to stamp the shared header/footer into
each page. You don't need it to run or host the site — the `.html` files are final. Keep it
only if you'd like to regenerate pages from one template later.
