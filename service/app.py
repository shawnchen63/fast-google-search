from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from model_api import get_results

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "ML React App", 
		  description = "Predict results using a trained model")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params', 
				  {'textField1': fields.String(required = True, 
				  							   description="Text Field 1", 
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = False, 
				  							   description="Text Field 2", 
    					  				 	   help="Text Field 2 cannot be blank"),
				  'select1': fields.Integer(required = False, 
				  							description="Select 1", 
    					  				 	help="Select 1 cannot be blank"),
				  'select2': fields.Integer(required = False, 
				  							description="Select 2", 
    					  				 	help="Select 2 cannot be blank"),
				  'select3': fields.Integer(required = False, 
				  							description="Select 3", 
    					  				 	help="Select 3 cannot be blank")})

# classifier = joblib.load('classifier.joblib')

@name_space.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)		
	def post(self):
		try: 
			formData = request.json
			data = [val for val in formData.values()]
			pos,neu,neg = get_results(data[0])
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"pos_result": {
					"rate" : f"Positive: {pos[0]*100:.2f}%",
					"title" : pos[1],
					"link" : pos[2]
					},
				"neu_result": {
					"rate" : f"Neutral: {neu[0]*100:.2f}%",
					"title" : neu[1],
					"link" : neu[2]
					},
				"neg_result": {
					"rate" : f"Negative: {neg[0]*100:.2f}%",
					"title" : neg[1],
					"link" : neg[2]
					}
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})