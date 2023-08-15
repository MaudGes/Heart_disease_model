# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:23:38 2023

@author: maudg
"""

from flask import Flask, request
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask('heart_diseases_api')
api = Api(app)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '****'
app.config['MYSQL_DB'] = 'heart_diseases_data'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

class CreatePerson(Resource):
    def post(self):
        try:
            conn = mysql.connection
            cursor = conn.cursor()

            # Extract data from request
            data = request.get_json()
            
            # Insert user data into the table
            user_data = {
                'highbp': data['highbp'],
                'highchol': data['highchol'],
                'cholcheck': data['cholcheck'],
                'bmi': data['bmi'],
                'smoker': data['smoker'],
                'stroke': data['stroke'],
                'diabetes': data['diabetes'],
                'physactivity': data['physactivity'],
                'fruits' : data['fruits'],
                'veggies' : data['veggies'],
                'hvyalcohol' : data['hvyalcohol'],
                'any_healthcare' : data['any_healthcare'],
                'no_doc_cost' : data['no_doc_cost'],
                'genhlth' : data['genhlth'],
                'menthlth': data['menthlth'],
                'physhlth': data['physhlth'],
                'diffwalk': data['diffwalk'],
                'sex': data['sex'],
                'age': data['age'],
                'education': data['education'],
                'income': data['income']
            }

            # Insert user data into the table
            query = """
                INSERT INTO heart_disease_table (
                    highbp, highchol, cholcheck, bmi,
                    smoker, stroke, diabetes, physactivity,
                    fruits, veggies, hvyalcohol, any_healthcare,
                    no_doc_cost, genhlth, menthlth,physhlth,diffwalk,
                    sex,age,education,income
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            values = (
                user_data['highbp'], user_data['highchol'], user_data['cholcheck'],
                user_data['bmi'], user_data['smoker'], user_data['stroke'], user_data['diabetes'],
                user_data['physactivity'], user_data['fruits'], user_data['veggies'], user_data['hvyalcohol'],
                user_data['any_healthcare'], user_data['no_doc_cost'], user_data['genhlth'], user_data['menthlth'],user_data['physhlth'],
                user_data['diffwalk'],user_data['sex'], user_data['age'], user_data['education'], user_data['income']
            )
            
            cursor.execute(query, values)

            # Commit the changes and close the connection
            conn.commit()
            cursor.close()

            return {'message': 'User data inserted successfully'}

        except Exception as e:
            return {'error': str(e)}
        
        '''Insérer ici le fait d'envoyer aussi les valeurs au modèle ?'''

class GetPerson(Resource):
    def get(self, user_id):
        try:
            conn = mysql.connection
            cursor = conn.cursor()

            # Fetch user data from heart_disease_table
            query = "SELECT * FROM heart_disease_table WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()

            # Close the connection
            cursor.close()

            if user_data:
                column_names = ['id','hda','highbp','highchol','cholcheck', 'bmi', 'smoker', 'stroke','diabetes','physactivity','fruits',
                                'veggies','hvyalcohol','any_healthcare', 'no_doc_cost','genhlth','menhlth','physhlth','diffwalk','sex',
                                'age','education','income']
                return {column_names[i]: user_data[i] for i in range(len(column_names))}
            else:
                return {'message': 'User not found'}

        except Exception as e:
            return {'error': str(e)}
           
            
           
class DeletePerson(Resource):
    def delete(self, user_id):
        try:
            conn = mysql.connection
            cursor = conn.cursor()
            
            query = "DELETE FROM heart_disease_table WHERE id = %s"
            cursor.execute(query, (user_id,))
            
            # Commit the changes and close the connection
            conn.commit()
            cursor.close()

            return {'message': 'User deleted successfully'}

        except Exception as e:
            return {'error': str(e)}
        
        
        
class UpdatePerson(Resource):
    def put(self, user_id):
        try:
            conn = mysql.connection
            cursor = conn.cursor()

            # Extract data from the request
            data = request.get_json()

            # Build the SET clause for the SQL query
            set_clause = ", ".join([f"{column} = %s" for column in data.keys()])

            # Build the values for the SQL query
            values = tuple(data.values()) + (user_id,)

            # Update user data in the table
            query = f"UPDATE heart_disease_table SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)

            # Commit the changes and close the connection
            conn.commit()
            cursor.close()

            return {'message': 'User data updated successfully'}

        except Exception as e:
            return {'error': str(e)}
            

api.add_resource(CreatePerson, '/CreatePerson')
api.add_resource(DeletePerson, '/DeletePerson/<int:user_id>')
api.add_resource(GetPerson, '/GetPerson/<int:user_id>')
api.add_resource(UpdatePerson, '/UpdatePerson/<int:user_id>')



if __name__ == '__main__':
    app.run()