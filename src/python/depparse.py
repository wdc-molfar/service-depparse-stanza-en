#!/usr/bin/python

import io
import json
import sys
import traceback

import stanza

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


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
            text = input_json['params']['text']
            output = None
            doc = nlp(text)
            if method == 'extract_dependencies':
                output = []
                for sentence in doc.sentences:
                    for (word1, dep, word2) in sentence.dependencies:
                        output.append(dict(
                            word1=word1.lemma,
                            dep=dep,
                            word2=word2.lemma
                        ))
                output = {"request": input_json, "response": {"dependencies": output}}
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
