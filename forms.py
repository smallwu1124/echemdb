from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectField, TextAreaField, DateTimeField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    affiliation = StringField('所属单位')
    submit = SubmitField('注册')


class ExperimentForm(FlaskForm):
    name = StringField('实验名称', validators=[DataRequired()])
    date_time = DateTimeField('日期时间', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    batch_id = StringField('批次号')
    
    # Reactor parameters
    cell_type = SelectField('反应器类型', choices=[
        ('', '请选择'), ('H型电解池', 'H型电解池'), ('单室坩埚', '单室坩埚'),
        ('微流控池', '微流控池'), ('三电极电池', '三电极电池'), ('其他', '其他')
    ])
    cell_volume = FloatField('反应器体积 (mL)', validators=[Optional()])
    separator = StringField('隔膜')
    
    # Electrode materials (text inputs for quick entry)
    we_material = StringField('工作电极材料', validators=[DataRequired()])
    we_area = FloatField('工作电极面积 (cm²)', validators=[Optional()])
    we_geometry = StringField('工作电极形貌')
    we_pretreatment = TextAreaField('工作电极预处理')
    re_type = StringField('参比电极类型')
    ce_material = StringField('对电极材料')
    
    # Solution parameters
    solvent = StringField('溶剂', validators=[DataRequired()])
    electrolyte = StringField('支持电解质')
    electrolyte_conc = FloatField('支持电解质浓度 (M)', validators=[Optional()])
    substrate = StringField('底物', validators=[DataRequired()])
    substrate_conc = FloatField('底物浓度 (M)', validators=[Optional()])
    ph = FloatField('pH', validators=[Optional(), NumberRange(min=0, max=14)])
    temperature = FloatField('温度 (℃)', validators=[Optional()])
    stirring_rpm = FloatField('搅拌速率 (rpm)', validators=[Optional()])
    atmosphere = StringField('气氛')
    feed_mode = SelectField('加料方式', choices=[
        ('', '请选择'), ('一次加入', '一次加入'), ('连续滴加', '连续滴加'),
        ('流动', '流动'), ('分次加入', '分次加入')
    ])
    feed_rate = FloatField('加料速率 (mL/min)', validators=[Optional()])
    
    # Electrochemical parameters
    electro_mode = SelectField('电化学模式', choices=[
        ('', '请选择'), ('恒电流', '恒电流'), ('恒电位', '恒电位'),
        ('线性扫描', '线性扫描'), ('循环伏安(CV)', '循环伏安(CV)'),
        ('EIS', 'EIS'), ('其他', '其他')
    ], validators=[DataRequired()])
    current = FloatField('电流 (A)', validators=[Optional()])
    potential = FloatField('电位 (V)', validators=[Optional()])
    scan_rate = FloatField('扫描速率 (mV/s)', validators=[Optional()])
    total_charge = FloatField('总电荷量 (C)', validators=[Optional()])
    duration = FloatField('实验时间', validators=[Optional()])
    duration_unit = SelectField('时间单位', choices=[('h', '小时'), ('s', '秒')], default='h')
    
    # Catalyst / additives
    catalyst = StringField('催化剂')
    catalyst_load = FloatField('催化剂负载 (mg)', validators=[Optional()])
    additives = StringField('添加剂')
    
    # Light parameters
    light_source = StringField('光源类型')
    light_intensity = FloatField('光照强度 (mW/cm²)', validators=[Optional()])
    light_duration = FloatField('光照时间 (s)', validators=[Optional()])
    
    # Measurement
    measurement_method = StringField('测量方法')
    sampling_rate = FloatField('采样频率 (Hz)', validators=[Optional()])
    analysis_method = StringField('产物分析方法')
    uncertainty = FloatField('不确定度 (%)', validators=[Optional()])
    
    # Other
    instrument_model = StringField('仪器型号')
    operator_name = StringField('操作人员')
    safety_info = TextAreaField('安全信息')
    waste_category = StringField('废弃物分类')
    notes = TextAreaField('备注')
    
    # SMILES for chemical structure (hidden, managed by molecule editor)
    smiles = StringField('SMILES / 结构式')
    substrate_smiles = StringField('原料 SMILES')
    product_smiles = StringField('产物 SMILES')
    reference_type = SelectField('参考来源', choices=[
        ('', '请选择'), ('literature', '文献 (Literature)'), ('patent', '专利 (Patent)'), ('none', '未公开 / 内部')
    ])
    doi = StringField('DOI')
    patent_number = StringField('专利号')
    
    submit = SubmitField('保存实验')


class AnalysisForm(FlaskForm):
    yield_pct = FloatField('产率 (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    selectivity = FloatField('选择性 (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    faraday_efficiency = FloatField('法拉第效率 (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    byproducts = TextAreaField('副反应/副产物')
    reproducibility_mean = FloatField('重复性均值', validators=[Optional()])
    reproducibility_std = FloatField('重复性标准差', validators=[Optional()])
    num_replicates = IntegerField('重复次数', default=1)
    anomalies = TextAreaField('异常事件')
    notes = TextAreaField('备注与结论')
    raw_data_path = StringField('原始数据文件路径')
    submit = SubmitField('保存分析结果')


class SearchForm(FlaskForm):
    we_material = StringField('工作电极材料')
    solvent = StringField('溶剂')
    substrate = StringField('底物')
    electrolyte = StringField('支持电解质')
    electro_mode = SelectField('电化学模式', choices=[
        ('', '全部'), ('恒电流', '恒电流'), ('恒电位', '恒电位'),
        ('线性扫描', '线性扫描'), ('循环伏安(CV)', '循环伏安(CV)'), ('EIS', 'EIS')
    ])
    ph_min = FloatField('pH 最小值', validators=[Optional()])
    ph_max = FloatField('pH 最大值', validators=[Optional()])
    temp_min = FloatField('温度最小值 (℃)', validators=[Optional()])
    temp_max = FloatField('温度最大值 (℃)', validators=[Optional()])
    keyword = StringField('关键词搜索')
    # SMILES structure search
    smiles = StringField('SMILES / 结构式')
    
    submit = SubmitField('搜索')


class ImportForm(FlaskForm):
    file = FileField('选择文件 (CSV/JSON)', validators=[DataRequired()])
    submit = SubmitField('导入数据')


class LiteratureForm(FlaskForm):
    title = StringField('标题/专利名', validators=[DataRequired(), Length(max=500)])
    authors = StringField('作者', validators=[Optional(), Length(max=1000)])
    journal = StringField('期刊/会议/来源', validators=[Optional(), Length(max=300)])
    year = IntegerField('年份', validators=[Optional()])
    volume = StringField('卷号', validators=[Optional(), Length(max=50)])
    issue = StringField('期号', validators=[Optional(), Length(max=50)])
    pages = StringField('页码', validators=[Optional(), Length(max=50)])
    doi = StringField('DOI', validators=[Optional(), Length(max=200)])
    patent_number = StringField('专利号', validators=[Optional(), Length(max=100)])
    literature_type = SelectField('文献类型', choices=[
        ('journal', '期刊 (Journal)'),
        ('patent', '专利 (Patent)'),
        ('review', '综述 (Review)'),
        ('conference', '会议 (Conference)'),
        ('book', '图书 (Book)')
    ], default='journal')
    abstract = TextAreaField('摘要', validators=[Optional()])
    keywords = StringField('关键词', validators=[Optional(), Length(max=500)])
    url = StringField('URL 链接', validators=[Optional(), Length(max=500)])
    research_field = StringField('研究领域', validators=[Optional(), Length(max=100)],
        description='如：CO2电还原, 有机电合成, HER')
    reaction_type = StringField('反应类型', validators=[Optional(), Length(max=100)],
        description='如：氧化, 还原, 交叉偶联')
    notes = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('保存')


class ReactionSearchForm(FlaskForm):
    reactant_smiles = StringField('反应物 SMILES', validators=[Optional()],
        description='输入反应物的化学结构式SMILES')
    product_smiles = StringField('产物 SMILES', validators=[Optional()],
        description='输入目标产物的化学结构式SMILES')
    we_material = StringField('工作电极材料', validators=[Optional()])
    solvent = StringField('溶剂', validators=[Optional()])
    electro_mode = SelectField('电化学模式', choices=[
        ('', '全部'), ('恒电流', '恒电流'), ('恒电位', '恒电位'),
        ('线性扫描', '线性扫描'), ('循环伏安(CV)', '循环伏安(CV)'), ('EIS', 'EIS')
    ])
    ph_min = FloatField('pH 最小值', validators=[Optional()])
    ph_max = FloatField('pH 最大值', validators=[Optional()])
    temp_min = FloatField('温度最小 (℃)', validators=[Optional()])
    temp_max = FloatField('温度最大 (℃)', validators=[Optional()])
    voltage_min = FloatField('电压最小 (V)', validators=[Optional()])
    voltage_max = FloatField('电压最大 (V)', validators=[Optional()])
    sim_threshold = FloatField('结构相似度阈值', default=0.3,
        validators=[Optional(), NumberRange(min=0, max=1)])
    keyword = StringField('关键词', validators=[Optional()])
    submit = SubmitField('搜索')
