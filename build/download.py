#!/usr/bin/python

import sys

import stanza

model_lang = sys.argv[1]
model_dir = sys.argv[2]

# Download base model:
stanza.download(model_lang, model_dir)

# Download processors:
stanza.Pipeline(lang=model_lang, dir=model_dir, processors='tokenize,mwt,pos,lemma,ner,depparse')  #TODO: add coref
