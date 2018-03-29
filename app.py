from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Assuming dbs is in your app root folder
fixtures = create_engine('sqlite:///Fixtures.db')
app = Flask(__name__)
api = Api(app)

class LeagueList(Resource):
    def get(self):
        conn = fixtures.connect()
        query = conn.execute('select "Code" from Leagues')
        resultset = {'Leagues': [i[0] for i in query.cursor.fetchall()]}
        return resultset

class Fixtures(Resource):
    def get(self,leagueCode):
        conn = fixtures.connect()
        query = conn.execute("select Date, HomeTeam, AwayTeam From '%s'"%leagueCode)
        return query.cursor.fetchall()

# Routes
api.add_resource(LeagueList,'/leagues')
api.add_resource(Fixtures,'/fixture/<string:leagueCode>')

if __name__ == '__main__':
    app.run(debug=True)
