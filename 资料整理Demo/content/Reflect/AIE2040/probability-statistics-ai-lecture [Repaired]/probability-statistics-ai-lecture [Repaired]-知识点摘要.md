# probability-statistics-ai-lecture [Repaired] 知识点摘要

## 一、知识点概述

<a id="sm-01"></a>
### 1. 概率公理与集合运算
- 概括：柯尔莫哥洛夫三条公理（非负性、归一性、可数可加性）是概率的数学地基；补集、并集、交集与并集公式 P(A ∪ B) = P(A) + P(B) − P(A ∩ B) 是基本运算规则。
- 📎 详见：[概率公理](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-01)、[集合运算与概率规则](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-02)

<a id="sm-02"></a>
### 2. 随机变量与分布描述
- 概括：随机变量把随机结果映射为数字，分离散/连续两类；离散用 PMF 给概率，连续用 PDF 给面积、CDF 给累计概率，核心误区是"密度 ≠ 概率"。
- 📎 详见：[随机变量](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-03)、[PMF/PDF/CDF](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-04)

<a id="sm-03"></a>
### 3. 期望、方差与独立性
- 概括：期望是长期平均，方差/标准差是波动幅度；独立性 P(A ∩ B) = P(A)P(B) 是强建模假设，让联合概率可分解，是朴素贝叶斯的前提。
- 📎 详见：[期望与方差](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-05)、[独立性](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-06)

<a id="sm-04"></a>
### 4. 条件概率与贝叶斯定理
- 概括：条件概率把世界缩小到 B；全概率公式按分支加权；贝叶斯定理"后验 ∝ 先验 × 似然"把证据变成更新后的信念，医学诊断是经典算例（阳性后验仅约 15.4%）。
- 📎 详见：[条件概率](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-07)、[全概率公式](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-08)、[贝叶斯定理](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-09)

<a id="sm-05"></a>
### 5. 大数定律与中心极限定理
- 概括：大数定律说样本均值收敛到期望（长期频率稳定）；中心极限定理说标准化样本均值趋近标准正态（不管原始分布长什么样）。
- 📎 详见：[大数定律](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-10)、[中心极限定理](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-11)

<a id="sm-06"></a>
### 6. 信息熵
- 概括：熵 H(X) = −Σ P(x) log P(x) 度量不确定性，p=0.5 时最大；最大熵原理要求"只承诺已知信息，不额外假设"。
- 📎 详见：[信息熵](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-12)

<a id="sm-07"></a>
### 7. 分布选择总览
- 概括：按数据类型选分布家族（二值→Bernoulli、计数→Poisson、钟形→Gaussian、概率→Beta 等）；分布是一种假设，选错会引入系统偏差。
- 📎 详见：[分布选择总览](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-13)、[分布选择的决策树](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-25)

<a id="sm-08"></a>
### 8. 离散分布族
- 概括：Bernoulli 描述一次 0-1 试验，Binomial 描述 n 次成功数，Poisson 描述区间内稀疏计数，Multinomial 推广到 K 类计数。
- 📎 详见：[伯努利分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-14)、[二项分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-15)、[泊松分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-16)、[多项分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-17)

<a id="sm-09"></a>
### 9. 连续分布族
- 概括：Uniform 是有限区间上的等可能；Normal 是钟形、由 μ 和 σ 决定；Exponential/Gamma 描述等待时间；Beta 描述概率参数本身、Dirichlet 描述概率向量。
- 📎 详见：[均匀分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-18)、[正态分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-19)、[指数分布与伽马分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-20)、[贝塔分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-21)、[狄利克雷分布](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-23)

<a id="sm-10"></a>
### 10. 指数族
- 概括：常见分布共用统一形式 f(x; η) = h(x) exp(η·T(x) − A(η))，带来充分统计量、共轭先验与广义线性模型的便利。
- 📎 详见：[指数族](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-24)

<a id="sm-11"></a>
### 11. 点估计：MLE 与矩估计
- 概括：MLE 选"让数据最可能"的参数，取对数似然求导；高斯 MLE 给出样本均值，并解释 MSE 损失的由来；矩估计让理论矩等于样本矩，简单但可能低效。
- 📎 详见：[最大似然估计](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-26)、[高斯 MLE](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-27)、[矩估计法](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-28)

<a id="sm-12"></a>
### 12. 贝叶斯估计：MAP、完整贝叶斯与共轭先验
- 概括：MAP 在似然上乘先验（正则化即先验）；完整贝叶斯输出整条后验并做后验预测；共轭先验使后验与先验同族、更新解析（Beta-Bernoulli 等）。
- 📎 详见：[最大后验估计](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-29)、[完整贝叶斯推断](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-30)、[共轭先验](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-22)

<a id="sm-13"></a>
### 13. 生成模型与判别模型
- 概括：生成模型学 p(x,y)/p(x)（能生成、能补全），判别模型直接学 p(y|x) 或决策边界；朴素贝叶斯是生成，逻辑回归是判别。
- 📎 详见：[生成模型与判别模型](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-31)

<a id="sm-14"></a>
### 14. 概率图模型与序列模型
- 概括：贝叶斯网络用有向图按父节点分解联合分布；MRF 用无向势函数表达对称相容；马尔可夫链"未来只看现在"；HMM 是隐状态+发射，配前向/维特比/Baum-Welch 三大算法。
- 📎 详见：[贝叶斯网络](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-32)、[马尔可夫随机场](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-33)、[马尔可夫链](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-34)、[隐马尔可夫模型](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-35)

<a id="sm-15"></a>
### 15. 深度学习中的概率
- 概括：softmax 归一化 logits，交叉熵训练=最大似然，但需校准；Dropout/BNN 用随机前向量化不确定性；GAN 隐式逼近分布、VAE 最大化 ELBO。
- 📎 详见：[Softmax、交叉熵与校准](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-36)、[Dropout 与贝叶斯神经网络](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-37)、[GAN 与 VAE](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-38)

<a id="sm-16"></a>
### 16. 应用案例
- 概括：朴素贝叶斯过滤垃圾邮件、贝叶斯诊断、贝叶斯矩阵分解推荐、MRF/CRF 图像分割、部分可观测强化学习的信念更新——概率贯穿真实系统。
- 📎 详见：[朴素贝叶斯垃圾邮件过滤](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-39)、[医疗诊断](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-40)、[推荐系统](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-41)、[图像分割](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-42)、[强化学习中的不确定性](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-43)

<a id="sm-17"></a>
### 17. 误区、总结与附录
- 概括：八条常见误区集中纠偏（密度≠概率、条件方向、阳性≠患病、CLT、校准等）；费雪信息与渐近正态性给 MLE 配标准误与置信区间。
- 📎 详见：[常见误区汇总](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-44)、[费雪信息与渐近正态性](probability-statistics-ai-lecture [Repaired]-知识点讲解.md#kp-45)

## 二、知识点联系（概览）

- 概率公理 → 集合运算 → 条件概率（依赖）：层层由公理推出。
- 条件概率 → 全概率公式 → 贝叶斯定理（依赖）：分母 P(B) 由全概率展开。
- 贝叶斯定理 → 共轭先验 → 完整贝叶斯推断（应用）：先验×似然→同族后验→后验预测。
- 期望与方差 → 大数定律 → 中心极限定理（递进）：均值收敛与波动形态。
- 伯努利 → 二项 → 多项（推广）：离散计数的层层推广。
- 伯努利 ↔ 贝塔、多项 ↔ 狄利克雷（对偶）：结果分布与"概率参数分布"互为表里。
- 各分布 → 指数族（抽象）：统一骨架；指数族 → 共轭先验/GLM（应用）。
- MLE → MAP → 完整贝叶斯（推广）：只信数据 → 加先验 → 保留完整不确定性。
- 贝叶斯网络 → HMM（特例）：链式结构 + 隐状态。
- MRF → 图像分割、贝叶斯网络 → 医疗诊断、朴素贝叶斯 → 垃圾邮件（应用）。
- 交叉熵训练 = 最大似然（联系）：深度学习的损失函数本质是 MLE。
