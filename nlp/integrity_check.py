
import os
import shutil

import bson

from .data import CorpusMatrix
from .word_count import CorpusDir, process_lemma_word
from .views import call_factorize


class IntegrityCheck(object):

    def __init__(self, corpusid: str = None, path: str = None):

        if not os.path.isdir(path):
            raise ValueError(path)

        self.path = path
        self.corpusid = corpusid

        self.doc_file_id = self.get_docids()

        self.matrix_data = CorpusMatrix(corpusid=corpusid, path=path)

    def __call__(self):

        added, removed = self.diff_docids()

        if added:
            self.add_texts(added)

        if removed:
            self.remove_texts(removed)

        self.make_matrix()
        self.update_features()

        return True

    def update_features(self):
        """Looping through all the features and updating these."""
        for feats in self.matrix_data.available_feats:
            shutil.rmtree(feats.get('path'))
            call_factorize(path=self.path,
                           corpusid=self.corpusid,
                           feats=int(feats.get('featcount')))

    def data_file_ids(self, docids):
        """Returns a list of file ids that map to the doc ids in doc_file_id.
        """
        return [_ for _ in self.doc_file_id if _[0] in docids]

    def add_texts(self, docids):
        """Adding new texts (documents) to the corpus."""
        inst = CorpusDir(

            added_texts=[_[1] for _ in self.data_file_ids(docids)],
            corpus_path=self.corpus_path,

            allwords=self.matrix_data.allwords,
            articletitles=self.matrix_data.doctitles,
            articlewords=self.matrix_data.docwords,
            lemma_words=self.matrix_data.lemma_to_dict,
        )
        inst()
        for obj in [
            {'objname': 'allwords', 'data': inst.allwords},

            {'objname': 'docwords', 'data': inst.articlewords},
            {'objname': 'doctitles', 'data': inst.articletitles},

            {'objname': 'lemma', 'data': list(
                process_lemma_word(inst.lemma_word)), 'ext': 'json'}
        ]:
            self.matrix_data.remove_file(obj.get('objname'))
            self.matrix_data.make_file(**obj)

    def make_matrix(self):

        for item in ['wordvec', 'wordmatrix', 'vectors']:
            self.matrix_data.remove_file(item)

        self.matrix_data.compute_matrices()

    def remove_texts(self, docids):
        pass

    @property
    def corpus_path(self):
        _ = os.path.join(self.path, 'corpus')
        if not os.path.isdir(_):
            raise ValueError(_)
        return _

    def wordmatrix_shape(self):

        pass

    def check_matrix(self):

        docids = self.get_docids(validate_id=True)

    def get_docids(self, validate_id: bool = False) -> tuple:
        """Retrieve document ids (DataObject) and file ids."""
        path = self.corpus_path
        out = []
        for doc in os.listdir(self.corpus_path):
            _id = open(os.path.join(path, doc), 'r').readline().strip()
            if validate_id:
                try:
                    bson.ObjectId(_id)
                except (bson.errors.InvalidId, TypeError,):
                    raise ValueError(_id)

            out.append((_id, doc,))
        return tuple(out)

    def diff_docids(self):

        docids = list(_[0] for _ in self.doc_file_id)
        existing_docids = self.matrix_data.doctitles

        return (
            # added texts - doc_file_id
            list(set(docids).difference(set(existing_docids))),
            # removed texts - doc_file_id
            list(set(existing_docids).difference(set(docids))),
        )

