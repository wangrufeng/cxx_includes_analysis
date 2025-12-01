"""
HTML 可视化器：生成基于 D3.js 的交互式 HTML 依赖图
"""
import os
import json
from collections import defaultdict
from .utils import (
    get_file_size, simplify_path, get_directory_cluster
)
from .html_template import get_html_template


class HtmlVisualizer:
    """HTML 交互式可视化器"""
    
    def __init__(self, modules_data):
        """
        初始化可视化器
        
        Args:
            modules_data: 模块数据列表，每个元素是字典 {'source_file': str, 'nodes': set, 'edges': list}
        """
        self.modules_data = modules_data
    
    def generate(self, output_file):
        """
        生成交互式 HTML 文件
        
        Args:
            output_file: 输出文件路径
        """
        # 为每个模块准备数据
        all_modules_json = []
        
        for module_info in self.modules_data:
            module_json = self._prepare_module_data(module_info)
            all_modules_json.append(module_json)
        
        # 生成 HTML
        modules_json_str = json.dumps(all_modules_json, ensure_ascii=False)
        html_content = get_html_template(modules_json_str, len(all_modules_json))
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _prepare_module_data(self, module_info):
        """
        为单个模块准备 JSON 数据
        
        Args:
            module_info: 模块信息字典
            
        Returns:
            准备好的模块数据字典
        """
        source_file = module_info['source_file']
        nodes = module_info['nodes']
        edges = module_info['edges']
        
        # 准备节点数据并计算依赖层级
        nodes_data = []
        node_id_map = {}
        
        # 构建依赖图
        dependencies = defaultdict(list)  # node -> [依赖的节点]
        dependents = defaultdict(list)    # node -> [依赖它的节点]
        
        for src, dst in edges:
            src_id = simplify_path(src)
            dst_id = simplify_path(dst)
            dependencies[src_id].append(dst_id)
            dependents[dst_id].append(src_id)
        
        # 使用 BFS 计算每个节点的层级（从源文件开始）
        source_id = simplify_path(os.path.abspath(source_file))
        queue = [(source_id, 0)]
        visited_level = {source_id: 0}
        
        while queue:
            current, level = queue.pop(0)
            for dep in dependencies.get(current, []):
                if dep not in visited_level or visited_level[dep] > level + 1:
                    visited_level[dep] = level + 1
                    queue.append((dep, level + 1))
        
        # 为所有节点分配层级
        for node in nodes:
            node_id = simplify_path(node)
            node_id_map[node] = node_id
            # 如果节点没有被访问到，说明它不在依赖链中，放在最后
            level = visited_level.get(node_id, 999)
            
            cluster = get_directory_cluster(node)
            
            nodes_data.append({
                'id': node_id,
                'name': os.path.basename(node),
                'path': node,
                'size': get_file_size(node),
                'cluster': cluster,
                'is_source': node == os.path.abspath(source_file),
                'level': level,
                'dep_count': len(dependencies.get(node_id, [])),
                'dependent_count': len(dependents.get(node_id, []))
            })
        
        # 按层级和目录排序节点，让相同目录的节点相邻
        nodes_data.sort(key=lambda x: (x['level'], x['cluster'], x['name']))
        
        # 准备边数据
        edges_data = []
        for src, dst in edges:
            edges_data.append({
                'source': node_id_map.get(src, simplify_path(src)),
                'target': node_id_map.get(dst, simplify_path(dst)),
                'size': get_file_size(dst)
            })
        
        return {
            'source_file': os.path.basename(source_file),
            'source_path': source_file,
            'nodes': nodes_data,
            'links': edges_data,
            'node_count': len(nodes),
            'edge_count': len(edges)
        }

