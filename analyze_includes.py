#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C++ 依赖关系分析工具 - 模块化版本

分析 C++ 源文件的 #include 依赖关系，并生成可视化图表。
支持生成 Graphviz DOT 格式和交互式 HTML 格式。
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

from analyze_includes_lib import (
    DEFAULT_INCLUDE_PATHS,
    DependencyAnalyzer,
    DotVisualizer,
    HtmlVisualizer
)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="分析 C++ 头文件依赖关系并生成可视化图表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 分析单个文件
  %(prog)s src/main.cpp
  
  # 批量分析多个模块
  %(prog)s file1.cpp file2.cpp file3.cpp -o deps.html
  
  # 添加自定义 include 路径
  %(prog)s src/main.cpp -I ./include -I ./third_party
  
  # 生成 DOT 格式
  %(prog)s src/main.cpp --format dot
  
  # 同时生成 HTML 和 DOT
  %(prog)s src/main.cpp --format both
        """
    )
    
    parser.add_argument(
        "source_files",
        nargs='+',
        help="要分析的 C++ 源文件（支持多个）"
    )
    
    parser.add_argument(
        "-I", "--include",
        action="append",
        help="添加 include 搜索路径（可多次使用）"
    )
    
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="最大递归深度（默认：3）"
    )
    
    parser.add_argument(
        "--deep-system",
        action="store_true",
        help="深度扫描系统头文件（默认：False）"
    )
    
    parser.add_argument(
        "--format",
        choices=['dot', 'html', 'both'],
        default='html',
        help="输出格式：dot (Graphviz), html (交互式 D3.js), both（默认：html）"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出文件名（默认：dependency_graph.html 或 dependencies.dot）"
    )
    
    args = parser.parse_args()
    
    # 准备 include 路径
    include_paths = list(DEFAULT_INCLUDE_PATHS)
    if args.include:
        include_paths.extend(args.include)
    
    # 创建分析器
    analyzer = DependencyAnalyzer(
        include_paths=include_paths,
        max_depth=args.depth,
        deep_system=args.deep_system
    )
    
    # 分析所有源文件
    print(f"开始分析 {len(args.source_files)} 个源文件...")
    print(f"配置：深度={args.depth}, 深度扫描系统头文件={args.deep_system}")
    print()
    
    modules_data = []
    for source_file in args.source_files:
        if not os.path.exists(source_file):
            print(f"⚠ 警告：文件 {source_file} 不存在，跳过。")
            continue
        
        print(f"正在分析：{source_file}")
        nodes, edges = analyzer.analyze(source_file)
        print(f"  ✓ 发现 {len(nodes)} 个文件和 {len(edges)} 个依赖关系")
        
        modules_data.append({
            'source_file': source_file,
            'nodes': nodes,
            'edges': edges
        })
    
    if not modules_data:
        print("\n✗ 错误：没有有效的源文件可分析。")
        sys.exit(1)
    
    print(f"\n总共成功分析了 {len(modules_data)} 个模块。")
    print()
    
    # 生成 DOT 文件（如果需要）
    if args.format in ['dot', 'both'] and modules_data:
        module = modules_data[0]
        dot_file = args.output if args.output and args.format == 'dot' else "dependencies.dot"
        
        print(f"正在生成 DOT 文件：{dot_file}（仅第一个模块）...")
        
        visualizer = DotVisualizer(
            nodes=module['nodes'],
            edges=module['edges'],
            source_file=module['source_file']
        )
        visualizer.generate(dot_file)
        
        print(f"✓ DOT 文件已生成：{dot_file}")
        print(f"  运行 'dot -Tpng {dot_file} -o dependency_graph.png' 生成 PNG 图片")
        print(f"  或运行 'dot -Tsvg {dot_file} -o dependency_graph.svg' 生成 SVG 图片")
        print()
    
    # 生成 HTML 文件（如果需要）
    if args.format in ['html', 'both']:
        html_file = args.output if args.output and args.format == 'html' else "dependency_graph.html"
        
        print(f"正在生成交互式 HTML：{html_file}...")
        
        visualizer = HtmlVisualizer(modules_data)
        visualizer.generate(html_file)
        
        print(f"✓ 交互式 HTML 已生成：{html_file}")
        print()
        print("功能说明：")
        print("  • 点击节点查看依赖关系（红色=依赖的文件，绿色=被依赖的文件）")
        print("  • 使用 Previous/Next 按钮或左右方向键切换模块")
        print("  • 拖拽节点调整位置")
        print("  • 使用搜索框过滤文件")
        print("  • 鼠标滚轮缩放，拖拽画布移动")
        print("  • 切换树状布局和力导向布局")
        print()
        print(f"请在浏览器中打开 {html_file} 查看可视化结果")


if __name__ == "__main__":
    main()

