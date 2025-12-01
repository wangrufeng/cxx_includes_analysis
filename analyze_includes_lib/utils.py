"""
工具函数：文件操作、路径处理、格式化等
"""
import os
from .config import SIZE_COLOR_MAP, THIRD_PARTY_LIBS


def get_file_size(path):
    """获取文件大小（字节）"""
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def format_size(size):
    """格式化文件大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}GB"


def get_node_color(size):
    """根据文件大小返回对应的颜色"""
    for threshold, color in SIZE_COLOR_MAP:
        if size < threshold:
            return color
    return SIZE_COLOR_MAP[-1][1]


def simplify_path(path):
    """简化路径：如果在当前工作目录下，返回相对路径"""
    cwd = os.getcwd()
    if path.startswith(cwd):
        return os.path.relpath(path, cwd)
    return path


def get_directory_cluster(path):
    """
    根据文件路径返回所属的集群（分组）名称
    
    分类优先级：
    1. 第三方库（Third-Party）
    2. 系统库（System）
    3. 生成的文件（Generated）
    4. 项目文件（Project）
    """
    directory = os.path.dirname(path)
    
    # 第三方库识别（优先级最高）
    for lib_path, lib_name in THIRD_PARTY_LIBS.items():
        if lib_path in directory:
            return f"Third-Party/{lib_name}"
    
    # 系统库识别（C/C++标准库和Linux系统库）
    if directory.startswith("/usr/include/c++") or directory.startswith("/usr/lib/gcc"):
        return "System/C++ Standard Library"
    elif directory.startswith("/usr/include"):
        return "System/Linux Headers"
    elif directory.startswith("/usr"):
        return "System/Other"
    
    # 生成的 Protobuf 文件
    if "build64_release" in directory:
        return "Generated/Proto Files"

    # 项目文件
    rel_dir = os.path.relpath(directory, os.getcwd())
    if rel_dir == ".":
        return "Project/Root"
    
    # 使用前2-3层目录进行分组，避免过多小分组
    parts = rel_dir.split(os.sep)
    if len(parts) > 3:
        return "Project/" + os.sep.join(parts[:3])
    return "Project/" + rel_dir


def get_cluster_priority(cluster_name):
    """
    返回集群的排序优先级
    
    优先级顺序：项目文件(0) -> 第三方库(1) -> 生成的Protobuf文件(2) -> 系统库(3)
    """
    if cluster_name.startswith("Project/"):
        return 0
    elif cluster_name.startswith("Third-Party/"):
        return 1
    elif cluster_name.startswith("Generated/"):
        return 2
    elif cluster_name.startswith("System/"):
        return 3
    else:
        return 4  # 未知类型放在最后

