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
    if model == 'user_information':
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


def admin_report(request, level):
    pass


def main_page(request, level):
    pass
