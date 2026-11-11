"""Deterministic, user-scoped report comparison. Never infer diagnoses.

Dates are upload dates, not necessarily specimen dates. Comparisons are made only
between matching test labels and compatible identical units.
"""
import math

def _valid_lab_map(report):
    found={}
    for lab in report.get('labs',[]):
        name=str(lab.get('name','')).strip()
        unit=str(lab.get('unit','')).strip().replace('μ','µ')
        value=lab.get('value')
        if not name or not unit or unit=='unit not found':
            continue
        if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value):
            continue
        key=(name.casefold(),unit.casefold())
        # Same test twice in one report is ambiguous. Exclude it.
        if key in found:
            found[key]=None
        else:
            found[key]=lab
    return {k:v for k,v in found.items() if v is not None}


def compare_reports(earlier:dict,later:dict)->list[dict]:
    if earlier.get('id') == later.get('id'):
        raise ValueError('Choose two distinct reports')
    a,b=_valid_lab_map(earlier),_valid_lab_map(later)
    rows=[]
    for key in sorted(a.keys() & b.keys()):
        left,right=a[key],b[key]
        old=float(left['value']); new=float(right['value'])
        rows.append({'name':left['name'],'unit':left['unit'],
                     'earlier':old,'later':new,'change':round(new-old,4),
                     'earlier_status':left.get('status','Not evaluated'),
                     'later_status':right.get('status','Not evaluated'),
                     'reference_earlier':left.get('reference',''),
                     'reference_later':right.get('reference','')})
    return rows
