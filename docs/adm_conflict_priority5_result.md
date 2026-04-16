# ADM 冲突批次结果填写页

## adm_conflict_priority_01

```text
case_id: adm_conflict_priority_01
sample_id: adm_auto_2143
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG

visual_observation:
图像像是桌面或设备底部的低照度近景拍摄，整体明暗关系和金属/塑料材质并非完全失真，因此第一眼仍可能被当成真实环境照片。但细看后可以发现多个结构异常：上方黑色大平面与下方支撑件的连接关系不清，左侧支腿、中央横杆和右侧竖杆的透视关系彼此打架，局部边缘出现不符合真实工业结构的软化与漂浮感。背景中的雾状高亮区域也缺少清晰来源，导致空间层次显得模糊而拼接感较强。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
支撑杆件之间的连接、遮挡和透视关系不稳定，像是模型生成了“像零件”的形状，但没有严格保持真实结构约束。

key_evidence_2:
低照度和材质反光在整体上营造了真实感，但局部边缘与背景亮区缺少明确物理来源，空间关系不够自洽。

paper_ready_summary:
`adm_conflict_priority_01` 表明，一类困难冲突样本并不依赖明显的人脸或文字错误，而是通过低照度、材质反光和近景构图制造整体真实感，同时在结构连接与空间透视层面暴露生成痕迹。这类样本可能更容易被关注局部异常模式的 Stay-Positive 捕捉，而被三组 FSD 共同漏判。

human_takeaway:
这是“整体像真实工业近景，但局部结构逻辑不成立”的典型强冲突样本。
```

## adm_conflict_priority_02

```text
case_id: adm_conflict_priority_02
sample_id: adm_auto_2720
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG

visual_observation:
图像主体像一组按键或键盘近景，黑灰色按键、磨损质感和斜向构图都很像真实拍摄，因此整体语义非常自然。但每个按键上的符号明显异常，既不像统一语言文字，也不像真实功能按键标记，而更像模型生成的伪字符；同时，个别按键边缘和刻印与表面贴合关系不稳定，部分字符存在轻微漂浮、扭曲和重复形态。这类图像在整体摄影感上很强，但局部文字/符号细节暴露出非常典型的生成缺陷。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
按键字符是最直接的异常来源，符号缺乏真实文字系统的一致性，明显属于伪文本现象。

key_evidence_2:
部分字符与按键表面的透视和附着关系不稳定，说明模型在细节层面没有保持精确的几何一致性。

paper_ready_summary:
`adm_conflict_priority_02` 说明，强冲突样本中有一类属于“整体摄影真实，但局部伪文本非常明显”的情况。此类样本对具备局部异常敏感性的判别器更友好，却可能因为整体场景过于自然而被 FSD 三个版本共同判断为 real。

human_takeaway:
这是最容易解释“Stay-Positive 抓住局部异常、FSD 受整体语义迷惑”的案例之一。
```

## adm_conflict_priority_03

```text
case_id: adm_conflict_priority_03
sample_id: adm_auto_2875
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG

visual_observation:
图像主体是一只电子表或可穿戴设备，外壳轮廓、拍摄角度和光照基本合理，因此外观上接近商品图或设备近景照。问题集中在屏幕区域：显示内容像由多个数字、文字和图标拼接而成，但缺少真实界面应有的排版规则，字符彼此拥挤、尺度不一致，并夹杂明显不可读的伪文本；表盘周围的小标识也存在类似问题。也就是说，设备外壳本身足够自然，但一旦观察界面内容，就会迅速暴露出生成式拼装痕迹。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
屏幕中的数字、符号和文字排布缺乏真实设备界面的结构规则，属于明显的伪 UI / 伪文本异常。

key_evidence_2:
外壳自然、界面失真，这种“外部真实感强而内部语义细节崩坏”的组合非常符合高仿真生成样本特征。

paper_ready_summary:
`adm_conflict_priority_03` 进一步支持了方法互补性判断：当样本依赖伪文本、伪界面和局部语义组织异常暴露问题时，Stay-Positive 可能仍能给出 fake，而 FSD 三个版本则可能因为整体设备外观自然、纹理稳定而共同漏判。

human_takeaway:
这是第二个非常强的“整体自然外观掩盖局部伪文本/伪界面错误”的冲突案例。
```

## adm_conflict_priority_04

```text
case_id: adm_conflict_priority_04
sample_id: adm_auto_0355
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG

visual_observation:
图像像一只白色小型犬的室内照片，毛发、地毯和人物腿部的存在使其第一眼接近真实宠物抓拍。可疑点首先集中在狗脸区域，该处出现大块不自然的模糊/抹除效果，像是局部结构无法稳定生成后被直接涂抹；其次，狗的头身比例、腹部轮廓和四肢落点也略显僵硬，人物手部与主体之间的互动关系不够清晰。这张图并不是整张都“假”，而是局部修补感和结构含混感比较强。

judgement:
偏向 AI 生成图像，但置信度略低于前两个伪文本案例。

key_evidence_1:
脸部区域存在大块异常模糊，像是生成失败后的局部掩盖，而不是正常景深或运动模糊。

key_evidence_2:
宠物身体轮廓、肢体受力和人与狗的接触关系不够自然，局部结构存在连续性问题。

paper_ready_summary:
`adm_conflict_priority_04` 代表了另一类更接近真实抓拍的困难冲突样本：整体语义合理，但主体关键区域出现局部修补和结构含混。这类样本说明，FSD 的系统性盲区不只来自伪文本，也可能来自对“局部失败被整体自然感掩盖”的宠物/生活场景图像。

human_takeaway:
这是“整体像真实宠物照，但关键区域被局部修补掩盖”的强冲突案例。
```

## adm_conflict_priority_05

```text
case_id: adm_conflict_priority_05
sample_id: adm_auto_2984
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG

visual_observation:
图像呈现为室内客厅场景，电视、柜体、地毯、墙面挂件和门框共同构成了很完整的家庭环境语义，因此整体非常容易被判成真实图像。细看时可以发现若干不协调：电视与壁龛/柜体的嵌合关系略显生硬，墙面装饰和上方摆件存在轻微漂浮与间距失衡，右侧音箱和家具的透视关系也不完全统一。它不是依赖单一巨大错误暴露，而是通过一组轻度结构异常累积出“看久了不对劲”的感觉。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
多个室内物体之间的尺寸、对齐和嵌合关系不够稳定，体现为轻度但持续的空间几何异常。

key_evidence_2:
整体家居摄影语义非常自然，导致这些异常都被压缩成弱信号，容易造成模型之间的稳定分歧。

paper_ready_summary:
`adm_conflict_priority_05` 说明，除了伪文本和局部结构失败外，ADM strong-conflict 样本还包括“整体家居场景自然、但空间几何和物体摆放持续轻微失真”的类型。这类弱异常累积样本非常适合用于说明 FSD 在高自然度室内场景上的系统性漏判风险。

human_takeaway:
这是“没有明显单点大错，但多处弱异常叠加”的典型强冲突样本。
```

## 共性观察汇总

```text
common_observation_1:
这 5 个 strong-conflict 样本都具有很强的整体真实感，真实感来源包括低照度材质、商品拍摄视角、家庭室内场景和宠物抓拍语义。

common_observation_2:
它们的异常更多集中在局部结构逻辑、伪文本/伪界面、空间几何关系或局部修补感，而不是整张图全面崩坏。

common_observation_3:
这进一步说明 Stay-Positive 与 FSD 的差异不只是阈值问题，还可能涉及对局部异常模式和整体语义自然性的取证权重不同。

discussion_paragraph:
对第二批 5 个 ADM strong-conflict 样本的真实视觉观察表明，FSD 的系统性盲区并不只体现在单一类型错误上，而是覆盖了多种“整体很像真实、局部却不自洽”的高仿真样本。具体来看，`adm_conflict_priority_02` 和 `adm_conflict_priority_03` 主要暴露伪文本与伪界面问题，`adm_conflict_priority_01` 和 `adm_conflict_priority_05` 更像结构连接与空间几何异常，`adm_conflict_priority_04` 则表现为生活场景中的局部修补与主体结构含混。五个案例共同说明，Stay-Positive 在校准后仍能抓住一部分局部异常证据，而 FSD official、首轮微调和第二轮保守微调会在整体场景过于自然时同时漏判。这一现象为论文中的“方法互补性”和“FSD 在高自然度 ADM 样本上的系统性盲区”提供了更直接的案例支撑。
```
