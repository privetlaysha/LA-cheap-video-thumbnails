# Lessons learned log

Append an entry here every time a generated thumbnail gets rejected or
critiqued, so future defaults improve. Format:

## [date] — [channel/project name]
- What was wrong:
- What fixed it:
- Takeaway for future defaults:

---

## 2026-07-15 — Laysha Production (ЧМ-2026 Nike/FIFA video)

- What was wrong (v1, plain `nano-banana`): background completely untouched
  (lamp, plant, books still sharp and cluttered), no crop, thin red-outline
  text on a plain badge — looked like text pasted on a raw screenshot, not a
  designed thumbnail.
- What fixed it: switched to `nano-banana-2`, and rewrote the prompt to
  explicitly command background blur/darken/vignette, rim-light glow around
  the subject, thick bold text with drop shadow, and — critically — added
  instructions to fill the empty side of the frame with topic-relevant
  graphics (FIFA World Cup emblem, money graphics, jersey/cleat icons).
- Takeaway: vague quality instructions ("boost contrast", "clean
  composition") get ignored unless paired with explicit "recompose/blur/crop"
  verbs. Composition balance (something on both sides of frame) needs to be
  stated explicitly — models default to leaving the non-subject side empty.

- What was wrong (v3 → v4): duplicated "2026" (once in a red top-left badge,
  once inside the FIFA emblem) and two trophy illustrations (one solid, one
  semi-transparent duplicate) — redundant elements from describing the full
  scene fresh each time instead of diffing against the previous version.
- What fixed it: switched to diff-style edit prompts that reference the
  CURRENT image as input and explicitly state "remove X, keep everything
  else identical."
- Takeaway: always edit from the last accepted file, never regenerate the
  full scene description for a revision — full-scene descriptions invite the
  model to improvise new (often redundant) elements.

- What was wrong (v4 → v5): the top-left trophy icon added no information
  (trophy already present in the FIFA emblem on the right).
- What fixed it: replaced it with a concrete data badge ("$100-200M
  SPONSORSHIP") pulled directly from the video's script — more informative
  and more clickable than a decorative icon.
- Takeaway: when a corner/slot feels empty or redundant, prefer a concrete
  number/fact from the source script over a generic decorative icon.
