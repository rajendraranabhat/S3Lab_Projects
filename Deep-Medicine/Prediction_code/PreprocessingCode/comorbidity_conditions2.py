#Swati Tezcan Version
import numpy as np
import pandas as pd
def convertDX(DXVALUE):
    dx3= DXVALUE[:3]
    dx2= DXVALUE[3:]
    dx2= "0."+dx2
    dxfinal = float(dx3)+float(dx2)
    return dxfinal

def comorb2_condition(DX,DRG):
    #DRG DATA is in form code *space* SomeText.We just need the codes
    # DRG FLAGS
    CARDDRG = RENALDRG = PERIDRG = NERVDRG = CEREDRG = PULMDRG = DIABDRG = HYPODRG = LIVERDRG = 0
    ULCEDRG = HIVDRG = LEUKDRG = CANCDRG = ARTHDRG = NUTRDRG = ANEMDRG = ALCDRG = HTNCXDRG = HTNDRG = COAGDRG = PSYDRG = OBESEDRG = DEPRSDRG = alc_drug = 0
    if DRG.strip() != 'nan' :
        DRG = int(DRG.split(" ", 1)[0])

        if DRG in [001, 002, 302, 303, 253, 254, 265, 296, 297, 298] or (DRG >= 215 and DRG <= 238) or (
                    DRG >= 242 and DRG <= 251) or (DRG >= 280 and DRG <= 293) \
                    or (DRG >= 258 and DRG <= 262) or (DRG >= 306 and DRG <= 313):
            CARDDRG = 1
        elif DRG >= 299 and DRG <= 301:
            PERIDRG = 1
        elif DRG in [652, 656, 657, 658, 659, 660, 661, 673, 674, 675] or (DRG >= 682 and DRG <= 700):
            RENALDRG = 1
        elif (DRG >= 020 and DRG <= 042) or (DRG >= 052 and DRG <= 103):
            NERVDRG = 1
        elif DRG in [020, 021, 022, 034, 035, 036, 037, 38, 064, 065, 066, 067, 68, 69, 070, 071, 072]:
            CEREDRG = 1
        elif DRG in [190, 191, 192, 202, 203]:
            PULMDRG = 1
        elif DRG in [637, 638, 639]:
            DIABDRG = 1
        elif DRG in [625, 626, 627, 643, 644, 645]:
            HYPODRG = 1
        elif DRG in [652, 682, 683, 684, 685]:
            RENFDRG = 1
        elif DRG in [420, 421, 422, 423, 424, 425, 432, 433, 434, 441, 442, 443, 444, 445, 446]:
            LIVERDRG = 1
        elif DRG in [377, 378, 379, 380, 381, 382, 383, 384]:
            ULCEDRG = 1
        elif DRG in [969, 970, 974, 975, 976, 977]:
            HIVDRG = 1
        elif DRG in [820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 834, 835, 836, 837, 838, 839, 840, 841, 842,
                     843, 844, 845, 846, 847, 848, 849]:
            LEUKDRG = 1
        elif DRG in [054, 055, 146, 147, 148, 180, 181, 182, 374, 375, 376, 435, 436, 437, 542, 544, 582, 583, 584, 585,
                 597, 598, 599, 656, 657, 658, 686, 687, 688, 715, 716, 722, 723, 724, 736, \
                 737, 738, 739, 740, 741, 754, 755, 756, 826, 827, 828, 829, 830, 843, 844, 845, 846, 847, 848, 849]:
            CANCDRG = 1
        elif DRG in [545, 546, 547]:
            ARTHDRG = 1
        elif DRG in [640, 641]:
            NUTRDRG = 1
        elif DRG in [808, 809, 810, 811, 812]:
            ANEMDRG = 1
        elif DRG in [894, 895, 896]:
            ALCDRG = 1
        elif DRG in [813]:
            COAGDRG = 1
        elif DRG in [077, 78, 304]:
            HTNCXDRG = 1
        elif DRG in [79, 305]:
            HTNDRG = 1
        elif DRG in [885]:
            PSYDRG = 1
        elif DRG in [619, 620, 621]:
            OBESEDRG = 1
        elif DRG in [881]:
            DEPRSDRG = 1

    #############################################################################################################################################
    #                                                         DX CODES                                                                          #
    #############################################################################################################################################
    HTNPREG = HTNWOCHF = HTNWCHF = HHRWRF =HHRWHRF = OHTNPREG = HRENWORF  = HRENWRF = HHRWOHRF  = HHRWCHF = 0;
    VALVE = HTNCX = HTN = PARA = NEURO = HYPOTHY = LYMPH = COAG = OBESE = WGHTLOSS = DEPRESS = ALCOHOL = DRUG = LYTES = ANEMDEF = BLDLOSS = anemia = HTN_C =0
    valve = ['V422', 'V433']
    obese = ['V854', 'V8554', 'V8530', 'V8531', 'V8532', 'V8533', 'V8534', 'V8535', 'V8536', 'V8537', 'V8538', 'V8539']


    for dx in DX:

        DXVALUE = dx.replace("dx", "")
        if DXVALUE == "":
            continue
        if DXVALUE[0]== 'V' or DXVALUE[0] == 'E':
            if DXVALUE in valve: VALVE = 1
            if DXVALUE in obese: OBESE = 1

        else:
            DXVALUE = convertDX(DXVALUE)

            if DXVALUE in [397.9] or (DXVALUE >= 394.0 and DXVALUE<=397.1) or (DXVALUE >= 93.2 and DXVALUE<=93.24) or (DXVALUE >= 424.0 and DXVALUE<=424.99):
                VALVE = 1
                continue
            if DXVALUE in [401.1,401.9] or (DXVALUE >= 642.00 and DXVALUE <= 642.04) :
                HTN = 1
                continue
            if DXVALUE in [401.0, 437.2]:
                HTNCX = 1
                continue
            if DXVALUE >= 642.20 and DXVALUE <= 642.24:
                HTNPREG = 1
                continue
            if DXVALUE in [402.00, 402.10,402.90,405.09,405.19,405.99]:
                HTNWOCHF = 1
                continue
            if DXVALUE in [402.01,402.11,402.91]:
                HTNWCHF = 1
                continue
            if DXVALUE in [403.00, 403.10, 403.90,405.01,405.11,405.91] or (DXVALUE >= 642.10 and DXVALUE <= 642.14):
                HRENWORF = 1
                continue
            if DXVALUE in [403.01,403.11,403.19]:
                HRENWRF = 1
                continue
            if DXVALUE in [404.00,404.10,404.90]:
                HHRWOHRF = 1
                continue
            if DXVALUE in [404.01, 404.11, 404.91]:
                HHRWCHF = 1
                continue
            if DXVALUE in [404.02, 404.12, 404.92]:
                HHRWRF = 1
                continue
            if DXVALUE in [404.03, 404.13, 404.93]:
                HHRWHRF = 1
                continue
            if (DXVALUE >= 642.70 and DXVALUE <= 642.74) or (DXVALUE >= 642.90 and DXVALUE <= 642.94):
                OHTNPREG = 1
                continue
            if (DXVALUE >= 342.0 and DXVALUE <= 344.9) or (DXVALUE >= 438.20 and DXVALUE <= 438.53) or DXVALUE in [780.72]:
                PARA = 1
                continue
            if (DXVALUE >= 330.0 and DXVALUE <= 331.9)   or (DXVALUE >= 334.0 and DXVALUE <= 335.9)   or \
               (DXVALUE >= 341.1 and DXVALUE <= 341.9)   or (DXVALUE >= 334.0 and DXVALUE <= 335.9)   or \
               (DXVALUE >= 345.0 and DXVALUE <= 345.11)  or (DXVALUE >= 345.2 and DXVALUE <= 345.3)   or \
               (DXVALUE >= 345.40 and DXVALUE <= 345.91) or (DXVALUE >= 347.00 and DXVALUE <= 347.01) or \
               (DXVALUE >= 347.10 and DXVALUE <= 347.11) or (DXVALUE >= 649.40 and DXVALUE <= 649.44) or \
               (DXVALUE >= 768.70 and DXVALUE <= 768.73) or DXVALUE in [332.0,333.4,333.5,333.7,333.71,333.72,333.79,333.85,333.94,338.0,340.0,768.7,780.3,780.31,780.32,780.39,780.97,784.3]:
                NEURO = 1
                continue
            if (DXVALUE >= 243.0 and DXVALUE <= 244.2) or  DXVALUE in [244.8,244.9] :
                HYPOTHY = 1
                continue
            if (DXVALUE >= 200.0 and DXVALUE <= 202.38) or (DXVALUE >= 202.50 and DXVALUE <= 203.01) or \
               (DXVALUE >= 203.02 and DXVALUE <= 203.82) or DXVALUE in [238.6, 273.3] :
                LYMPH = 1
                continue
            if (DXVALUE >= 286.0 and DXVALUE <= 286.9)  or (DXVALUE >= 287.3 and DXVALUE <= 287.5) or \
               (DXVALUE >= 649.3 and DXVALUE <= 649.34) or DXVALUE in [287.1, 289.84]:
                COAG = 1
                continue
            if (DXVALUE >= 649.10 and DXVALUE <= 649.14) or DXVALUE in [278.0, 278.01,793.91]:
                OBESE=1
                continue
            if (DXVALUE >= 260.0 and DXVALUE <= 263.9) or (DXVALUE >= 783.21 and DXVALUE <= 783.22):
                WGHTLOSS = 1
                continue
            if (DXVALUE >= 276.0 and DXVALUE <= 276.9):
                LYTES = 1
                continue
            if (DXVALUE >= 648.20 and DXVALUE <= 648.24) or DXVALUE in [280.0]:
                BLDLOSS = 1
                continue
            if (DXVALUE >= 285.21 and DXVALUE <= 285.29) or (DXVALUE >= 280.1 and DXVALUE <= 281.9) or DXVALUE in [285.9]:
                ANEMDEF = 1
                continue
            if (DXVALUE >= 303.00 and DXVALUE <= 303.93) or (DXVALUE >=305.00 and DXVALUE <= 305.3) or \
               (DXVALUE >= 291.0 and DXVALUE <= 291.3) or DXVALUE in [291.5, 291.8,291.9,291.81,291.82,291.89]:
                ALCOHOL =1
                continue
            if (DXVALUE >= 292.82 and DXVALUE <= 292.89) or (DXVALUE >= 304.00 and DXVALUE <= 304.93) or \
               (DXVALUE >= 305.20 and DXVALUE <= 305.93) or (DXVALUE >= 648.30 and DXVALUE <= 648.34) or DXVALUE in [292.0, 289.84]:
                DRUG =1
                continue
            if  DXVALUE in [300.4,311.0,309.0,309.1,301.12]:
                DEPRESS =1
                continue

                    #Initializing Hypertension and Renal Flags

    if HTNPREG :   HTNCX = 1
    if HTNWOCHF:   HTNCX = 1
    if HTNWCHF :   HTNCX = 1
    if HRENWORF:   HTNCX = 1
    if HRENWRF :   HTNCX = 1
    if HHRWOHRF:   HTNCX = 1
    if HHRWRF  :   HTNCX = 1
    if HHRWHRF :   HTNCX = 1
    if HHRWRF  :   RENLFAIL = 1
    if HHRWHRF :   RENLFAIL = 1
    if HRENWRF :   RENLFAIL = 1
    if OHTNPREG:   HTNCX =1

    # Set up code to only count the more severe comorbidity
    if HTNCX: HTN = 0;


    # Applying DRG Exlusions

    if VALVE        and CARDDRG  : VALVE = 0
    if HTN          and HTNDRG   : HTN   = 0
    if HTNCX        and HTNCXDRG : HTNCX = 0
    if HTNPREG      and HTNCXDRG : HTNCX = 0
    if HTNWOCHF     and (HTNCXDRG or CARDDRG) : HTNCX = 0
    if HTNWCHF      and (HTNCXDRG or CARDDRG) : HTNCX = 0
    if HRENWORF     and (HTNCXDRG or RENALDRG) : HTNCX = 0
    if HRENWRF      and (HTNCXDRG): HTNCX = 0
    if HRENWRF      and (RENALDRG): RENLFAIL = 0
    if HHRWOHRF     and (HTNCXDRG or CARDDRG or RENALDRG) : HTNCX = 0
    if HHRWCHF      and (HTNCXDRG or CARDDRG or RENALDRG) : HTNCX = 0
    if HHRWRF       and (HTNCXDRG or CARDDRG or RENALDRG) : HTNCX = 0
    if HHRWRF       and (RENALDRG): RENLFAIL = 0
    if HHRWHRF      and (HTNCXDRG or CARDDRG or RENALDRG): HTNCX = 0
    if HHRWHRF      and (RENALDRG): RENLFAIL = 0
    if OHTNPREG     and (HTNCXDRG or CARDDRG or RENALDRG): HTNCX = 0

    if NEURO    and NERVDRG:  NEURO = 0
    if HYPOTHY  and HYPODRG:  HYPOTHY = 0
    if LYMPH    and LEUKDRG:  LYMPH = 0
    if COAG     and COAGDRG:  COAG = 0
    if WGHTLOSS and NUTRDRG:  WGHTLOSS = 0
    if LYTES    and NUTRDRG:  LYTES = 0
    if BLDLOSS  and ANEMDRG:  BLDLOSS = 0
    if ANEMDEF  and ANEMDRG:  ANEMDEF = 0
    if ALCOHOL  and ALCDRG:   ALCOHOL = 0
    if DRUG     and ALCDRG:   DRUG = 0
    if DEPRESS  and DEPRSDRG: DEPRESS = 0
    if PARA     and CEREDRG:  PARA = 0
    if OBESE    and (NUTRDRG or OBESEDRG):  OBESE = 0


    #Combine HTN and HTNCX into HTN_C
    if HTN or HTNCX : HTN_C =1


    #Combine anemia
    if BLDLOSS or ANEMDEF: anemia = 1


    #Combine Drug and Alcohol Abuse
    if ALCOHOL or DRUG : alc_drug =1
    conditions = {
            'VALVE': VALVE,
            'HYPOTHY': HYPOTHY,
            'COAG': COAG,
            'OBESE': OBESE,
            'WGHTLOSS': WGHTLOSS,
            'LYTES': LYTES,
            'anemia': anemia,
            'alc_drug': alc_drug,
            'DEPRESS': DEPRESS,
            'HTN_C': HTN_C,
            'PARA': PARA,
            'NEURO': NEURO}

    return conditions