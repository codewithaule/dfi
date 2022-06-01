from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
 

from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm

from django.db.models import Q


from .models import Category, Product

 

def about(request):
    return render(request, 'shop/product/about.html')

def contact(request):
    return render(request, 'shop/product/contact.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)

 
    

def search(request):
    query = request.GET.get('query', '') # second is default parameter which is empty
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))


    return render(request, 'shop/product/search.html', {'products':products, 'query': query})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, "Registration successful." )
            
            return render(request, 'shop/product/list.html')

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render (request=request, template_name="shop/product/register.html", context={"register_form":form})
 
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request,  'shop/product/list.html')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="shop/product/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return render(request,'shop/product/list.html')

