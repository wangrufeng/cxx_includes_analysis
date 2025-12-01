"""
配置文件：包含默认路径和正则表达式
"""
import re

# 默认的 include 搜索路径
DEFAULT_INCLUDE_PATHS = [
    ".",
    "build64_release",
    "/usr/include",
    "/usr/local/include",
    "/usr/lib/gcc/x86_64-redhat-linux/8/include",
    "/usr/include/c++/8",
    "/usr/include/c++/8/x86_64-redhat-linux",
]

# 匹配 #include 语句的正则表达式
INCLUDE_PATTERN = re.compile(r'^\s*#\s*include\s+(["<])([^">]+)[">]')

# 第三方库识别配置
THIRD_PARTY_LIBS = {
    'boost': 'Boost',
    'absl': 'Abseil',
    'brpc': 'bRPC',
    'bthread': 'bThread',
    'butil': 'bUtil',
    'gflags': 'gflags',
    'glog': 'glog',
    'google/protobuf': 'Protobuf',
    'tbb': 'TBB',
    'mysql++': 'MySQL++',
    'rapidjson': 'RapidJSON',
}

# 文件大小颜色映射（用于可视化）
SIZE_COLOR_MAP = [
    (10 * 1024, "#E8F5E9"),   # < 10KB: 绿色（轻量）
    (50 * 1024, "#FFF9C4"),   # < 50KB: 黄色（中等）
    (200 * 1024, "#FFCC80"),  # < 200KB: 橙色（较大）
    (float('inf'), "#EF9A9A"), # > 200KB: 红色（巨大）
]

