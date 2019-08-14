def clean_variant(v,left=True,human_ref_pysam=None):
    # normalise variant.
    chrom,pos,ref,alt = v.split('-')
    pos = int(pos)
    if alt in set(['*','-']):
        # deletion, need human_ref for the missing base
        if human_ref_pysam is None:
            msg = 'need human ref pysam to normalise variant with alt as * or -'
            raise ValueError(msg)
        base = human_ref_pysam.fetch(chrom,pos-2,pos-1)
        return '-'.join([chrom, str(pos-1), base+ref, base])
    if len(ref) < len(alt):
        ran = range(len(ref))
    else:
        ran = range(len(alt))
    if left:
        for e in ran:
            ref_e = len(ref) - e - 1
            alt_e = len(alt) - e - 1
            if ref[ref_e] != alt[alt_e]: break
        for b in ran:
            if ref[b] != alt[b] or len(ref[b:ref_e+1]) == 1 or len(alt[b:alt_e+1]) == 1:
                break
    else:
        for b in ran:
            if ref[b] != alt[b]: break
        for e in ran:
            ref_e = len(ref) - e - 1
            alt_e = len(alt) - e - 1
            if ref[ref_e] != alt[alt_e] or len(ref[b:ref_e+1]) == 1 or len(alt[b:alt_e+1]) == 1:
                break

    return '-'.join([chrom,str(pos+b),ref[b:ref_e+1],alt[b:alt_e+1]])

'''
given a group of variants, return chrom, start and stop
all variants have to be on the same chrom
dirty tolerant
'''
def get_chrom_start_stop(vs):
    chrom = vs[0].split('-')[0]
    vs_arrays = [v.split('-') for v in vs]
    starts = [int(v[1]) for v in vs_arrays]
    stops = [starts[i] + len(vs_arrays[i][2]) for i in range(len(vs))]
    start = min(starts) - 1
    stop = max(stops) + 1
    return chrom,start,stop

