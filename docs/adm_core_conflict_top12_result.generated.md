# ADM 冲突批次结果填写页

## adm_conflict_priority_01

```text
case_id: adm_conflict_priority_01
sample_id: adm_auto_2143
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/421_adm_153.PNG

visual_observation:
图像像是低照度环境下的设备底部或桌面结构近景，材质反光和整体明暗关系比较自然，因此第一眼不容易判假。但支撑件之间的连接与透视明显不稳定，左侧与右侧杆件像是各自成立、彼此却没有统一空间关系，背景高亮区域也缺少明确来源。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
杆件与支撑件之间的连接关系和透视方向不够自洽。

key_evidence_2:
低照度和反光制造了真实感，但局部边缘存在漂浮与软化现象。

paper_ready_summary:
这是一类依赖低照度材质与近景构图掩盖局部结构逻辑错误的高仿真冲突样本。

human_takeaway:
整体像真实工业近景，但局部结构关系站不住。
```

## adm_conflict_priority_02

```text
case_id: adm_conflict_priority_02
sample_id: adm_auto_2720
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/508_adm_174.PNG

visual_observation:
图像像一组老旧按键或键盘的特写，材质磨损、斜向构图和景深都很像真实拍摄。但按键上的符号明显不是稳定的真实文字系统，而是由伪字符和扭曲记号拼出来的，个别字符与按键表面的贴合关系也不稳定。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
按键字符是非常典型的伪文本异常。

key_evidence_2:
字符刻印与按键表面的几何关系不稳定，存在漂浮和扭曲感。

paper_ready_summary:
这类样本说明局部伪文本信号已经足够强，但 FSD 三个版本仍会被整体摄影感误导。

human_takeaway:
整体很真，文字最假。
```

## adm_conflict_priority_03

```text
case_id: adm_conflict_priority_03
sample_id: adm_auto_2875
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/531_adm_153.PNG

visual_observation:
图像主体像一只电子表或穿戴设备，外壳轮廓、角度与灯光都较自然，接近产品图。真正异常集中在屏幕与表盘标识上：数字、符号和文字排布拥挤而无规则，存在明显不可读的伪界面与伪文本。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
屏幕内容缺少真实设备界面的排版与语义规则。

key_evidence_2:
表盘周围小标识同样存在伪文字与结构混乱问题。

paper_ready_summary:
这类样本是“外壳真实感强、界面语义失败”的代表，支持方法之间对局部语义异常取证权重不同的判断。

human_takeaway:
设备外观能骗过人，界面内容骗不过细看。
```

## adm_conflict_priority_04

```text
case_id: adm_conflict_priority_04
sample_id: adm_auto_0355
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/153_adm_153.PNG

visual_observation:
图像像一只白色小型犬的室内抓拍，整体语义和环境都自然，毛发与地毯也不是整片崩坏。可疑点在于狗脸区域出现明显不自然的模糊/抹除感，像是局部生成失败后的修补，同时身体轮廓和人与狗的接触关系也有轻微僵硬。

judgement:
偏向 AI 生成图像。

key_evidence_1:
脸部区域的异常模糊不像正常景深，更像局部修补。

key_evidence_2:
头身比例和肢体落点略显含混，结构连续性不足。

paper_ready_summary:
这是一类在生活场景中通过局部修补掩盖失败区域的困难样本，容易被整体自然感遮蔽。

human_takeaway:
关键错误不大，但恰好藏在最该清楚的区域。
```

## adm_conflict_priority_05

```text
case_id: adm_conflict_priority_05
sample_id: adm_auto_2984
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/548_adm_174.PNG

visual_observation:
图像呈现完整的室内客厅场景，电视、柜体、墙面装饰和门框共同构成很强的家庭环境真实感。问题不是单个巨大错误，而是多个轻度不协调同时出现，例如电视与柜体嵌合关系略生硬，摆件与墙面装饰存在轻微漂浮感，几何对齐也不够稳定。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
物体之间的对齐、嵌合和空间几何关系持续存在轻度失真。

key_evidence_2:
整体家居语义自然，导致这些异常被压缩成弱但持续的信号。

paper_ready_summary:
这类样本说明 FSD 在高自然度室内场景上可能系统性低估“多处弱异常累积”的风险。

human_takeaway:
没有单点大错，但越看越不对。
```

## adm_conflict_priority_06

```text
case_id: adm_conflict_priority_06
sample_id: adm_auto_1421
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/312_adm_85.PNG

visual_observation:
图像像一只昆虫停在叶片上的微距照片，色彩、景深和叶片纹理都很像自然摄影。细看昆虫身体时，会发现头胸腹的衔接略显拼接，腿部细节与着力关系不够清楚，翅膀边缘也带有轻微不自然的融合感。

judgement:
偏向 AI 生成图像，但置信度中等。

key_evidence_1:
昆虫身体分段和腿部连接缺少真实标本或微距摄影应有的精细结构感。

key_evidence_2:
翅膀边缘与身体衔接处存在轻度融合与模糊。

paper_ready_summary:
这类微距昆虫样本说明，即便不存在伪文本，局部生物结构异常仍可能被 Stay-Positive 捕捉，而被 FSD 共同漏掉。

human_takeaway:
整体是“真昆虫照片”的样子，但结构细看不够真。
```

## adm_conflict_priority_07

```text
case_id: adm_conflict_priority_07
sample_id: adm_auto_1390
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/308_adm_7.PNG

visual_observation:
图像像一只竹节虫或细长昆虫的极简背景拍摄，主体细长、背景虚化和光线都较自然。异常主要在肢体连接和轮廓连续性上：几根细腿像是从不同方向生长出来，关节关系不够明确，身体中段与末端也带有轻微拉伸感。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
细长肢体的关节与连接方向缺乏真实生物结构的一致性。

key_evidence_2:
主体轮廓过于平滑，局部细节像是被拉伸和简化过。

paper_ready_summary:
这类样本说明 FSD 在细长生物体的局部结构约束上也可能存在稳定盲区。

human_takeaway:
远看像标本，近看像拼出来的。
```

## adm_conflict_priority_08

```text
case_id: adm_conflict_priority_08
sample_id: adm_auto_1383
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/307_adm_34.PNG

visual_observation:
图像像一只绿色昆虫俯拍在地面上，整体构图稳定，颜色和阴影关系合理。可疑点在于昆虫前部触角与腿部的细节组织不够清晰，头胸连接带有轻微错位，身体与背景接触边界也不是完全自然。

judgement:
偏向 AI 生成图像，但属于更边界的样本。

key_evidence_1:
昆虫前端触角、足部和身体连接关系不够精确。

key_evidence_2:
主体边缘与地面接触处存在轻微融合和不干净的轮廓。

paper_ready_summary:
这类边界样本表明，即使整体摄影几乎无明显破绽，细粒度生物结构仍能暴露稳定的可疑信号。

human_takeaway:
这是更接近真实但仍留有细节破绽的一类。
```

## adm_conflict_priority_09

```text
case_id: adm_conflict_priority_09
sample_id: adm_auto_0280
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/141_adm_7.PNG

visual_observation:
图像主体是一只站在木桩上的鸟，背景虚化、姿态和色彩都非常接近真实野生动物摄影。问题在于鸟体腹部花纹与羽毛层次略显平滑，腿部和脚爪与木桩接触关系不够扎实，整体显得“非常像真图但少了一点真实羽毛结构”。

judgement:
偏向 AI 生成图像，但置信度低于伪文本样本。

key_evidence_1:
羽毛层次与腹部纹理略显过度平整。

key_evidence_2:
脚爪与木桩的接触感和受力感不足。

paper_ready_summary:
这类鸟类单体样本说明，高自然度生物摄影中最难的部分不在整体语义，而在局部羽毛和接触关系的真实性。

human_takeaway:
第一眼像真鸟照，问题主要藏在结构触点。
```

## adm_conflict_priority_10

```text
case_id: adm_conflict_priority_10
sample_id: adm_auto_2252
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/438_adm_174.PNG

visual_observation:
图像是一座高耸建筑的仰拍场景，天空、透视和主体轮廓整体成立，第一眼接近真实城市摄影。但建筑立面纹理和窗格细节存在轻微重复与僵硬感，塔体不同层级的几何过渡不够自然，右侧背景建筑也略带拼接感。

judgement:
更倾向 AI 生成图像。

key_evidence_1:
立面纹理、窗格和几何过渡不够自然，带有生成式重复感。

key_evidence_2:
主建筑与右侧背景建筑之间的空间关系略显拼接。

paper_ready_summary:
这类建筑样本表明，FSD 在高层建筑仰拍图像中也可能被全局透视成立所误导，而忽略局部立面结构异常。

human_takeaway:
透视看着真，但立面细节不够像真实建筑。
```

## adm_conflict_priority_11

```text
case_id: adm_conflict_priority_11
sample_id: adm_auto_1438
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/315_adm_7.PNG

visual_observation:
图像像一只透明翅昆虫的正面微距照，色彩、景深和对称构图很有真实生态摄影感。异常主要集中在头部与胸部的衔接和翅膀对称性上，两侧翅脉虽近似对称，但细节略显机械化，头部结构也有些过度光滑。

judgement:
偏向 AI 生成图像。

key_evidence_1:
头胸连接与面部细节略显简化和过度平滑。

key_evidence_2:
翅膀对称得过于规整，但局部翅脉细节不够自然。

paper_ready_summary:
这类昆虫正面微距样本支持一个判断：当图像整体依赖高度对称和浅景深制造真实感时，FSD 可能更容易忽略局部结构“过于整齐”的生成痕迹。

human_takeaway:
对称构图很真，但细节真得不够自然。
```

## adm_conflict_priority_12

```text
case_id: adm_conflict_priority_12
sample_id: adm_auto_2693
image_path: /net/8k3/e0fs01/users/xj62kv/260402_AI-image-forgery-recognition/data/GenImage/ADM/val/ai/503_adm_85.PNG

visual_observation:
图像像一只浅绿色昆虫停在叶片上的微距照，整体颜色、背景虚化和主体姿态都相当自然。细看后可见头部、触角和翅膀前缘的关系不够清楚，身体表面还有轻微发光和过度平滑感，像是生成模型把真实昆虫纹理“抹亮”了。

judgement:
偏向 AI 生成图像。

key_evidence_1:
头部、触角和翅膀前缘之间的结构边界不够干净。

key_evidence_2:
主体表面存在轻微不自然的发亮和平滑感。

paper_ready_summary:
这类样本说明，昆虫微距图像中的高质量背景虚化并不能掩盖主体结构边界和材质表达上的生成痕迹。

human_takeaway:
背景和姿态都真，问题出在主体边界和材质质感。
```
