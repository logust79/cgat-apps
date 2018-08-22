def clean_variant(v,left=True):
    # normalise variant.
    chrom,pos,ref,alt = v.split('-')
    pos = int(pos)
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
