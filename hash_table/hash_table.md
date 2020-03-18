1. 散列定义
    - a. 常数平均时间 进行插入、删除和查找的技术

2. 散列函数定义
    - a. 关键字 到 散列表下标的 映射关系
    - b. 运算简单
    - c. 不同的关键字 映射到不同的下标

3. 冲突
    - a. 两个不同的关键字 映射到相同的下标
    
4. 冲突解决的方式
    - a. 分离链接法 将 下标相同的元素放到 一个链表中
        - 缺点 维护另一个数据结构
    - b. 开放地址法 发生冲突 以 (Hash(key) + F(collision_time)) % TableSize 计算新的地址 直到不冲突为止
        - 1. 线性探测法  F(collision_time) = collision_time
            - 缺点 容易产生聚集
            - 填充率越高 失败查询和插入(都需要找到空的位置)效率越差
        - 2. 平方探测法  F(collision_time) = collision_time * collision_time
            - 缺点 最大值必须为素数 填充率不能超过0.5
            - 优点 解决了线性探测的 聚集 问题
        - 3. 双散列 F(collision_time) = collision_time * Hash2(key) Hash2()不能为0
            - 缺点 平方探测方法更加简单 更快

5. 再散列
    - 定义 当表的元素填充的太满时，增大散列表的大小，使用新的 散列函数进行计算迁移数据
    - 方法
        - 1. 只要表填满到 一半 就再散列
        - 2. 极端 插入失败时 再散列
        - 3. 途中策略 到达某一个装填因子 就进行散列
        
6. 可扩散列
    - 可扩散列设计图像![可扩散列](http://image.sprinkle.top/image/tree/extendable_hash_table.PNG)
    - 插入、删除、查找 实现 查看 hash_table.py (success 2020-03-18)
    