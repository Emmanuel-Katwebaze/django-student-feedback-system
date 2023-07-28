# migrations.py
from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_students_data(apps, schema_editor):
    Student = apps.get_model('core', 'Student')

    sample_data = [
        {'student_id': 2300000001, 'first_name': 'John', 'last_name': 'Doe',
            'email': 'john@example.com', 'course': 'BSCS', 'enrollment_year': 2023},
        {'student_id': 2300000002, 'first_name': 'Jane', 'last_name': 'Smith',
            'email': 'jane@example.com', 'course': 'BSMECH', 'enrollment_year': 2023},
        {'student_id': 2300000003, 'first_name': 'Luke', 'last_name': 'Shaw',
            'email': 'luke@example.com', 'course': 'BSCCIVIC', 'enrollment_year': 2023},
        {'student_id': 2300000004, 'first_name': 'Edward', 'last_name': 'NewGate',
            'email': 'edward@example.com', 'course': 'BSCCIVIC', 'enrollment_year': 2023},
        {'student_id': 2300000005, 'first_name': 'Mary', 'last_name': 'Smith',
            'email': 'mary@example.com', 'course': 'BSSE', 'enrollment_year': 2023},
        {'student_id': 2300000006, 'first_name': 'Ashanti', 'last_name': 'Trinity',
            'email': 'ashanti@example.com', 'course': 'BIST', 'enrollment_year': 2023},
    ]

    for data in sample_data:
        Student.objects.create(**data)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_students_data),
    ]
