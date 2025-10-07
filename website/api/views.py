from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from website.models import Product
from website.api.serialization.product_serializer import ProductSerializer

# -------------------------------
# List all products (Public)
# -------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])  # Public access
def product_list(request):
    print("Product list API called")
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# -------------------------------
# Create a new product
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Update a product
# -------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Require authentication
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Delete a product
# -------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Require authentication
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
