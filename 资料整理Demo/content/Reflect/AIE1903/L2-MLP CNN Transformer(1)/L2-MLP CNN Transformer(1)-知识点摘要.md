# L2-MLP CNN Transformer(1) 知识点摘要

## 一、知识点概述

<a id="sm-01"></a>
### 1. 神经网络基础：线性变换、激活与预测
- 概括：一切深度网络的重复运算都是「加权求和 + 偏置 + 激活」：z = wᵀx + b、a = φ(z)；线性层按矩阵乘法变换特征维度 [B, D_in] → [B, D_out]；激活函数（ReLU/Sigmoid/Tanh）提供非线性；预测时经 Logits → Softmax → argmax 三步把分数变成答案。
- 📎 详见：[仿射变换与神经元计算](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-01)、[线性层与特征维度变换](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-02)、[激活函数](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-03)、[张量形状追踪](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-04)、[Logits、Softmax 与决策](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-05)

<a id="sm-02"></a>
### 2. 多层感知机 MLP
- 概括：全连接（稠密）层让每个输出神经元连接所有输入特征，多层堆叠加激活即 MLP，能层层提炼特征；参数量随 D_in×D_out 增长。MLP 简单灵活、适合紧凑向量，但展平图像会丢空间结构、参数爆炸、输入尺寸固定。
- 📎 详见：[全连接（稠密）层](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-06)、[多层感知机与深层堆叠](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-07)、[手写数字识别的形状流](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-08)、[MLP 参数计数](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-09)、[MLP 处理图像的三个缺陷](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-10)

<a id="sm-03"></a>
### 3. 卷积神经网络 CNN
- 概括：CNN 用共享的卷积核在图上滑动做「乘加」，保留局部结构并大幅减参；padding 与 stride 控制输出尺寸（H_out = floor((H+2P−K)/S)+1）；多滤波器产生多通道特征图；池化压缩空间。推理时卷积块堆叠（空间递减、通道递增）后接分类头输出 logits。
- 📎 详见：[卷积核与滑动窗口](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-11)、[填充与步长](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-12)、[输出尺寸公式](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-13)、[通道与多滤波器](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-14)、[池化：最大池化与平均池化](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-15)、[CNN 完整推理流程](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-16)

<a id="sm-04"></a>
### 4. 自注意力机制
- 概括：自注意力让每个 token 用 Query 去匹配所有 token 的 Key 得到分数，Softmax 转成和为 1 的权重，再对 Value 加权求和，产出吸收全局上下文的 token 表示；完整公式 Attention(Q,K,V) = Softmax(QKᵀ/√D)V，注意力矩阵每行是一个 token 的分布。
- 📎 详见：[自注意力与 Query/Key/Value 三角色](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-17)、[注意力分数：Query–Key 相似度](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-18)、[Softmax 注意力权重](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-19)、[加权求和与上下文表示](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-20)、[注意力分布矩阵](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-21)、[缩放点积注意力公式](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-22)

<a id="sm-05"></a>
### 5. Transformer 层的结构
- 概括：一层 Transformer = LayerNorm → 自注意力 → 残差相加 → LayerNorm → MLP → 残差相加；注意力跨 token 混合信息，MLP 在 token 内变换特征，LayerNorm 稳定数值、残差连接提供直通梯度。输入输出形状都是 [B,N,D]，故可无限堆叠出更深语义。
- 📎 详见：[层归一化 LayerNorm](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-23)、[残差连接](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-24)、[Transformer 层完整数据流](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-25)、[Transformer 层的堆叠](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-26)

<a id="sm-06"></a>
### 6. 三种架构对比与选型
- 概括：MLP 全连接、适合紧凑向量与表格数据；CNN 局部共享核、适合图像与空间网格；Transformer 全局内容相关注意力、适合文本与长 token 序列。现代系统常组合三者（如 CNN + Transformer + MLP 头）。
- 📎 详见：[三种架构对比与选型](L2-MLP CNN Transformer(1)-知识点讲解.md#kp-27)

## 二、知识点联系（概览）
- 神经网络基础 → MLP / CNN / Transformer（依赖）：线性层、激活、Softmax 是三种架构共同的基础构件。
- MLP → CNN（动机）：MLP 在图像上的缺陷（丢结构、参数爆炸）催生了共享局部核的 CNN。
- CNN → Transformer（动机）：卷积只能看局部，Transformer 用全局注意力让远距离 token 直接交换信息。
- 自注意力 → Transformer 层（依赖）：注意力是层内「跨 token 混合」子层，配合 MLP、LayerNorm、残差构成完整层。
- Transformer 层 → 层堆叠（依赖）：单层形状不变，可反复堆叠加深语义。
- 三种架构 → 组合系统（应用）：现代多模态系统常 CNN 提取局部 + Transformer 全局推理 + MLP 做分类头。
