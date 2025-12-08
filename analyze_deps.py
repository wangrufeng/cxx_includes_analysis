#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blade 依赖关系分析工具

分析 Blade 构建系统中 target 的依赖关系，并生成可视化图表。
支持生成交互式 HTML 格式。
"""
import sys
import os
import argparse

# 设置默认编码为 UTF-8
if sys.version_info[0] >= 3:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加库路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyze_includes_lib.blade_parser import BladeParser, find_blade_root
from analyze_includes_lib.blade_visualizer import BladeHtmlVisualizer


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="分析 Blade 构建系统的 target 依赖关系并生成可视化图表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 分析指定 target 的依赖关系
  %(prog)s ads/serving/show:brpc_ranking_server
  
  # 指定 BLADE_ROOT 目录
  %(prog)s ads/serving/show:brpc_ranking_server --blade-root /path/to/project
  
  # 自定义输出文件名
  %(prog)s ads/serving/show:brpc_ranking_server -o server_deps.html
  
  # 设置最大递归深度
  %(prog)s ads/serving/show:brpc_ranking_server --depth 5

说明:
  target 规范格式为：path/to/dir:target_name
  例如：ads/serving/show:brpc_ranking_server
  
  工具会从 BLADE_ROOT 目录开始，查找 ads/serving/show/BUILD 文件，
  然后分析名为 brpc_ranking_server 的 target 及其所有依赖。
        """
    )
    
    parser.add_argument(
        "target",
        help="要分析的 target 规范（格式：path/to/dir:target_name）"
    )
    
    parser.add_argument(
        "--blade-root",
        help="BLADE_ROOT 文件所在的项目根目录（默认：自动查找）"
    )
    
    parser.add_argument(
        "--depth",
        type=int,
        default=10,
        help="最大递归深度（默认：10）"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出文件名（默认：blade_dependency_graph.html）"
    )
    
    args = parser.parse_args()
    
    # 查找 BLADE_ROOT
    if args.blade_root:
        blade_root = args.blade_root
    else:
        blade_root = find_blade_root()
        if not blade_root:
            print("✗ 错误：找不到 BLADE_ROOT 文件。")
            print("  请在 Blade 项目目录中运行此工具，或使用 --blade-root 参数指定项目根目录。")
            sys.exit(1)
    
    if not os.path.exists(blade_root):
        print(f"✗ 错误：指定的 BLADE_ROOT 目录不存在：{blade_root}")
        sys.exit(1)
    
    print(f"BLADE_ROOT: {blade_root}")
    print(f"分析 Target: {args.target}")
    print(f"最大深度: {args.depth}")
    print()
    
    # 创建解析器
    blade_parser = BladeParser(blade_root)
    
    # 分析依赖关系
    print("正在分析依赖关系...")
    try:
        nodes, edges = blade_parser.analyze_dependencies(args.target, max_depth=args.depth)
    except Exception as e:
        print(f"✗ 错误：分析依赖关系时出错：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if not nodes:
        print(f"✗ 错误：找不到 target {args.target} 或其没有依赖。")
        sys.exit(1)
    
    print(f"✓ 发现 {len(nodes)} 个 target 和 {len(edges)} 个依赖关系")
    print()
    
    # 统计信息
    target_types = {}
    external_count = 0
    for target_spec, target_info in nodes.items():
        target_type = target_info.get('type', 'unknown')
        target_types[target_type] = target_types.get(target_type, 0) + 1
        if target_info.get('external'):
            external_count += 1
    
    print("Target 类型统计：")
    for target_type, count in sorted(target_types.items()):
        print(f"  {target_type}: {count}")
    print(f"  外部依赖: {external_count}")
    print()
    
    # 生成 HTML 文件
    html_file = args.output if args.output else "blade_dependency_graph.html"
    
    print(f"正在生成交互式 HTML：{html_file}...")
    
    try:
        visualizer = BladeHtmlVisualizer(nodes, edges, args.target)
        visualizer.generate(html_file)
    except Exception as e:
        print(f"✗ 错误：生成 HTML 文件时出错：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print(f"✓ 交互式 HTML 已生成：{html_file}")
    print()
    print("功能说明：")
    print("  • 点击节点查看依赖关系（红色=依赖的 target，绿色=被依赖的 target）")
    print("  • 拖拽节点调整位置")
    print("  • 使用搜索框过滤 target")
    print("  • 鼠标滚轮缩放，拖拽画布移动")
    print("  • 切换树状布局和力导向布局")
    print("  • 点击左上角按钮收起/展开控制面板")
    print()
    print(f"请在浏览器中打开 {html_file} 查看可视化结果")


if __name__ == "__main__":
    main()

