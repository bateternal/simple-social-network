from django.shortcuts import render
from chat.forms import Search
from django.http import HttpResponseRedirect
from django.http import Http404
import psycopg2
import os


db_name = os.environ.get('SQL_DATABASE', '')
db_user = os.environ.get('SQL_USER', '')
db_password = os.environ.get('SQL_PASSWORD', '')
db_host = os.environ.get('SQL_HOST', '')
db_port = os.environ.get('SQL_PORT', '')


def adminproject(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return render(
        request, "landing.html",
        {
            "search": Search(),
            "user": request.user.username
        }
        )


def raw_data(request, model, level='5'):
    level = int(level)
    if model not in ['conversation', 'user_information', 'post']:
        raise Http404("not found")
    conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
    cur = conn.cursor()
    if model == 'user_information':
        query = ('select id, username, firstname, lastname, is_ban'
                 ' from user_information')
        cur.execute(query)
        heads = ['username', 'firstname', 'lastname', 'is_ban',
                 'action1', 'action2']
        data = []
        temp = cur.fetchone()
        while temp:
            payload = {"index": str(list(temp)[0]), "elements": list(temp)[1:]}
            payload['has_action_permit'] = level <= 4
            if list(temp)[4]:
                payload['action_button'] = 'unban'
                action = 'unban'
            else:
                action = 'ban'
                payload['action_button'] = 'ban'
            payload['action_link'] = '/panel/support/%s/%s/%s/%s/' % (
                action, model, str(list(temp)[0]), str(level))
            payload['has_delete_permit'] = level <= 2
            payload['delete_link'] = '/panel/support/delete/%s/%s/%s/' % (
                model, str(list(temp)[0]), str(level))
            data.append(payload)
            temp = cur.fetchone()
    elif model == 'conversation':
        query = ('select id, user_id, target_id, block'
                 ' from conversation')
        cur.execute(query)
        heads = ['user_id', 'target_id', 'block', 'action1', 'action2']
        data = []
        temp = cur.fetchone()
        while temp:
            payload = {"index": str(list(temp)[0]), "elements": list(temp)[1:]}
            payload['has_action_permit'] = level <= 3
            if list(temp)[3]:
                payload['action_button'] = 'unblock'
                action = 'unblock'
            else:
                action = 'block'
                payload['action_button'] = 'block'
            payload['action_link'] = '/panel/support/%s/%s/%s/%s/' % (
                action, model, str(list(temp)[0]), str(level))
            payload['has_delete_permit'] = level <= 1
            payload['delete_link'] = '/panel/support/delete/%s/%s/%s/' % (
                model, str(list(temp)[0]), str(level))
            data.append(payload)
            temp = cur.fetchone()
    elif model == 'post':
        query = ('select c.id, c.title, c.content, u.username'
                 ' from post as c join user_information as u'
                 ' on c.owner_id=u.owner_id')
        cur.execute(query)
        heads = ['title', 'content', 'owner', 'action1', 'action2']
        data = []
        temp = cur.fetchone()
        while temp:
            payload = {"index": str(list(temp)[0]), "elements": list(temp)[1:]}
            payload['has_action_permit'] = False
            payload['action_link'] = ''
            payload['action_button'] = ''
            payload['has_delete_permit'] = level == 0
            payload['delete_link'] = '/panel/support/delete/%s/%s' % (
                model, str(list(temp)[0]))
            data.append(payload)
            temp = cur.fetchone()
    return render(
        request, "admin_table.html",
        {
            "heads": heads,
            "data": data
        }
        )


def action(request, action, model, pk, level):
    pk = int(pk)
    if model not in ['conversation', 'user_information', 'post']:
        raise Http404("not found")
    conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
    cur = conn.cursor()
    if action == 'delete':
        query = 'delete from %s where id=%i' % (model, pk)
    elif model == 'user_information':
        if action == 'ban':
            query = 'update user_information set is_ban=true where id=%i' % pk
        elif action == 'unban':
            query = 'update user_information set is_ban=false where id=%i' % pk
    elif model == 'conversation':
        if action == 'block':
            query = 'update conversation set block=true where id=%i' % pk
        elif action == 'unblock':
            query = 'update conversation set block=false where id=%i' % pk
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return HttpResponseRedirect('/panel/support/%s/%s/' % (model, level))


def delete_data(request, model, pk, level):
    pk = int(pk)
    if model not in ['conversation', 'user_information', 'post']:
        raise Http404("not found")
    conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
    cur = conn.cursor()
    query = 'delete from %s where id=%i' % (model, pk)
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return HttpResponseRedirect('/panel/support/%s/%s/' % (model, level))


def admin_report(request, report_number, level):
    level = int(level)
    conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
    cur = conn.cursor()
    if report_number == 1:
        query = ('select '
                 '     case grouping(user_type)'
                 '     when 0 then user_type'
                 '     when 1 then \'all\''
                 '     end as user_type,'
                 '     max(score)'
                 '   from user_information' 
                 '     group by rollup (user_type)'
                 '       order by user_type;')
        heads = ['user_type', 'max']
    if report_number == 2:
        query = (
            'select sender_id from message '
            'group by sender_id having count(id) > 10;'
            )
        heads = ['sender_id']
    if report_number == 3:
        query = (
            '''
select * from crosstab(
    'select t.sender_id, t.hhour, count(t.id)  from 
  (select sender_id, split_part(date_time, '':'', 1) as hhour, id
  from message) as t 
    join message as m 
      on t.id=m.id 
    group by t.hhour, t.sender_id
    having count(t.id) > 0 order by sender_id',
    'select hhour from generate_series(1,24) hhour'
) as (
    sender_id int,
    "1 AM" int,
    "2 AM" int,
    "3 AM" int,
    "4 AM" int,
    "5 AM" int,
    "6 AM" int,
    "7 AM" int,
    "8 AM" int,
    "9 AM" int,
    "10 AM" int,
    "11 AM" int,
    "12 AM" int,
    "1 PM" int,
    "2 PM" int,
    "3 PM" int,
    "4 PM" int,
    "5 PM" int,
    "6 PM" int,
    "7 PM" int,
    "8 PM" int,
    "9 PM" int,
    "10 PM" int,
    "11 PM" int,
    "12 PM" int
);
            '''
            )
        heads = ['sender_id', '1 AM', '2 AM', '3 AM', '4 AM',
                 '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM',
                 '11 AM', '12 AM', '1 PM', '2 PM', '3 PM', '4 PM',
                 '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM',
                 '11 PM', '12 PM']
    if report_number == 4:
        query = (
            'select username, AVG (score) OVER (PARTITION by user_type) '
            'from user_information;'
            )
        heads = ['username', 'average']
    if report_number == 5:
        query = (
            'select username, RANK() OVER '
            '(PARTITION by user_type order by score) '
            'from user_information;'
            )
        heads = ['username', 'rank']
    if report_number == 6:
        query = (
                'select u.username, count(*) as count_sent_message '
                'from message as m join user_information as u on '
                'm.sender_id=u.owner_id group by u.username;'
            )
        heads = ['username', 'count_sent_message']
    cur.execute(query)
    data = []
    temp = cur.fetchone()
    while temp:
        payload = {"index": str(list(temp)[0]), "elements": list(temp)[1:]}
        data.append(payload)
        temp = cur.fetchone()
    return render(
        request, "admin_report.html",
        {
            "heads": heads,
            "data": data
        }
        )


def main_page(request, level):
    pass
