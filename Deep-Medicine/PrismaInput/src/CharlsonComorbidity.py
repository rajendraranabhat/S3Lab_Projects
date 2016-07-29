#Swati Tezcan Version
#Dictionary for conditons
#index:variablename:condition name
#0=imi = Myocardial Infarction
#1=ichf = Congestive Heart Failure
#2=ipvd = Peripheral Vascular Disease
#3=icvd = Cerebrovascular Disease
#4=iccidem = Dementia
#5=cpd = Chronic Pulmonary Disease
#6=rhemz = Connective Tissue Disease-Rheumatic Disease
#7=pud = Peptic Ulcer Disease
#8=mliverd = Mild Liver Disease
#9=idiabnc = Diabetes without complications
#10=idiabc = Diabetes with complications
#11=ihpplegia = Paraplegia and Hemiplegia
#12=irenald = Renal Disease
#13=icancer = Cancer
#14=imsliver = Moderate or Severe Liver Disease
#15=imcancer = Metastatic Carcinoma
#16=iaids = AIDS/HIV;
#17=cci = CCI Score calculated
#18 = cancer (icancer or imcancer = true)
#19 = liver (mliverd or imsliver =true)
#20 = diabetes(idiabnc or diabnc =true)

def convertDX(DXVALUE):
    dx3= DXVALUE[:3]
    dx2= DXVALUE[3:]
    dx2= "0."+dx2
    dxfinal = float(dx3)+float(dx2)
    return dxfinal


def CharlsonICD9CM(DX):

    mi = chf = pvd = cvd = ccidem = cpd = rhemz = pud = mliverd = diabnc = diabc = hpplegia = renald = cancer = msliver = mcancer = aids = can = liverd = diabetes =0


    for i in range(len(DX)):
        # Myocardial Infarction
        DX[i] = DX[i].replace("dx", "")
        if DX[i] == "":
            continue
        if DX[i][0] == 'V' or DX[i][0] == 'E':
            if DX[i] == 'V434': pvd = 1
            if DX[i] == 'V427': mliverd =1
            if DX[i] in ['V420', 'V451', 'V56']: renald =1
        else:
            DX[i] = convertDX(DX[i])
            if (DX[i]  >= 410.0 and DX[i] <=410.9) or (DX[i]  >= 412.0 and DX[i] <=412.9):
                mi = 1

            # Congestive Heart Failure
            if DX[i] in [398.91, 402.01, 402.11, 402.91, 404.01, 404.03, 404.11, 404.13, 404.91, 404.93,425.4, 425.5, 425.7, 425.8, 425.9, 428]\
                      or (DX[i]  >= 428.0 and DX[i] <=428.9):
                chf = 1;

            # Periphral Vascular Disease
            if DX[i] in [093.0, 437.3, 443.1, 443.2, 443.8, 443.9, 447.1, 557.1, 557.9] \
                    or (DX[i] >= 440.0 and DX[i] <= 440.9) \
                    or (DX[i] >= 441.0 and DX[i] <= 441.9):
                pvd = 1;

            # Cerebrovascular Disease
            if DX[i] in [362.34] or (DX[i] >= 430.0 and DX[i] <= 438.9):
                cvd = 1;

            # Dementia
            if DX[i] in [294.1, 331.2] or (DX[i] >= 290.0 and DX[i] <= 290.9):
                ccidem = 1

            # Chronic Pulmonary Disease
            if DX[i] in [416.8, 416.9, 506.4, 508.1, 508.8] or (DX[i] >= 490.0 and DX[i] <= 496.9) or (DX[i] >= 500.0 and DX[i] <= 505.9):
                cpd = 1;

            # Connective Tissue Disease - Rheumatic Disease
            if DX[i] in [446.5, 710.0, 710.1, 710.2, 710.3, 710.4, 714.0, 714.1, 714.2, 714.8]or (DX[i] >= 725.0 and DX[i] <= 725.9) :
                rhemz = 1;

            # Peptic Ulcer Disease * /
            if DX[i] >= 531.0 and DX[i] <= 534.9 :
                pud = 1

            # Mild Liver Disease
            if DX[i] in [070.22, 070.23, 070.32, 070.33, 070.44, 070.54, 070.6, 070.9, 573.3,573.4, 573.8, 573.9] or (DX[i] >= 570.0 and DX[i] <= 571.9):
                mliverd = 1

            # Diabetes without complications
            if DX[i] in [250.0, 250.1, 250.2, 250.3, 250.8, 250.9] :
                diabnc = 1

            # Diabetes with complications
            if DX[i] in [250.4, 250.5, 250.6, 250.7]:
                diabc = 1

            # Paraplegia and Hemiplegia
            if DX[i] in [334.1, 344.0, 344.1, 344.2, 344.3, 344.4, 344.5, 344.6, 344.9] or [DX[i] >= 342.0 and DX[i] <= 343.9]:
                hpplegia = 1

            # Renal Disease
            if DX[i] in [403.01, 403.11, 403.91, 404.02, 404.03, 404.12, 404.13, 404.92, 404.93, 583.0, 583.1, 583.2, 583.4, 583.6, 583.7,588.0] \
                    or DX[i] >= 582.0 and DX[i] <= 582.9 \
                    or DX[i] >= 585.0 and DX[i] <= 586.9:
                renald = 1

            # Cancer
            if DX[i] in [238.6] or DX[i] >= 140.0 and DX[i] <= 208.9:
                cancer = 1

            # Moderate or Severe Liver Disease
            if DX[i] in [456.0, 456.1, 456.2, 572.2, 572.3, 572.4, 572.8]:
                msliver = 1

            # Metastatic Carcinoma

            if DX[i] >= 196.0 and DX[i] <= 199.9 :
                mcancer = 1

            # AIDS / HIV
            if DX[i] in [042.0, 043.0, 044.0]:
                aids = 1

    cci = ((mi +chf +pvd +cvd +ccidem +cpd +rhemz +pud +mliverd +diabnc)*1)+((diabc +hpplegia +renald +cancer)*2 )+ (msliver*3) +((mcancer+ aids)*6)

    #Clubbing diseases together
    if cancer == 1 or mcancer == 1:
        can = 1
    if mliverd==1 or msliver ==1:
        liverd =1
    if diabnc ==1 or diabc ==1:
        diabetes =1

    conditions = [mi,chf ,pvd, cvd ,ccidem ,cpd ,rhemz, pud, mliverd,diabnc ,diabc ,hpplegia ,renald ,cancer ,msliver ,mcancer ,aids,cci,can,liverd,diabetes]
    return conditions