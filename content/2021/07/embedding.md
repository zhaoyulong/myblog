Date: 2021-07-17 16:51
Modified: 2021-07-17 18:01
Title: 机器学习--embedding
Category: machine learning
Slug: articles/2021/07/embedding
tags: machine learning, deep learning, embedding
summary: 介绍深度学习中的embedding

## 什么是embedding
Embedding 在形式上是一个向量，其维度根据需求而定，一般是集合的形式存在。在神经网络中，embedding 是非常有用的，因为它不光可以减少离散变量的空间维数，同时还可以有意义的表示该变量。

在实际应用中，Embedding可以代表一个词，一张图片，一个句子，一件商品等等。

## embedding特点

embedding 有以下 3 个主要目的：

1. 在 embedding 空间中查找最近邻，这可以用于根据用户的兴趣来进行推荐。
1. 作为监督性学习任务的输入。
1. 用于可视化不同离散变量之间的关系

要了解 embedding 的优点，我们可以对应 One-hot 编码来观察。One-hot 编码是一种最普通常见的表示离散数据的表示，首先我们计算出需要表示的离散或类别变量的总个数 N，然后对于每个变量，我们就可以用 N-1 个 0 和单个 1 组成的 vector 来表示每个类别。这样做有两个很明显的缺点：

1. 对于具有非常多类型的类别变量，变换后的向量维数过于巨大，且过于稀疏。
1. 映射之间完全独立，并不能表示出不同类别之间的关系
