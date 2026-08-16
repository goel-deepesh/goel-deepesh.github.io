# Editing the wording yourself

Everything on the site is plain HTML. There is no build step, no framework and no
database. To change a sentence, you open the file, find the sentence, and type over it.

---

## The fastest loop

1. Open the folder in **VS Code** (or any text editor, TextEdit works).
2. Open `index.html`.
3. Change some text, save.
4. Double-click `index.html` in Finder to open it in your browser, or refresh the tab if
   it's already open.

That's the whole cycle. If you'd rather see changes without refreshing, run this from the
`site/` folder and open `http://localhost:8000`:

```bash
python3 -m http.server 8000
```

---

## Which file holds what

| You want to change | Open |
| ------------------ | ---- |
| Name, job title, intro paragraph, buttons | `index.html`, the `HERO` section |
| The "Recent work" background text | `index.html`, the `RESEARCH` section |
| The three project summary cards | `index.html`, the `WORK` section |
| Publication list | `index.html`, the `PUBLICATIONS` section |
| Job history | `index.html`, the `EXPERIENCE` section |
| Education and skills | `index.html`, the `BACKGROUND` section |
| Contact wording | `index.html`, the `CONTACT` section |
| The fake-news writeup | `work/fake-news-human-ai-divide.html` |
| The MRI writeup | `work/ivim-histology-validation.html` |
| The JEPA writeup | `work/jepa-world-model.html` |
| Fonts, colours, spacing | `style.css` |

Each section in `index.html` is marked with a comment banner like this, so you can search
for it:

```html
<!-- ============================ PUBLICATIONS ============================ -->
```

---

## The rule that keeps you out of trouble

**Text lives between tags. Tags are the bits in angle brackets. Change the text, leave the
tags alone.**

```html
<p>
  I build and evaluate machine learning systems.     ← edit this line freely
</p>
```

If a sentence has formatting inside it, the tags wrap the specific words they affect:

```html
<p>
  Detectors scoring <strong>97–99%</strong> on their own test sets dropped to 48–51%.
</p>
```

`<strong>` makes text bold, `<em>` makes it italic, `<a href="...">` makes it a link, and
`<sub>`/`<sup>` make subscript and superscript. Keep each opening tag paired with its
closing tag and you can rewrite everything around them.

Line breaks in the file don't appear on the page. HTML collapses them, so a paragraph can
be one long line or five short ones and it renders identically. Write it however is easiest
to read while editing.

---

## Things that will break the page, and how to avoid them

**Deleting half a tag.** If you delete `</p>` but leave `<p>`, everything after it may
inherit the wrong styling. If the page looks suddenly wrong after an edit, this is almost
always why. Undo and try again.

**Typing `<`, `>` or `&` as literal characters.** These mean something to HTML. Write them
as `&lt;`, `&gt;` and `&amp;` instead. This mostly comes up with things like "p &lt; 0.01".

**Smart quotes from a word processor.** If you draft in Word or Google Docs and paste in,
you may bring curly quotes and invisible characters. Draft in a plain text editor, or paste
and then retype the quotes.

**Renaming a file.** The pages link to each other by filename. If you rename
`work/jepa-world-model.html`, the links from the homepage stop working.

---

## Small edits you're most likely to want

**Change a section heading**

```html
<h2>Recent work</h2>
```

**Change the label above a heading**

```html
<p class="eyebrow">Background</p>
```

**Add a bullet to a job**

Copy an existing `<li>...</li>` line and edit it. Keep it inside the surrounding `<ul>`.

```html
<ul>
  <li>An existing bullet.</li>
  <li>Your new bullet.</li>
</ul>
```

**Add a publication**

Copy a whole `<div class="pub"> ... </div>` block, paste it below the last one, and change
the number, title, authors and venue. Your own name is wrapped in
`<span class="me">Deepesh Goel</span>` so it renders bolder than the co-authors.

**Add or change a tag chip**

```html
<span class="chip">PyTorch</span>
```

**Remove a whole section.** Delete from the `<section id="...">` line down to its matching
`</section>`, and remove the matching link in the nav bar at the top.

---

## Changing the look

All colours and type sit at the top of `style.css` as variables. Change one value there
and it updates everywhere:

```css
--text:   #15181c;   /* body text */
--accent: #1e4d7b;   /* links and highlights */
--bg:     #ffffff;   /* page background */
```

Dark mode has its own block a few lines below, under
`@media (prefers-color-scheme: dark)`. If you change a colour in one, change its
counterpart in the other.

To change the typeface, edit the `--sans` variable and update the Google Fonts `<link>` in
the `<head>` of all four HTML files to load the new family.

---

## If you break something

Nothing here is destructive as long as you can get back to a working copy.

- **Before a big edit**, duplicate the folder. That's your undo.
- **Once it's on GitHub**, every commit is a restore point. The repo's commit history lets
  you view or revert any earlier version of a file from the web interface.
- **Editing directly on GitHub** (click a file, then the pencil icon) is often the safest
  path for small wording changes, because the change is committed separately and you can
  revert just that commit.

---

## What to be careful about rewriting

The three writeup pages state specific figures taken from your papers: accuracies, patient
counts, correlation values, presentation venues. Rewording the prose around them is
completely safe. If you change a number, check it against the source PDF first, because
these are the claims a reader is most likely to verify.
