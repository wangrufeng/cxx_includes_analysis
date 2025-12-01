"""
DOT 格式可视化器：生成 Graphviz DOT 文件
"""
import os
import re
from collections import defaultdict
from .utils import (
    get_file_size, format_size, get_node_color,
    simplify_path, get_directory_cluster
)


class DotVisualizer:
    """DOT 格式可视化器"""
    
    def __init__(self, nodes, edges, source_file):
        """
        初始化可视化器
        
        Args:
            nodes: 文件节点集合
            edges: 依赖关系边列表
            source_file: 源文件路径
        """
        self.nodes = nodes
        self.edges = edges
        self.source_file = os.path.abspath(source_file)
    
    def generate(self, output_file):
        """
        生成 DOT 文件
        
        Args:
            output_file: 输出文件路径
        """
        with open(output_file, "w") as f:
            f.write("digraph Dependencies {\n")
            f.write("  rankdir=LR;\n")  # Left to Right layout
            f.write("  node [shape=box, style=\"filled,rounded\", fontname=\"Helvetica\"];\n")
            f.write("  edge [color=\"#55555533\", arrowsize=0.5, weight=1];\n")
            f.write("  compound=true;\n")  # Allow edges between clusters
            f.write("  concentrate=true;\n")  # Merge multiple edges
            
            # 按目录分组节点
            clusters = defaultdict(list)
            cluster_edges = set()

            for node in self.nodes:
                cluster_name = get_directory_cluster(node)
                clusters[cluster_name].append(node)

            # 识别跨集群的边
            for src, dst in self.edges:
                src_cluster = get_directory_cluster(src)
                dst_cluster = get_directory_cluster(dst)
                if src_cluster != dst_cluster:
                    cluster_edges.add((src_cluster, dst_cluster))

            # 绘制集群
            self._draw_clusters(f, clusters)
            
            # 绘制边
            self._draw_edges(f)
                
            f.write("}\n")
    
    def _draw_clusters(self, f, clusters):
        """绘制集群（分组）"""
        cluster_id = 0
        cluster_map = {}

        for cluster_name, file_paths in clusters.items():
            safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', cluster_name)
            cluster_graph_id = f"cluster_{cluster_id}"
            cluster_map[cluster_name] = cluster_graph_id
            
            f.write(f"\n  subgraph {cluster_graph_id} {{\n")
            f.write(f"    label=\"{cluster_name}\";\n")
            f.write("    style=filled;\n")
            f.write("    color=lightgrey;\n")
            f.write("    fillcolor=\"#f5f5f5\";\n")
            
            for path in file_paths:
                size = get_file_size(path)
                color = get_node_color(size)
                
                # 创建标签：文件名 + 大小
                filename = os.path.basename(path)
                label = f"{filename}\\n({format_size(size)})"
                
                # DOT 中的节点 ID
                node_id = simplify_path(path)
                
                # 源文件特殊高亮
                penwidth = "3.0" if path == self.source_file else "1.0"
                
                f.write(f"    \"{node_id}\" [label=\"{label}\", fillcolor=\"{color}\", penwidth={penwidth}];\n")
            
            f.write("  }\n")
            cluster_id += 1
    
    def _draw_edges(self, f):
        """绘制边（依赖关系）"""
        f.write("\n  # Edges\n")
        
        # 按目标文件大小排序：小文件先画（背景），大文件后画（前景）
        edges_list = list(self.edges)
        edges_list.sort(key=lambda x: get_file_size(x[1]))

        for src, dst in edges_list:
            src_id = simplify_path(src)
            dst_id = simplify_path(dst)
            
            # 计算边的样式
            dst_size = get_file_size(dst)
            edge_style = ""
            weight = 1
            
            # 高亮大文件依赖
            if dst_size > 200 * 1024:
                edge_style = " [color=\"#B71C1C\", penwidth=2.5]"
                weight = 5
            elif dst_size > 50 * 1024:
                edge_style = " [color=\"#EF9A9A\", penwidth=1.5]"
                weight = 3
            
            # 高亮跨模块依赖
            src_cluster = get_directory_cluster(src)
            dst_cluster = get_directory_cluster(dst)
            
            if src_cluster != dst_cluster:
                if not edge_style:  # 如果还没有被大小高亮
                    edge_style = " [color=\"#1E88E5\", penwidth=1.2]"  # 蓝色表示跨模块
                    weight = 2
            
            # 添加权重到样式字符串
            if edge_style:
                edge_style = edge_style[:-1] + f", weight={weight}]"
            else:
                edge_style = f" [weight={weight}]"

            f.write(f"  \"{src_id}\" -> \"{dst_id}\"{edge_style};\n")

