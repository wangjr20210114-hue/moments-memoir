# Workflow and progress

Use visible stages for this long task. Percentages are phase bands, not invented estimates of bytes or posts.

The input is an already-exported Moments directory. There is no WeChat login, decryption, or export step.

| Band | Stage | Completion evidence |
|---|---|---|
| 0–5% | Preflight | Export directory located; moments.md, figure/, coverage.json confirmed |
| 5–12% | Ask questions | User answered time range, style, music, privacy, optional free-text |
| 12–25% | Read full archive | moments.md read end to end; key facts extracted |
| 25–30% | Inventory | Counts, date coverage, gaps verified via inspect_export.py |
| 30–40% | Fact verification | Self-disclosed facts cross-referenced; unresolved details flagged for user |
| 40–55% | Editorial pass | Periods, events, motifs selected; chapters outlined |
| 55–75% | Visual production | Style chosen, images copied and visually verified, responsive site built |
| 75–85% | Post-generation verification | Every image re-opened and checked against its caption; no mismatches |
| 85–95% | Build and QA | Desktop/mobile render, interactions, privacy, broken assets, music toggle checked |
| 95–100% | Delivery | Local package ready; hosted version ready only when requested |

## Question flow (stage 5–12%)

Ask all questions in one batch using multiple-choice options. After options, always include an optional free-text field.

1. 时间范围：全部 / 早段 / 近段 / 自定义
2. 视觉风格：暖色手账（默认）/ 电影质感 / 杂志排版 / 极简时间线 / 自由描述
3. 背景音乐：不需要 / 需要（推荐《无言感激》）/ 其他（填空）
4. 隐私处理：三字名取后两字（默认）/ 两字名保留 / 全部关系称呼
5. 补充说明（选填）

## Progress contract

- Show the current stage, elapsed time, last completed milestone and next action.
- Clearly label `处理中`, `已完成`, `需要处理` and `失败` states.
- Do not invent counts or dates; every number must come from the export or inspect script.

## Fact-checking discipline

Before writing any chapter, verify every personal fact against the source:

1. **Never infer any personal fact from stereotypes, campus names, location cues, or common patterns.** This applies to department/major, company name, relationship status, hometown, family details, and any other biographical detail.
2. If a fact is never explicitly stated in the posts, **ask the user** rather than guessing.
3. Cross-reference dated events: when a post says "转专业成功", note the exact date.
4. When in doubt, write around the uncertain detail or ask — never invent a name, institution, or relationship.

## Post-generation verification (mandatory, stage 75–85%)

After building the complete website, before deployment:

1. Open every image file and confirm its content matches the paragraph and caption.
2. Check no image is from a different post's timestamp directory.
3. Verify captions accurately describe what is in the photo.
4. Check no personal name violates the privacy rule.
5. Verify date ranges and counts match the source.

Fix any mismatch before delivery.

## Parallel work

Safe work while reading the archive:

- ask for style and music choices;
- create the design tokens and empty responsive shell;
- prepare neutral privacy labels.

After reading is complete:

- inventory and cache-gap analysis;
- media selection and image copying;
- timeline/event clustering;
- privacy scan and name-label mapping.
