"""
Blade 依赖可视化器：生成 Blade 依赖关系的 HTML 可视化
"""
import os
import json
from collections import defaultdict


class BladeHtmlVisualizer:
    """Blade 依赖关系 HTML 可视化器"""
    
    def __init__(self, nodes, edges, root_target):
        """
        初始化可视化器
        
        Args:
            nodes: target 节点字典 {target_spec: target_info}
            edges: 依赖关系边列表 [(src_spec, dst_spec), ...]
            root_target: 根 target 规范
        """
        self.nodes = nodes
        self.edges = edges
        self.root_target = root_target
    
    def _classify_target(self, target_spec, target_info):
        """
        对 target 进行分类
        
        Args:
            target_spec: target 规范
            target_info: target 信息
            
        Returns:
            分类名称
        """
        # 外部依赖
        if target_spec.startswith('#'):
            return f"External/{target_info.get('name', target_spec[1:])}"
        
        # 根据完整路径分类
        if ':' in target_spec:
            # 提取路径部分（冒号之前的部分）
            path_part = target_spec.split(':')[0]
            if path_part:
                return path_part
        
        return "Other"
    
    def _get_target_size(self, target_info):
        """
        估算 target 的大小（用于可视化）
        
        Args:
            target_info: target 信息
            
        Returns:
            估算的大小值
        """
        # 基础大小
        base_size = 10000
        
        # 根据源文件数量增加大小
        srcs = target_info.get('srcs', [])
        hdrs = target_info.get('hdrs', [])
        deps = target_info.get('deps', [])
        
        size = base_size + len(srcs) * 5000 + len(hdrs) * 2000 + len(deps) * 1000
        
        # 外部依赖较小
        if target_info.get('external'):
            size = 5000
        
        return size
    
    def generate(self, output_file):
        """
        生成 HTML 文件
        
        Args:
            output_file: 输出文件路径
        """
        # 准备节点数据
        nodes_data = []
        node_id_map = {}
        
        # 构建依赖图
        dependencies = defaultdict(list)  # node -> [依赖的节点]
        dependents = defaultdict(list)    # node -> [依赖它的节点]
        
        for src, dst in self.edges:
            dependencies[src].append(dst)
            dependents[dst].append(src)
        
        # 使用 BFS 计算每个节点的层级
        queue = [(self.root_target, 0)]
        visited_level = {self.root_target: 0}
        
        while queue:
            current, level = queue.pop(0)
            for dep in dependencies.get(current, []):
                if dep not in visited_level or visited_level[dep] > level + 1:
                    visited_level[dep] = level + 1
                    queue.append((dep, level + 1))
        
        # 为所有节点准备数据
        for target_spec, target_info in self.nodes.items():
            node_id = target_spec
            node_id_map[target_spec] = node_id
            
            level = visited_level.get(target_spec, 999)
            cluster = self._classify_target(target_spec, target_info)
            
            # 提取 target 名称
            if target_spec.startswith('#'):
                name = target_spec[1:]
            elif ':' in target_spec:
                name = target_spec.split(':')[-1]
            else:
                name = target_spec
            
            nodes_data.append({
                'id': node_id,
                'name': name,
                'path': target_spec,
                'size': self._get_target_size(target_info),
                'cluster': cluster,
                'is_source': target_spec == self.root_target,
                'level': level,
                'dep_count': len(dependencies.get(target_spec, [])),
                'dependent_count': len(dependents.get(target_spec, [])),
                'type': target_info.get('type', 'unknown'),
                'srcs_count': len(target_info.get('srcs', [])),
                'hdrs_count': len(target_info.get('hdrs', []))
            })
        
        # 按层级和分类排序
        nodes_data.sort(key=lambda x: (x['level'], x['cluster'], x['name']))
        
        # 准备边数据
        edges_data = []
        for src, dst in self.edges:
            dst_info = self.nodes.get(dst, {})
            edges_data.append({
                'source': node_id_map.get(src, src),
                'target': node_id_map.get(dst, dst),
                'size': self._get_target_size(dst_info)
            })
        
        # 准备模块数据
        module_data = {
            'source_file': self.root_target,
            'source_path': self.root_target,
            'nodes': nodes_data,
            'links': edges_data,
            'node_count': len(nodes_data),
            'edge_count': len(edges_data)
        }
        
        # 生成 HTML
        html_content = self._generate_html([module_data])
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_html(self, modules_data):
        """
        生成 HTML 内容
        
        Args:
            modules_data: 模块数据列表
            
        Returns:
            HTML 字符串
        """
        modules_json = json.dumps(modules_data, ensure_ascii=False)
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>Blade 依赖关系图</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    {self._get_html_body()}
    
    <script>
        {self._get_javascript_code(modules_json)}
    </script>
</body>
</html>"""
    
    def _get_css_styles(self):
        """返回 CSS 样式"""
        return """* {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            overflow: hidden;
        }
        
        #graph {
            width: 100vw;
            height: 100vh;
            background: #fafafa;
        }
        
        .node {
            cursor: pointer;
        }
        
        .node circle {
            stroke: #fff;
            stroke-width: 2px;
            transition: all 0.3s ease;
        }
        
        .node:hover circle {
            stroke-width: 3px;
            filter: brightness(1.1);
        }
        
        .node.dimmed {
            opacity: 0.2;
        }
        
        .node.highlighted {
            opacity: 1;
        }
        
        .node text {
            font-size: 11px;
            pointer-events: none;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }
        
        .link {
            stroke: #999;
            stroke-opacity: 0.3;
            stroke-width: 1.5px;
            fill: none;
            transition: all 0.3s ease;
        }
        
        .link.dimmed {
            stroke-opacity: 0.05;
        }
        
        .link.heavy {
            stroke: #ff9800;
            stroke-width: 2px;
        }
        
        .link.dependency {
            stroke: #f44336 !important;
            stroke-width: 2.5px !important;
            stroke-opacity: 0.8 !important;
        }
        
        .link.dependent {
            stroke: #4caf50 !important;
            stroke-width: 2.5px !important;
            stroke-opacity: 0.8 !important;
        }
        
        #controls {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 350px;
            z-index: 1000;
            transition: transform 0.3s ease, opacity 0.3s ease;
        }
        
        #controls.collapsed {
            transform: translateX(-370px);
            opacity: 0;
            pointer-events: none;
        }
        
        #controls h2 {
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #333;
            border-bottom: 2px solid #2196F3;
            padding-bottom: 8px;
        }
        
        #controls .info {
            margin-bottom: 15px;
            font-size: 13px;
            color: #666;
            line-height: 1.6;
        }
        
        .stats {
            display: flex;
            gap: 15px;
            margin-top: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 4px;
        }
        
        .stat-item {
            flex: 1;
            text-align: center;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
        }
        
        .stat-label {
            font-size: 11px;
            color: #999;
            margin-top: 2px;
        }
        
        #search {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            margin-top: 10px;
        }
        
        #search:focus {
            outline: none;
            border-color: #2196F3;
        }
        
        .layout-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        .layout-btn {
            flex: 1;
            padding: 8px;
            border: 1px solid #2196F3;
            background: white;
            color: #2196F3;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }
        
        .layout-btn:hover {
            background: #E3F2FD;
        }
        
        .layout-btn.active {
            background: #2196F3;
            color: white;
        }
        
        .cluster-rect {
            fill: rgba(33, 150, 243, 0.03);
            stroke: #2196F3;
            stroke-width: 2px;
            stroke-dasharray: 5,5;
            opacity: 0.6;
            transition: all 0.3s ease;
        }
        
        .cluster-rect:hover {
            fill: rgba(33, 150, 243, 0.08);
            opacity: 1;
        }
        
        .cluster-label {
            font-size: 11px;
            fill: #2196F3;
            font-weight: bold;
            pointer-events: none;
        }
        
        .level-label {
            font-size: 14px;
            fill: #666;
            font-weight: bold;
            text-anchor: middle;
        }
        
        .legend {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        .legend-title {
            font-weight: bold;
            margin-bottom: 8px;
            color: #333;
            font-size: 13px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 6px 0;
            font-size: 12px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 8px;
            border: 1px solid #ddd;
        }
        
        .legend-line {
            width: 30px;
            height: 3px;
            margin-right: 8px;
        }
        
        #node-info {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            min-height: 60px;
        }
        
        #node-info.empty {
            display: none;
        }
        
        #node-info strong {
            color: #2196F3;
            font-size: 14px;
        }
        
        #node-info div {
            margin: 5px 0;
            font-size: 12px;
            color: #666;
        }
        
        #toggle-btn {
            position: absolute;
            top: 20px;
            left: 390px;
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #2196F3;
            color: #2196F3;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1001;
            transition: all 0.3s ease;
        }
        
        #toggle-btn:hover {
            background: #E3F2FD;
            transform: scale(1.05);
        }
        
        #toggle-btn.collapsed {
            left: 20px;
        }"""
    
    def _get_html_body(self):
        """返回 HTML body 部分"""
        return """<button id="toggle-btn" title="收起/展开控制面板">◀</button>
    
    <div id="controls">
        <h2>Blade 依赖关系图</h2>
        <div class="info">
            <strong>根 Target：</strong><span id="current-module">-</span><br>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="node-count">0</div>
                    <div class="stat-label">Target</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="edge-count">0</div>
                    <div class="stat-label">依赖</div>
                </div>
            </div>
        </div>
        
        <input type="text" id="search" placeholder="搜索 target 名称..." />
        
        <div class="layout-buttons">
            <button class="layout-btn active" id="btn-tree">📊 树状布局</button>
            <button class="layout-btn" id="btn-force">🔄 力导向</button>
        </div>
        
        <div class="info" style="margin-top: 10px; font-size: 11px; color: #999;">
            💡 树状布局：从左到右按依赖层级排列，相同模块的 target 分组显示
        </div>
        
        <div class="legend">
            <div class="legend-title">节点大小（Target 复杂度）</div>
            <div class="legend-item">
                <div class="legend-color" style="background: #E8F5E9;"></div>
                <span>外部依赖</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FFF9C4;"></div>
                <span>简单 Target</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FFCC80;"></div>
                <span>中等 Target</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #EF9A9A;"></div>
                <span>复杂 Target</span>
            </div>
            
            <div class="legend-title" style="margin-top: 12px;">连线颜色（点击节点时）</div>
            <div class="legend-item">
                <div class="legend-line" style="background: #f44336;"></div>
                <span>当前节点依赖的 Target</span>
            </div>
            <div class="legend-item">
                <div class="legend-line" style="background: #4caf50;"></div>
                <span>依赖当前节点的 Target</span>
            </div>
        </div>
        
        <div id="node-info" class="empty"></div>
    </div>
    
    <svg id="graph"></svg>"""
    
    def _get_javascript_code(self, modules_json):
        """返回 JavaScript 代码"""
        return f"""// 所有模块的数据
        const allModules = {modules_json};
        let currentModuleIndex = 0;
        
        // 当前模块的数据
        let nodesData = [];
        let linksData = [];
        
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const svg = d3.select("#graph")
            .attr("viewBox", [0, 0, width, height])
            .call(d3.zoom()
                .scaleExtent([0.1, 10])
                .on("zoom", (event) => {{
                    g.attr("transform", event.transform);
                }}));
        
        const g = svg.append("g");
        
        // 颜色映射
        function getNodeColor(size) {{
            if (size < 10 * 1024) return "#E8F5E9";
            if (size < 50 * 1024) return "#FFF9C4";
            if (size < 200 * 1024) return "#FFCC80";
            return "#EF9A9A";
        }}
        
        function getNodeRadius(size) {{
            return Math.max(8, Math.min(30, Math.sqrt(size) / 50 + 8));
        }}
        
        // 获取集群的排序优先级
        function getClusterPriority(clusterName) {{
            if (clusterName.startsWith('External/')) return 3;
            return 0;
        }}
        
        // 计算层次化布局位置
        function calculateTreeLayout() {{
            g.selectAll('.cluster-rect').remove();
            g.selectAll('.cluster-label').remove();
            
            const levelClusterGroups = {{}};
            
            nodesData.forEach(d => {{
                const key = `${{d.level}}-${{d.cluster}}`;
                if (!levelClusterGroups[key]) {{
                    levelClusterGroups[key] = {{
                        level: d.level,
                        cluster: d.cluster,
                        nodes: []
                    }};
                }}
                levelClusterGroups[key].nodes.push(d);
            }});
            
            const groups = Object.values(levelClusterGroups).sort((a, b) => {{
                if (a.level !== b.level) return a.level - b.level;
                const priorityA = getClusterPriority(a.cluster);
                const priorityB = getClusterPriority(b.cluster);
                if (priorityA !== priorityB) return priorityA - priorityB;
                return a.cluster.localeCompare(b.cluster);
            }});
            
            const levels = [...new Set(groups.map(g => g.level))].sort((a, b) => a - b);
            const maxLevel = Math.max(...levels);
            const levelWidth = Math.max(250, (width - 300) / (maxLevel + 1));
            
            const levelGroups = {{}};
            groups.forEach(group => {{
                if (!levelGroups[group.level]) levelGroups[group.level] = [];
                levelGroups[group.level].push(group);
            }});
            
            const clusterRects = [];
            const levelLabels = [];
            
            levels.forEach((level, levelIdx) => {{
                const levelGroupList = levelGroups[level];
                const x = 150 + levelIdx * levelWidth;
                
                let currentY = 80;
                
                levelGroupList.forEach(group => {{
                    const nodes = group.nodes;
                    const nodeSpacing = Math.max(45, Math.min(60, 300 / nodes.length));
                    const groupHeight = nodes.length * nodeSpacing + 30;
                    const startY = currentY;
                    
                    nodes.forEach((node, idx) => {{
                        node.fx = x;
                        node.fy = startY + 25 + idx * nodeSpacing;
                        node.x = node.fx;
                        node.y = node.fy;
                    }});
                    
                    clusterRects.push({{
                        x: x - 50,
                        y: startY,
                        width: 220,
                        height: groupHeight,
                        cluster: group.cluster,
                        level: group.level,
                        nodeCount: nodes.length
                    }});
                    
                    currentY += groupHeight + 15;
                }});
                
                levelLabels.push({{
                    x: x,
                    y: 30,
                    text: level === 0 ? '根 Target' : `依赖层级 ${{level}}`,
                    level: level
                }});
            }});
            
            const clusterGroup = g.insert('g', ':first-child')
                .attr('class', 'cluster-rects');
            
            clusterGroup.selectAll('rect')
                .data(clusterRects)
                .join('rect')
                .attr('class', 'cluster-rect')
                .attr('x', d => d.x)
                .attr('y', d => d.y)
                .attr('width', d => d.width)
                .attr('height', d => d.height)
                .attr('rx', 8);
            
            clusterGroup.selectAll('.cluster-label')
                .data(clusterRects)
                .join('text')
                .attr('class', 'cluster-label')
                .attr('x', d => d.x + 10)
                .attr('y', d => d.y + 16)
                .text(d => `${{d.cluster}} (${{d.nodeCount}})`);
            
            clusterGroup.selectAll('.level-label')
                .data(levelLabels)
                .join('text')
                .attr('class', 'level-label')
                .attr('x', d => d.x)
                .attr('y', d => d.y)
                .text(d => d.text);
        }}
        
        const simulation = d3.forceSimulation(nodesData)
            .force("link", d3.forceLink(linksData).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => getNodeRadius(d.size) + 5))
            .stop();
        
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 20)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#999");
        
        let link = null;
        let node = null;
        let selectedNode = null;
        
        svg.on("click", function(event) {{
            if (event.target === this || event.target.tagName === 'svg') {{
                resetHighlight();
                selectedNode = null;
            }}
        }});
        
        function resetHighlight() {{
            if (!node || !link) return;
            
            node.classed("dimmed", false).classed("highlighted", false);
            link.classed("dimmed", false)
                .classed("dependency", false)
                .classed("dependent", false);
            
            const nodeInfo = document.getElementById("node-info");
            nodeInfo.className = "empty";
            nodeInfo.innerHTML = "";
        }}
        
        document.getElementById("search").addEventListener("input", function(e) {{
            const searchTerm = e.target.value.toLowerCase();
            
            if (!searchTerm) {{
                resetHighlight();
                return;
            }}
            
            if (!node || !link) return;
            
            node.classed("dimmed", d => !d.name.toLowerCase().includes(searchTerm))
                .classed("highlighted", d => d.name.toLowerCase().includes(searchTerm));
            
            link.classed("dimmed", l => {{
                const sourceMatch = l.source.name.toLowerCase().includes(searchTerm);
                const targetMatch = l.target.name.toLowerCase().includes(searchTerm);
                return !sourceMatch && !targetMatch;
            }});
        }});
        
        function updatePositions() {{
            link.attr("d", d => {{
                const sx = d.source.x || 0;
                const sy = d.source.y || 0;
                const tx = d.target.x || 0;
                const ty = d.target.y || 0;
                return `M${{sx}},${{sy}}L${{tx}},${{ty}}`;
            }});
            
            node.attr("transform", d => `translate(${{d.x || 0}},${{d.y || 0}})`);
        }}
        
        simulation.on("tick", updatePositions);
        
        let currentLayout = 'tree';
        
        function switchToTreeLayout() {{
            currentLayout = 'tree';
            simulation.stop();
            calculateTreeLayout();
            
            g.selectAll('.cluster-rects').style('display', 'block');
            
            node.transition()
                .duration(750)
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
            
            link.transition()
                .duration(750)
                .attr("d", d => `M${{d.source.x}},${{d.source.y}}L${{d.target.x}},${{d.target.y}}`);
            
            document.getElementById('btn-tree').classList.add('active');
            document.getElementById('btn-force').classList.remove('active');
        }}
        
        function switchToForceLayout() {{
            currentLayout = 'force';
            
            g.selectAll('.cluster-rects').style('display', 'none');
            
            nodesData.forEach(d => {{
                d.fx = null;
                d.fy = null;
            }});
            
            simulation.alpha(1).restart();
            
            document.getElementById('btn-tree').classList.remove('active');
            document.getElementById('btn-force').classList.add('active');
        }}
        
        document.getElementById('btn-tree').addEventListener('click', switchToTreeLayout);
        document.getElementById('btn-force').addEventListener('click', switchToForceLayout);
        
        function dragstarted(event, d) {{
            if (currentLayout === 'force') {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
            }}
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
            if (currentLayout === 'tree') {{
                updatePositions();
            }}
        }}
        
        function dragended(event, d) {{
            if (currentLayout === 'force') {{
                if (!event.active) simulation.alphaTarget(0);
            }}
        }}
        
        function loadModule(index) {{
            if (index < 0 || index >= allModules.length) return;
            
            currentModuleIndex = index;
            const module = allModules[index];
            
            nodesData = module.nodes;
            linksData = module.links;
            
            document.getElementById('current-module').textContent = module.source_file;
            document.getElementById('node-count').textContent = module.node_count;
            document.getElementById('edge-count').textContent = module.edge_count;
            
            redrawGraph();
        }}
        
        function redrawGraph() {{
            g.selectAll("*").remove();
            
            simulation.nodes(nodesData);
            simulation.force("link").links(linksData);
            
            const newLink = g.append("g")
                .selectAll("path")
                .data(linksData)
                .join("path")
                .attr("class", "link")
                .attr("marker-end", "url(#arrowhead)");
            
            link = newLink;
            
            const newNode = g.append("g")
                .selectAll("g")
                .data(nodesData)
                .join("g")
                .attr("class", "node")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            newNode.append("circle")
                .attr("r", d => getNodeRadius(d.size))
                .attr("fill", d => getNodeColor(d.size))
                .attr("stroke", d => d.is_source ? "#2196F3" : "#fff")
                .attr("stroke-width", d => d.is_source ? 4 : 2);
            
            newNode.append("text")
                .text(d => d.name)
                .attr("x", d => getNodeRadius(d.size) + 5)
                .attr("y", 4)
                .style("font-size", "11px");
            
            node = newNode;
            
            node.on("click", function(event, d) {{
                event.stopPropagation();
                
                if (selectedNode === d.id) {{
                    resetHighlight();
                    selectedNode = null;
                    return;
                }}
                
                selectedNode = d.id;
                
                node.classed("dimmed", true).classed("highlighted", false);
                link.classed("dimmed", true)
                    .classed("dependency", false)
                    .classed("dependent", false);
                
                d3.select(this).classed("dimmed", false).classed("highlighted", true);
                
                const relatedNodes = new Set([d.id]);
                let dependencyCount = 0;
                let dependentCount = 0;
                
                link.each(function(l) {{
                    if (l.source.id === d.id) {{
                        d3.select(this)
                            .classed("dimmed", false)
                            .classed("dependency", true);
                        relatedNodes.add(l.target.id);
                        dependencyCount++;
                    }} else if (l.target.id === d.id) {{
                        d3.select(this)
                            .classed("dimmed", false)
                            .classed("dependent", true);
                        relatedNodes.add(l.source.id);
                        dependentCount++;
                    }}
                }});
                
                node.filter(n => relatedNodes.has(n.id))
                    .classed("dimmed", false)
                    .classed("highlighted", true);
                
                const nodeInfo = document.getElementById("node-info");
                nodeInfo.className = "";
                nodeInfo.innerHTML = `
                    <strong>${{d.name}}</strong>
                    <div><strong>Target：</strong>${{d.path}}</div>
                    <div><strong>类型：</strong>${{d.type}}</div>
                    <div><strong>模块：</strong>${{d.cluster}}</div>
                    <div><strong>源文件：</strong>${{d.srcs_count}} 个</div>
                    <div><strong>头文件：</strong>${{d.hdrs_count}} 个</div>
                    <div style="margin-top: 10px;">
                        <strong>依赖：</strong><span style="color: #f44336;">${{dependencyCount}}</span> 个 Target<br>
                        <strong>被依赖：</strong><span style="color: #4caf50;">${{dependentCount}}</span> 个 Target
                    </div>
                `;
            }});
            
            resetHighlight();
            selectedNode = null;
            
            if (currentLayout === 'tree') {{
                switchToTreeLayout();
            }} else {{
                switchToForceLayout();
            }}
        }}
        
        // 控制面板收起/展开功能
        const toggleBtn = document.getElementById('toggle-btn');
        const controls = document.getElementById('controls');
        let isCollapsed = false;
        
        toggleBtn.addEventListener('click', () => {{
            isCollapsed = !isCollapsed;
            
            if (isCollapsed) {{
                controls.classList.add('collapsed');
                toggleBtn.classList.add('collapsed');
                toggleBtn.innerHTML = '▶';
                toggleBtn.title = '展开控制面板';
            }} else {{
                controls.classList.remove('collapsed');
                toggleBtn.classList.remove('collapsed');
                toggleBtn.innerHTML = '◀';
                toggleBtn.title = '收起控制面板';
            }}
        }});
        
        loadModule(0);"""

