"""
arXiv 学科分类常量
"""
from typing import Dict, List

# arXiv 主要学科分类
ARXIV_CATEGORIES = {
    # Computer Science - 计算机科学
    "cs.AI": "Artificial Intelligence - 人工智能",
    "cs.AR": "Hardware Architecture - 硬件架构", 
    "cs.CC": "Computational Complexity - 计算复杂性",
    "cs.CE": "Computational Engineering, Finance, and Science - 计算工程、金融和科学",
    "cs.CG": "Computational Geometry - 计算几何",
    "cs.CL": "Computation and Language - 计算与语言",
    "cs.CR": "Cryptography and Security - 密码学与安全",
    "cs.CV": "Computer Vision and Pattern Recognition - 计算机视觉与模式识别",
    "cs.CY": "Computers and Society - 计算机与社会",
    "cs.DB": "Databases - 数据库",
    "cs.DC": "Distributed, Parallel, and Cluster Computing - 分布式、并行和集群计算",
    "cs.DL": "Digital Libraries - 数字图书馆",
    "cs.DM": "Discrete Mathematics - 离散数学",
    "cs.DS": "Data Structures and Algorithms - 数据结构与算法",
    "cs.ET": "Emerging Technologies - 新兴技术",
    "cs.FL": "Formal Languages and Automata Theory - 形式语言与自动机理论",
    "cs.GL": "General Literature - 综合文献",
    "cs.GR": "Graphics - 图形学",
    "cs.GT": "Computer Science and Game Theory - 计算机科学与博弈论",
    "cs.HC": "Human-Computer Interaction - 人机交互",
    "cs.IR": "Information Retrieval - 信息检索",
    "cs.IT": "Information Theory - 信息论",
    "cs.LG": "Machine Learning - 机器学习",
    "cs.LO": "Logic in Computer Science - 计算机科学中的逻辑",
    "cs.MA": "Multiagent Systems - 多智能体系统",
    "cs.MM": "Multimedia - 多媒体",
    "cs.MS": "Mathematical Software - 数学软件",
    "cs.NA": "Numerical Analysis - 数值分析",
    "cs.NE": "Neural and Evolutionary Computing - 神经与进化计算",
    "cs.NI": "Networking and Internet Architecture - 网络与互联网架构",
    "cs.OH": "Other Computer Science - 其他计算机科学",
    "cs.OS": "Operating Systems - 操作系统",
    "cs.PF": "Performance - 性能",
    "cs.PL": "Programming Languages - 编程语言",
    "cs.RO": "Robotics - 机器人学",
    "cs.SC": "Symbolic Computation - 符号计算",
    "cs.SD": "Sound - 声音",
    "cs.SE": "Software Engineering - 软件工程",
    "cs.SI": "Social and Information Networks - 社交与信息网络",
    "cs.SY": "Systems and Control - 系统与控制",
    
    # Economics - 经济学
    "econ.EM": "Econometrics - 计量经济学",
    "econ.GN": "General Economics - 一般经济学",
    "econ.TH": "Theoretical Economics - 理论经济学",
    
    # Electrical Engineering and Systems Science - 电气工程与系统科学
    "eess.AS": "Audio and Speech Processing - 音频与语音处理",
    "eess.IV": "Image and Video Processing - 图像与视频处理",
    "eess.SP": "Signal Processing - 信号处理",
    "eess.SY": "Systems and Control - 系统与控制",
    
    # Mathematics - 数学
    "math.AC": "Commutative Algebra - 交换代数",
    "math.AG": "Algebraic Geometry - 代数几何",
    "math.AP": "Analysis of PDEs - 偏微分方程分析",
    "math.AT": "Algebraic Topology - 代数拓扑",
    "math.CA": "Classical Analysis and ODEs - 经典分析与常微分方程",
    "math.CO": "Combinatorics - 组合数学",
    "math.CT": "Category Theory - 范畴论",
    "math.CV": "Complex Variables - 复变函数",
    "math.DG": "Differential Geometry - 微分几何",
    "math.DS": "Dynamical Systems - 动力系统",
    "math.FA": "Functional Analysis - 泛函分析",
    "math.GM": "General Mathematics - 一般数学",
    "math.GN": "General Topology - 一般拓扑",
    "math.GR": "Group Theory - 群论",
    "math.GT": "Geometric Topology - 几何拓扑",
    "math.HO": "History and Overview - 历史与概述",
    "math.IT": "Information Theory - 信息论",
    "math.KT": "K-Theory and Homology - K理论与同调",
    "math.LO": "Logic - 逻辑",
    "math.MG": "Metric Geometry - 度量几何",
    "math.MP": "Mathematical Physics - 数学物理",
    "math.NA": "Numerical Analysis - 数值分析",
    "math.NT": "Number Theory - 数论",
    "math.OA": "Operator Algebras - 算子代数",
    "math.OC": "Optimization and Control - 优化与控制",
    "math.PR": "Probability - 概率论",
    "math.QA": "Quantum Algebra - 量子代数",
    "math.RA": "Rings and Algebras - 环与代数",
    "math.RT": "Representation Theory - 表示论",
    "math.SG": "Symplectic Geometry - 辛几何",
    "math.SP": "Spectral Theory - 谱理论",
    "math.ST": "Statistics Theory - 统计理论",
    
    # Physics - 物理学
    "physics.acc-ph": "Accelerator Physics - 加速器物理",
    "physics.ao-ph": "Atmospheric and Oceanic Physics - 大气与海洋物理",
    "physics.app-ph": "Applied Physics - 应用物理",
    "physics.atm-clus": "Atomic and Molecular Clusters - 原子与分子簇",
    "physics.atom-ph": "Atomic Physics - 原子物理",
    "physics.bio-ph": "Biological Physics - 生物物理",
    "physics.chem-ph": "Chemical Physics - 化学物理",
    "physics.class-ph": "Classical Physics - 经典物理",
    "physics.comp-ph": "Computational Physics - 计算物理",
    "physics.data-an": "Data Analysis, Statistics and Probability - 数据分析、统计与概率",
    "physics.ed-ph": "Physics Education - 物理教育",
    "physics.flu-dyn": "Fluid Dynamics - 流体动力学",
    "physics.gen-ph": "General Physics - 一般物理",
    "physics.geo-ph": "Geophysics - 地球物理",
    "physics.hist-ph": "History and Philosophy of Physics - 物理学史与哲学",
    "physics.ins-det": "Instrumentation and Detectors - 仪器与探测器",
    "physics.med-ph": "Medical Physics - 医学物理",
    "physics.optics": "Optics - 光学",
    "physics.plasm-ph": "Plasma Physics - 等离子体物理",
    "physics.pop-ph": "Popular Physics - 科普物理",
    "physics.soc-ph": "Physics and Society - 物理与社会",
    "physics.space-ph": "Space Physics - 空间物理",
    
    # Quantitative Biology - 定量生物学
    "q-bio.BM": "Biomolecules - 生物大分子",
    "q-bio.CB": "Cell Behavior - 细胞行为",
    "q-bio.GN": "Genomics - 基因组学",
    "q-bio.MN": "Molecular Networks - 分子网络",
    "q-bio.NC": "Neurons and Cognition - 神经与认知",
    "q-bio.OT": "Other Quantitative Biology - 其他定量生物学",
    "q-bio.PE": "Populations and Evolution - 种群与进化",
    "q-bio.QM": "Quantitative Methods - 定量方法",
    "q-bio.SC": "Subcellular Processes - 亚细胞过程",
    "q-bio.TO": "Tissues and Organs - 组织与器官",
    
    # Quantitative Finance - 定量金融
    "q-fin.CP": "Computational Finance - 计算金融",
    "q-fin.EC": "Economics - 经济学",
    "q-fin.GN": "General Finance - 一般金融",
    "q-fin.MF": "Mathematical Finance - 数学金融",
    "q-fin.PM": "Portfolio Management - 投资组合管理",
    "q-fin.PR": "Pricing of Securities - 证券定价",
    "q-fin.RM": "Risk Management - 风险管理",
    "q-fin.ST": "Statistical Finance - 统计金融",
    "q-fin.TR": "Trading and Market Microstructure - 交易与市场微观结构",
    
    # Statistics - 统计学
    "stat.AP": "Applications - 应用统计",
    "stat.CO": "Computation - 计算统计",
    "stat.ME": "Methodology - 统计方法",
    "stat.ML": "Machine Learning - 机器学习",
    "stat.OT": "Other Statistics - 其他统计",
    "stat.TH": "Statistics Theory - 统计理论",
}

# 按主学科分组
CATEGORY_GROUPS = {
    "Computer Science": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("cs.")],
    "Economics": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("econ.")],
    "Electrical Engineering": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("eess.")],
    "Mathematics": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("math.")],
    "Physics": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("physics.")],
    "Quantitative Biology": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("q-bio.")],
    "Quantitative Finance": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("q-fin.")],
    "Statistics": [cat for cat in ARXIV_CATEGORIES.keys() if cat.startswith("stat.")],
}

# 常用的计算机科学分类
POPULAR_CS_CATEGORIES = [
    "cs.AI",  # 人工智能
    "cs.LG",  # 机器学习
    "cs.CL",  # 计算语言学
    "cs.CV",  # 计算机视觉
    "cs.RO",  # 机器人学
    "cs.IR",  # 信息检索
    "cs.DB",  # 数据库
    "cs.DS",  # 数据结构与算法
    "cs.SE",  # 软件工程
    "cs.NI",  # 网络架构
]

def validate_category(category: str) -> bool:
    """验证分类代码是否有效"""
    return category in ARXIV_CATEGORIES

def get_category_description(category: str) -> str:
    """获取分类的描述"""
    return ARXIV_CATEGORIES.get(category, f"Unknown category: {category}")

def search_categories_by_keyword(keyword: str) -> List[str]:
    """根据关键词搜索相关分类"""
    keyword = keyword.lower()
    matching_categories = []
    
    for cat_code, description in ARXIV_CATEGORIES.items():
        if keyword in description.lower() or keyword in cat_code.lower():
            matching_categories.append(cat_code)
    
    return matching_categories

def get_categories_by_group(group: str) -> List[str]:
    """获取指定组的所有分类"""
    return CATEGORY_GROUPS.get(group, [])
