import math
from numpy import sqrt 
import numpy as np

def _repeated_seq_pos(text, seq_len):
    seq_pos = {}  
    for i, char in enumerate(text):
        next_seq = text[i:i+seq_len]
        if next_seq in seq_pos.keys():
            seq_pos[next_seq].append(i)
        else:
            seq_pos[next_seq] = [i]
    repeated = list(filter(lambda x: len(seq_pos[x]) >= 2, seq_pos))
    rep_seq_pos = [(seq, seq_pos[seq]) for seq in repeated]
    return rep_seq_pos

def _get_spacings(positions):
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]

def get_differencies(array):
    diffs = {}
    for key in array:
        diffs[key] = diffs.get(key, 0) + 1
    common_diff = diffs[max(diffs, key=lambda k: diffs[k])]
    min_accepted_diff = math.ceil(common_diff * 0.1)
    return [key for key in diffs if diffs[key] > min_accepted_diff]

def kasiski_test(cipher):
    gcd_table = []
    seq_spc = []
    for l in range(2, 25):
        seq_pos = _repeated_seq_pos(cipher, l)
        for seq, positions in seq_pos:
            seq_spc.append(_get_spacings(positions))
    spaces = [seq_spc[i][j] for i in range(len(seq_spc)) for j in range(len(seq_spc[i]))]
    for i in range(len(spaces)):
        for j in range(len(spaces)):
            gcd_table.append(math.gcd(spaces[i], spaces[j]))
    candidate_lengths = list(filter(lambda x:  x <= 20, gcd_table))
    sorted_gcds = sorted(set(gcd_table), key=lambda x: candidate_lengths.count(x), reverse=True)
    gcds = list(filter(lambda x:  x > 1,sorted_gcds))
    return gcds[0]