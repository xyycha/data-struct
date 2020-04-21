1. 双连通性定义
    - 如果一个连通的无向图的任一顶点删除之后，剩下的图依然连通，那么这样的无向连通图就称为是双连通的(biconnected)
    - 双连通图像 ![图像](http://image.sprinkle.top/image/graph/biconnected_graph.png)
    
2. 双连通性的条件
    - 连通的无向图
    - 删除任意节点，剩下的图依旧是连通的
    
3. 割点定义
    - 连通的无向图 删除某些节点就不再连通，那么这些节点叫做割点
    - 割点图像 ![图像](http://image.sprinkle.top/image/graph/cutvertex.png)
    
4. Num值定义 和 Low值的定义
    - Num值: 前序遍历时，节点的顺序值
    - Low值: min(节点通过n(n>=0)条正向边和一条反向边所到达最小Num值的节点的Num值， 节点本身的Num值)
        - 无子节点时 Low = Num
        - 有子节点时 
            - 无反向边时 Low = min(所有子节点的Low, 本身节点的Num值)
            - 有反向边时 Low = 反向边节点的Num值
        - 求解过程
            - 本身的Num值
            - 后续遍历 计算全部的子节点的Low值
            - 结合本身的反向边的节点的Num值
            - 取最小值
            
    
4. 割点的寻找
    - 前序遍历 计算每个节点的 Num 值
    - 后续遍历 计算每个节点的 Low 值
    - 寻找割点
        - 根节点
            - 两个及以上的子节点  割点
        - 非根节点
            - 存在一个子节点的 Low值 >= 本节点的 Num值
    - 寻找割点的图像 ![图像](http://image.sprinkle.top/image/graph/cutvertex_find.png)
