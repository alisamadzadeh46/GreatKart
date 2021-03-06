from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from randominfo import get_email

from accounts.email import random_char
from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests

from orders.models import Order, OrderProduct


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # username = email.split("@")[0]
            username = form.cleaned_data['phone_number']
            if email is None:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                                   email=random_char(7)+"@gmail.com",
                                                   username=username, password=password)
            else:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                   username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()
            # current_site = get_current_site(request)
            # mail_subject = 'فعالسازی حساب کاربری'
            # message = render_to_string('account/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            # return redirect('/account/login/?command=verification&email=' + email)
            messages.success(request, 'حساب کاربری شما با موفقیت فعال گردید')
            return redirect('account:login')


    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context)


def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = auth.authenticate(username=phone, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'شما با موفقیت وارد حساب شدید.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('account:dashboard')
        else:
            messages.error(request, 'خطا در ورود به حساب کاربری')
            return redirect('account:login')
    return render(request, 'account/login.html')


@login_required(login_url='account:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'شما با موفقیت از حساب کاربری خارج شدید.')
    return redirect('account:login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'حساب کاربری شما با موفقیت فعال گردید')
        return redirect('account:login')
    else:
        messages.error(request, 'لینک فعالسازی معتبر نیست')
        return redirect('account:register')


@login_required(login_url='account:login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get_or_create(user_id=request.user.id)
    image = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
        'image': image,
    }
    return render(request, 'account/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'بازیابی رمز عبور'
            message = render_to_string('account/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'لینک بازیابی به ایمیل شما ارسال گردید')
            return redirect('account:login')
        else:
            messages.error(request, 'ایمیل وارد شده اشتباه است.')
            return redirect('account:forgotPassword')
    return render(request, 'account/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    global uid
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'لطفا رمز عبور خود را تغییر دهید.')
        return redirect('account:resetPassword')
    else:
        messages.error(request, 'لینک فعالسازی شما فاید اعتبار می باشد')
        return redirect('account:login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر پیدا کرد')
            return redirect('account:login')
        else:
            messages.error(request, 'رمز عبور با تکرار ان مطابقت ندارد')
            return redirect('account:resetPassword')
    else:
        return render(request, 'account/reset_password.html')


@login_required(login_url='account:login')
def my_orders(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    context = {
        'orders': orders,
    }
    return render(request, 'account/my_orders.html', context)


@login_required(login_url='account:login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'اطلاعات شما با موفقیت بروزرسانی شد')
            return redirect('account:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'account/edit_profile.html', context)


@login_required(login_url='account:login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت بروزرسانی شد')
                return redirect('account:change_password')
            else:
                messages.error(request, 'رمز عبور شما فاقد اعتبار است.')
                return redirect('account:change_password')
        else:
            messages.error(request, 'رمزعبور با تکرار ان مطابقت ندارد')
            return redirect('account:change_password')
    return render(request, 'account/change_password.html')


@login_required(login_url='account:login')
def order_detail(request, order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
    context = {
        'order_details': order_details,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'account/order_detail.html', context)
