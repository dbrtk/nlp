
import os
import shutil
from typing import List

from .config.appconf import TEXT_FOLDER
from .data import DataFolder
from .errors import MatrixFileDoesNotExist
from .word_count import CorpusDir, process_lemma_word
from .views import call_factorize


class IntegrityCheck(object):

    def __init__(self, containerid: str = None, path: str = None):

        if not os.path.isdir(path):
            raise ValueError(path)

        self.path = path
        self.corpusid = containerid

        self.doc_file_id = self.get_docids()

        self.matrix_data = DataFolder(containerid=containerid, path=path)

        self.computed_feats = self.matrix_data.available_feats

    def __call__(self):

        try:
            self.update_matrices()
        except MatrixFileDoesNotExist as _:
            # the matrices have not been computed; ValueError is raised when
            # retrieving doctitles.
            return True
        except Exception as err:
            # deleting all matrices when an unknown error happens
            # todo(): review this
            self.matrix_data.purge_matrix()

        return True

    def update_matrices(self):
        """Computing the matrices, taking into account docuemnts that have
        been added or removed.
        """
        added, removed = self.diff_docids()

        if added:
            self.add_texts(added)

        if removed:
            self.remove_texts(removed)

        self.make_matrix()
        self.update_features()

    def update_features(self):
        """Looping through all the features and updating these."""
        for feats in self.computed_feats:
            shutil.rmtree(feats.get('path'))
            call_factorize(path=self.path,
                           corpusid=self.corpusid,
                           feats=int(feats.get('featcount')))

    def data_file_ids(self, docids):
        """Returns a list of file ids that map to the doc ids in doc_file_id.
        """
        return [_ for _ in self.doc_file_id if _ in docids]

    def add_texts(self, docids):
        """Adding new texts (documents) to the corpus."""
        inst = CorpusDir(

            added_texts=[_ for _ in self.data_file_ids(docids)],
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

    def remove_texts(self, del_ids: List[str] = None):
        """Removing the texts from all matrices."""

        allwords = self.matrix_data.allwords
        docwords = self.matrix_data.docwords
        docids = self.matrix_data.doctitles

        indices = {_: docids.index(_) for _ in del_ids}
        # cleaning up allwords
        for docid, idx in indices.items():
            for word, count in docwords[idx].items():
                allwords[word] -= count
                if allwords[word] < 0:
                    raise ValueError(docid)

        indices = indices.values()
        docids = [item for idx, item in enumerate(docids)
                  if idx not in indices]
        docwords = [item for idx, item in enumerate(docwords)
                    if idx not in indices]
        self.id_word_check(docids, docwords)
        for obj in [
            {'objname': 'allwords', 'data': allwords},
            {
                'objname': 'docwords',
                'data': docwords
            },
            {
                'objname': 'doctitles',
                'data': docids
            },
        ]:
            self.matrix_data.remove_file(obj.get('objname'))
            self.matrix_data.make_file(**obj)

    @property
    def corpus_path(self):
        _ = os.path.join(self.path, TEXT_FOLDER)
        if not os.path.isdir(_):
            raise ValueError(_)
        return _

    def get_docids(self, validate_id: bool = False) -> tuple:
        """Retrieve document ids (DataObject) and file ids."""
        # path = self.corpus_path
        # out = []
        # for doc in os.listdir(self.corpus_path):
        #     _id = open(os.path.join(path, doc), 'r').readline().strip()
        #     out.append((_id, doc,))
        return tuple(os.listdir(self.corpus_path))

    def diff_docids(self) -> tuple:
        """Returns the ids that have been added and the ones that have been
        removed from the corpus.
        """
        file_ids = list(_ for _ in self.doc_file_id)
        existing_docids = self.matrix_data.doctitles
        return (
            # added doc ids
            [_ for _ in file_ids if _ not in existing_docids],
            # removed doc ids
            [_ for _ in existing_docids if _ not in file_ids],
        )

    def docid_words(self):
        """Returns the mapping between docids and docwords."""
        return dict(zip(
            self.matrix_data.doctitles, self.matrix_data.docwords))

    def id_word_check(self, docids, docwords):
        """Check that documents that exist are in the right order."""
        mapping = self.docid_words()

        if len(docids) != len(docwords):
            raise ValueError(docids)
        for idx, docid in enumerate(docids):
            if docid in mapping:
                assert mapping[docid] == docwords[idx]
