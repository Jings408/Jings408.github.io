# 镇定学习工具箱文档站

这是一个自包含的静态文档站，介绍 `stabilization-learning` 的架构、环境、算法、用法和扩展方式。

## 打开方式

直接双击 `index.html`，或在项目根目录运行：

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/website/
```

站点没有构建步骤，也没有外部 CDN 依赖；`assets/mathjax/tex-svg.js` 是本地 MathJax，离线也能渲染公式。

## 文件

| 文件 | 作用 |
|---|---|
| `index.html` | 全部文档内容（单页 + 侧边栏锚点） |
| `styles.css` | 版式、深浅色、响应式、代码块、表格 |
| `app.js` | 主题切换、移动端目录、复制按钮、目录高亮、进度条 |
| `assets/mathjax/tex-svg.js` | 本地 MathJax 3（SVG 输出） |
| `assets/figures/*.svg` | 由运行数据重绘的训练曲线（矢量） |
| `assets/tasks/*.svg` | 任务示意图标 |
| `assets/diagrams/architecture.svg` | 五面板架构总览（Env / Algo / Runner / RGB / Push-SO101） |
| `assets/media/*.mp4` | SO101 任务片段与双积分器示意动画 |
| `scripts/make_media.py` | 生成训练曲线和双积分器动画 |
| `scripts/make_task_icons.py` | 生成任务示意图标 |
| `scripts/make_architecture_svg.py` | 生成五面板架构图 |

## 内容结构

- 概览：工具箱定位、Env/Algo/Runner、共同数学对象
- 架构：三层职责与代码位置
- 环境：9 个注册环境 + 专用任务
- 算法：6 个统一后端 + 专用/模型型算法 + RGB 变体
- 使用：安装、快速开始、Python API、统一 v4、配置
- 任务配方：状态控制、观测器、机器人、Push/SO101、RGB、Scratch、VIP/DINOv2
- 任务示意图：10 个任务图标与对应配方
- 训练效果、训练曲线、任务动画、输出结构
- 扩展：新任务、GMM-D、L 学习
- 命令参考、常见问题、延伸阅读

## 重新生成媒体

```bash
/home/ajingshou/anaconda3/envs/drones/bin/python scripts/make_media.py
/home/ajingshou/anaconda3/envs/drones/bin/python scripts/make_task_icons.py
/home/ajingshou/anaconda3/envs/drones/bin/python scripts/make_architecture_svg.py
```

`make_media.py` 从以下目录读取数据：

- `runs/non_rgb_overnight_20261101_HIhnEVgJ/book_disk/`
- `runs/non_rgb_overnight_20261101_HIhnEVgJ/book_grid/`
- `runs/rgb_representation_v2_20261030_z9RNX5Ou/figures_01/`

`so101_push.mp4` 是从 `runs/non_rgb_overnight_20261101_HIhnEVgJ/push_so101/arm/episodes/selected/T/000/episode.mp4` 复制的运行片段；`point_mass.mp4` 是脚本生成的 PD 控制示意动画。

## 修改

- 内容都在 `index.html`，按 `<section id="...">` 组织；侧边栏链接与 section id 对应。
- 颜色、字体、间距在 `styles.css` 顶部的 CSS 变量里改。
- 数学公式用 `\( ... \)` 和 `\[ ... \]`；MathJax 已跳过 `pre` / `code`，代码块里不会误渲染。
- 新增任务配方时，复制一个 `<details class="recipe" id="recipe-...">` 块，并在侧边栏加链接。

## 已验证

- 用 Chrome headless 渲染，`.math` 中的 **8** 个显示公式全部输出为 `mjx-container` SVG。
- 4 张训练曲线为矢量 SVG（含 Push PPO 的 step-vs-return 曲线），10 个任务示意图标、2 段 MP4 均可通过本地 HTTP 服务加载。
- MP4 播放检查：`readyState=4`、`paused=false`、无 `error`；SO101 1024×608，双积分器 960×540。
- 48 个锚点链接全部有对应目标；桌面 1440px、移动 420px 均无横向滚动。
- 深色/浅色主题、侧边栏目录、代码复制按钮均可切换。
