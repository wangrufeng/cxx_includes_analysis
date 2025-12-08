"""
Blade BUILD 文件解析器：解析 Blade 构建系统的 BUILD 文件
"""
import os
import re
from collections import defaultdict


class BladeParser:
    """Blade BUILD 文件解析器"""
    
    def __init__(self, blade_root):
        """
        初始化解析器
        
        Args:
            blade_root: BLADE_ROOT 文件所在的项目根目录
        """
        self.blade_root = os.path.abspath(blade_root)
        self.targets = {}  # 存储所有解析的 target: {name: target_info}
        
    def parse_target_path(self, target_spec):
        """
        解析 target 路径规范
        
        Args:
            target_spec: target 规范，如 "ads/serving/show:brpc_ranking_server"
            
        Returns:
            (build_dir, target_name) 元组
            - build_dir: BUILD 文件所在目录的绝对路径
            - target_name: target 名称
        """
        if ':' not in target_spec:
            raise ValueError(f"无效的 target 规范：{target_spec}，应该是 'path/to/dir:target_name' 格式")
        
        path_part, target_name = target_spec.split(':', 1)
        
        # 移除开头的 '//' 如果有
        if path_part.startswith('//'):
            path_part = path_part[2:]
        
        build_dir = os.path.join(self.blade_root, path_part)
        
        return build_dir, target_name
    
    def find_build_file(self, directory):
        """
        在指定目录查找 BUILD 文件
        
        Args:
            directory: 目录路径
            
        Returns:
            BUILD 文件的完整路径，如果找不到返回 None
        """
        build_file = os.path.join(directory, 'BUILD')
        if os.path.exists(build_file):
            return build_file
        return None
    
    def parse_build_file(self, build_file):
        """
        解析 BUILD 文件，提取所有 target 定义
        
        Args:
            build_file: BUILD 文件路径
            
        Returns:
            字典，key 为 target 名称，value 为 target 信息
        """
        targets = {}
        
        try:
            with open(build_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 创建一个安全的执行环境
            # 定义 Blade 的构建函数
            def capture_target(target_type):
                """创建一个捕获 target 信息的函数"""
                def target_func(name, **kwargs):
                    targets[name] = {
                        'type': target_type,
                        'name': name,
                        'deps': kwargs.get('deps', []),
                        'srcs': kwargs.get('srcs', []),
                        'hdrs': kwargs.get('hdrs', []),
                        'build_file': build_file,
                        'directory': os.path.dirname(build_file)
                    }
                return target_func
            
            # 创建执行环境，包含所有 Blade 构建函数
            exec_env = {
                'cc_library': capture_target('cc_library'),
                'cc_binary': capture_target('cc_binary'),
                'cc_test': capture_target('cc_test'),
                'proto_library': capture_target('proto_library'),
                'cc_plugin': capture_target('cc_plugin'),
                'lex_yacc_library': capture_target('lex_yacc_library'),
                'resource_library': capture_target('resource_library'),
                'swig_library': capture_target('swig_library'),
                'gen_rule': capture_target('gen_rule'),
                'foreign_cc_library': capture_target('foreign_cc_library'),
                # 可以根据需要添加更多 target 类型
            }
            
            # 执行 BUILD 文件内容
            exec(content, exec_env)
            
        except Exception as e:
            print(f"⚠ 警告：解析 BUILD 文件 {build_file} 时出错：{e}")
            return {}
        
        return targets
    
    def resolve_dep_path(self, dep, current_dir):
        """
        解析依赖路径为完整的 target 规范
        
        Args:
            dep: 依赖字符串，如 ':cpc_util', '//ads/proto:ranking_cpc_proto', '#glog'
            current_dir: 当前 BUILD 文件所在目录
            
        Returns:
            完整的 target 规范，如果是外部依赖返回原字符串
        """
        # 外部依赖（以 # 开头）
        if dep.startswith('#'):
            return dep
        
        # 相对依赖（以 : 开头）
        if dep.startswith(':'):
            rel_path = os.path.relpath(current_dir, self.blade_root)
            return f"{rel_path}:{dep[1:]}"
        
        # 绝对依赖（以 // 开头）
        if dep.startswith('//'):
            return dep[2:]
        
        # 其他形式的依赖
        return dep
    
    def get_target_info(self, target_spec):
        """
        获取指定 target 的信息
        
        Args:
            target_spec: target 规范
            
        Returns:
            target 信息字典，如果找不到返回 None
        """
        # 如果是外部依赖，返回简化信息
        if target_spec.startswith('#'):
            return {
                'type': 'external',
                'name': target_spec[1:],
                'deps': [],
                'external': True
            }
        
        # 解析 target 路径
        try:
            build_dir, target_name = self.parse_target_path(target_spec)
        except ValueError:
            return None
        
        # 查找 BUILD 文件
        build_file = self.find_build_file(build_dir)
        if not build_file:
            return None
        
        # 解析 BUILD 文件（如果还没解析过）
        if build_file not in self.targets:
            self.targets[build_file] = self.parse_build_file(build_file)
        
        # 获取 target 信息
        targets = self.targets.get(build_file, {})
        target_info = targets.get(target_name)
        
        if target_info:
            # 解析依赖路径
            resolved_deps = []
            for dep in target_info.get('deps', []):
                resolved_dep = self.resolve_dep_path(dep, build_dir)
                resolved_deps.append(resolved_dep)
            
            target_info['resolved_deps'] = resolved_deps
            target_info['full_spec'] = target_spec
        
        return target_info
    
    def analyze_dependencies(self, target_spec, max_depth=10):
        """
        分析指定 target 的依赖关系
        
        Args:
            target_spec: target 规范
            max_depth: 最大递归深度
            
        Returns:
            (nodes, edges) 元组
            - nodes: 所有 target 节点的集合（包含 target 信息）
            - edges: 依赖关系边的列表 [(src_spec, dst_spec), ...]
        """
        queue = [(target_spec, 0)]
        visited = set()
        edges = []
        nodes = {}  # target_spec -> target_info
        
        while queue:
            current_spec, depth = queue.pop(0)
            
            if current_spec in visited:
                continue
            visited.add(current_spec)
            
            # 获取 target 信息
            target_info = self.get_target_info(current_spec)
            if not target_info:
                print(f"⚠ 警告：找不到 target {current_spec}")
                continue
            
            nodes[current_spec] = target_info
            
            if depth >= max_depth:
                continue
            
            # 处理依赖
            for dep in target_info.get('resolved_deps', []):
                edges.append((current_spec, dep))
                
                if dep not in visited:
                    queue.append((dep, depth + 1))
        
        return nodes, edges


def find_blade_root(start_path=None):
    """
    查找 BLADE_ROOT 文件所在的项目根目录
    
    Args:
        start_path: 开始搜索的路径，默认为当前目录
        
    Returns:
        BLADE_ROOT 所在目录的绝对路径，如果找不到返回 None
    """
    if start_path is None:
        start_path = os.getcwd()
    
    current = os.path.abspath(start_path)
    
    while True:
        blade_root_file = os.path.join(current, 'BLADE_ROOT')
        if os.path.exists(blade_root_file):
            return current
        
        parent = os.path.dirname(current)
        if parent == current:  # 到达根目录
            break
        current = parent
    
    return None

