from .... import db
from ..models import (
    Template
)
from ..schemes import (
    TemplateSchema
)

from flask import Blueprint
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from flask_jwt_extended import (
    jwt_required,
    jwt_optional
)
from datetime import datetime
from sqlalchemy.orm.session import make_transient
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.exceptions import MethodNotAllowed, UnprocessableEntity


blueprint = Blueprint(
    'api.docker.templates',
    __name__,
    url_prefix='/api/docker/templates'
)


# endpoint: index
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@blueprint.route('/')
# @use_kwargs({'per_page': fields.Int(missing=10)}, locations=('query',))
# ...
def index():
    templates = Template.query.all()
    templates_schema = TemplateSchema(many=True)
    data = templates_schema.dump(templates, many=True)
    return jsonify({ 'data': data })

# endpoint: show
#  methods: GET
#   errors: 200 (OK) | 404 (Not Found)
@blueprint.route('/<int:id>')
def show(id):
    try:
        template = Template.query.get_or_404(id)
        template_schema = TemplateSchema()
        data = template_schema.dump(template)
        return jsonify({ 'data': data })
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

# endpoint: create
#  methods: POST
#   errors: 201 (Created) | [200 (OK) | 204 (No Content)] | 400 (Bad Request)
@blueprint.route('/', methods=['POST'])
@use_args(TemplateSchema(), location='json')
def create(args):
    '''curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"title":"First Template","url":"https://host.local/template.json"}' \
      http://127.0.0.1:5000/api/templates/
    '''
    template = Template(**args)
    try:
        db.session.add(template)
        db.session.commit()
    except IntegrityError as err:
        # TODO raises IntegrityError on duplicates (uniqueness)
        #       status
        pass

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })

# endpoint: edit
#  methods: PUT
#   errors: 201 (Created) | [200 (OK) | 204 (No Content)] | 409 (Conflict)
# endpoint: update
#  methods: PATCH
#   errors: ... 400 (Bad Request) | 409 (Conflict) | 415 (Unsupported Media Type)

# endpoint: delete/destroy
#  methods: DELETE (optional: POST)
#   errors: 204 (No Content) | 404 (Not Found)
@blueprint.route('/<int:id>', methods=['DELETE'])
# perhaps use webargs for id
def delete(id):
    '''curl --header "Content-Type: application/json" \
    -X "DELETE" \
    http://127.0.0.1:5000/api/templates/2
    '''
    # check error code and return json error
    try:
        template = Template.query.get_or_404(id)
        db.session.delete(template)
        db.session.commit()
    except IntegrityError as err:
        abort(400, { 'error': 'Bad Request' })

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data})

# ---

@blueprint.route('/<int:id>/refresh', methods=['POST'])
def refresh(id):
    template = Template.query.get_or_404(id)
    # ...

    db.session.delete(template)
    db.session.commit()

    make_transient(template)
    template.updated_at = datetime.utcnow()
    # template.items = items

    try:
        db.session.add(template)
        db.session.commit()
        print("Template \"" + template.title + "\" updated successfully.")
    except Exception as exc:
        db.session.rollback()
        raise

    template_schema = TemplateSchema()
    data = template_schema.dump(template)
    return jsonify({ 'data': data })
