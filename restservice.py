# using flask_restful 
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import nltk 
import requests

# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 

# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Hello(Resource): 

	# corresponds to the GET request. 
	# this function is called whenever there 
	# is a GET request for this resource 
	def get(self): 

		return jsonify({'message': 'hello world'}) 

	# Corresponds to POST request 
	def post(self): 
		
		data = request.get_json()	 # status code 
		return jsonify({'data': data}), 201


class AccountService(Resource):

	def get(self):
		service_type = str(request.args.get('servicetype'))
		sender_name =  str(request.args.get('sender'))
		receiver_name = str(request.args.get('receiver'))
		service_name = str(request.args.get('service'))
		amount_str = str(request.args.get('amount'))
		user_name = str(request.args.get('user'))
		amount=0.0
		found_match=False
		user_names = ['joseph', 'john', 'carole', 'peter', 'ram']
		subscription_services = ['credit report', 'mutual funds', 'financial consulting', 'retirement services']
        
		if(amount_str != "None"):
			amount=float(amount_str)
        # process the services type
		if(service_type.upper() == "TRANSFER"):
			if(amount == 0.0):
				result='Please enter a valid amount to transfer'
			elif(receiver_name.upper() == "JOSEPH"):
				result='Joseph is not registred as a reciever in your account, I have created a registration form for you , pleae authorize the registration using this form ([Registration form](http://xbcbank.com?ajb87u)) \n'
			elif(receiver_name.upper()== "PETER"):
				result='Insufficient funds to complete the transfer \n'
			elif(receiver_name.upper()=="RAM"):
				result=f"Amount ${amount} transferred successfully to {receiver_name}, I see that you make this transaction every month, you want me to add this as a recurring payment? \n"
			else:
				result= f'Amount ${amount} transferred successfully to {receiver_name}! \n'

		elif(service_type.upper() == "SUBSCRIBE"):
			for service in subscription_services:
				if(service.upper()==service_name.upper()):
					found_match=True

			if (found_match):
				result="Subsription completed successfully! \n"
			else:
				result=f"I am afraid we do not offer {service_name} as a service, can you please verify if you are requesting a valid banking services? \n"

		elif(service_type.upper() == "ADD"):

			for user in user_names :
				if(user.upper() == user_name.upper()):	
					found_match=True
			if(found_match):
				result=f"I see that {user_name} is a valid user and can be added to your account. Can you authorize the completed registration form ([Authorization form](http://xbcbank.com?uiue)) for me to complete the request? \n"
			else:
				result=f"The user {user_name} is not eligible for this service, Can you please check and reach out to bank for further assistance! \n"

		elif(service_type.upper() == "REMOVE"):
			found_match=False

			for user in user_names :
				if(user.upper() == user_name.upper()):
					found_match=True
			if(found_match):
				result=f"The user {user_name} removed successfully from your account! \n"
			else:
				result= f'The user {user_name} is not registered for this service, Can you please check and reach out to bank for further assistance! \n'			
			
		
		else:
			result="Invalid request, can you please explain what you are looking for? \n"


			

		return jsonify(
        	#servicetype=service_type,
            #sender=sender_name,
            #receiver=receiver_name,
            #amount=amount,
			#service=service_name,
			result=result
            )

is_noun = lambda pos: pos[:2] == 'NN'
is_verb = lambda pos: pos[:2] == 'VB'

class ProcessUserPromptWithNLP(Resource):

    def get(self):
        user_prompt = str(request.args.get('prompt'))
        text = nltk.word_tokenize(user_prompt)
        nouns = [word for (word, pos) in nltk.pos_tag(text) if is_noun(pos)]
        verbs = [word for (word, pos) in nltk.pos_tag(text) if is_verb(pos)]
        

        result = nltk.pos_tag(text)
		
        return jsonify(
            outcome='success',
            input=user_prompt,
			nouns=nouns,
			verbs=verbs,
			result=result
        )

class ProcessUserPrompt(Resource):

	def get(self):
		#static variables
		amount=0.0
		service = ''
		receiver = ''
		user=''
		subscriptionservice=''
		subscription_services = ['credit report', 'mutual funds', 'financial consulting', 'retirement services']
		services = ['subscribe', 'transfer', 'add', 'remove']
		receiver_names = ['joseph', 'john', 'carole', 'peter', 'ram'] # used for both receiver name and user depednding on the service

        
		user_prompt = str(request.args.get('prompt').lower())
		index = -1

		for service_type in services:
			index = user_prompt.find(service_type)
			if (index > 0):
				service = service_type

        #used for receiver and user for this demo
		for receiver_name in receiver_names:
			index = user_prompt.find(receiver_name)
			if (index > 0):
				receiver = receiver_name
		
		for subscriptionservice_type in subscription_services:
			index = user_prompt.find(subscriptionservice_type)
			if (index > 0):
				subscriptionservice=subscriptionservice_type

			
		words = user_prompt.split()
		for word in words:
			if word.startswith('$'):
				amount=float(word.strip('$'))
          
		accountservices_url=f'http://127.0.0.1:5000/accountservice?servicetype={service}&sender=xu&receiver={receiver}&service={subscriptionservice}&user={receiver}&amount={amount}'
		result = requests.get(accountservices_url).json()
		return result
		

		#return jsonify(
		#	prompt=user_prompt,
		#	service=service,
		#	receiver=receiver,
		#	amount=amount,
		#	user=receiver,
		#	subscriptionservice=subscriptionservice,
		#	url=accountservices_url
		#)

# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(AccountService,'/accountservice')
api.add_resource(ProcessUserPromptWithNLP,'/processpmtnlp')
api.add_resource(ProcessUserPrompt,'/processuserpmt')

# driver function 
if __name__ == '__main__': 

	app.run(debug = True) 

