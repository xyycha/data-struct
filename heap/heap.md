1. 完全二叉树
    - 定义：二叉树的深度为h，除第 h 层外，其它各层 (1～h-1) 的结点数都达到最大个数，第 h 层所有的结点都连续集中在最左边
    - ![完全二叉树示例](http://image.sprinkle.top/image/tree/complete_binary_tree.jpeg)
    - 性质: 二叉树可以使用 数组heap[] 表示. 
        - heap[index]节点的 父节点为 heap[(index - 1) // 2 ]  子节点为 heap[2 * index + 1] heap[2 * index + 2]
        - 第index(1, 2, 3 ...)节点 heap[index - 1] 的 父节点为 heap[index // 2 - 1] 子节点为 heap[index * 2 - 1] heap[index * 2]
    - [完全二叉树]详细信息(https://baike.baidu.com/item/%E5%AE%8C%E5%85%A8%E4%BA%8C%E5%8F%89%E6%A0%91/7773232?fr=aladdin)

2. 堆定义:
    - [完全二叉树](https://baike.baidu.com/item/%E5%AE%8C%E5%85%A8%E4%BA%8C%E5%8F%89%E6%A0%91/7773232?fr=aladdin)
    - 父节点的值 小于等于子节点的值

3. 堆操作:
    - pop 将 堆的根节点 抛出 heap数组元素个数减1，需要将最后一个元素填充到前面的某个位置，需要做的就是寻找目标位置
        - a. 根节点置为空穴
        - b. 是否存在 左右节点，否：步骤 g
        - c. 比较 空穴节点 的 左右节点 的权重，选择较小权重的节点 记为 节点A
        - d. 最后一个节点 记为 B; 将节点A 权重值 与 节点B 的权重值 比较
        - e. 如果 节点A 的权重值 小与 节点B 的权重值，空穴节点被节点A填充， 节点A 置为空穴， 重复 b c d 步骤
        - f. 如果 节点A 的权重值 大于等于 节点B 的权重值 步骤 g
        - g. 空穴节点被节点B填充
        - h. heap[] 数组 缩短 1
        
    - insert 将新节点插入到 heap数组的最后，一次判断该节点到根节点的路径上的 节点是否破坏了 堆的性质(父节点的值 小于等于子节点的值)
        - a. heap 添加一个 空穴
        - b. 判断空穴是否有 父节点 否: 步骤 f
        - c. 比较 空穴 和 父节点 的权重值
        - d. 如果 父节点 大于  新节点 的权重值 将空穴 父节点位置置换 重复 b
        - e. 如果 父节点 小于等于 新节点 的权重值 步骤 f
        - f. 空穴由新节点填充
        - g. heap[] 数组 增加 1