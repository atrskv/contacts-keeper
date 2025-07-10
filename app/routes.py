# pyright: reportUnusedFunction=false
from flask import (
    Flask,
    abort,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.datastructures.structures import ImmutableMultiDict

from app.common import date_to_str
from app.data.repository import Contact, ContactsRepository
from app.validators import ContactValidator

repo = ContactsRepository()
repo.generate_contacts_data()


def init_app(app: Flask):
    ...

    @app.get('/')
    @app.get('/contacts')
    def contacts_index():
        action = request.args.get('action')
        query = request.args.get('query', '')
        messages = get_flashed_messages(with_categories=True)

        if action == 'reset':
            contacts = repo.read()
            query = ''

        else:
            contacts = repo.find_by_name_or_last_name(query)

        return render_template(
            'contacts/index.html',
            search=query,
            contacts=contacts,
            messages=messages,
        )

    @app.route('/contacts/<id>')
    def contacts_show(id: str):
        contact = repo.find_by_id(id)

        if contact is None:
            abort(404, description='Contact not found')

        return render_template(
            'contacts/show.html', contact=contact, date_to_str=date_to_str
        )

    @app.route('/contacts/new')
    def contacts_new():
        contact: Contact = Contact.empty()
        errors: dict[str, str] = {}

        return render_template(
            'contacts/new.html', contact=contact, errors=errors
        )

    @app.post('/contacts')
    def contacts_post():
        form_data: ImmutableMultiDict[str, str] = request.form
        validator = ContactValidator(form_data)
        errors = validator.validate()
        contact = Contact.from_form_data(form_data)

        if errors:
            return render_template(
                'contacts/new.html', contact=contact, errors=errors
            ), 422

        repo.create(contact)

        flash('Контакт добавлен', 'success')

        return redirect(url_for('contacts_index'))

    @app.route('/contacts/<id>/edit')
    def contacts_edit(id: str):
        contact = repo.find_by_id(id)
        errors: dict[str, str] = {}

        if not contact:
            abort(404, description='Контакт не найден')

        return render_template(
            'contacts/edit.html', contact=contact, errors=errors
        )

    @app.post('/contacts/<id>')
    def contacts_patch(id: str):
        form_data: ImmutableMultiDict[str, str] = request.form
        validator: ContactValidator = ContactValidator(form_data)
        errors = validator.validate()
        contact = repo.find_by_id(id)

        if not contact:
            abort(404, description='Контакт не найден')

        if errors:
            return render_template(
                'contacts/edit.html', contact=contact, errors=errors
            ), 422

        updated_contact = Contact.from_form_data(form_data)

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

        return redirect(url_for('contacts_show', id=id))

    @app.post('/contacts/<id>/delete')
    def contacts_delete(id: str):
        repo.delete(id)

        flash('Контакт удален', 'success')

        return redirect(url_for('contacts_index'))
