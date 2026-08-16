# Deploying to deepeshgoel.com

Two phases. Get the site live on a GitHub URL first and confirm it looks right. Only then
move the domain. Your Google Sites version stays up untouched until the final step, so
there's no window where deepeshgoel.com is broken.

Budget about 20 minutes of actual work, plus waiting for DNS.

---

## Phase 1: Put the site on GitHub

### 1. Create the repository

On GitHub, click **New repository**. Name it exactly:

```
goel-deepesh.github.io
```

Set it to **Public**. Don't add a README, .gitignore or licence, since the folder already
has what it needs. Click **Create repository**.

The name has to match your username. That's what makes GitHub treat it as your personal
site and serve it at the domain root rather than under `/repo-name/`.

### 2. Upload the files

**The contents of the `site` folder go in the repository root.** Not the folder itself.
`index.html` must sit at the top level of the repo, not inside a `site/` subfolder. This is
the single most common way this goes wrong.

Easiest route, no command line:

1. On the empty repo page, click **uploading an existing file**.
2. Open the `site` folder in Finder, select all (⌘A), and drag everything into the browser.
3. Scroll down, click **Commit changes**.

If you'd rather use the terminal:

```bash
cd ~/Documents/website/site
git init
git add -A
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/goel-deepesh/goel-deepesh.github.io.git
git push -u origin main
```

**Two files look like clutter and are not.** `.nojekyll` stops GitHub trying to run the
site through Jekyll, which would ignore some files. `CNAME` holds your domain. Both must
make it into the repo. Finder hides dotfiles, so if you drag-and-drop, press
**⌘⇧.** first to reveal them, or use the terminal route which picks them up automatically.

### 3. Turn on Pages

Go to the repo's **Settings → Pages**. Under *Build and deployment*:

- Source: **Deploy from a branch**
- Branch: **main**, folder **/ (root)**
- Click **Save**

Wait a minute or two, then open **https://goel-deepesh.github.io**

### 4. Check it before going further

- Homepage loads with styling. If the text appears unstyled, `style.css` didn't land in the
  root.
- All four writeup pages open from the cards.
- The back arrow returns you to the homepage.
- The favicon appears in the tab.
- Your photo loads.
- On your phone, the layout stacks and nothing scrolls sideways.

Fix anything broken now, while the domain is still pointing at the old site.

---

## Phase 2: Move the domain

Google Sites and GitHub Pages both want to answer for `deepeshgoel.com`, and they can't
both. Order matters here.

Everything below happens at your **registrar** (wherever you bought the domain) except
step 1. If you bought it through Google Domains, that business moved to Squarespace, so
that's where you'll log in.

### Step 1: Tell GitHub about the domain

Repo **Settings → Pages → Custom domain**. Enter:

```
www.deepeshgoel.com
```

Click **Save**. GitHub will run a DNS check and it will fail. That's expected; the records
don't exist yet.

> Saving this rewrites the `CNAME` file in your repo. If you're working from a local clone,
> run `git pull` before your next push or you'll hit a merge conflict.

### Step 2: Release the domain from Google Sites

Open your old site in Google Sites → **Settings → Custom domains** → remove
`deepeshgoel.com`.

Do this before changing DNS. If the domain is still claimed there, certificate issuing on
the GitHub side can fail in ways that are annoying to diagnose.

### Step 3: Replace the DNS records

In your registrar's DNS settings, **delete** the records Google Sites created. These are
usually four `A` records pointing at `216.239.x.x` addresses, and a `CNAME` on `www`
pointing at `ghs.googlehosted.com`.

Then add these:

| Type    | Name  | Value                    |
| ------- | ----- | ------------------------ |
| `CNAME` | `www` | `goel-deepesh.github.io` |
| `A`     | `@`   | `185.199.108.153`        |
| `A`     | `@`   | `185.199.109.153`        |
| `A`     | `@`   | `185.199.110.153`        |
| `A`     | `@`   | `185.199.111.153`        |

Optionally add IPv6 as well:

| Type   | Name | Value                 |
| ------ | ---- | --------------------- |
| `AAAA` | `@`  | `2606:50c0:8000::153` |
| `AAAA` | `@`  | `2606:50c0:8001::153` |
| `AAAA` | `@`  | `2606:50c0:8002::153` |
| `AAAA` | `@`  | `2606:50c0:8003::153` |

**What each does.** The `CNAME` on `www` is what actually serves the site. The `A` records
on `@`, meaning the bare `deepeshgoel.com`, exist so GitHub can redirect the bare domain to
the www one. Skip them and `deepeshgoel.com` without the www simply won't load.

The `CNAME` value is `goel-deepesh.github.io`. Your username, no repository name, no
`https://`, no trailing slash.

### Step 4: Wait, then turn on HTTPS

DNS usually propagates in 15 to 60 minutes and can take up to 24 hours. Check from
Terminal:

```bash
dig www.deepeshgoel.com +short      # expect: goel-deepesh.github.io
dig deepeshgoel.com +short          # expect: the four 185.199.x.x addresses
```

Once GitHub's DNS check turns green, it issues a Let's Encrypt certificate, which can take
another hour. When **Enforce HTTPS** becomes clickable in Settings → Pages, tick it.

You're done when all four of these land on the HTTPS site:

- `deepeshgoel.com`
- `www.deepeshgoel.com`
- `http://deepeshgoel.com`
- `http://www.deepeshgoel.com`

---

## Right after launch

**Verify the domain.** GitHub **account** settings → **Pages** → *Add a domain*. This
stops anyone else pointing their repo at your domain. Two minutes, worth doing.

**Submit to Google.** [Search Console](https://search.google.com/search-console), add
`https://www.deepeshgoel.com`, and submit `sitemap.xml`. Without this, indexing can take
weeks. Your old Google Sites pages may linger in results for a while regardless.

**Check the link preview.** Paste your URL into a Slack or LinkedIn message and confirm the
card shows your photo and title. That comes from `assets/og-image.jpg`.

---

## Making changes later

Every page is plain HTML with no build step. Edit, commit, and the live site updates in
about a minute.

For small wording changes, editing directly on GitHub is safest: open the file, click the
pencil, edit, commit. Each change is its own commit, so you can revert exactly one thing if
you don't like it. See `EDITING.md` for what lives where.

---

## If something goes wrong

**Unstyled page, plain black text on white.** `style.css` isn't in the repo root, or the
whole `site` folder got uploaded as a subfolder.

**404 on the custom domain.** The `CNAME` file and the custom domain in Settings → Pages
have to match exactly. Re-save one of them.

**"Domain is already taken."** Still claimed somewhere else, usually the old Google Sites
config or another repo of yours.

**Certificate won't issue.** Nearly always leftover DNS records. Remove the custom domain
in Settings → Pages, wait ten minutes, add it back. That forces a retry.

**Old site still showing.** Browser or DNS cache. Try a private window, or
`sudo dscacheutil -flushcache` on macOS.

**Images missing but text fine.** The `assets` folder didn't upload. Check it exists in the
repo with all thirteen files.
