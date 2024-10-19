from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Check the file extension
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                return render(request, 'upload.html', {'error': 'Error processing the CSV file.'})
        elif filename.endswith('.xlsx'):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')  # Use 'openpyxl' for Excel files
            except Exception as e:
                return render(request, 'upload.html', {'error': 'Error processing the Excel file.'})
        else:
            return render(request, 'upload.html', {'error': 'Please upload a valid Excel or CSV file.'})

        # Generate a summary of the data
        summary = df.describe().to_string()

        # Send the summary via email
        send_mail(
            'Python Assignment - Rahul Mirji',
            summary,
            settings.EMAIL_HOST_USER,
            ['tech@themedius.ai'],
            fail_silently=False,
        )

        # Store summary in the session so it can be passed to the summary view
        request.session['summary'] = summary

        return redirect('summary')

    return render(request, 'upload.html')

def summary(request):
    # Fetch the summary from the session
    summary = request.session.get('summary', '')

    return render(request, 'summary.html', {'summary': summary})
