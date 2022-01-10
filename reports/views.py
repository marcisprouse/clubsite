# from excel_response import ExcelView, ExcelResponse
from certificates.models import Certificate

from accounts.models import MyProfile
from keys.models import Key
from schedule.models import Volunteer, Memberrsvp
from badges.models import Badge
from schedule.periods import Period

from django.utils import timezone



import xlwt

# from itertools import chain
from django.http import HttpResponse
from django.contrib.auth.models import User

# this is for staff only page views
from django.contrib.auth.decorators import user_passes_test

import datetime



''' Example using excel_response tool
class CertificateExcelView(ExcelView):
    model = Certificate '''


@user_passes_test(lambda user: user.is_staff)
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="members.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('members')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                'Member ID',
                'Username',
                'First name',
                'Last name',
                'Email address',
                'Cell Phone',
                'Other Phone',
                'Street Number',
                'Street',
                'Part Time Resident',
                'Away Address',
                'Active Member',
                'Is a Landlord',
                'Is a Renter',
                'Member Notes',
                'Certificate Number'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = MyProfile.objects.all().order_by('user__last_name').values_list(
                                                                            'member_id',
                                                                            'user__username',
                                                                            'user__first_name',
                                                                            'user__last_name',
                                                                            'user__email',
                                                                            'cell_phone',
                                                                            'other_phone',
                                                                            'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__street_number',
                                                                            'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__route',
                                                                            'is_a_member_part_time_resident',
                                                                            'member_part_time_away_address__formatted',
                                                                            'is_active_member',
                                                                            'is_a_landlord_with_transferred_membership',
                                                                            'is_a_renter_member',
                                                                            'member_notes',
                                                                            'member_coyote_lakes_qualifying_address__certificate_number'
                                                                           )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            if type(row[col_num]) is datetime.date:
                date_xf = xlwt.easyxf(num_format_str='MM/DD/YYYY')  # sets date format in Excel
                ws.write(row_num, col_num, row[col_num], date_xf)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response



@user_passes_test(lambda user: user.is_staff)
def export_certificates_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="certificate_by_member.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('certificates')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Certificate Number', 'Street Number', 'Street Address', 'Purchase Date', 'Is for Sale', 'Is for Sale As of Date', 'Is Club Held', 'Certificate Notes', 'Name Associated with Certificate', 'Is Landlord', 'Resident/Member Last Name', 'Resident/Member First Name', 'Is Renter', 'Resident/Member Email', 'Resident/Member Cell Phone', 'Resident/Member Other Phone', 'Member Notes']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = MyProfile.objects.all().order_by('member_coyote_lakes_qualifying_address__certificate_number').values_list(
                                                                                                                        'member_coyote_lakes_qualifying_address__certificate_number',
                                                                                                                        'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__street_number',
                                                                                                                        'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__route',
                                                                                                                        'member_coyote_lakes_qualifying_address__purchase_date',
                                                                                                                        'member_coyote_lakes_qualifying_address__is_for_sale',
                                                                                                                        'member_coyote_lakes_qualifying_address__is_for_sale_as_of_date',
                                                                                                                        'member_coyote_lakes_qualifying_address__is_club_held',
                                                                                                                        'member_coyote_lakes_qualifying_address__certificate_notes',
                                                                                                                        'member_coyote_lakes_qualifying_address__name_associated_with_certificate',
                                                                                                                        'is_a_landlord_with_transferred_membership',
                                                                                                                        'user__last_name',
                                                                                                                        'user__first_name',
                                                                                                                        'is_a_renter_member',
                                                                                                                        'user__email',
                                                                                                                        'cell_phone',
                                                                                                                        'other_phone',
                                                                                                                        'member_notes'
                                                                                                                        )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            if type(row[col_num]) is datetime.date:
                date_xf = xlwt.easyxf(num_format_str='MM/DD/YYYY')  # sets date format in Excel
                ws.write(row_num, col_num, row[col_num], date_xf)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response




@user_passes_test(lambda user: user.is_staff)
def export_keys_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="keys.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('keys')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                'First Key Assignment',
                'Second Key Assignement',
                'Certificate Number',
                'Street Number',
                'Street Address',
                'Cert Purchase Date',
                'Is for Sale',
                'Is for Sale as Of',
                'Is Club Held',
                'Name Associated with Certificate',
                'Certificate Notes',
                'Key Notes'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = Key.objects.all().order_by('key_number_one').values_list(
                                                                    'key_number_one',
                                                                    'key_number_two',
                                                                    'certificate_and_qualifying_address_for_keys__certificate_number',
                                                                    'certificate_and_qualifying_address_for_keys__member_coyote_lakes_address__street_number',
                                                                    'certificate_and_qualifying_address_for_keys__member_coyote_lakes_address__route',
                                                                    'certificate_and_qualifying_address_for_keys__purchase_date',
                                                                    'certificate_and_qualifying_address_for_keys__is_for_sale',
                                                                    'certificate_and_qualifying_address_for_keys__is_for_sale_as_of_date',
                                                                    'certificate_and_qualifying_address_for_keys__is_club_held',
                                                                    'certificate_and_qualifying_address_for_keys__name_associated_with_certificate',
                                                                    'certificate_and_qualifying_address_for_keys__certificate_notes',
                                                                    'key_notes'
                                                                    )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            if type(row[col_num]) is datetime.date:
                date_xf = xlwt.easyxf(num_format_str='MM/DD/YYYY')  # sets date format in Excel
                ws.write(row_num, col_num, row[col_num], date_xf)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response


@user_passes_test(lambda user: user.is_staff)
def export_certificate_full_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="certificate_by_number.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('keys')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                'Certificate Number',
                'Exclude from Site Search',
                'Name Associated with Certificate',
                'Street Number',
                'Street',
                'Purchase Date',
                'Is for Sale',
                'Is for Sale as of Date',
                'Is Club Held',
                'Certificate Notes'

                ]


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = Certificate.objects.all().order_by('certificate_number').values_list(
                                                                    'certificate_number',
                                                                    'exclude',
                                                                    'name_associated_with_certificate',
                                                                    'member_coyote_lakes_address__street_number',
                                                                    'member_coyote_lakes_address__route',
                                                                    'purchase_date',
                                                                    'is_for_sale',
                                                                    'is_for_sale_as_of_date',
                                                                    'is_club_held',
                                                                    'certificate_notes',
                                                                    )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            if type(row[col_num]) is datetime.date:
                date_xf = xlwt.easyxf(num_format_str='MM/DD/YYYY')  # sets date format in Excel
                ws.write(row_num, col_num, row[col_num], date_xf)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response





@user_passes_test(lambda user: user.is_staff)
def export_events_volunteers_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="event_volunteer.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('event_volunteer')

    # Sheet header, first row
    row_num = 0


    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Event Title', 'Date/Time', 'Volunteer Last Name', 'Volunteer First Name', 'Email', 'Cell Phone', 'Note']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)



    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()



    rows = Volunteer.objects.all().order_by('occurrence__start').values_list(
                                                                                'occurrence__title',
                                                                                'occurrence__start',
                                                                                'owner__last_name',
                                                                                'owner__first_name',
                                                                                'owner__email',
                                                                                'owner__my_profile__cell_phone',
                                                                                'text'
                                                                                )



    rows = [[x.strftime("%m-%d-%Y %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)



    wb.save(response)
    return response


@user_passes_test(lambda user: user.is_staff)
def export_events_rsvp_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="event_rsvp_dish.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('event_rsvp_dish')

    # Sheet header, first row
    row_num = 0


    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Event Title', 'Date/Time', 'Attendee Last Name', 'Attendee First Name', 'Email', 'Cell Phone', 'Is Attending', 'Guests', 'What Member is Bringing OR Optional Note', 'Silent Auction Donation if Applicable']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)



    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()



    rows = Memberrsvp.objects.all().order_by('occurrence__start').values_list(
                                                                                'occurrence__title',
                                                                                'occurrence__start',
                                                                                'owner__last_name',
                                                                                'owner__first_name',
                                                                                'owner__email',
                                                                                'owner__my_profile__cell_phone',
                                                                                'attending',
                                                                                'guests',
                                                                                'bringing',
                                                                                'mealchoice'
                                                                                )


    rows = [[x.strftime("%m-%d-%Y %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)



    wb.save(response)
    return response

'''
The view export_contacts_xls needs to be fixed.  Not using right now.
'''

@user_passes_test(lambda user: user.is_authenticated)
def export_contacts_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="contacts.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('contacts')

    # Sheet header, first row
    row_num = 0
    row_num_two = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Last name', 'First name', 'Email address']

    columns_two = ['Cell Phone', 'Other Phone', 'Street Number', 'Street',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    for col_num_two in range(len(columns_two)):
        ws.write(row_num_two, col_num_two+col_num+1, columns_two[col_num_two], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = User.objects.all().order_by('last_name').values_list('last_name', 'first_name', 'email')
    profilerows = MyProfile.objects.all().order_by('user__last_name').values_list('cell_phone',
                                                                                  'other_phone',
                                                                                  'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__street_number',
                                                                                  'member_coyote_lakes_qualifying_address__member_coyote_lakes_address__route',
                                                                                  )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            ws.write(row_num, col_num, row[col_num], font_style)


    for row in profilerows:
        row_num_two += 1
        for col in range(len(row)):
            ws.write(row_num_two, col+col_num+1, row[col], font_style)


    wb.save(response)
    return response




@user_passes_test(lambda user: user.is_staff)
def export_badges_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="badges_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('keys')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                'Member Last Name',
                'Member First Name',
                'Member ID',
                'Member Email',
                'Cell Phone',
                'Street Number',
                'Street',
                'Is Renter',
                'Badge Print Date',
                'Badge Color'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()


    rows = Badge.objects.all().order_by('members__user__username','print_date').values_list(
                                                                                            'members__user__last_name',
                                                                                            'members__user__first_name',
                                                                                            'members__member_id',
                                                                                            'members__user__email',
                                                                                            'members__cell_phone',
                                                                                            'members__member_coyote_lakes_qualifying_address__member_coyote_lakes_address__street_number',
                                                                                            'members__member_coyote_lakes_qualifying_address__member_coyote_lakes_address__route',
                                                                                            'members__is_a_renter_member',
                                                                                            'print_date',
                                                                                            'badge_color'
                                                                                            )


    for row in rows:
        row_num += 1
        for col_num in range(len(row)):

            if type(row[col_num]) is datetime.date:
                date_xf = xlwt.easyxf(num_format_str='MM/DD/YYYY')  # sets date format in Excel
                ws.write(row_num, col_num, row[col_num], date_xf)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response


@user_passes_test(lambda user: user.is_staff)
def export_logins_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="logins.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('logins')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Last Login Date', 'Last name', 'First name', 'Email address', 'Cell Phone', 'Temporary Password', 'Member ID', 'Is Active Member']


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = MyProfile.objects.all().order_by('-user__last_login', 'user__username').values_list(
                                                                                                'user__last_login',
                                                                                                'user__last_name',
                                                                                                'user__first_name',
                                                                                                'user__email',
                                                                                                'cell_phone',
                                                                                                'temporary_password',
                                                                                                'member_id',
                                                                                                'is_active_member'
                                                                                                )


    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response





@user_passes_test(lambda user: user.is_staff)
def export_blast_subscriptions_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="blast_subscriptions.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('blast_subscriptions')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
                'Last name',
                'First name',
                'Email address',
                'Cell Phone',
                'Newsletter Subscription',
                'Subscribed - If False, they Unsubscribed You can re-subscribe them.',
                'Member ID',
                'Is Active Member',
                'Site Permissions Active'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = MyProfile.objects.all().order_by('user__username').values_list(
                                                                            'user__last_name',
                                                                            'user__first_name',
                                                                            'user__email',
                                                                            'cell_phone',
                                                                            'user__subscription__newsletter__title',
                                                                            'user__subscription__subscribed',
                                                                            'member_id',
                                                                            'is_active_member',
                                                                            'user__is_active'
                                                                            )

    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response






