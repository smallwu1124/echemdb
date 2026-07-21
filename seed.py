# -*- coding: utf-8 -*-
"""Seed the database with sample data from the document examples."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime, timezone
from app import app
from models import db, User, Experiment, Electrode, Electrolyte, Sample, Instrument, Analysis
from models import experiment_electrode, experiment_electrolyte, experiment_sample


def seed():
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if User.query.count() > 0:
            print('Database already seeded, skipping.')
            return
        
        # Create admin user
        admin = User(username='admin', email='admin@ecdb.local', affiliation='电化学实验室')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create demo users
        zhang = User(username='张三', email='zhang@ecdb.local', affiliation='电化学实验室A组')
        zhang.set_password('123456')
        db.session.add(zhang)
        
        li = User(username='李四', email='li@ecdb.local', affiliation='电化学实验室B组')
        li.set_password('123456')
        db.session.add(li)
        
        wang = User(username='王五', email='wang@ecdb.local', affiliation='电化学实验室C组')
        wang.set_password('123456')
        db.session.add(wang)
        
        db.session.flush()
        
        # Create instrument
        inst = Instrument(model='CHI660E', manufacturer='上海辰华仪器', serial_number='CHI-2024-001')
        db.session.add(inst)
        db.session.flush()
        instr_id = inst.id
        
        # ========== Example 1: HER Hydrogen Evolution ==========
        exp1 = Experiment(
            name='HER产氢测试 — 水电解制氢',
            date_time=datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc),
            user_id=zhang.id,
            instrument_id=instr_id,
            batch_id='BATCH-2026-001',
            ph=13.0,
            temperature=25.0,
            stirring_rpm=600,
            atmosphere='氩气惰性保护 (Ar)',
            cell_type='H型电解池',
            cell_volume=100.0,
            separator='Nafion 117',
            electro_mode='恒电流',
            current=0.1,
            total_charge=360.0,
            duration=6.0,
            duration_unit='h',
            equipment_model='CHI660E',
            operator_name='张三'
        )
        db.session.add(exp1)
        db.session.flush()
        
        # WE
        we1 = Electrode(electrode_type='WE', material='Ni泡沫', geometry='泡沫状', area=1.0,
                        pretreatment='机械抛光 + 超声清洗')
        db.session.add(we1)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp1.id, electrode_id=we1.id, function='WE'))
        
        # RE
        re1 = Electrode(electrode_type='RE', material='Ag/AgCl (KCl饱和)')
        db.session.add(re1)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp1.id, electrode_id=re1.id, function='RE'))
        
        # CE
        ce1 = Electrode(electrode_type='CE', material='Ni泡沫')
        db.session.add(ce1)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp1.id, electrode_id=ce1.id, function='CE'))
        
        # Electrolyte
        elec1 = Electrolyte(solvent='1.0 M KOH水溶液', supporting_salt='KOH', concentration=1.0, ph=13.0)
        db.session.add(elec1)
        db.session.flush()
        db.session.execute(experiment_electrolyte.insert().values(
            experiment_id=exp1.id, electrolyte_id=elec1.id))
        
        # Sample (substrate)
        samp1 = Sample(name='纯水 (H2O)', concentration=55.5)
        db.session.add(samp1)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp1.id, sample_id=samp1.id, role='substrate'))
        
        # Sample (catalyst)
        samp_cat1 = Sample(name='NiMo合金', concentration=5.0)
        db.session.add(samp_cat1)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp1.id, sample_id=samp_cat1.id, role='catalyst'))
        
        # Analysis for exp1
        analysis1 = Analysis(
            experiment_id=exp1.id,
            yield_pct=85.0,
            faraday_efficiency=92.0,
            selectivity=95.0,
            byproducts='未检测到明显副产物',
            reproducibility_mean=85.0,
            reproducibility_std=3.5,
            num_replicates=3,
            reproducibility_rsd=4.12,
            notes='NiMo合金在碱性条件下表现出优异的HER性能，FE达92%。'
        )
        db.session.add(analysis1)
        
        # ========== Example 2: CO2 Reduction ==========
        exp2 = Experiment(
            name='CO₂还原产乙烯',
            date_time=datetime(2026, 7, 2, 14, 30, tzinfo=timezone.utc),
            user_id=li.id,
            instrument_id=instr_id,
            batch_id='BATCH-2026-002',
            ph=6.8,
            temperature=25.0,
            stirring_rpm=600,
            atmosphere='CO₂持续通入 (20 mL/min)',
            cell_type='H型电解池',
            cell_volume=100.0,
            separator='Nafion 117',
            electro_mode='线性扫描',
            potential=-1.0,
            scan_rate=50.0,
            duration=1.0,
            duration_unit='h',
            equipment_model='CHI660E',
            operator_name='李四'
        )
        db.session.add(exp2)
        db.session.flush()
        
        # WE
        we2 = Electrode(electrode_type='WE', material='铜箔', area=0.5,
                        pretreatment='化学刻蚀 (CuSO₄溶液)')
        db.session.add(we2)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp2.id, electrode_id=we2.id, function='WE'))
        
        # RE
        re2 = Electrode(electrode_type='RE', material='Ag/AgCl (KCl饱和)')
        db.session.add(re2)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp2.id, electrode_id=re2.id, function='RE'))
        
        # CE
        ce2 = Electrode(electrode_type='CE', material='铂片')
        db.session.add(ce2)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp2.id, electrode_id=ce2.id, function='CE'))
        
        # Electrolyte
        elec2 = Electrolyte(solvent='0.1 M KHCO₃水溶液', supporting_salt='KHCO₃', concentration=0.1, ph=6.8)
        db.session.add(elec2)
        db.session.flush()
        db.session.execute(experiment_electrolyte.insert().values(
            experiment_id=exp2.id, electrolyte_id=elec2.id))
        
        # Sample
        samp2 = Sample(name='CO₂ (饱和)', concentration=0.033)
        db.session.add(samp2)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp2.id, sample_id=samp2.id, role='substrate'))
        
        # Catalyst
        samp_cat2 = Sample(name='Cu纳米颗粒', concentration=1.0)
        db.session.add(samp_cat2)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp2.id, sample_id=samp_cat2.id, role='catalyst'))
        
        # Analysis
        analysis2 = Analysis(
            experiment_id=exp2.id,
            yield_pct=45.0,
            faraday_efficiency=60.0,
            selectivity=55.0,
            byproducts='H₂, CH₄, CO',
            reproducibility_mean=45.0,
            reproducibility_std=5.2,
            num_replicates=3,
            reproducibility_rsd=11.56,
            notes='铜电极可有效将CO₂还原为乙烯，但FE待优化，氢气为竞争副反应。'
        )
        db.session.add(analysis2)
        
        # ========== Example 3: Organic Synthesis ==========
        exp3 = Experiment(
            name='苯磺酰胺氧化合成',
            date_time=datetime(2026, 7, 3, 9, 0, tzinfo=timezone.utc),
            user_id=wang.id,
            instrument_id=instr_id,
            batch_id='BATCH-2026-003',
            ph=7.0,
            temperature=25.0,
            stirring_rpm=0,
            atmosphere='氩气惰性保护',
            cell_type='单室玻璃瓶',
            cell_volume=50.0,
            electro_mode='恒电位',
            potential=-2.0,
            total_charge=200.0,
            duration=1.5,
            duration_unit='h',
            light_source='LED 365 nm',
            light_intensity=50.0,
            light_duration=5400.0,
            equipment_model='CHI660E',
            operator_name='王五'
        )
        db.session.add(exp3)
        db.session.flush()
        
        # WE
        we3 = Electrode(electrode_type='WE', material='石墨烯沉积Pt', area=1.0,
                        pretreatment='热处理 + 表面修饰')
        db.session.add(we3)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp3.id, electrode_id=we3.id, function='WE'))
        
        # RE
        re3 = Electrode(electrode_type='RE', material='Ag/AgCl (KCl饱和)')
        db.session.add(re3)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp3.id, electrode_id=re3.id, function='RE'))
        
        # CE
        ce3 = Electrode(electrode_type='CE', material='铂片')
        db.session.add(ce3)
        db.session.flush()
        db.session.execute(experiment_electrode.insert().values(
            experiment_id=exp3.id, electrode_id=ce3.id, function='CE'))
        
        # Electrolyte
        elec3 = Electrolyte(solvent='MeCN (乙腈)', supporting_salt='TBAPF₆', concentration=0.1, ph=7.0)
        db.session.add(elec3)
        db.session.flush()
        db.session.execute(experiment_electrolyte.insert().values(
            experiment_id=exp3.id, electrolyte_id=elec3.id))
        
        # Substrate
        samp3 = Sample(name='苯磺酰胺', concentration=0.1)
        db.session.add(samp3)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp3.id, sample_id=samp3.id, role='substrate'))
        
        # Additive
        samp_add = Sample(name='K₂CO₃', concentration=0.01)
        db.session.add(samp_add)
        db.session.flush()
        db.session.execute(experiment_sample.insert().values(
            experiment_id=exp3.id, sample_id=samp_add.id, role='additive'))
        
        # Analysis
        analysis3 = Analysis(
            experiment_id=exp3.id,
            yield_pct=72.0,
            faraday_efficiency=78.0,
            selectivity=80.0,
            byproducts='未检测',
            reproducibility_mean=72.0,
            reproducibility_std=4.8,
            num_replicates=3,
            reproducibility_rsd=6.67,
            notes='光电催化条件下，苯磺酰胺氧化合成收率良好，FE达78%。'
        )
        db.session.add(analysis3)
        
        # Commit all
        db.session.commit()
        print('数据库初始化成功！')
        print(f'  创建了 {User.query.count()} 个用户')
        print(f'  创建了 {Experiment.query.count()} 个实验')
        print(f'  创建了 {Electrode.query.count()} 个电极')
        print(f'  创建了 {Electrolyte.query.count()} 个电解质')
        print(f'  创建了 {Sample.query.count()} 个样品')
        print(f'  创建了 {Analysis.query.count()} 个分析结果')


if __name__ == '__main__':
    seed()
