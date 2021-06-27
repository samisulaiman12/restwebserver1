from flask import Flask, render_template, request
from random import seed, randrange, choice
import datetime

app = Flask(__name__)


def check_passed(actual_marks):
    thresholds = {'math': 300, 'physics': 200, 'chemistry': 100,
                  'biology': 200, 'arabic': 200, 'english': 100, 'french': 100, 'total': 1500}
    pass_fail = {k: 'ناجح' if k in thresholds and actual_marks[k] >= thresholds[k] else 'راسب'
                 for k in actual_marks}
    return pass_fail


def gen_dummy_info(random_set_indicator):
    seed(random_set_indicator)
    start_date = datetime.date(2001, 1, 1)
    end_date = datetime.date(2005, 2, 1)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    female_names = ['جمانة', 'ريما', 'رنا', 'حلا', 'فيروز', 'سعاد', 'وداد', 'عفاف', 'مايا', 'ندى', 'سارة']
    male_names = ['علي', 'أحمد', 'يونس', 'حسام', 'جعفر', 'عبد الكريم', 'ابراهيم', 'سامي', 'سمير', 'مهند']
    city_names = ['اللاذقية', 'طرطوس', 'دمشق', 'حلب', 'حماه', 'حمص',
                  'ادلب', 'دير الزور', 'الرقة', 'القامشلي', 'ريف دمشق', 'السويداء', 'درعا']
    info = [
        choice(female_names + male_names),
        choice(male_names),
        choice(female_names),
        choice(male_names),
        choice(city_names),
        start_date + datetime.timedelta(days=randrange(days_between_dates))]
    return info


@app.route('/', methods=["GET", "POST"])
def index():
    if request.form:
        student_number = request.form['student_id']
        if not student_number or student_number is None:
            return render_template('./index.html', message='!! رقم الاكتتاب هذا غير صحيح')
        student_info = gen_dummy_info(student_number)
        seed(student_number)
        actual_marks = {'math': randrange(100, 600),
                        'physics': randrange(100, 600),
                        'chemistry': randrange(100, 400),
                        'biology': randrange(100, 400),
                        'arabic': randrange(50, 200),
                        'english': randrange(50, 200),
                        'french': randrange(50, 200)}
        actual_marks['total'] = sum(actual_marks.values())
        return render_template('./portal.html',
                               std_id=student_number,
                               student_firstname=student_info[0],
                               student_lastname=student_info[1],
                               mother=student_info[2],
                               father=student_info[3],
                               city=student_info[4],
                               date_of_birth=student_info[5],
                               actual_marks=actual_marks,
                               pass_fail=check_passed(actual_marks)
                               )
    return render_template('./index.html', message='أدخل رقم الاكتتاب من فضلك')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
