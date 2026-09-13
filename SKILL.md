---
name: moments-memoir
description: Analyze an already-exported WeChat Moments archive (moments.md + figure/ + coverage.json) and turn it into a curated personal memoir — responsive story website with optional background music. Guides the user through exporting first (wxMoments GitHub tool), then asks structured questions (time range, style, music, privacy) before generating. Use when a user wants a meaningful, fact-based summary of their Moments with photos, comments, custom visual style, and privacy-aware publication.
---

# Moments Memoir

Analyze an already-exported WeChat Moments archive and produce a selective, factual, emotionally coherent memory work as a responsive website. This skill does **not** handle WeChat login, database decryption, or raw data export.

## Two-step workflow

### Step 1: Set up the export (AI does it, user just double-clicks)

If the user has not yet exported their Moments, **do not tell them to open cmd and type commands yourself.** Instead:

1. Check if Python 3 is installed (`python --version` or `py --version`). If not, tell the user to install Python from python.org and wait.
2. Clone [wxMoments](https://github.com/claudemt/wxMoments) to a stable location (e.g. `%LOCALAPPDATA%\MomentsMemoir\wxMoments`).
3. Create a one-click batch file on the user's Desktop (e.g. `导出朋友圈.cmd`) that:
   - Opens a visible terminal window
   - Runs the wxMoments export script
   - Keeps the window open after finishing so the user can see the output path
4. Tell the user: "我已经帮你准备好了，双击桌面上的 `导出朋友圈.cmd`，扫码确认，等它跑完，然后回来告诉我文件夹在哪。"
5. Wait for the user to come back with the export directory path. The user does not need to type any commands themselves.

The batch file content:
```bat
@echo off
chcp 65001 >nul
title 导出朋友圈
cd /d "%LOCALAPPDATA%\MomentsMemoir\wxMoments"
echo 请在下方扫码确认微信登录，然后按提示操作...
python run.bat
echo.
echo 导出完成！文件夹在当前目录下的 output 文件夹里。
pause
```

### Step 2: Ask questions before generating

Once the export directory is available, ask the user a compact set of questions. **Use multiple-choice options as the primary format** (not open-ended text). After the options, always include one free-text field ("其他补充（选填）") where they can add anything the options didn't cover.

Ask these questions in one batch:

1. **时间范围**：全部年份 / 2020-2022 / 2023-2026 / 自定义（填空）
2. **视觉风格**：暖色手账风（默认，推荐）/ 电影质感深色 / 杂志排版 / 极简时间线 / 自由描述（填空）
3. **背景音乐**：不需要 / 需要（推荐：谭咏麟《无言感激》）/ 其他歌曲（填空）
4. **隐私处理**：三字名取后两字（默认）/ 两字名保留 / 全部用昵称或关系称呼（如"朋友""室友"）
5. **补充说明（选填）**：特别想强调的事、不想公开的内容、其他要求

Do not repeat questions already answered. Apply defaults if the user says "你看着办" or skips: all years, warm scrapbook style, no background music, three-character names → last two characters.

## Input contract

The user provides a directory containing the wxMoments export output:

- `moments.md` — chronological Markdown of all posts (primary source)
- `figure/` — image subdirectories keyed by timestamp
- `coverage.json`, `params.json` — date range and export metadata

If the user provides a PDF only, locate the companion export directory on disk; if it cannot be found, ask the user for the export folder path.

## Extract facts from data, never assume

**This is the most common failure mode.** Before writing any chapter:

1. **Read the full `moments.md`** end to end. Do not skim. Count the lines, track the timeline, and note every self-referential fact (school, major, department, city, dorm, job, project name, relationship status, family members).
2. **Never infer any personal fact from stereotypes, campus names, location cues, or common patterns.** If the posts mention a campus but never name the department, do not guess which college it belongs to. If a post says "在上海实习" but never names the company, do not guess which tech firm. Search for self-disclosure keywords first; if the fact is not explicitly stated in the text, **ask the user**.
3. **Cross-reference key events.** "转专业成功" appears in a specific dated post; cite that date. A project name appears with its own post; link it to the right period.
4. **Distinguish explicit facts from inference.** A post saying "被之前的专业折磨得太惨" tells you the previous major was disliked, not what it was called. Only write down what the text actually says.
5. **Run `scripts/inspect_export.py EXPORT_DIR --output ANALYSIS_JSON`** for counts and coverage gaps. Treat its flags as candidates for review, not final truth.

## Protect identity and private data

- Work locally by default. Publishing requires the user's intent.
- Do not expose the raw archive, contact list, or original database in a public deliverable.
- Keep raw facts separate from editorial inference.
- Apply the user's chosen name-privacy rule consistently.

## Editorial workflow

Read [editorial method](references/editorial-method.md) before selecting chapters or writing. Preserve meaningful transitions, relationships, creative work and representative comments. Remove low-value material without erasing ordinary life that gives the story texture.

### Image-text matching rule

For every image placed next to text, the image must actually depict what the surrounding paragraph describes:

1. **Do not grab the nearest timestamp directory blindly.** Look at the post's text content first, then choose the figure directory whose post matches that text.
2. **Verify the image visually before placing it.** Open the image and confirm it shows the event, place, or subject described in the caption. If it doesn't match, pick a different one.
3. **When multiple images exist for one post, pick the one that best illustrates the narrative point.** Skip generic screenshots that don't add visual meaning.
4. **If no suitable image exists for a passage, leave it without an image rather than forcing a mismatched photo.**

Read [workflow and progress](references/workflow.md) for stage boundaries.

### Background music

If the user requests background music:
- Add an `<audio>` element or a music player toggle button to the website.
- The audio file should be placed in the website directory and referenced by relative path.
- Default to off (user clicks to play) — never autoplay.
- If the user names a specific song, ask them to provide the audio file; do not search the web for it.

## Post-generation verification (mandatory)

After building the complete website, **re-read every image and its surrounding caption** before deploying:

1. Open each image file and confirm its content matches the paragraph and caption.
2. Check that no image is from a different post's timestamp directory.
3. Verify captions accurately describe what is in the photo (not just what the surrounding text says).
4. Check that no personal name in text or comments violates the privacy rule.
5. Verify date ranges and counts match `coverage.json` / `inspect_export.py`.

Fix any mismatch before telling the user it's done.

## Deployment

When the user wants to put the website online:

- Use **surge.sh** free hosting. Do not deploy directly from the agent's terminal.
- Create a Windows batch file on the user's desktop (e.g. `deploy-memoir.cmd`) that runs `surge . --domain <chosen-name>.surge.sh`.
- The first time, the batch file will prompt for surge email and password in a visible terminal window. The user enters these personally.
- After first login, credentials are saved and future deploys are non-interactive.
- Tell the user to double-click the batch file if they want to deploy themselves.

For a website, either adapt `assets/web-starter/` or build an equivalent responsive site. The starter supports preset themes through `data-theme`.

## Deliver

The final response should lead with the artifact link or local path, summarize the selected style and scope, state coverage limitations, and list any factual uncertainties.

For environments that do not natively load Agent Skills folders, read [portable use](references/portable-use.md).
