"""
依赖分析器：负责解析C++文件的依赖关系
"""
import os
from .config import INCLUDE_PATTERN


class DependencyAnalyzer:
    """C++ 依赖关系分析器"""
    
    def __init__(self, include_paths, max_depth=3, deep_system=False):
        """
        初始化分析器
        
        Args:
            include_paths: include 搜索路径列表
            max_depth: 最大递归深度
            deep_system: 是否深度扫描系统头文件
        """
        self.include_paths = include_paths
        self.max_depth = max_depth
        self.deep_system = deep_system
    
    def find_file(self, filename, is_system, current_dir):
        """
        查找头文件的完整路径
        
        Args:
            filename: 头文件名
            is_system: 是否为系统头文件（<> 包含）
            current_dir: 当前文件所在目录
            
        Returns:
            文件的绝对路径，如果找不到返回 None
        """
        # 如果是引号包含，先在当前目录查找
        if not is_system:
            candidate = os.path.join(current_dir, filename)
            if os.path.exists(candidate):
                return os.path.abspath(candidate)
        
        # 在 include 路径中查找
        for path in self.include_paths:
            candidate = os.path.join(path, filename)
            if os.path.exists(candidate):
                return os.path.abspath(candidate)
                
        return None
    
    def analyze(self, start_file):
        """
        分析指定文件的依赖关系
        
        Args:
            start_file: 要分析的源文件路径
            
        Returns:
            (nodes, edges) 元组
            - nodes: 所有文件节点的集合
            - edges: 依赖关系边的列表 [(src, dst), ...]
        """
        queue = [(os.path.abspath(start_file), 0)]
        visited = set()
        edges = []
        nodes = set()
        
        while queue:
            current_path, depth = queue.pop(0)
            
            if current_path in visited:
                continue
            visited.add(current_path)
            nodes.add(current_path)

            if depth >= self.max_depth:
                continue

            # 除非明确要求，否则不扫描系统头文件
            is_system_header = current_path.startswith("/usr/")
            if is_system_header and not self.deep_system:
                continue

            current_dir = os.path.dirname(current_path)
            
            # 解析文件中的 #include 语句
            try:
                with open(current_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        match = INCLUDE_PATTERN.match(line)
                        if match:
                            is_quote = (match.group(1) == '"')
                            inc_file = match.group(2)
                            
                            full_path = self.find_file(inc_file, not is_quote, current_dir)
                            
                            if full_path:
                                edges.append((current_path, full_path))
                                nodes.add(full_path)
                                
                                if full_path not in visited:
                                    queue.append((full_path, depth + 1))
                                    
            except Exception as e:
                # 忽略无法读取的文件
                pass

        return nodes, edges

