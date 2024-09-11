from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import (
    FoodCategory, 
    Menu, 
    Outlet, 
    FoodItem, 
    ItemVariant, 
    Addon, 
    Cart, 
    CartItem,
    OrderItem,
    Table,
    Order,
    TableArea)
from shop.api.serializers import (
    FoodCategorySerializer, 
    OutletSerializer, 
    ClientFoodCategorySerializer,
    CartItemSerializer,
    FoodItemSerializer,
    OrderSerializer,
    CheckoutSerializer,
    TableSerializer,
    AreaSerializer
    )
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class MenuAPIView(APIView):
    """
    API endpoint that returns a list of categories with nested subcategories and menu items.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        menu = Menu.objects.filter(outlet=outlet).first()
        categories = FoodCategory.objects.filter(menu=menu)

        serializer = FoodCategorySerializer(categories, many=True)
        return Response(serializer.data)

class ClientMenuAPIView(APIView):
    """
    API endpoint that returns a list of categories with nested subcategories and menu items for a client.
    """
    permission_classes = []
    def get(self, request, menu_slug, format=None):
        menu = Menu.objects.filter(menu_slug=menu_slug).first()
        categories = FoodCategory.objects.filter(menu=menu)
       
        # Serialize the existing categories
        serializer = ClientFoodCategorySerializer(categories, many=True)
        category_data = serializer.data

        # Add the recommended category
        recommended_category = self.get_recommended_category(menu)
        if recommended_category:
            category_data.insert(0, recommended_category)

        return Response(category_data)
    
    def get_recommended_category(self, menu):
        """Create a 'Recommended' category with all featured food items."""
        featured_items = FoodItem.objects.filter(menu=menu, featured=True)
        if featured_items.exists():
            food_items_data = FoodItemSerializer(featured_items, many=True).data
            recommended_category = {
                "id": -1,  # You can choose to leave it `None` or set a specific ID
                "name": "Recommended",
                "sub_categories": [],  # No subcategories in recommended
                "food_items": food_items_data
            }
            return recommended_category
        return None

class GetOutletAPIView(APIView):
    """
    API endpoint that returns a list of outlets.
    """
    permission_classes = []
    def get(self, request, menu_slug, format=None):
        menu = Menu.objects.filter(menu_slug=menu_slug).first()
        if menu:
            outlet = menu.outlet
            serializer = OutletSerializer(outlet)
            return Response(serializer.data)
        return Response({"detail": "Menu not found."}, status=status.HTTP_404_NOT_FOUND)
    

class OutletAPIView(APIView):
    """
    API endpoint that returns a list of outlets.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        outlets = Outlet.objects.filter(outlet_manager=user).first()
        serializer = OutletSerializer(outlets)
        return Response(serializer.data)

    def put(self, request, outlet_id, format=None):
        user = request.user
        outlet = Outlet.objects.filter(id=outlet_id, outlet_manager=user).first()
        data = request.data
        outlet.name = data.get('name', outlet.name)
        outlet.description = data.get('description', outlet.description)
        outlet.address = data.get('address', outlet.address)
        outlet.location = data.get('location', outlet.location)

        if 'logo' in request.FILES:
            outlet.logo = request.FILES['logo']

        minimum_order_value = data.get('minimum_order_value', outlet.minimum_order_value)
        average_preparation_time = data.get('average_preparation_time', outlet.average_preparation_time)
        service = data.get('service', outlet.service)

        outlet.phone = data.get('phone', outlet.phone)
        outlet.save()
        serializer = OutletSerializer(outlet)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class GetTableAPIView(APIView):
    """
    API endpoint that returns a list of tables in an outlet.
    """
    permission_classes = []
    def get(self, request, menu_slug, format=None):
        menu = Menu.objects.filter(menu_slug=menu_slug).first()
        outlet = menu.outlet
        tables = Table.objects.filter(outlet=outlet)
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

class GetTableDetail(APIView):
    """
    API endpoint that returns a list of tables in an outlet.
    """
    permission_classes = []
    def get(self, request, table_slug, format=None):
        table = Table.objects.filter(id=table_slug).first()
        serializer = TableSerializer(table)
        return Response(serializer.data)

class AreaAPIView(APIView):
    """
    API endpoint that returns a list of tables in an outlet.
    """
    permission_classes = []
    def get(self, request, format=None):
        areas = TableArea.objects.all()
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        data = request.data
        area = TableArea.objects.create(outlet=outlet, **data)
        serializer = AreaSerializer(area)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetTableSellerAPIView(APIView):
    """
    API endpoint that returns a list of tables in an outlet.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        tables = Table.objects.filter(outlet=outlet)
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        data = request.data
        name = data.get('name')
        capacity = data.get('capacity')
        area = data.get('area')
        area = TableArea.objects.filter(id=area).first()
        table = Table.objects.create(outlet=outlet, name=name, capacity=capacity, area=area)
        serializer = TableSerializer(table)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TableSellerAPIView(APIView):
    """
    API endpoint that returns a list of tables in an outlet.
    """
    permission_classes = [IsAuthenticated]   
    def put(self, request, table_slug, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        table = Table.objects.filter(id=table_slug, outlet=outlet).first()
        data = request.data
        table.name = data.get('name', table.name)
        table.capacity = data.get('capacity', table.capacity)
        table.area = TableArea.objects.filter(id=data.get('area', table.area.id)).first()
        table.save()
        serializer = TableSerializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, table_slug, format=None):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        table = Table.objects.filter(id=table_slug, outlet=outlet).first()
        table.delete()
        return Response({"message": "Table deleted successfully."}, status=status.HTTP_200_OK)


class CartView(APIView):
    def get(self, request, menu_slug):
        user = request.user
        menu = get_object_or_404(Menu, menu_slug=menu_slug)
        outlet = menu.outlet
        cart, created = Cart.objects.get_or_create(user=user, outlet=outlet)
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    def post(self, request, menu_slug):
        user = request.user
        menu = get_object_or_404(Menu, menu_slug=menu_slug)
        outlet = menu.outlet
        cart, created = Cart.objects.get_or_create(user=user, outlet=outlet)
        data = request.data

        food_item = get_object_or_404(FoodItem, id=data['food_item_id'])
        item_variant = get_object_or_404(ItemVariant, id=data['variant_id']) if data.get('variant_id') else None
        variants = item_variant.variant if item_variant else None
        addons = Addon.objects.filter(id__in=data.get('addons', []))
        quantity = data.get('quantity', 1)
        id = data.get('id')

        cart_item, item_created = CartItem.objects.get_or_create(
            id=id, cart=cart, food_item=food_item, variant=variants, defaults={'quantity': quantity}
        )
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_item.addons.set(addons)

        # Return all the cart items
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, menu_slug, item_id):
        user = request.user
        menu = get_object_or_404(Menu, menu_slug=menu_slug)
        outlet = menu.outlet
        cart = get_object_or_404(Cart, user=user, outlet=outlet)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

        # Return all the cart items
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, menu_slug, item_id):
        user = request.user
        menu = get_object_or_404(Menu, menu_slug=menu_slug)
        outlet = menu.outlet
        cart = get_object_or_404(Cart, user=user, outlet=outlet)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = request.data.get('quantity', 1)

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return Response({"message": "Cart updated successfully."}, status=status.HTTP_200_OK)

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, menu_slug):
        user = request.user
        
        # Get the cart
        menu = get_object_or_404(Menu, menu_slug=menu_slug)
        outlet = menu.outlet
        cart = get_object_or_404(Cart, user=user, outlet=outlet)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        
        order_type = request.data.get('order_type', 'dine_in')
        table_id = request.data.get('table_id', None)
        if order_type == 'dine-in' and not table_id:
            return Response({"detail": "Table number is required for dine-in orders."}, status=status.HTTP_400_BAD_REQUEST)
        
        table=None
        if table_id:
            table = get_object_or_404(Table, id=table_id)

        cooking_instructions = request.data.get('cooking_instructions', None)

        # Prepare order data
        total_price = sum(item.get_total_price() for item in cart_items)
        order_data = {
            "user": user,
            "outlet": cart.outlet,
            "total": total_price,
            "status": "pending",
            "order_type": order_type,
            "table": table,
            "cooking_instructions": cooking_instructions
        }


        # Create the order
        order_serializer = CheckoutSerializer(data=order_data)
        order_serializer.is_valid(raise_exception=True)
        order = Order.objects.create(**order_data)
        
        # Create OrderItems from CartItems
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                food_item=cart_item.food_item,
                variant=cart_item.variant,
                quantity=cart_item.quantity
            )
            order_item.save()
            order_item.addons.set(cart_item.addons.all())
        
        # Optionally clear the cart
        cart.delete()  

        # Notify the kitchen staff
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'seller_{menu_slug}',
            {
                'type': 'seller_notification',
                'message': OrderSerializer(order).data
            }
        )

        # async_to_sync(channel_layer.group_send)(
        #     f'order_{order.id}',
        #     {
        #         'type': 'order_update',
        #         'message': f'Your order {order.id} is now being processed.'
        #     }
        # )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, menu_slug=None, order_id=None):
        user = request.user
        print(user)
        if order_id:
            order = get_object_or_404(Order, order_id=order_id)
            if user.role == 'owner' and order.outlet.outlet_manager != user:
                return Response({"detail": "You are not authorized to view this order."}, status=status.HTTP_403_FORBIDDEN)
            elif user.role == 'customer' and order.user != user:
                return Response({"detail": "You are not authorized to view this order."}, status=status.HTTP_403_FORBIDDEN)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        elif user.role == 'owner':
            print("Owner")
            outlet = Outlet.objects.filter(outlet_manager=user).first()
            orders = Order.objects.filter(outlet=outlet).order_by('-created_at')
        elif menu_slug:
            menu = get_object_or_404(Menu, menu_slug=menu_slug)
            orders = Order.objects.filter(outlet=menu.outlet, user=user).order_by('-created_at')
        else:
            orders = Order.objects.filter(user=user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class SocketSeller(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        outlet = Outlet.objects.filter(outlet_manager=user).first()
        menu = Menu.objects.filter(outlet=outlet).first()
        url = f'/ws/sellers/{menu.menu_slug}'
        return Response({"url": url}, status=status.HTTP_200_OK)
