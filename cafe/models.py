from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
# from core.models import TimestampMixin
# Create your models here.

class Table(models.Model):
    table_number = models.CharField(max_length=3)
    cafe_space_position = models.CharField(max_length=100)

    def total_price(self):
        res = sum(map(lambda order: order.calculate_order_price(), self.orders.all()))
        return res

    def add_order(self, menu_item, num):
        res = Orders.objects.create(table_id=self.id, menu_item_id=menu_item, menu_item_number=num)
        return res

    def __str__(self):
        return f"{self.table_number}"


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"category: {self.name}"


class MenuItems(models.Model):
    name = models.CharField(max_length=30, verbose_name='menu item name', help_text='enter menu item name', null=False,
                            blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='menu item category',
                                 help_text='define category', null=False, blank=False)
    discount = models.IntegerField(verbose_name='item discount', help_text='enter item discount', null=True, blank=True,
                                   default=0)

    price = models.FloatField(verbose_name='item price', help_text='enter item price', null=False, blank=False)
    image = models.FileField(verbose_name='item image', help_text='upload image of item', null=True, blank=True,
                             upload_to='cafe5/menu_items/images/')
    create_timestamp = models.DateTimeField(verbose_name='date of adding item', help_text='date of creation of item',
                                            auto_now_add=True, null=False, blank=False)
    modify_timestamp = models.DateTimeField(verbose_name='date of update item', help_text='date of modify of item',
                                            auto_now=True, null=False, blank=False)

    @classmethod
    def filter_by_category(cls, category_id):
        res = cls.objects.filter(category=category_id)
        return res

    @classmethod
    def max_price(cls):
        res = cls.objects.aggregate(models.Max('price'))
        return res

    @classmethod
    def avg_price(cls):
        res = cls.objects.aggregate(models.Avg('price'))
        return res

    def final_price(self):
        if self.price < 0:
            raise AssertionError
        if self.discount < 0:
            raise AssertionError
        if self.discount > 100:
            raise AssertionError

        return self.price - ((self.discount / 100) * self.price)

    def __str__(self):
        return f"{self.id}# {self.name} : {self.price}"


class Orders(models.Model):

    status = models.CharField(max_length=50, default='new')
    time_stamp = models.DateTimeField(auto_now_add=True)
    table_id = models.ForeignKey(Table, related_name='orders', on_delete=models.RESTRICT, default=1)
    menu_item_id = models.ForeignKey(MenuItems, on_delete=models.RESTRICT)
    menu_item_number = models.IntegerField(default=1)

    def calculate_order_price(self):
        res = self.menu_item_number * (self.menu_item_id.price * (100 - self.menu_item_id.discount))
        return res

    @classmethod
    def filter_by_menuitem_id(cls, menu_item_id):
        res = cls.objects.filter(menu_item_id__id=menu_item_id)
        return res

    @classmethod
    def filter_by_menuitem_category(cls, category_id):
        res = cls.objects.filter(menu_item_id__category=category_id)
        return res

    @classmethod
    def today_orders(cls):
        today_orders_list = cls.objects.filter(time_stamp__day=timezone.now().day)
        return today_orders_list

    @classmethod
    def month_orders(cls):
        month_orders_list = cls.objects.filter(time_stamp__month=timezone.now().month)
        return month_orders_list

    @classmethod
    def sum_cost(cls, table_number):
        orders_res = cls.objects.filter(table_id=table_number)
        res = sum(map(lambda order: order.calculate_order_price(), orders_res))
        return res

    @classmethod
    def sum_today_cost(cls):
        orders_res = cls.objects.filter(time_stamp__day=timezone.now().day)
        res = sum(map(lambda order: order.calculate_order_price(), orders_res))
        return res

    def change_status(self, new_status):
        self.status = new_status
        return self


    def __str__(self):
        return f"{self.id}# order status: {self.status} - date&time: {self.time_stamp}"


class Receipts(models.Model):
    total_price = models.FloatField()
    final_price = models.FloatField()
    time_stamp = models.DateTimeField(datetime.now())
    orders_id = models.ManyToManyField(Orders)

    def __str__(self):
        return f"{self.final_price}"


# class Cashier(User, TimestampMixin):
#
#     phone_number = models.CharField(max_length=11, verbose_name='phone number', help_text='enter your phone',
#                                     null=False, blank=False)
#     national_code = models.CharField(max_length=10, verbose_name='national code', help_text='enter your national code',
#                                      null=False, blank=False)
#     address = models.TextField(max_length=50)
#
#
