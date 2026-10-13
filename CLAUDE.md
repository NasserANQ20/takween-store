# Takween — instructions for Claude

## Current mode: learn only
Until Nasser says otherwise ("ولّد" or "ابدأ التوليد"):
- Do not generate video/images and do not spend Higgsfield credits.
- For every reference Nasser sends (TikTok, Instagram or LinkedIn link, or a Drive file): download it, analyse it, and add the analysis to `promo/references.md`.
  - Analyse: idea and structure, shot length (cut detection), brightness, contrast and saturation in numbers, typography, colours, sound, what to take for Takween.
- TikTok links: if yt-dlp fails, use Playwright with an iPhone user agent and pull the `<video>` src.

## Before any video work
- Read `promo/references.md` (style guide + measured quality spec) and follow it.
- Check the measured numbers on 30 frames before delivery. Brightness ≥0.45, whites p95 ≥0.92, saturation 0.20–0.30. Process shots 0.7–1.2 s, hero 2.5–3.5 s.
- Brand: "بنكهة ناصر": dark minimal with lime `#d8ff5c` accents, IBM Plex Sans Arabic, Inter and Alexandria, Aref Ruqaa for the «بقلم المهندس ناصر» signature only. No heavy grain or vignette, no copper serif type. End card: signature, @takweentables, 0504688928, «اطلبها الآن · TikTok Shop».
- Generation happens on Higgsfield (the user's credits), not Claude. Editing, motion graphics and analysis are done locally with ffmpeg and Playwright.
