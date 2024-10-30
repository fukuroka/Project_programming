from django.shortcuts import render
from django.db import connections

def order_summary(request):
    user_id = request.GET.get('user_id')
    project_name = request.GET.get('project_name')
    order_id = request.GET.get('order_id')

    with connections['default'].cursor() as cursor:

        # Получение данных пользователя
        cursor.execute("SELECT * FROM client WHERE id_client = %s", [user_id])
        user_data = cursor.fetchone()

        # Получение данных проекта
        cursor.execute("""
            SELECT * FROM room_project WHERE title = %s AND id_client = %s
        """, [project_name, user_id])
        project_data = cursor.fetchone()

        # Получение данных заказа
        cursor.execute("""
            SELECT * FROM `order` WHERE id_order = %s
        """, [order_id])
        order_data = cursor.fetchone()


        cursor.execute("""
                    SELECT m.*, oi.quantity
                    FROM order_item oi
                    JOIN material m ON oi.id_material = m.id_material
                    WHERE oi.id_order = %s
                """, [order_id])
        materials_data = cursor.fetchall()

    context = {
        'user_data': user_data,
        'project_data': project_data,
        'order_data': order_data,
        'materials_data':materials_data,

    }
    return render(request, 'site_ros_stroy_torg/order_form.html', context)

def order_success(request):
    return render(request,'site_ros_stroy_torg/order_success.html')