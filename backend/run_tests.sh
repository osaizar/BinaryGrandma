#!/bin/bash

#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/metame64/NVAR/testing.json
#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/metame32/NVAR/testing.json
#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/pymetangine32/NVAR/testing.json
#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/pymetangine64/NVAR/testing.json
#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/pymetangine32/NMVAR/testing.json
#python binary_grandma_cli.py f ~/Dokumentuak/Modeling-Samples/metame32/NMVAR/testing.json

python /root/Documents/malmodel/engine_tests/generate_metame_samples.py nm
zip /root/Documents/malmodel/engine_tests/output/metame32/NVAR_ALT/metame32_model.zip /root/Documents/malmodel/engine_tests/output/metame32/NMVAR_ALT/*
python binary_grandma_cli.py m /root/Documents/malmodel/engine_tests/output/metame32/model_alt.json
