# Cram Course

[GitHub](https://github.com/WXK2905821189/cram-course-skill-)

大学期末考试突击学习 skill。它把课程课件转成一套可执行的冲刺资料：预测试、学习计划、逐章笔记、逐章题库、跨章专项训练、错题本、间隔重复日历和考前模拟卷。

> 适合场景：距离期末考试只剩几天，需要把 PPTX/PDF/DOCX 课件快速整理成能学、能背、能刷题的材料。

## 能生成什么

- `00_课程导学.md`：课程地图、熟悉度标记和导学问题
- `01_学习计划.md`：按剩余天数和每日时间生成的学习计划
- `02_覆盖矩阵.md`：逐页/逐节覆盖矩阵，检查是否漏掉课件内容
- `10_第01章_<章节名>_01学习笔记.md`：逐章笔记
- `10_第01章_<章节名>_02章节题库.md`：逐章题库
- `30_名词解释专项.md`：名词解释专项
- `31_公式计算专项.md`：公式计算专项
- `32_对比辨析专项.md`：对比辨析专项
- `33_简答论述专项.md`：简答论述专项
- `34_综合应用专项.md`：综合应用专项
- `40_间隔复习计划.md`：间隔重复复习日历
- `41_错题本.md`：错题分类追踪
- `50_模拟考试.md`：考前模拟卷

## 仓库结构

```text
.
├── cram-course/              # 真正的 skill 包，复制这个目录即可安装
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
├── examples/                 # 示例输入/输出，含 full-demo
├── tests/                    # 基础脚本测试
├── dist/                     # 已打包的 .skill 分发文件
├── manifest.json             # 发布元信息
├── requirements.txt
├── LICENSE
└── README.md
```

## 安装

1. 安装 Python 依赖：

```bash
python -m pip install -r requirements.txt
```

2. 将 `cram-course/` 目录复制到你的 AI 客户端 skills 目录。Codex 默认通常是：

```bash
cp -R cram-course "$HOME/.codex/skills/"
```

Windows Git Bash 示例：

```bash
cp -R cram-course "C:/Users/<你的用户名>/.codex/skills/"
```

如果 Windows 终端里中文输出乱码，可在运行脚本前设置：

```bash
export PYTHONUTF8=1
```

## 使用方式

先把课件解析成结构化 JSON：

```bash
cd cram-course
python scripts/extract_content.py "path/to/course.pptx" "path/to/notes.pdf" --output study_materials.json
```

再生成间隔重复复习日历：

```bash
python scripts/spaced_repetition.py --topics study_materials.json --exam-date "2026-06-28" --output "40_间隔复习计划.md"
```

然后在 Codex/Claude 中请求：

```text
使用 cram-course，帮我根据这些课件生成期末突击学习资料。考试日期是 2026-06-28，每天能学 4 小时。
```

## 支持的材料

- 推荐：`.pptx`、`.docx`、带文本层的 `.pdf`
- 暂不直接支持：旧版 `.ppt`，请先转换为 `.pptx`
- 扫描版 PDF：请先用 OCR 转成可复制文本的 PDF 或 DOCX

## 学习方法

这个 skill 不是简单总结课件，而是按学习科学组织冲刺流程：

- 资料诊断：先判断课件是否足够、是否扫描版、是否需要补材料
- 学科模式：按计算、论述、案例、记忆等课程类型调整题型比例
- 覆盖矩阵：逐 slide/page/section 对齐笔记和题目，防止漏知识点
- 课程导学：先看课程地图和导学问题，不要求零基础学生一开始答对题
- 主动回忆：合上笔记自测，而不是反复重读
- 生成效应：用自由回忆、变式题和简答题训练输出能力
- 间隔重复：按 1、3、7、14 天安排复习
- 元认知校准：每道题记录信心评分，找出“以为会了但其实不会”的内容

## 注意事项

- 不要把受版权保护的课程课件上传到公开仓库。
- AI 生成的考点和题目需要人工复核，不能保证完全等同于老师命题。
- 如果课件内容过少，建议补充教材、习题、课堂笔记或考试范围。
- 如果通过在线 AI 服务处理课件，课件内容可能会发送到对应服务商，请先确认隐私要求。

## 示例

- `examples/sample_study_materials.json`：最小结构化输入示例
- `examples/示例_40_间隔复习计划.md`：间隔重复脚本输出示例
- `examples/full-demo/`：一个迷你数据结构课程的完整输出形态示例

## 开发验证

```bash
python -m unittest discover -s tests
python cram-course/scripts/spaced_repetition.py --topics examples/sample_study_materials.json --exam-date "2026-07-15" --start-date "2026-07-08" --output "examples/示例_40_间隔复习计划.md"
```

## License

MIT License. See `LICENSE`.

## 发布前清单

- 在 README 顶部补充 GitHub 仓库地址。
- 使用一份不含版权风险的示例课件生成完整 demo。
- 确认 `cram-course/SKILL.md` 的描述能被目标客户端正确触发。
