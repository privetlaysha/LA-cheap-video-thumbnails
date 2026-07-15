# Prompt template — first generation (from raw screenshot)

Use this structure, filling in the bracketed parts from the questionnaire answers.
This is the version that reliably produces a real composited redesign instead of
"text pasted on the unedited screenshot" (the failure mode of vague prompts).

```
Redesign this into a punchy, professional YouTube thumbnail — do NOT just paste
text over the original photo. Actually re-edit the image:

1. SUBJECT: Crop tight on the person's face and upper chest/torso, positioned on
   the [LEFT/RIGHT/CENTER] of the frame. Add a [bright yellow-white / colored]
   rim-light glow outline around the silhouette to separate from the background.

2. BACKGROUND: Heavily blur and darken the background (strong bokeh, remove
   clutter). Add a subtle dark vignette so the subject pops.

3. COLOR GRADE: Boost contrast, saturation and clarity on the subject. Warm,
   punchy skin tones. Professionally color-graded, not a flat video screenshot.

4. HEADLINE TEXT: "[HOOK_PHRASE]" — [choose one style]:
   a) Thick condensed bold sans-serif (Impact/Anton-style), all caps, white
      fill with thick black outline (6-8px) and drop shadow, no background box.
   b) Same font, sitting on a rough hand-drawn marker-highlight stripe
      (uneven edges) — e.g. lime-green stripe for line 1, white/orange for line 2.
   c) White/black text on a solid or semi-transparent rounded badge.
   Position: [bottom-left / top / etc.], large enough to read at small size.

5. BALANCE — the side of the frame NOT occupied by the subject must be filled
   with graphic content (never leave one side empty while the other is busy):
   - Thematic icon cluster relevant to the topic: [list 3-5 icons based on
     topic keywords, e.g. brand logos/emblems, money graphics, relevant object
     silhouettes], arranged as a clean cluster, semi-transparent/blended so it
     looks designed, not stock-pasted.
   - Optional small badge (dark rounded rect, bold white/gold text) with a
     concrete number/fact pulled from the script: "[DATA_POINT]"

6. Overall: balanced composition across the full 16:9 frame, no dead empty
   areas, no duplicated elements (check: is any icon, number, or badge
   represented twice? If so, remove the duplicate before finalizing).

7. Aspect ratio [ASPECT_RATIO — 16:9, 1280x720 for standard YouTube thumbnail,
   or 9:16, 1080x1920 for Shorts/Reels/TikTok cover — resolved from the
   questionnaire, never left as a literal question in this prompt].
```

# Prompt template — revision/edit (from a previous accepted version)

Never re-describe the whole scene. Diff only.

```
Take this exact thumbnail image and fix ONE thing — keep everything else
([person, pose, glow, background, headline stripes, all other graphics])
pixel-for-pixel identical:

PROBLEM: [describe exactly what's wrong and where, e.g. "the trophy icon in
the top-left corner is redundant — trophy already appears in the emblem on
the right"]

FIX: [describe exactly what to do instead, e.g. "replace it with a dark
rounded badge showing '$100-200M SPONSORSHIP' in bold white/gold text,
same size/position as the icon it replaces"]

Do not change anything else — same [list everything that must stay identical].

Aspect ratio [ASPECT_RATIO — keep identical to the version being edited, unless
the user explicitly asks to change format].
```
