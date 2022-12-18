#!/usr/bin/env python3

from secrets import randbelow
import sys

class NestedMarkovChain:
    def __init__(self, desc_obj):
        defdat = list(desc_obj)
        if not NestedMarkovChain.lint(defdat):
            raise ValueError
        self.desc = defdat

    def __repr__(self):
        return 'NestedMarkovChain({})'.format(repr(self.desc))

    def lint(defdat):
        # plus 1 special entry/exit element at the end.
        desclen = len(defdat)
        if not isinstance(defdat, list):
            return False
        if desclen < 2:
            return False
        
        hasexit = []
        for i in range(desclen):
            e = defdat[i]
            if not isinstance(e, dict):
                return False
            if i < desclen - 1:
                if e['sym'] is not None:
                    if not isinstance(e['sym'], NestedMarkovChain):
                        return False
            if not isinstance(e['xsit'], list):
                return False
            if len(e['xsit']) != desclen:
                return False
            hasexit.append(e['xsit'][-1] != 0)
        
        for rnd in range(desclen):
            for i in range(desclen):
                if hasexit[i]:
                    continue
                for j in range(desclen):
                    if hasexit[j] and defdat[i]['xsit'][j] > 0:
                        hasexit[i] = True
                        break

        return all(hasexit)

    def __iter__(self):
        self.lastat = None
        return self

    def __next__(self):
        c = None
        if self.lastat is None:
            c = self.desc[-1]
        else:
            c = self.desc[self.lastat]

        s = randbelow(65536)
        p = sum(c['xsit'])
        s *= p
        a = 0
        for i in range(len(self.desc)):
            a += c['xsit'][i] * 65536
            if a < s:
                continue
            if i == len(self.desc) - 1:
                raise StopIteration()
            c = self.desc[i]
            self.lastat = i
            if c['sym'] is None:
                return i
            else:
                return c['sym']

def NMCFactory(n):
    while True:
        cand = [
            { 'sym': None, 'xsit': [ 0 ] * (n+1) } for j in range(n+1)
        ]
        for i in range(n+1):
            cand[i]['xsit'][(i*53+23)%n] = 23
            cand[i]['xsit'][(i*53+43)%n] = 11
            cand[i]['xsit'][(i*53+83)%n] = 5
            cand[i]['xsit'][n] = 2
        if NestedMarkovChain.lint(cand):
            return cand

def main_nested():
    desc = NMCFactory(16)
    for i in range(10):
        desc[i]['sym'] = NestedMarkovChain(NMCFactory(256))
    nmc = NestedMarkovChain(desc)
    for mc in nmc:
        if isinstance(mc, NestedMarkovChain):
            for u in mc:
                sys.stdout.buffer.write(bytes([u]))
        else:
            dyn = NestedMarkovChain(NMCFactory(256))
            for u in dyn:
                sys.stdout.buffer.write(bytes([u]))

def main_plain():
    desc = NMCFactory(256)
    mc = NestedMarkovChain(desc)
    for v in mc:
        sys.stdout.buffer.write(bytes([v]))

if __name__ == "__main__":
    main_nested()
