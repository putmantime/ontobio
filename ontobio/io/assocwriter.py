"""
Classes for exporting associations.

"""
import logging

def _str(v):
    if v is None:
        return ""
    else:
        return str(v)

class AssocWriterConfig():
    """
    Placeholder class for configuration object for all writers
    """
    pass

class AssocWriter():
    """
    Abstract superclass of all association writer objects (Gpad, GAF)
    """
    def _split_prefix(self, ref):
        id = ref['id']
        [prefix, local_id] = id.split(':', maxsplit=1)
        return prefix, local_id

    def _write_row(self, vals):
        line = "\t".join([_str(v) for v in vals])
        if self.file:
            self.file.write(line+"\n")
        else:
            print(line)

    def _extension_expression(self, assoc):
        xs = []
        for e in assoc.get('object_extensions',[]):
            xs.append('{}({})'.format(e['property'], e['filler']))
        return ",".join(xs)

    def write_assoc(self, assoc):
        """
        Write a single association to a line in the output file
        """
        pass  ## Implemented in subclasses

    def write(self, assocs, meta=None):
        """
        Write a complete set of associations to a file

        Arguments
        ---------
        assocs: list[dict]
            A list of association dict objects
        meta: Meta
            metadata about association set (not yet implemented)

        """
        for a in assocs:
            self.write_assoc(a)

class GpadWriter(AssocWriter):
    """
    Writes Associations in GPAD format
    """
    def __init__(self, file=None):
        self.file = file

    def write_assoc(self, assoc):
        """
        Write a single association to a line in the output file
        """
        subj = assoc['subject']

        db, db_object_id = self._split_prefix(subj)

        rel = assoc['relation']
        qualifier = rel['id']
        if assoc['negated']:
            qualifier = 'NOT|' + qualifier

        goid = assoc['object']['id']

        ev = assoc['evidence']
        evidence = ev['type']
        withfrom = "|".join(ev['with_support_from'])
        reference = "|".join(ev['has_supporting_reference'])

        date = assoc['date']
        assigned_by = assoc['provided_by']

        annotation_properties = '' # TODO
        interacting_taxon_id = '' ## TODO

        vals = [db,
                db_object_id,
                qualifier,
                goid,
                reference,
                evidence,
                withfrom,
                interacting_taxon_id, # TODO
                date,
                assigned_by,
                self._extension_expression(assoc),
                annotation_properties]

        self._write_row(vals)

class GafWriter(AssocWriter):
    """
    Writes Associations in GAF format. Not yet implemented
    """
    def __init__(self, file=None):
        self.file = file

    def write_assoc(self, assoc):
        """
        Write a single association to a line in the output file
        """
        subj = assoc['subject']

        db, db_object_id = self._split_prefix(subj)

        rel = assoc['relation']
        qualifier = rel['id']
        if assoc['negated']:
            qualifier = 'NOT|' + qualifier

        goid = assoc['object']['id']

        ev = assoc['evidence']
        evidence = ev['type']
        withfrom = "|".join(ev['with_support_from'])
        reference = "|".join(ev['has_supporting_reference'])

        date = assoc['date']
        assigned_by = assoc['provided_by']

        annotation_properties = '' # TODO
        interacting_taxon_id = '' ## TODO
        gene_product_isoform = '' ## TODO

        aspect = assoc['aspect']
        taxon = None
        if 'taxon' in subj:
            taxon = subj['taxon']['id']

        vals = [db,
                db_object_id,
                subj.get('label'),
                qualifier,
                goid,
                reference,
                evidence,
                withfrom,
                aspect,
                "|".join(subj.get('full_name',[])),
                "|".join(subj.get('synonyms',[])),
                subj.get('type'),
                taxon,
                date,
                assigned_by,
                self._extension_expression(assoc),
                gene_product_isoform]

        self._write_row(vals)
