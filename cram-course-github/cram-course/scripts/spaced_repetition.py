#!/usr/bin/env python3
"""
spaced_repetition.py — 基于间隔重复原理生成复习日历

用法:
    python spaced_repetition.py --topics study_materials.json --exam-date "2026-06-28" --output "40_间隔复习计划.md"

输出: Markdown 格式的每日复习日历，按间隔重复规律排布。
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta


def configure_utf8_output():
    """Keep CLI output readable in Git Bash, CI, and modern Windows terminals."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


# 默认间隔重复间隔（天）
DEFAULT_INTERVALS = [1, 3, 7, 14]

# 默认每日可用复习时间（小时）
DEFAULT_DAILY_HOURS = 2.0


def parse_date(date_str):
    """解析日期字符串，支持多种格式。"""
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%m-%d-%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"无法解析日期: {date_str}。请使用 YYYY-MM-DD 格式。")


def load_topics(topics_file):
    """从 JSON 文件加载知识点。"""
    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    topics = []
    # 从 knowledge_points 和 raw_content 中提取主题
    if "knowledge_points" in data:
        for kp in data["knowledge_points"]:
            topics.append({
                "title": kp.get("title", "未命名"),
                "source": kp.get("source", "unknown"),
                "type": "知识点"
            })

    # 也从 raw_content 中提取章节标题
    if "raw_content" in data:
        for item in data["raw_content"]:
            if isinstance(item, dict) and item.get("title"):
                t = item["title"]
                # 过滤掉幻灯片/页面编号标题
                if not t.startswith("幻灯片") and not t.startswith("第 ") and t != "正文":
                    topics.append({
                        "title": t,
                        "source": item.get("source", "unknown"),
                        "type": "章节"
                    })

    # 去重
    seen = set()
    unique_topics = []
    for t in topics:
        if t["title"] not in seen:
            seen.add(t["title"])
            unique_topics.append(t)

    return unique_topics


def estimate_review_time(topic_title):
    """估算复习一个主题所需的时间（小时）。"""
    # 简单的启发式：标题越长可能内容越多
    length = len(topic_title)
    if length < 10:
        return 0.25
    elif length < 30:
        return 0.5
    else:
        return 0.75


def generate_schedule(topics, exam_date, start_date, intervals, daily_hours):
    """生成间隔重复复习日历。"""
    days_until_exam = (exam_date - start_date).days

    if days_until_exam < 1:
        print("[WARN] 考试日期已过或为今天，将生成紧急复习计划...")
        days_until_exam = 1

    schedule = {}  # date -> list of reviews

    # 为每个主题分配学习日（尽量均匀分布）
    total_topics = len(topics)
    if total_topics == 0:
        print("[WARN] 未找到任何知识点，请检查输入文件。")
        return schedule

    # 计算每天能学几个新主题
    topics_per_day = max(1, total_topics // max(1, days_until_exam - 2))  # 最后2天留给总复习
    topics_per_day = min(topics_per_day, max(1, int(daily_hours / 0.5)))  # 假设每个主题至少需要0.5小时

    # 分配新学习日
    topic_days = {}  # topic_index -> first_learn_date
    day_offset = 0
    for i, topic in enumerate(topics):
        learn_date = start_date + timedelta(days=min(day_offset, days_until_exam - 1))
        topic_days[i] = learn_date
        if (i + 1) % topics_per_day == 0:
            day_offset += 1

    # 为每个主题计算复习日期
    for i, topic in enumerate(topics):
        learn_date = topic_days[i]
        review_dates = []

        for interval in intervals:
            review_date = learn_date + timedelta(days=interval)
            if review_date <= exam_date:
                review_dates.append(review_date)

        # 记录新学
        if learn_date not in schedule:
            schedule[learn_date] = {"new": [], "review": []}
        schedule[learn_date]["new"].append({
            "title": topic["title"],
            "source": topic["source"],
            "type": topic["type"],
            "estimate_hours": estimate_review_time(topic["title"])
        })

        # 记录复习
        for rd in review_dates:
            if rd not in schedule:
                schedule[rd] = {"new": [], "review": []}
            schedule[rd]["review"].append({
                "title": topic["title"],
                "round": intervals.index((rd - learn_date).days) + 1 if (rd - learn_date).days in intervals else "?",
                "estimate_hours": estimate_review_time(topic["title"]) * 0.5  # 复习时间约为新学的一半
            })

    return schedule


def format_schedule_md(schedule, exam_date, start_date):
    """将复习日历格式化为 Markdown。"""
    lines = []
    lines.append("# 📅 间隔重复复习日历")
    lines.append("")
    lines.append(f"> **考试日期**: {exam_date.strftime('%Y-%m-%d')}")
    lines.append(f"> **计划开始**: {start_date.strftime('%Y-%m-%d')}")
    lines.append(f"> **剩余天数**: {(exam_date - start_date).days} 天")
    lines.append(f"> **生成日期**: {date.today().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 按日期排序
    sorted_dates = sorted(schedule.keys())
    total_estimated_hours = 0

    for d in sorted_dates:
        day_data = schedule[d]
        day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()]
        days_left = (exam_date - d).days

        lines.append(f"## {d.strftime('%Y-%m-%d')} ({day_name}) — 距考试 {days_left} 天")
        lines.append("")

        day_hours = 0

        if day_data["new"]:
            lines.append("### 🆕 新学内容")
            lines.append("")
            lines.append("| 主题 | 来源 | 类型 | 预估耗时 |")
            lines.append("|------|------|------|---------|")
            for item in day_data["new"]:
                h = item["estimate_hours"]
                day_hours += h
                lines.append(f"| {item['title']} | {item['source']} | {item['type']} | {h:.1f}h |")
            lines.append("")

        if day_data["review"]:
            lines.append("### 🔄 复习内容")
            lines.append("")
            lines.append("| 主题 | 复习轮次 | 预估耗时 |")
            lines.append("|------|---------|---------|")
            for item in day_data["review"]:
                h = item["estimate_hours"]
                day_hours += h
                lines.append(f"| {item['title']} | 第{item['round']}轮 | {h:.1f}h |")
            lines.append("")

        lines.append(f"> 📊 本日预估总耗时: **{day_hours:.1f} 小时**")
        lines.append("")
        total_estimated_hours += day_hours

    lines.append("---")
    lines.append("")
    lines.append(f"## 📊 统计")
    lines.append("")
    total_items = sum(len(d["new"]) + len(d["review"]) for d in schedule.values())
    lines.append(f"- 总条目数: {total_items}")
    lines.append(f"- 预估总耗时: {total_estimated_hours:.1f} 小时")
    lines.append(f"- 日均耗时: {total_estimated_hours / max(1, len(sorted_dates)):.1f} 小时")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### 💡 使用建议")
    lines.append("")
    lines.append("1. 每天优先完成**新学内容**，再用剩余时间复习")
    lines.append("2. 复习时使用**主动回忆**：合上笔记尝试复述，而非重读")
    lines.append("3. 标记感到困难的主题，考前集中攻克")
    lines.append("4. 考前最后 2 天切换为**全真模拟 + 核心速记**模式")

    return "\n".join(lines)


def main():
    configure_utf8_output()

    parser = argparse.ArgumentParser(description="生成间隔重复复习日历")
    parser.add_argument("--topics", "-t", required=True, help="知识点 JSON 文件路径（由 extract_content.py 生成）")
    parser.add_argument("--exam-date", "-e", required=True, help="考试日期 (YYYY-MM-DD)")
    parser.add_argument("--start-date", "-s", default=None, help="开始复习日期，默认为今天 (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", default="40_间隔复习计划.md", help="输出 Markdown 文件路径")
    parser.add_argument("--intervals", "-i", nargs="+", type=int,
                        default=DEFAULT_INTERVALS,
                        help=f"复习间隔天数 (默认: {' '.join(map(str, DEFAULT_INTERVALS))})")
    parser.add_argument("--daily-hours", "-d", type=float, default=DEFAULT_DAILY_HOURS,
                        help=f"每日可用复习时间（小时，默认: {DEFAULT_DAILY_HOURS}）")
    args = parser.parse_args()

    # 解析日期
    try:
        exam_date = parse_date(args.exam_date)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)

    if args.start_date:
        try:
            start_date = parse_date(args.start_date)
        except ValueError as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        start_date = date.today()

    if start_date > exam_date:
        print("[WARN] 开始日期晚于考试日期！将使用今天作为开始日期。")
        start_date = date.today()

    # 加载知识点
    topics = load_topics(args.topics)

    if not topics:
        print("错误: 未找到任何知识点。请先运行 extract_content.py 生成材料文件。")
        sys.exit(1)

    print(f"已加载 {len(topics)} 个知识点/章节")
    print(f"考试日期: {exam_date}")
    print(f"开始日期: {start_date}")
    print(f"复习间隔: {args.intervals}")
    print(f"每日时间: {args.daily_hours}h")

    # 生成日历
    schedule = generate_schedule(topics, exam_date, start_date, args.intervals, args.daily_hours)

    # 格式化为 Markdown
    md_content = format_schedule_md(schedule, exam_date, start_date)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n[OK] 复习日历已生成: {args.output}")
    print(f"   - 涵盖 {len(schedule)} 天")
    print(f"   - 总条目: {sum(len(d['new']) + len(d['review']) for d in schedule.values())}")


if __name__ == "__main__":
    main()
