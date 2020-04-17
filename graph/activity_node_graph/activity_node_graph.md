1. 动作节点图定义
    1. 每个节点表示一个必须执行的动作以及完成动作所花费的时间
    2. 边 代表这 优先关系 E(v, w) 表示动作v 必须 在 动作w 开始前完成 确定了 动作节点图 不存在圈
    
2. 动作节点图的图像
    1. 图像 ![动作节点图](http://image.sprinkle.top/image/graph/activity_node_graph.png)

3. 事件节点图的图像
    1. 图像 ![事件节点图](http://image.sprinkle.top/image/graph/event_node_graph.png)
    
4. 寻找关键路径和每个节点的最晚结束时间和最早结束时间
    1. 无圈图 借助拓扑顺序遍历 所有节点
    2. 正向拓扑 最早结束时间为 max(父节点最早结束时间 + 边的权重值)
        - 图像 ![图像](http://image.sprinkle.top/image/graph/min_event_node_graph.png)
    3. 反向拓扑 最晚结束时间为 min(子节点最晚结束时间 - 边的权重值)
        - 图像 ![图像](http://image.sprinkle.top/image/graph/max_event_node_graph.png)
