---
name: LA-video-thumbnails
description: >-
  Generate YouTube thumbnails from a video screenshot plus title/script using
  Google Nano Banana 2 (via Replicate). Use when the user shares a video
  screenshot and wants a thumbnail, mentions "video thumbnails", "nano
  banana", "обложка для видео", "YouTube thumbnail", or asks to
  design/redesign a video cover. Handles the full flow — extract hook phrases
  from the title/script, run a short or full questionnaire, build a validated
  prompt, generate via Replicate, and iterate on the SAME generated file (not
  from scratch) for revisions.
---

# Nano Banana Thumbnail Generator

Produces composited, professional-looking YouTube thumbnails (not "text pasted on a screenshot") from a raw video screenshot, using Google's `google/nano-banana-2` model on Replicate.

## Prerequisites

### Replicate account + API token (one-time setup)
1. Create a free account at https://replicate.com (sign in with GitHub/Google/email).
2. Add a payment method under Account settings → Billing — Nano Banana 2 runs cost a few cents per image, there's no free tier, but no subscription either (pay-per-generation).
3. Go to https://replicate.com/account/api-tokens and create a token (starts with `r8_...`).
4. Do NOT paste the token into chat. Store it as an environment variable on your machine instead, e.g. add to `~/.zshrc`:
   `export REPLICATE_API_TOKEN="r8_xxxxxxxx"`
   then restart the terminal / run `source ~/.zshrc`.
5. If the token ever does end up pasted in chat by accident, revoke it immediately at the link above and generate a new one.

### Verify the token works
Ask Claude to run (via Desktop Commander, not the sandboxed bash tool):
`curl -s -H "Authorization: Token $REPLICATE_API_TOKEN" https://api.replicate.com/v1/account`
A successful response returns your Replicate username as JSON.

### Runtime notes
- Run all Replicate calls and file I/O through **Desktop Commander** (the user's real machine), not the sandboxed bash tool — the sandbox's network proxy blocks `api.replicate.com` and `replicate.delivery`. Desktop Commander's shell has direct internet access.
- If Claude doesn't have Desktop Commander connected yet, that's the first thing to set up — it's a separate MCP connection, not part of this skill.
- Never print/echo the API token in chat, ever — always reference it as `$REPLICATE_API_TOKEN` in commands, reading it from the environment.

## Workflow

### 1. Collect inputs
Ask the user for (if not already provided):
- A screenshot from the video (file path, e.g. on Desktop or Downloads — search for it if they just say "the screenshot")
- The video title/topic, and ideally the full script or description (more text = better hook extraction)
- Format: standard YouTube thumbnail (16:9, 1280x720) or Shorts/Reels/TikTok cover (9:16, 1080x1920)? Default to 16:9 unless the user says otherwise or the source screenshot is clearly vertical.

This resolves the aspect ratio ONCE, up front — never leave "ask user" or similar placeholder text inside a prompt that gets sent to the image model itself (see `reference/prompt_template.md` — it uses `[ASPECT_RATIO]` as a placeholder that must be filled with the resolved value before sending).

### 2. Extract hook phrase candidates
Read the title/script and pull out 3-4 short (2-4 word) hook phrases — the most clickable, concrete claims or numbers (a stat, a contradiction, a named brand/entity). Present them as options and let the user pick one or write their own. Example from a past session (ЧМ-2026 sponsorship video):
- "РОЗОВЫЕ БУТСЫ ВСЕХ"
- "NIKE НЕ ПЛАТИТ FIFA"
- "ДЕНЬГИ И БРЕНДЫ ЧМ"
- "LEVI'S ВЗОРВАЛИ ТУРНИР"

### 3. Questionnaire

**Quick mode (default)** — 3 questions, everything else uses smart defaults inferred from the topic:
1. Тон обложки — деловой / кликбейт-хайп / нейтральный
2. Стиль текста — маркер-хайлайтер полосой / плашка-бейдж / просто жирный текст с обводкой
3. Тематическая графика — да (я сама предложу 3-5 иконок по теме) / нет

**Full mode** (if user asks for more control) — adds:
4. Расположение человека в кадре (слева/справа/центр, кроп)
5. Обводка/глоу вокруг человека — да/нет, цвет
6. Обработка фона — блюр+затемнение оригинала / полная замена / почти не трогать
7. Доп. бейдж с цифрой/фактом — что именно написать (тяни цифры из сценария, если он есть — see past example: "$100-200M SPONSORSHIP" pulled directly from user's script)
8. Цветовая палитра — под бренд из темы, или фирменные цвета канала
9. Логотип/вотермарка канала — вставлять или нет
10. Референс — ссылка на понравившуюся обложку (YouTube URL). If given, fetch its thumbnail (`https://img.youtube.com/vi/{VIDEO_ID}/maxresdefault.jpg` via Desktop Commander curl) and view it (Desktop Commander `read_file` on the downloaded image renders it inline) to reverse-engineer its design techniques before building the prompt.

Show the assembled final prompt as text before sending it to Replicate, so the user can tweak wording first.

### 4. Pre-flight validation checklist (run silently before every generation)
- No duplicated elements (e.g. same number/icon appearing twice — this was the #1 recurring bug)
- No more than 2-3 distinct text blocks
- Composition balance: if the subject occupies one side, the opposite side must have graphic content (icons/badges/text) — never leave one side empty and the other crowded
- Text contrast against whatever is behind it (dark text needs light background/stripe and vice versa)

### 5. Generate
Use `scripts/generate_thumbnail.py` (run via Desktop Commander `start_process`, not the sandbox). First generation uses the raw screenshot as `image_input`. See `reference/prompt_template.md` for the base prompt structure that reliably avoids the "just text pasted on the original photo" failure mode.

### 6. Iterate on revisions — CRITICAL RULE
**Never regenerate from the original screenshot when making a revision.** Always use the most recent ACCEPTED output file as `image_input`, and phrase the prompt as a targeted diff:
- State the current problem explicitly (what's wrong, where)
- State the fix explicitly (what to add/remove/replace, and where)
- End with: "Do not change anything else — same [person/pose/glow/background/headline/etc.], pixel-for-pixel identical except for the fix above."

Only regenerate from the original screenshot if the user explicitly asks to start over / try a completely different direction.

### 7. Version files
Save each generation as `{descriptive_name}_v{N}.jpeg` in the same folder as the source screenshot (e.g. Desktop). Keep all versions — don't overwrite. View each result with Desktop Commander `read_file` (renders inline) before showing/describing it to the user — never describe a thumbnail you haven't actually looked at.

### 8. Learn from feedback
When the user rejects/critiques a version, don't just fix and move on — note *why* it failed in `reference/lessons_learned.md` (append). Over multiple thumbnails for the same channel, these notes become that channel's style profile — use them as defaults for future requests instead of re-asking the full questionnaire.

## Known failure modes (from real testing)

- **Plain `nano-banana`** (not `-2`) tends to conservatively preserve the original photo and just overlay text — background stays cluttered, no real recomposition. Always use `google/nano-banana-2` unless the user asks otherwise.
- Vague instructions like "boost contrast, clean composition" get ignored if the background isn't explicitly told to blur/darken/recompose.
- Thin text outlines read as weak/ugly at thumbnail size — use thick bold outlines or highlighter-stripe backgrounds instead.
- Empty space on one side of frame reads as "unbalanced" — always add graphic content to whichever side is emptier.
- Redundant elements (same icon/number appearing in two places) happen when the prompt describes the whole scene from scratch instead of diffing against the current state — always diff against the current file for edits.
