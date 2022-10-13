import string
import re
import random

from django.shortcuts import render
from django.views import View
from .forms import PassGenForm

class Index(View):
	def get(self, request):
		form = PassGenForm()

		context = {'form': form}
		return render(request, 'passgen/index.html', context)

	def post(self, request):
		form = PassGenForm(request.POST)

		if form.is_valid():
			available_characters = string.ascii_letters + string.digits

			if form.cleaned_data['include_symbols']:
				available_characters += string.punctuation

			if form.cleaned_data['remove_similar_characters']:
				ambiguous_characters = ['Z', '2', 'l', '1', '0', 'O', 'o']
				available_characters = re.sub('|'.join(ambiguous_characters), '', available_characters)

			password = ''.join(random.choice(available_characters) for i in range(form.cleaned_data['length']))
		return render(request, 'passgen/password.html', {'password': password})