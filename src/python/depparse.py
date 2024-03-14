#!/usr/bin/python

import io
import json
import sys
import traceback

import stanza

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


# Universal POS tags from https://universaldependencies.org/u/pos/
def get_possible_upos_tags():
    return [
        "ADJ",      # adjective
        "ADP",      # adposition
        "ADV",      # adverb
        "AUX",      # auxiliary
        "CCONJ",    # coordinating conjunction
        "DET",      # determiner
        "INTJ",     # interjection
        "NOUN",     # noun
        "NUM",      # numeral
        "PART",     # particle
        "PRON",     # pronoun
        "PROPN",    # proper noun
        "PUNCT",    # punctuation
        "SCONJ",    # subordinating conjunction
        "SYM",      # symbol
        "VERB",     # verb
        "X"         # other
    ]


if __name__ == '__main__':
    model_lang = sys.argv[1]
    model_dir = sys.argv[2]

    nlp = stanza.Pipeline(
        lang=model_lang,
        dir=model_dir,
        processors='tokenize,mwt,pos,lemma,ner,depparse',  #TODO: add coref
        download_method=stanza.DownloadMethod.REUSE_RESOURCES,
        logging_level='WARN'
    )
    input_json = None
    for line in input_stream:
        try:
            input_json = json.loads(line)
            method = input_json['method']

            if method == 'get_possible_upos_tags':
                tags = get_possible_upos_tags()
                output = {"request": input_json, "response": {"tags": tags}}
            else:
                text = input_json['params']['text']
                output = None
                doc = nlp(text)
                if method == 'extract_dependencies':
                    nodes = []
                    links = []
                    categories = get_possible_upos_tags()
                    upos_to_category_id_dict = {k: v for v, k in enumerate(categories)}
                    categories = [{"name": category} for category in categories]
                    output = []
                    for sent_id, sentence in enumerate(doc.sentences, start=1):
                        for word in sentence.words:
                            nodes.append(dict(
                                id=f'{sent_id}-{word.id}',
                                name=word.lemma,
                                value=word.text,
                                category=upos_to_category_id_dict[word.upos]
                            ))
                        for (source_word, dependency, target_word) in sentence.dependencies:
                            if dependency == 'root':
                                continue
                            links.append(dict(
                                source=f'{sent_id}-{source_word.id}',
                                value=dependency,
                                target=f'{sent_id}-{target_word.id}'
                            ))
                    output = {"request": input_json, "response": dict(nodes=nodes, links=links, categories=categories)}
        except BaseException as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()

            output = {"error": ''}
            output['error'] += "Exception type : %s; \n" % ex_type.__name__
            output['error'] += "Exception message : %s\n" % ex_value
            output['error'] += "Exception traceback : %s\n" % "".join(
                traceback.TracebackException.from_exception(ex).format()
            )

        output_json = json.dumps(output, ensure_ascii=False).encode('utf-8')
        sys.stdout.buffer.write(output_json)
        print()
