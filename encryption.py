from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash
from werkzeug.utils import secure_filename
import os
from flask import send_file
from PyPDF2 import PdfWriter, PdfReader
from flask_login import login_required, current_user
import zipfile
import secrets
from flask_mail import Mail, Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_login import login_required, current_user, logout_user, login_user


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'files')
app.config['ENCRYPT_FOLDER'] = os.path.join(app.instance_path, 'encrypt')
app.secret_key = 'xyzabc'
encryption_bp = Blueprint("encryption", __name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'manoj4322@gmail.com'
app.config['MAIL_PASSWORD'] = 'dqamznxurhgvzbcx'

mail = Mail(app)

@encryption_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        user_email = current_user.email
        session['user_email'] = user_email
        files = request.files.getlist('files')

        for f in files:
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(file_path)
            print(f"File {filename} uploaded")

        return redirect(url_for('encryption.encryption', file_path=file_path))
    else:
        return render_template('upload.html')


@encryption_bp.route('/add_encryption', methods=['GET', 'POST'])
def encryption():
    user_email = session.get('user_email')
    if not user_email:
        flash('User not authenticated', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        use_random_password = bool(request.form.get('use_random_password'))
        if use_random_password:
            password = secrets.token_urlsafe(12)
            print(f"Generated random password: {password}")
        else:
            password = request.form['password']

        file_path = request.args.get('file_path')

        if file_path:
            output_path = os.path.join(app.config['ENCRYPT_FOLDER'], 'encrypt_' + os.path.basename(file_path))
            encrypt_pdfs(file_path, output_path, password)
            print("File/files encrypted")

            send_email(mail, user_email, password, output_path)

            return render_template('encryption_success.html', output_path=output_path,
                                   file_name=os.path.basename(output_path))
        else:
            return render_template('error.html', message='File path is missing.')
    else:
        file_path = request.args.get('file_path')
        return render_template('add_encryption.html', file_path=file_path)


def send_email(mail, user_email, password, output_path):
    subject = 'Encrypted PDF'
    sender_email = 'manoj4322@gmail.com'
    recipient_email = user_email

    message = Message(subject, sender=sender_email, recipients=[recipient_email])
    message.body = f"Dear user, \n\nPlease find the encrypted PDF attached. Password: {password}"
    with open(output_path, 'rb') as pdf_file:
         message.attach(filename='encrypted_pdf.pdf', content_type='application/pdf', data=pdf_file.read())
    try:
        with app.app_context():
            mail.send(message)
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def encrypt_pdfs(file_path, output_path, password):
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(file_path)

    for page_number in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_number])

    pdf_writer.encrypt(password)

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)


@encryption_bp.route('/download_files', methods=['GET', 'POST'])
def download_files():
    file_name = request.args.get('file_name')
    if not file_name:
        return render_template('error.html', message='File name is missing.')

    folder_path = app.config['ENCRYPT_FOLDER']
    zip_file_path = os.path.join(folder_path, 'encryptedfile.zip')

    with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_STORED) as zipfolder:
        file_path = os.path.join(folder_path, file_name)
        zipfolder.write(file_path, os.path.relpath(file_path, folder_path))

    return send_file(zip_file_path, as_attachment=True, download_name='encryptedfile.zip')


@encryption_bp.route('/delete_files', methods=['GET', 'POST'])
def delete_files():
    output_path = session.get('output_path')
    if output_path and os.path.exists(output_path):
        os.remove(output_path)
        session.pop('output_path', None)
    print("File deleted successfully")
    return redirect(url_for('home'))

app.register_blueprint(encryption_bp)

if __name__ == '__main__':
    app.run(debug=True)
