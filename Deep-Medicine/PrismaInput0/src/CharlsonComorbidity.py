#Swati Tezcan Version
#Dictionary for conditons
#index:variablename:condition name
#0=imi = 'Myocardial Infarction'
#1=ichf = 'Congestive Heart Failure'
#2=ipvd = 'Peripheral Vascular Disease'
#3=icvd = 'Cerebrovascular Disease'
#4=iccidem = 'Dementia'
#5=cpd = 'Chronic Pulmonary Disease'
#6=rhemz = 'Connective Tissue Disease-Rheumatic Disease'
#7=pud = 'Peptic Ulcer Disease'
#8=mliverd = 'Mild Liver Disease'
#9=idiabnc = 'Diabetes without complications'
#10=idiabc = 'Diabetes with complications'
#11=ihpplegia = 'Paraplegia and Hemiplegia'
#12=irenald = 'Renal Disease'
#13=icancer = 'Cancer'
#14=imsliver = 'Moderate or Severe Liver Disease'
#15=imcancer = 'Metastatic Carcinoma'
#16=iaids = 'AIDS/HIV';
#17=cci = 'CCI Score calculated'
#18 = cancer (icancer or imcancer = true)
#19 = liver (mliverd or imsliver =true)
#20 = diabetes(idiabnc or diabnc =true)

def CharlsonICD9CM(DX):

    mi = chf = pvd = cvd = ccidem = cpd = rhemz = pud = mliverd = diabnc = diabc = hpplegia = renald = cancer = msliver = mcancer = aids = can = liverd = diabetes =0

    for i in range(len(DX)):
        # Myocardial Infarction

        if DX[i] in ['410', '412']:
            mi = 1

        # Congestive Heart Failure
        if DX[i] in ['39891', '40201', '40211', '40291', '40401', '40403', '40411', '40413', '40491', '40493','4254', '4255', '4257', '4258', '4259', '428']:
            chf = 1;

        # Periphral Vascular Disease
        if DX[i] in ['0930', '4373', '440', '441', '4431', '4432', '4438', '4439', '4471', '5571', '5579', 'V434']:
            pvd = 1;

        # Cerebrovascular Disease
        if DX[i] in ['36234', '430', '431', '432', '433', '434', '435', '436', '437', '438']:
            cvd = 1;

        # Dementia
        if DX[i] in ['290', '2941', '3312']:
            ccidem = 1;

        # Chronic Pulmonary Disease
        if DX[i] in ['4168', '4169', '490', '491', '492', '493', '494', '495', '496', '500', '501', '502', '503','504', '505', '5064', '5081', '5088']:
            cpd = 1;

        # Connective Tissue Disease - Rheumatic Disease
        if DX[i] in ['4465', '7100', '7101', '7102', '7103', '7104', '7140', '7141', '7142', '7148', '725']:
            rhemz = 1;

        # Peptic Ulcer Disease * /
        if DX[i] in ['531', '532', '533', '534'] :
            pud = 1

        # Mild Liver Disease
        if DX[i] in ['07022', '07023', '07032', '07033', '07044', '07054', '0706', '0709', '570', '571', '5733','5734', '5738', '5739', 'V427']:
            mliverd = 1

        # Diabetes without complications
        if DX[i] in ['2500', '2501', '2502', '2503', '2508', '2509'] :
            diabnc = 1
        # Diabetes with complications
        if DX[i] in ['2504', '2505', '2506', '2507']:
            diabc = 1

        # Paraplegia and Hemiplegia
        if DX[i] in ['3341', '342', '343', '3440', '3441', '3442', '3443', '3444', '3445', '3446', '3449']:
            hpplegia = 1

        # Renal Disease
        if DX[i] in ['40301', '40311', '40391', '40402', '40403', '40412', '40413', '40492', '40493', '582','5830', '5831', '5832', '5834', '5836', '5837', '585', '586', '5880', 'V420', 'V451', 'V56']:
            renald = 1

        # Cancer
        if DX[i] in ['140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153','154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '170', '171',
              '172', '174', '175', '176', '179', '180', '181', '182', '183', '184', '185', '186', '187', '188',
              '189', '190', '191', '192', '193', '194', '195', '200', '201', '202', '203', '204', '205', '206',
              '207', '208', '2386']:
            cancer = 1

        # Moderate or Severe Liver Disease
        if DX[i] in ['4560', '4561', '4562', '5722', '5723', '5724', '5728']:
            msliver = 1

        # Metastatic Carcinoma

        if DX[i] in ['196', '197', '198', '199']:
            mcancer = 1

        # AIDS / HIV
        if DX[i] in ['042', '043', '044']:
            aids = 1

    cci = ((mi +chf +pvd +cvd +ccidem +cpd +rhemz +pud +mliverd +diabnc)*1)+((diabc +hpplegia +renald +cancer)*2 )+ (msliver*3) +((mcancer+ aids)*6)

    #Clubbing diseases together
    if cancer==1 or mcancer==1:
        can = 1
    if mliverd==1 or msliver ==1:
        liverd =1
    if diabnc ==1 or diabc ==1:
        diabetes =1

    conditions = [mi,chf ,pvd, cvd ,ccidem ,cpd ,rhemz, pud, mliverd,diabnc ,diabc ,hpplegia ,renald ,cancer ,msliver ,mcancer ,aids,cci,can,liverd,diabetes]
    return conditions