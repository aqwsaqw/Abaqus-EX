# -*-coding:UTF-8-*-
from abaqus import *
from abaqusConstants import *
from caeModules import *

model_name = 'biper_nocement_01'
# step1：生成部件
s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.rectangle(point1=(-125.0, 35.0), point2=(-30.0, 0.0))
s.rectangle(point1=(125.0, 35.0), point2=(30.0, 0.0))
p = mdb.models[model_name].Part(name='hemo', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=30.0)
del mdb.models[model_name].sketches['__profile__']

s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.ArcByCenterEnds(center=(0.0, 45.0), point1=(-10.0, 44.0), point2=(10.0, 44.0), direction=COUNTERCLOCKWISE)
s.Line(point1=(-10.0, 44.0), point2=(10.0, 44.0))
p = mdb.models[model_name].Part(name='top', dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
p.AnalyticRigidSurfExtrude(sketch=s, depth=30.0)
p = mdb.models[model_name].parts['top']
del mdb.models[model_name].sketches['__profile__']
p = mdb.models[model_name].parts['top']
p.ReferencePoint(point=(0.0, 40.0, 0.0))

s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.ArcByCenterEnds(center=(-100.0, -5.0), point1=(-105.0, -4.5), point2=(-95.0, -4.5), direction=CLOCKWISE)
s.Line(point1=(-105.0, -4.5), point2=(-95.0, -4.5))
p = mdb.models[model_name].Part(name='left', dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
p.AnalyticRigidSurfExtrude(sketch=s, depth=30.0)
p = mdb.models[model_name].parts['left']
del mdb.models[model_name].sketches['__profile__']
p = mdb.models[model_name].parts['left']
p.ReferencePoint(point=(-100.0, -3.0, 0.0))

s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
s.ArcByCenterEnds(center=(100.0, -5.0), point1=(105.0, -4.5), point2=(95.0, -4.5), direction=COUNTERCLOCKWISE)
s.Line(point1=(95.0, -4.5), point2=(105.0, -4.5))
p = mdb.models[model_name].Part(name='right', dimensionality=THREE_D, type=ANALYTIC_RIGID_SURFACE)
p.AnalyticRigidSurfExtrude(sketch=s, depth=30.0)
p = mdb.models[model_name].parts['right']
del mdb.models[model_name].sketches['__profile__']
p = mdb.models[model_name].parts['right']
p.ReferencePoint(point=(100.0, -3.0, 0.0))

# step2：材料属性定义
mdb.models[model_name].Material(name='stone')
mdb.models[model_name].materials['stone'].Density(table=((3.0e-9,),))
mdb.models[model_name].materials['stone'].Elastic(table=((50000.0, 0.15),))
mdb.models[model_name].Material(name='asphalt')
mdb.models[model_name].materials['asphalt'].Density(table=((1.8e-9,),))
mdb.models[model_name].materials['asphalt'].Elastic(table=((800.0, 0.30),))
mdb.models[model_name].Material(name='cement')
mdb.models[model_name].materials['cement'].Density(table=((2.0e-9,),))
mdb.models[model_name].materials['cement'].Elastic(table=((15000.0, 0.20),))

mdb.models[model_name].Material(name='hemo')
mdb.models[model_name].materials['hemo'].Density(table=((2.5e-9,),))
mdb.models[model_name].materials['hemo'].Elastic(table=((20000.0, 0.25),))
mdb.models[model_name].Material(name='aa')
mdb.models[model_name].materials['aa'].Density(table=((1.8e-9,),))
mdb.models[model_name].materials['aa'].Elastic(type=TRACTION, table=((90816.0, 90816.0, 90816.0),))
mdb.models[model_name].materials['aa'].MaxsDamageInitiation(table=((8.96, 8.96, 8.96),))
mdb.models[model_name].materials['aa'].maxsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=POWER_LAW, power=1.0, table=((1.71, 1.71, 1.71),))
mdb.models[model_name].materials['aa'].maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)
mdb.models[model_name].Material(name='cc')
mdb.models[model_name].materials['cc'].Density(table=((2.0e-9,),))
mdb.models[model_name].materials['cc'].Elastic(type=TRACTION, table=((131208.0, 131208.0, 131208.0),))
mdb.models[model_name].materials['cc'].MaxsDamageInitiation(table=((4.81, 4.81, 4.81),))
mdb.models[model_name].materials['cc'].maxsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=POWER_LAW, power=1.0, table=((0.62, 0.62, 0.62),))
mdb.models[model_name].materials['cc'].maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)

mdb.models[model_name].Material(name='ac')
mdb.models[model_name].materials['ac'].Density(table=((1.9e-9,),))
mdb.models[model_name].materials['ac'].Elastic(type=TRACTION, table=((68904.0, 68904.0, 68904.0),))
mdb.models[model_name].materials['ac'].MaxsDamageInitiation(table=((1.4, 1.4, 1.4),))
mdb.models[model_name].materials['ac'].maxsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=POWER_LAW, power=1.0, table=((0.53, 0.53, 0.53),))
mdb.models[model_name].materials['ac'].maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)
mdb.models[model_name].Material(name='as')
mdb.models[model_name].materials['as'].Density(table=((1.8e-9,),))
mdb.models[model_name].materials['as'].Elastic(type=TRACTION, table=((75768.0, 75768.0, 75768.0),))
mdb.models[model_name].materials['as'].MaxsDamageInitiation(table=((2.8, 2.8, 2.8),))
mdb.models[model_name].materials['as'].maxsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=POWER_LAW, power=1.0, table=((0.77, 0.77, 0.77),))
mdb.models[model_name].materials['as'].maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)
mdb.models[model_name].Material(name='cs')
mdb.models[model_name].materials['cs'].Density(table=((1.9e-9,),))
mdb.models[model_name].materials['cs'].Elastic(type=TRACTION, table=((71544.0, 71544.0, 71544.0),))
mdb.models[model_name].materials['cs'].MaxsDamageInitiation(table=((3.03, 3.03, 3.03),))
mdb.models[model_name].materials['cs'].maxsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=POWER_LAW, power=1.0, table=((1.08, 1.08, 1.08),))
mdb.models[model_name].materials['cs'].maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)

#规划区域？
mdb.models[model_name].HomogeneousSolidSection(name='asphalt', material='asphalt', thickness=None)
mdb.models[model_name].HomogeneousSolidSection(name='cement', material='cement', thickness=None)
mdb.models[model_name].HomogeneousSolidSection(name='stone', material='stone', thickness=None)
mdb.models[model_name].HomogeneousSolidSection(name='hemo', material='hemo', thickness=None)
mdb.models[model_name].CohesiveSection(name='aa', material='aa', response=TRACTION_SEPARATION, outOfPlaneThickness=None)
mdb.models[model_name].CohesiveSection(name='cc', material='cc', response=TRACTION_SEPARATION, outOfPlaneThickness=None)
mdb.models[model_name].CohesiveSection(name='ac', material='ac', response=TRACTION_SEPARATION, outOfPlaneThickness=None)
mdb.models[model_name].CohesiveSection(name='as', material='as', response=TRACTION_SEPARATION, outOfPlaneThickness=None)
mdb.models[model_name].CohesiveSection(name='cs', material='cs', response=TRACTION_SEPARATION, outOfPlaneThickness=None)

p = mdb.models[model_name].parts['COHESIVE']
region=p.sets['AA_SET']
p.SectionAssignment(region=region, sectionName='aa', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)
region=p.sets['AC_SET']
p.SectionAssignment(region=region, sectionName='ac', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)
region=p.sets['AS_SET']
p.SectionAssignment(region=region, sectionName='as', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)

region = p.sets['A_SET']
p.SectionAssignment(region=region, sectionName='asphalt', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)

region=p.sets['CC_SET']
p.SectionAssignment(region=region, sectionName='cc', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)
region=p.sets['CS_SET']
p.SectionAssignment(region=region, sectionName='cs', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)

region=p.sets['C_SET']
p.SectionAssignment(region=region, sectionName='cement', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
    thicknessAssignment=FROM_SECTION)

region = p.sets['S_SET']
p.SectionAssignment(region=region, sectionName='stone', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
p = mdb.models[model_name].parts['hemo']
c = p.cells
cells = c[0:2]
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='hemo', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
