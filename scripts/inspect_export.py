#!/usr/bin/env python3
"""Inventory a wxMoments export for editorial review without deciding the story."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re

POST = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+·\s+(.+?)\s*$", re.M)
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LIKE = re.compile(r"^\*\*❤️\s*点赞\*\*[：:]\s*(.*)$", re.M)
COMMENT = re.compile(r"^-\s+(.+?[：:].+)$", re.M)
LINK = re.compile(r"^🔗\s+\*\*链接\*\*[：:]\s*(\S+)", re.M)
CREATIVE = re.compile(r"(临江仙|满江红|青玉案|江城子|沁园春|行香子|卜算子|七律|七绝|五律|五绝|诗|词|画|作品|视频|摄影|音乐)")
EVENT = re.compile(r"(毕业|入学|录取|转专业|获奖|比赛|项目|实习|工作|旅行|告别|生日|第一次|终于|决定|离开|搬|回家)")
AD = re.compile(r"(优惠券|拼单|砍价|代购|返现|推广|扫码领取|限时优惠|下单|带货)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a completed wxMoments export")
    parser.add_argument("export_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gap-days", type=int, default=120)
    return parser.parse_args()


def clean_body(block: str) -> str:
    lines = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("![") or line.startswith("**❤️") or line.startswith("**💬") or line.startswith("- ") or line.startswith("🔗"):
            continue
        lines.append(line)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    export_dir = args.export_dir.expanduser().resolve()
    markdown = export_dir / "moments.md"
    if not markdown.is_file():
        raise SystemExit(f"Missing {markdown}")
    source = markdown.read_text(encoding="utf-8-sig")
    matches = list(POST.finditer(source))
    posts = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        block = source[match.end():end]
        like_match = LIKE.search(block)
        likes = [name.strip() for name in re.split(r"[、,]", like_match.group(1)) if name.strip()] if like_match else []
        comments = COMMENT.findall(block)
        body = clean_body(block)
        date = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        images = IMAGE.findall(block)
        score = min(5, len(images)) + min(5, len(likes) // 5) + min(5, len(comments))
        if EVENT.search(body):
            score += 5
        if CREATIVE.search(body):
            score += 3
        if len(body) >= 100:
            score += 2
        posts.append({
            "datetime": match.group(1),
            "author": match.group(2).strip(),
            "text": body,
            "images": images,
            "like_count": len(likes),
            "comments": comments,
            "links": LINK.findall(block),
            "signals": {
                "event": bool(EVENT.search(body)),
                "creative": bool(CREATIVE.search(body)),
                "possible_ad": bool(AD.search(body)),
                "editorial_score": score,
            },
            "_date": date,
        })

    chronological = sorted(posts, key=lambda item: item["_date"])
    gaps = []
    for left, right in zip(chronological, chronological[1:]):
        days = (right["_date"] - left["_date"]).days
        if days >= args.gap_days:
            gaps.append({"after": left["datetime"], "before": right["datetime"], "days": days})

    for post in posts:
        post.pop("_date", None)
    years = Counter(post["datetime"][:4] for post in posts)
    figures = [path for path in (export_dir / "figure").rglob("*") if path.is_file()] if (export_dir / "figure").is_dir() else []
    candidates = sorted(posts, key=lambda item: (item["signals"]["editorial_score"], item["datetime"]), reverse=True)[:80]
    coverage_file = export_dir / "coverage.json"
    coverage = json.loads(coverage_file.read_text(encoding="utf-8-sig")) if coverage_file.is_file() else None
    result = {
        "export_dir": str(export_dir),
        "summary": {
            "post_count": len(posts),
            "image_references": sum(len(post["images"]) for post in posts),
            "media_files": len(figures),
            "posts_with_likes": sum(bool(post["like_count"]) for post in posts),
            "posts_with_comments": sum(bool(post["comments"]) for post in posts),
            "first_datetime": chronological[0]["datetime"] if chronological else None,
            "last_datetime": chronological[-1]["datetime"] if chronological else None,
            "posts_by_year": dict(sorted(years.items())),
            "gaps": gaps,
        },
        "coverage": coverage,
        "candidate_posts": candidates,
        "posts": posts,
        "notice": "Signals and scores are review aids, not final editorial decisions.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(f"analysis={args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
