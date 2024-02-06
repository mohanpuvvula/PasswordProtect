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
app.config['MAIL_ATTACHMENTS'] = os.path.join(app.instance_path, 'encrypt')
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
            flash(f"File {filename} uploaded", 'success')

        return redirect(url_for('encryption.encryption'))
    else:
        return render_template('upload.html', user=current_user)

def encrypt_pdfs(input_folder, output_folder, password):
    os.makedirs(output_folder, exist_ok=True)
    encrypted_files = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, 'encrypt_' + filename)

            with open(input_path, 'rb') as input_file:
                pdf_writer = PdfWriter()

                pdf_reader = PdfReader(input_file)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                pdf_writer.encrypt(password)

                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)

            print(f"File encrypted: {output_path}")
            encrypted_files.append('encrypt_' + filename)

    return encrypted_files

@encryption_bp.route('/add_encryption', methods=['GET', 'POST'])
@login_required
def encryption():
    user_email = session.get('user_email')
    if not user_email:
        flash('User not authenticated', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        use_random_password = bool(request.form.get('use_random_password'))
        if use_random_password:
            password = secrets.token_urlsafe(12)
            flash(f"Generated random password: {password}", 'info')
        else:
            password = request.form['password']

        output_folder = app.config['ENCRYPT_FOLDER']
        encrypted_files = encrypt_pdfs(app.config['UPLOAD_FOLDER'], output_folder, password)
        flash("Files encrypted", 'success')

        send_email(mail, user_email, password, output_folder, encrypted_files)

        return render_template('encryption_success.html', output_folder=output_folder, user=current_user)
    else:
        return render_template('add_encryption.html', user=current_user)


def send_email(mail, user_email, password, output_folder, encrypted_files):
    subject = 'Encrypted PDF'
    sender_email = 'manoj4322@gmail.com'
    recipient_email = user_email

    message = Message(subject, sender=sender_email, recipients=[recipient_email])
    message.body = f"Dear user, \n\nPlease find the encrypted PDFs attached. Password: {password}"

    try:
        with app.app_context():
            for filename in encrypted_files:
                pdf_file_path = os.path.join(output_folder, filename)
                with open(pdf_file_path, 'rb') as pdf_file:
                    message.attach(filename=filename, content_type='application/pdf', data=pdf_file.read())
            mail.send(message)
        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")

@encryption_bp.route('/download_zip', methods=['GET', 'POST'])
def download_zip():
    folder_path = app.config['ENCRYPT_FOLDER']
    zip_file_path = os.path.join(folder_path, 'encrypted_files.zip')

    with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_STORED) as zipfolder:
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)
                zipfolder.write(file_path, os.path.relpath(file_path, folder_path))

    return send_file(zip_file_path, as_attachment=True, download_name='encrypted_files.zip')


app.register_blueprint(encryption_bp)

if __name__ == '__main__':
    app.run(debug=True)
