python tests.py
for i in `seq 1 5`; do python pegSolitaire.py --input tests/game$i.txt --flag 0; done
