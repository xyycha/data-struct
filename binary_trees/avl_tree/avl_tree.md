1. AVL树定义
    - 二叉查找树
    - 平衡条件: 左子树高度与右子树高度差 最多1
    
2. AVL树的图像
    - 图像示例 ![AVL 树](http://image.sprinkle.top/image/tree/avl_tree.png)
    
3. AVL树性质
    - 高度为 h 为的AVL树的最少节点数 f(h)
        - 节点最少 左子树和右子树分别为 高度为 h-1 h-2的AVL树
        - 因此 f(h) = f(h-1) + f(h-2) + 1
        - 初始条件 f(0) = 1 f(1) = 2
        
4. AVL树的旋转操作
    - 左旋
        - k2必须存在左节点k1
        - k2 围绕 k1 顺时针旋转(将k1原有的 右子树Y打断 右子树Y 移动到k2空闲的左子树)
        - k1 的右节点 变为 k2
        - k2 的左子树 变为 k1的右子树
        - 图示: ![左旋转](http://image.sprinkle.top/image/tree/single_left_rotate.png)
    - 右旋
        - k1必须存在右节点k2
        - k1 围绕 k2 逆时针旋转(将k2原有的 左子树Y打断 右子树Y 移动到k1空闲的右子树)
        - k2 的左节点 变为 k1
        - k1 的右子树 变为 k2的左子树
        - 图示: ![右旋转](http://image.sprinkle.top/image/tree/single_right_rotate.png)
        
5. AVL树 失去平衡的四个情况 失去平衡的节点 记为 节点A
    - a. 节点A的左节点的左子树进行了插入
    - b. 节点A的左节点的右子树进行了插入
    - c. 节点A的右节点的右子树进行了插入
    - d. 节点A的右节点的左子树进行了插入
    
6. AVL树 恢复平衡的操作
    - a. 节点A进行左旋转
    - b. 节点A的左节点进行右旋转 节点A进行左旋转
    - c. 节点A进行右旋转
    - d. 节点A的右节点进行左旋转 节点A进行右旋转
    
7. 我的对AVL树旋转的理解：
    - 节点A的左旋转 效果只有 节点A左节点的左子树高度-1 A右子树的高度+1
    - 节点A的右旋转 效果只有 节点A右节点的右子树高度-1 A左子树的高度+1
    
8. 借助7理解5 6 的操作
    - a. 节点A的左节点的左子树进行了插入
        - 因为A是第一个失去了平衡的
        - A的 左子树高度 比 右子树高度 大 2
        - 但是 A 的左节点 是没有失去平衡 也就是A左节点的右子树的高度不能变更
        - 那么需要操作后的效果就是 A的左节点的左子树高度需要-1 A的右子树的高度需要 +1
        - 这就是 节点A的左旋

    - b. 节点A的左节点的右子树进行了插入
        - 需要做的效果 减少A左节点的右子树 整体 深度 增加A右子树深度
        - 见图示 ![双旋转](http://image.sprinkle.top/image/tree/double_rotate.jpg)
        - 需要进行两个旋转的原因是
            - 在节点L的右旋转 只能减少 LR的右子树?R深度  左子树没有变
            - 所以需要在A进行左旋 减少 L及其子树的深度（包括?L) 增加A的右子树R深度 同时不变动?R深度