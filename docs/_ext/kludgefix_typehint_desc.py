"""Kludge fix to typehints in parameter descriptions when using a restructured text builder.

When using "autodoc_typehints = 'description'", Sphinx will add a literal emphasis around every
signature node in the docstring description. The result is undesired because reStructuredText does
not recognize nested emphasis. For example, a type hint like "Optional[int]" becomes
"*Optional**[**int**]*". This fix modifies the behavior so that the type hint in the description
becomes "*Optional[int]*".
"""
from typing import Any, Dict, List, Tuple
from docutils import nodes
from docutils.nodes import Node
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.domains.python import PyXrefMixin
from sphinx.environment import BuildEnvironment
from sphinx.util.docfields import TypedField
from sphinx.util.typing import TextlikeNode

if False:
    # For type annotation
    from typing import Type  # for python3.5.1


def setup(app: Sphinx) -> Dict[str, Any]:
    """Register the extension."""
    _patch_python_domain()
    return {'version': '0.0.1', 'parallel_read_safe': True}


def _patch_python_domain() -> None:
    import sphinx.domains.python
    from sphinx.locale import _
    sphinx.domains.python.PyObject.doc_field_types.append(
        PyMultiTypedField('multi_type_param', label=_('Parameters'),
                          names=('param', 'parameter', 'arg', 'argument'),
                          typerolename='class', typenames=('paramtype', 'type'),
                          can_collapse=True))


class PyMultiTypedField(PyXrefMixin, TypedField):
    """A new multi typed field in the Python domain.

    Modified from sphinx.domains.python.PyTypedField and sphinx.util.docfields.TypedField.
    """

    def make_xref(self, rolename: str, domain: str, target: str,
                  innernode: "Type[TextlikeNode]" = nodes.generated,
                  contnode: Node = None, env: BuildEnvironment = None) -> Node:
        """Add unadorned nodes.

        Modified from sphinx.domains.python.PyTypedField. Use 'nodes.generated' instead of
        'addnodes.literal_emphasis'.
        """
        if rolename == 'class' and target == 'None':
            # None is not a type, so use obj role instead.
            rolename = 'obj'

        return super().make_xref(rolename, domain, target, innernode, contnode, env)

    def make_field(self, types: Dict[str, List[Node]], domain: str,
                   items: Tuple, env: "BuildEnvironment" = None) -> nodes.field:
        """Add emphasis once around the type hint.

        Modified from sphinx.util.docfields.TypedField.
        """
        def handle_item(fieldarg: str, content: str) -> nodes.paragraph:
            par = nodes.paragraph()
            par.extend(self.make_xrefs(self.rolename, domain, fieldarg,
                                       addnodes.literal_strong, env=env))
            if fieldarg in types:
                par += nodes.Text(' (*')
                # NOTE: using .pop() here to prevent a single type node to be
                # inserted twice into the doctree, which leads to
                # inconsistencies later when references are resolved
                fieldtype = types.pop(fieldarg)
                if len(fieldtype) == 1 and isinstance(fieldtype[0], nodes.Text):
                    typename = fieldtype[0].astext()
                    par.extend(self.make_xrefs(self.typerolename, domain, typename,
                                               nodes.generated, env=env))
                else:
                    par += fieldtype
                par += nodes.Text('*)')
            par += nodes.Text(' -- ')
            par += content
            return par

        fieldname = nodes.field_name('', self.label)
        if len(items) == 1 and self.can_collapse:
            fieldarg, content = items[0]
            bodynode = handle_item(fieldarg, content)  # type: nodes.Node
        else:
            bodynode = self.list_type()
            for fieldarg, content in items:
                bodynode += nodes.list_item('', handle_item(fieldarg, content))
        fieldbody = nodes.field_body('', bodynode)
        return nodes.field('', fieldname, fieldbody)
