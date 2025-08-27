import random

from flask import jsonify, request

from app.data import repo
from app.data.repository import Contact
from app.validators import ContactValidator


def init_api(app):
    ...

    @app.get('/api/contacts/')
    def api_contacts_index():
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
        contact = repo.find_by_id(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify(contact.to_dict())

    @app.get('/api/contacts/random/')
    def api_contacts_random():
        contact = random.choice(repo.read())

        return jsonify(contact.to_dict())

    @app.post('/api/contacts/')
    def api_contacts_create():
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
        contact = repo.find_by_id(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        repo.delete(id)

        return '', 204
