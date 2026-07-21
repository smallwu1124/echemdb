from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    affiliation = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')  # 'user', 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    experiments = db.relationship('Experiment', backref='operator', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Instrument(db.Model):
    __tablename__ = 'instrument'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    notes = db.Column(db.Text)

    experiments = db.relationship('Experiment', backref='instrument', lazy='dynamic')


class Electrode(db.Model):
    __tablename__ = 'electrode'
    id = db.Column(db.Integer, primary_key=True)
    electrode_type = db.Column(db.String(20), nullable=False)  # 'WE', 'CE', 'RE'
    material = db.Column(db.String(100), nullable=False, index=True)
    geometry = db.Column(db.String(100))
    area = db.Column(db.Float)  # cm²
    pretreatment = db.Column(db.Text)
    notes = db.Column(db.Text)


class Electrolyte(db.Model):
    __tablename__ = 'electrolyte'
    id = db.Column(db.Integer, primary_key=True)
    solvent = db.Column(db.String(100), nullable=False, index=True)
    supporting_salt = db.Column(db.String(100), index=True)
    concentration = db.Column(db.Float)  # M
    ph = db.Column(db.Float)
    buffer = db.Column(db.String(100))
    notes = db.Column(db.Text)


class Sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    cas_number = db.Column(db.String(50))
    formula = db.Column(db.String(100))
    concentration = db.Column(db.Float)  # M
    purity = db.Column(db.Float)  # percentage
    supplier = db.Column(db.String(200))
    notes = db.Column(db.Text)


# Association tables for many-to-many relationships
experiment_electrode = db.Table('experiment_electrode',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), primary_key=True),
    db.Column('electrode_id', db.Integer, db.ForeignKey('electrode.id'), primary_key=True),
    db.Column('function', db.String(20))  # 'WE', 'CE', 'RE'
)

experiment_electrolyte = db.Table('experiment_electrolyte',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), primary_key=True),
    db.Column('electrolyte_id', db.Integer, db.ForeignKey('electrolyte.id'), primary_key=True)
)

experiment_sample = db.Table('experiment_sample',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), primary_key=True),
    db.Column('sample_id', db.Integer, db.ForeignKey('sample.id'), primary_key=True),
    db.Column('role', db.String(50))  # 'substrate', 'catalyst', 'additive'
)


class Experiment(db.Model):
    __tablename__ = 'experiment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    date_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    batch_id = db.Column(db.String(50), index=True)
    
    # Reactor parameters
    cell_type = db.Column(db.String(100))
    cell_volume = db.Column(db.Float)  # mL
    separator = db.Column(db.String(100))
    electrode_geometry = db.Column(db.String(100))
    
    # Solution parameters
    ph = db.Column(db.Float)
    temperature = db.Column(db.Float)  # Celsius
    stirring_rpm = db.Column(db.Float)
    atmosphere = db.Column(db.String(100))
    feed_mode = db.Column(db.String(50))
    feed_rate = db.Column(db.Float)  # mL/min
    
    # Electrochemical parameters
    electro_mode = db.Column(db.String(50), nullable=False)  # '恒电流', '恒电位', '线性扫描', 'CV', 'EIS', etc.
    current = db.Column(db.Float)  # A
    potential = db.Column(db.Float)  # V
    scan_rate = db.Column(db.Float)  # mV/s
    total_charge = db.Column(db.Float)  # C
    duration = db.Column(db.Float)  # hours or seconds
    duration_unit = db.Column(db.String(10), default='h')  # 'h' or 's'
    
    # Light parameters
    light_source = db.Column(db.String(100))
    light_intensity = db.Column(db.Float)  # mW/cm²
    light_duration = db.Column(db.Float)  # s
    
    # Measurement parameters
    measurement_method = db.Column(db.String(100))
    sampling_rate = db.Column(db.Float)  # Hz
    analysis_method = db.Column(db.String(100))
    uncertainty = db.Column(db.Float)  # percentage
    
    # Safety & other
    safety_info = db.Column(db.Text)
    waste_category = db.Column(db.String(100))
    equipment_model = db.Column(db.String(100))
    operator_name = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    # SMILES for chemical structure
    smiles = db.Column(db.String(500), index=True)
    substrate_smiles = db.Column(db.String(500), index=True)
    product_smiles = db.Column(db.String(500), index=True)
    reference_type = db.Column(db.String(20))  # 'literature', 'patent', 'none'
    doi = db.Column(db.String(200))
    patent_number = db.Column(db.String(100))
    
    # SMILES for chemical structure
    smiles = db.Column(db.String(500), index=True)
    
    # Version control
    version = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    electrodes = db.relationship('Electrode', secondary=experiment_electrode, lazy='subquery',
        backref=db.backref('experiments', lazy=True))
    electrolytes = db.relationship('Electrolyte', secondary=experiment_electrolyte, lazy='subquery',
        backref=db.backref('experiments', lazy=True))
    samples = db.relationship('Sample', secondary=experiment_sample, lazy='subquery',
        backref=db.backref('experiments', lazy=True))
    analyses = db.relationship('Analysis', backref='experiment', lazy='dynamic')


class Analysis(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False)
    
    # Experiment conclusions
    yield_pct = db.Column(db.Float)  # 产率 (%)
    selectivity = db.Column(db.Float)  # 选择性 (%)
    faraday_efficiency = db.Column(db.Float)  # 法拉第效率 (%)
    byproducts = db.Column(db.Text)  # 副反应/副产物
    reproducibility_mean = db.Column(db.Float)  # 重复性均值
    reproducibility_std = db.Column(db.Float)  # 重复性标准差
    reproducibility_rsd = db.Column(db.Float)  # 相对标准偏差 (%)
    num_replicates = db.Column(db.Integer, default=1)  # 重复次数
    anomalies = db.Column(db.Text)  # 异常事件
    notes = db.Column(db.Text)  # 备注与结论
    
    # Raw data reference
    raw_data_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # 'CREATE', 'UPDATE', 'DELETE', 'VIEW'
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)


#
# Association: Literature <-> Experiment
#
literature_experiment = db.Table('literature_experiment',
    db.Column('literature_id', db.Integer, db.ForeignKey('literature.id'), primary_key=True),
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), primary_key=True)
)


class Literature(db.Model):
    """管理文献期刊和专利引用"""
    __tablename__ = 'literature'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    authors = db.Column(db.String(1000))
    journal = db.Column(db.String(300))
    year = db.Column(db.Integer, index=True)
    volume = db.Column(db.String(50))
    issue = db.Column(db.String(50))
    pages = db.Column(db.String(50))
    doi = db.Column(db.String(200), unique=True, index=True)
    patent_number = db.Column(db.String(100), index=True)
    literature_type = db.Column(db.String(20), default='journal', index=True)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(500))
    url = db.Column(db.String(500))
    research_field = db.Column(db.String(100))
    reaction_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    experiments = db.relationship('Experiment', secondary=literature_experiment, lazy='subquery',
                                  backref=db.backref('literature_refs', lazy=True))
    operator = db.relationship('User', backref='literature_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'journal': self.journal,
            'year': self.year,
            'doi': self.doi,
            'patent_number': self.patent_number,
            'type': self.literature_type,
            'reaction_type': self.reaction_type,
            'keywords': self.keywords,
        }


class ReactionFingerprint(db.Model):
    """缓存指纹向量加速相似性搜索"""
    __tablename__ = 'reaction_fingerprint'
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False, unique=True)
    reactant_fp = db.Column(db.Text)
    product_fp = db.Column(db.Text)
    combined_fp = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    experiment = db.relationship('Experiment', backref=db.backref('fingerprint', uselist=False))
