# pyright: reportUnusedFunction=false
import random
from datetime import datetime

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

from app.common import date_to_str
from app.data.repository import Contact, ContactsRepository
from app.validators import ContactValidator

repo = ContactsRepository()
repo.generate_contacts_data(1000)


def init_app(app: Flask):
    ...

    @app.get('/')
    @app.get('/contacts')
    def contacts_index():
        action = request.args.get('action')
        query = request.args.get('query', '')
        messages = get_flashed_messages(with_categories=True)
        page = request.args.get('page', 1, type=int)

        if action == 'reset':
            contacts = repo.read()
            query = ''

        else:
            contacts = repo.find_by_name_or_last_name(query)

        contacts = sorted(
            contacts,
            key=lambda c: (
                (c.last_name or '').lower(),
                (c.first_name or '').lower(),
            ),
        )

        search_placeholder = random.choice(
            [
                'Ну этот, как его...',
                'Ну эта, как ее...',
                'Тот, который...',
                'Та, которая...',
                'Человек с именем...',
            ]
        )

        total = len(contacts)
        per_page = 10
        pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        contacts_page = contacts[start:end]

        current_year = datetime.now().year

        return render_template(
            'contacts/index.html',
            search=query,
            search_placeholder=search_placeholder,
            contacts=contacts_page,
            current_year=current_year,
            messages=messages,
            page=page,
            pages=pages,
        )

    @app.route('/contacts/<id>')
    def contacts_show(id: str):
        contact = repo.find_by_id(id)
        messages = get_flashed_messages(with_categories=True)

        if contact is None:
            abort(404, description='Контакты не найдены')

        return render_template(
            'contacts/show.html',
            contact=contact,
            date_to_str=date_to_str,
            messages=messages,
        )

    @app.route('/contacts/random')
    def contacts_random_show():
        contact = random.choice(repo.read())

        return render_template(
            'contacts/show.html', contact=contact, date_to_str=date_to_str
        )

    @app.route('/contacts/new')
    def contacts_new():
        contact = Contact.empty()

        return render_template(
            'contacts/new.html', contact=contact, errors={}, form_data={}
        )

    @app.post('/contacts')
    def contacts_post():
        form_data = request.form
        validator = ContactValidator(form_data)
        errors = validator.validate()
        contact = Contact.from_form_data(form_data)

        if errors:
            return render_template(
                'contacts/new.html',
                form_data=form_data,
                errors=errors,
            ), 422

        repo.create(contact)

        flash('Контакт добавлен', 'success')

        return redirect(url_for('contacts_index'))

    @app.route('/contacts/<id>/edit')
    def contacts_edit(id: str):
        contact = repo.find_by_id(id)

        if not contact:
            abort(404, description='Контакт не найден')

        return render_template(
            'contacts/edit.html',
            contact=contact,
            errors={},
        )

    @app.post('/contacts/<id>')
    def contacts_patch(id: str):
        form_data = request.form
        validator = ContactValidator(form_data)
        errors = validator.validate()
        contact = repo.find_by_id(id)

        if not contact:
            abort(404, description='Контакт не найден')

        updated_contact = Contact.from_form_data(form_data)
        updated_contact.id = id

        if errors:
            return render_template(
                'contacts/edit.html',
                form_data=form_data,
                errors=errors,
                contact=updated_contact,
            ), 422

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

        flash('Контакт отредактирован', 'success')

        return redirect(url_for('contacts_show', id=id))

    @app.post('/contacts/<id>/delete')
    def contacts_delete(id: str):
        repo.delete(id)

        flash('Контакт удален', 'success')

        return redirect(url_for('contacts_index'))
