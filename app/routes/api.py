import random

from flasgger import Swagger
from flask import jsonify, request

from app.data.repository import Contact
from app.validators import ContactValidator


def init_api(app, repo):
    app.config['SWAGGER'] = {'title': 'Contacts Keeper'}

    template = {
        'info': {
            'title': 'Contacts',
            'description': 'A simple API for managing contacts',
        },
        'basePath': '/api',
        'definitions': {
            'Contact': {
                'type': 'object',
                'properties': {
                    'first_name': {
                        'type': 'string',
                        'example': 'Alice',
                    },
                    'last_name': {'type': 'string', 'example': 'Johnson'},
                    'email': {
                        'type': 'string',
                        'example': 'alice@example.com',
                    },
                    'phone': {'type': 'string', 'example': '+1-800-555-1234'},
                    'gender': {
                        'type': 'string',
                        'enum': ['male', 'female', 'other'],
                        'example': 'female',
                    },
                    'date_of_birth': {
                        'type': 'string',
                        'example': '01.11.1998',
                    },
                    'priority': {
                        'type': 'string',
                        'enum': ['regular', 'high'],
                        'example': 'regular',
                    },
                    'category': {
                        'type': 'string',
                        'enum': [
                            'not_selected',
                            'friends',
                            'family',
                            'work',
                            'clients',
                        ],
                        'example': 'friends',
                    },
                    'channels': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'enum': [
                                'can_call',
                                'can_message',
                                'email_preferred',
                            ],
                        },
                        'example': ['can_call', 'can_message'],
                    },
                    'current_address': {
                        'type': 'string',
                        'example': '123 Main St, Springfield',
                    },
                },
                'required': ['first_name'],
            }
        },
    }

    Swagger(app, template=template)

    @app.get('/api/contacts/')
    def api_contacts_index():
        """
        Get a list of contacts with pagination
        ---
        tags:
          - CRUD
        parameters:
          - name: query
            in: query
            type: string
            required: false
            description: search by first name or last name
          - name: page
            in: query
            type: integer
            required: false
            default: 1
            description: Page number
        responses:
          200:
            description: List of contacts
            schema:
              type: object
              properties:
                contacts:
                  type: array
                  items:
                    $ref: '#/definitions/Contact'
                total:
                  type: integer
                pages:
                  type: integer
                page:
                  type: integer
        """

        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)

        if query:
            contacts = repo.find_by_name_or_last_name(query)
        else:
            contacts = repo.read()

        # TODO: Refactor
        contacts = sorted(
            contacts,
            key=lambda c: (
                (c.last_name or '').lower(),
                (c.first_name or '').lower(),
            ),
        )

        # TODO: Refactor
        total = len(contacts)
        per_page = 10
        pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        contacts_page = contacts[start:end]

        return jsonify(
            {
                'contacts': [contact.to_dict() for contact in contacts_page],
                'total': total,
                'pages': pages,
                'page': page,
            }
        )

    @app.get('/api/contacts/<id>/')
    def api_contacts_show(id):
        """
        Get contact by id
        ---
        tags: [CRUD]
        parameters:
          - name: id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Contact found
          404:
            description: Contact not found
        """

        contact = repo.find_by_id(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify(contact.to_dict())

    @app.get('/api/contacts/random/')
    def api_contacts_random():
        """
        Get a random contact
        ---
        tags: [Other]
        responses:
          200:
            description: A random contact
        """

        contact = random.choice(repo.read())

        return jsonify(contact.to_dict())

    @app.post('/api/contacts/')
    def api_contacts_create():
        """
        Create a new contact
        ---
        tags: [CRUD]
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/Contact'
        responses:
          201:
            description: Contact created
            schema:
              $ref: '#/definitions/Contact'
          400:
            description: No data provided
          422:
            description: Validation errors
        """

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        validator = ContactValidator(data)
        errors = validator.validate()
        if errors:
            return jsonify({'errors': errors}), 422

        contact = Contact.from_json(data)

        repo.create(contact)

        return jsonify({'id': contact.id, **contact.to_dict()}), 201

    @app.put('/api/contacts/<id>/')
    def api_contacts_update(id):
        """
        Update a contact by id
        ---
        tags: [CRUD]
        consumes:
          - application/json
        parameters:
          - name: id
            in: path
            type: string
            required: true
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/Contact'
        responses:
          200:
            description: Contact updated
            schema:
              $ref: '#/definitions/Contact'
          400:
            description: No data provided
          404:
            description: Contact not found
          422:
            description: Validation errors
        """

        contact = repo.find_by_id(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        validator = ContactValidator(data)
        errors = validator.validate()
        if errors:
            return jsonify({'errors': errors}), 422

        updated_contact = Contact.from_json(data)
        updated_contact.id = id

        repo.update(
            id=id,
            first_name=updated_contact.first_name,
            last_name=updated_contact.last_name,
            gender=updated_contact.gender,
            phone=updated_contact.phone,
            email=updated_contact.email,
            date_of_birth=updated_contact.date_of_birth,
            priority=updated_contact.priority,
            category=updated_contact.category,
            channels=updated_contact.channels,
            current_address=updated_contact.current_address,
        )

        return jsonify(updated_contact.to_dict())

    @app.delete('/api/contacts/<id>/')
    def api_contacts_delete(id):
        """
        Delete contact by id
        ---
        tags: [CRUD]
        parameters:
          - name: id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Contact deleted
          404:
            description: Contact not found
        """

        contact = repo.find_by_id(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        repo.delete(id)

        return '', 204
