-- Step 2 of 6
-- Raw variable generation

-- some events have two readings for the same realtime - impossible. keep only one.
-- TODO: Due to round off, should perform distinct (icustay_id, hosp_time) at the end.

-- store temporary variables in a schema: easy to drop later
set search_path to buffer, workspace, mimic2v26, public;

-- there appears to be multiple entries for the same measurement (e.g., weight in chartevents)

-- Age
-- there could be multiple intime per icustay_id in censusevents. however, assuming the stay does not
-- span over a year, using any one of the intime to calculate age would be reasonable. that is, the
-- error is small, less than one year, which is accurate enough herein.
\echo Age
create temporary table age_t as
select distinct on(ce.icustay_id) ce.icustay_id, round(date_part('day',(ce.intime-dp.dob))/365.242) as val
from censusevents as ce
left join d_patients as dp on ce.subject_id=dp.subject_id
inner join included_icustay using (icustay_id);

create unique index age_idx on age_t (icustay_id);


-- Care unit
\echo Care unit
create temporary table care_unit_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, cuid as val
from chartevents as ce
inner join included_icustay as it
on it.icustay_id=ce.icustay_id;
create unique index care_unit_idx on care_unit_t (icustay_id, realtime);


-- Table 3.1

\echo Glasgow coma scale
create temporary table gcs_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=198 and it.icustay_id=ce.icustay_id;

create unique index gcs_idx on gcs_t (icustay_id, realtime);

update gcs_t set val=null where val<3 or val>15;

\echo Heart rate
create temporary table hr_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=211 and it.icustay_id=ce.icustay_id;

create unique index hr_idx on hr_t (icustay_id, realtime);
update hr_t set val=null where val<20 or val>300;


\echo Resp rate
create temporary table resp_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=618 and it.icustay_id=ce.icustay_id;

create unique index resp_idx on resp_t (icustay_id, realtime);

\echo Sodium
create temporary table na_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (837, 1536) and it.icustay_id=ce.icustay_id;

create unique index na_idx on na_t (icustay_id, realtime);

update na_t set val=null where val<115 or val>160;


\echo CO2
create temporary table co2_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=787 and it.icustay_id=ce.icustay_id;

create unique index co2_idx on co2_t (icustay_id, realtime);

update co2_t set val=null where val<0.1 or val>55;


\echo PAPMean
create temporary table papmean_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=491 and it.icustay_id=ce.icustay_id;

create unique index papmean_idx on papmean_t (icustay_id, realtime);

update papmean_t set val=null where val<0.1 or val>120;



\echo Bilirubin
create temporary table bilirubin_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (803, 1527) and it.icustay_id=ce.icustay_id;

create unique index bilirubin_idx on bilirubin_t (icustay_id, realtime);

update bilirubin_t set val=null where val<0 or val>50;



\echo BUN
create temporary table bun_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (781, 1162) and it.icustay_id=ce.icustay_id;

update bun_t set val=null where val<0.1 or val>180;

create unique index bun_idx on bun_t (icustay_id, realtime);

\echo Magnesium
create temporary table mg_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (821, 1532) and it.icustay_id=ce.icustay_id;

update mg_t set val=null where val<0.01 or val>5;

create unique index mg_idx on mg_t (icustay_id, realtime);

\echo Hematocrit
create temporary table hct_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=813 and it.icustay_id=ce.icustay_id;

update hct_t set val=null where val<15 or val>60;

create unique index hct_idx on hct_t (icustay_id, realtime);

\echo INR
create temporary table inr_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (815, 1530) and it.icustay_id=ce.icustay_id;

update inr_t set val=null where val<0.01 or val>12;

create unique index inr_idx on inr_t (icustay_id, realtime);

\echo WBC
create temporary table wbc_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (861, 1127, 1542) and it.icustay_id=ce.icustay_id;

update wbc_t set val=null where val<0.01 or val>70;

create unique index wbc_idx on wbc_t (icustay_id, realtime);

\echo Lactate
create temporary table lactate_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (818, 1531) and it.icustay_id=ce.icustay_id;

update lactate_t set val=null where val<0.2 or val>40;

create unique index lactate_idx on lactate_t (icustay_id, realtime);


\echo Temperature
create temporary table temp_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (678, 679) and it.icustay_id=ce.icustay_id;

update temp_t set val=null where val<80 or val>110;

create unique index temp_idx on temp_t (icustay_id, realtime);


\echo Platelets
create temporary table platelets_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=828 and it.icustay_id=ce.icustay_id;

update platelets_t set val=null where val<0.1 or val>1200;

create unique index platelets_idx on platelets_t (icustay_id, realtime);

\echo Potassium
create temporary table potassium_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (829,1535) and it.icustay_id=ce.icustay_id;

update potassium_t set val=null where val<1 or val>10;

create unique index potassium_idx on potassium_t (icustay_id, realtime);






-- Table 3.2

\echo Heart rhythm
create temporary table hrm_va_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=212 and value1 ~* 'Junctional|Idioventricular|Vent. Tachy|Ventricular Fib|Asystole'
and it.icustay_id=ce.icustay_id;

create unique index hrm_va_idx on hrm_va_t (icustay_id, realtime);

update hrm_va_t set val=4;	-- set default value
update hrm_va_t set val=1 where value1 ~* 'Junctional';
update hrm_va_t set val=2 where value1 ~* 'Idioventricular';
update hrm_va_t set val=3 where value1 ~* 'Vent. Tachy';
update hrm_va_t set val=4 where value1 ~* 'Ventricular Fib';
update hrm_va_t set val=5 where value1 ~* 'Asystole';

\echo Riker-SAS scale
create temporary table rikersas_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=1337 and it.icustay_id=ce.icustay_id;

create unique index rikersas_idx on rikersas_t (icustay_id, realtime);

update RikerSAS_t set val=0;	-- set default value
update RikerSAS_t set val=1 where value1 ~* 'Unarousable';
update RikerSAS_t set val=2 where value1 ~* 'Very Sedated';
update RikerSAS_t set val=3 where value1 ~* 'Sedated';
update RikerSAS_t set val=4 where value1 ~* 'Calm/Cooperative';
update RikerSAS_t set val=5 where value1 ~* 'Agitated';
update RikerSAS_t set val=6 where value1 ~* 'Very Agitated';
update RikerSAS_t set val=7 where value1 ~* 'Danger Agitation';

\echo Pace maker
create temporary table pacemkr_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=516 and it.icustay_id=ce.icustay_id;

create unique index pacemkr_idx on pacemkr_t (icustay_id, realtime);

update pacemkr_t set val=0;	-- set default value/false
update pacemkr_t set val=1 where value1 ~* 'Epicardial Wires|Permanent|Transcutaneous|Transvenous';

\echo Jaundice skin color
create temporary table jaundice_skin_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=643 and it.icustay_id=ce.icustay_id;

create unique index jaundice_skin_idx on jaundice_skin_t (icustay_id, realtime);

update jaundice_skin_t set val=0;	-- set to false, assuming jaundiced is mutually exclusive to other conditions
update jaundice_skin_t set val=1 where value1 ~* 'Jaundiced';

\echo CSRU service type
create temporary table sv_csru_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=1125 and it.icustay_id=ce.icustay_id;

create unique index sv_csru_idx on sv_csru_t (icustay_id, realtime);

update sv_csru_t set val=0;
update sv_csru_t set val=1 where value1 ~* 'CSRU';


-- Table 3.4
-- maybe IO's don't need to have unique realtime stamp
-- select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, volume as val

-- All types of output
\echo IO ouput
create temporary table output_t as
select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, volume as val
from ioevents as me
inner join included_icustay as it
on itemid in (select itemid from d_ioitems where category is null)
and it.icustay_id=me.icustay_id;

create unique index output_idx on output_t (icustay_id, realtime);


-- All types of input
\echo IO input
create temporary table input_t as
select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, volume as val
from ioevents as me
inner join included_icustay as it
on itemid in (select itemid from d_ioitems where not category is null)
and it.icustay_id=me.icustay_id;

create unique index input_idx on input_t (icustay_id, realtime);




-- Table 3.7
\echo HIV
create temporary table aids_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on subject_id in (select subject_id from ICD9 where code ~ '^042')
and it.icustay_id=ce.icustay_id;

create unique index aids_idx on aids_t (icustay_id);

update aids_t set val=1;

\echo Hematologic Malignancy
create temporary table hem_malig_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on subject_id in (select subject_id from ICD9 where code ~ '^20[0-8]')
and it.icustay_id=ce.icustay_id;

create unique index hem_malig_idx on hem_malig_t (icustay_id);

update hem_malig_t set val=1;

\echo Metastatic Carcinoma
create temporary table met_carcinoma_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on subject_id in (select subject_id from ICD9 where code ~ '^1[4-5][0-9]|^1[6-7][0-5]|^179|^1[8-9][0-9]')
and it.icustay_id=ce.icustay_id;

create unique index met_carcinoma_idx on met_carcinoma_t (icustay_id);

update met_carcinoma_t set val=1;

-- organ insufficiency variables
\echo Organ insufficiency
create temporary table organ_insuff_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on subject_id in (select subject_id from ICD9 where code ~ '^571|^585.6|^428.[234]2|^518.83')
and it.icustay_id=ce.icustay_id;

create unique index organ_insuff_idx on organ_insuff_t (icustay_id);

update organ_insuff_t set val=1;

-- Immuno-compromised
create temporary table immuno_comp_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on subject_id in (select subject_id from ICD9 where code ~ '^V58.65|^V58.0|^V58.1|^042|^208.0|^202.')
and it.icustay_id=ce.icustay_id;

create unique index immuno_comp_idx on immuno_comp_t (icustay_id);

update immuno_comp_t set val=1;


-- additional values needed to compute derivales -- Table 3.8
\echo Non-invasive blood pressure - systolic
create temporary table nbp_sys_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=455 and it.icustay_id=ce.icustay_id;

create unique index nbp_sys_idx on nbp_sys_t (icustay_id, realtime);

update nbp_sys_t set val=null where val<30 or val>250;


\echo Non-invasive blood pressure - diastolic
create temporary table nbp_dias_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value2num as val
from chartevents as ce
inner join included_icustay as it
on itemid=455 and it.icustay_id=ce.icustay_id;

create unique index nbp_dias_idx on nbp_dias_t (icustay_id, realtime);

update nbp_dias_t set val=null where val<8 or val>150;


\echo Non-invasive blood pressure mean
create temporary table nbp_mean_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=456 and it.icustay_id=ce.icustay_id;
create unique index nbp_mean_idx on nbp_mean_t (icustay_id, realtime);

update nbp_mean_t set val=null where val<20 or val>250;



\echo Arterial blood pressure - systolic
create temporary table sbp_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=51 and it.icustay_id=ce.icustay_id;
create unique index sbp_idx on sbp_t (icustay_id, realtime);

update sbp_t set val=null where val<30 or val>300;


\echo Arterial blood pressure - diastolic
create temporary table dbp_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value2num as val
from chartevents as ce
inner join included_icustay as it
on itemid=51 and it.icustay_id=ce.icustay_id;

create unique index dbp_idx on dbp_t (icustay_id, realtime);

update dbp_t set val=null where val<8 or val>150;


\echo Arterial blood pressure mean
create temporary table map_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=52 and it.icustay_id=ce.icustay_id;

create unique index map_idx on map_t (icustay_id, realtime);

update map_t set val=null where val<20 or val>170;



\echo Urine output (ml)
create temporary table urine_out_t as
select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, volume as val
from ioevents as me
inner join included_icustay as it
on itemid in (55,69,715,61,57,85,473,405,428)
and it.icustay_id=me.icustay_id;
create unique index urine_out_idx on urine_out_t (icustay_id, realtime);

--(select itemid from d_ioitems		-- itemid's that describe urine output (null category) in cc/kg/hr
--where label ~* 'urine.*/hr' and category is null)


\echo Antibiotics in IOevents
create temporary table io_antibiotics_t as
select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, volume as val
from ioevents as me
inner join included_icustay as it
on itemid in (1609, 1653, 4566, 3903, 3924, 4413, 5101, 5119, 5294, 5644, 5647, 4568, 5957)
and it.icustay_id=me.icustay_id;
create unique index io_antibiotics_idx on io_antibiotics_t (icustay_id, realtime);

\echo Weight
create temporary table weight_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=581 and it.icustay_id=ce.icustay_id;
update weight_t set val=null where val<20 or val>300;
create unique index weight_idx on weight_t (icustay_id, realtime);

\echo Urine output per lb
create temporary table urine_per_lb_t as
select distinct on (icustay_id,realtime) uo.icustay_id, uo.realtime,uo.val/wt.val as val from urine_out_t as uo inner join weight_t as wt on uo.icustay_id=wt.icustay_id and uo.realtime=wt.realtime;
create unique index urine_per_lb_idx on urine_per_lb_t (icustay_id, realtime);

\echo Admit weight
create temporary table admit_weight_t as
select distinct on (icustay_id) ce.icustay_id, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=762 and it.icustay_id=ce.icustay_id;

update admit_weight_t set val=null where val<20 or val>300;

create unique index admit_weight_idx on admit_weight_t (icustay_id);


\echo Creatinine
create temporary table creatinine_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (791, 1525) and it.icustay_id=ce.icustay_id;

create unique index creatinine_idx on creatinine_t (icustay_id, realtime);

update creatinine_t set val=null where val<0.1 or val>40;


\echo PaO2
create temporary table pao2_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=779 and it.icustay_id=ce.icustay_id;

create unique index pao2_idx on pao2_t (icustay_id, realtime);

update pao2_t set val=null where val<0.1 or val>500;



\echo FiO2
create temporary table fio2_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=190 and it.icustay_id=ce.icustay_id;

create unique index fio2_idx on fio2_t (icustay_id, realtime);

update fio2_t set val=null where val<0.1 or val>1;

-- okay, technically not a raw variable because we lump items into a category
-- for some reason, the following three tables are empty....
\echo Any Pressor in ChartEvent
create temporary table chart_pressor_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (3112,1136,1222,1327,4501,5682,5747,5805,5843,5329,2248,2334,2445,2561,2765,6255,6603,7341)
and it.icustay_id=ce.icustay_id;

create unique index chart_pressor_idx on chart_pressor_t (icustay_id, realtime);

\echo Any Antibiotics in ChartEvent
create temporary table chart_antibiotics_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (808,809,810,3303,3369,3412,3445,3554,845,846,847,854,855,856,1354,4391,4415,4426,4497,4557,4587,4715,4762,4806,4958,5658,5715,5873,5887,5380,5401,5478,5523,4220,7888,8078,6046,4972,5022,5043,5060,5062,5063,5141,5204,3679,3756,3757,3827,3828,2273,8273,6261,6536,6610,6896,7204,7301,7303,7362)
and it.icustay_id=ce.icustay_id;
create unique index chart_antibiotics_idx on chart_antibiotics_t (icustay_id, realtime);


\echo Worst SOFA at a given time -- if score=4 -> organ failure
create temporary table worst_sofa_t as
select ce.icustay_id, ce.realtime, max(value1num) as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20002,20003,20004,20005,20006,20007,20008) and it.icustay_id=ce.icustay_id
group by ce.icustay_id, ce.realtime;

create unique index worst_sofa_idx on worst_sofa_t (icustay_id, realtime);

create temporary table resp_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20002) and it.icustay_id=ce.icustay_id;
create unique index resp_sofa_idx on resp_sofa_t (icustay_id, realtime);

create temporary table hepatic_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20003) and it.icustay_id=ce.icustay_id;
create unique index hepatic_sofa_idx on hepatic_sofa_t (icustay_id, realtime);

create temporary table hematologic_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20004) and it.icustay_id=ce.icustay_id;
create unique index hematologic_sofa_idx on hematologic_sofa_t (icustay_id, realtime);

create temporary table cardio_pressor_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20005) and it.icustay_id=ce.icustay_id;
create unique index cardio_pressor_sofa_idx on cardio_pressor_sofa_t (icustay_id, realtime);

create temporary table cardio_map_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20006) and it.icustay_id=ce.icustay_id;
create unique index cardio_map_sofa_idx on cardio_map_sofa_t (icustay_id, realtime);

create temporary table neurologic_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20007) and it.icustay_id=ce.icustay_id;
create unique index neurologic_sofa_idx on neurologic_sofa_t (icustay_id, realtime);

create temporary table renal_sofa_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (20008) and it.icustay_id=ce.icustay_id;
create unique index renal_sofa_idx on renal_sofa_t (icustay_id, realtime);

\echo Ventilator type
-- a binary/boolean variable (Table 3.2)
create temporary table vent_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=722 and value1 ~* '7200A|Drager|Other/Remarks|Servo 900c'
and it.icustay_id=ce.icustay_id;

create unique index vent_idx on vent_t (icustay_id, realtime);

update vent_t set val=1;

-- Table 3.9
\echo SpO2
-- Table 3.1
create temporary table spo2_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=646 and it.icustay_id=ce.icustay_id;

create unique index spo2_idx on spo2_t (icustay_id, realtime);


\echo AST (Enzymes)
create temporary table ast_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=770 and it.icustay_id=ce.icustay_id;

create unique index ast_idx on ast_t (icustay_id, realtime);
update ast_t set val=null where val<10 or val>1000;


\echo PTT
create temporary table ptt_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (825,1533) and it.icustay_id=ce.icustay_id;

create unique index ptt_idx on ptt_t (icustay_id, realtime);
update ptt_t set val=null where val<10 or val>151;


\echo Calcium
create temporary table calcium_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (786, 1522) and it.icustay_id=ce.icustay_id;

create unique index calcium_idx on calcium_t (icustay_id, realtime);
update calcium_t set val=null where val<4 or val>14;

\echo Ionized calcium
create temporary table ion_cal_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=816 and it.icustay_id=ce.icustay_id;

create unique index ion_cal_idx on ion_cal_t (icustay_id, realtime);
update ion_cal_t set val=null where val<0 or val>2.5;

\echo Hemolobin
create temporary table hemoglobin_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=814 and it.icustay_id=ce.icustay_id;

create unique index hemoglobin_idx on hemoglobin_t (icustay_id, realtime);
update hemoglobin_t set val=null where val<4 or val>20;


\echo Aterial pH
create temporary table art_ph_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid in (780, 1126) and it.icustay_id=ce.icustay_id;

create unique index art_ph_idx on art_ph_t (icustay_id, realtime);
update art_ph_t set val=null where val<6.5 or val>8.5;


-- same as FiO2
-- \echo FiO2 Set
-- create temporary table fio2_set_t as
-- select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
-- from chartevents as ce
-- inner join included_icustay as it
-- on itemid=190 and it.icustay_id=ce.icustay_id;
-- 
-- create unique index fio2_set_idx on fio2_set_t (icustay_id, realtime);
-- update fio2_set_t set val=null where val<0.1 or val>1;


\echo ALT Set
create temporary table alt_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=769 and it.icustay_id=ce.icustay_id;

create unique index alt_idx on alt_t (icustay_id, realtime);
update alt_t set val=null where val<10 or val>1000;

\echo RBC count
create temporary table rbc_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=833 and it.icustay_id=ce.icustay_id;

create unique index rbc_idx on rbc_t (icustay_id, realtime);
update rbc_t set val=null where val<1 or val>7;

\echo PaCO2
create temporary table paco2_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, value1num as val
from chartevents as ce
inner join included_icustay as it
on itemid=778 and it.icustay_id=ce.icustay_id;

create unique index paco2_idx on paco2_t (icustay_id, realtime);
update paco2_t set val=null where val<5 or val>100;



\echo Mortality
-- a binary/boolean variable
-- difference of dates give results in days and then hours..
create temporary table died_t as
select distinct on (icustay_id) ce.icustay_id, date_part('day',dp.dod-ce.outtime)<30 as died, 0 as val 
from censusevents as ce
inner join d_patients as dp on ce.subject_id=dp.subject_id
inner join included_icustay as it on it.icustay_id=ce.icustay_id;

update died_t set val=1 where died;

create unique index died_idx on died_t (icustay_id);

\echo Time in hospital (minutes)
-- there could be multiple intime per icustay_id in censusevents. pick the first intime.
create temporary table length_of_stay_t as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime, round(date_part('epoch', ce.realtime-T2.min_intime)/60) as val
from chartevents as ce
inner join
(
	select icustay_id, min(intime) as min_intime
	from censusevents
	group by icustay_id
) as T2
on ce.icustay_id=T2.icustay_id and ce.icustay_id in
(
	select icustay_id from included_icustay
);

--select distinct on (icustay_id) ce.icustay_id, realtime, round(date_part('epoch', ce.realtime-T2.min_intime)/60) as val

create unique index length_of_stay_idx on length_of_stay_t (icustay_id, realtime);



-- Med items
drop table if exists var_id;
create temporary table var_id (itemid int, field text, remark text);
insert into var_id (itemid, field, remark) values -- shown in hours; converted to minutes at bottom
(42, 'dobutamine', 'Dobutamine'),
(43, 'dopamine', 'Dopamine'),
(44, 'epinephrine', 'Epinephrine'),
(47, 'levophed', 'Levophed'),
(119, 'epinephrine_k', 'Epinephrine-k'),
(120, 'levophed_k', 'Levophed-k'),
(127, 'neosynephrine', 'Neosynephrine'),
(128, 'neosynephrine_k', 'Neosynephrine-k'),
(117, 'esmolol', 'Esmolol'),
(122, 'labetolol', 'Labetolol'),
(51, 'vasopressin', 'Vasopressin'),
(45, 'insulin', 'Insulin'),
(133, 'sandostatin', 'Sandostatin'),
(123, 'lasix', 'Lasix'),
(112, 'amiodarone', 'Amiodarone'),
(115, 'diltiazem', 'Diltiazem'),
(48, 'lidocaine', 'Lidocaine'),
(52, 'procainamide', 'Procainamide'),
(113, 'atracurium', 'atracurium'),
(114, 'cistracurium', 'cistracurium'),
(116, 'doxacurium', 'doxacurium'),
(129, 'pancuronium', 'pancuronium'),
(138, 'vecuronium', 'vecuronium'),
(309,'epinephrine_drip','epinephrine drip'),
(306,'dobutamine_drip','dobutamine drip'),
(125,'milrinone','milrinone'),
(40,'levophed','amrinone'),
(307,'dopamine_drip','dopamine drip'),
(135,'tpa','TPA');



create or replace function tmp_function(boolean) returns boolean as $$
declare
	cur record;
begin
	for cur in select itemid, field, remark from var_id loop
		raise info '%', cur.remark;
		execute 'create temporary table ' || cur.field || '_t as'
			|| ' select distinct on (icustay_id, realtime) me.icustay_id, me.realtime, dose as val, stopped'
			|| ' from medevents as me'
			|| ' inner join included_icustay as it'
			|| ' on itemid=$1 and it.icustay_id=me.icustay_id'
		using cur.itemid;
	
		execute 'create unique index ' || cur.field || '_idx on ' 
			|| cur.field || '_t (icustay_id, realtime)';
			
		-- set stop realtimes to be have zero dose
		execute 'update ' || cur.field || '_t set val=0 where stopped ~* ''Stopped'' ';
		
	end loop;
	
	
	return true;
end;
$$ language plpgsql;
select tmp_function(true);




-- when computing variables (features), tables joins are used, and it is important to NOT introduce
-- new events (time stamps). so pay attention to the tables being joined to included_icustay or chartevets.
-- make sure there is no unecessary duplicated icusta_id and realtime entries. for example the age_t
-- can return multiple ages per icustay_id, which is undesired. this is mitigated by using distinct on icustay_id.
-- check entries count after done and compare to original entries count.
-- select count(*) from (
-- ) as count_check;


-- create two tables -- one raw (non-interpolated, i.e., no hold) and one interpolated with derived variables
-- some derived variables (e.g. slope) uses raw data, therefore it is good to keep a copy of the raw.
-- the raw data could also be used to validate the interpolation process.
drop table if exists raw_vars;

-- create a list of icustay_id with realtimes
\echo Fetch timestamps for all variables
create temporary table included_times as
select distinct on (icustay_id, realtime) ce.icustay_id, ce.realtime from chartevents as ce
inner join included_icustay
on ce.icustay_id=included_icustay.icustay_id;
create unique index it_idx on included_times (icustay_id, realtime);

\echo Create variable table - join with included times
create temporary table pre_raw_vars as
select it.icustay_id,
	it.realtime,
	length_of_stay_t.val as hosp_time,
	floor(length_of_stay_t.val/60/24)+1 as days,
	age_t.val as age,
	care_unit_t.val as care_unit,
	gcs_t.val as GCS,
	hr_t.val as HR,	
	na_t.val as na,
	co2_t.val as co2,
	bun_t.val as bun,
	mg_t.val as mg,
	hct_t.val as hct,
	inr_t.val as inr,
	wbc_t.val as wbc,
	hrm_va_t.val as hrm_va,
	rikersas_t.val as rikersas,
	pacemkr_t.val as pacemkr,
	jaundice_skin_t.val as jaundice,
	sv_csru_t.val as sv_csru,
	
	temp_t.val as temperature,
	
	output_t.val as io_output,
	platelets_t.val as platelets,
	potassium_t.val as potassium,
	aids_t.val as aids,
	hem_malig_t.val as hem_malig,
	met_carcinoma_t.val as met_carcinoma,
	organ_insuff_t.val as organ_insuff,
	immuno_comp_t.val as immuno_comp,
	nbp_sys_t.val as nbp_sys,
	nbp_dias_t.val as nbp_dias,
	nbp_mean_t.val as nbp_mean,
	sbp_t.val as abp_sys,
	dbp_t.val as abp_dias,
	map_t.val as abp_mean,
	urine_out_t.val as urine_out,
	urine_per_lb_t.val as urine_per_lb,
	weight_t.val as weight,
	admit_weight_t.val as admit_weight,
	creatinine_t.val as creatinine,
	pao2_t.val as pao2,
	fio2_t.val as fio2,
	vent_t.val as vent,
	spo2_t.val as spo2,
	died_t.val as died,
	sandostatin_t.val as sandostatin,
	papmean_t.val as papmean,
	
	dobutamine_t.val as dobutamine,
	dopamine_t.val as dopamine,
	epinephrine_t.val as epinephrine,
	epinephrine_k_t.val as epinephrine_k,
	levophed_t.val as levophed,
	levophed_k_t.val as levophed_k,
	neosynephrine_t.val as neosynephrine,
	neosynephrine_k_t.val as neosynephrine_k,
	esmolol_t.val as esmolol,
	labetolol_t.val as labetolol,
	vasopressin_t.val as vasopressin,
	insulin_t.val as insulin,
	lasix_t.val as lasix,
	
	amiodarone_t.val as amiodarone,
	diltiazem_t.val as diltiazem,
	lidocaine_t.val as lidocaine,
	procainamide_t.val as procainamide,
	atracurium_t.val as atracurium,
	cistracurium_t.val as cistracurium,
	doxacurium_t.val as doxacurium,
	pancuronium_t.val as pancuronium,
	vecuronium_t.val as vecuronium,
	
	io_antibiotics_t.val as io_antibiotics,
	chart_antibiotics_t.val as chart_antibiotics,
	chart_pressor_t.val as chart_pressor,
	epinephrine_drip_t.val as epinephrine_drip,
	dobutamine_drip_t.val as dobutamine_drip,
	milrinone_t.val as milrinone,
	dopamine_drip_t.val as dopamine_drip,
	amrinone_t.val as amrinone,
	resp_t.val as resp_rate,
	lactate_t.val as lactate,
	input_t.val as any_input,
	worst_sofa_t.val as worst_sofa,
	bilirubin_t.val as bilirubin,
	tpa_t.val as tpa,
	resp_sofa_t.val as resp_sofa,
    hepatic_sofa_t.val as hepatic_sofa,
    hematologic_sofa_t.val as hematologic_sofa,
    cardio_pressor_sofa_t.val as cardio_pressor_sofa,
    cardio_map_sofa_t.val as cardio_map_sofa,
    neurologic_sofa_t.val as neurologic_sofa,
    renal_sofa_t.val as renal_sofa,
	
	ast_t.val as ast,
	ptt_t.val as ptt,
	calcium_t.val as calcium,
	ion_cal_t.val as ion_calcium,
	hemoglobin_t.val as hemoglobin,
	art_ph_t.val as art_ph,
--	fio2_set_t.val as fio2_set,
	alt_t.val as alt,
	rbc_t.val as rbc,
	paco2_t.val as paco2


from included_times as it
left join age_t on it.icustay_id=age_t.icustay_id
left join care_unit_t on it.icustay_id=care_unit_t.icustay_id and it.realtime=care_unit_t.realtime
left join gcs_t on it.icustay_id=gcs_t.icustay_id and it.realtime=gcs_t.realtime
left join hr_t on it.icustay_id=hr_t.icustay_id and it.realtime=hr_t.realtime
left join na_t on it.icustay_id=na_t.icustay_id and it.realtime=na_t.realtime
left join co2_t on it.icustay_id=co2_t.icustay_id and it.realtime=co2_t.realtime
left join bun_t on it.icustay_id=bun_t.icustay_id and it.realtime=bun_t.realtime
left join mg_t on it.icustay_id=mg_t.icustay_id and it.realtime=mg_t.realtime
left join hct_t on it.icustay_id=hct_t.icustay_id and it.realtime=hct_t.realtime
left join inr_t on it.icustay_id=inr_t.icustay_id and it.realtime=inr_t.realtime
left join wbc_t on it.icustay_id=wbc_t.icustay_id and it.realtime=wbc_t.realtime
left join hrm_va_t on it.icustay_id=hrm_va_t.icustay_id and it.realtime=hrm_va_t.realtime
left join rikersas_t on it.icustay_id=rikersas_t.icustay_id and it.realtime=rikersas_t.realtime
left join pacemkr_t on it.icustay_id=pacemkr_t.icustay_id and it.realtime=pacemkr_t.realtime
left join jaundice_skin_t on it.icustay_id=jaundice_skin_t.icustay_id and it.realtime=jaundice_skin_t.realtime
left join sv_csru_t on it.icustay_id=sv_csru_t.icustay_id and it.realtime=sv_csru_t.realtime
left join temp_t on it.icustay_id=temp_t.icustay_id and it.realtime=temp_t.realtime

left join lactate_t on it.icustay_id=lactate_t.icustay_id and it.realtime=lactate_t.realtime

left join bilirubin_t on it.icustay_id=bilirubin_t.icustay_id and it.realtime=bilirubin_t.realtime
left join input_t on it.icustay_id=input_t.icustay_id and it.realtime=input_t.realtime


left join resp_t on it.icustay_id=resp_t.icustay_id and it.realtime=resp_t.realtime

left join output_t on it.icustay_id=output_t.icustay_id and it.realtime=output_t.realtime
left join platelets_t on it.icustay_id=platelets_t.icustay_id and it.realtime=platelets_t.realtime
left join potassium_t on it.icustay_id=potassium_t.icustay_id and it.realtime=potassium_t.realtime
left join aids_t on it.icustay_id=aids_t.icustay_id
left join hem_malig_t on it.icustay_id=hem_malig_t.icustay_id
left join met_carcinoma_t on it.icustay_id=met_carcinoma_t.icustay_id
left join organ_insuff_t on it.icustay_id=organ_insuff_t.icustay_id
left join immuno_comp_t on it.icustay_id=immuno_comp_t.icustay_id
left join nbp_sys_t on it.icustay_id=nbp_sys_t.icustay_id and it.realtime=nbp_sys_t.realtime
left join nbp_dias_t on it.icustay_id=nbp_dias_t.icustay_id and it.realtime=nbp_dias_t.realtime
left join nbp_mean_t on it.icustay_id=nbp_mean_t.icustay_id and it.realtime=nbp_mean_t.realtime
left join sbp_t on it.icustay_id=sbp_t.icustay_id and it.realtime=sbp_t.realtime
left join dbp_t on it.icustay_id=dbp_t.icustay_id and it.realtime=dbp_t.realtime
left join map_t on it.icustay_id=map_t.icustay_id and it.realtime=map_t.realtime
left join urine_out_t on it.icustay_id=urine_out_t.icustay_id and it.realtime=urine_out_t.realtime
left join urine_per_lb_t on it.icustay_id=urine_per_lb_t.icustay_id and it.realtime=urine_per_lb_t.realtime
left join weight_t on it.icustay_id=weight_t.icustay_id and it.realtime=weight_t.realtime
left join admit_weight_t on it.icustay_id=admit_weight_t.icustay_id
left join creatinine_t on it.icustay_id=creatinine_t.icustay_id and it.realtime=creatinine_t.realtime
left join pao2_t on it.icustay_id=pao2_t.icustay_id and it.realtime=pao2_t.realtime
left join fio2_t on it.icustay_id=fio2_t.icustay_id and it.realtime=fio2_t.realtime
left join vent_t on it.icustay_id=vent_t.icustay_id and it.realtime=vent_t.realtime
left join spo2_t on it.icustay_id=spo2_t.icustay_id and it.realtime=spo2_t.realtime
left join died_t on it.icustay_id=died_t.icustay_id
left join length_of_stay_t on it.icustay_id=length_of_stay_t.icustay_id and it.realtime=length_of_stay_t.realtime
left join papmean_t on it.icustay_id=papmean_t.icustay_id and it.realtime=papmean_t.realtime

left join chart_pressor_t on it.icustay_id=chart_pressor_t.icustay_id and it.realtime=chart_pressor_t.realtime
left join worst_sofa_t on it.icustay_id=worst_sofa_t.icustay_id and it.realtime=worst_sofa_t.realtime
left join resp_sofa_t on it.icustay_id=resp_sofa_t.icustay_id and it.realtime=resp_sofa_t.realtime
left join hepatic_sofa_t on it.icustay_id=hepatic_sofa_t.icustay_id and it.realtime=hepatic_sofa_t.realtime
left join hematologic_sofa_t on it.icustay_id=hematologic_sofa_t.icustay_id and it.realtime=hematologic_sofa_t.realtime
left join cardio_pressor_sofa_t on it.icustay_id=cardio_pressor_sofa_t.icustay_id and it.realtime=cardio_pressor_sofa_t.realtime
left join cardio_map_sofa_t on it.icustay_id=cardio_map_sofa_t.icustay_id and it.realtime=cardio_map_sofa_t.realtime
left join neurologic_sofa_t on it.icustay_id=neurologic_sofa_t.icustay_id and it.realtime=neurologic_sofa_t.realtime
left join renal_sofa_t on it.icustay_id=renal_sofa_t.icustay_id and it.realtime=renal_sofa_t.realtime


left join io_antibiotics_t on it.icustay_id=io_antibiotics_t.icustay_id and it.realtime=io_antibiotics_t.realtime
left join chart_antibiotics_t on it.icustay_id=chart_antibiotics_t.icustay_id and it.realtime=chart_antibiotics_t.realtime

left join sandostatin_t on it.icustay_id=sandostatin_t.icustay_id and it.realtime=sandostatin_t.realtime
left join insulin_t on it.icustay_id=insulin_t.icustay_id and it.realtime=insulin_t.realtime
left join lasix_t on it.icustay_id=lasix_t.icustay_id and it.realtime=lasix_t.realtime

left join dobutamine_t on it.icustay_id=dobutamine_t.icustay_id and it.realtime=dobutamine_t.realtime
left join dopamine_t on it.icustay_id=dopamine_t.icustay_id and it.realtime=dopamine_t.realtime
left join epinephrine_t on it.icustay_id=epinephrine_t.icustay_id and it.realtime=epinephrine_t.realtime
left join epinephrine_k_t on it.icustay_id=epinephrine_k_t.icustay_id and it.realtime=epinephrine_k_t.realtime
left join levophed_t on it.icustay_id=levophed_t.icustay_id and it.realtime=levophed_t.realtime
left join levophed_k_t on it.icustay_id=levophed_k_t.icustay_id and it.realtime=levophed_k_t.realtime
left join neosynephrine_t on it.icustay_id=neosynephrine_t.icustay_id and it.realtime=neosynephrine_t.realtime
left join neosynephrine_k_t on it.icustay_id=neosynephrine_k_t.icustay_id and it.realtime=neosynephrine_k_t.realtime
left join esmolol_t on it.icustay_id=esmolol_t.icustay_id and it.realtime=esmolol_t.realtime
left join labetolol_t on it.icustay_id=labetolol_t.icustay_id and it.realtime=labetolol_t.realtime
left join vasopressin_t on it.icustay_id=vasopressin_t.icustay_id and it.realtime=vasopressin_t.realtime

left join epinephrine_drip_t on it.icustay_id=epinephrine_drip_t.icustay_id and it.realtime=epinephrine_drip_t.realtime
left join dobutamine_drip_t on it.icustay_id=dobutamine_drip_t.icustay_id and it.realtime=dobutamine_drip_t.realtime
left join milrinone_t on it.icustay_id=milrinone_t.icustay_id and it.realtime=milrinone_t.realtime
left join dopamine_drip_t on it.icustay_id=dopamine_drip_t.icustay_id and it.realtime=dopamine_drip_t.realtime
left join amrinone_t on it.icustay_id=amrinone_t.icustay_id and it.realtime=amrinone_t.realtime

left join amiodarone_t on it.icustay_id=amiodarone_t.icustay_id and it.realtime=amiodarone_t.realtime
left join diltiazem_t on it.icustay_id=diltiazem_t.icustay_id and it.realtime=diltiazem_t.realtime
left join lidocaine_t on it.icustay_id=lidocaine_t.icustay_id and it.realtime=lidocaine_t.realtime
left join procainamide_t on it.icustay_id=procainamide_t.icustay_id and it.realtime=procainamide_t.realtime
left join atracurium_t on it.icustay_id=atracurium_t.icustay_id and it.realtime=atracurium_t.realtime
left join cistracurium_t on it.icustay_id=cistracurium_t.icustay_id and it.realtime=cistracurium_t.realtime
left join doxacurium_t on it.icustay_id=doxacurium_t.icustay_id and it.realtime=doxacurium_t.realtime
left join pancuronium_t on it.icustay_id=pancuronium_t.icustay_id and it.realtime=pancuronium_t.realtime
left join vecuronium_t on it.icustay_id=vecuronium_t.icustay_id and it.realtime=vecuronium_t.realtime
left join tpa_t on it.icustay_id=tpa_t.icustay_id and it.realtime=tpa_t.realtime

left join ast_t on it.icustay_id=ast_t.icustay_id and it.realtime=ast_t.realtime
left join ptt_t on it.icustay_id=ptt_t.icustay_id and it.realtime=ptt_t.realtime
left join calcium_t on it.icustay_id=calcium_t.icustay_id and it.realtime=calcium_t.realtime
left join ion_cal_t on it.icustay_id=ion_cal_t.icustay_id and it.realtime=ion_cal_t.realtime
left join hemoglobin_t on it.icustay_id=hemoglobin_t.icustay_id and it.realtime=hemoglobin_t.realtime
left join art_ph_t on it.icustay_id=art_ph_t.icustay_id and it.realtime=art_ph_t.realtime
--left join fio2_set_t on it.icustay_id=fio2_set_t.icustay_id and it.realtime=fio2_set_t.realtime
left join alt_t on it.icustay_id=alt_t.icustay_id and it.realtime=alt_t.realtime
left join rbc_t on it.icustay_id=rbc_t.icustay_id and it.realtime=rbc_t.realtime
left join paco2_t on it.icustay_id=paco2_t.icustay_id and it.realtime=paco2_t.realtime

order by icustay_id, realtime;

-- get rid of duplicates
create table workspace.raw_vars as select distinct on (icustay_id, hosp_time) * from pre_raw_vars order by icustay_id, hosp_time;

create unique index raw_vars_idx1 on raw_vars (icustay_id, realtime);
create index raw_vars_idx2 on raw_vars (icustay_id);
create unique index raw_vars_idx3 on raw_vars (icustay_id, hosp_time);

