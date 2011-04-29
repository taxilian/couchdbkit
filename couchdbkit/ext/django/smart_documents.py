# -*- coding: utf-8 -
#
# This file is an extension to couchdbkit and released under the MIT license.

from schema import Document, DateTimeProperty, ListProperty

class ExtendableDocument(Document):
    def __init__(self, *args, **kwargs):
        super(ExtendableDocument, self).__init__(*args, **kwargs)

    def save(self, **params):
        self.presave(**params)
        super(ExtendableDocument, self).save(**params)
        self.postsave(**params)

    def presave(self, **params):
        pass

    def postsave(self, **params):
        pass

class TimestampedDocument(ExtendableDocument):
    created = DateTimeProperty(verbose_name="Creation Time", auto_now_add=True, use_unix_timestamp=True)
    modified = DateTimeProperty(verbose_name="Creation Time", auto_now=True, use_unix_timestamp=True)

class RevisionedDocument(TimestampedDocument):
    revisions = ListProperty()

    def __init__(self, *args, **kwargs):
        self._rev_exclude = ["revisions", "doc_type", "created"]
        if "rev_exclude" in kwargs:
            self._rev_exclude.update(kwargs["rev_exclude"])
        super(RevisionedDocument, self).__init__(*args, **kwargs)

    def presave(self, **params):
        import copy
        old = copy.deepcopy(self._initialDoc)
        for key in self._initialDoc.keys():
            if key[:1] == "_" or key in self._rev_exclude:
                del old[key]
        self.revisions.insert(0, old)
