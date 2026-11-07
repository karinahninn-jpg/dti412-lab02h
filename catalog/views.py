 
from django.shortcuts import render
from django.http import Http404
 
 
COURSES_DATA = [
    {
        'id': 101,
        'code': 'DTI412',
        'title': 'DTI412 Special Topic in Application Development',
        'credits': 3,
        'instructor': 'Dr. Sirisuda Buathongkeow',
        'description': 'Learn Django, Django REST Framework, REST APIs, JWT authentication, and cloud technologies.'
    },
    {
        'id': 102,
        'code': 'DTI201',
        'title': 'DTI201 Database Systems & Data Modeling',
        'credits': 3,
        'instructor': 'Department Faculty',
        'description': 'Learn relational databases, ER diagrams, SQL, normalization, and transactions.'
    },
    {
        'id': 103,
        'code': 'DTI305',
        'title': 'DTI305 Frontend Web Technologies & React',
        'credits': 3,
        'instructor': 'Department Faculty',
        'description': 'Learn JavaScript ES6+, React, state management, and API integration.'
    },
]
 
 
def home_view(request):
    context = {
        'total_courses': len(COURSES_DATA),
        'featured_course': COURSES_DATA[0],
    }
    return render(request, 'catalog/home.html', context)
 
 
def course_list_view(request):
    query = request.GET.get('q', '').strip()
 
    if query:
        courses = [
            course for course in COURSES_DATA
            if query.lower() in course['title'].lower()
            or query.lower() in course['code'].lower()
        ]
    else:
        courses = COURSES_DATA
 
    context = {
        'courses': courses,
        'query': query,
    }
 
    return render(request, 'catalog/course_list.html', context)
 
 
 
 
def course_detail_view(request, course_id):
    course = next(
        (item for item in COURSES_DATA if item['id'] == course_id),
        None
    )
 
    if course is None:
        raise Http404("Course not found")
 
    return render(request, 'catalog/course_detail.html', {'course': course})
 
 
def inquiry_view(request):
    errors = []
    submitted_data = {}
 
    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        email = request.POST.get('email', '').strip()
        course_code = request.POST.get('course_code', '').strip()
        message = request.POST.get('message', '').strip()
 
        submitted_data = {
            'student_name': student_name,
            'email': email,
            'course_code': course_code,
            'message': message,
        }
 
        if not student_name:
            errors.append('Name is required.')
 
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
 
        if not message:
            errors.append('Message is required.')
 
        if not errors:
            return render(request, 'catalog/inquiry.html', {
                'success': True,
                'submitted_data': submitted_data,
            })
 
    return render(request, 'catalog/inquiry.html', {
        'errors': errors,
        'submitted_data': submitted_data,
    })
 