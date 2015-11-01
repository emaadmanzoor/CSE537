#!/usr/bin/env bash
for testfile in tests/*.txt;
do
  python convert2CNF.py $testfile $testfile.cnf;
  minisat $testfile.cnf $testfile.sat
done
