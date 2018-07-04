from rdflib.namespace import Namespace
from ..context import Context
from ..datasource import Informational, DataSource
from .. import CONTEXT
from .common_data import DS_NS


class DataWithEvidenceDataSource(DataSource):
    evidence_context_property = Informational(display_name='Evidence context',
                                              property_name='evidence_context',
                                              description='The context in which evidence'
                                                          ' for the "Data context" is defined')
    data_context_property = Informational(display_name='Data context',
                                          property_name='data_context',
                                          description='The context in which primary data'
                                                      ' for this data source is defined')

    combined_context_property = Informational(display_name='Combined context',
                                              property_name='combined_context',
                                              description='Context importing both the data and evidence contexts')

    rdf_namespace = Namespace(DS_NS['DataWithEvidenceDataSource#'])

    def __init__(self, *args, **kwargs):
        super(DataWithEvidenceDataSource, self).__init__(*args, **kwargs)

        self.data_context = Context.contextualize(self.context)(ident=self.identifier + '-data',
                                                                imported=(CONTEXT,))
        self.evidence_context = Context.contextualize(self.context)(ident=self.identifier + '-evidence',
                                                                    imported=(CONTEXT,))

        self.combined_context = Context.contextualize(self.context)(ident=self.identifier,
                                                                    imported=(self.data_context,
                                                                              self.evidence_context))

        self.data_context_property(self.data_context.rdf_object)
        self.evidence_context_property(self.evidence_context.rdf_object)
        self.combined_context_property(self.combined_context.rdf_object)

        self.__ad_hoc_contexts = dict()

    def data_context_for(self, **kwargs):
        ctx = self.context_for(**kwargs)
        self.data_context.add_import(ctx)
        return ctx

    def context_for(self, **kwargs):
        key = "&".join(k + "=" + kwargs[k].identifier for k in sorted(kwargs.keys()))
        res = self.__ad_hoc_contexts.get(key)
        if res is None:
            ctxid = self.identifier + '/context_for?' + key
            self.__ad_hoc_contexts[key] = Context.contextualize(self.context)(ident=ctxid)
            res = self.__ad_hoc_contexts[key]
        return res


__yarom_mapped_classes__ = (DataWithEvidenceDataSource,)
