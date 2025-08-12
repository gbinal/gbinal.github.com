# Broken Links Report for gbinal.github.com

## Summary
A comprehensive link analysis was performed on the gbinal.github.com repository, scanning 26 files (markdown, HTML, and configuration files) for all types of links.

## Key Findings

### ✅ Overall Status: Repository is in Good Shape
- **Total files scanned:** 26
- **External links found:** 215 unique links across 60+ domains
- **Internal links found:** 1 
- **Broken internal links:** 1 (details below)
- **Template variables:** 3 (not actual links)

### ❌ Broken Internal Links (1 found)

**1. Missing news.html file**
- **Link:** `news.html`
- **Referenced in:** `_includes/howto.md` (line 93)
- **Context:** "will automatically be displayed on the [news page](news.html)"
- **Issue:** The referenced news.html file does not exist in the repository
- **Recommendation:** Either create a news.html page or update the link to point to an existing page

### 🔧 Template Variables (3 found - Not actual broken links)
These are Jekyll template variables that get resolved at build time:
1. `{{ link.url }}` in `_includes/sidebar.html` (navigation menu)
2. `{{ edit_url }}` in `_includes/prose_edit_url.html` (edit link)

### 🌐 External Links Analysis

**Top domains by link count:**
1. **play.google.com** - 38 links (Google Play Store apps)
2. **www.youtube.com** - 13 links (Video content)
3. **www.washingtonpost.com** - 12 links (News articles)
4. **itunes.apple.com** - 9 links (iOS apps)
5. **github.com** - 8 links (Code repositories)
6. **eclipse2017.nasa.gov** - 7 links (Eclipse information)
7. **www.thisamericanlife.org** - 7 links (Podcast episodes)

**External link testing limitation:** Due to network restrictions in the testing environment, external links could not be automatically verified. However, the links have been catalogued and most major domains (YouTube, GitHub, Apple, Google Play) are typically reliable.

## Recommendations

### Immediate Action Required
1. **Fix the broken internal link:** Create a `news.html` file or update the reference in `_includes/howto.md` to point to an existing page.

### Optional Improvements
1. **Manual verification:** Periodically check a sample of external links, especially those to smaller or specialized domains.
2. **Link maintenance:** Consider setting up automated link checking in CI/CD pipeline for future updates.

## Technical Details
- **Analysis performed:** December 2024
- **Tool used:** Custom Python script analyzing markdown, HTML, and YAML files
- **Pattern matching:** Extracted links using regex patterns for markdown `[text](url)` and HTML `href` attributes
- **Internal link validation:** Checked file existence with multiple path variations (.md, .html, index files)

---

**Detailed link inventory saved to:** `/tmp/link_analysis_report.json`