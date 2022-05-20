
from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required
from milkanalyzer.models import SelectedProduct
from milkanalyzer.payment.forms import PaymentForm

payment = Blueprint('payment', __name__)

@payment.route("/payment/new", methods=['GET', 'POST'])
@login_required
def new_payment():
    payment_form = PaymentForm()
    selected_products = SelectedProduct.query.all()
    if payment_form.validate_on_submit():
        flash('Payment accepted!', 'success')
        return redirect(url_for('orders.new_order'))
    return render_template('confirm_payment.html', title='Confirm payment', form=payment_form, legend='Confirm payment', selected_products=selected_products)