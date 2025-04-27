from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
import openai
import os
import json
import re

# Configure OpenAI API key using the environment variable
openai.api_key = os.getenv('OPENAI_KEY')

# Function to generate tags using OpenAI
def generate_tags(product_name, product_description, product_category):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates relevant product tags."},
                {"role": "user", "content": f"Generate 5 relevant tags for this product as a JSON array. Don't include explanations, just return the array of tags.\n\nProduct Name: {product_name}\nDescription: {product_description}\nCategory: {product_category}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Extract the generated tags from the response
        tags_text = response.choices[0].message.content.strip()
        
        # Handle the possibility that the AI might return the tags in various formats
        # Try to parse directly as JSON
        try:
            # Remove any markdown code formatting
            if "```json" in tags_text:
                tags_text = re.search(r'```json\s*(.*?)\s*```', tags_text, re.DOTALL).group(1)
            elif "```" in tags_text:
                tags_text = re.search(r'```\s*(.*?)\s*```', tags_text, re.DOTALL).group(1)
                
            tags = json.loads(tags_text)
            
            # Ensure we have a list
            if isinstance(tags, list):
                return tags
            if isinstance(tags, dict) and 'tags' in tags:
                return tags['tags']
            
            # If we got here, the format is unexpected but we'll try to extract tags anyway
            return list(tags.values()) if isinstance(tags, dict) else ['general']
            
        except Exception as e:
            # If parsing fails, attempt to extract tags from text
            pattern = r'\["([^"]+)"(?:,\s*"([^"]+)")*\]'
            match = re.search(pattern, tags_text)
            if match:
                # Extract all groups and filter out None values
                tags = [g for g in match.groups() if g is not None]
                return tags
            
            # If all else fails, just return a default tag
            return ["general"]
            
    except Exception as e:
        print(f"Error generating tags: {e}")
        return ["general"]  # Default tag if the API call fails

# This view displays all the products
def product_list(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'store/product_list.html', {'products': products})  # Pass products to the template

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Create but don't save the product instance yet
            product = form.save(commit=False)
            
            # Generate tags using OpenAI
            tags = generate_tags(
                product_name=product.name,
                product_description=product.description,
                product_category=product.category
            )
            
            # Assign tags to the product
            product.tags = tags
            
            # Now save the product with tags
            product.save()
            
            return redirect('product_list')  # Redirect to the product list page
    else:
        form = ProductForm()

    # Debugging the context being passed to the template
    print(f"Form: {form}")
    print(f"Is form valid: {form.is_valid() if request.method == 'POST' else 'N/A'}")
    
    return render(request, 'store/add_product.html', {'form': form})