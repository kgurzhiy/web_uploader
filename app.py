import os
from datetime import datetime
from datetime import timedelta

from flask import request, render_template

from my_conf import app, db, APP_ROOT, celery
from my_forms import FormFile
from my_models import Entry


@app.route('/')
def index():
    db.create_all(app=app)
    form = FormFile()
    return render_template('upload_new.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'files/folder')

    if not os.path.isdir(target):
        os.mkdir(target)

    file_ = request.files.getlist('file')[0]
    expiration_time = int(request.form.get('expiration_time'))
    form = FormFile(expiration_time=expiration_time, file=file_)
    if form.validate() and form.file.__sizeof__() > 0:
        current_time = datetime.now()
        time_to_die = timedelta(minutes=expiration_time) + current_time
        entry = Entry(
            file=file_.read(),
            filename=file_.filename,
            time_to_die=time_to_die,
        )
        db.session.add(entry)
        db.session.commit()
        for upload in request.files.getlist('file'):
            filename = upload.filename
            destination = '/'.join([target, filename])
            upload.save(destination)
        entries = Entry.query.all()
        return render_template('gallery.html', entries=entries)
    else:
        pass


@celery.task
def delete():
    Entry.query.filter(Entry.time_to_die <= datetime.now()).delete()


@app.route('/gallery')
def get_gellery():
    entries = Entry.query.all()
    return render_template('gallery.html', entries=entries)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
