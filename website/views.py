from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Data, User
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        protein_intake   =  int(request.form.get('protein_intake'))
        calorie_intake   =  int(request.form.get('calorie_intake'))
        high_carb_days   =  int(request.form.get('high_carb_days'))
        low_carb_days    =  int(request.form.get('low_carb_days'))
        normal_carb_days =  int(request.form.get('normal_carb_days'))

        if high_carb_days < 1 or low_carb_days < 1:
            flash('You need at least a day of high or low carb in order to make a carb cycling.', 'Error')
            return redirect(url_for('views.home'))
        if high_carb_days > 5 or low_carb_days > 5 or normal_carb_days > 6:
            flash('Make a shorter period of time please (maximum 5 days per category)', 'Error')
            return redirect(url_for('views.home'))
        if calorie_intake - protein_intake*4 < 400:
            flash('There are not enough calories to make a carb cycling, lower the amount of proteins or raise your caloric intake', 'Error')
            return redirect(url_for('views.home'))

        user_id = current_user.id  
        user_data = Data.query.filter_by(user_id=user_id).first()
        if user_data:
            user_data.low_carb_days = low_carb_days
            user_data.protein_intake = protein_intake
            user_data.calorie_intake = calorie_intake
            user_data.high_carb_days = high_carb_days
            user_data.normal_carb_days = normal_carb_days
        else:
            new_data = Data(
                user_id=user_id,
                protein_intake=protein_intake,
                calorie_intake=calorie_intake,
                high_carb_days=high_carb_days,
                normal_carb_days=normal_carb_days,
                low_carb_days=low_carb_days,
            )
            db.session.add(new_data)
        db.session.commit()

        flash('Data saved successfully!', 'Success')
        return redirect(url_for('views.profile'))  

    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    # protein_intake, calorie_intake, high_carb_days, normal_carb_days, low_carb_days 

    user_data = Data.query.filter_by(user_id=current_user.id).first() 
    if user_data:
        microcycle_length = user_data.high_carb_days + user_data.low_carb_days + user_data.normal_carb_days
        total_calories = microcycle_length * user_data.calorie_intake
        protein_cals = user_data.protein_intake * 4 * microcycle_length
        remaining_cals = total_calories - protein_cals

        average_fat = int((0.3 * (user_data.calorie_intake * 1.03)) / 9) 
        low_fat = int(average_fat * 1.25)
        high_fat = int(average_fat * 0.82) 

        total_fat_cals = (low_fat * 9 * user_data.low_carb_days) + (average_fat * 9 * user_data.normal_carb_days) + (high_fat * 9 * user_data.high_carb_days)
        remaining_after_fat = remaining_cals - total_fat_cals

        low_cho = max(0, int((0.85 * user_data.calorie_intake - user_data.protein_intake * 4 - low_fat * 9) / 4))
        average_cho = max(0, int((1.03 * user_data.calorie_intake - user_data.protein_intake * 4 - average_fat * 9) / 4))

        total_cho_low = low_cho * user_data.low_carb_days
        total_cho_avg = average_cho * user_data.normal_carb_days
        remaining_for_high_cho = remaining_after_fat - (total_cho_low * 4 + total_cho_avg * 4)

        high_cho = max(0, int(remaining_for_high_cho / (4 * user_data.high_carb_days)))

        # Calories for each day type to be displayed
        low_cal = low_cho * 4 + low_fat * 9 + user_data.protein_intake * 4
        average_cal = average_cho * 4 + average_fat * 9 + user_data.protein_intake * 4
        high_cal = high_cho * 4 + high_fat * 9 + user_data.protein_intake * 4

        return render_template("profile.html", user=current_user, data=user_data,
            low_cal=low_cal, average_cal=average_cal, high_cal=high_cal,
            low_fat=low_fat, average_fat=average_fat, high_fat=high_fat,
            low_cho=low_cho, average_cho=average_cho, high_cho=high_cho)


    return render_template("profile.html", user=current_user, data=user_data)